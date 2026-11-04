#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 REC 1.21.11 jar 中 mixin 注解（已被 loom 直接重映射为 intermediary）的目标类/方法是否存在。"""
import os
import re
import subprocess
import sys
import tempfile
import zipfile

JAVAP = r'C:\Users\wxtc\AppData\Roaming\PrismLauncher\java\java-runtime-delta\bin\javap.exe'


def parse_mapping(path):
    classes = set()
    members = set()
    cur = None
    with open(path, encoding='utf-8', errors='replace') as f:
        first = f.readline().rstrip('\n').split('\t')
        if first[0] == 'umf':
            ns = f.readline().rstrip('\n').split('\t')
        else:
            ns = first[3:]
        inter_idx = ns.index('intermediary')
        for line in f:
            parts = line.rstrip('\n').split('\t')
            if parts[0] == 'c':
                cur = parts[1 + inter_idx]
                classes.add(cur)
            elif len(parts) >= 2 + len(ns) and parts[1] in ('m', 'f') and cur:
                members.add((cur, parts[2 + inter_idx].split(';')[0]))
    return classes, members


MIXIN = re.compile(r'org\.spongepowered\.asm\.mixin\.Mixin\(')
TARGET_CLASS = re.compile(r'value=\[class L?([\w./$]+);?\]')
TARGETS = re.compile(r'targets=\["([^"]+)"')
INJ = re.compile(r'org\.spongepowered\.asm\.mixin\.injection\.\w+\(')
METHOD_ARG = re.compile(r'\bmethod=\["([^"]+)"')
SHADOW = re.compile(r'method=\["([^"]+)"')


def main(jar, mapping, label):
    classes, members = parse_mapping(mapping)
    work = tempfile.mkdtemp()
    with zipfile.ZipFile(jar) as z:
        names = [n for n in z.namelist() if n.startswith('dev/rstminecraft/mixin/') and n.endswith('.class')]
        z.extractall(work)
    missing = []
    checked = 0
    for n in names:
        out = subprocess.run([JAVAP, '-v', '-p', os.path.join(work, n)], capture_output=True,
                             text=True, encoding='utf-8', errors='replace').stdout
        # 目标类
        target = None
        m = TARGET_CLASS.search(out)
        if m:
            target = m.group(1).replace('.', '/')
        elif 'targets=[' in out:
            continue  # baritone 目标，跳过
        if not target:
            continue
        # 注解里的方法名
        for mm in METHOD_ARG.finditer(out):
            spec = mm.group(1)
            name = spec.split('(')[0]
            if not name or name.startswith('<'):
                continue
            checked += 1
            if target not in classes:
                missing.append((n, target, name, 'NO CLASS'))
            elif (target, name) not in members:
                missing.append((n, target, name, 'NO MEMBER'))
    print(f'{label}: target classes+methods checked={checked} missing={len(missing)}')
    for x in missing[:20]:
        print('  MISS', x)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
