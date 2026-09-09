# Rozdeleni do dilu serie + KONTROLA souctu (draft mel 3 z 6 bloku spatne secteno).
# Zdroj minut = souhrnna tabulka v n2-tabulka-FN.md, parsovana automaticky.
import re, os

TAB = 'C:/tmp/workshop-namety/_raw/n2-tabulka-FN.md'
OUT = 'C:/tmp/workshop-namety/_raw/n5-bloky.md'

minutes, names, roles, prio = {}, {}, {}, {}
with open(TAB, encoding='utf-8') as f:
    for ln in f:
        m = re.match(r'\|\s*([FNKRMOAUX]-\d\d)\s*\|\s*\w\s*\|\s*(.+?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*(must|should|could)\s*\|', ln)
        if m:
            i, nm, ro, mi, pr = m.group(1), m.group(2), m.group(3), int(m.group(4)), m.group(5)
            minutes[i] = mi
            names[i] = nm.replace(' ⚑', '').replace(' ⚠', '')
            roles[i] = ro
            prio[i] = pr

print('nacteno namietu:', len(minutes), '| celkem minut:', sum(minutes.values()))

# Dily navrzene tak, aby ZADNY neprekrocil 90 minut (brana c. 5 zadani).
# Cil: kazdy dil ma jedno tema a da se odejit s jednou vetou.
DILY = [
    ('0', 'Příprava (nepřednáší se)',
     ['N-06'],
     'Cvičný repozitář, na kterém se smí rozbíjet. Bez něj polovina dem nejde předvést.'),
    ('1', 'Co se pod tím děje a co tě to stojí',
     ['F-01', 'F-02', 'F-05', 'N-05', 'F-03', 'F-04'],
     'Model si nic nepamatuje, celá historie se posílá znovu, a proto dlouhá session '
     'zdražuje každý další prompt. Kompaktace session zachrání, ale zahodí 97 % — a dá se '
     'jí říct, co má nechat.'),
    ('2', 'Než pustíš agenta na svá data',
     ['N-01', 'N-02', 'N-03', 'M-02', 'N-04'],
     'Tři zákazy, tři úrovně zpět, vestavěný režim plánování a jedna věta („nic neměň"). '
     'A jedno pravidlo, které se nedá vzít zpátky: prompt je zápis, ne rozhovor.'),
    ('3', 'Zadání: dokument nese kontext, prompt nese rozhodnutí',
     ['K-01', 'R-01', 'K-02', 'X-04', 'K-03', 'A-02'],
     'Krátký prompt funguje jen nad postaveným kontextem. Dlouhé zadání patří do souboru — '
     'dá se revidovat, spustit znovu a je v Gitu.'),
    ('4', 'Jak se ptát, aby odpověď byla k něčemu',
     ['A-04', 'A-03', 'A-05', 'K-04', 'A-09', 'U-04'],
     'Hypotéza místo otázky, rozpočet na otázky, páka místo nejasnosti, a útok na náklad '
     'údržby — čtyři věty, které z modelu udělají oponenta místo pochlebovače.'),
    ('5', 'Když to nejde: zmenši úlohu, ne prompt',
     ['A-06', 'A-07', 'X-03', 'O-05'],
     'Po třetím nepovedeném kole nepiš čtvrtý prompt — zmenši úlohu a napiš invariant. '
     'A poznej tři situace, kdy je ruční práce rychlejší.'),
    ('6', 'Proč to, co postavíš, přestaneš používat',
     ['M-01', 'K-07', 'X-02', 'U-02', 'X-01', 'M-07'],
     'Nejsilnější a nejnepříjemnější díl. Brána, kterou nikdo nespouští, je taky jen '
     'prompt — a mezi „postaveno" a „používáno" je propast, kterou je vidět na vlastních '
     'datech.'),
    ('7', 'Revize a kvalita bez slepé automatiky',
     ['M-03', 'M-05', 'M-06', 'M-04', 'A-08'],
     'Dva ze tří nálezů jsou falešné, takže triáž nesmí dělat model. Vykazuj, kolik jsi '
     'NEzkontroloval. A nenech sémantickou kontrolu předstírat, že dělá práci deterministické.'),
    ('8', 'Orchestrace: kam jde hluk',
     ['O-01', 'O-02', 'O-03', 'O-04'],
     'Subagent se nepoužívá pro rychlost, ale proto, že jeho hluk zůstane mimo tvůj '
     'kontext. Model se vybírá podle povahy úlohy — a stojí za to změřit, jestli to k něčemu bylo.'),
    ('9', 'Vlastní výbava a jak ji předat dál',
     ['R-02', 'R-04', 'R-03', 'U-05', 'U-06', 'R-05'],
     'Metodika bez spouštěče je jen text. Skill a příkaz jsou to, co postup skutečně '
     'spustí — a Git je to, co ho dá kolegovi.'),
    ('10', 'Velký audit a co z toho všeho žije',
     ['A-01', 'U-01', 'U-03', 'U-07'],
     'Vrstvový audit jako vrchol série: tytéž skutečnosti ve třech dokumentech, rozpory '
     'na hranicích vrstev. A závěr: drží se to, co má spouštěč nebo nulovou cenu vyvolání.'),
    ('P', 'Příloha pro toho, kdo bude stavět nástroje',
     ['K-05', 'M-08', 'K-06'],
     'Nepatří do hlavní série. Kdo bude stavět validátory a kontrolu citací pro tým, '
     'najde tu zásady i cenu.'),
]

out = []
W = out.append
W('---')
W('')
W('# Návrh dílů série')
W('')
W('**Podmínka, kterou návrh drží:** žádný díl nepřekračuje **90 minut** čistého obsahu.')
W('Součty jsou spočítané skriptem (`_raw/n5-bloky.py`) z minut v souhrnné tabulce, ne')
W('odhadem — draft měl tři ze šesti bloků sečtené špatně a red-team to našel.')
W('')
W('**Jak návrh čítat.** Katalog má 56 námětů a 694 minut, což je při kratších setkáních')
W('deset až jedenáct dílů. To je hodně — ale katalog je **zásoba, ne program**. Pokud')
W('série má být kratší, škrtej podle priority (`must` je 37 námětů) nebo vezmi jen díly')
W('1, 3 a 6, které nesou tři hlavní myšlenky. Díl 0 a příloha `P` se nepřednáší.')
W('')

total_all = 0
for code, tema, ids, veta in DILY:
    mins = [minutes.get(i, 0) for i in ids]
    s = sum(mins)
    if code not in ('0', 'P'):
        total_all += s
    flag = '' if s <= 90 else '  ⚠ PŘEKRAČUJE 90 MIN'
    W('## Díl ' + code + ' — ' + tema)
    W('')
    W('**' + str(s) + ' minut**' + flag + ' · ' + str(len(ids)) + ' námětů')
    W('')
    W('| ID | Námět | Role | Min | Prio |')
    W('|---|---|---|---|---|')
    for i in ids:
        W('| ' + i + ' | ' + names.get(i, '?') + ' | ' + roles.get(i, '?') + ' | '
          + str(minutes.get(i, 0)) + ' | ' + prio.get(i, '?') + ' |')
    W('')
    W('**Co si z toho odnesou:** ' + veta)
    W('')

W('## Kontrola součtů')
W('')
W('| Díl | Námětů | Minut | Do 90 min? |')
W('|---|---|---|---|')
for code, tema, ids, veta in DILY:
    s = sum(minutes.get(i, 0) for i in ids)
    W('| ' + code + ' | ' + str(len(ids)) + ' | ' + str(s) + ' | ' + ('ano' if s <= 90 else '**NE**') + ' |')
W('')
covered = set()
for _, _, ids, _ in DILY:
    covered |= set(ids)
missing = sorted(set(minutes) - covered)
extra = sorted(covered - set(minutes))
W('Přednášených dílů 1–10: **' + str(total_all) + ' minut.** Plus příprava (díl 0) a příloha `P`.')
W('')
W('Námětů v tabulce: ' + str(len(minutes)) + ' · zařazených do dílů: ' + str(len(covered))
  + ' · nezařazených: ' + str(len(missing)))
if missing:
    W('')
    W('**Nezařazené:** ' + ', '.join(missing))
if extra:
    W('')
    W('**V dílech, ale ne v tabulce (chyba):** ' + ', '.join(extra))
W('')
W('---')
W('')
W('## Tři možné střihy, kdyby série měla být kratší')
W('')
W('| Varianta | Díly | Minut | Co publikum dostane |')
W('|---|---|---|---|')
v1 = sum(minutes.get(i, 0) for _, _, ids, _ in DILY if _ in ('1', '3', '6') for i in ids)
W('| **Tři díly** | 1, 3, 6 | '
  + str(sum(sum(minutes.get(i, 0) for i in ids) for c, _, ids, _ in DILY if c in ('1', '3', '6')))
  + ' | mechanika, zadávání, a proč postavené věci umírají |')
W('| **Pět dílů** | 1, 2, 3, 6, 7 | '
  + str(sum(sum(minutes.get(i, 0) for i in ids) for c, _, ids, _ in DILY if c in ('1', '2', '3', '6', '7')))
  + ' | plus bezpečné pouštění agenta a revizní disciplína |')
W('| **Celá série** | 1–10 | ' + str(total_all) + ' | vše včetně velkého auditu a předání kolegovi |')
W('')
W('U každé varianty platí, že **díl 0 (cvičný repozitář) musí existovat předem.**')

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(out) + '\n')

print('zapsano:', OUT)
print('prednasenych minut (1-10):', total_all)
print('nezarazene:', missing)
print('prebyvajici:', extra)
for code, tema, ids, veta in DILY:
    s = sum(minutes.get(i, 0) for i in ids)
    if s > 90:
        print('!!! DIL', code, 'ma', s, 'min')
