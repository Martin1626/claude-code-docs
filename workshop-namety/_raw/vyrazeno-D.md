---

## D. Co vyřadil nebo přeformuloval red-team

Proti hotovému draftu (66 námětů) běžel jeden adversariální průchod se zadáním „rozbij to,
nevylepšuj". Vznesl **42 nálezů**, každý s dokladem a povinnou akcí. Plné znění je
v `_raw/faze5-redteam.md`. Tady je, co z toho vypadlo nebo se změnilo — aby se to nevracelo.

### D1 — Faktická chyba ve vlajkovém čísle (a proč to sem patří jako první)

Draft tvrdil **21 kompaktací** a **11,7 milionu zahozených tokenů**. Obojí bylo špatně:

| Co draft tvrdil | Skutečnost | Proč |
|---|---|---|
| 21 kompaktací | **19** | fork session kopíruje záznam, dvě události byly započtené dvakrát |
| 11 700 496 tokenů | **8 601 191** | u jednoho záznamu se do „kroku" dostal kumulativní součet |
| „97,3 % (583 578 → 12 127)" | 97,3 %, ale pár je **464 352 → 13 344** | draft slepil mediánový podíl s párem z jiné kompaktace |

**Kde byla chyba v mém skriptu:** krok jsem počítal jako rozdíl kumulativních součtů,
keyovaný podle ID session. Fork má jiné ID, takže první záznam ve forku dostal celý
kumulativ jako jeden krok. Správné je počítat `před − po`, což je přímé a na kumulativu
nezávislé.

**Co s tím:** čísla jsou opravená všude (`NAMETY.md`, `FUNDAMENT.md`, `DOKLADY.md`),
skript má opravu i vysvětlení v komentáři, a `DOKLADY.md` má nově sekci se třemi výhradami.
Mediánový podíl **97,3 % zůstal správný** — hlavní tvrzení se nezměnilo, jen jeho okolí.

**A proč to nechávám takhle popsané:** je to přesně ta rodina chyb, kterou mám ve vlastním
znalostním inboxu pojmenovanou jako **„měřím jiný jev, než jaký popisuji"**. Bez druhého
průchodu bych si toho nevšiml — a tvrdil bych na workshopu číslo o třetinu vyšší.

### D2 — Vyřazeno úplně

| Co | Proč |
|---|---|
| **„Nastavení nasazuj na diagnózu, ne na dojem"** | Podkladový agent to sám označil: *„osobní zvyk, specifické pro stroj uživatele, předvedatelnost slabá — nedoporučuju."* Draft to přesto povýšil. Zůstal jen tvar otázky („rozhodni mezi hypotézami A/B/C"), sloučený do A-04. |
| **`/insights` jako demo** | Nikdy jsem to nespustil, neznám dobu běhu, a promítlo by to na projektor jména zákazníka. Zůstává jako **domácí úkol** na konec dílu, ne jako demo. |
| **Slepé „pokračuj" jako námět** | Pět minut na to, že jednoslovný prompt je slabý. Sloučeno do K-02 (bezcílný rozkaz) — je to tentýž problém. |
| **Devět z dvanácti antipatternů jako samostatné položky** | Byly to negativní dvojčata pozitivních námětů, osm z nich mělo na svého dvojčete i závislost. Sloučeny do příslušných karet jako sekce „a co se stane, když to nedělám". Ušetřilo to devět slotů a asi 90 minut. |

### D3 — Přesunuto do přílohy „pro toho, kdo bude stavět"

Tři náměty jsou hodnotné, ale bez postavené infrastruktury si z nich kolega odnese jen cíl:
kontrola citací obsahem (`K-05`), dva exit kódy (`M-08`), hierarchie autority zdrojů
(`K-06`). Red-team to formuloval přesně: **blok „brány a kvalita" byl nejdražší a nejméně
odnesitelný blok programu.**

### D4 — Dema, která nejdou předvést (a proto se změnila role)

| Námět | Proč demo nejde | Nová forma |
|---|---|---|
| Tokenizace (F-02) | Na stroji **není API klíč** a veřejný tokenizér pro Claude neexistuje. Není čím tokeny spočítat. | `[výklad]` s měřenými znaky a principem |
| Kompaktace (F-03) | Trvá medián **181 s** a zabila by session, ve které přednáším | `[výklad]` + statická tabulka z transkriptů, zmrazená předem |
| Slepý recenzent (M-04) | Demo by bylo **tvrzení o tom, jak se model zachová** — když se zachová jinak, vyvrátí se to před publikem | `[výklad]` + statický exponát (klauzule v definici agenta) |
| Oříznutý prompt (X-04) | Není reprodukovatelné na požádání; nepovedená reprodukce tvrzení vyvrátí silněji, než by ho potvrdila | `[příběh]` se snímkem transkriptu |
| Evidence dodavatelů (R-03) | Promítlo by jména zákazníka i dodavatelů a otevřené závazky | demo nad **anonymizovanou kopií** v cvičném repozitáři |
| Hook na kompaktaci (R-05) | Nikdy jsem ho nespustil — nesmím doporučovat jako vyzkoušené | demo jen dvou hooků, které **skutečně běží** |
| Jedno ★★★ demo z podkladů | Ověřeno, že **dnes už selže** — repozitář se od té doby změnil | vyřazeno; obecné pravidlo: **každé demo projít týden před workshopem** |

### D5 — Opravená čísla u dalších dokladů

| Draft tvrdil | Skutečnost |
|---|---|
| „11 doložených dvojic" bezcílného rozkazu | **5 dvojic** (jedna ve třech kolech) + 5 bezcílných rozkazů bez opravy — obojí je vada, ale jiná |
| „kontext před prvním slovem ≈ 13 000 tokenů" | **minimálně** ~13 000, a je to odhad jen ze souborů, které umím přečíst |
| „137 promptů na plugin" | 151 bloků, z toho 93 věcných promptů a asi 56 na vlastní inženýrství |
| „oprava decku 3,5 → 4 znaky/token" | **Sama sporná.** Tokenizér od Opus 4.7 dává ~30 % víc tokenů, takže pro Opus 5 je to spíš ≈ 3,1 — a 3,5 je blíž než 4. Správná oprava je uvést rozsah s oběma citacemi. |
| tři ze šesti bloků měl draft **špatně sečtené** | součty se teď generují skriptem z tabulky, ne odhadem |

### D6 — Doplněno, protože to chybělo

Red-team našel jedenáct mezer. Devět z nich se stalo námětem, dvě zůstávají přiznané
v sekci C:

| Nové | Doklad, že to chybělo |
|---|---|
| **Režim plánování** (N-03) | Vestavěná funkce, `/plan` v 2 671 promptech **jednou** — a hned po něm jiný příkaz, tedy neúspěšný pokus. Sedm měsíců jsem si ji nahrazoval ručními náhradami. |
| **Tři úrovně zpět** (N-02) | `/rewind` **nulakrát**, checkpointy nikde. Draft měl `must` příběh o smazané práci a **žádný lék**. |
| **Prompt je zápis, ne rozhovor** (N-04) | „GDPR", „osobní údaj", „anonymizace" — **nula skutečných zásahů ve 286 290 znacích** promptů, a přitom je to korpus zákaznických dokumentů. Jediný doklad, který v datech je, jsou 4 zveřejněné přístupové tokeny. |
| **Kdy nástroj nepoužít** (X-03) | „raději ručně", „udělám to sám" — nula výskytů. Katalog měl dvanáct antipatternů typu „dělej to jinak" a ani jeden „tady to nezkoušej". |
| **Cvičný repozitář** (N-06) | 24 dem a 7 cvičení, a všechna by běžela v zákazníkově repozitáři, kde nesmím commitovat a kde leží patnáct rozpracovaných souborů. |
| **Co commitnout kolegovi** (U-05) | Nulová evidence v datech — a je to obsah celé série. |
| **Co to stojí** (N-05) | Ceny mám ověřené, vlastní spotřebu **ne**. `/usage` jako domácí úkol. |
| **Vysvětlovací artefakt** (U-06) | Udělal jsem to třikrát a nikde si to nezapsal jako postup. |
| **Co z toho doopravdy žije** (U-07) | Bez tohohle by série vyzněla jako seznam vlastních selhání. Šest věcí se drží samo — a všechny mají spouštěč nebo nulovou cenu vyvolání. |

### D7 — Nález, který katalog přepsal nejvíc

Třináct nálezů říká **jednu věc**: postavil jsem to, nenavěsil na rutinu, přestal používat.
Projektový asistent v `CLAUDE.md` (12,7 % souboru, ~1000 tokenů každý tah) — nespuštěn
za 2 678 promptů. Pětiagentní revizní pipeline — nikdy nespuštěná. Znalostní smyčka — pět
povýšení, všechna v prvních šesti dnech. Týdenní snapshoty — kadence vynechala tři týdny
v řadě. A vlastní pravidlo „vynucuj bránou" v projektu, kde **žádná brána neběží
automaticky** (`core.hooksPath` míří do prázdného adresáře, `.githooks/` nedotčené
7,2 měsíce).

Podle vlastní metody katalogu je trojí nezávislá konvergence nejsilnější signál. Tady je
třináctinásobná — takže to není nález, je to **nosné téma série** (díl 6) a devět námětů
je jím označených.

**Poučení, které z toho publikum odnese, a je to poučení pro každého:** brána má tři části
a lidé postaví jen první. Kontrola · **spouštěč** · reakce na výsledek. Bez druhé části
je to nástroj, na který si musíš vzpomenout — tedy zase jen prosba, akorát v jiném souboru.
