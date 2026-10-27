#!/usr/bin/env python3
"""Validate translation coverage, fingerprints, local links and protected spans."""
import json
import re
from collections import Counter
from pathlib import Path

from translate import FORMAT_VERSION, ROOT, VERSION, protect, sha


def main():
    source_root, translated_root = ROOT/'collection', ROOT/'collection_zh'
    sources = json.loads((source_root/'manifest.json').read_text())['items']
    manifest = json.loads((translated_root/'manifest.json').read_text())
    translated = {row['source_file']:row for row in manifest['items']}
    assert manifest['completed'] == len(sources) == len(translated), 'Incomplete coverage'
    assert not manifest['failures'], manifest['failures']
    index = (translated_root/'INDEX.md').read_text()
    protected_count = 0
    for row in sources:
        info = translated[row['file']]
        original = (source_root/row['file']).read_text()
        path = translated_root/info['file']
        output = path.read_text()
        assert info['source_sha256'] == sha(original), f'Source changed: {path}'
        assert info['output_sha256'] == sha(output), f'Output changed: {path}'
        assert info['engine'] == VERSION and info['format_version'] == FORMAT_VERSION, f'Outdated: {path}'
        assert row['file'] in index, f'Not in index: {path}'
        assert not re.search(r'⟦P\d{6}⟧',output), f'Unrestored placeholder: {path}'
        _, mapping = protect(original)
        expected = Counter(mapping.values())
        for value, count in expected.items():
            assert output.count(value) >= count, f'Protected source span missing: {path}: {value[:80]}'
        protected_count += len(mapping)
        assert len(re.findall(r'[\u4e00-\u9fff]',output)) > 200, f'Too little Chinese: {path}'
        match = re.search(r'\[查看本地英文原文\]\(([^)]+)\)',output)
        assert match and (path.parent/match.group(1)).resolve() == (source_root/row['file']).resolve(), f'Invalid original link: {path}'
        if row['status']=='abstract_only':
            assert '不是论文全文' in output, f'Missing abstract-only notice: {path}'
    result = {'passed':True,'documents':len(sources),'kinds':dict(Counter(r['kind'] for r in sources)),
              'protected_spans_checked':protected_count,'failures':0,
              'checks':['all sources translated','source/output fingerprints','translation format version',
                        'index coverage','protected spans retained','no unresolved placeholders',
                        'Chinese text present','local original links','abstract-only notice']}
    (translated_root/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
