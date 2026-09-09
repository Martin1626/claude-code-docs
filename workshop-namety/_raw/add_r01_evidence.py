import os

p = 'C:/tmp/workshop-namety/NAMETY.md'
with open(p, encoding='utf-8') as f:
    t = f.read()

BT = chr(96)  # backtick

a = ('**Co ukážu na obrazovce:** vedle sebe jednořádkový prompt a 12,8 kB soubor za ním.\n'
     '**A pak meta-ukázka: tenhle katalog vznikl přesně tak** — zadání mělo 12 kB v souboru\n'
     'a prompt zněl „Přečti si celý a proveď".')

extra = (
    '\n\n**A ještě jeden doklad, který se stal sám, během psaní tohoto katalogu.** V 9:31 padl\n'
    'v jedné session pokyn *„Napiš prompt, který provede i v pluginu ontology-registry. Já jej\n'
    'pak spustím sám."* — v 9:48 se v jiné session a jiném repozitáři objevilo\n'
    '*„Přečti ' + BT + 'C:/tmp/prompt-ontology-registry-kotvy.md' + BT + ' a proveď to."* a v 9:51 byly změněné\n'
    'čtyři soubory. Ten vzor tedy nefunguje jen ve starých datech — použil se **nezávisle\n'
    'v tu samou hodinu**, kdy jsem ho tady označoval za nejsilnější praxi. Je to nejlepší\n'
    'možný doklad, protože ho nikdo nepřipravoval.'
)

if a not in t:
    raise SystemExit('vzor nenalezen')

t = t.replace(a, a + extra, 1)
with open(p, 'w', encoding='utf-8') as f:
    f.write(t)
print('doplneno do R-01 | NAMETY.md =', round(os.path.getsize(p) / 1024, 1), 'KB')
