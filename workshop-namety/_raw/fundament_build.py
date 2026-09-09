import os

SRC = 'C:/tmp/workshop-namety/_raw/faze4a-fundament.md'
DST = 'C:/tmp/workshop-namety/FUNDAMENT.md'

with open(SRC, encoding='utf-8') as f:
    body = f.read().strip()

header = """> **Součást katalogu námětů na workshop.**
> Hlavní katalog: [NAMETY.md](NAMETY.md) · doklady a statistiky: [DOKLADY.md](DOKLADY.md) ·
> vyřazené náměty: [VYRAZENO.md](VYRAZENO.md).
> Pracovní podklady dvanácti agentů zůstaly v `_raw/`.

> **Jak tento dokument vznikl.** Výklad tří mechanik (bezstavovost, tokenizace, kontextové
> okno) napsal agent na modelu opus, který u každého tvrzení musel označit, jestli je
> ověřené, odhadnuté, nebo nevěděl. Bodů „nevím a nehádám" bylo v první verzi **jedenáct**.
> Druhý agent je ověřil proti dokumentaci a **deset padlo**. Zbylých pět (dva z nich nové)
> je poctivě uvedeno na konci jako úkoly na přípravu — u dvou z nich brání API klíč, který
> na tomto stroji není.
>
> Ta jedenáctka je sama o sobě námět: **výklad, který si dovolí říct „tady nevím",
> se dá ověřit. Výklad, který to zamlčí, se ověřit nedá.**

"""

with open(DST, 'w', encoding='utf-8') as f:
    f.write(header + body + '\n')

print('zapsano:', DST, round(os.path.getsize(DST) / 1024, 1), 'KB')
with open(DST, encoding='utf-8') as f:
    print('radku:', len(f.read().split(chr(10))))
