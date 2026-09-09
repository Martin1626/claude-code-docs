#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

HIST = 'C:/Users/ai_martint/.claude/history.jsonl'
PREF = ('c:/git/alzask', 'c:/git/fhb', 'c:/git/myfaber', 'c:/git/shared')

# Přečti a normalizuj
rows_by_proj = defaultdict(list)

with open(HIST, encoding='utf-8') as f:
    for line in f:
        try:
            o = json.loads(line)
        except:
            continue
        p = (o.get('project') or '').lower().replace('\\', '/')

        # Projekty: alzask, fhb, myfaber, shared, spec-factory
        if p.startswith('c:/git/alzask'):
            proj = 'alzask'
        elif p.startswith('c:/git/fhb'):
            proj = 'fhb'
        elif p.startswith('c:/git/myfaber'):
            proj = 'myfaber'
        elif 'spec-factory' in p and 'shared' in p and 'plugins' in p:
            proj = 'spec-factory'
        elif p.startswith('c:/git/shared'):
            proj = 'shared'
        else:
            continue

        # Timestamp
        ts = o.get('timestamp')
        if isinstance(ts, (int, float)):
            ts_ms = ts if ts > 1e10 else ts * 1000
            dt = datetime.fromtimestamp(ts_ms / 1000)
        else:
            dt = datetime.now()

        display = o.get('display', '') or ''

        rows_by_proj[proj].append((dt, display))

# Seřaď chronologicky
for proj in rows_by_proj:
    rows_by_proj[proj].sort(key=lambda x: x[0])

# === Generuj soubory ===

def write_prompts(proj, period_filter, filename):
    """Napiš prompty pro projekt a období"""
    prompts = []
    for dt, display in rows_by_proj[proj]:
        if period_filter(dt):
            prompts.append((dt, display))

    if not prompts:
        return 0

    out = []
    out.append(f"# {filename.replace('.md', '').upper()}\n\n")

    for dt, display in prompts:
        out.append(f"## {dt.strftime('%Y-%m-%d %H:%M')}\n")
        out.append(display + "\n\n")

    out.append(f"---\n**Celkem promptů v souboru: {len(prompts)}**\n")

    output_path = Path(f"C:/tmp/workshop-namety/_raw/{filename}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(out)

    return len(prompts)

# Filtery pro období
def h1_filter(dt):
    return dt.year == 2026 and dt.month <= 5

def h2_filter(dt):
    return dt.year == 2026 and dt.month >= 6

# Part C soubory
files_info = []

# 1. AlzaSk H1 (2026-01 až 05)
cnt = write_prompts('alzask', h1_filter, 'prompty-alzask-H1.md')
files_info.append((f"prompty-alzask-H1.md", cnt))

# 2. AlzaSk H2 (2026-06 až 08)
cnt = write_prompts('alzask', h2_filter, 'prompty-alzask-H2.md')
files_info.append((f"prompty-alzask-H2.md", cnt))

# 3. FHB + MyFABER
fhb_prompts = []
for dt, display in rows_by_proj['fhb']:
    fhb_prompts.append((dt, display))
for dt, display in rows_by_proj.get('myfaber', []):
    fhb_prompts.append((dt, display))
fhb_prompts.sort(key=lambda x: x[0])

out = []
out.append("# PROMPTY-FHB-MYFABER\n\n")
for dt, display in fhb_prompts:
    out.append(f"## {dt.strftime('%Y-%m-%d %H:%M')}\n")
    out.append(display + "\n\n")
out.append(f"---\n**Celkem promptů v souboru: {len(fhb_prompts)}**\n")

output_path = Path("C:/tmp/workshop-namety/_raw/prompty-fhb-myfaber.md")
with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(out)
files_info.append(("prompty-fhb-myfaber.md", len(fhb_prompts)))

# 4. Shared + Spec-factory
shared_prompts = []
for dt, display in rows_by_proj.get('shared', []):
    shared_prompts.append((dt, display))
for dt, display in rows_by_proj.get('spec-factory', []):
    shared_prompts.append((dt, display))
shared_prompts.sort(key=lambda x: x[0])

out = []
out.append("# PROMPTY-SHARED\n\n")
for dt, display in shared_prompts:
    out.append(f"## {dt.strftime('%Y-%m-%d %H:%M')}\n")
    out.append(display + "\n\n")
out.append(f"---\n**Celkem promptů v souboru: {len(shared_prompts)}**\n")

output_path = Path("C:/tmp/workshop-namety/_raw/prompty-shared.md")
with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(out)
files_info.append(("prompty-shared.md", len(shared_prompts)))

# Shrnutí
print("=== PART C: Extrakty promptů ===")
for fname, count in files_info:
    fpath = Path(f"C:/tmp/workshop-namety/_raw/{fname}")
    size = fpath.stat().st_size
    print(f"{fname}: {count} promptů ({size} B)")
