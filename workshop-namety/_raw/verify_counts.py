import json, re, collections

HIST = 'C:/Users/ai_martint/.claude/history.jsonl'
PREF = ('c:/git/alzask', 'c:/git/fhb', 'c:/git/myfaber', 'c:/git/shared')
BS = chr(92)

total_lines = 0
work = []
allrows = []
with open(HIST, encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        total_lines += 1
        try:
            o = json.loads(line)
        except Exception:
            continue
        allrows.append(o)
        p = (o.get('project') or '').lower().replace(BS, '/')
        if p.startswith(PREF):
            work.append(o)

print('radku v souboru:', total_lines)
print('parsovanych JSON:', len(allrows))
print('pracovnich promptu:', len(work))

# per projekt
per = collections.Counter()
for o in work:
    p = (o.get('project') or '').lower().replace(BS, '/')
    per[p] += 1
print()
print('--- per projekt (pracovni) ---')
for k, v in per.most_common():
    print(v, k)

# poslednich 12 zaznamu casove - jsou to prompty z teto session?
import datetime
ts = sorted(((o.get('timestamp') or 0), (o.get('project') or ''), (o.get('display') or '')[:70]) for o in allrows)
print()
print('--- 8 nejnovejsich zaznamu v cele historii ---')
for t, p, d in ts[-8:]:
    dt = datetime.datetime.fromtimestamp(t/1000).strftime('%Y-%m-%d %H:%M:%S')
    print(dt, '|', p, '|', d.replace('\n', ' '))

# slash commandy - pracovni vs cela historie
rx = re.compile(r'^/([a-z0-9:_-]+)', re.I)
def slash(rows):
    c = collections.Counter()
    for o in rows:
        d = (o.get('display') or '').strip()
        m = rx.match(d)
        if m:
            c[m.group(1).lower()] += 1
    return c

sw = slash(work)
sa = slash(allrows)
print()
print('--- slash commandy: klic | pracovni | cela historie ---')
keys = ['compact', 'model', 'context', 'resume', 'effort', 'clear', 'body-z-jednani', 'spec', 'spec-factory:spec', 'btw']
for k in keys:
    print(k, '|', sw.get(k, 0), '|', sa.get(k, 0))
print()
print('--- top 20 v cele historii ---')
for k, v in sa.most_common(20):
    print(v, k)

# delky - pracovni
L = sorted(len(o.get('display') or '') for o in work)
def pct(q):
    return L[min(len(L) - 1, int(q * len(L)))]
print()
print('--- delky promptu (pracovni) ---')
print('n =', len(L), 'min', L[0], 'p25', pct(.25), 'median', pct(.5), 'p75', pct(.75), 'p90', pct(.9), 'p99', pct(.99), 'max', L[-1])
print('nad 1000 znaku:', sum(1 for x in L if x > 1000))

La = sorted(len(o.get('display') or '') for o in allrows)
def pcta(q):
    return La[min(len(La) - 1, int(q * len(La)))]
print()
print('--- delky promptu (cela historie) ---')
print('n =', len(La), 'median', pcta(.5), 'max', La[-1])
print('nad 1000 znaku:', sum(1 for x in La if x > 1000))
