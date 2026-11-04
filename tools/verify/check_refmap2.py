#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 yarn/unimined 的 tiny 映射校验 mixin refmap 里的 intermediary 目标是否真实存在。"""
import json
import re
import sys
import zipfile


def parse_tiny(path):
    classes = set()
    members = set()  # (inter_class, inter_member)
    with open(path, encoding='utf-8', errors='replace') as f:
        f.readline()
        cur = None
        for line in f:
            parts = line.rstrip('\n').split('\t')
            if parts[0] == 'c':
                cur = parts[2]
                classes.add(cur)
            elif len(parts) >= 6 and parts[1] in ('m', 'f') and cur:
                members.add((cur, parts[4]))
    return classes, members


def validate(jar, refmap, tiny, label):
    classes, members = parse_tiny(tiny)
    with zipfile.ZipFile(jar) as z:
        data = json.loads(z.read(refmap))
    maps = data.get('mappings', {})
    # 兼容两种结构：{mixin: {named: inter}} 或 {mixin: {key: Linter...}} —— 统一取所有字符串值
    entries = []

    def walk(obj):
        if isinstance(obj, str):
            entries.append(obj)
        elif isinstance(obj, dict):
            for v in obj.values():
                walk(v)

    walk(maps)
    missing = []
    checked = 0
    pat = re.compile(r'L([\w/$]+);([\w$<>]+)(\([^;]*)?')
    for e in entries:
        m = pat.search(e)
        if not m:
            continue
        checked += 1
        cls, mem = m.group(1), m.group(2)
        if cls not in classes:
            missing.append((cls, mem, 'NO CLASS'))
        elif (cls, mem) not in members:
            missing.append((cls, mem, 'NO MEMBER'))
    print(f'{label}: entries={checked} missing={len(missing)}')
    for x in missing[:15]:
        print('  MISS', x)


if __name__ == '__main__':
    validate(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
