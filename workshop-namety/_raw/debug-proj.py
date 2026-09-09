#!/usr/bin/env python3
import json

HIST = 'C:/Users/ai_martint/.claude/history.jsonl'
alzask_projects = {}

with open(HIST, encoding='utf-8') as f:
    for line in f:
        try:
            o = json.loads(line)
        except:
            continue
        p = (o.get('project') or '').lower().replace('\\', '/')
        if p.startswith(('c:/git/alzask', 'c:/git/fhb', 'c:/git/myfaber', 'c:/git/shared')):
            if 'alzask' in p:
                if p not in alzask_projects:
                    alzask_projects[p] = 0
                alzask_projects[p] += 1

print(f"Unique alzask project paths ({len(alzask_projects)}):")
for p in sorted(alzask_projects.keys()):
    print(f"{alzask_projects[p]:3d}x {p}")
