> **Hlavní katalog námětů na sérii workshopů o Claude Code pro analytiky.**
> Výklad fundamentu: [FUNDAMENT.md](FUNDAMENT.md) · doklady a statistiky: [DOKLADY.md](DOKLADY.md) ·
> vyřazené náměty a přiznané mezery: [VYRAZENO.md](VYRAZENO.md).
> Pracovní podklady třinácti agentů zůstaly v `_raw/`.

# Katalog námětů

**Toto není program workshopu.** Je to zásoba, ze které se program skládá — proto má
každý námět odhad času, závislosti a poznámku, co konkrétně půjde ukázat na obrazovce.
Návrh rozdělení do dílů je na konci a je to jen návrh.

## Z čeho to vzniklo

| Zdroj | Rozsah |
|---|---|
| Historie zadávání | 2 671 promptů, 2026-01-19 → 2026-08-26; z toho **1 508 v pracovních projektech** |
| Transkripty session | 84 souborů, 120 MB — z nich 19 kompaktací s přesnými čísly |
| Repozitáře | `alzask`, `fhb`, `myfaber`, `shared` — metodiky, validátory, pravidla, 3 vlastní pluginy |
| Konfigurace | `~/.claude` — settings, hooky, output style, pluginy |

Prošlo to **třináct agentů** v sedmi fázích, našlo asi **267 kandidátů**, a pak jeden
adversariální průchod, který proti hotovému draftu vznesl **42 nálezů s povinnou akcí**.
Skripty zůstaly v `_raw/`, takže se to dá přepočítat.

## Co ten adversariální průchod změnil — a proč to stojí na začátku

Red-team našel v draftu **faktickou chybu ve vlajkovém čísle**: kompaktací nebylo 21, ale
19 (fork session kopíruje záznam, takže dvě byly započtené dvakrát), a součet zahozených
tokenů byl nadhodnocený o 36 %. Čísla v tomto katalogu jsou už opravená. Ta chyba
je zároveň exponát: **měřil jsem jiný jev, než jaký jsem popisoval** — a nevšiml bych si
toho bez druhého průchodu.

A našel ještě něco důležitějšího. Třináct jeho nálezů říká **jednu a tutéž věc**:

> ## Mezi „postavil jsem to" a „používám to" je propast.
>
> - Celá sekce „Projektový asistent" v mém `CLAUDE.md` (12,7 % souboru, ~1000 tokenů
>   každý tah) **nebyla za 2678 promptů spuštěna ani jednou.**
> - Pětiagentní revizní pipeline: postavená, **nikdy nespuštěná.**
> - Znalostní smyčka: z 63 zachycených kandidátů povýšeno 5, všech 5 v prvních šesti
>   dnech. Pak **47 dní nic.**
> - Pravidlo „vynucuj bránou, neinstruuj v promptu" je nejsilnější konvergence celé
>   inventury — a **v tom projektu žádná brána neběží.** `core.hooksPath` míří do
>   `.git/hooks`, kde není jediný aktivní hook, a `.githooks/` je nedotčené 7,2 měsíce.
> - Týdenní snapshoty: kadence vynechala tři týdny v řadě a objem spadl na sedminu.
>
> Podle vlastní metody tohoto katalogu je trojí nezávislá konvergence nejsilnější možný
> signál. Tady je třináctinásobná. Takže to není námět — **je to nosné téma série.**

Náměty, které tohle téma nesou, jsou v tabulce označené **⚑**. Je jich devět a stojí
za nimi nejsilnější doklady, jaké v katalogu jsou — protože doklad „přestal jsem to
používat" se nedá vyvrátit dobrým dojmem.

## Jak jsem vybíral, co je přenositelné

Hlavní kritérium nebylo „funguje mi to", ale **„odnese si to kolega, který nemá moje
validátory, pluginy a 23 KB `CLAUDE.md`?"** Co neprošlo, je ve [VYRAZENO.md](VYRAZENO.md)
s důvodem.

Prioritu dostaly **konvergence** — věci, které našlo víc agentů nezávisle nad jinými daty:

| Konvergující nález | Nezávislých nálezů |
|---|---|
| Mezi „postaveno" a „používáno" je propast | **13** |
| Brána místo instrukce v promptu | 5 |
| Číslovaný picklist a odpověď čísly | 4 |
| Grounding: citace se ověřuje, nevěří | 4 |
| Dlouhé zadání patří do souboru, ne do chatu | 3 |
| Read-only brána „nic neměň, jen vypiš" | 3 |
| Triáž nálezů dělá člověk, ne model | 3 |
| Meta-analýza vlastních běhů | 3 |
| Konvence bez validátoru se rozpadne | 3 |

## Jedna věc, kterou je potřeba říct hned na začátku

Data ukazují něco, co jde proti intuici, a **kdyby si publikum odneslo jen půlku, uškodí
mu to.**

Medián mého promptu je **65 znaků**. Promptů nad 1000 znaků je 31 z 1508, tedy **2 %**.
Vypadá to jako doporučení „piš krátce". Ale ono to znamená něco jiného: nejdelší prompt
jednoho měsíce nese **patnáct odpovědí a ani jednu otázku** — otázky totiž žijí
v `BACKLOG.md`. Ty krátké prompty fungují jen proto, že kontext leží v souborech.

> **Dokument nese kontext, prompt nese rozhodnutí.**
>
> Kolega, který si odnese „piš krátké prompty", dostane špatný výsledek. Musí si odnést
> „nejdřív postav místo, kam ty otázky patří".

## Značení

**Okruhy:** `F` fundament · `N` nastavení a prostředí · `K` kontext a grounding ·
`R` rozšíření · `M` mechanika kvality · `O` orchestrace · `A` analytické postupy ·
`U` učení a znalostní smyčka · `X` antipatterny

**Role:** `[výklad]` · `[demo]` předvedu naživo · `[cvičení]` zkusí si sami ·
`[příběh]` konkrétní historka s doklady · `[infra]` musí někdo postavit pro tým

**⚑** = námět nesoucí nosné téma „postaveno vs. používáno"
**⚠** = námět, který si vyžádal opravu po red-teamu (doklad byl slabší, než draft tvrdil)

**Poznámka k okruhu `X`.** Red-team správně namítl, že antipattern většinou není samostatné
téma, ale **odvrácená strana** pozitivního námětu — devět z dvanácti položek draftu bylo
negativní dvojče něčeho jiného. Ty jsem sloučil do příslušných karet jako sekci
„jak to vypadá, když to nedělám". V okruhu `X` zůstaly **čtyři**, které vlastní dvojče
nemají a stojí samy.

---
