#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通用：用 unimined/yarn 的 tiny/umf 映射校验 mixin refmap 的 intermediary 目标是否存在。"""
import json
import re
import sys
import zipfile


def parse_mapping(path):
    """返回 (inter_classes, (inter_class, inter_member))"""
    with open(path, encoding='utf-8', errors='replace') as f:
        first = f.readline().rstrip('\n').split('\t')
        if first[0] == 'tiny':
            namespaces = first[3:]
            inter_idx = namespaces.index('intermediary')
            classes = set()
            members = set()
            cur = None
            for line in f:
                parts = line.rstrip('\n').split('\t')
                if parts[0] == 'c':
                    cur = parts[1 + inter_idx]
                    classes.add(cur)
                elif len(parts) >= 2 + len(namespaces) and parts[1] in ('m', 'f') and cur:
                    members.add((cur, parts[3 + inter_idx]))
            return classes, members
        elif first[0] == 'umf':
            namespaces = f.readline().rstrip('\n').split('\t')
            inter_idx = namespaces.index('intermediary')
            classes = set()
            members = set()
            cur = None
            for line in f:
                parts = line.rstrip('\n').split('\t')
                if parts[0] == 'c':
                    cur = parts[1 + inter_idx]
                    classes.add(cur)
                elif len(parts) >= 2 + len(namespaces) and parts[1] in ('m', 'f') and cur:
                    spec = parts[2 + inter_idx]
                    members.add((cur, spec.split(';')[0]))
            return classes, members
    raise SystemExit('unknown mapping format: ' + path)


VAL = re.compile(r'^L([\w/$]+);([\w$<>]+)(?:\(.*|:.*)$')
CLASS = re.compile(r'^([\w/$]+)$')


def validate(jar, refmap, mapping, label):
    classes, members = parse_mapping(mapping)
    with zipfile.ZipFile(jar) as z:
        data = json.loads(z.read(refmap))
    entries = []

    def walk(o):
        if isinstance(o, str):
            entries.append(o)
        elif isinstance(o, dict):
            for v in o.values():
                walk(v)

    walk(data.get('mappings', {}))
    checked = 0
    missing = []
    inherited = 0
    all_members = {m for (_, m) in members}
    for e in entries:
        m = VAL.match(e)
        if m:
            checked += 1
            cls, mem = m.group(1), m.group(2)
            if cls not in classes:
                missing.append((cls, mem, 'NO CLASS'))
            elif (cls, mem) not in members:
                if mem in all_members:
                    inherited += 1   # 继承自父类/接口，按名字能查到
                else:
                    missing.append((cls, mem, 'NO SUCH MEMBER ANYWHERE'))
            continue
        m = CLASS.match(e)
        if m and 'minecraft' in m.group(1):
            checked += 1
            if m.group(1) not in classes:
                missing.append((m.group(1), '', 'NO CLASS'))
    print(f'{label}: entries={checked} inherited_ok={inherited} missing={len(missing)}')
    for x in missing[:15]:
        print('  MISS', x)


if __name__ == '__main__':
    validate(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
