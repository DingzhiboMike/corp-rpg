#!/usr/bin/env python3
"""Проверка структуры скилла: все ссылки на .md живы, SKILL.md в бюджете."""
import glob
import os
import re
import sys

MAX_SKILL_LINES = 150
SUBDIRS = ['start', 'play', 'world', 'world/roles', 'finale', 'modes']
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)

bad = 0
files = ['SKILL.md', 'README.md'] + glob.glob('references/**/*.md', recursive=True)
for f in files:
    for i, line in enumerate(open(f, encoding='utf-8'), 1):
        for m in re.finditer(r'`((?:references/)?[\w./_-]+\.md)`', line):
            p = m.group(1)
            cands = [p, 'references/' + p] + ['references/%s/%s' % (d, p) for d in SUBDIRS]
            if p != 'SKILL.md' and not any(os.path.exists(c) for c in cands):
                print('%s:%d: нет файла %s' % (f, i, p))
                bad += 1

n = sum(1 for _ in open('SKILL.md', encoding='utf-8'))
if n > MAX_SKILL_LINES:
    print('SKILL.md: %d строк, бюджет %d' % (n, MAX_SKILL_LINES))
    bad += 1

print('ok' if not bad else 'проблем: %d' % bad)
sys.exit(1 if bad else 0)
