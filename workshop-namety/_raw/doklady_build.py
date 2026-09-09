import os

RAW = 'C:/tmp/workshop-namety/_raw/'
DST = 'C:/tmp/workshop-namety/DOKLADY.md'


def read(name):
    p = RAW + name
    if not os.path.isfile(p):
        return '_(zdroj `' + name + '` nenalezen)_\n'
    with open(p, encoding='utf-8') as f:
        t = f.read()
    # snizit uroven nadpisu o 1, aby se vlozily pod nase H2
    out = []
    for ln in t.split('\n'):
        if ln.startswith('#'):
            out.append('##' + ln)
        else:
            out.append(ln)
    return '\n'.join(out).strip() + '\n'


parts = []
W = parts.append

W("""> **Tento dokument je příloha katalogu námětů na workshop.**
> Hlavní katalog: [NAMETY.md](NAMETY.md) · výklad fundamentu: [FUNDAMENT.md](FUNDAMENT.md) ·
> vyřazené náměty: [VYRAZENO.md](VYRAZENO.md).

# Doklady — statistiky a inventář výbavy

Všechno v tomto dokumentu je **měřené**, ne odhadnuté, pokud u toho není napsáno „odhad".
Skripty, které to spočítaly, zůstaly v `_raw/` (`verify_counts.py`, `doklady_gen.py`,
`compact_stats.py`, `context_cost.py`) — čísla jsou tedy přepočitatelná.

## Jak to čítat

Tři nezávislé zdroje dat, každý měří něco jiného:

| Zdroj | Co v něm je | K čemu je dobrý |
|---|---|---|
| `~/.claude/history.jsonl` | 2 671 promptů zadaných člověkem, 7 měsíců, 0,84 MB | Jak zadávám. Délky promptů, slash commandy, rozložení v čase. |
| `~/.claude/projects/*/*.jsonl` | 84 sessions, 120 MB transkriptů | Co se v session skutečně stalo. **Kompaktace s přesnými čísly.** |
| Soubory v repozitářích | `CLAUDE.md`, pravidla, paměti, skilly | Kolik místa zabere kontext, než začnu psát. |

**Pozor na dvě sady čísel.** Statistiky se liší podle toho, jestli měřím celou historii
zadávání, nebo jen projekty v rozsahu tohoto workshopu (alzask, fhb, myfaber, shared).
Rozdíl není kosmetický — u `/compact` je to 67× proti 51×. Kde to hraje roli, jsou
uvedené obě.

**Jedna metodická poznámka, která se hodí i jako námět.** Když jsem tato čísla měřil,
historie mezi dvěma běhy skriptu povyrostla — o moje vlastní prompty z toho měření.
`history.jsonl` je soubor, který roste s každým zadáním. Proto se drobné odchylky
v kontrolních součtech (1503 → 1507 → 1508) nevysvětlují chybou, ale tím, že měřím
běžící systém.

---

""")

W('# Část 1 — Statistiky zadávání\n')
W(read('doklady-statistiky.md'))
W('\n---\n')
W('# Část 2 — Kompaktace kontextu\n')
W("""Tohle je nejtvrdší doklad celé inventury, protože si ho **harness zapsal sám**.
U každé kompaktace ukládá do transkriptu přesná čísla — nemusím nic odhadovat.

> **Výhrada, kterou je nutné uvést.** Dokumentace parsování transkriptů výslovně
> nedoporučuje: formát záznamů je interní a mění se mezi verzemi. Doporučená cesta je
> `/export` nebo `claude -p --output-format json`. Čísla níže jsou platná pro tuto verzi.
> A těch 21 kompaktací je **podvýběr** — historie zná 175 sessions jen pro alzask, ale
> transkriptů na disku je 84.

""")
W(read('doklady-kompaktace.md'))
W('\n---\n')
W('# Část 3 — Co zabírá místo v kontextu\n')
W(read('doklady-cena-kontextu.md'))
W('\n---\n')
W('# Část 4 — Inventář výbavy\n')
W(read('faze1-inventar.md'))
W('\n---\n')
W('# Část 5 — Korekce inventáře: hooky a nastavení\n')
W("""První průchod inventářem nahlásil **nula hooků**. To bylo nesprávné — hooky nejsou jen
v `settings.json`, ale hlavně v pluginech (`<plugin>/hooks/hooks.json`). Doklad, že aspoň
jeden fakticky běží: knowledge-loop `SessionStart` hook dodal na startu session handle
autora a obsah jeho znalostního inboxu.

Je to samo o sobě použitelné poučení pro workshop: **inventář, který se dívá jen na jedno
místo, vykáže nulu tam, kde je čtyřka.**

""")
W(read('faze1-korekce-hooky.md'))

with open(DST, 'w', encoding='utf-8') as f:
    f.write('\n'.join(parts))

print('zapsano:', DST, round(os.path.getsize(DST) / 1024, 1), 'KB')
