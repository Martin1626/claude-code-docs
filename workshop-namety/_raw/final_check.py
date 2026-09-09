import re, os, subprocess

OUT = 'C:/tmp/workshop-namety/'
FILES = ['NAMETY.md', 'FUNDAMENT.md', 'DOKLADY.md', 'VYRAZENO.md']
BAD_PROJ = ['epistema', 'openclaw', 'plaudsync', 'ha-security', 'webkyskova',
            'dp-krimi', 'md-writter', 'myclaw', 'speach2text', 'laconex',
            'ventus', 'foxconn']
BAD_SEC = ['id_rsa', '.ssh/', 'credentials.json', 'ssh-key']

print('=' * 68)
print('FINALNI KONTROLA SEDMI BRAN')
print('=' * 68)

nam = open(OUT + 'NAMETY.md', encoding='utf-8').read()
karty = re.split(r'^### ([FNKRMOAUX]-\d\d) ', nam, flags=re.M)[1:]
pairs = [(karty[i], karty[i + 1]) for i in range(0, len(karty), 2)]

# BRANA 1
bez = [i for i, b in pairs if '**Doklad' not in b]
print()
print('BRANA 1 -- kazdy namet ma neprazdny doklad')
print('   karet:', len(pairs), '| bez dokladu:', len(bez), bez if bez else '')
print('   VYSLEDEK:', 'SPLNENO' if not bez else 'NESPLNENO')

# BRANA 2
demo = []
for i, b in pairs:
    m = re.search(r'\*\*Role:\*\*(.+?)·', b, re.S)
    if m and 'demo' in m.group(1):
        demo.append((i, b))
bez2 = [i for i, b in demo if 'Co ukážu na obrazovce' not in b]
vague = [i for i, b in demo
         if 'Co ukážu na obrazovce' in b
         and len(b.split('Co ukážu na obrazovce')[1].split('**Výhrada')[0].strip()) < 80]
print()
print('BRANA 2 -- kazde demo ma konkretni "co ukazu na obrazovce"')
print('   karet s demem:', len(demo), '| bez sekce:', len(bez2), '| prilis kratkych (<80 zn.):', len(vague))
print('   VYSLEDEK:', 'SPLNENO' if not bez2 and not vague else 'NESPLNENO')

# BRANA 3
f = [i for i, _ in pairs if i.startswith('F-')]
print()
print('BRANA 3 -- okruh F ma minimalne 3 namety (bezstavovost, tokenizace, kontext)')
print('   okruh F:', len(f), f)
has = {'bezstav': False, 'token': False, 'kontext': False}
for i, b in pairs:
    if not i.startswith('F-'):
        continue
    low = b.lower()
    if 'nepamatuje' in low or 'bezstav' in low:
        has['bezstav'] = True
    if 'token' in low:
        has['token'] = True
    if 'kontext' in low or 'kompaktac' in low:
        has['kontext'] = True
print('   temata:', has)
print('   VYSLEDEK:', 'SPLNENO' if len(f) >= 3 and all(has.values()) else 'NESPLNENO')

# BRANA 4
hits = {}
for fn in FILES:
    t = open(OUT + fn, encoding='utf-8').read().lower()
    for bad in BAD_PROJ + BAD_SEC:
        if bad in t:
            hits.setdefault(fn, []).append(bad)
print()
print('BRANA 4 -- zadny namet neodkazuje na projekty mimo rozsah (+ zadne citlive cesty)')
print('   nalezy:', hits if hits else 'zadne')
print('   VYSLEDEK:', 'SPLNENO' if not hits else 'NESPLNENO')

# BRANA 5
blocks = re.findall(r'^\| (\d+|P) \| (\d+) \| (\d+) \| (ano|\*\*NE\*\*) \|', nam, re.M)
over = [b for b in blocks if b[3] != 'ano']
print()
print('BRANA 5 -- kazdy blok ma soucet minut a nepresahuje 90')
print('   bloku:', len(blocks), '| presahujicich 90 min:', len(over), over if over else '')
if blocks:
    print('   minuty:', ', '.join(b[0] + '=' + b[2] for b in blocks))
print('   VYSLEDEK:', 'SPLNENO' if blocks and not over else 'NESPLNENO')

# BRANA 6
print()
print('BRANA 6 -- nic nezapsano do zadneho repozitare')
for r in ['alzask', 'fhb', 'shared', 'myfaber']:
    p = 'C:/Git/' + r
    try:
        o = subprocess.run(['git', 'status', '--porcelain'], capture_output=True,
                           text=True, cwd=p, timeout=60).stdout.strip()
    except Exception as e:
        print('  ', r, 'CHYBA:', e)
        continue
    n = len([x for x in o.splitlines() if x.strip()])
    print('  ', r + ':', n, 'zmen')
    for ln in o.splitlines()[:6]:
        print('       ', ln)

# BRANA 7
x = [i for i, _ in pairs if i.startswith('X-')]
print()
print('BRANA 7 -- pocet nametu v okruhu X je nenulovy')
print('   okruh X:', len(x), x)
print('   VYSLEDEK:', 'SPLNENO' if x else 'NESPLNENO')

# doplnkove statistiky
print()
print('=' * 68)
print('STATISTIKY KATALOGU')
print('=' * 68)
okruhy = {}
mins = {}
prio = {'must': 0, 'should': 0, 'could': 0}
for ln in nam.split('\n'):
    m = re.match(r'\|\s*([FNKRMOAUX])-(\d\d)\s*\|\s*\w\s*\|.+?\|.+?\|\s*(\d+)\s*\|\s*(must|should|could)\s*\|', ln)
    if m:
        okruhy[m.group(1)] = okruhy.get(m.group(1), 0) + 1
        mins[m.group(1)] = mins.get(m.group(1), 0) + int(m.group(3))
        prio[m.group(4)] += 1
print('nametu celkem:', sum(okruhy.values()), '| minut celkem:', sum(mins.values()))
for k in 'FNKRMOAUX':
    if k in okruhy:
        print('  ', k, ':', okruhy[k], 'nametu,', mins[k], 'min')
print('priority:', prio)
print()
print('velikosti vystupu:')
for fn in FILES:
    print('  ', fn, round(os.path.getsize(OUT + fn) / 1024, 1), 'KB')
raw = [f for f in os.listdir(OUT + '_raw') if f.endswith('.md')]
print('  _raw/: ', len(raw), 'md souboru +',
      len([f for f in os.listdir(OUT + '_raw') if f.endswith('.py')]), 'skriptu')
