#!/usr/bin/env python3
"""Translate collected Markdown into Simplified Chinese, with resumable caching."""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import threading
import time

import requests

ROOT = Path(__file__).resolve().parent
VERSION = 'google-zh-CN-v5'
FORMAT_VERSION = 2
CHINESE_TITLES = {
 'Context Engineering (Agent Memory) for AI Agents Starts with Retrieval':'智能体上下文工程（智能体记忆）从检索开始',
 'Context Engineering with Deep Agents: How To Remember Without Keeping Everything In Context':'Deep Agents 上下文工程：如何在不把一切塞进上下文的情况下保留记忆',
 'Continuous Context Management':'持续上下文管理',
 'MemAgent: Learning to Manage Heterogeneous Memory Providers for LLM Agents':'MemAgent：学习为大语言模型智能体管理异构记忆系统',
 'Towards Reliable Context Compression for Long-Horizon Agents: An Empirical Study of Execution Instability':'迈向长程智能体的可靠上下文压缩：执行不稳定性的实证研究',
 'DTOC: Dynamic Tool Output Compression for Adaptive Context Management in AI Agents':'DTOC：面向 AI 智能体自适应上下文管理的动态工具输出压缩',
 'ACM: Agentic Context Management for Long Horizon Tasks':'ACM：面向长程任务的智能体上下文管理',
 'Agentic Context Management: Solving Agent Memory and Cost by Treating Them as Lifecycle and Architecture Problems':'智能体上下文管理：从生命周期与架构视角解决智能体记忆和成本问题',
 'MemRefine: LLM-Guided Compression for Long-Term Agent Memory':'MemRefine：大语言模型引导的智能体长期记忆压缩',
 'LongMemEval-V2: Evaluating Long-Term Agent Memory Toward Experienced Colleagues':'LongMemEval-V2：评估智能体长期记忆，迈向经验丰富的协作伙伴',
 'ReasoningBank: Enabling agents to learn from experience':'ReasoningBank：让智能体从经验中学习',
 'Context Engineering: From Prompts to Corporate Multi-Agent Architecture':'上下文工程：从提示词到企业多智能体架构',
 'Memory for Autonomous LLM Agents:Mechanisms, Evaluation, and Emerging Frontiers':'自主大语言模型智能体的记忆：机制、评估与新兴前沿',
 'Active Context Compression: Autonomous Memory Management in LLM Agents':'主动上下文压缩：大语言模型智能体的自主记忆管理',
 'Context Engineering for AI Agents: Part 2':'AI 智能体上下文工程：第二部分',
 'Effective harnesses for long-running agents':'为长时间运行的智能体构建有效的运行框架',
 'Introducing advanced tool use for Claude':'Claude 高级工具使用能力介绍',
 'Code execution with MCP for efficient agents':'通过 MCP 执行代码，构建高效智能体',
 'Equipping agents with Agent Skills':'用 Agent Skills 为智能体赋予技能',
 'Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models':'智能体上下文工程：通过演化上下文实现语言模型自我改进',
 'ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory':'ReasoningBank：借助推理记忆扩展智能体的自我演化能力',
 'Effective context engineering for AI agents':'AI 智能体的高效上下文工程',
 'ReSum: Unlocking Long-Horizon Search Intelligence via Context Summarization':'ReSum：通过上下文摘要释放长程搜索智能',
 'Context Engineering for AI Agents: Lessons from Building Manus':'AI 智能体上下文工程：构建 Manus 的经验',
 'A Survey of Context Engineering for Large Language Models':'大语言模型上下文工程综述',
 'MemOS: A Memory OS for AI System':'MemOS：面向 AI 系统的记忆操作系统',
 'MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent':'MemAgent：通过基于多轮对话强化学习的记忆智能体重塑长上下文大语言模型',
 'Context Engineering':'上下文工程',
 'How we built our multi-agent research system':'我们如何构建多智能体研究系统',
 'Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory':'Mem0：利用可扩展长期记忆构建可用于生产环境的 AI 智能体',
 'Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory':'动态速查表：利用自适应记忆进行测试时学习',
 'A-MEM: Agentic Memory for LLM Agents':'A-MEM：面向大语言模型智能体的能动式记忆',
 'On the Structural Memory of LLM Agents':'论大语言模型智能体的结构化记忆',
}
GLOSSARY = {
    'context engineering': '上下文工程', 'context management': '上下文管理',
    'context compression': '上下文压缩', 'context window': '上下文窗口',
    'context windows': '上下文窗口', 'context rot': '上下文退化',
    'long-term memory': '长期记忆', 'short-term memory': '短期记忆',
    'working memory': '工作记忆', 'episodic memory': '情景记忆',
    'semantic memory': '语义记忆', 'procedural memory': '程序性记忆',
    'retrieval-augmented generation': '检索增强生成',
    'large language models': '大语言模型', 'large language model': '大语言模型',
    'reinforcement learning': '强化学习', 'multi-agent': '多智能体',
    'tool calls': '工具调用', 'tool call': '工具调用',
    'tool outputs': '工具输出', 'tool output': '工具输出',
    'compaction': '压缩整合', 'agents': '智能体', 'agent': '智能体',
    'contexts': '上下文', 'context': '上下文', 'tokens': '词元', 'token': '词元',
}
TERMS = re.compile(r'\b(?:'+'|'.join(re.escape(x) for x in sorted(GLOSSARY,key=len,reverse=True))+r')\b',re.I)
PLACEHOLDER = re.compile(r'⟦P\d{6}⟧')
# Preserve fenced/inline code, LaTeX math, URLs, HTML tags and Markdown destinations.
PROTECTED = re.compile(
    r'(?ms)^(`{3,}|~{3,})[^\n]*\n.*?^\1[^\n]*(?:\n|$)'
    r'|`+[^`\n]+`+'
    r'|\$\$.*?\$\$|(?<!\$)\$(?!\$)[^$\n]+\$(?!\$)'
    r'|\\\[.*?\\\]|\\\(.*?\\\)'
    r'|(?m:^\|[^\n]*\\[^\n]*\|[ \t]*$)'
    r'|[^\s|]*\\(?:[A-Za-z]+|_)[^\s|]*'
    r'|https?://[^\s<>\[\]()"\']+'
    r'|<[^>\n]+>'
    r'|\b(?:Claude (?:Sonnet|Opus|Haiku) [\d.]+|Qwen[\w.-]+|GPT-[\w.-]+|GLM-[\w.-]+|Kimi K\d+|TerminalBench-\d|Terminal-Bench [\d.]+|WebShop|Endless Terminals)\b'
    r'|(?m:^- (?:来源|发布日期|日期依据|类型|主题|抓取状态|正文来源|抓取时间 UTC|作者|说明):[^\n]*$)'
)
LOCAL = threading.local()
PRINT_LOCK = threading.Lock()
REQUEST_LOCK = threading.Lock()
NEXT_REQUEST = 0.0
REQUEST_DELAY = 1.5


class PreservationError(ValueError):
    pass


def log(message):
    with PRINT_LOCK:
        print(message, flush=True)


def wait_for_request():
    global NEXT_REQUEST
    while True:
        with REQUEST_LOCK:
            wait = NEXT_REQUEST-time.monotonic()
            if wait <= 0:
                NEXT_REQUEST = time.monotonic()+REQUEST_DELAY
                return
        time.sleep(min(wait,10))


def cool_down(seconds):
    global NEXT_REQUEST
    with REQUEST_LOCK:
        NEXT_REQUEST = max(NEXT_REQUEST,time.monotonic()+seconds)


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def protect(text):
    mapping = {}
    def put(value):
        key = f'⟦P{len(mapping):06d}⟧'
        mapping[key] = value
        return key
    text = PROTECTED.sub(lambda m: put(m.group()), text)
    return text, mapping


def reflow(text):
    paragraphs = re.split(r'(\n[ \t]*\n)',text)
    result = []
    for block in paragraphs:
        lines = block.splitlines()
        if len(lines)>1 and not any(re.match(r'^\s*(?:[|#>*]|[-+]\s|\d+[.)]\s)',line) for line in lines):
            block = re.sub(r'(?<=\S)\n(?=\S)', ' ', block)
        result.append(block)
    return ''.join(result)


def repair_markdown(text):
    # Translation engines sometimes replace Markdown's ASCII title quotes or parentheses.
    # Optional link titles can be omitted without losing the link label or destination.
    text = re.sub(r'\]（\s*(?=https?://)', '](', text)
    text = re.sub(r'(\]\(https?://[^\s"“”）)]+)[ \t]*["“][^\n"”]*["”][ \t]*[)）]', r'\1)', text)
    text = re.sub(r'(\]\(https?://[^\s）)]+)）', r'\1)', text)
    text = re.sub(r'(?m)^[ \t]*\*[ \t]*•[ \t]*\n[ \t]*\n[ \t]*', '- ', text)
    return text


def split_text(text, limit):
    # Keep paragraphs together where possible; split long paragraphs only at whitespace.
    units = re.split(r'(\n\s*\n)', text)
    chunks, buf = [], ''
    for unit in units:
        while unit:
            remaining = limit-len(buf)
            if len(unit) <= remaining:
                buf += unit
                break
            if buf:
                chunks.append(buf)
                buf = ''
                continue
            cut = max(unit.rfind('\n',0,limit), unit.rfind(' ',0,limit))
            if cut < limit//3:
                cut = limit
            # Never cut a placeholder in half.
            for match in PLACEHOLDER.finditer(unit):
                if match.start() < cut < match.end():
                    cut = match.start()
                    break
            chunks.append(unit[:cut])
            unit = unit[cut:]
    if buf:
        chunks.append(buf)
    assert ''.join(chunks) == text
    return chunks


def translate_chunk(source, cache, attempts=5):
    if not re.search(r'[A-Za-z]{2}', PLACEHOLDER.sub('',source)):
        return source, False
    digest = sha(VERSION+'\n'+source)
    target = cache/(digest+'.json')
    if target.exists():
        stored = json.loads(target.read_text())
        if stored.get('source_sha256') == sha(source):
            return stored['translation'], True
    session = getattr(LOCAL,'session',None)
    if session is None:
        LOCAL.session = session = requests.Session()
        session.headers['User-Agent'] = 'ContextReadingTranslation/1.0'
    expected = Counter(PLACEHOLDER.findall(source))
    last = None
    for attempt in range(attempts):
        try:
            wait_for_request()
            response = session.get('https://translate.googleapis.com/translate_a/single',
                params={'client':'gtx','sl':'en','tl':'zh-CN','dt':'t','q':source}, timeout=(15,60))
            if response.status_code==429:
                retry_after = response.headers.get('Retry-After','120')
                seconds = int(retry_after) if retry_after.isdigit() else 120
                cool_down(seconds)
                log(f'Translation rate limit: cooling down {seconds}s; cached progress retained')
            if response.status_code>=400:
                raise requests.HTTPError(f'Translation service HTTP {response.status_code}',response=response)
            payload = response.json()
            result = ''.join(row[0] for row in payload[0] if row and row[0])
            # Preserve boundary whitespace across chunk joins.
            result = source[:len(source)-len(source.lstrip())]+result.strip()+source[len(source.rstrip()):]
            if Counter(PLACEHOLDER.findall(result)) != expected:
                raise PreservationError('Protected code/link/formula/term placeholder mismatch')
            if not result.strip() or (len(source)>200 and len(result)<len(source)*0.15):
                raise ValueError('Translation empty or suspiciously truncated')
            if re.search(r'[A-Za-z]{30}', PLACEHOLDER.sub('',source)) is None and len(re.findall(r'[A-Za-z]',PLACEHOLDER.sub('',source)))>100:
                if not re.search(r'[\u4e00-\u9fff]',result):
                    raise ValueError('No Chinese translation returned')
            target.write_text(json.dumps({'source_sha256':sha(source),'translation':result},ensure_ascii=False))
            time.sleep(0.25)
            return result, False
        except PreservationError:
            if len(source) < 500:
                # An isolated protected span is copied, never sent for translation.
                # This fallback also handles engines dropping a trailing inline formula.
                pieces = re.split(r'(⟦P\d{6}⟧)',source)
            else:
                pieces = split_text(source,max(250,len(source)//2))
            result = ''.join(translate_chunk(piece,cache,attempts)[0] for piece in pieces)
            if Counter(PLACEHOLDER.findall(result)) != expected:
                raise
            target.write_text(json.dumps({'source_sha256':sha(source),'translation':result},ensure_ascii=False))
            return result, False
        except (requests.RequestException, ValueError, TypeError, IndexError) as exc:
            last = f'{type(exc).__name__}: {exc}'
            if attempt+1 < attempts:
                time.sleep(min(30,2**(attempt+1)))
    raise RuntimeError(last)


def process(record, args):
    source_path = args.source/record['file']
    original = source_path.read_text()
    output = args.output/record['file']
    metadata = output.with_suffix('.translation.json')
    source_hash = sha(original)
    if output.exists() and metadata.exists():
        prior = json.loads(metadata.read_text())
        if prior.get('source_sha256') == source_hash and prior.get('engine') == VERSION and prior.get('format_version')==FORMAT_VERSION:
            return prior
    protected, mapping = protect(original)
    protected = reflow(protected)
    chunks = split_text(protected,args.chunk_size)
    translated = []
    log(f"START {record['title']} ({len(chunks)} chunks)")
    for index, chunk in enumerate(chunks,1):
        text, cached = translate_chunk(chunk,args.cache)
        translated.append(text)
        if index % 5 == 0 or index == len(chunks):
            log(f"  {record['file'].split('/')[-1][:62]}: {index}/{len(chunks)}"+(' [cache]' if cached else ''))
    result = ''.join(translated)
    assert Counter(PLACEHOLDER.findall(result)) == Counter(PLACEHOLDER.findall(protected))
    # Normalize technical vocabulary only outside protected source spans.
    result = TERMS.sub(lambda m:GLOSSARY[m.group().lower()],result)
    for source_term, target_term in [('情境工程','上下文工程'),('上下文工程学','上下文工程'),
        ('代理人','智能体'),('代理','智能体'),('安全带','运行框架'),('线束','运行框架'),('令牌','词元'),
        ('代币','词元'),('智能体内存','智能体记忆'),('长期内存','长期记忆'),
        ('短期内存','短期记忆'),('深层特工','Deep Agents'),('深度智能体','Deep Agents'),('Deep 智能体','Deep Agents'),
        ('开放重量模型','开放权重模型'),('开放权重的模型','开放权重模型'),('长视野','长程'),
        ('冷冻副本','冻结副本'),('每次转动','每个回合'),('更新的内存','更新的记忆'),('保留的内存','保留的记忆')]:
        result = result.replace(source_term,target_term)
    result = re.sub(r'\]（(?=⟦P)','](',result)
    result = re.sub(r'(⟦P\d{6}⟧)）',r'\1)',result)
    result = PLACEHOLDER.sub(lambda m:mapping[m.group()],result)
    chinese_title = CHINESE_TITLES.get(record['title'])
    if chinese_title:
        result = re.sub(r'^#\s+[^\n]+',lambda m:'# '+chinese_title,result,count=1,flags=re.M)
    result = result.replace('## 摘要正文','## 抓取正文（中文翻译）')
    result = repair_markdown(result)
    relative = os.path.relpath(source_path,output.parent)
    banner = ('> 本文为简体中文机器翻译，使用 Google Translate 公开接口并统一技术术语，尚未经逐句人工校对。'
              '代码、链接和公式按原文保留；实验数字及技术结论请对照原文。\n'
              f'> [查看本地英文原文]({relative}) · [原始来源]({record["url"]})\n\n')
    if record['status']=='abstract_only':
        banner += '> 原始资料仅抓取到摘要，本文件也仅翻译已保存的摘要，不是论文全文。\n\n'
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(banner+result+'\n')
    title_match = re.search(r'^#\s+(.+)$',result,re.M)
    info = {'source_file':record['file'],'file':record['file'],'source_sha256':source_hash,
            'output_sha256':sha(banner+result+'\n'),'title':title_match.group(1) if title_match else record['title'],
            'original_title':record['title'],'kind':record['kind'],'date':record['date'],
            'source_status':record['status'],'url':record['url'],'chunks':len(chunks),
            'protected_spans':len(mapping),'source_characters':len(original),
            'translated_characters':len(result),'engine':VERSION,'format_version':FORMAT_VERSION,
            'completed_at':datetime.now(timezone.utc).isoformat()}
    metadata.write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
    log(f"DONE {record['title']}")
    return info


def write_index(args, complete, failures, count):
    complete.sort(key=lambda r:(r['date'],r['original_title']),reverse=True)
    manifest = {'engine':VERSION,'total_sources':count,'completed':len(complete),
                'items':complete,'failures':failures,'generated_at':datetime.now(timezone.utc).isoformat()}
    (args.output/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    lines = ['# Agent 上下文管理中文资料索引\n',f'中文译文：{len(complete)}/{count} 篇。\n',
             '全部译文为简体中文机器翻译，未经逐句人工审校；代码、链接、公式和作者姓名保留原文。原始资料中仅有摘要的条目也只翻译摘要。\n',
             '[英文原文索引](../collection/INDEX.md)\n',
             '| 日期 | 类型 | 中文标题 | 原文范围 |','|---|---|---|---|']
    for r in complete:
        title = r['title'].replace('|','\\|')
        lines.append(f"| {r['date']} | {'论文' if r['kind']=='paper' else '博客'} | [{title}]({r['file']}) | {'仅摘要' if r['source_status']=='abstract_only' else '已抓取正文'} |")
    lines.append('\n## 未完成条目\n')
    lines.extend('- '+x['title']+'：'+x['error'] for x in failures)
    if not failures and len(complete)==count:
        lines.append('无，所有已爬取资料均已翻译。')
    (args.output/'INDEX.md').write_text('\n'.join(lines)+'\n')


def main():
    global REQUEST_DELAY
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=ROOT/'collection')
    parser.add_argument('--output',type=Path,default=ROOT/'collection_zh')
    parser.add_argument('--cache',type=Path,default=ROOT/'.translation_cache')
    parser.add_argument('--workers',type=int,default=3)
    parser.add_argument('--chunk-size',type=int,default=3200)
    parser.add_argument('--limit',type=int,default=0)
    parser.add_argument('--request-delay',type=float,default=1.5)
    parser.add_argument('--cooldown',type=float,default=0)
    args = parser.parse_args()
    REQUEST_DELAY = max(0.5,args.request_delay)
    if args.cooldown:
        cool_down(args.cooldown)
    if not 500 <= args.chunk_size <= 4000 or not 1 <= args.workers <= 4:
        parser.error('chunk-size must be 500..4000; workers must be 1..4')
    if args.source.resolve()==args.output.resolve():
        parser.error('output must differ from source')
    args.output.mkdir(parents=True,exist_ok=True)
    args.cache.mkdir(parents=True,exist_ok=True)
    records = json.loads((args.source/'manifest.json').read_text())['items']
    if args.limit:
        records = records[:args.limit]
    complete, failures = [], []
    write_index(args,complete,failures,len(records))
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        pending = {executor.submit(process,row,args):row for row in records}
        for future in as_completed(pending):
            row = pending[future]
            try:
                complete.append(future.result())
            except Exception as exc:
                failures.append({'title':row['title'],'file':row['file'],'error':str(exc)})
                log(f"FAILED {row['title']}: {exc}")
            write_index(args,complete,failures,len(records))
    for item in complete:
        path = args.output/item['file']
        before = path.read_text()
        after = repair_markdown(before)
        if after != before:
            path.write_text(after)
            item['output_sha256'] = sha(after)
            path.with_suffix('.translation.json').write_text(json.dumps(item,ensure_ascii=False,indent=2)+'\n')
    write_index(args,complete,failures,len(records))
    log(f'Translated {len(complete)}/{len(records)}. Failures: {len(failures)}')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
