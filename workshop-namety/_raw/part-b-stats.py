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

# Normalizace projektů
def norm_proj(p):
    p = p.lower().replace('\\', '/')
    if 'alzask' in p:
        return 'alzask'
    elif 'fhb' in p:
        return 'fhb'
    elif 'spec-factory' in p or 'plugins/spec-factory' in p:
        return 'spec-factory'
    elif 'shared' in p and 'plugins' in p:
        return 'shared/plugins'
    elif 'shared' in p:
        return 'shared'
    elif 'myfaber' in p:
        return 'myfaber'
    return 'other'

# 1. Per projekt
per_proj = defaultdict(int)
for r in rows:
    p = norm_proj(r.get('project', ''))
    per_proj[p] += 1

print("=== PER PROJEKT ===")
for p in sorted(per_proj.keys()):
    print(f"{p}: {per_proj[p]}")
print(f"CELKEM: {sum(per_proj.values())}")
print()

# 2. Per měsíc
per_month = defaultdict(lambda: defaultdict(int))
for r in rows:
    ts = r.get('timestamp')
    if isinstance(ts, (int, float)):
        ts_ms = ts if ts > 1e10 else ts * 1000
        dt = datetime.fromtimestamp(ts_ms / 1000)
        month = dt.strftime('%Y-%m')
        proj = norm_proj(r.get('project', ''))
        per_month[month][proj] += 1

print("=== PER MĚSÍC ===")
for m in sorted(per_month.keys()):
    total = sum(per_month[m].values())
    detail = ', '.join(f"{p}={per_month[m][p]}" for p in sorted(per_month[m].keys()))
    print(f"{m}: {total} ({detail})")
print()

# 3. Slash commands
slash_cmds = defaultdict(int)
for r in rows:
    display = r.get('display', '') or ''
    m = re.search(r'^/([a-z0-9:_-]+)', display)
    if m:
        slash_cmds[m.group(1)] += 1

print("=== SLASH COMMANDS (top 20) ===")
for cmd in sorted(slash_cmds.keys(), key=lambda x: -slash_cmds[x])[:20]:
    print(f"{cmd}: {slash_cmds[cmd]}")
print()

# 4. Délka promptů
lengths = []
for r in rows:
    display = r.get('display', '') or ''
    lengths.append(len(display))

lengths.sort()
n = len(lengths)
print("=== DISTRIBUCE DÉLEK PROMPTŮ ===")
print(f"Min: {min(lengths)}")
print(f"P25: {lengths[n//4]}")
print(f"Medián: {lengths[n//2]}")
print(f"P75: {lengths[3*n//4]}")
print(f"P90: {lengths[int(0.9*n)]}")
print(f"P99: {lengths[int(0.99*n)]}")
print(f"Max: {max(lengths)}")

# Histogram
bins = {
    '0-50': 0, '50-100': 0, '100-250': 0,
    '250-500': 0, '500-1000': 0, '1000+': 0
}
for l in lengths:
    if l < 50:
        bins['0-50'] += 1
    elif l < 100:
        bins['50-100'] += 1
    elif l < 250:
        bins['100-250'] += 1
    elif l < 500:
        bins['250-500'] += 1
    elif l < 1000:
        bins['500-1000'] += 1
    else:
        bins['1000+'] += 1

for b in ['0-50', '50-100', '100-250', '250-500', '500-1000', '1000+']:
    pct = 100 * bins[b] / n
    print(f"{b}: {bins[b]} ({pct:.1f}%)")
print()

# 5. Prompty nad 1000 znaků
over1k = []
for r in rows:
    display = r.get('display', '') or ''
    if len(display) > 1000:
        ts = r.get('timestamp')
        if isinstance(ts, (int, float)):
            ts_ms = ts if ts > 1e10 else ts * 1000
            dt = datetime.fromtimestamp(ts_ms / 1000)
            over1k.append((dt, len(display), display[:200]))

print(f"=== PROMPTY NAD 1000 ZNAKŮ ({len(over1k)} celkem) ===")
for dt, l, text in sorted(over1k)[:44]:
    print(f"{dt.strftime('%Y-%m-%d %H:%M')} | {l} | {text[:100].strip()}")
print()

# 6. pastedContents
pasted = sum(1 for r in rows if r.get('pastedContents'))
print(f"=== PASTED CONTENTS ===")
print(f"Prompty s pastedContents: {pasted}")
# Průměrná velikost
sizes = []
for r in rows:
    pc = r.get('pastedContents', [])
    if pc:
        for item in pc:
            if isinstance(item, dict):
                s = len(json.dumps(item))
                sizes.append(s)
if sizes:
    print(f"Průměr pastedContents: {sum(sizes)/len(sizes):.0f} B")
    print(f"Max pastedContents: {max(sizes)} B")
print()

# 7. Unikátní sessionId per projekt
per_proj_sessions = defaultdict(set)
for r in rows:
    sid = r.get('sessionId', '')
    p = norm_proj(r.get('project', ''))
    if sid:
        per_proj_sessions[p].add(sid)

print("=== UNIKÁTNÍ SESSIONS PER PROJEKT ===")
for p in sorted(per_proj_sessions.keys()):
    print(f"{p}: {len(per_proj_sessions[p])}")
