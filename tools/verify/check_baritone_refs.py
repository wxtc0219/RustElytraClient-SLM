#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查 REC jar 里引用的 baritone 类是否都存在于给定 MagicBaritone jar 里（防止 NoClassDefFoundError）。"""
import zipfile
import subprocess
import re
import os
import sys
import tempfile

JAVAP = r'C:\Users\wxtc\AppData\Roaming\PrismLauncher\java\java-runtime-delta\bin\javap.exe'

rec_jar, mb_jar, mcver = sys.argv[1], sys.argv[2], sys.argv[3]
mb_classes = set()
with zipfile.ZipFile(mb_jar) as z:
    for n in z.namelist():
        if n.endswith('.class'):
            mb_classes.add(n[:-6])

work = tempfile.mkdtemp()
with zipfile.ZipFile(rec_jar) as z:
    z.extractall(work)
    rec_names = [n for n in z.namelist() if n.endswith('.class')]

pat = re.compile(r'//\s*(baritone/[\w/$]+)')
refs = {}
for n in rec_names:
    path = os.path.join(work, n)
    try:
        out = subprocess.run([JAVAP, '-v', '-p', path], capture_output=True, text=True,
                             encoding='utf-8', errors='replace').stdout
    except Exception as e:
        continue
    for m in pat.finditer(out):
        c = m.group(1)
        if c.startswith('baritone/'):
            refs.setdefault(c, set()).add(n)

missing = {c: v for c, v in refs.items() if c not in mb_classes}
print(f'== {mcver}: REC references {len(refs)} baritone classes; missing in MB: {len(missing)}')
for c, v in sorted(missing.items()):
    print('  MISSING', c, '<-', sorted(v)[:3])
