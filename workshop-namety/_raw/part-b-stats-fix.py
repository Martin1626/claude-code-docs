#!/usr/bin/env python3
import json
import re
from datetime import datetime
from collections import defaultdict

HIST = 'C:/Users/ai_martint/.claude/history.jsonl'
PREF = ('c:/git/alzask', 'c:/git/fhb', 'c:/git/myfaber', 'c:/git/shared')

rows = []
with open(HIST, encoding='utf-8') as f:
    for line in f:
        try:
            o = json.loads(line)
        except Exception:
            continue
        p = (o.get('project') or '').lower().replace('\\', '/')
        if any(p.startswith(prf) for prf in PREF):
            rows.append(o)

# Normalizace: rozlišit spec-factory v shared/plugins od zbytku
def norm_proj(p):
    p = p.lower().replace('\\', '/')
    if 'shared' in p and 'plugins' in p and 'spec-factory' in p:
        return 'spec-factory'
    elif 'plugins/spec-factory' in p or '/spec-factory' in p:
        return 'spec-factory'
    elif 'alzask' in p:
        return 'alzask'
    elif 'fhb' in p:
        return 'fhb'
    elif 'shared' in p:
        return 'shared'
    elif 'myfaber' in p:
        return 'myfaber'
    return 'other'

# Debug: check non-spec-factory in shared
for r in rows:
    p = r.get('project', '')
    normed = norm_proj(p)
    if 'shared' in p and normed not in ('spec-factory', 'shared'):
        print(f"WARN: {p} -> {normed}")

# 1. Per projekt
per_proj = defaultdict(int)
for r in rows:
    p = norm_proj(r.get('project', ''))
    per_proj[p] += 1

print("\n=== PER PROJEKT ===")
for p in sorted(per_proj.keys()):
    print(f"{p}: {per_proj[p]}")
total = sum(per_proj.values())
print(f"CELKEM: {total}")
print(f"KONTROLA (ma byt 1503): {total == 1503}")
print()

# Vypis chybejicich
expected = {'alzask': 1134, 'fhb': 212, 'myfaber': 6, 'shared': 14, 'spec-factory': 137}
for p, expected_count in expected.items():
    actual = per_proj.get(p, 0)
    if actual != expected_count:
        print(f"CHYBA: {p} ma {actual}, ocekavano {expected_count} (diff: {actual - expected_count})")
