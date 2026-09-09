---

## Okruh M — Mechanika kvality

### M-01 — Brána, ne prompt

**O čem to je.** Nejsilnější konvergence celé inventury — našlo ji pět nezávislých analýz.
Zásada je jednoduchá: **kontrolu, kterou umí skript, nikdy nepiš jako věty do promptu.**

Důvod není lenost, ale to, že věta v promptu je **prosba**, kdežto skript je **fakt**.
Prosbu model splní většinou. Skript vrátí chybu vždy, i za půl roku, i když tu instrukci
mezitím vytlačila kompaktace.

**Doklad:** projektové pravidlo `RULE-GOV-002` · a hlavně důkaz z opačné strany:
pravidlo o pořadí záznamů v changelogu existuje 2,5 měsíce a **dodnes se mechanicky
porušuje**, protože ho nic nevynucuje. Zdroj: `_raw/faze3c-pravidla-inbox.md`.
Konvergence: `_raw/faze3a` (1), `_raw/faze3b` (1), `_raw/faze3c` (5),
`_raw/faze2b` (M7), `_raw/faze2a` (X4).

**Role:** `[výklad]` + `[demo]` · **Náročnost:** střední · **Odhad:** 18 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** vezmu soubor, udělám v něm chybu, kterou pravidlo v `CLAUDE.md`
zakazuje. Model ji někdy chytí, někdy ne. Pak spustím validátor — chytí ji vždy a vypíše
konkrétní řádek. Rozdíl je vidět okamžitě.

**Výhrada:** cena. Postavit bránu je půl dne na zadání plus dva až tři dny doladění —
a brána není hotová, když kód běží, ale až když se změří, kolik planých poplachů dělá.
Pro publikum je důležitější **zásada** než můj validátor.

### M-02 — „Napiš to do chatu, nic neměň"

**O čem to je.** Nejlepší poměr hodnoty a nákladu z celé inventury. Jedna věta, nulová
infrastruktura, funguje první den. Před zápisem do souborů si vyžádáš návrh **do chatu**
a zakážeš úpravu.

Je to zároveň nejlepší odpověď na strach z autonomie: nemusíš agentovi zakazovat práci
se soubory natrvalo, jen si oddělíš **návrh** od **provedení**.

**Doklad:** *„Navrhni ještě vhodnější pojmenování akce než je assignContainer. Napiš
varianty zde do chatu, nic neměň."* (2026-07-09 08:44) → o 25 minut později
*„OK, rozhodl jsem se pro containerPlaced. Oprav všude."* (09:09).
Celkem **14 výskytů**, z toho 5× s explicitním zákazem zápisu. Zdroj:
`_raw/faze2b-prompty-alzask-07.md` (M1, M2).

**Role:** `[demo]` + `[cvičení]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** tentýž úkol dvakrát. Bez té věty model začne editovat soubory.
S ní vypíše čtyři varianty s odůvodněním a čeká. Publikum vidí rozdíl v jednom kole —
a je to nejsnáze napodobitelná věc z celé série.

**Výhrada:** žádná.

### M-03 — Dva exit kódy = dva různé signály

**O čem to je.** Brána musí rozlišit „evidence je poškozená" (blokuj, exit 2) od „je tu
otevřená práce" (jen upozorni, exit 1). Bez toho nastane jedna ze dvou špatných věcí:
buď zablokuješ proces kvůli běžnému čekání, nebo si zvykneš ignorovat i skutečné chyby.

Zvláštní případ, na který se snadno zapomene: brána musí rozlišit **„čekáme na externí
vstup"** od chyby. Placeholder, který čeká na hodnotu od dodavatele, není vada —
je to stav.

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (3.5, 4.4b) — `questions.py --check` vrací
0 porušených invariantů a 102 nálezů; PLC linter má placeholder jako WARN, ne ERROR

**Role:** `[demo]` · **Náročnost:** střední · **Odhad:** 10 min ·
**Závislosti:** M-01 · **Priorita:** should

**Co ukážu na obrazovce:** spustím kontrolu na evidenci s otevřenými dotazy → exit 1
a výpis. Pak porušim invariant → exit 2 a jiná hláška. Publikum vidí, že to jsou dva
odlišné signály, ne dvě hlasitosti téhož.

**Výhrada:** `[infra]`. Zásada je přenositelná, konkrétní kódy jsou moje.

### M-04 — Vykazuj, kolik jsi toho NEzkontroloval

**O čem to je.** „Nic jsem nenašel" a „nic jsem neměřil" vypadají v reportu stejně.
Rozdíl udělá jediná věc: **součtová pojistka.** Kontrola musí vykázat nejen nálezy, ale
i to, kolik položek vůbec nekontrolovala a proč.

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (2.3, 2.4) — brána vykazuje součet
`2558 = 1278 kontrolováno + 0 bez kotvy + 661 mimo kontrolu + 619 opakovaných`.
Bez toho čísla by „1278 zkontrolováno" znělo jako úplnost.

**Role:** `[demo]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** M-01 · **Priorita:** must

**Co ukážu na obrazovce:** ten součet naživo. A pak stejnou úlohu bez pojistky — report
řekne „vše v pořádku", i když se polovina položek nekontrolovala.

**A meta-ukázka:** tenhle katalog má tu pojistku taky — `VYRAZENO.md` sekce C přiznává,
co jsem nenašel a co v datech není. Report bez sekce „co chybí" je nedokončený report.

**Výhrada:** je to nepohodlné. Pojistka vždycky ukáže, že jsi zkontroloval méně,
než si myslel.

### M-05 — Triáž dělá člověk. Dva ze tří nálezů jsou falešné.

**O čem to je.** Když necháš model najít chyby a hned je opravit, dostaneš dvě věci
zároveň: opravené skutečné chyby a **zanesené nové**, protože část nálezů byla falešná.
Triáž — rozhodnutí, který nález je skutečný — **nesmí být delegovaná.**

Číslo, které to dělá konkrétní: **počítej, že dva ze tří nálezů jsou falešné.**
Nezávislé měření precision LLM revizorů dává 21–31 %.

**Doklad:** vlastní diagnóza z 2026-08-19 16:20: *„při opravách často dochází k zanášení
nových chyb a zároveň spotřebovává mnoho tokenů"* → o tři hodiny později náhrada:
linter bez LLM → **slepí** recenzenti, každý s jednou optikou → triáž člověkem →
opravy po jedné větě, ne přepisem sekce. Zdroj: `_raw/faze2c-prompty-alzask-08.md`
(X01 → V03 → P19), `_raw/faze3c-pravidla-inbox.md` (7), `_raw/faze3b-pluginy.md` (13).

**Role:** `[výklad]` + `[příběh]` · **Náročnost:** střední · **Odhad:** 15 min ·
**Závislosti:** M-02 · **Priorita:** must

**Co ukážu na obrazovce:** report z revize a v něm si s publikem projdu tři nálezy —
u jednoho se ukáže, že je falešný. Pak ten protokol: co dělá stroj, co člověk.

**Výhrada:** vyžaduje to disciplínu, ne nástroj. A je to nepříjemné, protože „nechat to
opravit samo" je pohodlnější.

### M-06 — Slepý recenzent

**O čem to je.** Recenzentovi **neříkej, co a proč jsi změnil.** Když to ví, hledá potvrzení
tvého záměru. Když to neví, čte artefakt jako cizí text — a najde, co v něm skutečně je.

Praktická formulace ze zadání: *„artefakt jako cizí text, bez věty, co a proč jsme měnili"*.
A u verifikace opravy: *„ANI SLOVO o tom, že jde o opravenou verzi"*.

**Doklad:** `_raw/faze3b-pluginy.md` (2) — agent-soudce v pluginu nesmí vidět verdikty
ostatních ani metadata původu · `_raw/faze2c-prompty-alzask-08.md` (P18)

**Role:** `[demo]` · **Náročnost:** střední · **Odhad:** 10 min ·
**Závislosti:** M-05 · **Priorita:** should

**Co ukážu na obrazovce:** tentýž dokument dvěma recenzentům — jednomu s větou „opravil
jsem tam pojmenování, zkontroluj to", druhému bez ní. První potvrdí, druhý najde něco jiného.

**Výhrada:** platí pro kontrolu, ne pro práci. U vlastní editace kontext naopak potřebuješ.

### M-07 — Deterministická kontrola vs. sémantická

**O čem to je.** Rozděl kontroly na dvě hromádky: **ověřitelné bez porozumění** (čísla,
odkazy, formát, součty → skript) a **vyžadující porozumění** (souhlasí popis s diagramem?
→ model nebo člověk).

A pak to hlavní: **nikdy nenech druhou hromádku předstírat, že dělá práci první.**
Model, který „zkontroluje formát", ho zkontroluje většinou. Skript vždy.

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (4.2, 7.1) — PLC linter má pravidla A1–B14
deterministicky, sémantickou konzistenci explicitně nechává na LLM kontrole

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** M-01 · **Priorita:** must

**Co ukážu na obrazovce:** změním v tabulce typ hodnoty tak, aby porušil pravidlo →
linter to chytí okamžitě s konkrétním kódem chyby. Pak změním **význam** popisu tak,
aby nesouhlasil s diagramem → linter mlčí, protože na to nemá nástroj. To je ta hranice.

**Výhrada:** hranice není vždycky ostrá a někdy se posouvá. Ale mít ji napsanou je lepší
než ji nemít.

### M-08 — Práh, který realita trvale překračuje

**O čem to je.** Brána, která hlásí 56 varování, přestala být bránou. Mezi těmi varováními
se ztratí dvě skutečné chyby — a lidé si zvyknou přehlížet i je.

Tři možnosti, co s tím: zvednout práh na hodnotu, kterou realita respektuje; snížit
závažnost z chyby na informaci; nebo práh zrušit. **Nechat bránu křičet do prázdna je
nejhorší ze všech.**

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (1.3) — práh 30 dní na rozpracovaný požadavek,
23 požadavků je v draftu 55–201 dní, výsledek 56 varování a 2 skutečné chyby

**Role:** `[příběh]` + `[demo]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** M-03 · **Priorita:** should

**Co ukážu na obrazovce:** spustím validátor a nechám publikum **najít ty dvě chyby
v 56 varováních.** Nikdo je nenajde. To je celý námět.

**Výhrada:** žádná — je to obecná vlastnost varovných systémů, ne specialita Claude Code.

### M-09 — Opakovaná korekce se povyšuje na pravidlo

**O čem to je.** Když totéž opravuješ třikrát, přestal to být problém modelu a stal se
tvůj. Korekce v chatu je **jednorázová a zmizí s kompaktací**; pravidlo v souboru zůstane.

Poznávací znamení: napíšeš „Řešili jsme to už mnohokrát".

**Doklad:** 2026-06-19 10:50: *„není správně pořadí změn v changelogu. Jak je to možné?
Řešili jsme to už mnohokrát…"* — a o deset dní později tentýž formátovací požadavek
**dvakrát v odstupu dvou minut.** Zdroj: `_raw/faze2a-prompty-alzask-H1-06.md` (X4).
Protipól: `plc-lint` vznikl přesně z takové opakované korekce a stal se z něj skript (V2).

**Role:** `[příběh]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** M-01 · **Priorita:** must

**Co ukážu na obrazovce:** ty dva prompty dvě minuty po sobě. Pak validátor, který
z podobné korekce vznikl. Oblouk problém → improvizace → zafixování.

**Výhrada:** ne každá korekce si zaslouží pravidlo. Kritérium je **opakování**, ne
naštvání — jednorázová oprava do pravidel nepatří, jinak se z nich stane smetiště.

---

## Okruh O — Orchestrace

### O-01 — Subagent není o rychlosti, ale o tom, kam jde hluk

**O čem to je.** Nejčastější nedorozumění: subagent se používá, aby to bylo rychlejší.
Hlavní důvod je jiný — **jeho hluk zůstane mimo tvůj kontext.** Agent přečte 70 souborů,
udělá 40 volání nástrojů a vrátí ti dvacet řádků. Těch 70 souborů se do tvého okna
nikdy nedostane.

**Doklad:** tenhle katalog. Třináct agentů zpracovalo přes 500 KB podkladů; do hlavního
kontextu se z toho vrátily souhrny po dvaceti řádcích. Bez toho by hlavní session
kompaktovala třikrát — a viděli jste, co kompaktace udělá (97 %).

**Role:** `[výklad]` + `[demo]` · **Náročnost:** střední · **Odhad:** 15 min ·
**Závislosti:** F-05 · **Priorita:** must

**Co ukážu na obrazovce:** zadám agentovi „prohledej tenhle adresář a vrať mi tři nálezy",
pak ukážu `/context` — okno se prakticky nezvětšilo. Vedle toho totéž bez agenta: okno
naroste o stovky řádků výpisů.

**A pak čísla z této práce:** kolik tokenů spotřebovali agenti proti tomu, co přišlo
do hlavního okna.

**Výhrada:** agent nevidí tvou konverzaci. Co mu neřekneš v zadání, to neví — a proto
špatně zadaný agent vrátí sebevědomou hloupost. Platí u něj vše z okruhu K, jen dvakrát.

### O-02 — Volba modelu podle povahy podúlohy

**O čem to je.** Model se nevybírá podle důležitosti úkolu, ale podle **povahy práce**.
Mechanické čtení a výčty zvládne malý model; rozlišit „přenositelná praxe" od „jednorázovka"
je úsudek, na který malý model vrátí seznam všeho.

Gotcha, na kterou se dá naletět: **subagent nedědí tvou volbu modelu automaticky** —
musíš mu ji předat.

**Doklad:** tenhle katalog — fáze inventáře běžela na nejmenším modelu (mechanické výčty),
destilace praxe na nejsilnějším (úsudek o přenositelnosti), mapování metodik na středním.
Zdroj: `_raw/faze2b-prompty-alzask-07.md` (O3, N2), `_raw/faze2c` (P21).

**Role:** `[výklad]` + `[demo]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** O-01 · **Priorita:** should

**Co ukážu na obrazovce:** rozdělení modelů v této práci a proč. Pak ukázka, kde to
nedopadlo: mechanická fáze na nejmenším modelu **nahlásila nula hooků**, přitom jsou
čtyři — protože se podívala jen do jednoho souboru a nedomyslela, že hooky bývají
i v pluginech. To je přesně mez malého modelu.

**Výhrada:** je to úsudek, ne tabulka. A nejlevnější model dělá chyby, které musíš umět
poznat — jinak jsi ušetřil tokeny a koupil si nesprávná data.

### O-03 — Jak předat práci sobě zítra

**O čem to je.** Session skončí, kontext zmizí, a zítra začínáš znovu. Rozdíl mezi
`/resume` a `/clear` s předáním je v tom, co si nesete: `/resume` obnoví celou historii
(a s ní všechen hluk), předání přes soubor nese **jen závěry**.

Co `/resume` **neobnoví**: prompt cache (první request je pak nejdražší v session)
a běžící úlohy na pozadí — nikdy.

**Doklad:** `/resume` 33× v pracovních projektech proti `/clear` 1× · runbook jako
předávka mezi sessions doložen v `_raw/faze2b-prompty-alzask-07.md` (O1) ·
`_raw/faze2c` (P17) — handoff prompt s prioritami, doklady a varováním o tom, co ještě neplatí

**Role:** `[demo]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** F-04 · **Priorita:** should

**Co ukážu na obrazovce:** reálný handoff soubor z mé praxe — priority, doklady, a hlavně
sekce „co ještě neplatí". Pak `/clear` a start nové session jen s tím souborem.

**Výhrada:** napsat dobrý handoff trvá deset minut. Vyplatí se u úlohy na několik dní,
ne u půlhodinové práce.

### O-04 — Jedna session = jedno téma, pojmenované

**O čem to je.** Session, ve které řešíš tři různé věci, má trojnásobný kontext a nedá
se v ní zpětně nic najít. Pojmenovaná session je navíc podmínka toho, aby se dala později
analyzovat.

**Doklad:** `/rename` 35× v celé historii — je to pátý nejčastější příkaz vůbec.
Zdroj: `DOKLADY.md` část 1. A `_raw/faze2b-prompty-alzask-07.md` (O2).

**Role:** `[demo]` · **Náročnost:** nízká · **Odhad:** 8 min ·
**Závislosti:** — · **Priorita:** should

**Co ukážu na obrazovce:** `/resume` se seznamem pojmenovaných session proti seznamu
nepojmenovaných. V druhém nikdo nic nenajde.

**Výhrada:** je to zvyk, ne mechanika. Nic ho nevynucuje — což je mimochodem přesně
kandidát na hook (`UserPromptSubmit`), ale to jsem nezkoušel.

### O-05 — Vágní pokyn k izolaci smazal rozpracovanou práci

**O čem to je.** Imperativ bez jednoznačného cíle je nedeterministický. „Pracuj
v samostatné worktree!" neurčuje **které** — a agent použil existující, ve které byla
rozpracovaná práce.

**Doklad:** 2026-06-19 22:08: *„Měl sis založit nové worktree. Můžeš obnovit soubory,
které jsi mi vymazal?"* Náprava je v datech vidět o hodinu později — explicitní cesta
plus slovo „izolovaně". Zdroj: `_raw/faze2a-prompty-alzask-H1-06.md` (X1).

**Role:** `[příběh]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** ten prompt a jeho opravenou verzi. **Demo naživo jen
na testovacím repozitáři** — a i tam radši ne, stačí ukázat ty dva prompty.

**Výhrada:** je to nejtvrdší příběh v katalogu (ztráta dat) a musí se podat věcně,
ne jako strašení. Poučení: destruktivní operace potřebuje jednoznačný cíl, ne příslovce.

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
**jako produkt pěti iterací z jednovětného zadání**, ne najednou.
Zdroj: `_raw/faze2c-prompty-alzask-08.md` (P06).

**Role:** `[výklad]` + `[cvičení]` · **Náročnost:** vysoká · **Odhad:** 25 min ·
**Závislosti:** K-03, K-04 · **Priorita:** must

**Co ukážu na obrazovce:** tu kostru jako handout, pak jeden reálný nález, který audit
našel. A cvičení: publikum dostane dva svoje dokumenty a zkusí vyplnit body 1–4.

**Výhrada:** potřebuje to jedinou věc — **aby v projektu existovaly dva dokumenty
popisující totéž na jiné úrovni.** Žádný nástroj. Ale je to nejdelší námět v katalogu
a na krátké setkání se nevejde spolu s ničím jiným.

### A-02 — Číslovaný picklist a odpověď čísly

**O čem to je.** Druhá nejsilnější konvergence (čtyři nezávislé nálezy). Model vypíše
očíslovaný seznam — nálezů, otázek, variant, bodů z jednání — a ty odpovíš **čísly**.
Bez toho se konverzace rozpadne na dohadování, který bod se právě řeší.

**Doklad:** vlastní příkaz `/body-z-jednani` použit **34×** — je to můj nejpoužívanější
vlastní příkaz vůbec. Zdroj: `DOKLADY.md` část 1. Konvergence: `_raw/faze2a` (P9),
`_raw/faze2b` (M4, označeno jako vzor měsíce), `_raw/faze2c` (P02), `_raw/faze2e` (P6).

**Role:** `[demo]` + `[cvičení]` · **Náročnost:** nízká · **Odhad:** 15 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** vezmu přepis jednání, nechám z něj vygenerovat číslovaný
picklist a odpovím „3, 7, 9 ano; 4 ne; 5 později". Publikum vidí, jak se z hodinového
jednání stane seznam úkolů za dvě minuty.

**Výhrada:** funguje to jen s **uzavřenými** body. Číslovaný seznam otevřených otázek
typu „zvážit architekturu" se čísly odpovědět nedá.

### A-03 — Rozpočet na otázky a páka místo nejasnosti

**O čem to je.** Dvě věci, které dělají doptávání použitelným.

**Rozpočet:** „zeptej se na nejvýš pět věcí" donutí model vybírat. Bez rozpočtu dostaneš
dvacet otázek a odpovíš na tři.

**Páka místo nejasnosti:** neptej se „co je nejasné", ale **„co drží nejvíc navazujícího"**.
To je jiné řadicí kritérium — nejasností je vždycky víc než těch, na kterých něco závisí.

**Doklad:** `_raw/faze2c-prompty-alzask-08.md` (P04, P05) — rozpočet 5 uzavřených otázek
s nerovnoměrným rozdělením a „páka" jako explicitní řadicí kritérium ve vrstvovém auditu

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** A-01 · **Priorita:** must

**Co ukážu na obrazovce:** tentýž úkol s „zeptej se, co je nejasné" a s „vyber tři body
s nejvyšší pákou". První dá výčet, druhý prioritu.

**Výhrada:** žádná. Je to jedna věta v zadání.

### A-04 — Straw-man: napiš hypotézu, ať ji jen opraví

**O čem to je.** Otevřená otázka („jak to má fungovat?") dá esej. **Hypotéza k vyvrácení**
(„myslím, že to funguje takhle — kde se mýlím?") dá opravu. A opravu se dá snáz posoudit
než návrh.

Funguje to i směrem k lidem: dotaz dodavateli, který **obsahuje navrhovanou odpověď**,
se vrací rychleji a konkrétněji, protože protistrana jen potvrdí nebo škrtne.

**Doklad:** `_raw/faze2c-prompty-alzask-08.md` (P11, P23) — hypotéza k vyvrácení místo
otevřené otázky; straw-man dotaz na dodavatele s předepsanou odpovědí ·
`_raw/faze3b-pluginy.md` (11) — agent v pluginu píše vlastní hypotézu řešení **dřív**,
než se začne ptát

**Role:** `[výklad]` + `[demo]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** tentýž problém zadaný jako otázka a jako hypotéza.
Rozdíl v délce i použitelnosti odpovědi je okamžitě vidět.

**Výhrada:** hypotéza musí být formulovaná tak, aby se dala vyvrátit. „Myslím, že by to
mělo být dobré" není hypotéza.

### A-05 — Sebekritika útokem na náklad na údržbu

**O čem to je.** Nejcennější dosud nepojmenovaná praxe. Návrh se nekritizuje otázkou
„je to správně" (na tu model odpoví ano), ale **„kolik to bude stát na údržbě"** —
a to je otázka, kterou si model sám nikdy nepoloží.

Konkrétní formulace, které fungují: *„Mám obavy, že se tyto odkazy rychle rozjedou."*
*„Připadá mi to neefektivní, chybné a zbytečné. Je to tak?"*

**Doklad:** sedm výskytů v posledních pěti dnech měřeného období.
Zdroj: `_raw/faze2c-prompty-alzask-08.md` (P28).

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** návrh, který model označil za dobrý, a pak tutéž věc po otázce
na náklad údržby — model sám najde tři místa, která se rozjedou.

**Výhrada:** žádná, a je to nejlevnější způsob, jak z modelu dostat oponenturu.
Ale musí to zaznít **před** implementací, ne po ní.

### A-06 — Eviduj, co v odpovědi CHYBÍ

**O čem to je.** U odpovědi (od dodavatele, kolegy, zákazníka) se eviduje nejen co přišlo,
ale i **co konkrétně chybí**. Bez té věty se nedá zformulovat doptání — a mlčení k jednomu
bodu je jiná situace než „neodpověděl vůbec".

**Doklad:** reálný případ — dodavatel napsal „parametry máme v nastavení" a v přiloženém
screenshotu byly konkrétní hodnoty (3 pokusy / 4000 ms). **Devět dní se to vedlo jako
„chybí hodnoty"**, protože nikdo neotevřel přílohu.
Zdroj: `_raw/faze3a-alzask-metodiky.md` (3.3).

**Role:** `[demo]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** should

**Co ukážu na obrazovce:** záznam dotazu s polem „co chybí" a vedle toho ten screenshot.
Publikum vidí, že odpověď existovala devět dní, jen ne v textu e-mailu.

**Výhrada:** `[infra]` v implementaci (evidence je můj nástroj), ale **zásada je čistě
přenositelná** a poučení „příloha není dekorace" platí bez jakéhokoli nástroje.

### A-07 — Redukce na minimální případ

**O čem to je.** Po sérii selhání se nepokračuje dalším pokusem, ale **zmenšením úlohy
tak, aby se dala ověřit.** Klasické ladění, ale u práce s modelem se na to zapomíná,
protože „ještě jeden prompt" je vždycky po ruce.

Průlom v mém nejhorším případě přišel od člověka, ne od modelu:
*„Pojďme to řešit po částech… Pokud by měl dopravník jen segmenty Z1, Z2, Z3…"*

**Doklad:** 30 promptů na jeden algoritmus, 8 kol ladění screenshoty (13.–14. 7.).
Zdroj: `_raw/faze2b-prompty-alzask-07.md` (A1, označeno jako nejsilnější příběh měsíce).

**Role:** `[příběh]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** časovou osu těch 30 promptů a v ní bod, kde se to zlomilo.
Publikum uvidí, že to nebyl lepší prompt, ale menší úloha.

**Výhrada:** žádná, ale vyžaduje to sebeovládání. „Ještě jeden pokus" je vždycky
lákavější než „pojďme to zmenšit".

### A-08 — Specifikace invariantem místo symptomu

**O čem to je.** Rub předchozího námětu. Když popisuješ, co je špatně („nosič se zasekne
na křižovatce"), model opravuje symptom. Když popíšeš **invariant, který má platit vždy**
(„na segmentu smí být nejvýš jeden nosič, a to i během přesunu"), model má co ověřovat.

Invariant je zároveň testovatelný — symptom není.

**Doklad:** `_raw/faze2b-prompty-alzask-07.md` (A2) — v obou nejdelších selhavších
obloucích měsíce chyběl testovatelný invariant a zafixovaná základna

**Role:** `[výklad]` · **Náročnost:** vysoká · **Odhad:** 12 min ·
**Závislosti:** A-07 · **Priorita:** must

**Co ukážu na obrazovce:** tentýž problém popsaný jako symptom a jako invariant.
U druhého model sám navrhne, jak to ověřit.

**Výhrada:** formulovat invariant je analytická práce a chvíli to trvá. Není to
zkratka — je to investice, která se vrátí u třetího kola ladění.

### A-09 — Publikum dokumentu jako parametr zadání

**O čem to je.** Adresát dokumentu není kosmetika, je to **omezení, co v něm smí být.**
Specifikace pro externího dodavatele musí být sebe-nosná — nesmí odkazovat na interní
rozhodnutí, která adresát nemá. A pokud to nevynucuje brána, pomalu se to poruší.

**Doklad:** v produkční specifikaci pro externího dodavatele jsou **dva odkazy na interní
rozhodnutí, které prošly revizí.** Zdroj: `_raw/faze3a-alzask-metodiky.md` (4.3).

**Role:** `[výklad]` + `[demo]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** should

**Co ukážu na obrazovce:** `grep` na interní identifikátory v dokumentu, který je určený
externímu adresátovi. Dva zásahy. Pak stejná kontrola jako součást brány.

**Výhrada:** je to konkrétní příklad obecné zásady „napiš, pro koho to je". Publikum
si z toho odnese víc, když má vlastní dokument pro externího čtenáře.

### A-10 — Vyjednej terminologii dřív, než začneš psát

**O čem to je.** Když se pojmy dohodnou až v revizi, přepisuje se celý dokument.
A druhá, méně zjevná část: **nezaváděj nový pojem — zjisti, který se už v projektu
používá častěji.** Model rád vymyslí čistší termín, než jaký tým skutečně používá.

**Doklad:** `_raw/faze2c-prompty-alzask-08.md` (P12, P13) — vyjednání terminologie před
psaním; zjištění, který pojem už v projektu převažuje, místo zavedení nového ·
`_raw/faze2b` (K6) — sjednocení terminologie napříč dokumenty a zavedení do glosáře

**Role:** `[výklad]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** should

**Co ukážu na obrazovce:** `grep -c` na dva konkurenční termíny v repozitáři. Čísla
rozhodnou spor, který by jinak byl otázkou vkusu.

**Výhrada:** funguje to jen tam, kde už nějaká dokumentace je. Na zelené louce se
terminologie vyjednat nedá, tam se dá jen zapsat.
