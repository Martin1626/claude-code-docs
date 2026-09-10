# -*- coding: utf-8 -*-
"""Srovná tvrzení o součtech v NAMETY.md se skutečností po přidání K-08 až K-10."""
import io

P = r'C:\github\claude code docs\workshop-namety\NAMETY.md'
s = io.open(P, encoding='utf-8', newline='').read()
CRLF = '\r\n' in s
if CRLF:
    s = s.replace('\r\n', '\n')


def sub1(a, b, l=''):
    global s
    assert s.count(a) == 1, (l, s.count(a))
    s = s.replace(a, b, 1)


sub1(u'**Celkem 56 námětů, 694 minut.**',
     u'**Celkem 59 námětů, 738 minut.**', 'celkem')

sub1(u'Katalog má 56 námětů a 694 minut',
     u'Katalog má 59 námětů a 738 minut', 'katalog')

sub1(u'série má být kratší, škrtej podle priority (`must` je 37 námětů)',
     u'série má být kratší, škrtej podle priority (`must` je 41 námětů)', 'must')

sub1(u'Součty jsou spočítané skriptem (`_raw/n5-bloky.py`) z minut v souhrnné tabulce, ne\nodhadem — draft měl tři ze šesti bloků sečtené špatně a red-team to našel.',
     u'Součty jsou spočítané skriptem (`_raw/prepocet-souctu.py`) přímo z minut v souhrnné\ntabulce a z tabulek dílů, ne odhadem — draft měl tři ze šesti bloků sečtené špatně\na red-team to našel. Skript hlásí i nesoulad mezi tvrzením v textu a skutečností;\npři přidání K-08 až K-10 (10. 9. 2026) tak vyšlo najevo, že údaj „`must` je 37 námětů"\nbyl zastaralý už předtím — správně jich bylo 39, po doplnění 41.', 'skript')

sub1(u'| 10 | 4 | 62 | ano |\n| P | 3 | 37 | ano |',
     u'| 10 | 4 | 62 | ano |\n| 11 | 3 | 44 | ano |\n| P | 3 | 37 | ano |', 'tabulka')

sub1(u'Přednášených dílů 1–10: **642 minut.** Plus příprava (díl 0) a příloha `P`.',
     u'Přednášených dílů 1–11: **686 minut.** Plus příprava (díl 0) a příloha `P`.', 'prednasene')

sub1(u'Námětů v tabulce: 56 · zařazených do dílů: 56 · nezařazených: 0',
     u'Námětů v tabulce: 59 · zařazených do dílů: 59 · nezařazených: 0', 'zarazene')

sub1(u'| **Celá série** | 1–10 | 642 | vše včetně velkého auditu a předání kolegovi |',
     u'| **Celá série** | 1–11 | 686 | vše včetně velkého auditu a předání kolegovi |', 'strihy')

io.open(P, 'w', encoding='utf-8', newline='').write(s.replace('\n', '\r\n') if CRLF else s)
print('srovnano')
