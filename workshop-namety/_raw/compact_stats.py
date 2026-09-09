import json, os, glob, collections, datetime

DIRS = {
    'alzask': 'C:/Users/ai_martint/.claude/projects/c--Git-alzask',
    'fhb': 'C:/Users/ai_martint/.claude/projects/c--Git-fhb',
}
OUT = 'C:/tmp/workshop-namety/_raw/doklady-kompaktace.md'


def num(x):
    return x if isinstance(x, (int, float)) else 0


raw = []
sess_stat = {}
for proj, d in DIRS.items():
    if not os.path.isdir(d):
        continue
    files = glob.glob(os.path.join(d, '*.jsonl'))
    sess_stat[proj] = (len(files), sum(os.path.getsize(f) for f in files) / 1048576)
    for fp in files:
        with open(fp, encoding='utf-8', errors='replace') as f:
            for line in f:
                line = line.strip()
                if not line or 'compactMetadata' not in line:
                    continue
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                cm = o.get('compactMetadata')
                if not isinstance(cm, dict):
                    continue
                raw.append({
                    'proj': proj,
                    'session': os.path.basename(fp)[:8],
                    'ts': str(o.get('timestamp') or ''),
                    'trigger': cm.get('trigger'),
                    'pre': num(cm.get('preTokens')),
                    'post': num(cm.get('postTokens')),
                    'cum': num(cm.get('cumulativeDroppedTokens')),
                    'ms': num(cm.get('durationMs')),
                })

# DEDUPLIKACE: fork/resume kopiruje zaznam do noveho souboru session,
# takze tataz udalost je zapsana vickrat. Identita udalosti = (timestamp, pre, post).
seen = {}
dups = 0
for r in raw:
    key = (r['ts'][:19], r['pre'], r['post'])
    if key in seen:
        dups += 1
        seen[key]['also_in'].append(r['session'])
        continue
    r['also_in'] = []
    seen[key] = r
recs = sorted(seen.values(), key=lambda r: r['ts'])

# KROK zahozenych tokenu = pre - post (prime, nezavisle na kumulativu).
# Puvodni verze skriptu pocitala krok jako rozdil cumulativeDroppedTokens
# keyovany podle session ID -- a fork session ma jine ID, takze prvni zaznam
# ve forku dostal cely kumulativ jako "krok". Odtud nadhodnoceni o 36 %.
for r in recs:
    r['step'] = r['pre'] - r['post']

out = []
W = out.append
W('# Doklady o kompaktaci kontextu — z transkriptů')
W('')
W('Zdroj: `~/.claude/projects/c--Git-alzask/*.jsonl` a `...c--Git-fhb/*.jsonl`, odečteno '
  + datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + '.')
W('')
W('Kompaktace se v transkriptu značí záznamem s `isCompactSummary: true` a klíčem')
W('`compactMetadata`, doplněným systémovým záznamem `system/compact_boundary`. Metadata')
W('nesou přesná čísla, takže se nemusí nic odhadovat.')
W('')
W('## Tři výhrady, které patří k těmto číslům')
W('')
W('**1. Deduplikace.** Fork a obnovení session kopírují záznam o kompaktaci do dalšího')
W('souboru, takže tatáž událost je v datech vícekrát. Identita události je zde určena')
W('trojicí (čas, tokeny před, tokeny po). Nalezeno **' + str(dups) + ' duplikátů**, které')
W('jsou z počtů vyřazené. První verze tohoto souboru je vykazovala jako samostatné')
W('kompaktace — chyba nalezená red-teamem.')
W('')
W('**2. Krok se počítá jako `před − po`,** ne jako rozdíl kumulativních součtů. Původní')
W('verze skriptu odečítala `cumulativeDroppedTokens` proti předchozímu záznamu **téže')
W('session** — a protože fork má jiné ID session, první záznam ve forku dostal celý')
W('kumulativ jako jeden krok. Součet tím byl nadhodnocený o 36 %.')
W('')
W('**3. Je to podvýběr, ne úplný počet.** Historie příkazů zná 51× `/compact` v pracovních')
W('projektech, ale transkriptů na disku je jen 84 souborů (historie zná 175 sessions jen')
W('pro alzask). Čísla níže tedy popisují **vzorek**, ne všechny kompaktace.')
W('')
W('**A ještě jedna, obecnější.** Dokumentace parsování těchto souborů výslovně')
W('nedoporučuje — formát je interní a mění se mezi verzemi. Doporučená cesta je `/export`')
W('nebo `claude -p --output-format json`. Tato čísla platí pro tuto verzi.')
W('')
W('| Projekt | Sessions | MB transkriptů |')
W('|---|---|---|')
for p, (n, mb) in sess_stat.items():
    W('| ' + p + ' | ' + str(n) + ' | ' + str(round(mb, 1)) + ' |')
W('')
W('## Co obsahuje `compactMetadata`')
W('')
W('| Klíč | Význam |')
W('|---|---|')
W('| `trigger` | `manual` (napsal jsem `/compact`) nebo `auto` (harness zasáhl sám před stropem) |')
W('| `preTokens` | kolik tokenů měl kontext **před** kompaktací |')
W('| `postTokens` | kolik tokenů zůstalo **po** ní |')
W('| `cumulativeDroppedTokens` | kolik se v této session zahodilo celkem (POZOR: kumulativ, ne krok) |')
W('| `durationMs` | jak dlouho kompaktace trvala |')
W('| `preservedSegment` | ukazatel na část konverzace zachovanou doslovně |')
W('')

W('## Všechny zaznamenané kompaktace (po deduplikaci)')
W('')
W('| # | Datum | Projekt | Session | Trigger | Před | Po | Zahozeno | Ubylo | Trvalo |')
W('|---|---|---|---|---|---|---|---|---|---|')


def sp(n):
    return '{:,}'.format(int(n)).replace(',', ' ')


for i, r in enumerate(recs, 1):
    pct = (100.0 * r['step'] / r['pre']) if r['pre'] else 0
    ts = r['ts'][:16].replace('T', ' ')
    W('| ' + str(i) + ' | ' + ts + ' | ' + r['proj'] + ' | `' + r['session'] + '` | '
      + str(r['trigger']) + ' | ' + sp(r['pre']) + ' | ' + sp(r['post']) + ' | '
      + sp(r['step']) + ' | ' + str(round(pct, 1)) + ' % | ' + str(round(r['ms'] / 1000.0, 1)) + ' s |')
W('')

n = len(recs)
pres = sorted(r['pre'] for r in recs if r['pre'])
posts = sorted(r['post'] for r in recs if r['post'])
pcts = sorted(100.0 * r['step'] / r['pre'] for r in recs if r['pre'])
mss = sorted(r['ms'] for r in recs if r['ms'])
trig = collections.Counter(r['trigger'] for r in recs)
total = sum(r['step'] for r in recs)


def med(xs):
    return xs[len(xs) // 2] if xs else 0


W('## Souhrn')
W('')
W('| Metrika | Hodnota |')
W('|---|---|')
W('| Zaznamenaných kompaktací (po deduplikaci) | **' + str(n) + '** |')
W('| Vyřazených duplikátů | ' + str(dups) + ' |')
W('| Ručních (`/compact`) / automatických | **' + str(trig.get('manual', 0)) + ' / ' + str(trig.get('auto', 0)) + '** |')
W('| Medián kontextu před kompaktací | ' + sp(med(pres)) + ' tokenů |')
W('| Maximum před kompaktací | ' + sp(max(pres)) + ' tokenů |')
W('| Medián kontextu po kompaktaci | ' + sp(med(posts)) + ' tokenů |')
W('| **Medián podílu zahozeného kontextu** | **' + str(round(med(pcts), 1)) + ' %** |')
W('| Rozsah zahozeného podílu | ' + str(round(pcts[0], 1)) + ' % – ' + str(round(pcts[-1], 1)) + ' % |')
W('| Medián doby kompaktace | ' + str(round(med(mss) / 1000.0, 1)) + ' s |')
W('| Nejdelší kompaktace | ' + str(round(mss[-1] / 1000.0, 1)) + ' s |')
W('| **Celkem zahozeno tokenů** | **' + sp(total) + '** |')
W('')
W('Medián páru před/po je ' + sp(med(pres)) + ' → ' + sp(med(posts)) + '. Pozor: to nejsou')
W('dvě hodnoty téže kompaktace, jsou to dva nezávislé mediány — proto se z nich nemá')
W('počítat procento. Mediánový **podíl** je uvedený zvlášť výše.')
W('')

per_sess = collections.defaultdict(int)
per_cnt = collections.Counter()
for r in recs:
    per_sess[(r['proj'], r['session'])] += r['step']
    per_cnt[(r['proj'], r['session'])] += 1
W('### Sessions s nejvíc zahozeným kontextem')
W('')
W('| Projekt | Session | Kompaktací | Zahozeno tokenů |')
W('|---|---|---|---|')
for (p, s), v in sorted(per_sess.items(), key=lambda kv: -kv[1])[:10]:
    W('| ' + p + ' | `' + s + '` | ' + str(per_cnt[(p, s)]) + ' | ' + sp(v) + ' |')
W('')
W('## Jak to čítat na workshopu')
W('')
W('Medián zahozeného podílu je **' + str(round(med(pcts), 1)) + ' %.** Po typické kompaktaci')
W('zůstane z konverzace zlomek; zbytek je nahrazený shrnutím. Shrnutí drží záměr a')
W('rozhodnutí, ale doslovné výstupy nástrojů, čísla řádků a přesné citace v něm nejsou.')
W('Analytik, který se opírá o `soubor:řádek`, po kompaktaci pracuje s vyprávěním o zdroji.')
W('')
W('Druhá, méně zjevná cena je čas: medián **' + str(round(med(mss) / 1000.0, 1)) + ' s**,')
W('nejdéle ' + str(round(mss[-1] / 1000.0, 1)) + ' s. Kompaktace není okamžitá operace — je to')
W('další volání modelu, které musí přečíst celou dosavadní konverzaci.')
W('')
W('A třetí věc, nejdůležitější: **ani jedna z těch kompaktací nebyla vyvolaná automaticky**')
W('a **ani jedna neměla instrukci.** `/compact` přijímá argument (`/compact zachovej …`),')
W('kterým se dá říct, co má souhrn udržet. Nevyužil jsem to ani jednou.')

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out) + '\n')

print('zapsano:', OUT)
print('surovych zaznamu:', len(raw), '| po deduplikaci:', n, '| duplikatu:', dups)
print('celkem zahozeno:', sp(total))
print('median pre:', sp(med(pres)), '| median post:', sp(med(posts)), '| median podil:', round(med(pcts), 1), '%')
print('median doba:', round(med(mss) / 1000.0, 1), 's | trigger:', dict(trig))
