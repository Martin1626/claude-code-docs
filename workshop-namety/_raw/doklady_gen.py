import json, re, collections, datetime, os

HIST = 'C:/Users/ai_martint/.claude/history.jsonl'
OUT = 'C:/tmp/workshop-namety/_raw/doklady-statistiky.md'
BS = chr(92)
PREF = ('c:/git/alzask', 'c:/git/fhb', 'c:/git/myfaber', 'c:/git/shared')

allrows, work = [], []
with open(HIST, encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except Exception:
            continue
        allrows.append(o)
        p = (o.get('project') or '').lower().replace(BS, '/')
        if p.startswith(PREF):
            work.append(o)

def dt(o):
    return datetime.datetime.fromtimestamp((o.get('timestamp') or 0) / 1000)

def disp(o):
    return o.get('display') or ''

L = []
out = []
W = out.append

W('# Statistiky z history.jsonl — ověřený podklad')
W('')
W('Zdroj: `C:/Users/ai_martint/.claude/history.jsonl`, odečteno ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + '.')
W('Jeden řádek = jeden prompt zadaný člověkem. Normalizace cesty: lowercase + zpětná lomítka na dopředná (cesty v souboru mají nekonzistentní velikost písmen).')
W('')
W('## Základní rozsah')
W('')
W('| Celek | Promptů | Období |')
W('|---|---|---|')
tsa = sorted(dt(o) for o in allrows)
tsw = sorted(dt(o) for o in work)
W('| Celá historie (všechny projekty) | ' + str(len(allrows)) + ' | ' + tsa[0].strftime('%Y-%m-%d') + ' → ' + tsa[-1].strftime('%Y-%m-%d') + ' |')
W('| Jen pracovní projekty (v rozsahu) | ' + str(len(work)) + ' | ' + tsw[0].strftime('%Y-%m-%d') + ' → ' + tsw[-1].strftime('%Y-%m-%d') + ' |')
W('')
W('> **Pozor na dvě sady čísel.** Většina statistik níže je uvedena dvakrát — pro celou historii a jen pro pracovní projekty. Rozdíl je podstatný (např. `/compact` 67× vs. 51×) a záměna vede k nesprávně atribuovanému tvrzení.')
W('')

W('## Prompty per projekt (pracovní projekty)')
W('')
per = collections.Counter()
for o in work:
    per[(o.get('project') or '').lower().replace(BS, '/')] += 1
W('| Projekt | Promptů | % z pracovních |')
W('|---|---|---|')
for k, v in per.most_common():
    W('| `' + k + '` | ' + str(v) + ' | ' + str(round(100.0 * v / len(work), 1)) + ' % |')
W('| **Celkem** | **' + str(len(work)) + '** | **100 %** |')
W('')

W('## Prompty per měsíc')
W('')
mall = collections.Counter(dt(o).strftime('%Y-%m') for o in allrows)
mwork = collections.Counter(dt(o).strftime('%Y-%m') for o in work)
proj_short = {'c:/git/alzask': 'alzask', 'c:/git/fhb': 'fhb', 'c:/git/myfaber': 'myfaber',
              'c:/git/shared': 'shared', 'c:/git/shared/plugins/spec-factory': 'spec-factory'}
permonth = collections.defaultdict(collections.Counter)
for o in work:
    k = proj_short.get((o.get('project') or '').lower().replace(BS, '/'), 'jine')
    permonth[dt(o).strftime('%Y-%m')][k] += 1
cols = ['alzask', 'fhb', 'spec-factory', 'shared', 'myfaber']
W('| Měsíc | Celá historie | Pracovní | ' + ' | '.join(cols) + ' |')
W('|---|---|---|' + '---|' * len(cols))
for m in sorted(set(list(mall.keys()) + list(mwork.keys()))):
    row = [str(permonth[m].get(c, 0)) for c in cols]
    W('| ' + m + ' | ' + str(mall.get(m, 0)) + ' | ' + str(mwork.get(m, 0)) + ' | ' + ' | '.join(row) + ' |')
W('')

W('## Slash commandy')
W('')
rx = re.compile(r'^/([a-zA-Z0-9:_-]+)')
def slash(rows):
    c = collections.Counter()
    for o in rows:
        m = rx.match(disp(o).strip())
        if m:
            c[m.group(1).lower()] += 1
    return c
sa, sw = slash(allrows), slash(work)
W('### Vestavěné — vypovídají o praxi řízení kontextu a modelu')
W('')
W('| Příkaz | Celá historie | Pracovní projekty | Co to říká |')
W('|---|---|---|---|')
notes = {
    'compact': 'tolikrát mi kontext došel a musel se destruktivně shrnout',
    'model': 'tolikrát jsem přepínal model — volba modelu je vědomá operace, ne nastavení jednou navždy',
    'resume': 'tolikrát jsem se vracel do staré session místo psaní nové',
    'context': 'tolikrát jsem si šel ručně zkontrolovat zaplnění okna',
    'effort': 'reasoning effort přepínám řádově méně často než model',
    'clear': 'čistý reset s předáním — proti 51 kompaktacím prakticky nepoužívaný',
}
for k in ['compact', 'model', 'resume', 'context', 'effort', 'clear']:
    W('| `/' + k + '` | ' + str(sa.get(k, 0)) + '× | ' + str(sw.get(k, 0)) + '× | ' + notes[k] + ' |')
W('')
W('**Klíčový poměr:** `/compact` ' + str(sw.get('compact', 0)) + '× proti `/clear` ' + str(sw.get('clear', 0)) + '× v pracovních projektech. Kontext jsem nechával dojet do kompaktace místo řízeného resetu s předáním.')
W('')
W('### Vlastní commandy a skilly')
W('')
W('| Příkaz | Celá historie | Pracovní projekty |')
W('|---|---|---|')
for k in ['body-z-jednani', 'spec', 'spec-factory:spec', 'btw', 'dodavatele:mail', 'dodavatele:stav', 'dodavatele:hotovo', 'pruzkum', 'review-docs', 'lookup', 'learn', 'glossary', 'overview']:
    if sa.get(k, 0) or sw.get(k, 0):
        W('| `/' + k + '` | ' + str(sa.get(k, 0)) + '× | ' + str(sw.get(k, 0)) + '× |')
W('')
W('### Kompletní pořadí (pracovní projekty, vše nad 2×)')
W('')
W('| Příkaz | Počet |')
W('|---|---|')
for k, v in sw.most_common():
    if v > 2:
        W('| `/' + k + '` | ' + str(v) + '× |')
W('')

W('## Délka promptu')
W('')
def stats(rows):
    xs = sorted(len(disp(o)) for o in rows)
    def p(q):
        return xs[min(len(xs) - 1, int(q * len(xs)))]
    return xs, p
xa, pa = stats(allrows)
xw, pw = stats(work)
W('| Metrika | Celá historie | Pracovní projekty |')
W('|---|---|---|')
for lbl, q in [('minimum', None), ('p25', .25), ('medián', .5), ('p75', .75), ('p90', .9), ('p99', .99), ('maximum', None)]:
    if lbl == 'minimum':
        W('| ' + lbl + ' | ' + str(xa[0]) + ' | ' + str(xw[0]) + ' |')
    elif lbl == 'maximum':
        W('| ' + lbl + ' | ' + str(xa[-1]) + ' | ' + str(xw[-1]) + ' |')
    else:
        W('| ' + lbl + ' | ' + str(pa(q)) + ' | ' + str(pw(q)) + ' |')
W('')
W('Hodnoty ve znacích.')
W('')
W('### Histogram (pracovní projekty)')
W('')
bands = [(0, 50), (50, 100), (100, 250), (250, 500), (500, 1000), (1000, 10 ** 9)]
W('| Pásmo (znaků) | Promptů | % | Co to typicky je |')
W('|---|---|---|---|')
bn = {0: 'jednoslovné dodatky, potvrzení, slash commandy', 50: 'krátký dodatek v rozjeté konverzaci',
      100: 'jedna konkrétní otázka nebo úkol', 250: 'úkol s kontextem', 500: 'úkol s kontextem a omezeními',
      1000: 'strukturované zadání — kontext, úkol, omezení, formát výstupu'}
for lo, hi in bands:
    n = sum(1 for x in xw if lo <= x < hi)
    W('| ' + (str(lo) + '–' + str(hi) if hi < 10 ** 9 else '1000+') + ' | ' + str(n) + ' | ' + str(round(100.0 * n / len(xw), 1)) + ' % | ' + bn[lo] + ' |')
W('')
W('**Napětí, které stojí za pozornost:** medián ' + str(pw(.5)) + ' znaků, ale ' + str(sum(1 for x in xw if x > 1000)) + ' promptů nad 1000 znaků (celá historie: medián ' + str(pa(.5)) + ', ' + str(sum(1 for x in xa if x > 1000)) + ' nad 1000). Zadávání má dva režimy: velké strukturované zadání na začátku úlohy a pak desítky krátkých dodatků. Ty krátké dodatky jsou levné na napsání, ale každý z nich přeposílá celou historii znovu.')
W('')

W('## Nejdelší prompty (pracovní projekty, nad 1000 znaků)')
W('')
W('| # | Datum | Znaků | Projekt | Začátek |')
W('|---|---|---|---|---|')
longs = sorted((o for o in work if len(disp(o)) > 1000), key=lambda o: -len(disp(o)))
for i, o in enumerate(longs, 1):
    head = re.sub(r'\s+', ' ', disp(o))[:150].replace('|', '/')
    W('| ' + str(i) + ' | ' + dt(o).strftime('%Y-%m-%d %H:%M') + ' | ' + str(len(disp(o))) + ' | ' +
      proj_short.get((o.get('project') or '').lower().replace(BS, '/'), '?') + ' | ' + head + ' |')
W('')

W('## Sessions a vložený obsah')
W('')
sess = collections.defaultdict(set)
for o in work:
    sess[proj_short.get((o.get('project') or '').lower().replace(BS, '/'), '?')].add(o.get('sessionId'))
W('| Projekt | Sessions | Promptů | Promptů na session |')
W('|---|---|---|---|')
for k in cols:
    n = per.get([kk for kk, vv in proj_short.items() if vv == k][0], 0)
    s = len(sess.get(k, ()))
    W('| ' + k + ' | ' + str(s) + ' | ' + str(n) + ' | ' + (str(round(1.0 * n / s, 1)) if s else '—') + ' |')
W('')
pc = [o for o in work if o.get('pastedContents')]
W('Promptů s vloženým obsahem (`pastedContents`): **' + str(len(pc)) + '** z ' + str(len(work)) + '.')
if pc:
    sizes = sorted(len(json.dumps(o.get('pastedContents'), ensure_ascii=False)) for o in pc)
    W('Velikost vloženého obsahu ve znacích: medián ' + str(sizes[len(sizes) // 2]) + ', maximum ' + str(sizes[-1]) + '.')
W('')
W('## Poznámka k reprodukovatelnosti')
W('')
W('Když jsem tato čísla měřil, historie mezi dvěma běhy povyrostla o 4 prompty — o moje vlastní prompty z toho měření. `history.jsonl` je soubor, který roste s každým zadáním. Je to drobnost, ale dobře ilustruje, že „paměť" Claude Code je soubor na disku, ne vlastnost modelu.')
W('')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out) + '\n')
print('zapsano:', OUT, round(os.path.getsize(OUT) / 1024, 1), 'KB')
print('kontrola: pracovnich', len(work), '| celkem', len(allrows), '| longs', len(longs))
