#!/usr/bin/env python3
import json
from collections import defaultdict

HIST = 'C:/Users/ai_martint/.claude/history.jsonl'

alzask_recs = []
with open(HIST, encoding='utf-8') as f:
    for line in f:
        try:
            o = json.loads(line)
            p = (o.get('project') or '').lower().replace('\\', '/')
            if p.startswith('c:/git/alzask'):
                alzask_recs.append((o.get('timestamp', 0), p, (o.get('display') or '')[:50]))
        except:
            pass

alzask_recs.sort(reverse=True)
print(f"TOTAL: {len(alzask_recs)}")
print("\nLast 10 (newest first):")
for ts, p, disp in alzask_recs[:10]:
    print(f"{ts} | {p} | {disp}")

# Unique projects
proj_set = set()
for ts, p, disp in alzask_recs:
    proj_set.add(p)

print(f"\nUnique projects: {len(proj_set)}")
for p in sorted(proj_set):
    cnt = sum(1 for ts, px, d in alzask_recs if px == p)
    print(f"{cnt:4d}x {p}")
