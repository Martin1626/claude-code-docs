# -*- coding: utf-8 -*-
"""Přepočítá součty v NAMETY.md ze skutečného obsahu souboru.
Čte souhrnnou tabulku i tabulky jednotlivých dílů a hlásí nesoulady.
Spouštět po každé změně katalogu.
"""
import io
import re
import sys

P = r'C:\github\claude code docs\workshop-namety\NAMETY.md'
s = io.open(P, encoding='utf-8', newline='').read().replace('\r\n', '\n')

# --- souhrnná tabulka: | ID | Okruh | Název | Role | Min | Prio | Blok | dep |
souhrn = re.findall(
    r'^\|\s*([FNKRMOAUX]-\d\d)\s*\|\s*\w\s*\|[^|]*\|[^|]*\|\s*(\d+)\s*\|\s*(must|should|could)\s*\|',
    s, re.M)
minut = {i: int(m) for i, m, _ in souhrn}
prio = {i: p for i, _, p in souhrn}

print('SOUHRNNÁ TABULKA')
print('  námětů: %d' % len(souhrn))
print('  minut:  %d' % sum(minut.values()))
for p in ('must', 'should', 'could'):
    print('  %-7s %d' % (p + ':', sum(1 for v in prio.values() if v == p)))

# --- tabulky dílů: "## Díl X — název" a pod ním | ID | ... | Min | Prio |
print('\nTABULKY DÍLŮ')
dily = re.findall(r'^## Díl ([0-9P]+) — (.+?)$(.*?)(?=^## |\Z)', s, re.M | re.S)
zarazene = set()
celkem_prednasene = 0
radky = []
for cislo, nazev, telo in dily:
    ids = re.findall(r'^\|\s*([FNKRMOAUX]-\d\d)\s*\|', telo, re.M)
    mm = sum(minut.get(i, 0) for i in ids)
    zarazene.update(ids)
    if cislo not in ('0', 'P'):
        celkem_prednasene += mm
    radky.append((cislo, len(ids), mm))
    stav = 'ano' if mm <= 90 else 'PŘES 90'
    print('  Díl %-2s %-46s %2d námětů %4d min  %s' % (cislo, nazev[:46], len(ids), mm, stav))
    # kontrola deklarovaného počtu v textu dílu
    dek = re.search(r'\*\*(\d+) minut\*\*\s*·\s*(\d+)\s*námět', telo)
    if dek and (int(dek.group(1)) != mm or int(dek.group(2)) != len(ids)):
        print('     ⚠ v textu je uvedeno %s minut / %s námětů' % (dek.group(1), dek.group(2)))

print('\n  přednášené díly (bez 0 a P): %d minut' % celkem_prednasene)
nezarazene = sorted(set(minut) - zarazene)
print('  zařazených do dílů: %d · nezařazených: %d %s'
      % (len(zarazene), len(nezarazene), nezarazene if nezarazene else ''))

# --- tvrzení v textu, která se musí shodovat
print('\nTVRZENÍ V TEXTU')
for vzor, skutecnost in [
    (r'\*\*Celkem (\d+) námětů, (\d+) minut\.\*\*', (len(souhrn), sum(minut.values()))),
    (r'Katalog má (\d+) námětů a (\d+) minut', (len(souhrn), sum(minut.values()))),
    (r'Námětů v tabulce: (\d+) · zařazených do dílů: (\d+)', (len(souhrn), len(zarazene))),
]:
    m = re.search(vzor, s)
    if m:
        nalezeno = tuple(int(g) for g in m.groups())
        ok = nalezeno == skutecnost
        print('  %-46s v textu %s, skutečnost %s  %s'
              % (m.group(0)[:46], nalezeno, skutecnost, 'OK' if ok else 'NESEDÍ'))

# pozor: v textu je i historická zmínka na starou hodnotu v uvozovkách — hledá se jen platné tvrzení
m = re.search(r'škrtej podle priority \(`must` je (\d+) námětů\)', s)
if m:
    sk = sum(1 for v in prio.values() if v == 'must')
    print('  must v textu %s, skutečnost %d  %s' % (m.group(1), sk, 'OK' if int(m.group(1)) == sk else 'NESEDÍ'))

m = re.search(r'Přednášených dílů ([0-9–-]+): \*\*(\d+) minut', s)
if m:
    print('  přednášené v textu %s min, skutečnost %d  %s'
          % (m.group(2), celkem_prednasene, 'OK' if int(m.group(2)) == celkem_prednasene else 'NESEDÍ'))
