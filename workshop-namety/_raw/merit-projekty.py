# -*- coding: utf-8 -*-
"""Odečte strukturu a velikosti obou pracovních projektů (alzask, fhb).
Zdroj čísel pro deck 2. sezení a pro novou část DOKLADY.md.
Spouštět: PYTHONUTF8=1 python _raw/merit-projekty.py
"""
import io
import os
import re
import sys

PROJEKTY = {
    'alzask': r'C:\Git\alzask',
    'fhb': r'C:\Git\fhb',
}


def velikost(p):
    if not os.path.isfile(p):
        return None
    b = os.path.getsize(p)
    with io.open(p, encoding='utf-8', errors='replace') as f:
        t = f.read()
    return b, len(t), t.count('\n') + 1


def seznam(d, pattern=None):
    if not os.path.isdir(d):
        return []
    out = []
    for n in sorted(os.listdir(d)):
        if pattern and not re.search(pattern, n):
            continue
        out.append(n)
    return out


def rule_ids(d):
    ids = {}
    for n in seznam(d, r'\.md$'):
        m = re.match(r'(RULE-[A-Z]+-\d+)', n)
        if m:
            ids[m.group(1)] = n
    return ids


print('=' * 72)
print('MĚŘENÍ PROJEKTŮ — %s' % os.popen('date /t').read().strip() if os.name == 'nt' else '')
print('=' * 72)

rules = {}
for kod, root in PROJEKTY.items():
    print('\n### %s  (%s)' % (kod, root))
    if not os.path.isdir(root):
        print('  ADRESÁŘ NEEXISTUJE')
        continue

    v = velikost(os.path.join(root, 'CLAUDE.md'))
    if v:
        print('  CLAUDE.md .................. %d B · %d znaků · %d řádků' % v)

    cl = os.path.join(root, '.claude')
    for pod in ('agents', 'commands', 'hooks', 'skills', 'output-styles'):
        polozky = seznam(os.path.join(cl, pod))
        polozky = [x for x in polozky if not x.startswith('__')]
        if polozky:
            print('  .claude/%-14s %2d: %s' % (pod + '/', len(polozky), ', '.join(polozky)))

    # pravidla — shared i další vrstvy
    for vrstva in ('shared', 'arch-spec', 'personal'):
        d = os.path.join(cl, 'rules', vrstva)
        r = rule_ids(d)
        if r:
            print('  rules/%-12s %2d: %s' % (vrstva + '/', len(r), ', '.join(sorted(r))))
            if vrstva == 'shared':
                rules[kod] = set(r)

    # docs — podadresáře první úrovně
    docs = os.path.join(root, 'docs')
    pod = [n for n in seznam(docs) if os.path.isdir(os.path.join(docs, n)) and not n.startswith('.')]
    print('  docs/ .................... %d podadresářů: %s' % (len(pod), ', '.join(pod)))

    # validátory (skryté nástrojové adresáře)
    val = []
    for dirpath, dirnames, _ in os.walk(docs):
        for dn in dirnames:
            if dn.startswith('.') and dn.endswith('-tools'):
                val.append(os.path.relpath(os.path.join(dirpath, dn), root).replace('\\', '/'))
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
    if val:
        print('  validátory ............... %d: %s' % (len(val), ', '.join(sorted(val))))

if len(rules) == 2:
    a, b = rules['alzask'], rules['fhb']
    print('\n### PRAVIDLA — překryv')
    print('  alzask shared ............ %d' % len(a))
    print('  fhb shared ............... %d' % len(b))
    print('  SPOLEČNÝCH ............... %d: %s' % (len(a & b), ', '.join(sorted(a & b))))
    print('  jen alzask ............... %d: %s' % (len(a - b), ', '.join(sorted(a - b))))
    print('  jen fhb .................. %d: %s' % (len(b - a), ', '.join(sorted(b - a))))

# --- registr ontologie ---
ONT = r'C:\Git\alzask\docs\ontology'
print('\n### REGISTR ONTOLOGIE  (%s)' % ONT)
for n in ('INDEX.md', 'TERMS.tsv', 'RELATIONS.tsv', 'conflicts.md', 'ontology.yaml', 'coverage.md', 'anchors.tsv'):
    v = velikost(os.path.join(ONT, n))
    if v:
        print('  %-16s %9d B · %6d řádků' % (n, v[0], v[2]))
ent = seznam(os.path.join(ONT, 'entities'), r'\.md$')
karty = [x for x in ent if not x.endswith('.notes.md')]
print('  entities/ ........ %d souborů = %d karet + %d poznámek'
      % (len(ent), len(karty), len(ent) - len(karty)))
nastroje = [x for x in seznam(os.path.join(ONT, '.ontology-tools')) if x.endswith(('.py', '.cmd'))]
print('  .ontology-tools/ . %d: %s' % (len(nastroje), ', '.join(nastroje)))

# hlavička INDEX.md nese souhrnná čísla
idx = os.path.join(ONT, 'INDEX.md')
if os.path.isfile(idx):
    with io.open(idx, encoding='utf-8') as f:
        head = f.read(2000)
    m = re.search(r'\*\*(\d+)\s+entit\*\*\s*\(([^)]*)\)\s*·\s*\*\*(\d+)\s+vztahů\*\*\s*·\s*\*\*(\d+)\s+atributů\*\*\s*·\s*\*\*(\d+)\s+rozporů\*\*', head)
    if m:
        print('  souhrn z INDEX.md: %s entit (%s) · %s vztahů · %s atributů · %s rozporů'
              % (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)))

# vrstvy autority z conflicts.md
conf = os.path.join(ONT, 'conflicts.md')
if os.path.isfile(conf):
    with io.open(conf, encoding='utf-8') as f:
        c = f.read(4000)
    vrstvy = re.findall(r'^\|\s*(\d[ab]?)\s*\|\s*(.+?)\s*\|$', c, re.M)
    print('  vrstev autority: %d' % len(vrstvy))
    for cislo, popis in vrstvy:
        print('     %-3s %s' % (cislo, popis[:88]))
