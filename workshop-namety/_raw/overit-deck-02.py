# -*- coding: utf-8 -*-
u"""Ověří, že čísla v decku 2. sezení odpovídají skutečnosti na disku.
Nesedící číslo je chyba, ne zaokrouhlení.

Přepsáno 2026-09-11 po přestavbě decku na osm témat po dvou snímcích
(indexové soubory, zápisy, ADR, FR, TC, ontologie, dodavatelé, skilly a pluginy).
Předchozí verze kontrolovala slidy o kostře projektu a vrstvách autority,
které v decku už nejsou — ta měření zůstávají v DOKLADY.md část 6.
"""
import collections
import glob
import io
import os
import re

DECK = r'C:\Git\shared\docs\claude-code\claude-code-struktura-a-zdroje.html'
ALZ = r'C:\Git\alzask'
FHB = r'C:\Git\fhb'
ONT = os.path.join(ALZ, 'docs', 'ontology')

d = io.open(DECK, encoding='utf-8').read()
chyby = []


def zkontroluj(popis, vzor, ocekavano):
    u"""Ověří, že se v decku u daného vzoru vyskytuje očekávaná hodnota."""
    nalez = re.findall(vzor, d)
    ok = any(n.replace(u'\u00a0', ' ').replace(' ', '') == str(ocekavano).replace(' ', '')
             for n in nalez)
    print('  %-42s deck %-20s disk %-10s %s'
          % (popis, (nalez[:3] if nalez else 'NENALEZENO'), ocekavano, 'OK' if ok else 'NESEDI'))
    if not ok:
        chyby.append(popis)


def rovno(popis, v_decku, na_disku):
    ok = str(v_decku) == str(na_disku)
    print('  %-42s deck %-20s disk %-10s %s' % (popis, v_decku, na_disku, 'OK' if ok else 'NESEDI'))
    if not ok:
        chyby.append(popis)


# ---------------------------------------------------------------- 03/04 indexy
print('INDEXOVE SOUBORY (slidy 03-04)')
zapisu = len(glob.glob(os.path.join(ALZ, 'docs', 'meetings', '*.md')))
adr = glob.glob(os.path.join(ALZ, 'docs', 'adr', '*', 'ADR-*.md'))
zkontroluj(u'zápisů ze schůzek', r'<b>(\d+)</b> zápisů v <code>docs/meetings/</code>', zapisu)
zkontroluj(u'ADR celkem — dlaždice', r'<b>(\d+)</b><span>rozhodnutí</span>', len(adr))

idx = io.open(os.path.join(ALZ, 'docs', 'adr', 'INDEX.md'), encoding='utf-8').read(2000)


def z_indexu(klic):
    m = re.search(r'\|\s*%s\s*\|\s*(\d+)\s*\|' % klic, idx)
    return m.group(1) if m else '?'


zkontroluj(u'ADR ve výpisu INDEX.md', r'\| Celkem ADR \|\s+<span class="w">(\d+)</span>', z_indexu(u'Celkem ADR'))
zkontroluj(u'aktivních', r'\| Aktivních\s+\|\s+<span class="w">(\d+)</span>', z_indexu(u'Aktivních'))
zkontroluj(u'navržených', r'\| Navržených \|\s+<span class="w">(\d+)</span>', z_indexu(u'Navržených'))

kat = collections.Counter(os.path.basename(os.path.dirname(f)) for f in adr)
for jmeno, adresar in [(u'process/', 'process'), (u'api/', 'api'), (u'hw/', 'hw'),
                       (u'db/', 'db'), (u'integration/', 'integration')]:
    zkontroluj(u'kategorie %s' % jmeno,
               r'\| %s\s*\|\s*(\d+) \|' % re.escape(jmeno), kat[adresar])

indexu = len(glob.glob(os.path.join(ALZ, 'docs', 'adr', 'INDEX.md'))) + \
    len(glob.glob(os.path.join(ALZ, 'docs', 'adr', '*', 'INDEX.md')))
rovno(u'rejstříků v docs/adr (deck říká 7)', 7, indexu)

# ------------------------------------------------------------------- 09/10 FR
print('\nFR (slidy 09-10)')
fr = len([f for f in glob.glob(os.path.join(ALZ, 'docs', 'fr', '**', 'FR-*.md'), recursive=True)])
zkontroluj(u'požadavků', r'<h3>(\d+) požadavk\w+, dvě sekce</h3>', fr)

# ------------------------------------------------------------------- 11/12 TC
print('\nTC (slidy 11-12)')
feat = glob.glob(os.path.join(ALZ, 'docs', 'fr', '**', '*.feature'), recursive=True)
csv = io.open(os.path.join(ALZ, 'docs', 'fr', 'tc-list.csv'), encoding='utf-8-sig').read()
radky = [r.split(';') for r in csv.strip().split('\n')[1:] if r.strip()]
h = csv.strip().split('\n')[0].split(';')
stav = collections.Counter(r[h.index('Stav')] for r in radky)
klas = collections.Counter(r[h.index('Klasifikace')] for r in radky)
zkontroluj(u'scénářů', r'<b>(\d+)</b><span>scénářů</span>', len(radky))
zkontroluj(u'testovacích případů', r'<b>(\d+)</b><span>testovacích případů</span>',
           len(set(r[0].split('.')[0] for r in radky)))
zkontroluj(u'souborů .feature', r'<b>(\d+)</b><span>souborů</span>', len(feat))
zkontroluj(u'hotových scénářů', r'<b>(\d+)</b><span>hotových</span>', stav['done'])
zkontroluj(u'rozepsaných v poznámce', r'zbylých (\d+) je rozepsaných', stav['draft'])
zkontroluj(u'negativních v kickeru', r'Negativních scénářů je (\d+) z', klas['negative'])
zkontroluj(u'z kolika v kickeru', r'Negativních scénářů je \d+ z (\d+)', len(radky))

# ------------------------------------------------------------ 13/14 ontologie
print('\nONTOLOGIE (slidy 13-14)')
hlav = io.open(os.path.join(ONT, 'INDEX.md'), encoding='utf-8').read(1500)
m = re.search(r'\*\*(\d+) entit\*\*.*?\*\*(\d+) vztahů\*\*\s*·\s*\*\*(\d+) atributů\*\*'
              r'\s*·\s*\*\*(\d+) rozporů\*\*', hlav, re.S)
assert m, 'hlavicku INDEX.md se nepodarilo precist'
ent, vaz, atr, roz = m.groups()
zkontroluj(u'prvků', r'<b>(\d+)</b><span>prvků</span>', ent)
zkontroluj(u'vazeb', r'<b>(\d+)</b><span>vazeb</span>', vaz)
zkontroluj(u'atributů', r'<b>(\d+)</b><span>atributů</span>', atr)
zkontroluj(u'rozporů', r'>(\d+)</b><span>rozporů</span>', roz)
vsech = glob.glob(os.path.join(ONT, 'entities', '*.md'))
karet = len([f for f in vsech if not f.endswith('.notes.md')])
zkontroluj(u'karet prvků', r'<td>(\d+) karet</td>', karet)

# kB = 1000 B (SI), stejně jako to počítá deck i DOKLADY.md část 6.5
for jmeno, vzor in [('INDEX.md', r'<td>INDEX\.md</td><td>(\d+) kB</td>'),
                    ('TERMS.tsv', r'<td>TERMS\.tsv</td><td>(\d+) kB</td>'),
                    ('RELATIONS.tsv', r'<td>RELATIONS\.tsv</td><td>(\d+) kB</td>'),
                    ('conflicts.md', r'<td>conflicts\.md</td><td>(\d+) kB</td>')]:
    zkontroluj(u'velikost %s' % jmeno, vzor,
               int(round(os.path.getsize(os.path.join(ONT, jmeno)) / 1000.0)))
mb = os.path.getsize(os.path.join(ONT, 'ontology.yaml')) / 1000000.0
zkontroluj(u'velikost ontology.yaml', r'ontology\.yaml</td><td class="win">([\d,]+) MB</td>',
           ('%.1f' % mb).replace('.', ','))

# ---------------------------------------------------------- 15/16 dodavatele
print('\nDODAVATELE (slidy 15-16)')
q = io.open(os.path.join(ALZ, 'docs', 'suppliers', 'QUESTIONS.tsv'), encoding='utf-8').read()
qh = q.split('\n')[0].split('\t')
qr = [r.split('\t') for r in q.split('\n')[1:] if r.strip()]
st = collections.Counter(r[qh.index('status')] for r in qr)
li = qh.index('landed_in')
zkontroluj(u'otázek', r'<b>(\d+)</b><span>otázek</span>', len(qr))
zkontroluj(u'zodpovězeno', r'<b>(\d+)</b><span>zodpovězeno</span>', st['Answered'])
zkontroluj(u'částečně', r'>(\d+)</b><span>částečně</span>', st['Partially'])
zkontroluj(u'bez odpovědi', r'<b>(\d+)</b><span>bez odpovědi</span>', st['No answer'])
zkontroluj(u'odmítnutých', r'a (\d+) odmítnutých', st['Declined'])
zkontroluj(u'vyplněné landed_in', r'Ze 152 otázek ho má vyplněných (\d+)',
           sum(1 for r in qr if len(r) > li and r[li].strip()))
zkontroluj(u'kolik otázek v té větě', r'Ze (\d+) otázek ho má vyplněných',  len(qr))

# ------------------------------------------------------ 17/18 skilly a pluginy
print('\nSKILLY A PLUGINY (slidy 17-18)')
sk = glob.glob(os.path.join(ALZ, '.claude', 'skills', '*', 'SKILL.md'))
cmds = glob.glob(os.path.join(ALZ, '.claude', 'commands', '**', '*.md'), recursive=True)
ag = glob.glob(os.path.join(ALZ, '.claude', 'agents', '*.md'))
fag = glob.glob(os.path.join(FHB, '.claude', 'agents', 'spec-*.md'))
rovno(u'skillů alzask (deck říká dva)', 2, len(sk))
zkontroluj(u'příkazů a agentů', r'(Devět) příkazů, pět revizních agentů\.',
           u'Devět' if len(cmds) == 9 else u'jiný počet (%d)' % len(cmds))
rovno(u'agentů alzask (deck říká pět)', 5, len(ag))
rovno(u'agentů fhb (deck říká sedmice)', 7, len(fag))
gen = io.open(sk[0] if 'ontologie' in sk[0] else sk[-1], encoding='utf-8').read(900)
rovno(u'skill ontologie je generovaný', True, 'GENEROVANO' in gen)

print('\n%s' % ('VSE SEDI' if not chyby else 'NESEDI: %s' % ', '.join(chyby)))
