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

## Souhrnná tabulka

| ID | Okruh | Název | Role | Min | Prio | Blok | dep |
|---|---|---|---|---|---|---|---|
| F-01 | F | Claude si tě nepamatuje. Vede si o tobě složku. | výklad+demo | 15 | must | 1 | — |
| F-02 | F | Čeština není dražší, protože je delší ⚠ | výklad | 12 | must | 1 | F-01 |
| F-03 | F | Tomu shrnutí můžeš říct, co má zachovat ⚠ | výklad | 15 | must | 1 | F-01 |
| F-04 | F | Padesát jedna ku jedné | příběh+demo | 12 | must | 1 | F-03 |
| F-05 | F | Co tě stojí místo, o kterém nevíš ⚠ | výklad+demo | 15 | must | 1 | F-01 |
| N-01 | N | Tři zákazy, které si nastav dřív než cokoli jiného | demo | 8 | must | 1 | — |
| N-02 | N | Tři úrovně zpět: `Esc Esc`, `/rewind`, `git diff` | demo | 8 | must | 1 | — |
| N-03 | N | Režim plánování: rozhodnutí odděleně od provedení | demo | 10 | must | 1 | — |
| N-04 | N | Prompt je zápis, ne rozhovor | příběh+výklad | 15 | must | 1 | — |
| N-05 | N | Co to stojí a jak to zjistíš | demo | 10 | should | 1 | F-05 |
| N-06 | N | Cvičný repozitář — nulté dílo série | infra | 15 | must | 0 | — |
| K-01 | K | Dokument nese kontext, prompt nese rozhodnutí | výklad+demo | 20 | must | 2 | F-05 |
| K-02 | K | Bezcílný rozkaz ⚠ | příběh+cvičení | 12 | must | 2 | — |
| K-03 | K | Co NEčíst — a proč u každé položky | výklad+cvičení | 12 | must | 2 | K-01 |
| K-04 | K | Ticho je nález, ne absence nálezu | výklad | 10 | must | 2 | K-03 |
| K-05 | K | Citace se ověřuje, nevěří | demo+infra | 15 | should | P | K-01 |
| K-06 | K | Hierarchie autority rozhoduje spor, ne datum | výklad | 12 | should | 5 | — |
| K-07 | K | Čtvrtina mého `CLAUDE.md`, kterou nikdo nespustil ⚑ | příběh+demo | 15 | must | 3 | — |
| K-08 | K | Kostra je stejná, výbava se liší | výklad | 14 | must | 11 | — |
| K-09 | K | Rejstřík prvků je index faktů, ne jejich autorita | výklad | 18 | must | 11 | K-01 |
| K-10 | K | Kotva stárne, a devět z patnácti hlášení je šum | výklad | 12 | should | 11 | K-09 |
| R-01 | R | Zadání do souboru, session ho jen provede | demo+cvičení | 15 | must | 2 | K-01 |
| R-02 | R | Metodika bez spouštěče je jen text ⚑ | příběh+demo | 12 | must | 3 | R-01 |
| R-03 | R | Uložený postup místo opakovaného promptu | demo | 12 | should | 4 | R-02 |
| R-04 | R | Dvě vrstvy se rozjedou, když jednu nikdo nečte ⚑ | výklad | 10 | should | 3 | — |
| R-05 | R | Dva hooky, které mi běží, a šest, které neznám | demo | 12 | could | 4 | — |
| M-01 | M | Brána, kterou nikdo nespouští, je taky jen prompt ⚑ | výklad+demo | 18 | must | 3 | — |
| M-02 | M | „Napiš to do chatu, nic neměň" | demo+cvičení | 10 | must | 1 | — |
| M-03 | M | Triáž dělá člověk. Dva ze tří nálezů jsou falešné. | výklad+příběh | 15 | must | 4 | M-02 |
| M-04 | M | Slepý recenzent ⚠ | výklad | 10 | should | 4 | M-03 |
| M-05 | M | Vykazuj, kolik jsi toho NEzkontroloval | demo | 12 | must | 4 | M-01 |
| M-06 | M | Deterministická kontrola vs. sémantická | výklad | 12 | must | 4 | M-01 |
| M-07 | M | Práh, který realita překračuje — a prázdné pole ⚑ | příběh+demo | 12 | should | 3 | M-01 |
| M-08 | M | Dva exit kódy = dva různé signály | demo+infra | 10 | could | P | M-01 |
| O-01 | O | Subagent není o rychlosti, ale o tom, kam jde hluk | výklad+demo | 15 | must | 5 | F-05 |
| O-02 | O | Model podle povahy úlohy — a měřím to vůbec? ⚑ | výklad+příběh | 12 | should | 5 | O-01 |
| O-03 | O | Jak předat práci sobě zítra | demo | 12 | should | 5 | F-04 |
| O-04 | O | Jedna session = jedno téma, pojmenované | demo | 8 | should | 2 | — |
| O-05 | O | Izolace, které nerozumíš, tě stojí dopoledne ⚑ | příběh | 10 | must | 5 | N-02 |
| A-01 | A | Vrstvový audit dokumentace | výklad+cvičení | 25 | must | 6 | K-03, K-04 |
| A-02 | A | Číslovaný picklist a odpověď čísly | demo+cvičení | 15 | must | 2 | — |
| A-03 | A | Rozpočet na otázky a páka místo nejasnosti | výklad | 12 | must | 6 | A-01 |
| A-04 | A | Straw-man: napiš hypotézu, ať ji jen opraví | výklad+demo | 12 | must | 2 | — |
| A-05 | A | Sebekritika útokem na náklad na údržbu | výklad | 10 | must | 6 | — |
| A-06 | A | Redukce na minimální případ | příběh | 12 | must | 6 | — |
| A-07 | A | Specifikace invariantem místo symptomu | výklad | 12 | must | 6 | A-06 |
| A-08 | A | Publikum jako parametr — a pravidlo, které se poruší ⚑ | výklad+demo | 12 | should | 6 | — |
| A-09 | A | Vyjednej terminologii dřív, než začneš psát | výklad | 10 | should | 6 | — |
| U-01 | U | Debuguj prompt, ne výstup | výklad+cvičení | 15 | must | 7 | — |
| U-02 | U | Záchyt bez povyšovací brány je archiv ⚑ | příběh | 15 | must | 3 | M-01 |
| U-03 | U | Nástroj cestoval mezi projekty a vyrostl | příběh | 12 | should | 7 | — |
| U-04 | U | Nech si to vysvětlit laicky a pojmenuj, co nevíš | výklad | 10 | should | 7 | — |
| U-05 | U | Co commitnout, aby to fungovalo i kolegovi | demo | 12 | must | 7 | R-02 |
| U-06 | U | Vysvětlovací artefakt: osnovu nech schválit první | demo | 10 | should | 7 | — |
| U-07 | U | Co z toho po sedmi měsících doopravdy žije ⚑ | výklad | 10 | must | 7 | — |
| X-01 | X | Vygeneroval jsem 22 souborů a pak je smazal ⚑ | příběh | 10 | must | 3 | — |
| X-02 | X | Postavil jsem pipeline a nikdy ji nespustil ⚑ | příběh | 12 | must | 3 | — |
| X-03 | X | Tři situace, kdy jsem měl vypnout terminál | výklad | 10 | must | 7 | — |
| X-04 | X | Dlouhý prompt v chatu se tiše ořízne ⚠ | příběh | 10 | must | 2 | R-01 |

**Celkem 59 námětů, 738 minut.**
F 5 (69 min) · N 6 (66) · K 7 (96) · R 5 (61) · M 8 (99) · O 5 (57) · A 9 (120) ·
U 7 (84) · X 4 (42)

must 37 · should 16 · could 3 · `[demo]` 24 · `[příběh]` 16 · `[cvičení]` 7 · `[infra]` 3

**Blok `P`** = příloha „pro toho, kdo to bude stavět" — dva náměty, které jsou hodnotné,
ale bez postavené infrastruktury si z nich kolega odnese jen cíl.
**Blok `0`** = přípravné, musí existovat dřív než první díl.

---

# Karty námětů

## Okruh F — Fundament

Plný výklad všech pěti je ve [FUNDAMENT.md](FUNDAMENT.md), včetně dořešení jedenácti bodů,
které si první verze nedovolila tvrdit. Zde jen karty.

### F-01 — Claude si tě nepamatuje. Vede si o tobě složku.

**O čem to je.** Model je funkce z textu na text. Mezi dvěma voláními si nepamatuje nic.
„Paměť" konverzace je iluze, kterou vytváří okolí: při každém dalším promptu se **celá
dosavadní historie posílá znovu**. Proto „už jsem ti to říkal" nefunguje jako argument
a proto každý další prompt v dlouhé session stojí víc než ten předchozí, i když je kratší.

**Doklad:** `history.jsonl` — 2 671 promptů zapsaných na disku. Když jsem během této práce
data měřil, soubor mezi dvěma běhy skriptu povyrostl o čtyři prompty: o moje vlastní
prompty z toho měření.

**Role:** `[výklad]` + `[demo]` · **Náročnost:** nízká · **Odhad:** 15 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** otevřu `~/.claude/history.jsonl` a adresář se transkripty —
publikum vidí, že jejich konverzace je řada JSON řádků na jejich vlastním disku. Pak
slide 01 existujícího decku (model jako automat na text).

**Výhrada:** nesmí to sklouznout k „model je hloupý". Bezstavovost není nedostatek, je to
vlastnost, díky které funguje `/resume` i subagent.

### F-02 — Čeština není dražší, protože je delší ⚠

**O čem to je.** Model nevidí písmena ani slova, ale tokeny — kousky slov. Za ně se platí
a ony plní kontext. Čeština s diakritikou se seká na víc kousků, takže **tatáž informace
stojí víc tokenů, i když je napsaná kratšími slovy.** Praktický důsledek: šetři v souborech,
které se posílají pokaždé (`CLAUDE.md`, pravidla), ne v promptu, který napíšeš jednou.

**Doklad a poctivé rozdělení, co víme a co ne:**

| Tvrzení | Stav |
|---|---|
| ≈ 3,5 (glosář) až ≈ 4 znaky / 0,75 slova (Pricing FAQ) na token pro angličtinu | **dokumentováno, dvě oficiální stránky, dvě čísla** → uvádět rozsah (ověřeno 2026-09-09) |
| Tokenizér od Opus 4.7 dává na tomtéž textu ~30 % víc tokenů | **dokumentováno** — takže pro Opus 5 je to spíš ≈ 3,1 znaku/token |
| Poměr pro češtinu | **Anthropic nezveřejňuje** — žádné číslo neexistuje |
| Proč diakritika stojí víc | **odvozeno** z obecného principu byte-level BPE, nezávislý zdroj |
| `tiktoken` podhodnocuje o 15–20 %, „mnohem víc na neanglickém vstupu" | ~~dokumentováno~~ **zdroj nedohledán (2026-09-09)** — v oficiální dokumentaci Anthropic nenalezeno; nevyslovovat s číslem |

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** F-01 · **Priorita:** must

**Co ukážu na obrazovce:** slide 02 existujícího decku, ale **s upozorněním, že ten
tokenizér tokeny nepočítá** — jsou to zadrátovaná pole. Pak porovnám délku téže věty
ve znacích a vysvětlím princip.

**Výhrada — a je vážná.** Tohle **není demo**, je to výklad. Na tomto stroji neexistuje
způsob, jak tokeny spočítat: veřejný tokenizér pro Claude není a `count_tokens` API
vyžaduje klíč, který tu není. **Nesmí se vyslovit konkrétní počet tokenů pro českou větu.**
A pozor na past: draft původně chtěl v decku „opravit 3,5 na 4" — ale s tokenizérem
od Opus 4.7 je 3,5 blíž skutečnosti než 4. Správná oprava je uvést **rozsah s oběma
citacemi**, ne jedno číslo.

### F-03 — Tomu shrnutí můžeš říct, co má zachovat ⚠

**O čem to je.** Když se kontext plní, kompaktace starší část konverzace shrne a nahradí
souhrnem. Session tím zachrání — ale je to **nevratná ztráta neznámé části** historie.
Zůstane záměr a rozhodnutí, zmizí doslovné výstupy nástrojů, čísla řádků a přesné citace.
Analytik, který se opírá o `soubor:řádek`, po kompaktaci pracuje s vyprávěním o zdroji.

**A teď to, co většina lidí neví:** `/compact` **přijímá instrukci.**
`/compact zachovej rozhodnutí o pojmenování a čísla řádků u citací` — souhrn pak zachová,
co řekneš, místo toho, co si vybere sám.

**Doklad:** 19 kompaktací z transkriptů, **medián 97,3 % zahozeného kontextu.**
A **ani jedna z těch 19 neměla instrukci.** Plus dokumentovaný důsledek: popisky skillů
se po kompaktaci nenačtou znovu, takže Claude pak nezná skilly, které do té doby nepoužil.

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 15 min ·
**Závislosti:** F-01 · **Priorita:** must

**Co ukážu na obrazovce:** **statickou tabulku** z vlastních transkriptů (`preTokens` →
`postTokens` u devatenácti kompaktací) a `/context` v rozjeté session. Publikum vidí,
že „97 % zahozeno" není interpretace, ale číslo, které si harness sám zapsal.

**Výhrada:** **živou kompaktaci nepředvádět.** Medián je 181 s, nejdéle 224 s — tři minuty
spinneru a navíc si tím zabiješ session, ve které přednášíš. A parsování transkriptů
dokumentace nedoporučuje (formát je interní), takže čísla je nutné **zmrazit do statické
tabulky** předem, ne generovat naživo.

### F-04 — Padesát jedna ku jedné

**O čem to je.** `/compact` a `/clear` vypadají jako dvě varianty téhož. Nejsou.

| | `/clear` | `/compact` |
|---|---|---|
| Posílá request? | ne | ano, přes celou historii |
| Cena | nulová | plný vstup celé konverzace |
| Trvá | okamžik | medián 181 s, nejdéle 224 s |
| Zachová kontext? | ne — a ty to víš | částečně — a nevíš co |
| Kolikrát jsem to použil | **1×** | **51×** |

**Doklad:** `/compact` 51× proti `/clear` 1× v pracovních projektech. Celkem zahozeno
**8,6 milionu tokenů**. A z 19 zaznamenaných kompaktací bylo **19 ručních a 0
automatických** — nikdy jsem nenarazil na strop, vždycky jsem zasáhl sám při mediánu
464 352 tokenů, tedy asi na 46 % okna.

**Role:** `[příběh]` + `[demo]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** F-03 · **Priorita:** must

**Co ukážu na obrazovce:** tu tabulku a tři čísla na tabuli: **51 / 1 / 8 600 000.**
Nepotřebuje demo, čísla mluví sama.

**Výhrada:** je to přiznání vlastní chyby, ne best practice — musí se to tak i podat.

### F-05 — Co tě stojí místo, o kterém nevíš ⚠

**O čem to je.** V kontextu je řada věcí, které tam nikdo vědomě nedal: systémový prompt,
definice nástrojů, popisky všech dostupných skillů, obsah `CLAUDE.md`, paměti. Všechno
se posílá **znovu s každým promptem**. Prompt cache to zlevní na desetinu, ale **místo
v okně to zabírá pořád** — cache snižuje cenu za token, ne počet tokenů.

**Doklad:** dokumentace uvádí jako ilustrativní příklad projektové `CLAUDE.md` ≈ 1 800
tokenů. Moje má **23 427 znaků, tedy odhadem ~7 800 tokenů — přes čtyřnásobek.**
K tomu `MEMORY.md` 13 426 znaků.

**Role:** `[výklad]` + `[demo]` · **Náročnost:** střední · **Odhad:** 15 min ·
**Závislosti:** F-01 · **Priorita:** must

**Co ukážu na obrazovce:** **`/context` naživo** — to je jediné skutečné měření, které
mám k dispozici, a je okamžité. Rozpad zaplnění po složkách, přímo na této instalaci.

**Výhrada:** moje číslo „~13 000 tokenů, než napíšu první slovo" je **spodní hranice
a odhad** — spočítal jsem jen soubory, které umím přečíst, a přepočet na tokeny je
při 3,0 znaku/token odhad. Systémový prompt, definice nástrojů a metadata skillů do toho
nejsou zahrnuté, protože je ze souborů nevidím. Správná formulace je „**minimálně**
13 000 tokenů, a to je jen to, co si můžu změřit". Skutečné číslo dá `/context`.

---

## Okruh N — Nastavení a prostředí

### N-01 — Tři zákazy, které si nastav dřív než cokoli jiného

**O čem to je.** Nebezpečná operace se nezakazuje větou v `CLAUDE.md`, ale položkou
v nastavení. V obou mých projektech jsou tři: mazání souborů, `git push` a `git reset
--hard`. Není to nedůvěra k modelu — je to pojistka proti záměně, která stojí odpoledne.

**Doklad:** `.claude/settings.json` v alzask i fhb, shodně
`deny: ["Bash(rm *)", "Bash(git push*)", "Bash(git reset --hard*)"]`.
A živý doklad, že to funguje: **při psaní tohoto katalogu mi ten zákaz zabránil smazat
vlastní pomocný soubor v `C:\tmp`.** Nepohodlné, a přesně proto správné.

**Role:** `[demo]` · **Náročnost:** nízká · **Odhad:** 8 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** zkusím v cvičném repozitáři smazat soubor. Přijde odmítnutí.
Pak otevřu `settings.json` a ukážu ty tři řádky — je to celá implementace.

**Výhrada:** žádná. Je to osm minut a odnese si to každý.

### N-02 — Tři úrovně zpět: `Esc Esc`, `/rewind`, `git diff`

**O čem to je.** První otázka člověka, který se bojí pustit agenta na svá data, je
„a co když to rozbije". Prevence (N-01) je jen půlka odpovědi. Druhá půlka je náprava,
a má tři úrovně podle toho, jak daleko se to dostalo:

| Úroveň | Nástroj | Co vrátí |
|---|---|---|
| Špatný směr konverzace | `Esc Esc` | vrátí konverzaci o kus zpět |
| Špatná změna v souborech | `/rewind` | konverzaci **i kód** na předchozí checkpoint |
| Cokoli, co se dostalo dál | `git diff` a `git checkout` | poslední záchranná síť |

**Doklad:** v mých 2 671 promptech je `/rewind` **nulakrát**. Neznal jsem ho — a přitom
mám v katalogu jako `must` příběh o tom, jak mi vágní pokyn smazal rozpracovanou práci
(O-05). Položit problém a nedat lék je nejhorší kombinace, jaká v programu může být.

**Role:** `[demo]` · **Náročnost:** nízká · **Odhad:** 8 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** v cvičném repozitáři nechám udělat změnu, pak `/rewind`
a vrácení. Deterministické, okamžité, a je to jediná věc, která publiku sundá strach.

**Výhrada:** **netestováno** — `/rewind` jsem nikdy nepoužil. Před workshopem si to musím
vyzkoušet, jinak to nesmím předvádět.

### N-03 — Režim plánování: rozhodnutí odděleně od provedení

**O čem to je.** Analytik ze všeho nejvíc potřebuje „nejdřív si to rozmysli a napiš plán,
teprve pak sahej na soubory". Claude Code to má **vestavěné** — režim plánování,
přepínatelný klávesou. V tom režimu model nemůže měnit soubory, jen čte a navrhuje plán,
který schvaluješ.

**Doklad:** v 2 671 promptech je `/plan` **právě jednou** (2026-07-07 19:03, a hned po něm
jiný příkaz — vypadá to na neúspěšný pokus). Celou tuhle funkci jsem si sedm měsíců
nahrazoval ručně postavenými náhradami: zadáním do souboru (R-01), straw-manem (A-04),
větou „nic neměň" (M-02). Ty náhrady jsou dobré a zůstávají v katalogu — ale publikum
má zdarma vestavěný mechanismus, o kterém se z programu jinak nedozví.

**Role:** `[demo]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** přepnu do režimu plánování, zadám úkol, který by jinak začal
editovat soubory. Model vrátí plán a čeká na schválení. Přepnutí je deterministické
a okamžité.

**Výhrada:** je to přiznání — *„v mých 1508 promptech to není, naučil jsem se to pozdě."*
A **musím si to před workshopem vyzkoušet**, protože z vlastní praxe to neznám.

### N-04 — Prompt je zápis, ne rozhovor

**O čem to je.** Prompt vypadá jako chat, ale je to **záznam na disku** — v `history.jsonl`,
v transkriptu, a odchází na server. Co do něj napíšeš, tam zůstane. To má dva důsledky,
které si analytik musí uvědomit: **přístupové údaje do promptu nepatří nikdy**,
a **klientská data do něj patří jen s rozmyslem**.

**Doklad — nejostřejší v celém vzorku:** **čtyři přístupové tokeny v plném znění v pěti
promptech během 45 minut. Tři z nich musely být zneplatněny.**

**Doklad druhého druhu — absence:** slova „GDPR", „osobní údaj", „anonymizace",
„de-identifikace", „citlivé" mají ve **286 290 znacích** mých promptů **nula skutečných
zásahů** (šest nalezených výskytů „NDA" bylo uvnitř slova „standardní"). A obsahem té
práce jsou zákaznické specifikace, přepisy jednání se jmény lidí a e-maily dodavatelů.
Sedm měsíců jsem si tu otázku ani jednou nepoložil.

**Role:** `[příběh]` + `[výklad]` · **Náročnost:** nízká · **Odhad:** 15 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** ten prompt s tokenem (**maskovaně**) a datum, kdy musel být
zneplatněn. Pak `history.jsonl` — publikum vidí, že jejich prompty jsou soubor, který
si může přečíst kdokoli s přístupem k jejich profilu. Praktický závěr: co dát do souboru
a odkázat, co nedávat vůbec.

**A jeden odstavec navíc, který sem patří:** vlastnictví a licence výstupu. V mých datech
je k tomu **nula výskytů**, a přitom výstupy chodí zákazníkovi. Nemám na to odpověď
z praxe — patří to k dotazu na právní oddělení, ne do mého katalogu. Ale musí to zaznít.

**Výhrada:** nesmí to sklouznout do strašení. Cíl je jeden reflex — *než to odešlu,
je v tom něco, co bych nedal do e-mailu?*

### N-05 — Co to stojí a jak to zjistíš

**O čem to je.** Cena se skládá ze tří věcí, které se chovají jinak: **vstupní tokeny**
(a ty rostou s délkou session), **výstupní tokeny** (dražší, ale je jich méně)
a **prompt cache** (čtení za desetinu, ale zápis dráž než běžný vstup).

Orientační ceny za milion tokenů u nejsilnějšího modelu: **$5 vstup, $25 výstup**,
čtení z cache $0,50. Dlouhý kontext **nemá cenový příplatek** — 900tisícový požadavek
se účtuje stejnou sazbou jako devítitisícový.

**Doklad:** ověřené ceny z dokumentace (2026-08-26). **A přiznaná mezera:** kolik mě
sedm měsíců reálně stálo, **nevím** — nesbíral jsem to. Slova „pracnost", „man-day",
„story point" mají v mých promptech nula výskytů.

**Role:** `[demo]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** F-05 · **Priorita:** should

**Co ukážu na obrazovce:** `/usage` a `/context` — dva příkazy, které to řeknou za pár
sekund. To je celý námět: **nezkoumej ceník, změř si to.**

**Výhrada:** bez vlastních dat je to předčítání ceníku. Než tohle půjde na workshop,
musím pár týdnů sledovat `/usage` — jinak z toho není příběh, ale tabulka.

### N-06 — Cvičný repozitář — nulté dílo série

**O čem to je.** Katalog má 24 námětů s demem a 7 s cvičením — a **nikde se nesmí
sáhnout.** Všechna dema by se opírala o produkční repozitáře zákazníka, kde nesmím
commitovat a kde právě teď leží patnáct rozpracovaných souborů. Publikum nemůže cvičit
v zákazníkových datech a přednášející si nemůže dovolit reflexivní `git checkout .`.

**Řešení:** malý cvičný repozitář mimo produkci — tři až pět dokumentů, jeden `CLAUDE.md`,
jeden jednoduchý validátor a jeden **záměrně rozbitý** soubor. Na něm se dá předvést
prakticky vše z okruhů `N`, `M` a `K`, a hlavně si na něm publikum může zkusit i to,
co rozbije.

**Doklad:** stav produkčního repozitáře během psaní tohoto katalogu — patnáct
necommitnutých změn, včetně `CLAUDE.md` a samotných nástrojů, které by byly demo-rekvizitou.
Plus pravidlo, které mi v tom repozitáři zakazuje commitovat.

**Role:** `[infra]` · **Náročnost:** — (příprava, ne obsah) · **Odhad:** 15 min přípravy ·
**Závislosti:** — · **Priorita:** must, ale jako **blok 0** — musí existovat před prvním dílem

**Co ukážu na obrazovce:** nic. Tohle není námět na přednášení, je to **podmínka**, aby
ostatní dema fungovala.

**Výhrada:** je to práce navíc, kterou nikdo neuvidí. Ale bez ní se polovina katalogu
předvést nedá — a to je horší.

---

## Okruh K — Kontext a grounding

### K-01 — Dokument nese kontext, prompt nese rozhodnutí

**O čem to je.** Nejdůležitější námět celé série a jde proti intuici. Můj medián promptu
je 65 znaků, promptů nad 1000 znaků jsou 2 %. Vypadá to jako „piš krátce" — ale znamená
to, že **kontext leží v souborech, ne v promptu.**

Nejdelší prompt jednoho měsíce (2106 znaků) nese **patnáct odpovědí a ani jednu otázku.**
Otázky žijí v `BACKLOG.md`. Prompt je jen doručení rozhodnutí do rozjeté úlohy.

**Doklad:** `_raw/faze2b-prompty-alzask-07.md` (prompt z 2026-07-09 21:54) ·
`DOKLADY.md` část 1 (histogram: 47 % promptů pod 100 znaků)

**Role:** `[výklad]` + `[demo]` · **Náročnost:** střední · **Odhad:** 20 min ·
**Závislosti:** F-05 · **Priorita:** must

**Co ukážu na obrazovce:** vedle sebe ten 2106znakový prompt a `BACKLOG.md`, na který
odpovídá. Publikum vidí, že „krátký prompt" je vrchol ledovce.

**Výhrada:** funguje to jen tam, kde ten dokument někdo vede. Pro kolegu bez zavedeného
backlogu je první krok „založ si soubor", ne „piš krátce". Bez toho je rada škodlivá.

### K-02 — Bezcílný rozkaz ⚠

**O čem to je.** Nejčastější vada mého zadávání: prompt odejde jako holý rozkaz bez
uvedení, čeho se týká, a musí se poslat znovu s doplněnou cestou. Čistá režie.

**Doklad — pět doložených dvojic** (jedna z nich ve třech kolech) **a dalších pět
bezcílných rozkazů bez opravy:**

| Odeslané | O pár minut později |
|---|---|
| „V dokumentu" (07-10 07:14) | „V dokumentu @docs/analysis/Seznam_prvku…xml na listu Prvky…" (07:20) |
| „Oprav barevné signalizace podle nových změn v" (14:52) | „…v `docs/adr/hw/ADR-ASK-HW-001.md`" (14:54) |
| „Doplňuji info" (16:26) | „Doplňuji info do @docs/plc/BACKLOG.md: Reset tlačítko…" (16:28) |
| „Navrhni nejvhodnější pojmenování" (07-09 21:04) | + sloupce, list, soubor, zdroje — **tři kola** |

Bez opravy: `Proveď opravy`, `Reviduj`, `backlog aktualizuj`, `proveď revizi`, `Proveď revizi`.

**Role:** `[příběh]` + `[cvičení]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** ty dvojice vedle sebe. Pak cvičení: publikum dostane pět holých
rozkazů a doplní, co v nich chybí. Nejlevnější zlepšení v celé sérii.

**Výhrada:** draft původně tvrdil „jedenáct dvojic" — red-team ukázal, že doložených
párů je pět a zbytek jsou bezcílné rozkazy bez opravy. Obojí je vada, ale je to jiná
vada a číslo muselo být opravené.

### K-03 — Co NEčíst — a proč u každé položky

**O čem to je.** Do zadání nepatří jen „co si přečti", ale i **„co ignoruj, a proč".**
Bez toho model sáhne po souboru, který vypadá relevantně, a postaví na něm odpověď.

Klíčové je to „proč" u každé položky. Ne „neřeš baseline", ale **„rozdíl proti zmraženému
baseline NENÍ nález, je to vývoj"** — to si model nedomyslí.

**Doklad:** `_raw/faze2c-prompty-alzask-08.md` (P07) — sekce `CO NEČÍST` s důvody v obou
instancích vrstvového auditu · `_raw/faze2a-prompty-alzask-H1-06.md` (P3, P4)

**Role:** `[výklad]` + `[cvičení]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** K-01 · **Priorita:** must

**Co ukážu na obrazovce:** tentýž úkol dvakrát — bez sekce `CO NEČÍST` a s ní. Bez ní
model najde „rozpory", které jsou jen zastaralý baseline.

**Výhrada:** dá se to přehnat. Zadání, které vylučuje třicet souborů, má problém jinde.

### K-04 — Ticho je nález, ne absence nálezu

**O čem to je.** Když se ptáš, jestli tři dokumenty souhlasí, a jeden z nich o věci
**mlčí**, není to „v pořádku". Je to zjištění. Model bez explicitní instrukce mlčení
přeskočí, protože nemá co citovat — a ty se dozvíš „rozpor nenalezen".

Proto se u každé vrstvy vyžaduje **buď `soubor:řádek`, nebo doslovně „mlčí"**.

**Doklad:** `_raw/faze2c-prompty-alzask-08.md` (P15) — ta formulace je doslova v zadání
vrstvového auditu z 2026-08-14

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 10 min ·
**Závislosti:** K-03 · **Priorita:** must

**Co ukážu na obrazovce:** dva výstupy téhož auditu — bez té věty a s ní. Nálezy typu
„vrstva mlčí" jsou přesně ta místa, kde se implementace rozhodne sama za sebe.

**Výhrada:** je to zásada pro audit dokumentace, ne univerzální pravidlo.

### K-05 — Citace se ověřuje, nevěří `[příloha]`

**O čem to je.** `soubor:řádek` vypadá jako důkaz, ale je to **pozice, ne obsah.** Jak
dokument roste, řádek 412 ukazuje na něco jiného než včera — a citace vypadá pořád stejně
důvěryhodně. Odtud dvě odlišné situace: **posun** (obsah existuje, přesunul se) se opraví
mechanicky, **zmizení** (obsah tam není) je rozhodnutí pro člověka.

Kdo opraví zmizelou citaci přepsáním čísla řádku, vyrobí horší stav než zastaralý:
**tvar sedí, obsah lže.**

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (2.3) — verdikty `OK` / `POSUN` / `ZMIZELA`,
jednoznačnost kotvy 86 % → 95 % → 99 % podle šířky okna

**Role:** `[demo]` + `[infra]` · **Náročnost:** vysoká · **Odhad:** 15 min ·
**Závislosti:** K-01 · **Priorita:** should, **blok `P`** (příloha pro budovatele)

**Co ukážu na obrazovce:** přidám tři řádky nad citaci → `POSUN` a automatická oprava.
Pak citovaný text smažu → `ZMIZELA` a nástroj odmítne opravit sám.

**Výhrada:** patří do přílohy, ne do hlavního programu. Kolega bez toho nástroje si odnese
jen ostražitost vůči starým citacím — a to je málo na patnáct minut.

### K-06 — Hierarchie autority rozhoduje spor, ne datum

**O čem to je.** Když si dva dokumenty odporují, potřebuješ pravidlo, které rozhodne
**předem** — jinak rozhodne to, co model přečte první. Novější dokument nemusí vyhrát:
u mě specifikace prohrála s daty ze skutečného nasazení.

Nejhorší případ je **rozpor uvnitř téže vrstvy** — tam hierarchie nepomůže a implementátor
si vybere verzi, kterou přečte první.

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (2.6b/h) — sedm vrstev autority, doložený
případ, kdy novější specifikace prohrála

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** should

**Co ukážu na obrazovce:** tabulku vrstev a jeden reálný spor s verdiktem. Pak otázku
publiku: který z vašich dokumentů je nejvyšší autorita? (většinou to nikdo neví)

**Výhrada:** hierarchii musí někdo napsat a je to doménová práce.

### K-07 — Čtvrtina mého `CLAUDE.md`, kterou nikdo nikdy nespustil ⚑

**O čem to je.** `CLAUDE.md` je taky dokumentace — a stárne jako každá jiná. Rozdíl je
v tom, že **tuhle dokumentaci model bere jako platnou** a **platíš ji každý tah.**

**Čtyři exponáty z jednoho souboru:**

| Exponát | Doklad |
|---|---|
| Sekce „Projektový asistent" — 3 031 znaků, 12,7 % souboru, ~1000 tokenů každý tah | **za 2 678 promptů nespuštěna ani jednou** (`/learn`, `/lookup`, `/overview`, `/glossary` = 0×) |
| Popsaný formát souborů, který se už nepoužívá | soubor je na disku v jiném formátu, než `CLAUDE.md` tvrdí |
| Lokální nástroj, nahrazený pluginem | `CLAUDE.md` ho pořád popisuje jako aktuální |
| Vrstva „cross-project shared" pravidel | **ten adresář na disku vůbec není** (viz X-04 v `VYRAZENO.md`) |

**Doklad:** `_raw/faze5-redteam.md` (RT-02, RT-39) — nulový výskyt těch příkazů ve všech
2 671 promptech, ověřeno skriptem · `_raw/faze2d-prompty-fhb-myfaber.md` (X9) — tři doložené
nesoulady · velikost sekce měřená v znacích proti celku souboru

**Role:** `[příběh]` + `[demo]` · **Náročnost:** nízká · **Odhad:** 15 min ·
**Závislosti:** — · **Priorita:** must ⚑

**Co ukážu na obrazovce:** otevřu vlastní `CLAUDE.md`, označím tu čtvrtinu a řeknu, kolik
mě stála. Pak `grep` na příkazy, které v ní jsou popsané — nula výskytů v celé historii.
A `ls` na adresář, který v ní je uvedený a neexistuje.

**Výhrada:** je to nepříjemné přiznání, ne technika. A právě proto to funguje — publikum
má to samé a nevědí o tom. Zásada, kterou si odnesou: **co je v `CLAUDE.md`, platíš
každý tah, tak to jednou za čtvrt roku projdi.**

### K-08 — Kostra je stejná, výbava se liší

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

---

## Okruh R — Rozšíření

### R-01 — Zadání do souboru, session ho jen provede

**O čem to je.** Nejsilnější přenositelná praxe z celé inventury a stojí to jeden soubor.
Dlouhé zadání se napíše jako verzovaný Markdown **mimo chat** a prompt je jen ukazatel:
„Přečti X a proveď ho celý." Vypadá to jako prompt o 52 znacích — a je za ním 12,8 kB
zadání.

Řeší to tři věci naráz: zadání se dá **revidovat před spuštěním**, dá se **spustit znovu**
v jiné session, a je **v Gitu**, takže se z něj stane dokumentace postupu.

**Ověřená anatomie** (z obou reálných souborů, ne domněnka):

```
Proč (podklad — neměň závěry, můžeš je doplnit)
Dekompozice na části (Část A1 / A2 / B), každá:
    Problém / Vstup / Návrhové rozhodnutí, které dodrž / Fáze
Mantinely (platí pro celý úkol)
Definition of done
```

Druhý soubor navíc: `Krok 0 — ověření předpokladů (brána běhu, bez ní nepokračuj)`,
`Antipatterny`, `Historie revizí`.

**Doklad:** 2026-08-19 21:39 — 52 znaků → 12,8 kB · 2026-08-24 11:32 — 88 znaků → 7,3 kB.
Zdroj: `_raw/faze2e-prompty-shared.md` (P10). Vzor **v čase silní** — oba nejčistší
výskyty jsou nejnovější.

**Role:** `[demo]` + `[cvičení]` · **Náročnost:** nízká · **Odhad:** 15 min ·
**Závislosti:** K-01 · **Priorita:** must

**Co ukážu na obrazovce:** vedle sebe jednořádkový prompt a 12,8 kB soubor za ním.
**A pak meta-ukázka: tenhle katalog vznikl přesně tak** — zadání mělo 12 kB v souboru
a prompt zněl „Přečti si celý a proveď".

**A ještě jeden doklad, který se stal sám, během psaní tohoto katalogu.** V 9:31 padl
v jedné session pokyn *„Napiš prompt, který provede i v pluginu ontology-registry. Já jej
pak spustím sám."* — v 9:48 se v jiné session a jiném repozitáři objevilo
*„Přečti `C:/tmp/prompt-ontology-registry-kotvy.md` a proveď to."* a v 9:51 byly změněné
čtyři soubory. Ten vzor tedy nefunguje jen ve starých datech — použil se **nezávisle
v tu samou hodinu**, kdy jsem ho tady označoval za nejsilnější praxi. Je to nejlepší
možný doklad, protože ho nikdo nepřipravoval.

**Výhrada:** žádná. Nepotřebuje plugin ani nástroj, jen soubor.

### R-02 — Metodika bez spouštěče je jen text ⚑

**O čem to je.** Napsat postup do `README.md` nestačí — nikdo ho nespustí, protože
v README není „jak na to", ale „co platí". Postup potřebuje **spouštěč**: skill, který
se sám najde podle popisu, nebo slash command jako tenkou obálku nad ním.

Poznávací znamení, že ti spouštěč chybí: v návodu píšeš odstavec **„co řekneš Claude
Code"**. Tím jsi právě přiznal, že tam patří příkaz.

**Doklad:** vlastní zkušenost z 2026-08-25 — postavil jsem evidenci se třemi vrstvami
dokumentace a dostal otázku „Proč jsi na to nevytvořil skills? Rád bych to používal
opakovaně jednoduchým způsobem." Za tři hodiny z toho byly tři slash commandy.

**A tady je to sebe-ilustrující:** tenhle poznatek jsem si tehdy zapsal jako kandidáta
na pravidlo — a **do pravidla se nikdy nepovýšil.** Sám o něm mluvím na workshopu a sám
jsem ho nedotáhl. To je přesně ta propast mezi „vím to" a „mám to zařízené".

**Role:** `[příběh]` + `[demo]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** R-01 · **Priorita:** must ⚑

**Co ukážu na obrazovce:** návod s odstavcem „co řekneš Claude Code" a vedle toho command,
který ten odstavec nahradil. Pak ho spustím. A nakonec ten záznam v inboxu, který nikdy
nedošel do pravidel.

**Výhrada:** commandů má být tři až čtyři. Víc znamená, že si člověk nevybere.

### R-03 — Uložený postup místo opakovaného promptu

**O čem to je.** Když tentýž prompt píšeš třikrát, patří do souboru s příkazem. Zvlášť
u kroků, které se **snadno opomenou** — u nich rada v návodu nestačí, musí být součástí
postupu.

Reálný případ: „vždycky otevři přílohy" bylo devět dní radou. Pak se ukázalo, že
v přiloženém obrázku byly konkrétní hodnoty, které se devět dní vedly jako „chybí".
Dnes je čtení příloh **součást příkazu**.

**Doklad:** `docs/suppliers/POSTUP-pro-analytiky.md` — tři příkazy na osm situací ·
`_raw/faze3a-alzask-metodiky.md` (8, 9)

**Role:** `[demo]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** R-02 · **Priorita:** should

**Co ukážu na obrazovce:** spustím příkaz **nad anonymizovanou kopií dvou záznamů
v cvičném repozitáři** — ne nad produkční evidencí. Pak otevřu ten command a ukážu,
že je to obyčejný Markdown soubor.

**Výhrada:** původní plán byl pustit to nad skutečnou evidencí. To nejde — promítlo by to
jména zákazníka i dodavatelů a otevřené závazky na projektor. Anonymizovaná kopie je
podmínka, ne detail.

### R-04 — Dvě vrstvy se rozjedou, když jednu z nich nikdo nečte ⚑

**O čem to je.** Doporučení zní: dlouhá metodika pro člověka na vyžádání a krátký checklist
v automaticky načítaném kontextu; z krátkého ukazuj na dlouhé, neduplikuj.

**A teď co se stane, když se to nedodrží.** Mám 1201řádkovou metodiku a 69řádkový
quick-reference. Ale ten dlouhý dokument nikdo nečte, protože se načítá jen na vyžádání —
takže se rozešel se skutečností a nikdo si toho nevšiml. Rozdíl adresátů (`README` pro
člověka · `CLAUDE.md` pravidla · **skill = postup k provedení**) je správný princip,
ale **bez čtenáře je i dobrá struktura jen archiv.**

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (1.1) — poměr 1201 : 69 řádků ·
a doložené nesoulady v tom dlouhém dokumentu (K-07)

**Role:** `[výklad]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** should ⚑

**Co ukážu na obrazovce:** oba soubory vedle sebe, počet řádků, a pak jedno místo,
kde se ten dlouhý rozešel se skutečností.

**Výhrada:** `CLAUDE.md` v podadresáři se spolehlivě uplatní jen při práci v tom adresáři.
Na to se dá naletět — a já jsem naletěl.

### R-05 — Dva hooky, které mi běží, a šest, které neznám

**O čem to je.** Hook je příkaz, který harness spustí sám v určitém okamžiku. Rozdíl proti
validátoru: **nemusíš si na něj vzpomenout.**

**Doklad:** mám **čtyři aktivní hooky, ale jen dva různé eventy** z asi osmi.
Nejnápadnější mezera: při 51 kompaktacích nemám na kompaktaci pověšenou žádnou automatiku,
i když dokumentovaný vzor existuje. Zdroj: `_raw/faze1-korekce-hooky.md`.

**Role:** `[demo]` · **Náročnost:** vysoká · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** could

**Co ukážu na obrazovce:** **jen ty dva, které mi skutečně běží.** `/clear` a hned potom
hláška, kterou vypsal startovací hook — publikum vidí, že to nikdo nespustil ručně.
Pak `hooks.json`, aby bylo vidět, že je to pár řádků.

**Výhrada:** o hookech, které nepoužívám, mluvit jen jako o možnosti — **ne je předvádět.**
Draft původně chtěl doporučit hook na kompaktaci; ten sice existuje, ale nikdy jsem ho
nespustil, takže to nesmím podávat jako vyzkoušené.

---

## Okruh M — Mechanika kvality

### M-01 — Brána, kterou nikdo nespouští, je taky jen prompt ⚑

**O čem to je.** Zásada „kontrolu, kterou umí skript, nepiš jako věty do promptu" je
nejsilnější konvergence celé inventury — našlo ji pět nezávislých analýz. Důvod: věta
v promptu je **prosba** (model ji splní většinou), skript je **fakt** (vrátí chybu vždy,
i za půl roku, i po kompaktaci).

**A teď druhá polovina, kterou by draft zamlčel.** V tom samém projektu, který má na tuhle
zásadu vlastní pravidlo, **žádná brána neběží automaticky:**

- `core.hooksPath` míří do `.git/hooks`, kde není **jediný aktivní hook**
- `.githooks/` je v repozitáři nedotčené **7,2 měsíce** a i tak by kontrolovalo jen
  typy souborů, které tam nejsou
- CI spouští jen jednu denní úlohu, která kontroluje changelog

Takže validátory existují, jsou dobré, a **spouští je jedině člověk, když si vzpomene.**
To je přesně to, co ta zásada zakazuje.

**Doklad:** `_raw/faze5-redteam.md` (RT-35) — ověřeno na konfiguraci repozitáře ·
a protipól: pravidlo o pořadí záznamů v changelogu existuje 2,5 měsíce a **dodnes se
mechanicky porušuje**, protože ho nic nevynucuje

**Role:** `[výklad]` + `[demo]` · **Náročnost:** střední · **Odhad:** 18 min ·
**Závislosti:** — · **Priorita:** must ⚑

**Co ukážu na obrazovce:** dvě věci vedle sebe. Nejdřív **validátor naživo** — udělám
v souboru chybu, spustím, vrátí nenulový kód s pojmenovaným polem za necelou sekundu.
Nejrychlejší demo v katalogu. A hned potom `git config core.hooksPath` a `ls` na ten
adresář — je prázdný. Publikum vidí obojí: **že to funguje, a že to nikdo nespouští.**

**Výhrada a poučení, které si publikum odnese:** brána má tři části a lidé postaví jen
první. Kontrola (skript) · **spouštěč** (hook nebo CI) · a **reakce na výsledek**. Bez
druhé části je to nástroj, na který si musíš vzpomenout — tedy zase jen prosba, akorát
v jiném souboru.

### M-02 — „Napiš to do chatu, nic neměň"

**O čem to je.** Nejlepší poměr hodnoty a nákladu z celé inventury. Jedna věta, nulová
infrastruktura, funguje první den. Před zápisem do souborů si vyžádáš návrh **do chatu**
a zakážeš úpravu.

Je to zároveň nejlepší odpověď na strach z autonomie: nemusíš zakazovat práci se soubory
natrvalo, jen si oddělíš **návrh** od **provedení**.

**Doklad:** *„Navrhni ještě vhodnější pojmenování akce než je assignContainer. Napiš
varianty zde do chatu, nic neměň."* (2026-07-09 08:44) → o 25 minut později *„OK, rozhodl
jsem se pro containerPlaced. Oprav všude."* (09:09). Celkem **14 výskytů**, z toho 5×
s explicitním zákazem zápisu.

**Role:** `[demo]` + `[cvičení]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** tentýž úkol dvakrát. Bez té věty model začne editovat soubory.
S ní vypíše varianty s odůvodněním a čeká.

**Výhrada:** žádná — ale stojí za to zmínit, že vestavěný **režim plánování** (N-03) dělá
totéž systémověji. Tahle věta je to, co člověk použije, když si na režim nevzpomene.

### M-03 — Triáž dělá člověk. Dva ze tří nálezů jsou falešné.

**O čem to je.** Když necháš model najít chyby a hned je opravit, dostaneš dvě věci
zároveň: opravené skutečné chyby a **zanesené nové**, protože část nálezů byla falešná.
Triáž — rozhodnutí, který nález je skutečný — **nesmí být delegovaná.**

Číslo, které to dělá konkrétní: **počítej, že dva ze tří nálezů jsou falešné.**
Nezávislé měření precision revizorů dává 21–31 %.

**Doklad:** vlastní diagnóza z 2026-08-19 16:20: *„při opravách často dochází k zanášení
nových chyb a zároveň spotřebovává mnoho tokenů"* → o tři hodiny později náhrada:
linter bez modelu → **slepí** recenzenti, každý s jednou optikou → **triáž člověkem** →
opravy po jedné větě, ne přepisem sekce.

**A ještě jeden doklad z této práce:** red-team proti tomuto katalogu vznesl 42 nálezů.
Zapracoval jsem je **selektivně** — část jako opravu, část jako přeformulování, část
jako odmítnutí. Kdybych je nechal zapracovat automaticky, katalog by se scvrkl na tři díly
a přišel bych o zásobu, která byla cílem.

**Role:** `[výklad]` + `[příběh]` · **Náročnost:** střední · **Odhad:** 15 min ·
**Závislosti:** M-02 · **Priorita:** must

**Co ukážu na obrazovce:** report z revize a projdu s publikem tři nálezy — u jednoho
se ukáže, že je falešný. Pak ten protokol: co dělá stroj, co člověk.

**Výhrada:** vyžaduje to disciplínu, ne nástroj. A je to nepohodlné, protože „nechat to
opravit samo" je pohodlnější.

### M-04 — Slepý recenzent ⚠

**O čem to je.** Recenzentovi **neříkej, co a proč jsi změnil.** Když to ví, hledá
potvrzení tvého záměru. Když to neví, čte artefakt jako cizí text.

Praktická formulace: *„artefakt jako cizí text, bez věty, co a proč jsme měnili"*.
A u verifikace opravy: *„ANI SLOVO o tom, že jde o opravenou verzi"*.

**Doklad:** `_raw/faze3b-pluginy.md` (2) — v definici revizního agenta je klauzule
o slepotě napsaná explicitně · `_raw/faze2c-prompty-alzask-08.md` (P18)

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 10 min ·
**Závislosti:** M-03 · **Priorita:** should

**Co ukážu na obrazovce:** **statický exponát** — tu klauzuli v definici agenta,
a vedle ní zadání, které slepotu ruší.

**Výhrada:** draft to chtěl jako demo („spustím dva recenzenty a uvidíte rozdíl").
To nejde: model není deterministický, takže demo je **tvrzení o tom, jak se model
zachová** — a když se zachová jinak, tvrzení se před publikem samo vyvrátí.
Statický exponát tuhle slabinu nemá.

### M-05 — Vykazuj, kolik jsi toho NEzkontroloval

**O čem to je.** „Nic jsem nenašel" a „nic jsem neměřil" vypadají v reportu stejně.
Rozdíl udělá **součtová pojistka**: kontrola vykáže nejen nálezy, ale i kolik položek
vůbec nekontrolovala a proč.

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (2.3) — brána vykazuje součet
`2558 = 1278 kontrolováno + 0 bez kotvy + 661 mimo kontrolu + 619 opakovaných`.
Bez toho čísla by „1278 zkontrolováno" znělo jako úplnost.

**A meta-doklad:** tenhle katalog má tu pojistku taky — `VYRAZENO.md` sekce C přiznává,
co v datech není. **Report bez sekce „co chybí" je nedokončený report.**

**Role:** `[demo]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** M-01 · **Priorita:** must

**Co ukážu na obrazovce:** ten součet naživo. A pak stejnou úlohu bez pojistky — report
řekne „vše v pořádku", i když se polovina položek nekontrolovala.

**Výhrada:** je to nepohodlné. Pojistka vždycky ukáže, že jsi zkontroloval méně,
než sis myslel.

### M-06 — Deterministická kontrola vs. sémantická

**O čem to je.** Rozděl kontroly na **ověřitelné bez porozumění** (čísla, odkazy, formát,
součty → skript) a **vyžadující porozumění** (souhlasí popis s diagramem? → model nebo
člověk). A pak to hlavní: **nikdy nenech druhou hromádku předstírat, že dělá práci první.**

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (4.2) — linter má pravidla deterministicky,
sémantickou konzistenci **explicitně nechává** na kontrole modelem, a je to napsané
v jeho dokumentaci jako známé omezení

**A doklad, proč to platí:** tučně značená tabulka místo nadpisu tiše vypnula celou třídu
kontrol — a přesně tak unikla chyba ve velikosti datového pole. Nástroj kontroluje jen to,
co pozná.

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** M-01 · **Priorita:** must

**Co ukážu na obrazovce:** změním hodnotu tak, aby porušila pravidlo → linter to chytí
okamžitě s kódem chyby. Pak změním **význam** popisu, aby nesouhlasil s diagramem →
linter mlčí. To je ta hranice.

**Výhrada:** hranice není vždy ostrá. Ale mít ji napsanou je lepší než ji nemít.

### M-07 — Práh, který realita překračuje — a prázdné pole, ze kterého se počítá ⚑

**O čem to je.** Brána, která hlásí 56 varování, přestala být bránou — mezi nimi se ztratí
dvě skutečné chyby a lidé si zvyknou přehlížet i je.

**A druhá vrstva téhož problému:** ten práh se počítá z pole, které **32 z 35 dokumentů
vůbec nemá vyplněné.** Takže brána měří stárnutí na datech, která z většiny neexistují.
A devět nejstarších architektonických rozhodnutí je pořád ve stavu „draft".

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (1.3) — práh 30 dní, 23 dokumentů v draftu
55–201 dní, výsledek 56 varování a 2 skutečné chyby · `_raw/faze5-redteam.md` (RT-40) —
prázdné pole u 32 z 35, devět rozhodnutí ve stavu draft

**Role:** `[příběh]` + `[demo]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** M-01 · **Priorita:** should ⚑

**Co ukážu na obrazovce:** spustím validátor a nechám publikum **najít ty dvě chyby
v 56 varováních.** Nikdo je nenajde. Pak ukážu, že pole, ze kterého se práh počítá,
je většinou prázdné.

**Výhrada:** žádná — je to obecná vlastnost varovných systémů. Tři možnosti, co s tím:
zvednout práh, snížit závažnost, nebo ho zrušit. Nechat ho křičet do prázdna je nejhorší.

### M-08 — Dva exit kódy = dva různé signály `[příloha]`

**O čem to je.** Brána musí rozlišit „evidence je poškozená" (blokuj) od „je tu otevřená
práce" (jen upozorni). Bez toho buď zablokuješ proces kvůli běžnému čekání, nebo si zvykneš
ignorovat i skutečné chyby. Zvláštní případ: **„čekáme na externí vstup" není chyba,
je to stav.**

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (3.5, 4.4b)

**Role:** `[demo]` + `[infra]` · **Náročnost:** střední · **Odhad:** 10 min ·
**Závislosti:** M-01 · **Priorita:** could, **blok `P`**

**Co ukážu na obrazovce:** spustím kontrolu nad evidencí, ve které jsou otevřené dotazy
čekající na odpověď dodavatele — vrátí nenulový kód a výpis „je tu otevřená práce",
ale proces to nezastaví. Pak v té evidenci porušim invariant (dva záznamy se stejným
identifikátorem) a spustím totéž — vrátí jiný kód a jinou hlášku, a tenhle stav
proces zastavit má. Publikum vidí, že to nejsou dvě hlasitosti téhož signálu,
ale dva různé signály, na které se reaguje jinak.

**Výhrada:** patří do přílohy pro budovatele. Zásada je přenositelná, kódy jsou moje.

---

## Okruh O — Orchestrace

### O-01 — Subagent není o rychlosti, ale o tom, kam jde hluk

**O čem to je.** Nejčastější nedorozumění: subagent se používá, aby to bylo rychlejší.
Hlavní důvod je jiný — **jeho hluk zůstane mimo tvůj kontext.** Agent přečte sedmdesát
souborů, udělá čtyřicet volání nástrojů a vrátí ti dvacet řádků. Těch sedmdesát souborů
se do tvého okna nikdy nedostane.

**Doklad:** tenhle katalog. Třináct agentů zpracovalo přes 500 KB podkladů; do hlavního
kontextu se z toho vrátily souhrny po dvaceti řádcích. Bez toho by hlavní session
kompaktovala několikrát — a víme, co kompaktace udělá (medián 97,3 %).

**Role:** `[výklad]` + `[demo]` · **Náročnost:** střední · **Odhad:** 15 min ·
**Závislosti:** F-05 · **Priorita:** must

**Co ukážu na obrazovce:** zadám agentovi „prohledej tenhle adresář a vrať tři nálezy",
pak `/context` — okno se prakticky nezvětšilo. Vedle toho totéž bez agenta: okno naroste
o stovky řádků výpisů.

**Výhrada:** agent nevidí tvou konverzaci. Co mu neřekneš v zadání, to neví — a špatně
zadaný agent vrátí sebevědomou hloupost. Platí u něj vše z okruhu `K`, jen dvakrát.
Konkrétní doklad z této práce: jeden agent nahlásil **nula hooků**, přitom jsou čtyři —
podíval se jen do jednoho souboru a nedomyslel, že hooky bývají i v pluginech.

### O-02 — Model podle povahy úlohy — a měřím to vůbec? ⚑

**O čem to je.** Model se nevybírá podle důležitosti úkolu, ale podle **povahy práce**.
Mechanické čtení a výčty zvládne malý model; rozlišit „přenositelná praxe" od „jednorázovka"
je úsudek, na který malý model vrátí seznam všeho. A gotcha: **subagent nedědí tvou volbu
modelu automaticky.**

**A teď to nepříjemné.** Přepnul jsem model **63×** — a v celé své praxi jsem
**ani jednou neměřil, jestli to k něčemu bylo.** Jeden doložený oblouk končí tím, že jsem
po ~20 promptech ladění modelu a reasoning effortu všechno **revertoval** — protože jsem
neměl srovnávací základnu a nevěděl jsem, co bylo nastavené předtím. Průlom přišel
otázkou, kterou jsem si měl položit na začátku: *„Jaký model a effort byl používaný
předtím, než jsme začali provádět dnešní změny?"*

**Doklad:** `/model` 63× v celé historii, 53× v pracovních projektech · `/effort` jen 9× ·
`_raw/faze2b-prompty-alzask-07.md` (O3, N2, X4)

**Role:** `[výklad]` + `[příběh]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** O-01 · **Priorita:** should ⚑

**Co ukážu na obrazovce:** rozdělení modelů v této práci a proč. Pak ten oblouk, který
skončil revertem. Poučení: **než začneš ladit nastavení, zapiš si, co bylo předtím.**

**Výhrada:** je to úsudek, ne tabulka. A nejlevnější model dělá chyby, které musíš umět
poznat — jinak jsi ušetřil tokeny a koupil si nesprávná data.

### O-03 — Jak předat práci sobě zítra

**O čem to je.** Session skončí, kontext zmizí. Rozdíl mezi `/resume` a novou session
s předáním je v tom, co si nesete: `/resume` obnoví celou historii (a s ní všechen hluk),
předání přes soubor nese **jen závěry**.

Co `/resume` **neobnoví**: prompt cache (první request je pak nejdražší v session)
a běžící úlohy na pozadí — nikdy.

**Doklad:** `/resume` 33× v pracovních projektech proti `/clear` 1× ·
`_raw/faze2c-prompty-alzask-08.md` (P17) — handoff prompt s prioritami, doklady
a **sekcí o tom, co ještě neplatí**

**Role:** `[demo]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** F-04 · **Priorita:** should

**Co ukážu na obrazovce:** reálný handoff soubor — priority, doklady, a hlavně ta sekce
„co ještě neplatí". Pak start nové session jen s tím souborem.

**Výhrada:** napsat dobrý handoff trvá deset minut. Vyplatí se u úlohy na několik dní,
ne u půlhodinové práce.

### O-04 — Jedna session = jedno téma, pojmenované

**O čem to je.** Session, ve které řešíš tři různé věci, má trojnásobný kontext a nedá se
v ní zpětně nic najít. Pojmenovaná session je navíc podmínkou toho, aby se dala později
analyzovat — bez jména je seznam session k nepoužití.

**Doklad:** `/rename` **35×** v celé historii — pátý nejčastější příkaz vůbec.
Zdroj: `DOKLADY.md` část 1.

**Role:** `[demo]` · **Náročnost:** nízká · **Odhad:** 8 min ·
**Závislosti:** — · **Priorita:** should

**Co ukážu na obrazovce:** seznam pojmenovaných session proti seznamu nepojmenovaných.
V druhém nikdo nic nenajde. Třicet sekund a je to jasné.

**Výhrada:** je to zvyk, ne mechanika — nic ho nevynucuje.

### O-05 — Izolace, které nerozumíš, tě stojí dopoledne ⚑

**O čem to je.** Imperativ bez jednoznačného cíle je nedeterministický. „Pracuj
v samostatné worktree!" neurčuje **které** — a agent použil existující, ve které byla
rozpracovaná práce.

**Doklad:** 2026-06-19 22:08: *„Měl sis založit nové worktree. Můžeš obnovit soubory,
které jsi mi vymazal?"* Náprava je v datech vidět o hodinu později — explicitní cesta
plus slovo „izolovaně".

**A druhá polovina příběhu, která je vlastně poučnější:** izolaci jsem zkoušel **jeden
den**, pak jsem ji v nastavení **vypnul** a nikdy k ní nevrátil. Nástroj, kterému jsem
nerozuměl, mě stál dopoledne a skončil vypnutý. To není chyba nástroje — je to doklad,
že **izolaci si musíš nejdřív pochopit na cvičném repozitáři**, ne na rozpracované práci.

**Role:** `[příběh]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** N-02 · **Priorita:** must ⚑

**Co ukážu na obrazovce:** ten prompt a jeho opravenou verzi. Pak nastavení, kde je
izolace dodnes vypnutá. **Demo naživo ne** — stačí ty dva prompty.

**Výhrada:** je to nejtvrdší příběh v katalogu (ztráta dat) a musí se podat věcně,
ne jako strašení. A **nesmí zůstat bez léku** — proto je závislost na N-02 (jak to vzít
zpátky) povinná.

---

## Okruh A — Analytické postupy

### A-01 — Vrstvový audit dokumentace

**O čem to je.** Nejsilnější jednotlivý artefakt celé inventury. Model dostane **tytéž
skutečnosti popsané ve dvou nebo třech dokumentech na různých úrovních** (záměr / kontrakt /
návod) a hledá rozpory **na hranici mezi vrstvami**, ne uvnitř jedné.

Devítibodová kostra, ověřená ve dvou reálných instancích:

```
1  ROLE SOUBORŮ    které jsou vrstvy a co která znamená
2  JAK ČÍST        „včetně poznámek, TODO a odstavců typu k dořešení —
                    právě tam bývá věta, která ruší platnost mechanismu nad ní"
3  CO NEČÍST       + důvod u každé položky
4  ROZHODČÍ        kde je rozhodnutí, když si vrstvy odporují
5  CO HLEDAT       pojmenovaná taxonomie rozporů (A–H)
6  ÚKOL            3 body s nejvyšší pákou
7  VÝSTUP          stav ve VŠECH vrstvách: citace soubor:řádek NEBO „mlčí"
8  OTÁZKY          rozpočet 5, uzavřené, varianty (a)/(b)/(c), doporučená
9  PRAVIDLA        nic z paměti · pravidlo ≠ instance · nesahej na soubory
```

**Doklad:** dvě plné instance (2026-08-14 19:36 a 20:29) plus tři předchůdci — vznikl
**jako produkt pěti iterací z jednovětného zadání**, ne najednou. Zdroj:
`_raw/faze2c-prompty-alzask-08.md` (P06).

**Role:** `[výklad]` + `[cvičení]` · **Náročnost:** vysoká · **Odhad:** 25 min ·
**Závislosti:** K-03, K-04 · **Priorita:** must

**Co ukážu na obrazovce:** tu kostru jako handout, pak jeden reálný nález. A cvičení:
publikum dostane dva svoje dokumenty a zkusí vyplnit body 1–4.

**Výhrada:** potřebuje jedinou věc — **aby v projektu existovaly dva dokumenty popisující
totéž na jiné úrovni.** Žádný nástroj. Ale je to nejdelší námět v katalogu a na krátké
setkání se nevejde s ničím jiným.

### A-02 — Číslovaný picklist a odpověď čísly

**O čem to je.** Druhá nejsilnější konvergence (čtyři nezávislé nálezy). Model vypíše
očíslovaný seznam — nálezů, otázek, variant, bodů z jednání — a ty odpovíš **čísly**.
Bez toho se konverzace rozpadne na dohadování, který bod se právě řeší.

**Doklad:** vlastní příkaz na body z jednání použit **34×** — je to můj nejpoužívanější
vlastní příkaz vůbec, a to je samo o sobě doklad (na rozdíl od těch, které mám postavené
a nespouštím).

**Role:** `[demo]` + `[cvičení]` · **Náročnost:** nízká · **Odhad:** 15 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** vezmu přepis jednání (**anonymizovaný**), nechám z něj
vygenerovat číslovaný picklist a odpovím „3, 7, 9 ano; 4 ne; 5 později". Publikum vidí,
jak se z hodinového jednání stane seznam úkolů za dvě minuty.

**Výhrada:** funguje to jen s **uzavřenými** body. Číslovaný seznam otevřených otázek
typu „zvážit architekturu" se čísly odpovědět nedá.

### A-03 — Rozpočet na otázky a páka místo nejasnosti

**O čem to je.** Dvě věty, které dělají doptávání použitelným.

**Rozpočet:** „zeptej se na nejvýš pět věcí" donutí model vybírat. Bez rozpočtu dostaneš
dvacet otázek a odpovíš na tři.

**Páka místo nejasnosti:** neptej se „co je nejasné", ale **„co drží nejvíc navazujícího"**.
Nejasností je vždycky víc než těch, na kterých něco závisí.

**Doklad:** `_raw/faze2c-prompty-alzask-08.md` (P04, P05) — rozpočet pěti uzavřených otázek
a „páka" jako explicitní řadicí kritérium; vzniklo ve čtyřech iteracích

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** A-01 · **Priorita:** must

**Co ukážu na obrazovce:** tentýž úkol s „zeptej se, co je nejasné" a s „vyber tři body
s nejvyšší pákou". První dá výčet, druhý prioritu.

**Výhrada:** žádná. Jsou to dvě věty v zadání.

### A-04 — Straw-man: napiš hypotézu, ať ji jen opraví

**O čem to je.** Otevřená otázka („jak to má fungovat?") dá esej. **Hypotéza k vyvrácení**
(„myslím, že to funguje takhle — kde se mýlím?") dá opravu. A opravu se posoudí snáz
než návrh.

Funguje to i směrem k lidem: dotaz dodavateli, který **obsahuje navrhovanou odpověď**,
se vrací rychleji, protože protistrana jen potvrdí nebo škrtne. A obecná forma téhož:
*„zjisti to a rozhodni mezi hypotézami A, B, C"* místo otevřeného „prozkoumej".

**Doklad:** `_raw/faze2c-prompty-alzask-08.md` (P11, P23) · `_raw/faze3b-pluginy.md` (11)
— agent v pluginu píše vlastní hypotézu řešení **dřív**, než se začne ptát

**Role:** `[výklad]` + `[demo]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** tentýž problém zadaný jako otázka a jako hypotéza. Rozdíl
v délce i použitelnosti odpovědi je okamžitě vidět.

**Výhrada:** hypotéza musí být formulovaná tak, aby se dala vyvrátit. „Myslím, že by to
mělo být dobré" není hypotéza.

### A-05 — Sebekritika útokem na náklad na údržbu

**O čem to je.** Nejcennější dosud nepojmenovaná praxe. Návrh se nekritizuje otázkou
„je to správně" (na tu model odpoví ano), ale **„kolik to bude stát na údržbě"** — a to
je otázka, kterou si model sám nikdy nepoloží.

Formulace, které fungují: *„Mám obavy, že se tyto odkazy rychle rozjedou."*
*„Připadá mi to neefektivní, chybné a zbytečné. Je to tak?"*

**Doklad:** sedm výskytů v posledních pěti dnech měřeného období.
Zdroj: `_raw/faze2c-prompty-alzask-08.md` (P28).

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** návrh, který model označil za dobrý, a pak tutéž věc po otázce
na náklad údržby — model sám najde tři místa, která se rozjedou.

**Výhrada:** musí to zaznít **před** implementací, ne po ní. A je to nejlevnější způsob,
jak z modelu dostat oponenturu.

### A-06 — Redukce na minimální případ

**O čem to je.** Po sérii selhání se nepokračuje dalším pokusem, ale **zmenšením úlohy
tak, aby se dala ověřit.** Klasické ladění — ale u práce s modelem se na to zapomíná,
protože „ještě jeden prompt" je vždycky po ruce.

Průlom v mém nejhorším případě přišel od člověka, ne od modelu: *„Pojďme to řešit
po částech… Pokud by měl dopravník jen segmenty Z1, Z2, Z3…"*

**Doklad:** **30 promptů na jeden algoritmus, 8 kol ladění obrázky** (13.–14. 7.).
Zdroj: `_raw/faze2b-prompty-alzask-07.md` (A1, nejsilnější příběh měsíce).

**Role:** `[příběh]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** časovou osu těch 30 promptů a v ní bod, kde se to zlomilo.
Publikum uvidí, že to nebyl lepší prompt, ale menší úloha.

**Výhrada:** vyžaduje sebeovládání. „Ještě jeden pokus" je vždycky lákavější
než „pojďme to zmenšit".

### A-07 — Specifikace invariantem místo symptomu

**O čem to je.** Rub předchozího námětu. Když popisuješ, co je špatně („nosič se zasekne
na křižovatce"), model opravuje symptom. Když popíšeš **invariant, který má platit vždy**
(„na segmentu smí být nejvýš jeden nosič, a to i během přesunu"), model má co ověřovat.
Invariant je navíc testovatelný — symptom není.

**Doklad:** `_raw/faze2b-prompty-alzask-07.md` (A2) — v obou nejdelších selhavších
obloucích měsíce chyběl testovatelný invariant a zafixovaná základna

**Role:** `[výklad]` · **Náročnost:** vysoká · **Odhad:** 12 min ·
**Závislosti:** A-06 · **Priorita:** must

**Co ukážu na obrazovce:** tentýž problém popsaný jako symptom a jako invariant.
U druhého model sám navrhne, jak to ověřit.

**Výhrada:** formulovat invariant je analytická práce a chvíli to trvá. Není to zkratka,
je to investice, která se vrátí u třetího kola ladění.

### A-08 — Publikum jako parametr — a pravidlo, které se poruší ⚑

**O čem to je.** Adresát dokumentu není kosmetika, je to **omezení, co v něm smí být.**
Specifikace pro externího dodavatele musí být sebe-nosná — nesmí odkazovat na interní
rozhodnutí, která adresát nemá.

**A pak druhá polovina:** tohle pravidlo mám napsané, prošlo revizí — a **v produkční
specifikaci pro externího dodavatele jsou dva odkazy na interní rozhodnutí.** Pravidlo bez
brány se pomalu poruší, i když ho autor zná a věří mu.

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (4.3) — dva doložené zásahy v produkčním
dokumentu, který prošel revizí

**Role:** `[výklad]` + `[demo]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** should ⚑

**Co ukážu na obrazovce:** `grep` na interní identifikátory v dokumentu určeném externímu
adresátovi. Dva zásahy. Pak stejná kontrola jako součást brány — a otázka, proč jsem ji
nikdy nespustil.

**Výhrada:** je to zároveň námět o publiku a doklad k M-01. Dá se použít v obou rolích.

### A-09 — Vyjednej terminologii dřív, než začneš psát

**O čem to je.** Když se pojmy dohodnou až v revizi, přepisuje se celý dokument. A druhá,
méně zjevná část: **nezaváděj nový pojem — zjisti, který se už v projektu používá
častěji.** Model rád vymyslí čistší termín, než jaký tým skutečně používá.

**Doklad:** `_raw/faze2c-prompty-alzask-08.md` (P12, P13) · `_raw/faze2b` (K6) —
sjednocení terminologie napříč dokumenty a zavedení do glosáře

**Role:** `[výklad]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** should

**Co ukážu na obrazovce:** `grep -c` na dva konkurenční termíny v repozitáři. Čísla
rozhodnou spor, který by jinak byl otázkou vkusu.

**Výhrada:** funguje jen tam, kde už nějaká dokumentace je. Na zelené louce se terminologie
nevyjednává, tam se zapisuje.

---

## Okruh U — Učení a znalostní smyčka

### U-01 — Debuguj prompt, ne výstup

**O čem to je.** Když odpověď není dobrá, obvyklá reakce je opravit odpověď. Užitečnější
je opravit **zadání** — a ještě užitečnější zpětně se podívat, **proč** to zadání selhalo.

Otázky, které to spustí: *„Zajímají mě především principy a to, jak se mohu poučit, jak
lépe agenty instruovat, aby buď vytvořili kvalitnější řešení, nebo se mě doptali."*
*„Díky čemu se to podařilo? Bude to fungovat i příště?"*

**Doklad:** deset promptů tohoto typu, nulová infrastruktura. Konvergence čtyř nezávislých
nálezů. Zdroj: `_raw/faze2a-prompty-alzask-H1-06.md` (P6), `_raw/faze2b` (U1, U2, U5),
`_raw/faze2c` (P33).

**Role:** `[výklad]` + `[cvičení]` · **Náročnost:** střední · **Odhad:** 15 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** vezmu skutečně selhaný běh a zeptám se modelu, co v zadání
chybělo. Odpověď je použitelná — a je to zdarma.

**Výhrada:** žádná, a je to nejlepší způsob, jak se v tom zlepšovat bez učitele.

### U-02 — Záchyt bez povyšovací brány je archiv ⚑

**O čem to je.** Postavil jsem třístupňovou znalostní smyčku: zachytit chybu → povýšit
na osobní pravidlo → konsolidovat do sdílených. Governance, vlastnictví, všechno.

**Výsledek po dvou a půl měsících:** z asi 63 zachycených kandidátů se povýšilo **pět** —
a všech pět v **prvních šesti dnech** provozu. Pak 47 dní nic. Prostřední stanice je
od založení **prázdná**.

**Proč:** zachytávání má spouštěč — hook mi inbox nabídne na začátku každé session.
Povyšování spouštěč nemá. **Smyčka, která sama nemá bránu na svůj vlastní krok, není
smyčka, je to archiv.** A je to zvlášť ironické u mechanismu, jehož vlastní pravidlo říká
„vynucuj bránou, neinstruuj v promptu".

**Doklad:** `_raw/faze3c-pravidla-inbox.md` — 5 z 63, git log potvrzuje prázdnou
prostřední zónu

**Role:** `[příběh]` · **Náročnost:** střední · **Odhad:** 15 min ·
**Závislosti:** M-01 · **Priorita:** must ⚑

**Co ukážu na obrazovce:** obsah inboxu (počet souborů a kandidátů) proti počtu pravidel,
která z nich vznikla. A datum posledního povýšení.

**Výhrada:** ten záchyt **sám o sobě cenu má** — tenhle katalog z něj čerpá. Takže poučení
není „nedělej to", ale **„počítej s tím, že bez spouštěče to zůstane archivem, a rozhodni
se, jestli ti archiv stačí."**

### U-03 — Nástroj cestoval mezi projekty a vyrostl

**O čem to je.** Nejlepší příběh o přenositelnosti, jaký v datech mám. Šablona vrstvového
auditu (A-01) **vznikla na jednom projektu** a za **šestnáct minut** jela na druhém —
kde se navíc rozšířila o dva nové bloky (`CO NEČÍST` a `ROZHODČÍ`) a rozpočet otázek.

Poučení: **přenos nástroje mezi projekty ho zlepší**, protože druhý projekt má jiné
slabiny než první.

**Doklad:** 2026-08-14 — 19:36 vznik na projektu A, 20:29 běh na projektu B už v rozšířené
podobě. Zdroj: `_raw/faze2d-prompty-fhb-myfaber.md`.

**Role:** `[příběh]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** should

**Co ukážu na obrazovce:** oba prompty vedle sebe s časy a rozdílem — publikum vidí,
co přibylo.

**Výhrada:** ostatní přenosy takhle nedopadly. Deset ze třinácti pravidel se přeneslo
**ruční kopií souborů** a čtyři soubory jsou bit-shodné — takže se od té doby nesladilo
nic (viz `VYRAZENO.md` A3). Ten jeden úspěšný přenos byl úspěšný proto, že se **neopisoval,
ale používal.**

### U-04 — Nech si to vysvětlit laicky a pojmenuj, co nevíš

**O čem to je.** Před rozhodnutím si nech věc vysvětlit **bez žargonu** a pak si
pojmenuj, čemu pořád nerozumíš. To druhé je ta cenná část — a je to legitimní prompt:
*„Ještě tomu nerozumím."* / *„Jen pro mou informaci, vysvětli mi…"*

Funguje to i naopak: nechat si od modelu položit kvíz na téma, které se učíš, je rychlejší
kontrola pochopení než čtení dokumentace.

**Doklad:** `_raw/faze2a-prompty-alzask-H1-06.md` (P10, P11, P12) — „nevím" jako legitimní
vstup, ověření pochopení kvízem, učení domény mimo úkol · `_raw/faze2c` (P29)

**Role:** `[výklad]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** should

**Co ukážu na obrazovce:** krátkou ukázku, jak se z „nerozumím tomu" stane použitelná
odpověď — a jak se z toho dá udělat kvíz.

**Výhrada:** je to námět, který publikum bude považovat za samozřejmý, dokud neuvidí,
že to většina lidí nedělá.

### U-05 — Co commitnout, aby to fungovalo i kolegovi

**O čem to je.** Celá tahle série je o tom, jak si postavit prostředí. Ale prostředí
je k ničemu, když ho má jen jeden člověk. Otázka, kterou katalog musí odpovědět:
**které z těch souborů patří do Gitu a které jsou jen tvoje?**

Praktické rozdělení:

| Do Gitu | Zůstává lokální |
|---|---|
| `CLAUDE.md`, pravidla, skilly, commandy, hooky | osobní nastavení modelu a effortu |
| validátory a jejich konfigurace | přístupové údaje, cesty ke klíčům |
| zadání v souborech (jsou to dokumentace) | pracovní temp soubory |
| šablony a checklisty | paměti asistenta (jsou per-stroj) |

**Doklad:** **nulová evidence v mých datech** — je to mezera, kterou přiznávám. Všechna
data jsou moje sólo praxe a otázku „jak to předat kolegovi" jsem si nikdy nezapsal.
Přitom je to obsah téhle série.

**Role:** `[demo]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** R-02 · **Priorita:** must

**Co ukážu na obrazovce:** `git status` na cvičném repozitáři s postavenou výbavou —
co je verzované a co ne. Plus `.gitignore`.

**Výhrada:** **postavené na rozumu, ne na doložené praxi.** Musí to tak i zaznít — je to
návrh k diskusi s týmem, ne ověřený postup.

### U-06 — Vysvětlovací artefakt: osnovu nech schválit první

**O čem to je.** Když má z práce vzniknout dokument pro lidi (prezentace, onboarding,
vysvětlení), nejdřív nech vygenerovat **osnovu** a tu schval. Teprve pak obsah. Bez toho
dostaneš patnáct stran, ze kterých je použitelná třetina, a přepisuje se všechno.

**Doklad:** udělal jsem to třikrát (vysvětlující deck o Claude Code, návod pro analytiky,
onboarding), a **nikde jsem si to nezapsal jako postup** — přišlo mi to samozřejmé.
Zdroj: `_raw/faze0-existujici-material.md`, `_raw/faze2c` (P34).

**Role:** `[demo]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** should

**Co ukážu na obrazovce:** osnovu, kterou jsem schválil, a výsledný dokument. A vedle
toho jeden případ, kdy jsem osnovu přeskočil — a jak to skončilo.

**Výhrada:** je to podmnožina M-02 („nic neměň, napiš návrh"), aplikovaná na psaní
dokumentů. Dá se sloučit, když bude potřeba škrtat.

### U-07 — Co z toho po sedmi měsících doopravdy žije ⚑

**O čem to je.** Tenhle katalog je poctivý až do nepříjemnosti — devět námětů nese téma
„postavil jsem to a nepoužívám". Kdyby série skončila tím, publikum si odnese, že se
nemá do ničeho pouštět. To by byl špatný závěr, protože **není pravdivý.**

Co se po sedmi měsících **drží samo, bez připomínání:**

| Co žije | Doklad |
|---|---|
| Zadání do souboru (R-01) | vzor **v čase silní**, oba nejčistší výskyty jsou nejnovější |
| Číslovaný picklist (A-02) | 34 použití, nejpoužívanější vlastní příkaz |
| „Napiš do chatu, nic neměň" (M-02) | 14 výskytů rozložených přes celé období |
| Evidence dodavatelů (R-03) | postavená v srpnu a **používá se** — má spouštěč |
| Pojmenování session (O-04) | 35 použití |
| Grounding na `soubor:řádek` | průběžně přes celé období, ve všech měsících |

**Vzor je vidět na první pohled:** drží se to, co má **spouštěč nebo nulovou cenu
vyvolání**. Umírá to, co vyžaduje, aby si na to člověk vzpomněl.

**Doklad:** `DOKLADY.md` část 1 (počty použití příkazů napříč celým obdobím) ·
`_raw/faze2e-prompty-shared.md` (P10 — oba nejčistší výskyty jsou nejnovější) ·
`_raw/faze2c-prompty-alzask-08.md` (V01 — evidence dodavatelů v provozu tentýž den) ·
`_raw/faze5-redteam.md` (RT-42 — kontra-doklad sestavený nezávisle)

**Role:** `[výklad]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** must ⚑

**Co ukážu na obrazovce:** tu tabulku. A jednu větu jako závěr série: **postav to tak,
aby se to spouštělo samo, nebo aby to bylo zdarma. Cokoli mezi tím zemře.**

**Výhrada:** žádná. Tohle je ten námět, který má stát na konci — jinak série vyzní jako
seznam vlastních selhání.

---

## Okruh X — Antipatterny

Zůstaly čtyři, které nemají pozitivní dvojče. Ostatních devět z draftu je sloučených
do příslušných karet jako sekce „a co se stane, když to nedělám".

### X-01 — Vygeneroval jsem 22 souborů a pak je smazal ⚑

**O čem to je.** Nechal jsem z požadavků vygenerovat testovací případy pro služby, které
**nebyly implementované** — takže jejich pojmenování ani parametry nikdo neznal. Vzniklo
22 souborů, které popisovaly něco, co neexistuje.

Formulace z rozhodnutí, které to zrušilo: generované případy **„vytváří iluzi
otestovanosti"**. Prázdná složka říká „netestováno". Složka s 22 nesmyslnými soubory
říká „hotovo".

**Doklad:** rozhodnutí `ADR-ASK-PROC-009`, smazáno 22 souborů. Ověřitelné živě:
`find docs/fr/comp/wes -name "*.feature"` vrátí prázdno.

**Role:** `[příběh]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** must ⚑

**Co ukážu na obrazovce:** ten prázdný výsledek hledání a vedle něj rozhodnutí, které
to zrušilo. Pak vysvětlení, co zůstalo: testovací případy proti **stabilnímu kontraktu**
existují dál a fungují.

**Výhrada:** poučení není „negeneruj", ale **„generuj jen proti něčemu, co se nemění
pod rukama."** Iluze pokrytí je horší než jeho absence.

### X-02 — Postavil jsem pipeline a nikdy ji nespustil ⚑

**O čem to je.** Mám v projektu **pět revizních agentů** s rozdělenými rolemi, dokumentovanou
orchestrací v pěti fázích a příkazem, který to spustí. Návrh je dobrý: levný mechanický
filtr vpředu, drahé sémantické posouzení vzadu, automatická oprava jen tam, kde nejde
o spor autorit.

**Za celou historii to nebylo spuštěno ani jednou.** Ani příkaz, ani jména těch agentů
se v žádném z 2 671 promptů nevyskytují.

**Doklad:** `_raw/faze5-redteam.md` (RT-03) — nulový výskyt příkazu i jmen agentů
v celé historii

**Role:** `[příběh]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** must ⚑

**Co ukážu na obrazovce:** definice těch pěti agentů (je to hezky navržené) a hned potom
`grep` v historii — nula. Otázka pro publikum: **proč?**

Moje odpověď: protože to nemá spouštěč a protože ruční triáž (M-03) je práce, kterou
jsem místo toho dělal jednodušeji. Návrh byl lepší než potřeba.

**Výhrada:** to není argument proti subagentům (O-01 je `must` a doložený). Je to argument
proti **stavění pro budoucnost, kterou si vymyslíš.**

### X-03 — Tři situace, kdy jsem měl vypnout terminál

**O čem to je.** Katalog má dvanáct námětů typu „takhle to děláš špatně, dělej to jinak"
a **ani jeden** typu „tady to nezkoušej vůbec". Zkušené publikum tuhle otázku má,
a odpověď na ni je test důvěryhodnosti celé série.

Tři doložené situace z mých vlastních dat:

| Situace | Doklad | Co jsem měl udělat |
|---|---|---|
| Ladění algoritmu obrázky | 30 promptů, 8 kol | vzít papír a nakreslit stavový diagram |
| Mikro-iterace vzhledu | ~25 kol na jednom souboru | otevřít to v editoru a upravit ručně |
| Ladění nastavení bez základny | ~20 promptů, konec revertem | zapsat výchozí stav a měnit jednu věc |

Společný jmenovatel: **úloha, u které je zpětná vazba vizuální nebo subjektivní.**
Tam je ruční práce rychlejší než popisování.

**Doklad:** `_raw/faze2b-prompty-alzask-07.md` (X2, X3, X4) · a absence: slova
„raději ručně", „udělám to sám" mají v mých promptech **nula výskytů**

**Role:** `[výklad]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** ty tři časové osy. Žádná nová teorie, jen vlastní doložené
oblouky.

**Výhrada:** žádná. Je to nejžádanější slide zkušeného publika a mám ho čím podložit.

### X-04 — Dlouhý prompt v chatu se tiše ořízne ⚠

**O čem to je.** Dlouhý text vložený do promptu se může **tiše zkrátit** — bez chyby,
bez upozornění. Model pak odpovídá na neúplné zadání a ty nevíš, že ti něco chybí.

**Doklad:** ve zdrojích je doložitelně poškozený prompt o 3052 znacích, kde v půlce
zmizel text (*„Nic z paměti ani z obecné znalost**zení citací**"*). A 29 promptů je
přeposlání téhož zadání — protože „se nic nestalo".

**Role:** `[příběh]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** R-01 · **Priorita:** must

**Co ukážu na obrazovce:** **snímek toho poškozeného promptu z transkriptu.**

**Výhrada — a je důležitá:** **demo nezkoušet.** Není to reprodukovatelné na požádání,
a pokud se reprodukce nepovede, publikum uvidí, že se tvrzení nepotvrdilo — což ho
vyvrátí silněji, než by ho potvrdilo. Statický snímek je jediná bezpečná forma.
Lék je stejně R-01: zadání do souboru se neořízne.

---

# Návrh dílů série

**Podmínka, kterou návrh drží:** žádný díl nepřekračuje **90 minut** čistého obsahu.
Součty jsou spočítané skriptem (`_raw/prepocet-souctu.py`) přímo z minut v souhrnné
tabulce a z tabulek dílů, ne odhadem — draft měl tři ze šesti bloků sečtené špatně
a red-team to našel. Skript hlásí i nesoulad mezi tvrzením v textu a skutečností;
při přidání K-08 až K-10 (10. 9. 2026) tak vyšlo najevo, že údaj „`must` je 37 námětů"
byl zastaralý už předtím — správně jich bylo 39, po doplnění 41.

**Jak návrh čítat.** Katalog má 59 námětů a 738 minut, což je při kratších setkáních
deset až jedenáct dílů. To je hodně — ale katalog je **zásoba, ne program**. Pokud
série má být kratší, škrtej podle priority (`must` je 41 námětů) nebo vezmi jen díly
1, 3 a 6, které nesou tři hlavní myšlenky. Díl 0 a příloha `P` se nepřednáší.

## Díl 0 — Příprava (nepřednáší se)

**15 minut** · 1 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| N-06 | Cvičný repozitář — nulté dílo série | infra | 15 | must |

**Co si z toho odnesou:** Cvičný repozitář, na kterém se smí rozbíjet. Bez něj polovina dem nejde předvést.

## Díl 1 — Co se pod tím děje a co tě to stojí

**79 minut** · 6 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| F-01 | Claude si tě nepamatuje. Vede si o tobě složku. | výklad+demo | 15 | must |
| F-02 | Čeština není dražší, protože je delší | výklad | 12 | must |
| F-05 | Co tě stojí místo, o kterém nevíš | výklad+demo | 15 | must |
| N-05 | Co to stojí a jak to zjistíš | demo | 10 | should |
| F-03 | Tomu shrnutí můžeš říct, co má zachovat | výklad | 15 | must |
| F-04 | Padesát jedna ku jedné | příběh+demo | 12 | must |

**Co si z toho odnesou:** Model si nic nepamatuje, celá historie se posílá znovu, a proto dlouhá session zdražuje každý další prompt. Kompaktace session zachrání, ale zahodí 97 % — a dá se jí říct, co má nechat.

## Díl 2 — Než pustíš agenta na svá data

**51 minut** · 5 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| N-01 | Tři zákazy, které si nastav dřív než cokoli jiného | demo | 8 | must |
| N-02 | Tři úrovně zpět: `Esc Esc`, `/rewind`, `git diff` | demo | 8 | must |
| N-03 | Režim plánování: rozhodnutí odděleně od provedení | demo | 10 | must |
| M-02 | „Napiš to do chatu, nic neměň" | demo+cvičení | 10 | must |
| N-04 | Prompt je zápis, ne rozhovor | příběh+výklad | 15 | must |

**Co si z toho odnesou:** Tři zákazy, tři úrovně zpět, vestavěný režim plánování a jedna věta („nic neměň"). A jedno pravidlo, které se nedá vzít zpátky: prompt je zápis, ne rozhovor.

## Díl 3 — Zadání: dokument nese kontext, prompt nese rozhodnutí

**84 minut** · 6 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| K-01 | Dokument nese kontext, prompt nese rozhodnutí | výklad+demo | 20 | must |
| R-01 | Zadání do souboru, session ho jen provede | demo+cvičení | 15 | must |
| K-02 | Bezcílný rozkaz | příběh+cvičení | 12 | must |
| X-04 | Dlouhý prompt v chatu se tiše ořízne | příběh | 10 | must |
| K-03 | Co NEčíst — a proč u každé položky | výklad+cvičení | 12 | must |
| A-02 | Číslovaný picklist a odpověď čísly | demo+cvičení | 15 | must |

**Co si z toho odnesou:** Krátký prompt funguje jen nad postaveným kontextem. Dlouhé zadání patří do souboru — dá se revidovat, spustit znovu a je v Gitu.

## Díl 4 — Jak se ptát, aby odpověď byla k něčemu

**64 minut** · 6 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| A-04 | Straw-man: napiš hypotézu, ať ji jen opraví | výklad+demo | 12 | must |
| A-03 | Rozpočet na otázky a páka místo nejasnosti | výklad | 12 | must |
| A-05 | Sebekritika útokem na náklad na údržbu | výklad | 10 | must |
| K-04 | Ticho je nález, ne absence nálezu | výklad | 10 | must |
| A-09 | Vyjednej terminologii dřív, než začneš psát | výklad | 10 | should |
| U-04 | Nech si to vysvětlit laicky a pojmenuj, co nevíš | výklad | 10 | should |

**Co si z toho odnesou:** Hypotéza místo otázky, rozpočet na otázky, páka místo nejasnosti, a útok na náklad údržby — čtyři věty, které z modelu udělají oponenta místo pochlebovače.

## Díl 5 — Když to nejde: zmenši úlohu, ne prompt

**44 minut** · 4 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| A-06 | Redukce na minimální případ | příběh | 12 | must |
| A-07 | Specifikace invariantem místo symptomu | výklad | 12 | must |
| X-03 | Tři situace, kdy jsem měl vypnout terminál | výklad | 10 | must |
| O-05 | Izolace, které nerozumíš, tě stojí dopoledne | příběh | 10 | must |

**Co si z toho odnesou:** Po třetím nepovedeném kole nepiš čtvrtý prompt — zmenši úlohu a napiš invariant. A poznej tři situace, kdy je ruční práce rychlejší.

## Díl 6 — Proč to, co postavíš, přestaneš používat

**82 minut** · 6 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| M-01 | Brána, kterou nikdo nespouští, je taky jen prompt | výklad+demo | 18 | must |
| K-07 | Čtvrtina mého `CLAUDE.md`, kterou nikdo nespustil | příběh+demo | 15 | must |
| X-02 | Postavil jsem pipeline a nikdy ji nespustil | příběh | 12 | must |
| U-02 | Záchyt bez povyšovací brány je archiv | příběh | 15 | must |
| X-01 | Vygeneroval jsem 22 souborů a pak je smazal | příběh | 10 | must |
| M-07 | Práh, který realita překračuje — a prázdné pole | příběh+demo | 12 | should |

**Co si z toho odnesou:** Nejsilnější a nejnepříjemnější díl. Brána, kterou nikdo nespouští, je taky jen prompt — a mezi „postaveno" a „používáno" je propast, kterou je vidět na vlastních datech.

## Díl 7 — Revize a kvalita bez slepé automatiky

**61 minut** · 5 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| M-03 | Triáž dělá člověk. Dva ze tří nálezů jsou falešné. | výklad+příběh | 15 | must |
| M-05 | Vykazuj, kolik jsi toho NEzkontroloval | demo | 12 | must |
| M-06 | Deterministická kontrola vs. sémantická | výklad | 12 | must |
| M-04 | Slepý recenzent | výklad | 10 | should |
| A-08 | Publikum jako parametr — a pravidlo, které se poruší | výklad+demo | 12 | should |

**Co si z toho odnesou:** Dva ze tří nálezů jsou falešné, takže triáž nesmí dělat model. Vykazuj, kolik jsi NEzkontroloval. A nenech sémantickou kontrolu předstírat, že dělá práci deterministické.

## Díl 8 — Orchestrace: kam jde hluk

**47 minut** · 4 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| O-01 | Subagent není o rychlosti, ale o tom, kam jde hluk | výklad+demo | 15 | must |
| O-02 | Model podle povahy úlohy — a měřím to vůbec? | výklad+příběh | 12 | should |
| O-03 | Jak předat práci sobě zítra | demo | 12 | should |
| O-04 | Jedna session = jedno téma, pojmenované | demo | 8 | should |

**Co si z toho odnesou:** Subagent se nepoužívá pro rychlost, ale proto, že jeho hluk zůstane mimo tvůj kontext. Model se vybírá podle povahy úlohy — a stojí za to změřit, jestli to k něčemu bylo.

## Díl 9 — Vlastní výbava a jak ji předat dál

**68 minut** · 6 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| R-02 | Metodika bez spouštěče je jen text | příběh+demo | 12 | must |
| R-04 | Dvě vrstvy se rozjedou, když jednu nikdo nečte | výklad | 10 | should |
| R-03 | Uložený postup místo opakovaného promptu | demo | 12 | should |
| U-05 | Co commitnout, aby to fungovalo i kolegovi | demo | 12 | must |
| U-06 | Vysvětlovací artefakt: osnovu nech schválit první | demo | 10 | should |
| R-05 | Dva hooky, které mi běží, a šest, které neznám | demo | 12 | could |

**Co si z toho odnesou:** Metodika bez spouštěče je jen text. Skill a příkaz jsou to, co postup skutečně spustí — a Git je to, co ho dá kolegovi.

## Díl 10 — Velký audit a co z toho všeho žije

**62 minut** · 4 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| A-01 | Vrstvový audit dokumentace | výklad+cvičení | 25 | must |
| U-01 | Debuguj prompt, ne výstup | výklad+cvičení | 15 | must |
| U-03 | Nástroj cestoval mezi projekty a vyrostl | příběh | 12 | should |
| U-07 | Co z toho po sedmi měsících doopravdy žije | výklad | 10 | must |

**Co si z toho odnesou:** Vrstvový audit jako vrchol série: tytéž skutečnosti ve třech dokumentech, rozpory na hranicích vrstev. A závěr: drží se to, co má spouštěč nebo nulovou cenu vyvolání.

## Díl 11 — Kde to leží a odkud to víš

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

## Díl P — Příloha pro toho, kdo bude stavět nástroje

**37 minut** · 3 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| K-05 | Citace se ověřuje, nevěří | demo+infra | 15 | should |
| M-08 | Dva exit kódy = dva různé signály | demo+infra | 10 | could |
| K-06 | Hierarchie autority rozhoduje spor, ne datum | výklad | 12 | should |

**Co si z toho odnesou:** Nepatří do hlavní série. Kdo bude stavět validátory a kontrolu citací pro tým, najde tu zásady i cenu.

## Kontrola součtů

| Díl | Námětů | Minut | Do 90 min? |
|---|---|---|---|
| 0 | 1 | 15 | ano |
| 1 | 6 | 79 | ano |
| 2 | 5 | 51 | ano |
| 3 | 6 | 84 | ano |
| 4 | 6 | 64 | ano |
| 5 | 4 | 44 | ano |
| 6 | 6 | 82 | ano |
| 7 | 5 | 61 | ano |
| 8 | 4 | 47 | ano |
| 9 | 6 | 68 | ano |
| 10 | 4 | 62 | ano |
| 11 | 3 | 44 | ano |
| P | 3 | 37 | ano |

Přednášených dílů 1–11: **686 minut.** Plus příprava (díl 0) a příloha `P`.

Námětů v tabulce: 59 · zařazených do dílů: 59 · nezařazených: 0

---

## Tři možné střihy, kdyby série měla být kratší

| Varianta | Díly | Minut | Co publikum dostane |
|---|---|---|---|
| **Tři díly** | 1, 3, 6 | 245 | mechanika, zadávání, a proč postavené věci umírají |
| **Pět dílů** | 1, 2, 3, 6, 7 | 357 | plus bezpečné pouštění agenta a revizní disciplína |
| **Celá série** | 1–11 | 686 | vše včetně velkého auditu a předání kolegovi |

U každé varianty platí, že **díl 0 (cvičný repozitář) musí existovat předem.**
