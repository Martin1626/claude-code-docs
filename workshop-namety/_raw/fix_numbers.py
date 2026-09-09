import os, re

# Oprava cisel po nalezu RT-14 (red-team): duplikaty a smichane metriky.
# Stare -> nove:
#   21 kompaktaci        -> 19
#   11 700 496 tokenu    -> 8 601 191
#   583 578 -> 12 127    -> 464 352 -> 13 344 (a nepocitat z toho procento)
#   177,5 s              -> 180,7 s
#   224,1 s              -> zkontrolovat v novem souboru

FILES = [
    'C:/tmp/workshop-namety/FUNDAMENT.md',
    'C:/tmp/workshop-namety/NAMETY.md',
    'C:/tmp/workshop-namety/VYRAZENO.md',
    'C:/tmp/workshop-namety/_raw/korekce-pro-syntezu.md',
    'C:/tmp/workshop-namety/_raw/katalog-draft.md',
]

SUBS = [
    # celkovy soucet
    (r'11\s?700\s?496', '8 601 191'),
    (r'11,7\s?milionu', '8,6 milionu'),
    (r'11,7\s?mil\.', '8,6 mil.'),
    # pocet kompaktaci
    (r'\b21\s+kompaktac[ií]', '19 kompaktací'),
    (r'\b21\s+zaznamenaných\s+kompaktac', '19 zaznamenaných kompaktac'),
    (r'21\s+zaznamenaných\s+kompaktacích', '19 zaznamenaných kompaktacích'),
    (r'21\s*/\s*0\b', '19 / 0'),
    (r'\b21\s+ručních\s+a\s+0', '19 ručních a 0'),
    (r'21×\s*`manual`,\s*0×\s*`auto`', '19× `manual`, 0× `auto`'),
    (r'21\s+z\s+21\s+ručn', '19 z 19 ručn'),
    (r've\s+všech\s+21\s+zaznamenaných', 've všech 19 zaznamenaných'),
    (r'z\s+21\s+kompaktac[ií]', 'z 19 kompaktací'),
    (r'těch\s+21\s+je', 'těch 19 je'),
    (r'21\s+je\s+\*\*podvýběr', '19 je **podvýběr'),
    (r'21\s+kompaktací\s+z\s+transkriptů', '19 kompaktací z transkriptů'),
    # medianovy par
    (r'583\s?578\s*(→|->)\s*12\s?127', '464 352 → 13 344'),
    (r'583\s?578', '464 352'),
    (r'12\s?127', '13 344'),
    # doba
    (r'177,5\s*s', '180,7 s'),
    (r'177\s*s', '181 s'),
]

for fp in FILES:
    if not os.path.isfile(fp):
        print('CHYBI:', fp)
        continue
    with open(fp, encoding='utf-8') as f:
        t = f.read()
    orig = t
    hits = {}
    for pat, rep in SUBS:
        t, n = re.subn(pat, rep, t)
        if n:
            hits[pat] = n
    if t != orig:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(t)
        print('OPRAVENO', os.path.basename(fp), '->', sum(hits.values()), 'zmen')
        for k, v in hits.items():
            print('    ', v, 'x', k)
    else:
        print('bez zmeny', os.path.basename(fp))

# kontrola, ze nikde nezustala stara cisla
print()
print('--- kontrola zbytku ---')
BAD = ['11 700 496', '11,7 milionu', '583 578', '12 127', '177,5']
for fp in FILES:
    if not os.path.isfile(fp):
        continue
    with open(fp, encoding='utf-8') as f:
        t = f.read()
    for b in BAD:
        if b in t:
            print('ZBYVA', os.path.basename(fp), ':', b)
print('hotovo')
