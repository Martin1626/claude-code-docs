> **Součást katalogu námětů na workshop.**
> Hlavní katalog: [NAMETY.md](NAMETY.md) · výklad fundamentu: [FUNDAMENT.md](FUNDAMENT.md) ·
> doklady: [DOKLADY.md](DOKLADY.md).

# Vyřazeno — a proč se to nemá vracet

Tento dokument existuje proto, aby se vyřazené náměty nevracely. U každého je **doklad**,
ne dojem. Kde doklad znamená „přestal jsem to dělat", je uvedeno datum nebo rozhodnutí,
které to ukončilo.

Tři důvody vyřazení, každý jinak vážný:

| Důvod | Co to znamená | Smí se to vrátit? |
|---|---|---|
| **Neosvědčilo se** | Zkoušel jsem to a opustil, nebo to zrušilo rozhodnutí | Ne. Ale patří to do workshopu jako **antipattern** — kolega to zkusí taky. |
| **Osobní zvyk / `[infra]`** | Funguje to jen s infrastrukturou, kterou kolega nemá | Ne do hlavního programu. Případně do samostatného dílu „pro toho, kdo to bude stavět". |
| **Bez dokladu** | Znělo to dobře, ale nenašel jsem, čím to podložit | Ano, kdyby se doklad našel. |

---

## A. Neosvědčilo se — doloženo tím, že jsem to opustil

### A1 — Generování testovacích případů z funkčních požadavků pro neimplementované služby

**Co to bylo:** z každého FR se generoval `.feature` soubor s testovacími scénáři.

**Proč to padlo:** služby nebyly implementované, takže jejich pojmenování ani parametry
nebyly známé. Testy tedy popisovaly něco, co neexistovalo. Formulace z rozhodnutí:
generované TC „vytváří iluzi otestovanosti".

**Doklad:** `ADR-ASK-PROC-009`, smazáno **22 souborů** z `docs/fr/comp/wes/*/tc/`.
Ověřitelné živě: `find docs/fr/comp/wes -name "*.feature"` vrátí prázdno.

**Přenositelné poučení (a proto to v katalogu ZŮSTÁVÁ jako antipattern):**
generuj testovací artefakty jen proti **stabilnímu kontraktu**. API TC zůstala, protože
mají YAML kontrakt, který se nemění pod rukama. **Iluze pokrytí je horší než jeho absence** —
prázdná složka říká „netestováno", zatímco složka s 22 nesmyslnými soubory říká „hotovo".

### A2 — Znalostní smyčka jako *smyčka*

**Co to bylo:** zachytím chybu do inboxu → povýším na osobní pravidlo → konsoliduji
do sdílených pravidel. Tři stanice, jasná governance, CODEOWNERS.

**Proč to padlo:** **z asi 63 kandidátů v inboxu se povýšilo 5, a všech 5 v prvních šesti
dnech provozu.** Od 10. 7. do 25. 8. — tedy 46 dní a asi 58 kandidátů, mimochodem nejlépe
napsaných — **ani jeden.** Prostřední stanice (`rules-personal`) je v alzask od založení
prázdná, což potvrzuje git log.

**Doklad:** `_raw/faze3c-pravidla-inbox.md`.

**Přenositelné poučení (v katalogu ZŮSTÁVÁ jako příběh):** zachytávání je snadné, protože
má spouštěč — hook mi inbox nabídne na začátku každé session. Promoce spouštěč nemá, tak
se nedělá. **Smyčka, která sama nemá bránu na svůj vlastní krok, není smyčka, je to
archiv.** A je to zvlášť ironické u mechanismu, jehož jedno pravidlo přímo říká
„vynucuj bránou, neinstruuj v promptu".

### A3 — Vrstva „cross-project shared" pravidel

**Co to mělo být:** obě `CLAUDE.md` uvádějí v precedenci pravidel vrstvu
„cross-project shared" nad osobními pravidly.

**Proč to padlo:** **ta vrstva neexistuje.** `C:\Git\shared\` žádný adresář `rules/` nemá.
Přenos mezi projekty byl ve skutečnosti ruční kopie souborů — 10 ze 13 pravidel ve fhb
je kopie z alzask, čtyři soubory bit-shodné. A protože kopie není mechanismus,
**od 11. 7. se nesladilo nic.**

**Doklad:** `_raw/faze2d-prompty-fhb-myfaber.md`.

**Přenositelné poučení (ZŮSTÁVÁ jako antipattern):** dokumentovaná architektura není
architektura. Když `CLAUDE.md` popisuje vrstvu, která neexistuje, je to horší než mlčení —
čtu ji jako platnou a spoléhám na ni.

### A4 — Lokální orchestrátor a agenti pro tvorbu specifikací

**Co to bylo:** vlastní orchestrátor, agenti, nástroje a hook přímo v repozitáři alzask.

**Proč to padlo:** nahradil to plugin `spec-factory` (adopce 7. 7.). Lokální verze byla
smazána, protože dvě kopie téže mechaniky se rozejdou.

**Doklad:** `_raw/faze3b-pluginy.md`, `_raw/faze2b-prompty-alzask-07.md` (4denní oblouk
adopce, ~14 promptů čisté režie — restart, 6× `/resume`, 8× `/reload-plugins`).

**Přenositelné poučení (ZŮSTÁVÁ v námětu o migraci):** migrace nástroje **není hotová,
dokud nezmizel starý vstupní bod.** Starý `.claude/commands/spec.md` musel být řešen
dvakrát a ještě 11. 7. jsem volal `/spec-factory:spec /spec` zaráz — tedy nový i starý
příkaz v jednom promptu.

### A5 — Interaktivní tokenizér v existujícím decku jako demo

**Co to mělo být:** slide 02 v `claude-code-jak-funguje.html` má přepínač
Angličtina / Čeština a zobrazuje znaky, tokeny a poměr. Vypadá to jako hotové demo
tokenizace, které nemusím stavět.

**Proč to padlo:** **nepočítá tokeny.** Jsou to dvě zadrátovaná pole (`TOK_EN`, `TOK_CZ`
v JS na ř. 596–597) a „poměr" je jen `text.length / arr.length`. Nelze do něj nic napsat.
Deck to sám označuje za ilustrativní. Navíc tvrdí ≈ 3,5 znaku na token, kdežto
dokumentovaná hodnota je ≈ 4.

**Doklad:** `_raw/faze4b-verifikace-a-mezery.md`, `_raw/faze4a-fundament.md`.

**Důsledek:** demo tokenizace **hotové není**. Bez API klíče (na stroji není) musí námět
o tokenizaci skončit u měřených **znaků** a vysvětlení principu — nesmí vyslovovat počty
tokenů pro češtinu, protože je nemá čím podložit. Deck je jinak dobrý; potřebuje opravu
dvou míst.

### A6 — Práh 30 dní na rozpracovaný požadavek

**Co to bylo:** validátor hlásí požadavek, který je v draftu déle než 30 dní.

**Proč to padlo:** 23 požadavků je v draftu 55–201 dní. Práh tedy generuje 56 warningů,
mezi nimiž se ztratí 2 skutečné chyby. **Práh, který realita trvale překračuje, přestává
být signálem** — a lidé si zvyknou přehlížet i to, co pod ním leží.

**Doklad:** `_raw/faze3a-alzask-metodiky.md`. Ověřitelné živě: `validate.py` na `docs/fr/`.

**Přenositelné poučení (ZŮSTÁVÁ jako námět):** buď zvedni práh na hodnotu, kterou realita
respektuje, nebo změň úroveň závažnosti. Nechat bránu křičet do prázdna je nejhorší
ze tří možností.

---

## B. Můj osobní zvyk nebo infrastruktura, kterou kolega nemá

Tyto věci fungují — ale kolega si z nich neodnese nic než cíl. Do hlavního programu tedy
nepatří; patří do samostatného dílu pro toho, kdo bude stavět nástroje pro tým.

### B1 — Validátory (`validate.py`, `plc-lint.py`, `questions.py`, `audit.py`, `cite.py`)

Každý z nich je půl dne až tři dny práce a předpokládá konkrétní strukturu dokumentů.
**Doložená cena postavení jedné brány:** půl dne na zadání + jeden reálný běh jako
testovací stolice + dva až tři dny doladění (doloženo na `findings_rejected_ratio_max`
v `spec-factory` 1.8.0). A hlavně: brána nebyla hotová, když kód běžel, ale až když se
změřilo, kolik planých poplachů produkuje.

Do katalogu jde **zásada** („brána, ne prompt") a **cena**, ne návod na můj validátor.

### B2 — Tři vlastní pluginy

137 promptů jen na `spec-factory`, z toho asi 56 na vlastní inženýrství. Poměr práce:
návrh 1 : audit a opravy 2 : dokumentace pro lidi 1.

**Střízlivá odpověď na otázku, jestli se to vyplatilo:** ano, ale jen jako produkt pro tým.
Zlomový bod je **druhý uživatel**. Věta do workshopu, ne námět: *postav plugin, až budeš
mít druhého uživatele — do té doby stačí `CLAUDE.md` a jedno dobře napsané zadání
v souboru.*

### B3 — Ontologie prvků, registr dodavatelů, FR metodika, PLC linter

Všechno jsou to projektové artefakty pro konkrétní domain (sklad, PLC, dodavatelé HW).
Kolega z jiného projektu si odnese nejvýš strukturu, ne obsah. Zásady z nich (stabilní ID,
zdroj pravdy vs. derivát, evidovat co v odpovědi chybí) do katalogu patří —
implementace ne.

### B4 — Dávková organizace práce (D1…D13, „pokračuj dávkou B")

Funguje mi, ale je to můj způsob členění velké úlohy, ne přenositelná technika.
Kolega, který dostane radu „rozděl si to na dávky", nedostal žádnou informaci.

### B5 — Koordinace více session přes Session ID a práci v noci

Osobní provozní zvyk. Zajímavý je jen jeden vedlejší produkt — otázka, **jak poznáš,
že si dvě tvoje session sahají na týž soubor** (viz níže C3).

---

## C. Mezery, které si uvědomuji — chybí, ale nemám z čeho to postavit

Tohle nejsou vyřazené náměty, ale **poctivě přiznané mezery katalogu.** Publikum je bude
potřebovat a moje data na ně odpověď nedají.

### C1 — Cena a rozpočet

Mám ověřené ceny ($5 / $25 za milion tokenů u Opus 5, čtení z cache za desetinu, zápis
1,25× nebo 2×) a mám změřeno, že jsem zahodil 8,6 milionu tokenů kontextu. **Nemám ale
ani jedno číslo o tom, kolik mě sedm měsíců práce reálně stálo** — nesbíral jsem to.

Bez toho je jakýkoli námět o rozpočtu jen předčítání ceníku. Chybějící krok: spustit
`/cost` nebo `/usage` a pár týdnů to sledovat, než se o tom bude mluvit před lidmi.

### C2 — Práce ve dvojici a v týmu

Všechna data jsou moje sólo praxe. **Nemám doklad o tom, jak se s Claude Code pracuje
ve dvou nad jedním repozitářem** — jak se dělí kontext, kdo commituje, jak se řeší, že
každý má jiný `CLAUDE.md` v hlavě. Přitom je to první věc, na kterou tým narazí.

### C3 — Souběh vlastních session

Během tohoto běhu měl jeden člověk **čtyři paralelní session v jednom repozitáři** (tato,
oprava kotev ontologie, příprava e-mailu dodavateli, ladění output stylu). Nesrazily se —
ale jen proto, že každá psala jinam. Nikdo to nekoordinoval.

Otázka „jak poznáš, že si dvě tvoje session sahají na týž soubor" nemá v mých datech
odpověď. Vidím ji až v `git status`, tedy pozdě.

### C4 — Kdy Claude Code nepoužít

V 1508 promptech není ani jeden, ve kterém bych se rozhodl to nepoužít. To neznamená,
že taková situace neexistuje — znamená to, že jsem si ji nikdy nezapsal. Pro publikum,
které má nástroj používat s rozumem, je to podstatná mezera.

### C5 — Ostatní

Jednání se zákazníkem · odhady pracnosti · prezentace výsledků · práce s cizím kódem ·
code review · onboarding nového člena týmu · citlivá data a GDPR · licenční otázky.
Nic z toho v mých datech není v použitelné podobě.

---

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

---

## E. Doložení brány „nic nezapsáno do repozitářů"

Zadání této inventury mělo jedinou povolenou zápisovou zónu — `C:\tmp\workshop-namety\`.
Na konci běhu ale **`shared` má pět necommitnutých změn** a `alzask` je měl v průběhu
patnáct. Protože je to přesně ta situace, ve které se nemá věřit tvrzení bez dokladu,
je tady rozbor.

**Výsledek:** ani jednu z těch změn nezpůsobila tato session ani žádný z jejích třinácti
agentů.

**Doklad je časový a tematický.** Během tohoto běhu pracoval tentýž člověk v **pěti
paralelních session**:

| Session | Repozitář | Co v ní dělal |
|---|---|---|
| `87fe6ffd` | alzask | **tato inventura** |
| `d651a725` | alzask | automatizace opravy zmizelých kotev ontologie |
| `2ead8bd4` | alzask | příprava e-mailu dodavateli |
| `be023ba3` | alzask | ladění stylu odpovědí |
| `5edcb929` | **shared** | propsání té automatizace kotev do šablony pluginu |

Změny v `alzask` (kotvy, `RULE-ONT-003`, `ADR-ASK-PROC-020`, nový příkaz) odpovídají
promptu ze session `d651a725` z 8:44 a byly změněné mezi 8:58 a 9:14. Do konce běhu je
ta session commitla, takže `alzask` je teď čistý.

Změny v `shared` mají doslovnou předehru: v **9:31** padlo v session `d651a725`
*„Napiš prompt, který provede i v pluginu ontology-registry. Já jej pak spustím sám."*
a v **9:48** se v session `5edcb929` objevilo *„Přečti
`C:/tmp/prompt-ontology-registry-kotvy.md` a proveď to."* Soubory jsou změněné 9:51–9:56.

**Proč to nemohla být tato session:**

1. Žádný ze třinácti agentů nedostal v zadání ontologii kotev, `ADR-ASK-PROC-020`
   ani cokoli z `ontology-registry`.
2. Všech třináct mělo v zadání explicitní zákaz zápisu do repozitářů a všichni ho
   v souhrnu potvrdili. `fhb` a `myfaber` zůstaly čisté po celou dobu.
3. Poslední agent (adversariální průchod) dokončil dřív, než ty soubory vznikly.
4. Harness sám během běhu ohlásil přírůstek dostupného příkazu a změnu `CLAUDE.md` —
   tedy změny vzniklé **vně** této session.

**A je z toho námět.** Pět paralelních session v jednom pracovním prostoru se nesrazilo —
ale jen proto, že každá psala jinam. Nikdo to nekoordinoval. Otázka **„jak poznáš, že si
dvě tvoje session sahají na týž soubor?"** nemá v mých datech odpověď; vidím to teprve
v `git status`, tedy pozdě. Je to přiznaná mezera (sekce C3) a zároveň nejlepší doklad,
jak se to dá zaměnit: kdybych se spolehl jen na `git status` na konci, vyvodil bych
z něj, že jsem porušil zadání.
