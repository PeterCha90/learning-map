#!/usr/bin/env python3
"""Render a learning-map .md file into one self-contained, offline HTML mindmap.

Usage: python3 render.py MAP.md [-o OUT.html]
Default output: same folder, same name with .html.
Stdlib only, so it runs anywhere python3 exists.
"""
import json, re, sys, html
from pathlib import Path

ITEM = re.compile(r'^(\s*)[-*]\s+\[( |x|X)\]\s+(.*)$')
BRANCH = re.compile(r'^##\s+(.*?)\s*(?:\[(\d)\s*/\s*5\])?\s*$')
SPLIT = re.compile(r'\s+(?:—|--|::)\s+')


def parse(text):
    meta, body = {}, text
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            for line in text[3:end].splitlines():
                if ':' in line:
                    k, v = line.split(':', 1)
                    meta[k.strip()] = v.strip().strip('"')
            body = text[end + 4:]
    root = {'label': meta.get('title', 'Learning Map'), 'children': [], 'kind': 'root'}
    branch, stack = None, []
    for raw in body.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith('# '):
            root['label'] = line[2:].strip()
            continue
        m = BRANCH.match(line)
        if m:
            branch = {'label': m.group(1).strip(), 'kind': 'branch', 'children': [],
                      'level': int(m.group(2)) if m.group(2) else None}
            root['children'].append(branch)
            stack = []
            continue
        m = ITEM.match(raw)
        if m and branch is not None:
            indent = len(m.group(1).replace('\t', '  '))
            parts = SPLIT.split(m.group(3).strip(), maxsplit=1)
            node = {'label': parts[0], 'desc': parts[1] if len(parts) > 1 else '',
                    'learned': m.group(2).lower() == 'x', 'kind': 'concept', 'children': []}
            while stack and stack[-1][0] >= indent:
                stack.pop()
            (stack[-1][1]['children'] if stack else branch['children']).append(node)
            stack.append((indent, node))
    return meta, root


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__); sys.exit(0)
    src = Path(args[0]).expanduser().resolve()
    out = Path(args[args.index('-o') + 1]).expanduser().resolve() if '-o' in args else src.with_suffix('.html')
    meta, root = parse(src.read_text(encoding='utf-8'))
    tpl = (Path(__file__).resolve().parent.parent / 'assets' / 'template.html').read_text(encoding='utf-8')
    data = json.dumps({'meta': meta, 'root': root}, ensure_ascii=False).replace('</', '<\\/')
    page = tpl.replace('__TITLE__', html.escape(root['label'])).replace('__DATA__', data)
    out.write_text(page, encoding='utf-8')

    def count(n):
        k = [count(c) for c in n['children']]
        own = (1, 1 if n.get('learned') else 0) if n['kind'] == 'concept' else (0, 0)
        return (own[0] + sum(a for a, _ in k), own[1] + sum(b for _, b in k))
    total, learned = count(root)
    print(f'{out}  ({learned}/{total} learned, {len(root["children"])} branches)')


if __name__ == '__main__':
    main()
