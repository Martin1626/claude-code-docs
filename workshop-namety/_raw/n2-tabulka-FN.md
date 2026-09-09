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

**Celkem 56 námětů, 694 minut.**
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
| ≈ 4 znaky na token pro angličtinu | **dokumentováno** — doslovná citace z FAQ Anthropic |
| Tokenizér od Opus 4.7 dává na tomtéž textu ~30 % víc tokenů | **dokumentováno** — takže pro Opus 5 je to spíš ≈ 3,1 znaku/token |
| Poměr pro češtinu | **Anthropic nezveřejňuje** — žádné číslo neexistuje |
| Proč diakritika stojí víc | **odvozeno** z obecného principu byte-level BPE, nezávislý zdroj |
| `tiktoken` podhodnocuje o 15–20 %, „mnohem víc na neanglickém vstupu" | **dokumentováno** |

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
