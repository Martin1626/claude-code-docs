#!/usr/bin/env python3
import json
from collections import defaultdict

HIST = 'C:/Users/ai_martint/.claude/history.jsonl'
PREF = ['c:/git/alzask', 'c:/git/fhb', 'c:/git/myfaber', 'c:/git/shared']

counts = defaultdict(int)
total = 0
with open(HIST, encoding='utf-8') as f:
    for line in f:
        try:
            o = json.loads(line)
            p = (o.get('project') or '').lower().replace('\\', '/')
            if any(p.startswith(prf) for prf in PREF):
                total += 1
                for prf in PREF:
                    if p.startswith(prf):
                        counts[prf] += 1
                        break
        except:
            pass

for prf in sorted(counts.keys()):
    print(f'{prf}: {counts[prf]}')
print(f'CELKEM: {total}')

# Expected
exp = {'c:/git/alzask': 1134, 'c:/git/fhb': 212, 'c:/git/myfaber': 6, 'c:/git/shared': 14}
# spec-factory by měl být v shared/plugins
spec_fact = 0
for prf in PREF:
    if counts[prf] > exp.get(prf, 0):
        print(f'EXTRA v {prf}: {counts[prf] - exp.get(prf, 0)}')

print(f'\nExpected total: {sum(exp.values()) + 137}')
