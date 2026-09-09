import json, datetime, collections, os

HIST = 'C:/Users/ai_martint/.claude/history.jsonl'
OUT = 'C:/tmp/workshop-namety/_raw'
BS = chr(92)

rows = []
with open(HIST, encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except Exception:
            continue
        p = (o.get('project') or '').lower().replace(BS, '/')
        if p == 'c:/git/alzask':
            rows.append(o)

rows.sort(key=lambda o: o.get('timestamp') or 0)

buckets = collections.OrderedDict()
for o in rows:
    ts = o.get('timestamp') or 0
    dt = datetime.datetime.fromtimestamp(ts / 1000)
    key = dt.strftime('%Y-%m')
    buckets.setdefault(key, []).append((dt, o))

# H1 = 01..05, pak samostatne 06, 07, 08
groups = {
    'H1': ['2026-01', '2026-02', '2026-03', '2026-04', '2026-05'],
    '06': ['2026-06'],
    '07': ['2026-07'],
    '08': ['2026-08'],
}

for name, months in groups.items():
    items = []
    for m in months:
        items.extend(buckets.get(m, []))
    items.sort(key=lambda x: x[0])
    path = os.path.join(OUT, 'prompty-alzask-' + name + '.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('# Prompty alzask — ' + name + ' (' + ', '.join(months) + ')\n\n')
        for dt, o in items:
            f.write('## ' + dt.strftime('%Y-%m-%d %H:%M') + '\n')
            f.write((o.get('display') or '').rstrip() + '\n\n')
        f.write('\n---\nPocet promptu v souboru: ' + str(len(items)) + '\n')
    kb = os.path.getsize(path) / 1024
    print(name, '|', len(items), 'promptu |', round(kb, 1), 'KB |', path)

# kontrola ostatnich souboru
for fn in ['prompty-fhb-myfaber.md', 'prompty-shared.md', 'prompty-alzask-H2.md']:
    p = os.path.join(OUT, fn)
    if os.path.exists(p):
        print(fn, '|', round(os.path.getsize(p) / 1024, 1), 'KB')
