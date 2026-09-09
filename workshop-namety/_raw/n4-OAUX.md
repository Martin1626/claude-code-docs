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
