#!/usr/bin/env python3
import json
import re
from datetime import datetime
from collections import defaultdict
from pathlib import Path

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

# 1. Per projekt
per_proj = defaultdict(int)
for r in rows:
    p = norm_proj(r.get('project', ''))
    per_proj[p] += 1

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

# 3. Slash commands
slash_cmds = defaultdict(int)
for r in rows:
    display = r.get('display', '') or ''
    m = re.search(r'^/([a-z0-9:_-]+)', display)
    if m:
        slash_cmds[m.group(1)] += 1

# 4. Délka promptů
lengths = []
for r in rows:
    display = r.get('display', '') or ''
    lengths.append(len(display))

lengths.sort()
n = len(lengths)

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

# 6. pastedContents
pasted = sum(1 for r in rows if r.get('pastedContents'))
sizes = []
for r in rows:
    pc = r.get('pastedContents', [])
    if pc:
        for item in pc:
            if isinstance(item, dict):
                s = len(json.dumps(item))
                sizes.append(s)

# 7. Unikátní sessionId per projekt
per_proj_sessions = defaultdict(set)
for r in rows:
    sid = r.get('sessionId', '')
    p = norm_proj(r.get('project', ''))
    if sid:
        per_proj_sessions[p].add(sid)

# === Výstup ===
out = []
out.append("# PART B — Statistiky z history.jsonl\n\n")

out.append(f"**Soubor:** C:/Users/ai_martint/.claude/history.jsonl\n")
with open(HIST, encoding='utf-8') as f:
    total_lines = sum(1 for _ in f)
out.append(f"**Zpracováno:** {len(rows)} promptů (z {total_lines} řádků)\n")
out.append(f"**Období:** 2026-01 až 2026-08\n\n")

out.append("## Per projekt\n\n")
out.append("| Projekt | Počet | % |\n|---------|-------|----|\n")
total = sum(per_proj.values())
for p in sorted(per_proj.keys()):
    pct = 100 * per_proj[p] / total
    out.append(f"| {p} | {per_proj[p]} | {pct:.1f}% |\n")
out.append(f"| **CELKEM** | **{total}** | **100%** |\n\n")

out.append("**KONTROLA:** Očekáváno (alzask 1134, fhb 212, myfaber 6, shared 14, spec-factory 137) = 1503; aktuálně = {} (diff: {}).\n\n".format(total, total - 1503))

out.append("## Per měsíc\n\n")
out.append("| Měsíc | Celkem | alzask | fhb | myfaber | shared | spec-factory |\n|-------|--------|--------|-----|---------|--------|---------------|\n")

for m in sorted(per_month.keys()):
    t = sum(per_month[m].values())
    az = per_month[m].get('alzask', 0)
    fh = per_month[m].get('fhb', 0)
    mf = per_month[m].get('myfaber', 0)
    sh = per_month[m].get('shared', 0)
    sf = per_month[m].get('spec-factory', 0)
    out.append(f"| {m} | {t} | {az} | {fh} | {mf} | {sh} | {sf} |\n")

out.append("\n## Slash commands (top 15)\n\n")
out.append("| Příkaz | Počet |\n|--------|-------|\n")
for cmd in sorted(slash_cmds.keys(), key=lambda x: -slash_cmds[x])[:15]:
    out.append(f"| /{cmd} | {slash_cmds[cmd]} |\n")

out.append("\n## Distribuce délek promptů\n\n")
out.append(f"| Metrika | Hodnota |\n|---------|----------|\n")
out.append(f"| Minimum | {min(lengths)} znaků |\n")
out.append(f"| P25 | {lengths[n//4]} znaků |\n")
out.append(f"| Medián | {lengths[n//2]} znaků |\n")
out.append(f"| P75 | {lengths[3*n//4]} znaků |\n")
out.append(f"| P90 | {lengths[int(0.9*n)]} znaků |\n")
out.append(f"| P99 | {lengths[int(0.99*n)]} znaků |\n")
out.append(f"| Maximum | {max(lengths)} znaků |\n\n")

out.append("### Histogram\n\n")
out.append("| Rozpětí | Počet | % |\n|---------|-------|----|\n")
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
    out.append(f"| {b} | {bins[b]} | {pct:.1f}% |\n")

out.append("\n## Prompty nad 1000 znaků\n\n")
out.append(f"**Celkem:** {len(over1k)}\n\n")
out.append("| Datum | Délka | Text (prvních 100 znaků) |\n|-------|-------|-------------------------|\n")
for dt, l, text in sorted(over1k)[:44]:
    safe_text = text[:100].replace('|', '\\|').replace('\n', ' ')
    out.append(f"| {dt.strftime('%Y-%m-%d %H:%M')} | {l} | {safe_text} |\n")

out.append("\n## PastedContents\n\n")
out.append(f"| Metrika | Hodnota |\n|---------|----------|\n")
out.append(f"| Prompty s pastedContents | {pasted} |\n")
if sizes:
    out.append(f"| Průměrná velikost | {sum(sizes)/len(sizes):.0f} B |\n")
    out.append(f"| Maximální velikost | {max(sizes)} B |\n")

out.append("\n## Unikátní sessions per projekt\n\n")
out.append("| Projekt | Sessions |\n|---------|----------|\n")
for p in sorted(per_proj_sessions.keys()):
    out.append(f"| {p} | {len(per_proj_sessions[p])} |\n")

# Uložení
output_path = Path("C:/tmp/workshop-namety/_raw/faze1-statistiky.md")
with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(out)

print(f"Statistiky uloženy: {output_path}")
print(f"Velikost: {output_path.stat().st_size} B")
