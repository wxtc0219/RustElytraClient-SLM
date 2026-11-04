#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查 REC jar 里引用的 baritone 方法/字段是否在 MagicBaritone jar 的对应类中存在。"""
import zipfile
import subprocess
import re
import os
import sys
import tempfile

JAVAP = r'C:\Users\wxtc\AppData\Roaming\PrismLauncher\java\java-runtime-delta\bin\javap.exe'

rec_jar, mb_jar, mcver = sys.argv[1], sys.argv[2], sys.argv[3]

# 1. 收集 REC 里引用到的 baritone 成员
work = tempfile.mkdtemp()
with zipfile.ZipFile(rec_jar) as z:
    z.extractall(work)
    rec_names = [n for n in z.namelist() if n.endswith('.class')]

mem_pat = re.compile(r'//\s*(Method|InterfaceMethod|Field)\s+(baritone/[\w/$]+)\.([\w$<>]+):(\S+)')
refs = set()
for n in rec_names:
    path = os.path.join(work, n)
    out = subprocess.run([JAVAP, '-v', '-p', path], capture_output=True, text=True,
                         encoding='utf-8', errors='replace').stdout
    for m in mem_pat.finditer(out):
        refs.add((m.group(1), m.group(2), m.group(3), m.group(4)))
print(f'== {mcver}: {len(refs)} baritone member refs')

# 2. 收集 MB 每个 baritone 类的成员签名
mb_work = tempfile.mkdtemp()
with zipfile.ZipFile(mb_jar) as z:
    mb_names = {n[:-6] for n in z.namelist() if n.endswith('.class')}
    z.extractall(mb_work)

decl_pat = re.compile(r'^\s*(?:public|protected|private|static|final|abstract|default|synchronized|native|transient|volatile|\s)*[\w$.\[\]]+\s+([\w$<>]+)\(([^)]*)\)', re.M)
field_pat = re.compile(r'^\s*(?:public|protected|private|static|final|volatile|transient|\s)+[\w$.\[\]<>]+ ([\w$]+);', re.M)

cache = {}
def members(cls):
    if cls in cache:
        return cache[cls]
    path = os.path.join(mb_work, cls + '.class')
    if not os.path.isfile(path):
        cache[cls] = (set(), set())
        return cache[cls]
    out = subprocess.run([JAVAP, '-p', '-s', path], capture_output=True, text=True,
                         encoding='utf-8', errors='replace').stdout
    methods = set()
    lines = out.splitlines()
    for line in lines:
        if '(' not in line or line.startswith('Compiled'):
            continue
        head = line.split('(')[0].strip()
        if not head:
            continue
        name = head.split()[-1]
        if name in ('class', 'interface', 'enum'):
            continue
        methods.add(name)
    fields = set()
    for line in lines:
        m = re.match(r'^\s*(?:public|protected|private|static|final|volatile|transient|synchronized|\s)+[\w$.\[\]<>]+ ([\w$]+);\s*$', line)
        if m:
            fields.add(m.group(1))
    cache[cls] = (methods, fields)
    return cache[cls]

missing = []
for kind, cls, name, desc in sorted(refs):
    if cls not in mb_names:
        missing.append((kind, cls, name, desc, 'NO CLASS'))
        continue
    methods, fields = members(cls)
    if kind == 'Field':
        if name not in fields:
            missing.append((kind, cls, name, desc, 'NO FIELD'))
    else:
        if name not in methods:
            missing.append((kind, cls, name, desc, 'NO METHOD'))

print('missing members:', len(missing))
for x in missing[:40]:
    print('  ', x)
