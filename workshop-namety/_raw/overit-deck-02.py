# -*- coding: utf-8 -*-
"""Ověří, že čísla v decku 2. sezení odpovídají skutečnosti na disku.
Nesedící číslo je chyba, ne zaokrouhlení.
"""
import io
import os
import re
import glob

DECK = r'C:\Git\shared\docs\claude-code\claude-code-struktura-a-zdroje.html'
ALZ = r'C:\Git\alzask'
FHB = r'C:\Git\fhb'
ONT = os.path.join(ALZ, 'docs', 'ontology')

d = io.open(DECK, encoding='utf-8').read()
chyby = []


def zkontroluj(popis, vzor, ocekavano):
    """Ověří, že se v decku vyskytuje očekávaná hodnota u daného vzoru."""
    nalez = re.findall(vzor, d)
    ok = any(n.replace('\u00a0', ' ').replace(' ', '') == str(ocekavano).replace(' ', '') for n in nalez)
    print('  %-46s deck %-24s disk %-10s %s'
          % (popis, (nalez[:3] if nalez else 'NENALEZENO'), ocekavano, 'OK' if ok else 'NESEDI'))
    if not ok:
        chyby.append(popis)


def podadresare(root):
    p = os.path.join(root, 'docs')
    return sorted(n for n in os.listdir(p)
                  if os.path.isdir(os.path.join(p, n)) and not n.startswith('.'))


def pravidla(root):
    ids = set()
    for f in glob.glob(os.path.join(root, '.claude', 'rules', 'shared', '*.md')):
        m = re.match(r'(RULE-[A-Z]+-\d+)', os.path.basename(f))
        if m:
            ids.add(m.group(1))
    return ids


print('STRUKTURA PROJEKTU')
a_docs, f_docs = podadresare(ALZ), podadresare(FHB)
spol = sorted(set(a_docs) & set(f_docs))
zkontroluj('docs/ alzask', r'<b>(\d+)</b><span>adresářů docs/ · alzask', len(a_docs))
zkontroluj('docs/ fhb', r'<b>(\d+)</b><span>adresářů docs/ · fhb', len(f_docs))
zkontroluj('společných docs/', r'>(\d+)</b><span>společných', len(spol))
print('     společné: %s' % ', '.join(spol))

a_r, f_r = pravidla(ALZ), pravidla(FHB)
zkontroluj('pravidla alzask', r'<span>(\d+) · alzask</span>', len(a_r))
zkontroluj('pravidla fhb', r'<span>(\d+) · fhb</span>', len(f_r))
zkontroluj('společných pravidel', r'<h3>(\d+) · v obou projektech</h3>', len(a_r & f_r))
zkontroluj('jen alzask', r'>(\d+) · jen alzask</h3>', len(a_r - f_r))
zkontroluj('jen fhb', r'>(\d+) · jen fhb</h3>', len(f_r - a_r))

print('\nCO SE NAČTE PŘI STARTU')


def znaku(p):
    return len(io.open(p, encoding='utf-8', errors='replace').read())


cl = znaku(os.path.join(ALZ, 'CLAUDE.md'))
mem = znaku(r'C:\Users\ai_martint\.claude\projects\c--Git-alzask\memory\MEMORY.md')
sty = znaku(os.path.join(ALZ, '.claude', 'output-styles', 'Feynman-CZ.md'))
prav = sum(znaku(f) for f in glob.glob(os.path.join(ALZ, '.claude', 'rules', 'shared', '*.md')))
zkontroluj('CLAUDE.md znaků', r'<td>CLAUDE\.md</td><td style="text-align:right">([\d\s\u00a0]+)</td>', '%d' % cl)
zkontroluj('MEMORY.md znaků', r'<td>MEMORY\.md</td><td style="text-align:right">([\d\s\u00a0]+)</td>', '%d' % mem)
zkontroluj('styl výstupu znaků', r'<td>styl výstupu</td><td style="text-align:right">([\d\s\u00a0]+)</td>', '%d' % sty)
zkontroluj('celkem při startu', r'celkem při startu</b></td><td style="text-align:right"><b>([\d\s\u00a0]+)</b>', '%d' % (cl + mem + sty))
zkontroluj('pravidla znaků', r'<td>18 pravidel</td><td style="text-align:right">([\d\s\u00a0]+)</td>', '%d' % prav)

# všechna pravidla musí mít paths:, jinak tvrzení na slidu neplatí
bez_cesty = []
for f in glob.glob(os.path.join(ALZ, '.claude', 'rules', 'shared', '*.md')) + \
          glob.glob(os.path.join(FHB, '.claude', 'rules', 'shared', '*.md')):
    t = io.open(f, encoding='utf-8', errors='replace').read()
    fm = t.split('---')[1] if t.startswith('---') else ''
    if not re.search(r'^paths:', fm, re.M):
        bez_cesty.append(os.path.basename(f))
print('  %-46s %s' % ('pravidel bez `paths:` (musí být 0)',
                      'OK (0)' if not bez_cesty else 'NESEDI: %s' % bez_cesty))
if bez_cesty:
    chyby.append('pravidla bez paths')

print('\nREGISTR ONTOLOGIE')
idx = io.open(os.path.join(ONT, 'INDEX.md'), encoding='utf-8').read(1500)
m = re.search(r'\*\*(\d+) entit\*\*\s*\(physical (\d+) · logical (\d+) · enum (\d+) · actor (\d+)\)'
              r'\s*·\s*\*\*(\d+) vztahů\*\*\s*·\s*\*\*(\d+) atributů\*\*\s*·\s*\*\*(\d+) rozporů\*\*', idx)
assert m, 'hlavicka INDEX.md se nepodarila precist'
ent, fyz, log, enu, act, vaz, atr, roz = m.groups()
zkontroluj('prvků', r'<b>(\d+)</b><span>prvků</span>', ent)
zkontroluj('vazeb', r'<b>(\d+)</b><span>vazeb</span>', vaz)
zkontroluj('atributů', r'<b>(\d+)</b><span>atributů</span>', atr)
zkontroluj('rozporů', r'>(\d+)</b><span>rozporů</span>', roz)
zkontroluj('rozpad prvků', r'(\d+ fyzických · \d+ logických)',
           '%s fyzických · %s logických' % (fyz, log))

vrstev = len(re.findall(r'^\|\s*\d[ab]?\s*\|',
                        io.open(os.path.join(ONT, 'conflicts.md'), encoding='utf-8').read(4000), re.M))
v_deck = len(re.findall(r'<tr><td>(?:1a|1b|[2-6])</td>', d))
print('  %-46s deck %-24s disk %-10s %s'
      % ('vrstev autority', v_deck, vrstev, 'OK' if v_deck == vrstev else 'NESEDI'))
if v_deck != vrstev:
    chyby.append('vrstvy autority')

print('\n%s' % ('VSE SEDI' if not chyby else 'NESEDI: %s' % ', '.join(chyby)))
