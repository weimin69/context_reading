#!/usr/bin/env python3
"""Download dated agent-context papers/blogs as Markdown; no API key required."""
from __future__ import annotations

import argparse
import calendar
import hashlib
import json
import re
import time
import xml.etree.ElementTree as ET
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT = Path(__file__).resolve().parent
UA = 'ContextReadingResearchBot/1.0 (personal academic reading; requests)'
TERMS = ['context engineering', 'context management', 'context compression',
         'agent memory', 'agentic memory', 'long-term memory']


def two_years_before(d):
    return d.replace(year=d.year-2, day=min(d.day, calendar.monthrange(d.year-2, d.month)[1]))


def iso_date(value):
    if not value:
        return None
    match = re.search(r'\d{4}-\d{2}-\d{2}', str(value))
    if match:
        return date.fromisoformat(match.group())
    for fmt in ('%b %d %Y', '%B %d %Y', '%B %d, %Y', '%Y/%m/%d'):
        try:
            return datetime.strptime(str(value).strip(), fmt).date()
        except ValueError:
            pass
    return None


class Crawler:
    def __init__(self, delay=1.5, timeout=35):
        self.session = requests.Session()
        self.session.headers['User-Agent'] = UA
        # Do not block for hours on Retry-After; record rate limits and retry on a later run.
        retry = Retry(total=0)
        self.session.mount('https://', HTTPAdapter(max_retries=retry))
        self.delay, self.timeout = delay, timeout
        self.last, self.robots = {}, {}

    def raw(self, url):
        host = urlparse(url).netloc
        base = f'{urlparse(url).scheme}://{host}'
        rp = self.robots.get(base)
        delay = max(self.delay, (rp.crawl_delay(UA) or 0) if rp else 0)
        time.sleep(max(0, delay - (time.monotonic() - self.last.get(host, 0))))
        try:
            response = self.session.get(url, timeout=self.timeout, stream=True)
            response.raise_for_status()
            chunks, size, began = [], 0, time.monotonic()
            try:
                for chunk in response.iter_content(8192):
                    size += len(chunk)
                    if size > 30_000_000 or time.monotonic() - began > 90:
                        raise ValueError('Response exceeds 30 MB or 90-second body download budget')
                    chunks.append(chunk)
                response._content = b''.join(chunks)
                response._content_consumed = True
            finally:
                response.close()
            return response
        finally:
            self.last[host] = time.monotonic()

    def get(self, url):
        parsed = urlparse(url)
        base = f'{parsed.scheme}://{parsed.netloc}'
        if base not in self.robots:
            rp = RobotFileParser()
            response = self.session.get(base+'/robots.txt', timeout=self.timeout)
            if response.status_code == 404:
                rp.parse([])
            else:
                response.raise_for_status()
                rp.parse(response.text.splitlines())
            self.robots[base] = rp
        if not self.robots[base].can_fetch(UA, url):
            raise PermissionError('Disallowed by robots.txt')
        return self.raw(url)


def meta(soup, name):
    item = soup.find('meta', attrs={'name': name}) or soup.find('meta', attrs={'property': name})
    return item.get('content', '') if item else ''


def page_date(soup):
    for key in ('citation_date', 'citation_publication_date', 'article:published_time', 'date', 'datePublished'):
        found = iso_date(meta(soup, key))
        if found:
            return found, 'page metadata: '+key
    for script in soup.select('script[type="application/ld+json"]'):
        try:
            obj = json.loads(script.string or script.get_text())
        except (ValueError, TypeError):
            continue
        stack = [obj]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                if iso_date(node.get('datePublished')):
                    return iso_date(node['datePublished']), 'JSON-LD datePublished'
                stack.extend(node.values())
            elif isinstance(node, list):
                stack.extend(node)
    for node in soup.select('time'):
        found = iso_date(node.get('datetime') or node.get_text(' ', strip=True))
        if found:
            return found, 'page time element'
    return None, None


def to_md(node, url):
    for item in list(node.select('script, style, nav, footer, header, noscript, button, form, .ltx_bibliography')):
        item.decompose()
    for item in list(node.select('img[src*="fetch_website_favicon"]')):
        item.decompose()
    for item in node.select('[href], [src]'):
        for attr in ('href', 'src'):
            if item.get(attr):
                item[attr] = urljoin(url, item[attr])
    return re.sub(r'\n{3,}', '\n\n', markdownify(str(node), heading_style='ATX')).strip()


def discover(crawler, start, end, limit):
    query = '('+' OR '.join(f'all:"{t}"' for t in TERMS)+') AND (all:agent OR all:agentic)'
    query += f' AND submittedDate:[{start:%Y%m%d}0000 TO {end:%Y%m%d}2359]'
    url = 'https://export.arxiv.org/api/query?'+requests.compat.urlencode({
        'search_query': query, 'start': 0, 'max_results': limit,
        'sortBy': 'submittedDate', 'sortOrder': 'descending'})
    root = ET.fromstring(crawler.get(url).content)
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    found = []
    for entry in root.findall('a:entry', ns):
        link = entry.findtext('a:id', '', ns).replace('http://', 'https://')
        if '/abs/' in link:
            found.append({'url': re.sub(r'v\d+$', '', link), 'kind': 'paper',
                          'topics': ['自动检索，待人工精读'], 'discovered_by': url})
    return found


def collect(crawler, seed, start, end):
    url = seed['url']
    soup = BeautifulSoup(crawler.get(url).content, 'html.parser')
    title = meta(soup, 'citation_title') or meta(soup, 'og:title')
    if not title:
        title = (soup.h1 or soup.title).get_text(' ', strip=True)
    published, basis = page_date(soup)
    if seed['kind'] == 'paper' and 'arxiv.org/abs/' in url:
        history = soup.select_one('.submission-history')
        if history:
            text = history.get_text(' ', strip=True)
            first = re.search(r'\[v1\]\s*(\d{1,2} [A-Za-z]+ \d{4})', text)
            if first:
                published = datetime.strptime(first.group(1), '%d %b %Y').date()
                basis = 'arXiv v1 submission date'
    if not published and seed.get('date'):
        published, basis = iso_date(seed['date']), 'curated source date (verified from source/search)'
    if not published:
        raise ValueError('No verifiable publication date; not included')
    if not start <= published <= end:
        return {'url': url, 'status': 'outside_date_range', 'date': str(published), 'title': title}
    authors = [x.get('content') for x in soup.select('meta[name="citation_author"]')]
    abstract = soup.select_one('blockquote.abstract')
    description = abstract.get_text(' ', strip=True) if abstract else meta(soup, 'description') or meta(soup, 'og:description')
    content_url, notes = url, []
    if seed['kind'] == 'paper':
        aid = url.rsplit('/', 1)[-1]
        content_url = 'https://arxiv.org/html/'+aid
        try:
            full = BeautifulSoup(crawler.get(content_url).content, 'html.parser')
            node = full.select_one('article.ltx_document') or full.select_one('main') or full.select_one('article')
            if not node or len(node.get_text()) < 3000:
                raise ValueError('Full-text HTML missing or too short')
            body, status = to_md(node, content_url), 'full_text_html'
        except Exception as exc:
            body, status, content_url = description, 'abstract_only', url
            notes.append(f'HTML full text unavailable: {type(exc).__name__}: {exc}')
    else:
        node = soup.select_one('article') or soup.select_one('main')
        if not node:
            raise ValueError('No article/main body; refusing to save navigation as article')
        body, status = to_md(node, url), 'article_html'
        if len(body) < 800:
            raise ValueError('Article too short or requires JavaScript')
    record = {**seed, 'title': title, 'date': str(published), 'date_basis': basis,
              'authors': authors, 'status': status, 'content_url': content_url,
              'retrieved_at': datetime.now(timezone.utc).isoformat(),
              'characters': len(body), 'notes': notes}
    digest = hashlib.sha256(url.encode()).hexdigest()[:8]
    slug = re.sub(r'[^\w-]+', '-', title, flags=re.UNICODE).strip('-')[:100]
    record['file'] = f"{seed['kind']}s/{published}-{slug}-{digest}.md"
    header = '\n'.join(f'- {key}: {value}' for key, value in [
        ('来源', url), ('发布日期', published), ('日期依据', basis),
        ('类型', seed['kind']), ('主题', '、'.join(seed.get('topics', []))),
        ('抓取状态', status), ('正文来源', content_url), ('抓取时间 UTC', record['retrieved_at'])])
    if authors:
        header += '\n- 作者: '+', '.join(authors)
    if notes:
        header += '\n- 说明: '+'; '.join(notes)
    intro = seed.get('note', '')
    document = f'# {title}\n\n{header}\n\n'
    if intro:
        document += f'## 阅读提示（人工整理）\n\n{intro}\n\n'
    if description and status != 'abstract_only':
        document += f'## 来源摘要 / 页面简介\n\n{description}\n\n'
    document += ('## 原文摘要（非全文）' if status == 'abstract_only' else '## 抓取正文')+'\n\n'+body+'\n'
    return record, document


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--end', type=date.fromisoformat, default=date.today())
    parser.add_argument('--start', type=date.fromisoformat)
    parser.add_argument('--output', type=Path, default=ROOT/'collection')
    parser.add_argument('--seeds', type=Path, default=ROOT/'sources.json')
    parser.add_argument('--discover', type=int, default=0, help='Additional recent arXiv papers (0 disables)')
    parser.add_argument('--delay', type=float, default=1.5)
    parser.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    start = args.start or two_years_before(args.end)
    if start > args.end or args.delay < 0:
        parser.error('invalid date range or delay')
    args.output.mkdir(parents=True, exist_ok=True)
    crawler = Crawler(args.delay)
    seeds = json.loads(args.seeds.read_text())
    logs, records = [], []
    old_file = args.output/'manifest.json'
    old = {x['url']: x for x in json.loads(old_file.read_text()).get('items', [])} if old_file.exists() else {}
    if args.discover:
        try:
            seeds.extend(discover(crawler, start, args.end, args.discover))
        except Exception as exc:
            logs.append({'stage': 'discovery', 'error': str(exc)})
            print('Discovery failed:', exc, flush=True)
    unique = {seed['url'].rstrip('/'): seed for seed in seeds}
    for i, seed in enumerate(unique.values(), 1):
        url = seed['url']
        print(f'[{i}/{len(unique)}] {url}', flush=True)
        previous = old.get(url)
        if not args.refresh and previous and start <= date.fromisoformat(previous['date']) <= args.end and (args.output/previous['file']).exists():
            records.append(previous)
            continue
        try:
            result = collect(crawler, seed, start, args.end)
            if isinstance(result, dict):
                logs.append(result)
                continue
            record, document = result
            target = args.output/record['file']
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(document, encoding='utf-8')
            records.append(record)
            old_file.write_text(json.dumps({'start': str(start), 'end': str(args.end),
                'items': records, 'events': logs}, ensure_ascii=False, indent=2)+'\n')
            print(f"  {record['status']}: {record['characters']} chars", flush=True)
        except Exception as exc:
            logs.append({'url': url, 'status': 'failed', 'error': f'{type(exc).__name__}: {exc}'})
            print('  FAILED:', exc, flush=True)
    records.sort(key=lambda x: (x['date'], x['title']), reverse=True)
    manifest = {'start': str(start), 'end': str(args.end), 'items': records, 'events': logs,
                'generated_at': datetime.now(timezone.utc).isoformat()}
    old_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    lines = [f'# Agent 上下文管理资料索引\n', f'收录区间：{start} 至 {args.end}（含边界）。共 {len(records)} 篇。\n',
             '日期以首次发表为准；arXiv 使用 v1 日期。全文为自动 HTML 转换，公式、表格和图片可能有损失，请对照原链接。预印本不等于同行评审结论。\n',
             '状态：`full_text_html` = 论文 HTML 正文；`article_html` = 博客页面正文；`abstract_only` = 仅摘要。\n',
             '| 日期 | 类型 | 标题 | 主题 | 状态 |', '|---|---|---|---|---|']
    for row in records:
        title = row['title'].replace('|', '\\|')
        lines.append(f"| {row['date']} | {row['kind']} | [{title}]({row['file']}) | {'、'.join(row.get('topics', []))} | {row['status']} |")
    lines.extend(['\n## 未收录 / 抓取异常\n'])
    lines.extend('- '+json.dumps(event, ensure_ascii=False) for event in logs)
    if not logs:
        lines.append('无。')
    (args.output/'INDEX.md').write_text('\n'.join(lines)+'\n')
    print(f'Saved {len(records)} articles; {len(logs)} events. Index: {args.output / "INDEX.md"}', flush=True)


if __name__ == '__main__':
    main()
