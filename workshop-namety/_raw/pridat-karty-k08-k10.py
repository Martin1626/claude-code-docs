# -*- coding: utf-8 -*-
"""Vloží karty K-08 až K-10 do NAMETY.md, doplní souhrnnou tabulku,
přidá Díl 11 a přepočítá kontrolu součtů ze skutečného obsahu souboru.
Spustit jednou. Idempotence se hlídá kontrolou, že K-08 tam ještě není.
"""
import io
import re

P = r'C:\github\claude code docs\workshop-namety\NAMETY.md'
s = io.open(P, encoding='utf-8', newline='').read()
CRLF = '\r\n' in s
if CRLF:
    s = s.replace('\r\n', '\n')

assert 'K-08' not in s, 'K-08 uz v souboru je — skript se spousti jen jednou'

KARTY = u"""### K-08 — Kostra je stejná, výbava se liší

**O čem to je.** Dva projekty pro dva různé zákazníky, dvě různé domény, dva různé týmy —
a skoro stejný adresářový strom. Nikdo to neopisoval; oba do toho tvaru dorostly, protože
se v nich opakovaně pracuje s agentem. **Devět adresářů `docs/` ze šestnácti a dvanácti je
společných** a **deset sdílených pravidel z osmnácti a třinácti je totožných.** Co se liší,
je výbava: jeden projekt má registr prvků a pět revizních agentů, druhý sedm agentů na psaní
specifikace. Zásada pro publikum: **kopíruj kostru, ne cizí výbavu** — ta odpovídá tomu, co
ten konkrétní projekt bolelo.

**Doklad:** `DOKLADY.md` část 6.1–6.3. Změřeno 2026-09-10 skriptem `_raw/merit-projekty.py`
přímo v obou repozitářích: `docs/` 16 a 12 podadresářů, průnik 9; sdílených pravidel 18 a 13,
průnik 10 (`RULE-AP-001`, `-AP-002`, `-CL-001`, `-DIAG-001`, `-GOV-001`, `-GOV-002`,
`-META-001`, `-SPEC-001`, `-SPEC-002`, `-TERM-001`).

**Role:** `[výklad]` · **Náročnost:** nízká · **Odhad:** 14 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** stromy obou projektů vedle sebe — jen kořen a `docs/` do druhé
úrovně. Přepínačem zvýrazním společné adresáře, ať je ten průnik vidět naráz. Pak průnik
sdílených pravidel a dvě karty s výbavou.

**Ověřitelný výstup:** posluchač do příště vyjmenuje, které z devíti společných adresářů ve
svém projektu má a které mu chybí.

**Kam dál:** [code.claude.com/docs/en/claude-directory](https://code.claude.com/docs/en/claude-directory)

**Výhrada:** druhý projekt je **jiný zákazník**. Na plátno jde jen strom adresářů, nikdy obsah
dokumentů. A nesmí to sklouznout k „takhle to má vypadat" — tvar je důsledek práce, ne šablona
ke stažení.

### K-09 — Rejstřík prvků je index faktů, ne jejich autorita

**O čem to je.** Rejstřík prvků je seznam všeho, s čím se v projektu pracuje — fyzické prvky,
logické entity, číselníky, aktéři — s popisem, vazbami a **citací zdroje u každého tvrzení**.
Smysl je, aby si model doménu nemusel domýšlet a aby se dalo dohledat, odkud se co ví.

Dvě věty, na kterých ta karta stojí:

1. **Citace je adresa *plus* úryvek.** Samotné `soubor:řádek` je souřadnice; tři až šest slov
   doslova z toho místa je to, co drží tvrzení pohromadě, když se zdroj změní.
2. **Cituj původní zdroj, ne rejstřík.** Rejstřík je index faktů, ne jejich autorita. Citace
   rejstříku založí druhou vrstvu zastarávání — dokument → rejstřík → zdroj — a hlídá se jen jedna.

**Doklad:** `DOKLADY.md` část 6.5 — registr projektu alzask má **176 prvků** (48 fyzických,
48 logických, 61 číselníků, 19 aktérů), **354 vazeb**, **703 atributů** a **97 zapsaných rozporů**;
rejstřík `INDEX.md` 32 kB se čte celý, zdroj pravdy `ontology.yaml` 1,7 MB nikdy.
Pravidlo o citování zdroje: `.claude/rules/shared/RULE-ONT-002_cituj-zdroj-ne-registr.md`.

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 18 min ·
**Závislosti:** K-01 · **Priorita:** must

**Co ukážu na obrazovce:** hlavičku rejstříku s těmi čtyřmi čísly, jednu kartu prvku se sloupcem
„co na tom místě stojí", a tabulku velikostí souborů, ze které je vidět, proč se zdroj pravdy
o 1,7 MB nečte celý a rejstřík o 32 kB ano.

**Ověřitelný výstup:** posluchač najde ve svém posledním dokumentu jedno tvrzení bez citace
a doplní k němu zdroj i úryvek.

**Kam dál:** F-05 (co zabírá místo v okně) a K-06 (hierarchie autority).

**Výhrada:** plný rejstřík stojí generátor a nástroje. Kdo je nemá, si to nepostaví — a odejde
s pocitem „hezké, ale to my nemáme". Karta proto **musí končit minimální verzí**: jeden soubor
s rejstříkem, citace s úryvkem, napsané pořadí vrstev. Registr se 176 prvky takhle vznikl;
nástroje přišly, až když to ručně přestalo stačit.

### K-10 — Kotva stárne, a devět z patnácti hlášení je šum

**O čem to je.** **Číslo řádku je adresa, ne identita.** Někdo vloží odstavec nad citované
místo a citace ukazuje jinam — soubor sedí, číslo sedí, obsah je cizí, a není to jak poznat.
Proto se u citace drží **kotva**, otisk několika řádků okolí, a ověřuje se nástrojem, který
vrátí **verdikt** místo textu: `OK`, `POSUN`, `ZMIZELA`.

Jenže kotva je otisk *okolí*. Shodí ji i odstavec vložený **vedle** citace — a to je šum,
ne nález. Pravidlo, které pošle člověku všechna hlášení, mu naloží mechanické případy smíchané
se skutečnými; člověk pak buď odklikne všechno, nebo to odloží. **Obojí je horší než automatika.**

**Doklad:** měření nad registrem **2026-08-26**: z **15 hlášení jich 9** byl vložený odstavec
vedle citace, tedy šum, a jen 6 skutečných rozhodnutí. Kvůli tomu se pravidlo přepsalo —
`.claude/rules/shared/RULE-ONT-003_kotvy-tri-tridy.md` (dřív `_zmizela-resi-clovek`).
Shrnutí v `DOKLADY.md` část 6.7.

**Role:** `[výklad]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** K-09 · **Priorita:** should

**Co ukážu na obrazovce:** tři verdikty vedle sebe a měření, kvůli kterému se pravidlo změnilo.
Pointa je ta změna, ne ty verdikty.

**Ověřitelný výstup:** posluchač řekne, co udělá s citací, u které se zdroj změnil — a proč je
přepsat číslo řádku horší než nechat citaci zastaralou.

**Kam dál:** K-05 (citace se ověřuje, nevěří).

**Výhrada:** bez nástroje na ověření kotev je z toho jen ostražitost. Říct to nahlas.
Zároveň je to nejlepší doklad v celém katalogu na to, že **se pravidlo mění měřením, ne názorem** —
a ten se přenáší i bez nástroje.

"""

# --- 1) karty před oddělovač okruhu R ---
KOTVA = u'---\n\n## Okruh R — Rozšíření'
assert s.count(KOTVA) == 1
s = s.replace(KOTVA, KARTY + KOTVA, 1)

# --- 2) řádky do souhrnné tabulky za K-07 ---
ROW = u'| K-07 | K | Čtvrtina mého `CLAUDE.md`, kterou nikdo nespustil ⚑ | příběh+demo | 15 | must | 3 | — |'
assert s.count(ROW) == 1
NOVE = (u'\n| K-08 | K | Kostra je stejná, výbava se liší | výklad | 14 | must | 11 | — |'
        u'\n| K-09 | K | Rejstřík prvků je index faktů, ne jejich autorita | výklad | 18 | must | 11 | K-01 |'
        u'\n| K-10 | K | Kotva stárne, a devět z patnácti hlášení je šum | výklad | 12 | should | 11 | K-09 |')
s = s.replace(ROW, ROW + NOVE, 1)

# --- 3) nový Díl 11 před Díl P ---
DILP = u'## Díl P — Příloha pro toho, kdo bude stavět nástroje'
assert s.count(DILP) == 1
DIL11 = u"""## Díl 11 — Kde to leží a odkud to víš

**44 minut** · 3 náměty

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| K-08 | Kostra je stejná, výbava se liší | výklad | 14 | must |
| K-09 | Rejstřík prvků je index faktů, ne jejich autorita | výklad | 18 | must |
| K-10 | Kotva stárne, a devět z patnácti hlášení je šum | výklad | 12 | should |

**Co si z toho odnesou:** Kostra projektu je u různých zákazníků stejná, liší se výbava.
Rejstřík prvků je index faktů, ne jejich autorita — a citace je adresa *plus* úryvek.

**Poznámka.** Tenhle díl v původním návrhu nebyl; katalog na strukturu projektu a dohledatelnost
zdrojů kartu neměl. Doplněn 2026-09-10 podle skutečně připraveného 2. sezení (`PROGRAM-02.md`).
S `K-06` a `K-05` z přílohy `P` dává **71 minut**, což je rozsah toho sezení bez diskuse.

"""
s = s.replace(DILP, DIL11 + DILP, 1)

io.open(P, 'w', encoding='utf-8', newline='').write(s.replace('\n', '\r\n') if CRLF else s)

# --- 4) přepočet z obsahu souboru ---
tab = re.findall(r'^\|\s*([FNKRMOAUX]-\d\d)\s*\|\s*\w\s*\|.*?\|\s*(\d+)\s*\|\s*(must|should|could)\s*\|\s*([0-9P]+)\s*\|',
                 s, re.M)
minut = {i: int(m) for i, m, _, _ in tab}
prio = {i: p for i, _, p, _ in tab}
blok = {i: b for i, _, _, b in tab}
print('namietu v souhrnne tabulce: %d' % len(tab))
print('celkem minut: %d' % sum(minut.values()))
print('must: %d · should: %d · could: %d'
      % (sum(1 for v in prio.values() if v == 'must'),
         sum(1 for v in prio.values() if v == 'should'),
         sum(1 for v in prio.values() if v == 'could')))
poradi = sorted(set(blok.values()), key=lambda x: (x == 'P', int(x) if x.isdigit() else 99))
print('\nDil | namietu | minut')
prednasene = 0
for b in poradi:
    ids = [i for i in minut if blok[i] == b]
    mm = sum(minut[i] for i in ids)
    if b not in ('0', 'P'):
        prednasene += mm
    print('%3s | %7d | %5d %s' % (b, len(ids), mm, 'ANO' if mm <= 90 else 'PRES 90!'))
print('\nprednasene dily celkem: %d minut' % prednasene)
