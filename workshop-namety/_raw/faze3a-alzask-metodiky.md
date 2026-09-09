# FÁZE 3a — Analytické metodiky a mechaniky v repozitáři AlzaSk

> Podklad pro workshop pro kolegy analytiky softwaru (publikum: Claude Code už používají,
> metodiky nemají postavené). Cíl každé položky: **přenositelná zásada**, kterou si kolega
> odnese, i když konkrétní nástroj z tohoto repozitáře nikdy nepoužije.
>
> Zdroj: `C:\Git\alzask` (branch `dev/martint`), stav k 2026-08-26.
> Do repozitáře nebylo nic zapsáno — jen čtení.

Struktura: 11 zmapovaných oblastí, na konci **Kandidáti na náměty workshopu**
s okruhem z taxonomie `K` kontext a grounding · `R` rozšíření · `M` mechanika kvality ·
`A` analytické postupy · `X` antipatterny.

---

## 1. `docs\fr\` — metodika funkčních požadavků a testovacích scénářů

**Rozsah.** `CLAUDE.md` (69 ř., quick-reference), `README.md` (**1 201 ř.**, plná
metodika, 12 sekcí), `_templates/` (`FR-template.md` 45 ř., `TC-template.feature`),
`.fr-tools/` (`validate.py` 821 ř., `schema.yaml` 49 ř., `tc-schema.yaml` 80 ř.,
`config.yaml` 25 ř., `tc-list.py` 337 ř., `export_tc.py` 376 ř.).
Živý stav: **50 FR** souborů, **105 TC** `.feature` souborů.

### 1.1 Dvouúrovňová struktura FR + CLAUDE.md jako quick-reference

**Co to je.** Metodika má **dvě vrstvy**: `README.md` je plná metodika pro lidi (1 201
řádků — nikdo si to nepamatuje), `CLAUDE.md` je 69řádkový quick-reference s tím, co se
nesmí zvorat, a **načítá se automaticky do kontextu**. Kořenový `CLAUDE.md` na něj ukazuje,
jinak by ho model nenašel.

**Doklad — explicitní rozlišení.** Kořenový `CLAUDE.md`, tabulka „Dokumentační konvence":
README = „pro lidi, Claude čte na vyžádání, ❌ nenačítá se"; CLAUDE.md = „když v adresáři
**aktivně tvořím/edituji** a jsou tam pravidla, která musím pokaždé dodržet… **Musí na něj
ukazovat root `CLAUDE.md`**, jinak ho nenajdu"; INDEX = status-dashboard, ne pravidla.
`docs/fr/CLAUDE.md:3-4` to potvrzuje: „**Kompletní metodika:** `README.md`… Tento soubor je
stručný quick-reference."

**Přenositelná zásada.** Rozděl dokumentaci podle **toho, kdo ji čte a kdy**: plná metodika
pro člověka na vyžádání, krátký checklist toho, co se nesmí zvorat, do vždy načteného
kontextu. A **z krátkého ukazuj na dlouhé**, nikdy neduplikuj obsah.

**Předvedatelnost.** Otevřít `docs/fr/CLAUDE.md` (69 ř., vejde se na obrazovku — sekce
„Klíčová pravidla (checklist)" s 10 zaškrtávacími body) vedle `wc -l README.md` (1 201).
Kontrast je vidět okamžitě.

### 1.2 Struktura FR — ID, frontmatter, povinné sekce

**Co to je.** FR je markdown s YAML frontmatterem a pevně danými sekcemi. ID kóduje
zařazení: `FR-COMP-{WES|API|UI|ALG}-{OBLAST}-{SEQ}` nebo `FR-BP-{OBLAST}-{SEQ}`
(`schema.yaml:38-39` jako regexy). Adresářový strom **odráží PBS scope** — včetně složek
označených `⏳ plánováno`, které zatím neexistují (`README.md:39-104`).

**Co validátor vynucuje** (`schema.yaml`):
- **required_fields** (`:4-11`): `id`, `title`, `curator`, `pbs_ref`, `status`, `created`.
- **optional_fields** (`:13-22`): `depends_on`, `updated`, `components`, `related_adr`,
  `related_pbs`, `blocked_by`, `blocked_reason`, `tc_refs`.
- **enums.status** (`:24-31`): `draft | ready | in_progress | review | done | blocked`
  (životní cyklus `README.md:105-123`).
- **required_sections** (`:41-46`): `## Popis`, `## Požadavky`, `## Testovací scénáře`,
  `## Changelog`, `## Historie revizí`.
- **conditional_rules** (`:48-53`): **`status: blocked` ⟹ povinné `blocked_by`
  a `blocked_reason`**. To je elegantní — nelze „zablokovat" požadavek bez uvedení, čím
  a proč.
- **staleness** (`config.yaml:11-13`): `draft_max_days: 30`, `blocked_max_days: 14`.
- **ignore** (`config.yaml:15-22`): `_templates/*`, `.fr-tools/*`, `README.md`, `CLAUDE.md`,
  `ROADMAP-*.md`, `**/tc/*`.

**Přenositelná zásada.** **Podmíněná povinnost** je nejsilnější vlastnost schématu, kterou
většina lidí nepoužívá: „status = blocked ⟹ musíš uvést čím a proč" zabrání nejčastější
formě mrtvého záznamu — stavu bez příčiny.

**Předvedatelnost.** Ukázat `schema.yaml:48-53` (13 řádků YAML) a vedle reálný FR
s `status: draft` (`comp/wes/port/FR-COMP-WES-PORT-001_Rizeni_portu.md:1-16`).

### 1.3 Validátor — co skutečně hlásí (živý běh)

Skutečný běh při průzkumu (26.8.2026, `python docs/fr/.fr-tools/validate.py`):

```
ERRORS:
  - FR-BP-EXPED-001_Expedice_spolecne_pozadavky.md: Changelog (ř.592): poslední řádek
    má verzi 3.14, ale nejvyšší v tabulce je 6.5 — nový záznam patří na KONEC tabulky
    (RULE-CL-001)
  - tentýž soubor: poslední řádek má datum 2026-08-19, ale nejnovější v tabulce
    je 2026-08-24 — nový záznam patří na KONEC tabulky (RULE-CL-001)

Summary: 2 errors, 56 warnings        (exit 1; --strict také 1)
```

**To je nejlepší dostupné demo v celém repozitáři:** validátor našel **živou, skutečnou
chybu** — někdo vložil changelog záznam doprostřed tabulky. A kontroluje to **dvakrát
nezávisle** (podle verze i podle data), takže to nejde obejít jednou z obou cest.
Kód: `_extract_changelog_rows()` (`validate.py:24`).

**Ostatní kontroly** (`validate.py`): `check_dependencies` (`:228`),
`check_tc_refs` (`:239`), `check_staleness` (`:265`), `check_index_sync` (`:290`),
a pro TC `_validate_scenario_metadata` (`:568`), `check_fr_exists` (`:716`).

**TC validátor je čistý:** `python docs/fr/.fr-tools/validate.py --tc` →
`All TC files are valid! Summary: 0 errors, 0 warnings` napříč 105 soubory.

**ANTIPATTERN — 56 warningů jako tapeta.** Dvě skupiny:
1. **`Depends on non-existent FR`** — FR-BP-INBOUND-001..004 závisí na
   `FR-COMP-WES-CONTAINER-002`, `FR-COMP-WES-RCS-BE-001`, `FR-COMP-WES-MEASURE-001`,
   `FR-COMP-API-CONTAINER-002`, které **neexistují** (plánované oblasti ze stromu PBS).
2. **Staleness** — 23 FR je v `draft` **55 až 201 dní** při prahu 30 dní
   (`FR-COMP-WES-STATION-001` = 201 dní, `FR-COMP-WES-CONTAINER-001` = 200 dní).

Práh nastavený na hodnotu, kterou realita systematicky překračuje, přestane být signálem.
Porovnej s `docs/suppliers/`, kde je totéž řešené **oddělením exit 1 (nález, neblokuje)
od exit 2 (invariant, blokuje)** — tady mají errory i warningy stejný exit 1, takže
„2 errors" a „56 warnings" jsou pro CI k nerozeznání.
→ *Zásada:* každý práh, který realita trvale překračuje, se musí buď zvednout, nebo
překlasifikovat na jinou úroveň závažnosti. Warning, který svítí vždycky, nikdo nečte.

**Předvedatelnost.** Spustit `validate.py` naživo a nechat publikum najít v odpovědi ty dva
ERRORy mezi 56 warningy — to je celá pointa v jednom obrázku. Pak `--tc` → čistá nula.

### 1.4 Stabilní `@S` identifikátory — nejcennější TC konvence

**Co to je.** Každý testovací scénář má dvouciferné číslo (`@S07`), a kombinace
`{TC-ID}.S{NN}` (např. `TC-COMP-API-CONTAINER-001-01.S07`) je **permanentní a neměnná po
celou dobu života projektu** (`README.md:342-350`).

**Čtyři pravidla neměnnosti** (`README.md:352-359`):

| Pravidlo | Detail |
|---|---|
| Nepřečíslovávat | jednou přidělené `@S` číslo se NIKDY nemění |
| Nerecyklovat | smazané `@S` se NIKDY nepřidělí novému scénáři |
| **Mezery povolené** | smazaný S03 → další nový dostane **S16**, ne S03 |
| TC file ID neměnný | jakmile soubor existuje, jeho ID se nemění |

**Evidence smazání a přesunu** (`README.md:361-390`):
```gherkin
# Retired: S03 — auto-set compartmentTypeId přesunut do AddContainer (v2.0)
# Retired: S09 — duplikát S08 (v2.2)
# Moved:   S07 → TC-COMP-API-CONTAINER-001-02.S01 (v3.0)   ← v původním souboru
# Moved from: TC-COMP-API-CONTAINER-001-01.S07              ← v novém souboru
```
**Jeden řádek = jeden retired `@S`, výslovně „kvůli bezkonfliktním mergím"**
(`README.md:376`). To je detail, který prozrazuje zkušenost s reálnými merge konflikty.
Validátor to vynucuje: `scenario_ids_immutable` (`tc-schema.yaml:69`) — „pokud @S existoval
v předchozí verzi a chybí v aktuální, musí být v `# Retired:`".

**Proč to vzniklo — traceability chain** (`README.md:405-420`): `@S` číslo je stabilní část
názvu C# testovací metody, takže vzniká úplný řetěz:
```
C# test:    ContainerPutUpsertTests.S07_CreateOutboundWithSku_Returns201
TC scénář:  TC-COMP-API-CONTAINER-001-01.S07
FR:         FR-COMP-API-CONTAINER-001
```
Popis za `@S` v názvu metody se může měnit — **`@S` část ne**.

**Přenositelná zásada.** Identifikátor, který slouží k trasovatelnosti přes víc artefaktů
(požadavek → test → kód), musí být **neměnný a nikdy recyklovaný, i za cenu mezer v číslech**.
Mezera v číslování je levná; přečíslování zneplatní všechny odkazy naráz. A **smazání se
eviduje, nemaže** — jeden řádek na jeden záznam, aby se dva lidé nepřetloukli v mergi.

**Předvedatelnost.** V TC souboru přečíslovat jeden `@S` nebo smazat scénář bez záznamu
`# Retired:` → `validate.py --tc` to zahlásí (`scenario_ids_immutable`). Vedle toho ukázat
`# Retired:` řádky v reálném souboru a `tc-list.csv`, kde `TC-BP-DECANT-002-01` má S02–S09
**s chybějícím S07** — mezera je vidět v datech.

### 1.5 Per-scénář status a datum — granularita na správné úrovni

**Co to je.** Status („rozpracovaný / hotový") a datum poslední změny nejsou u **souboru**,
ale u **každého scénáře zvlášť**. Soubor se 12 scénáři, kde je 9 hotových a 3 rozpracované,
tak neleží celý jako „draft".

**Dva zápisy podle typu scénáře** (`README.md:288-312`):
- **Samostatný Scénář** — jako Gherkin tagy nad `Scénář:`:
  `@S07 @positive @contract @priority1 @scope_id:TC-API-002 @status:done @updated:2026-05-10`
- **Osnova scénáře** — jako **sloupce** `status` a `updated` v tabulce `Příklady:`
  (per řádek = per `@S`). README to zvlášť zdůrazňuje: „`@status:` a `@updated:` v Osnově
  **nepatří** mezi Gherkin tagy nad Osnovou" (`README.md:307-310`).

**Statusy redukované na dva** (`tc-schema.yaml:25-27`): `draft | done`. Vysvětlení
v README: `draft` = „kroky/data se mohou ještě měnit, není referenční", `done` = „hotový
a otestovaný — **kanonická podoba**".

**Pravidlo pro `@updated:`** (`README.md:284-286`): „Aktualizuj při každé věcné změně
scénáře (kroky Když/Pak, hodnoty v Příkladech, odpovědní pole). **Pouhý refactoring názvu
nebo formátování datum neaktualizuje.**"
→ To je přesně to rozlišení „posunulo se" vs. „změnilo se" jako u kotev citací (sekce 2.3).

**DEPRECATED s migrační cestou.** `# status:` a `# updated:` v hlavičce souboru jsou
deprecated. Ale **nezakázané naráz** — `tc-schema.yaml:11-15` má vlastní sekci
`deprecated_fields` s komentářem: „Pole, která BÝVALA v hlavičce, ale jsou nahrazena
per-scénář tagy. **Validator je toleruje (warning „deprecated"), aby migrace mohla probíhat
postupně.**" Stejně chybějící `@status:`/`@updated:` je **warning, ne error**
(`tc-schema.yaml:73-80`, `README.md:311-313`): „Při běžné práci na TC souboru postupně
doplňuj per-scénář hodnoty."

**Přenositelná zásada.** Když měníš konvenci na existující sadě dokumentů, **zaveď starý
tvar jako výslovně deprecated s warningem, ne jako chybu** — a migruj při běžné práci na
souboru, ne zvláštní kampaní. Zároveň: **atribut patří na tu úroveň granularity, na které
se skutečně mění** — status per soubor u souboru s 12 scénáři nese nulovou informaci.

**Předvedatelnost.** `tc-schema.yaml:11-15` (pět řádků, které řeší migraci) a vedle
`tc-list.csv`, kde je sloupec `Stav` a `Upraveno` **per scénář** s reálně různými daty
(2026-06-12 vs. 2026-08-18 v jednom TC souboru).

### 1.6 Doménový jazyk v krocích + registr kroků

**Co to je.** Krok testu popisuje **doménovou akci**, ne implementaci: `přidám nosič`,
ne `ContainerService.AddContainer`. Existující kroky jsou vedené v **registru** —
tabulce 34 doménových kroků s popisem operace (`README.md:632-666`).

**Tři pravidla** (`README.md:625-628`): žádné názvy service metod v krocích; **žádné
`<<internal>>` bloky** — WES TC neobsahují interní anotace; **nové kroky přidávej do
registru níže a dodrž styl**.

**Proč to vzniklo.** Implementační názvy se liší od specifikace a mění se refactoringem —
krok popsaný doménově refactoring přežije. Česká Gherkin notace je součástí téhož
(`README.md:126-139`): `Za předpokladu / Když / Pak`, `Osnova scénáře` / `Příklady`, nikoli
Given/When/Then.

**Přenositelná zásada.** Ve testech i specifikaci mluv **jazykem domény, ne jazykem
implementace** — a **veď uzavřený registr povolených formulací**. Bez registru vznikne pět
způsobů, jak napsat totéž (`přidám nosič` / `vytvořím nosič` / `založím nosič`), a nic se
už nedá vyhledat.

**Předvedatelnost.** Tabulka 34 kroků (`README.md:632-666`) — a hned pod ní `grep` v TC
souborech, že se skutečně používají právě tyto formulace.

### 1.7 Princip „žádná replikace schématu"

**Co to je.** TC nesmí kopírovat strukturu API schématu. Místo výčtu všech polí response
se uvádí **jen 5–9 klíčových polí**, která ověřují chování (`README.md:492-530`).
README má vedle sebe **SPRÁVNĚ / ŠPATNĚ** příklad — 6 klíčových polí vs. 11polní kopie
schématu.

**Odůvodnění.** `README.md:494`: „TC přináší **přidanou hodnotu**. API TC nereplikují
schéma (YAML), WES TC nereplikují kód služby. Obě testují kontrakty, business logiku
a chybové stavy." WMS vývojáři mají přístup k YAML — opisovat ho do TC je práce, která
vytváří druhou, dřív zastarávající kopii.

**Přenositelná zásada.** Nikdy neopisuj do svého dokumentu strukturu, kterou vlastní jiný
dokument — vznikne druhá pravda, která zastará dřív než originál. Uveď **jen ta pole, která
něco rozhodují**. (Přesně totéž pravidlo má registr ontologie jako „schéma se neopisuje" —
sekce 2.6a. Dva nezávisle vzniklé zápisy téhož principu.)

**Předvedatelnost.** `README.md:498-528` — dva bloky kódu vedle sebe, SPRÁVNĚ nad ŠPATNĚ.
Nejlepší didaktický útvar v celém repozitáři: kontrastní pár, ne pravidlo.

**Související konvence.** `Osnova scénáře` pro varianty + **jeden detailní příklad** pro
nejkomplexnější variantu (typicky `outbound`) — `README.md:531-556`. Struktura sekcí
v TC souboru: **CONTRACT → BEHAVIOR → BOUNDARY** (`README.md:468`).

### 1.8 Generované přehledy — `tc-list.csv`

`python docs/fr/.fr-tools/tc-list.py` generuje `tc-list.csv` (186 KB) — plochý seznam
**všech scénářů napříč 105 TC soubory**, jeden řádek = jeden `@S`:
`TC_ID;Nazev_TC;Nazev_scenare;Scope_ID;Klasifikace;Typ;Priorita;Kurator;Stav;Upraveno`.
`export_tc.py` dělá totéž do Excelu s navíc sloupci „Popis" a „Účel testu".
`CLAUDE.md:29`: „**Po změně TC vždy aktualizuj `tc-list.csv`.**"

**Přenositelná zásada.** Když je pravda rozprostřená ve stovce strukturovaných souborů,
vygeneruj z ní **jeden plochý seznam** — až tehdy jde odpovědět na otázky typu „kolik
scénářů je hotových a kdo je vlastní". Ale generuj ho skriptem, ne rukou.

**ANTIPATTERN — mrtvý odkaz v nástroji.** `export_tc.py:9` instruuje:
„Sloupec 'Účel testu' vyžaduje cache soubor generovaný přes:
`python docs/fr/.fr-tools/generate_descriptions.py`" — **tento skript v `.fr-tools/`
neexistuje** (ověřeno `ls`). Zůstala po něm jen `tc-descriptions-cache.json` (51 KB,
naposledy 4.5.2026). Nástroj tedy odkazuje na krok, který nikdo nemůže zopakovat.
→ *Zásada:* nástroj, který v návodu odkazuje na jiný nástroj, potřebuje kontrolu, že ten
druhý existuje — jinak vznikne cache, kterou nikdo neumí přegenerovat.

### 1.9 ANTIPATTERN — zrušené generování TC pro WES služby (ADR-ASK-PROC-009)

**Co se zrušilo.** `ADR-ASK-PROC-009` („WES služby — TC až po implementaci, ne z FR",
status **accepted**, 2026-03-17, autor Martin Tomis). Pro FR ve `docs/fr/comp/wes/`
se **TC v době psaní FR negenerují**; vzniknou až po implementaci ze skutečného kódu.
**Existujících 22 TC souborů bylo smazáno** (9 komponent). Netýká se API TC, kde je YAML
stabilní kontrakt.

**Proč — čtyři důvody z ADR** (sekce Důvody):
1. **Neznámá implementace** — v době psaní FR neexistuje kód, ze kterého by šly odvodit
   přesné parametry, návratové hodnoty a chybové stavy.
2. **Zbytečná práce** — TC z FR by se po implementaci kompletně přepsaly.
3. **Falešný pocit pokrytí** — „Existence TC, které neodpovídají skutečnému kódu, **vytváří
   iluzi otestovanosti**." ← nejcennější věta celého ADR.
4. **Jasný kontrakt u API** — API TC fungují, protože YAML je stabilní.

**Co konkrétně TC z FR produkovaly** (sekce Kontext): scénáře, které „odkazovaly na
neexistující nebo jinak pojmenované metody a parametry", „musely by se kompletně přepsat"
a „nepřinášely přidanou hodnotu oproti samotnému FR".

**Zvažované a zamítnuté alternativy** — ADR je uvádí obě: (1) generovat a přepsat po
implementaci → „dvojí práce, TC v mezičase neodpovídají realitě"; (2) skeleton TC bez
implementačních detailů → „příliš abstraktní, **totéž co FR samotný**".

**Přiznaná negativa a riziko.** „Mezi FR a implementací neexistuje formální testovací
artefakt pro WES služby"; „TC vzniknou s určitým zpožděním"; riziko „programátoři mohou
zapomenout vytvořit TC po implementaci — mitigace: tracking v task management systému".

**Ověřeno naživo:** `find comp/wes -name "*.feature"` → **0 souborů**. Rozhodnutí platí,
nevrátilo se to.

**Přenositelná zásada.** Artefakt, který vzniká z odhadu a musel by se po implementaci celý
přepsat, není „včasné pokrytí" — je to **iluze pokrytí, která je horší než jeho absence**.
Generuj testovací artefakty proti tomu, co je **stabilní kontrakt** (API schéma), ne proti
tomu, co se bude teprve navrhovat.

**Předvedatelnost.** ADR-ASK-PROC-009 s prázdným `find comp/wes -name "*.feature"` vedle
`find comp/api -name "*.feature"` (existují) — jedno rozhodnutí, dvě různé odpovědi podle
stability kontraktu.

### 1.10 Další drifty a nálezy v FR oblasti (antipatterny)

**a) Šablona se rozešla se schématem — a validátor ji nekontroluje.**
`_templates/FR-template.md` **neobsahuje `status:`** ve frontmatteru, přitom
`schema.yaml:4-11` ho má jako **required_field**. A **neobsahuje sekci
`## Historie revizí`** (ověřeno `grep -c` → 0), přitom `schema.yaml:41-46` ji má
v `required_sections`. FR vyplněný přesně podle šablony **by validaci neprošel**.
Nezachytí to nic, protože `_templates/*` je v `config.yaml:16` v ignore listu.
Reálné FR `status:` mají (`FR-COMP-WES-PORT-001…md:14`) — autoři si ho doplňují sami.
→ *Zásada:* **šablona je taky artefakt a musí projít stejnou bránou jako to, co z ní
vzniká.** Vyloučení šablony z validace je pohodlné a přesně proto se rozejde.
**Předvedatelnost:** `schema.yaml:4-11` vedle `head -8 _templates/FR-template.md` —
chybějící `status:` je vidět na první pohled.

**b) README popisuje metodiku pro WES TC, ale nezmiňuje, že se negenerují.**
README má rozsáhlou sekci „Doménové kroky WES TC" (`:619-666`, 34 kroků) a zmínky
o WES TC na `:245` a `:494`, ale **`grep "PROC-009"` v README nenajde nic**. Čtenář
metodiky se nikde nedozví, že WES TC se momentálně netvoří. Metodika sama je nadále
platná (TC vzniknou po implementaci) — chybí jen jedna věta s odkazem na ADR.
→ *Zásada:* když ADR zruší nebo pozastaví postup, musí se to objevit **v metodice, kterou
lidé čtou**, ne jen v ADR, které nikdo neotevře.

**c) Nezdokumentovaný adresář `docs/fr/proces/`.** Existuje (od 24.8.2026) a obsahuje
`Odpovedi-dodavatele-BlueSword-2026-08-21.md` a `Rizeni-kapacity-AGV-zony-.md` — **není
ani v README `:39-104`** (strom struktury zná jen `comp/` a `bp/`), **ani v kořenovém
`CLAUDE.md`**. Druhý soubor má navíc v názvu **koncovou pomlčku** (`-zony-.md`) — porušení
konvence pojmenování. Stejný typ driftu jako `T24_PREHLED-…` v bp-overview (sekce 5.2).

**d) Jednorázový plánovací artefakt v kořeni.** `PLAN-generovani-FR-dekantace.md`
(15 KB, 9.4.2026) leží v kořeni `docs/fr/` mezi metodikou. Není v ignore listu ani
v dokumentované struktuře — pravděpodobně dosloužil.

**e) Dva zrušené statusy TC.** `ready` a `review` byly z TC statusů zrušeny, zůstaly jen
`draft` a `done` (`tc-schema.yaml:25-27`). Méně stavů = méně sporů o to, co který znamená.
→ *Zásada:* číselník stavů zjednodušuj, dokud každá hodnota nemá jasný rozhodovací důsledek.
Stejný motiv jako u dodavatelů, kde volný text ve stavu (13 hodnot) rozpadl celou evidenci.

---

## 2. `docs\ontology\` — registr prvků systému

**Jednou větou:** registr faktů o prvcích systému s vynuceným zdrojem pravdy — **173 entit**
(physical 48 · logical 48 · enum 58 · actor 19), **349 vztahů**, **689 atributů**,
**96 rozporů** (`INDEX.md:7`), každý fakt s citací `soubor:řádek` do skutečného zdroje.

### 2.1 Proč registr vznikl

**Co to je.** Fakta o jednom prvku (třeba „port") byla roztroušená po datovém modelu, API
kontraktu, PLC specifikaci, ADR, FR a procesní analýze — a zdroje si často odporovaly.
Než někdo napsal „port má X vlastností", musel je dohledat na šesti místech a rozhodnout,
který zdroj má pravdu. Registr je jedno místo, kam se fakta sepíšou **s odkazem, odkud
pocházejí**, a s pravidlem, kdo vyhrává při sporu.

**Proč to vzniklo — nejsilnější doklad.** `ADR-ASK-PROC-020.md:33-40`: registr „je hotový
a čistý, ale **stojí vedle práce, ne v ní**: `grep -ri "ontolog"` nad `CLAUDE.md`
a `.claude/` vrací 0 výskytů… **měřením přitom vyšlo, že 79 % citací by se rozjelo za
30 dní**."
→ Pozor, to je poučení samo pro sebe: *hotový artefakt, na který nic neukazuje, je mrtvý
artefakt.* ADR-ASK-PROC-020 je právě ta práce, která ho zapojila do workflow.

Nutnost dokládá i `BUILD-LOG.md:39-64` — pro fyzické prvky měl registr do dávky D4
„u většiny HW prvků jen nepřímé doklady" a vrstvy zdrojů se navzájem přebíjejí podle
přesných pravidel. To se v hlavě neudrží.

**Přenositelná zásada.** Když fakta o jedné věci žijí na víc místech, která se mohou
rozejít, vytvoř JEDEN index s citacemi na originály a explicitním pravidlem „kdo vyhrává
při sporu" — neopakuj fakta, jen na ně ukazuj.

**Předvedatelnost.** `docs/ontology/INDEX.md`, řádek `port` — jedna řádka řekne, co to je,
kolik má vazeb, atributů, instancí, otevřených otázek a jestli má zdroj pravdy.

### 2.2 Zdroj pravdy vs. generované deriváty

**Co to je.** Ručně se edituje přesně JEDEN soubor — `ontology.yaml` (**1 637 936 bajtů**),
který se ale **nikdy nenačítá celý**. Vše ostatní se z něj generuje jedním příkazem.
Model nečte syrová data, čte generované, čitelné výřezy.

**Deriváty** (hlavička `INDEX.md:1-3`: `<!-- GENEROVANO — needituj. Zdroj:
docs/ontology/ontology.yaml, Regenerace: docs/ontology/.ontology-tools/build.cmd -->`):

| Výstup | Pro koho | K čemu | doklad |
|---|---|---|---|
| `INDEX.md` | model | rejstřík, vejde se celý do kontextu | `.ontology-tools/README.md:93` |
| `TERMS.tsv` | model | termín → entita → pole → zdroj; **jen grep** | tamtéž:94 |
| `RELATIONS.tsv` | model | vztahy obousměrně, bez citací | tamtéž:95 |
| `entities/<id>.md` | model | fakta o prvku | tamtéž:96 |
| `entities/<id>.notes.md` | model | próza, poznámky, otevřené otázky | tamtéž:97 |
| `SKILL.md` + zrcadlo do `.claude/skills/` | model | navigační vstupní bod | tamtéž:98, `UKOTVENI.md:121-124` |
| `ontology-view.html` | **člověk** | filtry, detail, ego-graf, klikatelné citace | tamtéž:99 |

**Ručně psané výjimky** (negenerují se): `conflicts.md`, `coverage.md`, `NAVRHY.md`,
`UKOTVENI.md`, `BUILD-LOG.md` — hlavička `BUILD-LOG.md:1-3`: „RUČNĚ PSANÝ dokument —
NEGENERUJE SE."

**Přenositelná zásada.** Jeden zdroj pravdy + generovaná navigační vrstva („čitelná
cache"). Derivát nikdy needituj — pozná se podle hlavičky `GENEROVANO — needituj`.
A **model čte deriváty, ne zdroj pravdy** (ten je moc velký) — jinak porušíš vlastní
pravidlo „nikdy nenačítat celý".

**Předvedatelnost (živě ověřeno).** `docs/ontology/.ontology-tools/build.cmd --check` →
`Registr: 173 entit, 349 vztahu, 689 atributu, 96 rozporu... hash 6cde6006166b` +
`AKTUALNI: vystupy odpovidaji registru (vc. zrcadla skillu).` — brána pozná, že derivát
zastaral proti zdroji (hash v hlavičce gate-souborů).

### 2.3 Kotvy citací — OK / POSUN / ZMIZELA (nejcennější mechanika celého repa)

**Co to je.** `soubor.yaml:14` je jen **adresa**, a adresy se rozjíždějí, protože lidé nad
citovaným souborem dál pracují a vkládají řádky nad ním. Nástroj proto vedle čísla řádku
ukládá **otisk obsahu** (sha1 okna textu kolem řádku). Text na místě → kotva sedí (`OK`).
Text se jen posunul → nástroj ho najde podle otisku a nahlásí novou adresu (`POSUN`),
rutinní oprava. **Text se skutečně změnil → kotva zmizí (`ZMIZELA`)** — a to nejde
opravit automaticky, protože samotné tvrzení v registru už může být neplatné.

**Proč to vzniklo — nejlepší citát pro workshop.** `.ontology-tools/README.md:147-151`:
„Za pár měsíců editací se rozjede většina citací — u živě rozpracovaných dokumentů i
o stovky řádků. Validátor to nepozná — soubor existuje, řádek existuje, tvar sedí.
**To je horší než chyba: tiše ukáže cizí text.**"

**Jak kotva funguje.** `.ontology-tools/README.md:153-169` — sha1 **adaptivního** okna
(±2 až ±6 řádků); rozšiřuje se, když kotva nese méně než 10 slov nebo se okno v souboru
opakuje. Změřeno 2026-08-24: samotný řádek = 86 % jednoznačných kotev, pevné okno ±2 =
95 %, **adaptivní okno = 99 % (1 190 z 1 192)**.

**Tři verdikty** (`.ontology-tools/README.md:182-190`, `UKOTVENI.md:87-92`):

| Verdikt | Exit | Význam | Reakce | Kdo |
|---|---|---|---|---|
| `OK` | 0 | kotva sedí | nic | — |
| `POSUN` | 0 | text žije, jen se posunul | dávkově `reanchor.py --apply` → `build.cmd`, **bez schvalování obsahu** | kurátor |
| `ZMIZELA` | 1 (blok) | citovaný text SE ZMĚNIL | člověk ověří tvrzení proti novému znění: oprava faktu, nebo jen nové ukotvení | **výhradně člověk** |

`RULE-ONT-003` to říká natvrdo: *„Kdo 'opraví' ZMIZELOU citaci přepsáním čísla řádku,
vyrobí horší stav než zastaralý: tvar sedí, obsah lže."*

**Přenositelná zásada.** **Cituj obsah, ne pozici.** Adresa (číslo řádku) je pomíjivá,
otisk obsahu přežije posun a **správně selže**, když se citovaný text změní. A rozliš
„posunulo se" (mechanická oprava) od „změnilo se" (rozhodnutí patří člověku) — nikdy je
neřeš stejným postupem.

**Předvedatelnost (živě ověřeno).**
```
python docs/ontology/.ontology-tools/cite.py "../myfaber/DbModels/Wes/Tables/Port.yaml:14"
→ OK   kotva sedí     + úryvek "- code: Code"

python docs/ontology/.ontology-tools/reanchor.py --check
→ OK 1278 (100 %) | posunutych: 0 | k overeni (GONE): 0 | bez kotvy: 0
→ součtová pojistka: "citaci v registru celkem: 2558 = 1278 (kontrolováno)
   + 0 (bez kotvy) + 661 (mimo kontrolu záměrně) + 619 (opakované odkazy)
   ... soucet SEDI na celek"
```
Ta **součtová pojistka** je samostatný námět: řeší mezeru z `UKOTVENI.md:39-41`, kde dřív
žádný nástroj nevykazoval, kolik citací kontrola vůbec **neviděla** — tedy aby
„nic jsem nenašel" nebylo k nerozeznání od „nic jsem neměřil".

### 2.4 Brány G1–G6 a tři vrstvy vynucení

**Nástroje** (`.ontology-tools/README.md:7-18`):

| Nástroj | Co dělá | Mění data? | Exit |
|---|---|---|---|
| `audit.py` | anomálie a porušené invarianty | ne | 0 čisto / 1 anomálie / 2 invariant |
| `fix.py` | narovná 3 typy nekonzistencí (O2, O3, O6) | ano, jen `--apply` | 2 při neshodě počtů (pojistka) |
| `build.py`/`build.cmd` | generátor navigační vrstvy | ne | `--check` 0/1 |
| `anchors.py` | jádro kotev (knihovna) | ne | — |
| `cite.py` | ověří JEDNU citaci | ne, **nikdy nezapisuje** | 1 při GONE/NOFILE |
| `reanchor.py` | vyrobí/srovná kotvy dávkově | ano, jen `--apply` | `--check` = 1 **jen** při ZMIZELA |
| `session-check.py` | SessionStart kontrola | ne | **vždy 0** (warning-only) |

**Brány G1–G6** z `ADR-ASK-PROC-020` (`UKOTVENI.md:63-70`):

| # | Měří | Práh |
|---|---|---|
| G1 | deriváty odpovídají zdroji | binární (hash) |
| G2 | invarianty a anomálie registru | exit ≠ 0 = blok |
| G3 | zmizelé kotvy citací | GONE = 0 pevně; POSUN neblokuje |
| G4 | **úplnost kontroly kotev** (aby „nic jsem nenašel" ≠ „nic jsem neměřil") | N = 0 |
| G5 | zrcadlo skillu odpovídá registru | binární |
| G6 | drift kopie nástrojů proti master šabloně pluginu | informativní |

**Tři vrstvy vynucení** (`UKOTVENI.md:94-98`): (1) `review.linters` ve `spec-config.yaml` —
automaticky ve fázi 2 `/review-spec`, nenulový exit = blok; (2) ruční postup po dávce
(`README.md:198-206`): `audit.py --quiet` → `fix.py` náhled → `--apply` → `git diff` →
`reanchor.py --check` → `build.cmd`; (3) **SessionStart hook** — jediný moment, který
zachytí zastarání i **mimo** formální review běhy.

**Přenositelná zásada.** Vynucuj **bránou** (deterministický skript s exit kódem napojený
na review/CI/start session), ne větou v promptu. V projektu je to pojmenované vlastní
pravidlo `RULE-GOV-002` „brána, ne prompt", citované přímo v ADR-ASK-PROC-020.

**Předvedatelnost (živě).** `python docs/ontology/.ontology-tools/audit.py --quiet` →
15 řádků kontrol `O2b`…`Z2`, každá `[OK]` nebo `[ i]`, na konci
`Invarianty: 0 porušených | Anomálie k opravě: 0`.

### 2.5 Guard — registr smí měnit jen člověk

`CLAUDE.md`: „Zápis do `docs/ontology/` je pro automatické agenty blokován guardem —
registr mění jen hlavní session / člověk." Automatický agent nový prvek jen **nahlásí jako
nález**, nezapisuje (`RULE-ONT-001`). Detail mechaniky viz sekce 10.2.

### 2.6 Antipatterny z `BUILD-LOG.md` a `conflicts.md` — nejcennější část

Skutečné chyby myšlení, kterými si tvůrci registru prošli.

**a) Schéma se neopisuje.** `BUILD-LOG.md:152-155`: „SCHÉMA SE NEOPISUJE (antipattern
zadání §9). Registr neuvádí pole ani typy objektových schémat — u `oneOf` variant zapisuje
POUZE diskriminátor, výčet variant, ROZLIŠOVACÍ PRAVIDLO a citaci."
→ *Zásada:* registr fakt **indexuje, nekopíruje** strukturu zdroje — jinak vznikne druhá,
dřív zastarávající kopie téže informace.

**b) „Novější" ≠ „autoritativnější".** `conflicts.md:9-15` definuje 7 vrstev autority
(1a data nasazení → 1b popis modelu → 2 API kontrakt → 3 accepted ADR → 4 FR →
5 PLC/fyzické prvky → 6 procesní analýza/přepisy jednání). `BUILD-LOG.md:104-110`:
argument „starší zdroj má míň váhy" se ukázal **mylný** — mezaninová PLC spec byla NOVĚJŠÍ
než data nasazení, a přesto prohrála, protože přednost vrstvy 1a stojí na pravidle „data
nasazení jsou stav systému, ne popis stavu" — ne na datu dokumentu.

**c) Draft ADR ≠ draft FR.** `BUILD-LOG.md:377-381`: „U FR NEPLATÍ ANALOGIE S ADR. Draft
ADR není normativní, protože rozhodnutí bez schválení nikoho nezavazuje. **Draft FR se ale
IMPLEMENTUJE**: 33 ze 47 je `draft`, včetně `FR-COMP-WES-PORT-001`, který je kanonickým
vlastníkem modelu portu."
→ *Zásada:* stejné slovo statusu má v různých typech dokumentů opačný praktický důsledek —
ověř, nepředpokládej podle názvu pole.

**d) „Accepted stojí na draftu."** `BUILD-LOG.md:256-260`: tři accepted ADR se opírají
o neaccepted premisy (`ADR-ASK-PROC-007` accepted stojí na `ADR-ASK-INT-003` proposed).
Na platformové úrovni horší — `BUILD-LOG.md:279-289`: **ze 25 globálních ADR je 0 accepted**
(24 draft, 1 superseded) — „schvalovací kolečko tedy neproběhlo ani jednou"; u 17 z 25
chybí i kurátor.
→ *Zásada:* projdi celý řetěz odůvodnění, nezastavuj se na první nalezené ADR.

**e) Jednostranný override je neúčinný.** `BUILD-LOG.md:253-255` (C043):
`ADR-ASK-OVR-001` (draft) přebíjí `ADR-MF-PROC-003`, ale ten nemá vyplněný zpětný odkaz —
„oba dokumenty jsou navíc draft, takže žádný normativní override neexistuje."
→ *Zásada:* override je vztah, který musí být doložený z OBOU stran.

**f) TODO není rozpor.** `BUILD-LOG.md:112-113`: „TODO A 'K OVĚŘENÍ' V PLC SPEC NEJSOU
ROZPORY. Jsou to legitimní otevřené body dokumentu psaného pro dodavatele a jdou do
`open_questions`, nikdy do `conflicts.md`."
→ *Zásada:* rozliš „zdroj tvrdí dvě různé věci" (rozpor) od „zdroj přiznává nejistotu"
(otevřená otázka).

**g) Endpoint není prvek, algoritmus není prvek.** `BUILD-LOG.md:146-150,390-392`: API
cesty ani operace nezakládají entity (jsou to vztahy `produces`/`consumes`); 8
algoritmických oblastí (`comp/alg/*`) nemá vlastní entity — znalost patří k prvkům,
o kterých algoritmus rozhoduje.
→ *Zásada:* než založíš entitu, zeptej se „je to VĚC, nebo způsob práce s věcí?"

**h) Rozpor uvnitř téže vrstvy je nejhorší druh.** `BUILD-LOG.md:410-415`: „Precedence pro
to pravidlo nedává… Je to riziko největší, protože obě strany jsou stejně závazné zadání
a **implementátor si vybere tu, kterou přečte první**."

**i) `fix.py` — tři nálezy, které NEJSOU chyby.** `.ontology-tools/README.md:68-77`: citace
na celý adresář (počet souborů), vícenásobná citace v jednom poli, negenerovaný
`conflicts.md`.
→ *Zásada:* automatická kontrola musí rozlišit „vypadá to jako chyba" od „je to záměrný
doložený tvar" — jinak nástroj kazí legitimní data.

**Souhrnná zásada sekce.** Písemný žurnál rozhodnutí („co jsme zkusili a co se ukázalo
mylné") je sám artefakt k udržování — antipatterny z dávky D4 by se jinak v D9 zopakovaly.

---

## 3. `docs\suppliers\` — evidence dotazů a odpovědí s dodavateli

Dodavatelé HW: **BullsEye** (4D shuttle, dopravníky), **BlueSword** (AGV/RCS).

**Rozsah zdrojů:** `README.md` (212 ř., plná metodika), `CLAUDE.md` (78 ř., quick-reference
pro Claude), `POSTUP-pro-analytiky.md` (224 ř., laický návod pro lidi),
`.tools\questions.py` (619 ř., brány Q1–Q6 + generátor), `questions.yaml` (zdroj pravdy,
**164 dotazů** dle live `--stats` k 26.8.2026; README zmiňuje 65 — číslo v README je
z dřívějšího stavu).

### 3.1 Jeden záznam = jedna otázka, ne jeden e-mail

**Co to je.** Záznam v registru není celý e-mail ani celé vlákno, ale **jedna konkrétní
otázka**, tak jak byla dodavateli poslána. Nese doslovné znění otázky (`question`),
doslovné znění odpovědi (`answer`), kdy a kterým mailem šla/přišla, a pokud odpověď
nestačí, větu, co konkrétně chybí (`still_missing`).

**Proč to vzniklo.** `README.md:3-4` — „Jedno místo, kde je vidět, na co u dodavatele
čekáme a co už víme. **Nahrazuje rekapitulaci v Excelu, ze které se stav dal vyčíst jen
ručním čtením.**"

**Schéma jednoho záznamu:** `README.md:57-74` — `id`, `thread`, `supplier`, `ref_in_mail`,
`question`, `answer`, `sent_on`/`answered_on`/`mail`/`answer_mail`, `reminders`,
`follows_up_on`, `status`, `still_missing`, `promised`, `evidence`, `about`, `landed_in`,
`owner`.

**Přenositelná zásada.** Evidenci komunikace veď na úrovni **jednotlivé otázky** s trvalým
ID a doslovným textem obou stran — ne na úrovni e-mailu nebo vlákna. Jedno vlákno
obvykle obsahuje víc otázek s různým stavem.

**Předvedatelnost.** Otevřít `questions.yaml:2312-2337` (záznam `ISS-004`) a ukázat vedle
sebe `question` / `answer` / `still_missing` / `evidence` — na jedné obrazovce je vidět
celý životní cyklus jednoho bodu.

### 3.2 ID se nikdy nepřečísluje a nerecykluje

**Co to je.** ID má tvar `<THREAD>-NNN`, kde `THREAD` je zkratka e-mailového vlákna:
`PRE`, `MEZ`, `PORT`, `ISS`, `AGV`, `SEQ`, `MTG`, `SAFE`, `ESTOP`, `DWS`, `SIM`, `SHIP`
(`questions.yaml:16-30`). Číslo je stabilní; uvolněné číslo (po zaniklém dotazu) se
nikdy nedává dalšímu dotazu.

**Proč to vzniklo.** `README.md:59` — „`id` … stabilní, nepřečísluje se, uvolněné se
nerecykluje." Důvod `README.md:20-22`: „Nic z toho se nepřejmenovává — **na ID odkazuje
i dodavatel ve svých odpovědích** (list Overview: *'Please refer to the question IDs in
replies, so both sides can track each item'*)." Totéž `CLAUDE.md:19-20`.

**Doptávání = nová otázka, ne přepis staré.** `README.md:78-84` — follow-up dostává nové
ID s vazbou `follows_up_on` (`PRE-001 → PRE-005, PRE-006, PRE-007`). Číslování dodavatele
se mezi koly resetuje a mění schéma (`Q1–Q12` v jednom kole, `1.–7.` v jiném, `1.1/2.2`
ve třetím), proto žije **jen jako text** v `ref_in_mail` a nikdy nevstupuje do ID —
viz `questions.yaml:1616` u `PORT-005`: `ref_in_mail: "13 Aug - to 1.1"`.

**Přenositelná zásada.** ID, na které odkazuje i druhá strana, musí být neměnné a nikdy
recyklovatelné — jinak ztrácíš schopnost odkázat na konkrétní bod napříč měsíci
komunikace. Cizí číslování si nikdy neber za vlastní identitu; ulož ho jako popisek.

**Předvedatelnost.** `grep "follows_up_on" docs/suppliers/questions.yaml` — ukázat řetěz
doptávání a vedle něj `ref_in_mail` s cizím číslováním.

### 3.3 `still_missing` — eviduje se, co v odpovědi CHYBÍ

**Co to je.** Pole `still_missing` je věta popisující, co konkrétně v odpovědi chybí, aby
šla použít k rozhodnutí. Je **povinné**, kdykoli odpověď přišla, ale nestačí
(`Partially`, `Declined`), nebo když dodavatel bod mlčky přeskočil.

**Jak se to vynucuje mechanicky.** Brána Q6, `questions.py:144-151`:
`needs_gap = status in ('Partially', 'Declined') or id in silent` — pokud `needs_gap`
a pole chybí, hlásí `!!` a **blokuje** (invariant, exit 2). Není to instrukce v promptu,
je to brána.

**Proč to vzniklo.** `README.md:96-97` — „Nuance patří do `still_missing`, ne do stavu —
**volný text ve stavu byl jedna z příčin, proč se Excel rozpadl (13 různých hodnot)**."
Tedy: stav je uzavřený pětihodnotový číselník, veškerou nuanci nese `still_missing`.
`POSTUP-pro-analytiky.md:144-145` — „Co když je odpověď 'ano, ale…': může být ve stavu
`Partially`… Pak je u ní věta, co konkrétně chybí. **To je často důležitější než sama
odpověď.**" `CLAUDE.md` (odpovídající pasáž): „Bez věty 'co konkrétně chybí' nelze
doptání formulovat."

**Nejsilnější doklad — hodnota schovaná v příloze.** `ISS-004` (`questions.yaml:2312-2337`):
text odpovědi zní vágně („Parameters for retry count and retry interval are available
within our settings"), ale **příloha (screenshot konfigurace WCS) obsahuje konkrétní
čísla** `interface_retry_max = 3`, `interface_retry_interval = 4000` ms. `still_missing`
u záznamu explicitně rozlišuje „chybí data" od „data jsou, chybí rozhodnutí o nich":
chybí (a) potvrzení závaznosti pro projekt, (b) kdo a kde je konfiguruje, (c) zápis do
specifikace. Poučení je zapsané i v `README.md:127-129` a `CLAUDE.md:45-47`:
**„devět dní se to vedlo jako 'chybí hodnoty'"** — dokud si někdo neotevřel přílohu.

**Přenositelná zásada.** Nedostatečnou odpověď neevidujte jen stavem („částečně") —
zapište explicitní větu, co přesně schází k rozhodnutí. Bez ní se doptání nedá
zformulovat a informace v přílohách zmizí za vágním textem mailu.

**Předvedatelnost.** Ukázat `ISS-004` a vedle otevřít ten screenshot
(`docs/plc/sources/bullseye/BullsEye-konfigurace-retry-parametry-2026-08-20.png`) —
publikum vidí, jak devět dní ležela odpověď, kterou nikdo nepřečetl.

### 3.4 Inbox jako fronta — a proč se nepřesouvá rukou

**Co to je.** `<dodavatel>/inbox/` je **vstupní fronta**: člověk sem nahraje uložený
`.msg` z Outlooku pod libovolným názvem. `<dodavatel>/mails/` je trvalé úložiště, kam
soubor po zpracování přejde pod normalizovaným názvem `YYYY-MM-DD_slug.msg`. **Přesun
dělá skript** (`--archive`), nikdy ruka.

**Kdo co dělá.** Nahrává člověk — `README.md:118-120`: „Nahraj `.msg` do fronty… Tím
vzniká povinnost zprávu zpracovat: **brána Q4 hlásí každou zprávu, která ve frontě leží.**"
Zpracovává `/dodavatele:mail`: přečte tělo i přílohy, napíše přepis, zapíše záznamy do
`questions.yaml` a na konci spustí `--archive`.

**Proč ne rukou.** `README.md:155-157` — „Přesouvá skript, ne ruka: cílem je `mails[].msg`
ze záznamu, takže **cesta v registru a umístění souboru nemohou vzájemně zestárnout**.
Cíl se nikdy nepřepisuje — existující soubor na cílové cestě je chyba, ne rutina."
Ruční přesun jiným jménem = záznam v YAML ukazuje na neexistující cestu; přesně to hlídá
Q4 jako **invariant** (`questions.py:262-267`: `msg: neexistuje ani ve frontě` → blokuje).

**Prázdná fronta = jediný potřebný signál „vše zpracované."** `README.md:159-162`:
„Zpráva bez záznamu v `mails:` i zpracovaná zpráva, kterou nikdo nepřesunul, jsou nález;
záznam ukazující na `.msg`, který neexistuje ani ve frontě, je invariant — **visící odkaz
na důkaz**." Ověřeno naživo: oba inboxy (`bullseye/inbox/`, `bluesword/inbox/`) obsahují
jen `.gitkeep` → `--check` vypíše `OK fronta inbox/ je prázdná` (`questions.py:253-254`).

**Analogický, už napálený případ — přepsaná verze dokumentu.** `README.md:136-138`
a `CLAUDE.md:51-52`: pod označením **„V1.6" existují v repozitáři dnes dva různé soubory**
(44 a 46 stran, různý obsah), protože se verze přepsala, aniž se zvedlo číslo. Proto se
dodavatelské PDF/PNG ukládají s **datem v názvu** a stará verze se nemaže.

**Přenositelná zásada.** Kde existuje závazný odkaz cesta→soubor v datovém zdroji, dělej
přesun i přejmenování výhradně nástrojem, který mění odkaz i soubor atomicky spolu.
Ruční přesun je právě ten krok, který registr a filesystem rozjede.

**Předvedatelnost.** Nakopírovat testovací `.msg` do `bullseye/inbox/`, spustit
`questions.py --check` (Q4 zahlásí zprávu ve frontě), pak `--archive` a `--check` znovu →
`OK fronta inbox/ je prázdná`. Krátká, čistá smyčka.

### 3.5 Brány Q1–Q6 — a dva různé druhy signálu

Tabulka bran `README.md:185-195`, implementace `questions.py:113-284` (funkce `check()`).
Pořadí v kódu není číselné — Q6 je první blok, protože je základní strukturální kontrola,
na kterou ostatní navazují.

| Brána | Co kontroluje | Typ / kde |
|---|---|---|
| **Q6** struktura a číselníky | stav z uzavřeného číselníku; `thread` existuje a `supplier` na něj sedí; otázka není prázdná; stav s odpovědí má `answer`; `Partially`/`Declined`/mlčení má `still_missing`; `mail` odkazuje na existující záznam v `mails:` | invariant `!!`, `questions.py:126-154` |
| **Q1** vazba na ontologii | `about` míří na existující `id` entity v `ontology.yaml`; opačně orphan `q:` reference z ontologie na neexistující dotaz | invariant, `questions.py:158-183` |
| **Q2** `landed_in` je platná citace | soubor existuje, číslo řádku je v rozsahu souboru | invariant, `questions.py:185-198` |
| **Q5** nedostatečná odpověď bez doptání | `Partially`/`Declined`, ale žádný dotaz na něj nenavazuje přes `follows_up_on` | nález `->`, `questions.py:200-212` |
| **Q3** stárnutí, přísliby, nevytěžené odpovědi | čeká déle než SLA (výchozí 7 dní); `promised.by` v minulosti; odpověď došla, ale `landed_in` prázdné | nález, `questions.py:214-233` |
| **Q4** fronta a úložiště | zpráva čeká ve frontě; `mails[].msg` na neexistující soubor; originál `.msg` bez MD přepisu; `transcript:` na neexistující soubor | mix, `questions.py:235-280` |

**Klíčové rozhodnutí — dva exit kódy.** `questions.py:17-20`, `README.md:197`:
**exit 2** = porušený invariant → blokuje (chyba v evidenci samotné: visící odkaz,
neplatná citace, neznámý stav). **exit 1** = nález → neblokuje (věcná otevřená práce:
stárnutí, propadlý příslib, nepropsaná odpověď). Odůvodnění `README.md:197-199`:
„Exit 2 blokuje, exit 1 ne. **Stárnutí a mlčení dodavatele nejsou vada dokumentu —
nesmí zastavit review nesouvisející specifikace.**"

**CLI** (`questions.py:7-15`, `main()` `587-611`): `--check` (brány), `--build`
(přegeneruje `OTEVRENE.md` + `QUESTIONS.tsv`), `--stats` (souhrn per vlákno), `--inbox`
(co čeká ve frontě), `--archive` (přesun inbox→mails), `--today YYYY-MM-DD`
(deterministické datum pro test stárnutí). Kombinovatelné, typicky `--check --build`.

**Přenositelná zásada.** Odděl v nástroji „evidence je vnitřně poškozená" (blokuje) od
„je tu otevřená práce" (jen upozorní). Jinak buď zablokuješ proces kvůli běžnému čekání
na dodavatele, nebo si zvykneš ignorovat i skutečné chyby.

**Předvedatelnost — nejsilnější demo v této oblasti.** Skutečný běh při průzkumu:
```
python docs/suppliers/.tools/questions.py --check
→ 0 porušených invariantů, 102 nálezů
   např. "AGV-014: PROPADLÝ PŘÍSLIB o 9 dní", "SHIP-001: čeká 84 dní (SLA 7)"

python docs/suppliers/.tools/questions.py --stats
→ 164 dotazů, 50 čeká na dodavatele, 58 odpovědí došlo a NENÍ ve specifikaci,
   2 přísliby (1 propadlý), nejstarší nezodpovězený SHIP-001 (84 dní)
```
Na obrazovce je okamžitě vidět rozdíl „0 invariantů" (evidence je strukturálně v pořádku)
vs. „102 nálezů" (věcná rozpracovanost, ne chyba).

### 3.6 Zdroj pravdy vs. generovaný derivát

**Co to je.** `questions.yaml` je jediné místo, které se edituje ručně (nebo Claudem) —
a to **řádkově, nikdy přes `yaml.dump`** (`CLAUDE.md:13`). `OTEVRENE.md` (lidský přehled:
čeká se / mlčení / propadlé přísliby) a `QUESTIONS.tsv` (grep-ovatelná tabulka) se
generují `--build` a **needitují se ručně**.

**Doklad.** `README.md:6-8` — „Zdroj pravdy: `questions.yaml` — píše se ručně nebo
Claudem, nikdy generátorem. Přehled pro lidi: `OTEVRENE.md` — generovaný, needituj.
Pro grep: `QUESTIONS.tsv` — generovaný." `POSTUP-pro-analytiky.md:194-195` — „Neupravovat
`OTEVRENE.md` ani `QUESTIONS.tsv`. Jsou vygenerované — **při dalším přegenerování se změna
ztratí**." Derivát to nese sám v hlavičce (`OTEVRENE.md:1-2`, generuje
`questions.py:338-339`): `<!-- GENEROVANO — needituj. Zdroj: docs/suppliers/questions.yaml -->`.

**Dvě textové vrstvy dohledatelnosti** (`README.md:164-176`): (1) doslovné
`question:`/`answer:` u záznamu + `QUESTIONS.tsv` — pokrývá všechny dotazy; (2) plný přepis
mailu v `<dodavatel>/threads/*.md` — sem míří citace `soubor:řádek`, protože v binárním
`.msg` citovat nelze. README **sám přiznává mezeru**: vrstva 2 je zatím jen u části mailů,
starší pocházejí z přebraného registru bez doslovného textu zprávy.

**Přenositelná zásada.** Generovaný derivát nikdy needituj přímo — je to jen projekce
zdroje pravdy. Potřebuješ jinou strukturu výstupu? Změň generátor nebo zdroj, ne výstup.
A napiš varování **do generovaného souboru samotného**, ne jen do README.

**Předvedatelnost.** Ukázat hlavičku `OTEVRENE.md`, pak `--build` a `git diff` → soubor
se přepsal beze zbytku.

### 3.7 Dva chytré detaily navíc

**Mlčení se nezapisuje slovy, dopočítává se strukturou.** `README.md:99-104`: když
příchozí mail v `mails:` vyjmenuje otázky, které měl řešit, a některá z nich nemá
`answered_on`, je to **automaticky detekovaný „přeskočený bod"** — žádné nové pole není
potřeba.
→ *Zásada:* mlčení dokládej strukturou (co mělo být zodpovězeno vs. co skutečně je),
ne subjektivním zápisem.

**`Answered` × `landed_in` je záměrně oddělené.** `README.md:106-114`: odpověď, která
dorazila, ale nepropsala se do specifikace, je „stejně neúčinná jako odpověď, která
nedorazila". A je to dnes **největší otevřená položka registru: 58 ze 164 dotazů** —
ležící na naší straně, ne na straně dodavatele.
→ *Zásada:* měř nejen „přišla odpověď", ale „je odpověď použitá". Druhé číslo bývá
nepříjemnější a je celé tvoje.

---

## 4. `docs\plc\.plc-tools\` — linter PLC specifikace

**Kontext pro netechnické publikum.** PLC specifikace popisuje, jak si WES (nadřazený
systém) a PLC (řídicí automat dopravníků) povídají přes **datové bloky** — sdílené kusy
paměti PLC, kam WES zapisuje příkazy a PLC stavy. Tvar bloku definuje **UDT** (vlastní
datová struktura) — tabulka s offsety (na kterém bajtu pole začíná), typem a názvem.
`plc-lint.py` je Python skript bez závislostí, který tabulku čte jako text a kontroluje
aritmetiku a konvence. Funguje jako **brána**: `exit 0` projde, `exit 2` blokuje (aspoň
jedna ERROR); WARN/INFO neblokují (`--strict` zpřísní).

### 4.1 Co linter kontroluje deterministicky (4 vybraná pravidla)

**a) B14 — countery musí být `WORD`, ne `INT`.** Counter = čítač, který se zvedne o 1,
kdykoli jedna strana říká druhé „stala se událost". `WORD` = bezznaménkové 1–65535,
`INT` = i záporné. Pro čítač, co se počítá nahoru a přetáčí, znaménko nedává smysl.
Konvenci fixuje `ADR-ASK-HW-003.md:149` („`WORD`, 1–65535, `0` = po inicializaci").
Pravidlo v kódu `plc-lint.py:321`; živý příklad `AlzaSk-PLC-specifikace.md:1049`.
**Zajímavost:** šablona má v ČÁST 1 historicky ještě `INT` (`Šablona-PLC-specifikace.md:248,278`),
proto ji `--all` běh **záměrně vynechává** (`.plc-tools/README.md:40-42`).
→ *Zásada:* když se konvence změní, starý referenční dokument nemusí hned dohnat realitu —
lepší ho z brány vyloučit **explicitně a viditelně** než ho nechat generovat šum.

**b) B3/B15 — sudé zarovnání každého pole.** Paměť PLC se čte po dvojicích bajtů; víceubajtové
hodnoty musí začínat na sudé adrese. Pravidlo platí pro **každé** pole (i bitové bloky
a rezervy), ne jen „velká". **Vzniklo z reálného nálezu:** `Šablona-PLC-specifikace.md:326-334`
uvádí scénář — bitmapa 35 tlačítek jako `BYTE[7]` (lichá velikost) skončí na liché adrese
a posune všechna následující pole. Stalo se to v produkci a bylo opraveno:
`AlzaSk-PLC-specifikace.md:11` (changelog 1.6) — `ButtonsPressed` zvětšen z `BYTE[7]`
na `BYTE[8]`. Kód `plc-lint.py:356`.
→ *Zásada:* **pravidlo, které vzniklo z jednoho konkrétního nálezu v realitě (ne z teorie),
je nejsilnější kandidát na zápis do linteru** — je to nejlevnější způsob, jak zajistit,
že se stejná chyba nestane podruhé.

**c) B9 — handshake páry `{Pole}Counter` ↔ `Last{Pole}Counter`.** Handshake = podání ruky:
jedna strana zvýší čítač, druhá to zpozoruje, zpracuje a hodnotu si překopíruje do pole
`Last...`, čímž potvrdí přijetí. B9 kontroluje, že ke každému čítači existuje protějšek.
`ADR-ASK-HW-003.md:67-80` zavedl **per-field** model — každé sledované pole
(`AccessState`, `ResetPressed`, `StartPressed`, `FaultCode`) má **svůj** pár, aby příjemce
věděl, co se změnilo, bez porovnávání celého snapshotu. Kód `plc-lint.py:412-421`;
živý pár `AlzaSk-PLC-specifikace.md:1487` ↔ `:1472`.
→ *Zásada:* když architektonické rozhodnutí znásobí počet symetrických dvojic, které musí
zůstat v páru (countery, getter/setter, request/response), je to kandidát na cross-reference
kontrolu, ne na pozornost autora.

**d) B4/B5 — UDT „Celkem" = součet polí a násobek 50.** Na konci tabulky UDT je řádek
„Celkem" s celkovou velikostí bloku. Linter ověří (1) že součet polí dá deklarované číslo
(**B4, ERROR**) a (2) že je to násobek 50 (**B5, warning** — rezerva pro rozšíření).
`.plc-tools/README.md:101`; živé příklady `AlzaSk-PLC-specifikace.md:1477,1500,2194`.
→ *Zásada:* **kontrolní součet na konci strukturovaného dokumentu** je nejlevnější způsob,
jak zachytit chybu „utekla mi jedna číslice" dřív, než ji najde implementátor.

### 4.2 Co linter NEKONTROLUJE — sémantika (třída 4)

**Co to je.** Linter čte tabulky jako čísla a text podle vzoru — **nerozumí významu**.
Neumí posoudit, jestli slovní popis chování odpovídá stavovému diagramu o dva odstavce
níž, jestli barva majáku v textu sedí s prioritní tabulkou, jestli číselník v UDT odpovídá
protokolu. To je práce čtenáře s porozuměním — zde subagenta **`review-semantic`**.

**Doklad.** `.plc-tools/README.md:87-91` to explicitně pojmenovává jako „Třída 4 —
sémantika" s odkazem na „rozhodnutí v průzkumu linterů" — **vědomé rozhodnutí**
nerozšiřovat deterministický nástroj na věci vyžadující porozumění. Stejná dělba je
napříč repem: `.claude/agents/review-structural.md:159` a `review-design.md:215`
(„Nekontroluj obsah scénářů — to je práce review-semantic agenta"), `CLAUDE.md:282`.

**Konkrétní případ, který linter nikdy nezachytí.** `AlzaSk-PLC-specifikace.md:12`
(changelog 1.7): „**Po adversariální revizi:** … ze stavového diagramu 4.D odstraněn
chybně přidaný přechod `CLOSING → ALARMED`." Obě strany (diagram i text) jsou syntakticky
v pořádku — jen si odporují významem.

**Přenositelná zásada.** Rozděl kontrolu na to, co je **ověřitelné bez porozumění** (čísla
sedí, odkazy existují, formát je dodržen → linter), a na to, co vyžaduje **porozumění
obsahu** (souhlasí popis s diagramem → LLM/člověk) — a nikdy nenech druhé předstírat, že
to dělá první.

### 4.3 „Spec je pro externího PAC" — self-contained dokument

**Co to je.** PLC specifikaci čte primárně **externí programátor PAC** (dodavatel
elektrifikace a programování PLC), který **nemá přístup** k internímu repozitáři — nevidí
ADR, FR ani šablonu. Dokument musí „unést sám sebe": vysvětlit chování inline, ne odkazem
„viz ADR-ASK-HW-003".

**Zajímavý nález pro workshop.** Princip existuje **jako záznam v osobní paměti, ne jako
vynucená brána** — a proto se pomalu porušuje. `grep "ADR-ASK|FR-COMP"` v
`AlzaSk-PLC-specifikace.md` najde **2 výskyty** (`:343` a `:1617`, oba `ADR-ASK-HW-001`
v poznámce k barvě majáku), které prošly reviewem nepovšimnuty. Zbytek dokumentu princip
drží — changelog (`:3-13`) popisuje změny věcně, bez odkazů na interní rozhodovací proces.

**Přenositelná zásada.** Publikum specifikace určuje, co v ní smí být jako odkaz — dokument
pro čtenáře bez tvého interního kontextu musí být sebe-nosný. **A pokud tohle pravidlo
není vynucené branou, bude se v praxi pomalu porušovat, i když je zapsané.**

**Předvedatelnost.** `grep -n "ADR-ASK\|FR-COMP" docs/plc/AlzaSk-PLC-specifikace.md` →
ukáže právě ty 2 řádky. Dobrý úvod do diskuze „měl by to linter hlídat?".

### 4.4 Meze nástroje — GOTCHY

**a) Tučně značené UDT tabulky jsou pro linter neviditelné.** Linter pozná UDT podle
markdown **nadpisu** (`#### UDT_X_WesToPlc`). Když je název jen tučně v odstavci
(`**UDT_X_WesToPlc**`, jak to dělá mezaninová spec — `AlzaSk-PLC-specifikace-mezanin.md:1025`),
linter tabulku **nerozpozná jako UDT** a B1/B2/B4 se na ni vůbec nespustí.
**Přesně tímhle mechanismem unikla reálná chyba** vedoucí k `ADR-ASK-HW-006`:
`STRING[40]` byl počítán jako 40 B místo 42 B (N+2). Zdokumentováno v
`ADR-ASK-HW-006.md:99-103` v sekci „Negativní / omezení", včetně přiznání, že sjednocení
značení tabulek na `####` je otevřený bod tooling mimo rozsah ADR.
→ *Zásada:* **deterministický nástroj je jen tak dobrý, jak dobře rozpozná svůj vstup** —
konvence formátování může tiše vypnout celou třídu kontrol. Zdokumentuj to jako známé
omezení, nenechávej jako skryté riziko.

**b) A1 — vědomě „měkké" pravidlo pro placeholder ID.** ID zařízení má mít formát `PLCxxx`,
ale dokud dodavatel nepřidělí finální číslo, spec smí obsahovat rozsahy jako `PLC511–516`.
Linter je hlásí jen jako WARN (`.plc-tools/README.md:54`), stejně jako `TODO`/„k ověření"
(`README.md:103`).
→ *Zásada:* brána musí rozlišit „nedodělané, protože čekáme na externí vstup" od „chyba" —
jinak si autoři zvyknou bránu obcházet, protože jim blokuje i legitimně otevřené body.

**c) A8 — zónové bloky jako vědomá výjimka.** Každé ID v mapování DB by mělo být
v „Seznamu zařízení"; bezpečnostní zónové bloky (`UDT_ZoneSafety`) mají v mapování víc
instancí, proto jen INFO (`plc-lint.py:493-498`, `README.md:82`, živě
`AlzaSk-PLC-specifikace.md:2477-2501`).

### 4.5 Předvedatelnost — návrh bloku workshopu

1. **Živá brána:** `docs/plc/.plc-tools/validate.cmd` na produkční spec → exit 0, ale
   desítky WARN (A1 placeholdery, A8 zónové bloky) — rozdíl blokující/neblokující.
2. **Rozbít pravidlo naživo:** `WORD`→`INT` u counteru → `[ERROR] B14 ... musí být WORD
   (1–65535)`, exit 2. Nejrychlejší a nejnázornější demo celého workshopu.
   Alternativy: smazat `LastAccessStateCounter` → `[ERROR] B9 ... rozbitý handshake`;
   smazat řádek pole a nechat „Celkem" → `[ERROR] B4`.
3. **Sémantika mimo rozsah:** `README.md:87-91` + changelog 1.7 (odstraněný chybný přechod
   `CLOSING → ALARMED`).
4. **GOTCHA mezanin:** `python docs/plc/.plc-tools/plc-lint.py docs/plc/AlzaSk-PLC-specifikace-mezanin.md`
   → u tučně značených tabulek (`:1025`, `:1044`) **ticho tam, kde má být kontrola**.

---

## 5. `docs\bp-overview\` — týdenní snapshoty

### 5.1 WIP v kořeni vs. zmražený snapshot

**Co to je.** Jeden živý dokument (`Prehled_BP_use_cases.md`) shrnuje stav všech skladových
procesů — průběžně se do něj píše. Jednou za čas se z něj udělá **otisk** (kopie), který
se předá zákazníkovi/týmu jako oficiální předávka za daný týden. Otisk se už nikdy nemění.

**Doklad.** `README.md:79-81`: „Soubor `Prehled_BP_use_cases.md` v kořeni `bp-overview/`
je **pracovní** — obsahuje aktuální stav včetně rozpracovaných kapitol pro budoucí týdny.
**Nepřejmenovává se** (žádný prefix), protože je živý." `CLAUDE.md:27`: „Zamrzlý baseline
staršího týdne se zpětně NEpřejmenovává — měň jen aktuální týden."

**Přenositelná zásada.** Odděl „živý pracovní dokument" (jeden, stále se přepisuje) od
„zmražených historických otisků" (mnoho, nemění se nikdy zpětně) — každý má jiná pravidla
úprav.

**Předvedatelnost.** `Prehled_BP_use_cases.md` (bez prefixu, bez hlavičky s verzí) vedle
`T30+31+32/T30_T31_T32_Prehled_BP_use_cases.md` (prefix + hlavička s verzí/datem/autorem).

### 5.2 Pomlčka = kód, podtržítko = popis

**Co to je.** V názvu souboru se identifikátor a čitelný popis píší dvěma různými styly:
kód (`TC-BP-DECANT-002-01`) má pomlčky a VELKÁ písmena, popis (`Prehled_BP_use_cases`)
podtržítka a Title-case. Vše ASCII, bez mezer a diakritiky (`CLAUDE.md:14`).
Pravidlo zkráceně `README.md:29-37`: *„pomlčka = kód, podtržítko = popis."*
Konvence je **převzatá z `docs/fr/`**, nevymyšlená znovu (`CLAUDE.md:14`).

**Přenositelná zásada.** Konvence pojmenování se nevymýšlí per adresář — přebírá se odjinud
z repozitáře, aby byl vizuální jazyk napříč projektem jednotný.

**ANTIPATTERN nalezený v praxi.** `T24/T24_PREHLED-BP-use-cases.md` konvenci **porušuje**
(VELKÁ písmena a pomlčky v popisné části; mělo být `T24_Prehled_BP_use_cases.md`, jak to
mají všechny ostatní týdny). V této oblasti **neexistuje validátor** jako u FR/ADR/PLC —
jde o čistě manuální disciplínu.
→ *Zásada pro workshop:* konvence popsaná v README/CLAUDE.md, kterou nikdo nekontroluje
skriptem, se rozpadne. Tohle je ta ukázka.
**Předvedatelnost:** `ls docs/bp-overview/T24/` vs. `ls docs/bp-overview/T23/`.

### 5.3 Hlavička s „Poslední změny" — lehký diff pro čtenáře

**Co to je.** Každý předaný dokument má na začátku razítko (verze / datum / autor) a hned
pod ním odrážky „co se od minula změnilo" — čtenář nemusí porovnávat celý dokument.

**Doklad.** Vzor `README.md:45-51`: `> **Verze:** T{NN} · **Datum:** YYYY-MM-DD ·
**Autor:** {Jméno Příjmení}` + povinná sekce „Poslední změny (od verze T{NN-1}):".
Reálně `T23/T23_Prehled_BP_use_cases.md:1-15` (verze T23, 2026-06-08, čtyři odrážky změn
oproti T22). Novější příklad zaznamenává i přečíslování kapitol:
`T30+31+32/T30_T31_T32_Prehled_BP_use_cases.md:9-15` — „nová kapitola **12. Expediční
dopravníkový výtah**… následující kapitoly přečíslovány (původní 12–18 → 13–19)".
Changelog jde dál a je explicitně **rozdílový**: `T30+31+32/T30_31_32_Changelog.md:4` —
„Dokument je **rozdílový** vůči předchozí verzi (T27+28+29)… Změny už jednou předané se
neopakují."

**Přenositelná zásada.** Verzovaný předávaný dokument nese vlastní „od-do" deltu přímo
v hlavičce — čtenář nemusí dělat diff sám.

### 5.4 Co se předává vs. co je interní — dvojí changelog

**Co to je.** Ne všechno interní jde k zákazníkovi. Existují **dvě verze changelogu**:
surová interní (`Changelog_interni.md` — vše, i drobnosti a technický žargon) a z ní
odvozená zákaznická (`Changelog.md` — jen relevantní a srozumitelné). Podobně `tc-katalog/`
je pracovní podklad, který se nikdy neodesílá.

**Doklad.** `README.md:65-77` — tabulka „Co se předává a co ne": `Changelog_interni.md` →
„❌ NE — interní"; `tc-katalog/` → „❌ NE — interní"; „Interní podsložky… zůstávají bez
prefixu, protože opouštějí strukturu jen pro interní použití." Totéž `CLAUDE.md:29-30`.
Reálný pár: `T23/T23_Changelog_interni.md:1-11` (technický, „11 novinek, 7 vylepšení…")
vs. `T23/T23_Changelog.md:1-10` (orientovaný na dopad pro WMS/API).

**Přenositelná zásada.** Odděl „pracovní podklad / surový zdroj" od „hotového výstupu pro
čtenáře mimo tým" už na úrovni adresářové struktury + explicitní tabulkou „předává se /
nepředává se".

**ANTIPATTERN — dokumentace driftuje od praxe.** `tc-katalog/` existuje jen v `T22/`
(32 souborů) — v žádném pozdějším týdnu už ne, ačkoli README pravidlo pro něj stále
popisuje jako platné. `Changelog_interni.md` mizí od `T27+28+29/` dál (poslední výskyt
`T25+T26/T26_Changelog_interni.md`). README nikdo needitoval po 2026-06-11
(commit `85ddca1`), zatímco poslední snapshoty jsou z 8/2026.
**Předvedatelnost:** `find docs/bp-overview/T22 -type d` (má `tc-katalog/`) vs.
`find "docs/bp-overview/T27+28+29" -type d` (nemá).

### 5.5 ANTIPATTERN — praxe utekla metodice (sloučené snapshoty)

Praxe se posunula od jednoho snapshotu za týden (`T22/`, `T23/`, `T24/`) ke **sloučeným**
(`T25+T26/`, `T27+28+29/`, `T30+31+32/`), když se k předání nedostalo každý týden.
README ani CLAUDE.md vzor `T{NN}+T{NN+1}+...` **nikde nezmiňují** — workflow
(`README.md:89-106`) počítá jen s jednotýdenním `T{NN+1}`.
→ *Zásada:* konkrétní příklad, kdy praxe v repozitáři „utekla" dokumentované metodice.
Dobrý materiál pro diskusi „kdy je čas README aktualizovat" — a proč se to nestane samo.

---

## 6. `docs\scenarios\` — procesní scénáře SCE-*

### 6.1 Třetí typ artefaktu vedle FR a TC

**Co to je.** SCE je **provázaná ukázka z praxe** — čtivý příběh jednoho konkrétního
průchodu skladem od začátku do konce (např. jak paleta přijede, vydekantuje se a prázdný
obal se vrátí), který ukazuje spolupráci víc algoritmů a procesů. Není to formální
požadavek (co systém MUSÍ — to je FR) ani technický test (Gherkin kroky — to je TC).

**Doklad.** `README.md:3`: „Tato složka obsahuje **E2E referenční scénáře** — koloběhy
demonstrující spolupráci více algoritmů a BP v jednom souvislém průchodu systémem AlzaSk
WES." `README.md:5` explicitně vymezuje scope: „scénáře **nejsou FR** (žádné normativní
*Požadavky*) **ani TC** (žádný Gherkin). Slouží jako orientační walkthrough s explicitní
vazbou na konkrétní FR a TC přes pole `covers_fr` / `covers_tc`."

**Přenositelná zásada.** Normativní požadavek (co musí platit), technický test (jak se to
ověří) a naratívní walkthrough (jak to vypadá v realitě, propojující víc požadavků) jsou
**tři různé artefakty s různým publikem** — nemíchat je do jednoho dokumentu.

**Předvedatelnost.** `SCE-DEKANT-01_Automaticka_dekantace_palety.md:76-80` (plynulý český
text Kroku 1) vedle formálního Gherkin TC, na který odkazuje
(`../fr/comp/alg/stacking/tc/TC-COMP-ALG-STACKING-001-01_Rozhodovaci_logika.feature`) —
kontrast „čtivý příběh" vs. „strojově strukturovaný test".

### 6.2 Obousměrná trasovatelnost na dvou úrovních granularity

**Co to je.** Každý SCE má v hlavičce seznam, které FR a TC pokrývá; navíc **každý Krok**
má na konci jednořádkovou poznámku „toto pokrývá tenhle konkrétní FR a tenhle test".
Je tedy vidět, který kus vyprávění odpovídá kterému formálnímu dokumentu.

**Doklad.** `README.md:32-47` — povinný YAML frontmatter (`id`, `title`, `curator`,
`status`, `created`, `updated`, `covers_fr`, `covers_tc`). `README.md:51-58` — struktura:
Úvod → Scope koloběhu → Konfigurace → Přehled kroků → Kroky 1..N (každý s blokem
`> Pokrytí: ...`) → Konečný stav. Reálně: `SCE-DEKANT-01…md:1-23` (11 FR a TC odkazů)
a `:76-80` — Krok 1 končí `> Pokrytí: STACKING-001 *Krok 1 rozhodovací logiky* ·
[TC-COMP-ALG-STACKING-001-01](...) S01.`

**Přenositelná zásada.** Naratívní dokument, který má být „mapou" mezi formálními
artefakty, potřebuje **explicitní strojově čitelné odkazy (ne jen prózu)** na obou
úrovních — dokument jako celek i jednotlivé kroky. Jinak z něj bude jen další volný text
bez trasovatelnosti.

### 6.3 I vyprávěcí dokument má ID, vlastníka a stav

Formát `SCE-{OBLAST}-{NN}_{Nazev}.md`, oblasti DEKANT, PICK, INBOUND, EXPED, EMPTY, CROSS
(`README.md:9-28`). Tabulka „Aktuální scénáře" (`README.md:62-67`) má ID / Název / Status /
Kurátor — oba existující scénáře (SCE-DEKANT-01, SCE-PICK-01) jsou `draft`, kurátor
Tomáš Wrona. Samostatný `INDEX.md` zde **nevznikl záměrně** — pro 2 položky stačí tabulka
v README (práh ~10 položek dle kořenového `CLAUDE.md`).

**Přenositelná zásada.** I „vyprávěcí" dokument potřebuje stabilní ID, vlastníka a stav —
jinak se v adresáři s desítkami souborů ztratí, co je hotové a kdo za to odpovídá.
A registr (INDEX) se zakládá až nad prahem, ne preventivně.

---

## 7. `.claude\agents\review-*.md` — pět review subagentů

**Co to je (pro publikum).** Subagent = specializovaný „asistent" s jedním úkolem
a omezenou sadou nástrojů. Zde jich je pět; **čtyři smí jen číst a napsat nález do textu**,
jeden jediný (`review-fixer`) smí skutečně editovat dokumenty. Nad nimi běží řídicí příkaz
`/review-docs`, který je spouští ve vlnách, sbírá výstupy a rozhoduje, kdy je potřeba
člověk.

**Soubory:** `review-structural.md`, `review-semantic.md`, `review-design.md`,
`review-fixer.md`, `review-reporter.md` (vše `.claude\agents\`); orchestrace
`.claude\commands\review-docs.md`.

### 7.1 Dělba práce — levné vpředu, drahé vzadu

| Agent | Model | Úkol | Smí editovat? |
|---|---|---|---|
| `review-structural` | **haiku** (levný) | mechanická kontrola: existují odkazované soubory, sedí ID vzory, jsou vyplněná povinná pole frontmatteru, sedí číselníkové kódy proti `initData.json` (`:3-6, 60-121`) | ne |
| `review-semantic` | **sonnet** | obsahová konzistence FR/TC vůči API YAML, ADR, procesní analýze; drží explicitní **hierarchii autorit** (procesní analýza > ADR > API YAML > initData > FR > TC), při rozporu vždy viní **nižší** dokument (`:3-6, 22-33`) | ne |
| `review-design` | **opus** (nejdražší) | nejvyšší patro — ADR ↔ API spec ↔ procesní analýza ↔ FR jako celek („vyprávějí konzistentní příběh"), cross-reference `related_adr`, `supersedes`/`superseded_by`, webhook/event konzistence (`:3-6, 23-33`) | ne |
| `review-reporter` | haiku | **nic sám nezkoumá** — agreguje a dedupuje výstupy tří výše, klasifikuje nález na AUTO-FIX / ARCH-DECISION / CONTENT-GAP (`:3-6, 15-21, 47-56`) | jen zápis reportu |
| `review-fixer` | opus | **jediný editor** — aplikuje auto-fixy, respektuje seznam zakázaných cest (`docs/analysis/**`, `docs/api/**`, celé `../myfaber/**`) (`:3-6, 40-63`) | **ano** |

**Doklad úspory.** `review-docs.md:166-176` uvádí ~80 % úsporu u haiku kroků.

**Přenositelná zásada.** Review lze rozložit podle **náročnosti a rizika**: levný/rychlý
mechanický filtr nejdřív, drahé posouzení obsahu až na to, co projde filtrem — a **právo
zapisovat dej jen jedné roli**, ne všem.

### 7.2 Auto-fix bez schvalování × ARCH-DECISION

`review-fixer.md:13`: „Opravuješ VŠECHNY auto-fixable nálezy **bez čekání na schválení**."
Rozlišuje mechanickou opravu (doplnění chybějícího pole, TC reference, tagu) od
**ARCH-DECISION** — rozporu mezi dvěma autoritativními zdroji (např. FR odporuje ADR),
kde se auto-fix vždy zastaví a čeká na člověka (`review-fixer.md:23-38, 93-105`).
Report pro člověka (`docs/fr/REVIEW-REPORT.md`) obsahuje **výhradně** ARCH-DECISION —
nic mechanického tam nepatří (`review-reporter.md:13, 180`).

**Přenositelná zásada.** Automaticky opravuj vše, co je jednoznačné; člověku předkládej
**jen to, co je skutečné rozhodnutí** — report zaplavený mechanickými nálezy se přestane
čítat.

### 7.3 Orchestrace v pěti fázích

`.claude\commands\review-docs.md:1-186`: **0** příprava scope + smazání temp adresářů →
**1** paralelní běh `review-structural` + `review-semantic` per detekovaná oblast +
`review-design` jednou napříč (`run_in_background: true`) → **2** `review-reporter`
agreguje → **3** **iterativní auto-fix smyčka (max 3×**: fixer → `validate.py` → re-check
→ reporter) → **4** prezentace výsledků → **5** aplikace lidských rozhodnutí
z `REVIEW-REPORT.md`.

**Přenositelná zásada.** Smyčka „oprav → znovu zvaliduj → znovu zkontroluj" s **pevným
limitem iterací** je lepší než jednorázový průchod i než nekonečné dolaďování.

**Předvedatelnost.** `/review-docs container` — ukázat (a) plán ve Fázi 0 (kolik souborů
a agentů), (b) paralelní běh v pozadí s hlášením „Dokončeno 3/7…", (c) výsledný
`docs/fr/REVIEW-REPORT.md` s kartami ARCH-DECISION a poli `Rozhodnutí:`/`Stav:`,
(d) že mechanické nálezy zmizely samy.

---

## 8. `.claude\commands\` — vlastní slash commandy (8)

**Co to je.** Slash command = uložený pojmenovaný postup, který se vyvolá krátkým příkazem
(`/prikaz argument`) místo psaní celé instrukce znovu. Pokrývají dvě domény: komunikaci
s dodavateli a „projektového asistenta" pro vývojáře.

| Soubor | Co dělá |
|---|---|
| `dodavatele\hotovo.md` | Zapíše, že odpověď dodavatele je propsaná do specifikace. Bere `$ARGUMENTS` (ID + místo), **ověří citaci**, doplní `landed_in` v `questions.yaml`, spustí bránu `questions.py --check --build` (`:1-23`) |
| `dodavatele\mail.md` | Zpracuje e-mail od/pro dodavatele. Bez argumentu projde frontu `--inbox`; **povinně otevírá přílohy**, zapisuje doslovný přepis, archivuje originál (`:1-30`) |
| `dodavatele\stav.md` | Vypíše, na co se čeká. Rozsah vše/dodavatel/vlákno/téma; odděluje **4 situace** (čekáme / dodavatel přeskočil bod / propadlý příslib / odpověď nepropsaná) (`:1-27`) |
| `glossary.md` | Termín v projektovém slovníku — čte `docs/onboarding/glossary.md`, cituje `soubor:řádek`, u datové vazby odkáže tabulku v myFABER (`:1-23`) |
| `learn.md` | Režim UČENÍ — klade 1-2 kalibrační otázky, čte **10 zdrojů v pevném pořadí** (overview→glossary→analýza→PBS→FR→ADR→API→myFABER ADR→datový model→kód) (`:1-43`) |
| `lookup.md` | Režim DOHLEDÁNÍ — stručná faktická odpověď (max 5-10 řádků) s přesnou citací, **žádný konverzační tón** (`:1-38`) |
| `overview.md` | Prezentuje `docs/onboarding/project-overview.md`, případně zaměřený na oblast z `$ARGUMENTS` (`:1-17`) |
| `review-docs.md` | Koordinovaný review — orchestruje 5 agentů (viz sekce 7) (`:1-186`) |

**Poznámka — nesoulad dokumentace vs. realita.** Kořenový `CLAUDE.md` je dokumentuje jako
`/project:learn`, `/project:lookup` atd., ale soubory leží **přímo** v `.claude/commands/`
(ne v podsložce `project/`) — reálné vyvolání je `/learn`, `/lookup`, `/overview`,
`/glossary`, `/review-docs` a namespace `/dodavatele:*`. Drobný, ale konkrétní příklad
driftu dokumentace.

**Přenositelná zásada.** Opakovaný, přesně definovaný postup (zpracování zprávy, styl
odpovědi, kontrolní sekvence) ulož jako **pojmenovaný znovupoužitelný příkaz**, ne jako
naději, že si ho pokaždé správně zformuluješ. Zvlášť cenné u kroků, které se snadno
opomenou — `dodavatele:mail` má „vždy otevři přílohy" jako součást postupu, ne jako radu.

**Předvedatelnost.** `/dodavatele:stav` bez argumentu — živý report se čtyřmi odlišenými
situacemi. Nebo `/lookup <projektový dotaz>` — stručná odpověď s `soubor:řádek` citací.

---

## 9. `.claude\skills\` — projektové skills (2)

**Co to je.** Skill = balíček instrukcí a postupů, který se aktivuje, když na něj přijde
řeč (description říká, kdy ho použít). Rozdíl od commandu: command vyvolává **člověk**,
skill si vybírá **model** podle situace.

**Ověřeno výpisem: v tomto repozitáři jsou přesně 2 projektové skills.** Ostatní jmenované
(`pruzkum`, `body-z-jednani`, `therapy`…) přicházejí z pluginu/uživatelské úrovně;
`glossary`/`learn`/`lookup`/`overview`/`review-docs` zde existují jako **commandy**, ne
skills (viz sekce 8).

### 9.1 `dotazy-dodavatele-alzask`

**Description** (`SKILL.md:3-9`): „Evidence dotazů a odpovědí s dodavateli BullsEye
(4D shuttle, dopravníky) a BlueSword (AGV/RCS) — otázka s trvalým ID, doslovná odpověď,
co konkrétně chybí, příslib s termínem a odkaz, kde je odpověď propsaná ve specifikaci.
Použij, kdykoli přijde nebo se posílá e-mail dodavateli, kdykoli je potřeba zjistit, na co
se u dodavatele čeká nebo jestli už na něco odpověď máme, a kdykoli se odpověď dodavatele
zapisuje do FR, ADR nebo PLC specifikace."

Rozpozná **šest situací A–F** (`:18-27`): nová zpráva / stav / dohledání / propsání /
doptání / příslib.

**Navázání na nástroje** — skill je tenká vrstva nad skripty:
`questions.py --inbox` (`:37`), `msg_extract.py <soubor.msg> [--body|--attachments]`
(`:47-49`), `questions.py --archive` (`:84`), `questions.py --check --build` jako brána
(`:156-161`, exit 2 = blok, 1 = nálezy, 0 = čisto), zdroj pravdy `questions.yaml`
edituje **řádkově, nikdy `yaml.dump`** (`:68`).

### 9.2 `ontologie-prvku-alzask`

**Description** (`SKILL.md:3-9`): „Registr prvků systému AlzaSk — fyzické prvky, datové
entity, číselníky a aktéři s atributy, vztahy, instancemi a citacemi `soubor:řádek`.
Použij při psaní specifikací, FR, ADR a technických dokumentů, kdykoli potřebuješ ověřit
fakt o prvku systému — kolik jich je, kdo je dodal, čím jsou řízené, co na ně navazuje,
nebo které zdroje si o nich odporují."

**Soubor je generovaný** ze `ontology.yaml`, needituje se ručně (`:11-13`) — skill sám je
derivát, viz sekce 2.2 (a bránu G5 „zrcadlo skillu odpovídá registru").

**Navázání:** `INDEX.md` (rejstřík, vejde se celý — `:22, 41`), `entities/<id>.md`
(otevírat **jen potřebné** karty — `:25`), `TERMS.tsv` a `RELATIONS.tsv` — velké soubory,
**jen grepovat, nenačítat** (`:27-33`), `conflicts.md` (`:34-35`),
`cite.py <soubor:řádek> [--context N | --entity <id>]` — verdikt `OK`/`POSUN`/`ZMIZELA`,
číslo řádku **nikdy neopravovat ručně** přes `Read` (`:49-70`).

**Přenositelná zásada (obě skills).** Skill nemá obsahovat znalost — má obsahovat
**navigaci ke znalosti a příkaz, který ji ověří**. Když je referenční báze příliš velká na
načtení, dej modelu malý rejstřík + nástroj, který umí ověřit platnost konkrétní citace,
místo aby slepě věřil číslu řádku.

**Předvedatelnost.** `python docs/ontology/.ontology-tools/cite.py <soubor:řádek>` → živý
verdikt; nebo `python docs/suppliers/.tools/questions.py --stats` → živá čísla.

---

## 10. `.claude\settings.json` — hooky

**Co to je (pro publikum).** Hook = automatický spouštěč: „když se stane X, spusť Y".
Nezávisí na tom, jestli si to model nebo člověk vzpomene.

**Dva zdroje hooků.** Projektový `settings.json` má **jeden** hook; druhý, mechanicky
klíčový, přichází z **pluginu `spec-factory`** nainstalovaného na uživatelské úrovni
(mimo repozitář). `settings.local.json` žádné hooky nemá — jen `permissions.allow`
a `skillOverrides` (lokální, negitovaný).

### 10.1 SessionStart — warning-only kontrola registru

**Co to je.** Spouští se při otevření nové konverzace i po `/clear` a zkontroluje, jestli
je registr prvků aktuální — jestli se nezapomnělo přegenerovat deriváty nebo neposunuly
citace.

**Konfigurace.** `.claude\settings.json:10-20` — event `SessionStart`, matcher
`"startup|clear"` (tedy **ne** po `/compact`), příkaz
`python "docs/ontology/.ontology-tools/session-check.py"`.

**Co skript dělá.** `session-check.py` (79 ř.) volá `build.py --check` (`:41`) a
`reanchor.py --check` (`:51`).

**Klíčová vlastnost — vždy exit 0.** `session-check.py:74`:
`return 0  # warning-only: NIKDY neblokovat start session`. Při nálezu jen vypíše
`[ontologie] …` do kontextu. Tvrdé vynucení týchž kontrol dělá až brána `review.linters`
při `/review-spec` (`spec-config.yaml:47-49`) — komentář na `:11` to říká explicitně.
Je to **vědomý kompromis** (rychlost startu vs. tvrdost), ne opomenutí.

**Přenositelná zásada.** Levná neblokující kontrola konzistence při každém startu práce
odchytí drift dřív než drahá zpětná rekonstrukce — ale **neblokující kontrola nikdy
nenahradí tvrdou bránu** tam, kde na chybě něco závisí. Mít obě, každou na svém místě.

**Předvedatelnost.** `/clear` v repu a ukázat hlášku `[ontologie] …`; nebo ručně
`python docs/ontology/.ontology-tools/session-check.py` + `echo %ERRORLEVEL%` → 0 i při nálezu.

### 10.2 PreToolUse spec-guard — `guard.protect_list`

**Co to je.** Spouštěč, který se aktivuje **těsně předtím**, než jakýkoli automatický agent
(ne hlavní konverzace s člověkem) zapíše nebo upraví soubor. Zeptá se „smí tenhle typ
agenta psát sem?" a pokud ne, zápis **zablokuje ještě předtím, než k němu dojde**.

**Kde je co.** Registrace hooku **není v repozitáři** — je v pluginu:
`…\plugins\cache\kvados-plugins\spec-factory\1.9.0\hooks\hooks.json:3-13`, event
`PreToolUse`, matcher `"Write|Edit|NotebookEdit"`. **Co je chráněno** je naopak
per-projekt: `.claude\spec-config.yaml:53-56`, sekce `guard.protect_list` — AlzaSk přidává
`.gitlab/CODEOWNERS` a **`docs/ontology/*`** k jádrovému seznamu pluginu
(`CLAUDE.md`, `.claude/*`, `spec-config.yaml`).

**Rozhodovací logika** (`spec_guard_core.py`, funkce `decide()`):
1. Vstup: `agent_type` (kdo píše) + `tool_input.file_path` (kam).
2. `agent_type` chybí nebo je `"claude"` (hlavní/lidská session) → **žádná kontrola**,
   píše volně (`:118-120`).
3. Jinak (automatický subagent) dvě vrstvy:
   - **VRSTVA 1 PROTECT** (`protect_list` + automaticky odvozené `docs/adr/*`, `docs/fr/*`,
     `docs/analysis/*` z `governance.*` a grounding packu — `:92-106`) → **blok pro všechny
     automatické agenty**, bez ohledu na typ.
   - **VRSTVA 2 ALLOW** (workspace `spec/*` z `workspace.base_path`) → psát smí jen agenti
     typu začínajícího `"spec-"` (`:136-141`); ostatní ne (`:144-147`).
4. Blok = exit 2 + JSON `{"decision":"block","reason":…}` (`spec-guard.py:53-55`).

**Zdokumentovaný záměrný limit.** Guard kryje **jen** `Write|Edit|NotebookEdit` — agent
s přímým Bash přístupem jím neprojde. Je to napsané přímo v kódu
(`spec_guard_core.py:20-25`): „**guard je mantinel, ne bezpečnostní perimetr**".
Selhání jádra guardu (např. chybějící PyYAML) je fail-**open** pro lidskou session
a fail-**closed** pro automatické agenty (`spec-guard.py:46-51`).

**Přenositelná zásada.** Hranice zápisu, na které závisí integrita sdíleného zdroje pravdy,
nemá spoléhat na paměť nebo domluvu („agent si to bude pamatovat") — má být **automaticky
vynucená bránou před zápisem**, s explicitní výjimkou pro člověka, který smí rozhodnout.
A **napiš do nástroje, co nekryje** („mantinel, ne perimetr"), ať si nikdo nemyslí opak.

**ANTIPATTERN / riziko.** Guard vypadá jako projektová governance, ale **žije z části mimo
repozitář** (`~/.claude/plugins/`). Kdyby plugin nebyl nainstalován nebo aktualizován,
ochrana `docs/ontology/*` nefunguje, i když je v `spec-config.yaml` nakonfigurovaná.

---

## 11. `docs\adr\` — governance napojená na myFABER

**Co to je (pro publikum).** ADR = zápis architektonického rozhodnutí: „rozhodli jsme se
X, protože Y; zvažovali jsme Z a zamítli kvůli W". `INDEX.md` je přehledová tabulka nad
všemi zápisy.

### 11.1 INDEX jako status-dashboard

**Čísla** (`INDEX.md:9-30`): celkem **51** ADR — Aktivních **26**, Override **1**,
Navržených **24**, Nahrazených **0**. Šest kategorií: DB (3), API (16), INT (3, kurátor
Martin Tomis), PROC (20), HW (8), OVR (1).

**Struktura** (`INDEX.md:34-107`): čtyři sekce — Aktivní (Accepted) `:38-66`, Override
`:67-71`, Navržená (draft/proposed) `:73-101`, Nahrazená `:102-106` (**prázdná**).
Každý řádek: ID (odkaz na soubor), Název, Kategorie/Autor/Typ, Datum, Komponenty.

**Sekce „Závislosti na myFABER"** (`INDEX.md:110-123`): tabulka `related_to` vazeb na
globální ADR (`ADR-MF-PROC-001`…`-006`, `ADR-MF-API-001`) — ukazuje, kde lokální
rozhodnutí navazují na sdílenou platformu.

**Changelog** (`INDEX.md:126-256`, append-only, nejnovější dole dle `RULE-CL-001`) +
„Historie revizí" (`:257-263`).

**Přenositelná zásada.** Status v přehledovém indexu se nikdy neudržuje odhadem — musí
přesně odpovídat poli `status:` ve frontmatteru zdrojového dokumentu, jinak index lže.
Doklad, že i to zaostává: changelog `:218` (záznam 3.2) — „Audit: doplněna chybějící ADR
do indexu — OVR-001… a PROC-008…".

### 11.2 `.adr-tools\` — tenký wrapper, logika je centrálně

`config.yaml`: absolutní cesty k oběma repozitářům (`myfaber_adr: C:\Git\myfaber\Docs\adr`,
`alzask_adr: C:\Git\alzask\docs\adr`), cesta k jádrovému schématu (v myFABER), prahy
stárnutí (`proposed_max_days: 14`, `draft_max_days: 30`, `audit_interval_days: 90`),
ignore-list.

`validate.cmd` **nemá žádnou vlastní validační logiku**: ověří existenci
`C:\Git\myfaber\Docs\adr\.adr-tools\validate.py` (`:9-13`, s chybovou hláškou, když
myFABER repo chybí) a zavolá `python "%MYFABER_VALIDATE%" --config "%CONFIG%"
--project all %*` (`:15`). Veškerá logika (schéma, kontroly frontmatteru) žije **výhradně
v myFABER**.

**Přenositelná zásada.** Sdílené nástroje a schéma patří na jedno centrální místo (jeden
zdroj pravdy pro logiku); projektová data a jejich konfigurace (cesty, prahy) zůstávají
u projektu. Projekt na centrální nástroj **ukazuje, nekopíruje ho**.

### 11.3 Override — odchylka od standardu se nikdy nedělá mlčky

**Co to je.** Platforma (myFABER) předepíše obecné řešení pro všechny zákazníky; konkrétní
projekt někdy potřebuje jiné. Override ADR je zápis „vědomě se odchylujeme, a tady je
proč" — odchylka je zdokumentovaná a viditelná na obou stranách.

**Příklad** `docs\adr\override\ADR-ASK-OVR-001.md`: přepisuje `ADR-MF-PROC-003` (globálně
patří periodické zásobování stanice pod `StationService`); AlzaSk rozhodla, že
`PeriodicSupplyService` bude samostatná top-level komponenta, protože logika zásobování je
výrazně komplexnější než typický WES scénář (`:44-50`).

**Klíčová pole:** `overrides: ADR-MF-PROC-003` (`:18`), `override_type: extension` (`:19`;
z trojice `extension | replacement | restriction`), sekce Kontext (`:40-50`) vysvětluje
nutnost, sekce Rizika (`:101-106`) počítá s budoucí změnou globálního ADR a řeší ji
**novým override ADR, ne tichou úpravou**. Status je `draft` (`:4`), reviewery
`approved: pending` (`:9-13`) — **i override čeká na schválení**, není platný jen tím, že
je zapsaný. Vznik: potřeba ze schůzky 2026-02-23 (`:130`).

**Přenositelná zásada.** Lokální odchylka od sdíleného standardu se nikdy neprovádí mlčky —
zapisuje se jako explicitní prohledatelný záznam s odkazem zpět na to, co přepisuje, a
s důvodem, proč obecné pravidlo nestačí. (A z předchozí sekce: **musí být doložená z obou
stran**, jinak neplatí — `BUILD-LOG.md:253-255`.)

### 11.4 ANTIPATTERNY z changelogu — dvě kolize ID

Ručně přidělovaná sekvenční čísla + paralelní práce = kolize. Dvakrát doloženo:

**a) Kolize `PROC-015`/`-016`** (`INDEX.md:156, 232-233`): commit `27b1060` zapsal novou
metodiku pod **už obsazené** ID `-015` (patřilo „WES-autonomní containerRemoved", kurátor
Natálie Rašková) a **přepsal tím obsah existujícího souboru**. Týž commit navíc vrátil
starší verzí změny v pěti dalších ADR a obou INDEXech. Náprava: `-015` obnoveno, nová
metodika přečíslována na `-016`.

**b) Kolize `PROC-018`** (`INDEX.md:252`, changelog 6.6): dvě nesouvisející rozhodnutí
(expirace replenish objednávek vs. koordinace inbound/outbound na mezaninu) obsadila stejné
ID nezávisle na dvou větvích a kolidovala při merge do `main`.
**Pravidlo řešení:** ID si nechává rozhodnutí publikované na `main`, druhé se přečísluje
**beze změny obsahu**.

→ *Zásada:* ručně přidělovaná sekvenční ID jsou při paralelní práci více lidí/větví
spolehlivý zdroj kolizí. Buď generuj ID, nebo měj **předem napsané pravidlo, kdo si ID
nechá** — tady existuje a bylo použito opakovaně.

**Poznámka.** Sekce „Nahrazená (Superseded/Deprecated)" je prázdná (`INDEX.md:102-106`,
`Nahrazených: 0`) — mechanismus supersedování **nebyl v praxi ještě ani jednou vyzkoušen**.

---

# Kandidáti na náměty workshopu

Taxonomie okruhů: **K** kontext a grounding · **R** rozšíření (skills/commands/subagenti/
hooks) · **M** mechanika kvality (brány, validátory, lintery) · **A** analytické postupy ·
**X** antipatterny.

Sloupec **Demo** = jak silná je ukázka naživo: ★★★ spustitelné za 30 s s viditelným
výsledkem · ★★ ukázat soubory vedle sebe · ★ jen výklad.

## Nosné náměty (silné demo + široká přenositelnost)

| # | Okruh | Námět (přenositelná zásada) | Zdroj | Demo |
|---|---|---|---|---|
| 1 | **M** | **Brána, ne prompt.** Kontrolu, kterou umí skript, nikdy nepiš jako věty do promptu. V projektu má vlastní pravidlo `RULE-GOV-002`. | 2.4, ADR-ASK-PROC-020 | ★★★ |
| 2 | **M** | **Dva exit kódy = dva různé signály.** „Evidence je poškozená" (blokuje, exit 2) vs. „je tu otevřená práce" (jen upozorní, exit 1). Bez toho buď zablokuješ proces kvůli běžnému čekání, nebo si zvykneš ignorovat i chyby. | 3.5 | ★★★ `questions.py --check` → 0 invariantů, 102 nálezů |
| 3 | **K** | **Cituj obsah, ne pozici.** `soubor:řádek` tiše ukáže cizí text, jak dokument roste. Otisk obsahu (hash okna) přežije posun a **správně selže** při skutečné změně. Změřeno: 86 % → 95 % → **99 %** jednoznačnosti podle šířky okna. | 2.3 | ★★★ `cite.py <soubor:řádek>` → OK/POSUN/ZMIZELA |
| 4 | **M** | **POSUN je oprava, ZMIZELA je rozhodnutí.** „Kdo opraví ZMIZELOU citaci přepsáním čísla řádku, vyrobí horší stav než zastaralý: tvar sedí, obsah lže." Rozliš mechanickou opravu od té, která patří člověku. | 2.3, `RULE-ONT-003` | ★★ |
| 5 | **K** | **Zdroj pravdy vs. generovaný derivát.** Jeden editovatelný zdroj + generovaná čitelná vrstva. Varování „GENEROVANO — needituj" patří **do generovaného souboru**, ne jen do README. Model čte deriváty, protože zdroj je moc velký. | 2.2, 3.6 | ★★★ `build.cmd --check` → AKTUALNI / hash |
| 6 | **M** | **Deterministická kontrola vs. sémantická.** Rozděl na „ověřitelné bez porozumění" (čísla, odkazy, formát → linter) a „vyžaduje porozumění" (souhlasí popis s diagramem → LLM/člověk). Nikdy nenech druhé předstírat, že to dělá první. | 4.2, 7.1 | ★★★ `WORD`→`INT` → `[ERROR] B14`, exit 2 |
| 7 | **A** | **Eviduj, co v odpovědi CHYBÍ**, ne jen co přišlo. „Devět dní se to vedlo jako 'chybí hodnoty'" — dokud si někdo neotevřel přílohu, kde ta čísla byla. Bez věty „co konkrétně chybí" nelze zformulovat doptání. | 3.3 | ★★★ `ISS-004` + screenshot |
| 8 | **A** | **Stabilní ID se nikdy nepřečísluje ani nerecykluje** — ani u dotazů dodavateli (odkazuje na ně druhá strana), ani u testovacích scénářů (drží řetěz FR→TC→C# test). **Mezera v číslování je levná, přečíslování zneplatní všechny odkazy naráz.** | 1.4, 3.2 | ★★ |
| 9 | **X** | **Iluze pokrytí je horší než jeho absence.** TC generované z FR pro neimplementované služby „vytváří iluzi otestovanosti" → 22 souborů smazáno. Generuj testovací artefakty jen proti **stabilnímu kontraktu**. | 1.9, ADR-ASK-PROC-009 | ★★★ prázdný `find comp/wes -name "*.feature"` |
| 10 | **X** | **Konvence bez validátoru se rozpadne.** Tři nezávislé doklady v jednom repu: `T24_PREHLED-…` (jiné pojmenování), `docs/fr/proces/` (nezdokumentovaný adresář + koncová pomlčka v názvu), šablona FR bez `status:` a bez `Historie revizí` (a je v ignore listu). | 1.10a, 5.2 | ★★★ `schema.yaml:4-11` vs. `head -8 FR-template.md` |

## Silné náměty

| # | Okruh | Námět | Zdroj | Demo |
|---|---|---|---|---|
| 11 | **R** | **Dvě vrstvy dokumentace podle čtenáře.** 1 201řádková metodika pro člověka na vyžádání + 69řádkový checklist toho, co se nesmí zvorat, ve vždy načteném kontextu. Z krátkého ukazuj na dlouhé, neduplikuj. | 1.1 | ★★ |
| 12 | **R** | **Levná neblokující kontrola na startu práce** (`SessionStart`, vždy exit 0) odchytí drift dřív než drahá rekonstrukce — ale **nikdy nenahradí tvrdou bránu** tam, kde na chybě něco závisí. Mít obě, každou na svém místě. | 10.1 | ★★★ `/clear` → `[ontologie] …` |
| 13 | **R** | **Hranici zápisu vynuť bránou, ne domluvou.** Guard před zápisem: hlavní session píše volně, automatický agent do governance zón nesmí. A **napiš do nástroje, co nekryje** — „guard je mantinel, ne bezpečnostní perimetr". | 10.2 | ★★ |
| 14 | **R** | **Review rozděl podle nákladu a rizika.** Levný mechanický filtr (haiku) → drahé sémantické posouzení (sonnet/opus) → auto-fix jen tam, kde nejde o spor autorit. **Právo zapisovat má jedna role z pěti.** Doloženo ~80 % úsporou. | 7.1 | ★★★ `/review-docs <oblast>` |
| 15 | **M** | **Automaticky oprav vše jednoznačné, člověku předlož jen skutečná rozhodnutí.** Report zaplavený mechanickými nálezy se přestane čítat — proto do `REVIEW-REPORT.md` jdou **výhradně** ARCH-DECISION nálezy. | 7.2 | ★★ |
| 16 | **M** | **Práh, který realita trvale překračuje, přestává být signálem.** 23 FR v draftu 55–201 dní při prahu 30 → 56 warningů, mezi nimiž se ztratí 2 skutečné errory. Buď zvedni práh, nebo změň úroveň závažnosti. | 1.3 | ★★★ `validate.py` → najdi 2 errory v 56 warningech |
| 17 | **A** | **Hierarchie autority zdrojů rozhoduje spor — ne datum, ne přesvědčivost textu.** Sedm vrstev; novější PLC spec prohrála s daty nasazení. A **rozpor uvnitř téže vrstvy je nejhorší**, protože „implementátor si vybere tu, kterou přečte první". | 2.6b/h, 7.1 | ★★ |
| 18 | **X** | **Hotový artefakt, na který nic neukazuje, je mrtvý.** Registr „stojí vedle práce, ne v ní: `grep -ri "ontolog"` nad `CLAUDE.md` a `.claude/` vrací 0 výskytů" — a měřením 79 % citací by se rozjelo za 30 dní. Zapojení do workflow je samostatná práce. | 2.1 | ★★★ ten grep naživo |
| 19 | **M** | **Vykazuj, kolik jsi toho NEZKONTROLOVAL.** Brána G4 + součtová pojistka `2558 = 1278 kontrolováno + 0 bez kotvy + 661 mimo kontrolu + 619 opakovaných` — aby „nic jsem nenašel" nebylo k nerozeznání od „nic jsem neměřil". | 2.3, 2.4 | ★★★ `reanchor.py --check` |
| 20 | **A** | **Deprecated s migrační cestou, ne zákaz naráz.** Starý tvar zůstane jako warning („aby migrace mohla probíhat postupně"), migruje se při běžné práci na souboru — ne zvláštní kampaní. | 1.5 | ★★ `tc-schema.yaml:11-15` |
| 21 | **A** | **Atribut patří na tu úroveň granularity, na které se skutečně mění.** Status per soubor u souboru s 12 scénáři nese nulovou informaci → status a datum jsou per scénář. | 1.5 | ★★ `tc-list.csv` |
| 22 | **X** | **Schéma se neopisuje.** Dvě nezávisle vzniklá znění téhož pravidla v jednom repu (TC „žádná replikace schématu" + registr „SCHÉMA SE NEOPISUJE") — opsaná struktura je druhá pravda, která zastará dřív než originál. | 1.7, 2.6a | ★★★ SPRÁVNĚ/ŠPATNĚ blok `README.md:498-528` |

## Doplňkové náměty

| # | Okruh | Námět | Zdroj | Demo |
|---|---|---|---|---|
| 23 | **X** | **Nástroj kontroluje jen to, co pozná.** Tučně značená UDT tabulka místo nadpisu tiše vypne celou třídu kontrol — a přesně tak unikla chyba `STRING[40]` = 40 B místo 42 B. Zdokumentuj to jako známé omezení. | 4.4a | ★★★ linter na mezaninovou spec = ticho |
| 24 | **M** | **Brána musí rozlišit „čekáme na externí vstup" od „chyba"** (placeholder `PLC511–516` = WARN, ne ERROR) — jinak si autoři zvyknou bránu obcházet. | 4.4b | ★★ |
| 25 | **A** | **Publikum určuje, co smí být odkaz.** Spec pro externího dodavatele musí být sebe-nosná. A pokud to není vynucené branou, pomalu se to poruší — v produkční spec jsou 2 odkazy na interní ADR, které prošly reviewem. | 4.3 | ★★★ `grep "ADR-ASK\|FR-COMP"` → 2 řádky |
| 26 | **A** | **Tři typy artefaktu, tři publika:** normativní požadavek (FR) / technický test (TC) / naratívní walkthrough (SCE). Nemíchat. A walkthrough potřebuje **strojově čitelné odkazy na dvou úrovních** (dokument + každý krok), jinak je to jen volný text. | 6.1, 6.2 | ★★ |
| 27 | **A** | **Živý dokument vs. zmražený otisk** mají jiná pravidla úprav; předávaná verze nese vlastní „od-do" deltu v hlavičce, aby čtenář nemusel dělat diff. | 5.1, 5.3 | ★★ |
| 28 | **A** | **Mluv jazykem domény, ne implementace — a veď uzavřený registr formulací** (34 doménových kroků). Bez registru vzniknou tři způsoby, jak napsat totéž, a nic se nedá vyhledat. | 1.6 | ★★ |
| 29 | **R** | **Uložený pojmenovaný postup místo opakovaného promptu** — zvlášť u kroků, které se snadno opomenou („vždy otevři přílohy" je součást postupu, ne rada). 8 commandů, 2 skills. | 8, 9 | ★★★ `/dodavatele:stav` |
| 30 | **K** | **Skill nemá obsahovat znalost, ale navigaci ke znalosti + příkaz, který ji ověří.** U příliš velké báze: malý rejstřík + nástroj na ověření citace, ne slepá věra číslu řádku. | 9.2 | ★★ |
| 31 | **M** | **Smyčka „oprav → znovu zvaliduj → znovu zkontroluj" s pevným limitem iterací** (max 3×) je lepší než jednorázový průchod i než nekonečné dolaďování. | 7.3 | ★★ |
| 32 | **M** | **Kontrolní součet na konci strukturovaného dokumentu** (UDT „Celkem" = součet polí) zachytí „utekla mi číslice" dřív než implementátor. A **kontroluj dvěma nezávislými cestami** — changelog se validuje podle verze i podle data. | 4.1d, 1.3 | ★★★ smazat pole, nechat „Celkem" → `[ERROR] B4` |
| 33 | **A** | **Pravidlo, které vzniklo z jednoho reálného nálezu, je nejsilnější kandidát na zápis do linteru** — `BYTE[7]`→`BYTE[8]` po skutečné chybě zarovnání. Nejlevnější způsob, jak se táž chyba nestane podruhé. | 4.1b | ★★ |
| 34 | **X** | **Ručně přidělovaná sekvenční ID při paralelní práci kolidují.** Dvakrát doloženo: přepsaný obsah cizího ADR pod obsazeným ID; kolize dvou větví při merge. Buď generuj ID, nebo měj předem napsané pravidlo, kdo si ID nechá. | 11.4 | ★★ changelog `INDEX.md:232,252` |
| 35 | **X** | **Přesouvej nástrojem, ne rukou.** Kde je závazný odkaz cesta→soubor, ruční přesun rozjede registr a filesystem. A cíl se nikdy nepřepisuje — pod jménem „V1.6" jsou v repu **dva různé soubory**. | 3.4 | ★★★ inbox → `--check` → `--archive` → `--check` |
| 36 | **X** | **Mechanismus, který nikdy neproběhl, není odzkoušený.** Supersedování ADR: 0 případů z 51. A na platformové úrovni 0 accepted z 25 ADR — „schvalovací kolečko neproběhlo ani jednou". | 2.6d, 11.4 | ★ |
| 37 | **X** | **Governance, která žije mimo repozitář, může zmizet.** Guard chránící `docs/ontology/*` je konfigurovaný v repu, ale registrovaný v pluginu v `~/.claude/plugins/` — bez pluginu ochrana nefunguje. | 10.2 | ★ |
| 38 | **X** | **Nástroj odkazující na neexistující nástroj.** `export_tc.py` instruuje spustit `generate_descriptions.py`, který v `.fr-tools/` není — zůstala jen cache, kterou nikdo neumí přegenerovat. | 1.8 | ★★ |
| 39 | **A** | **Číselník stavů zjednodušuj, dokud každá hodnota nemá rozhodovací důsledek.** TC statusy 4→2 (`draft`/`done`); u dodavatelů naopak volný text ve stavu (13 hodnot) rozpadl celou evidenci. | 1.10e, 3.3 | ★★ |
| 40 | **A** | **Žurnál rozhodnutí je artefakt k udržování.** `BUILD-LOG.md` (dávky D1–D13) drží devět pojmenovaných antipatternů — bez něj by se poučení z dávky D4 v D9 zopakovalo. | 2.6 | ★★ |
| 41 | **M** | **Podmíněná povinnost ve schématu.** `status: blocked` ⟹ povinné `blocked_by` + `blocked_reason`. Třináct řádků YAML, které zabrání nejčastější formě mrtvého záznamu: stavu bez příčiny. | 1.2 | ★★ `schema.yaml:48-53` |
| 42 | **A** | **Registr (INDEX) zakládej až nad prahem, ne preventivně** — pro 2 scénáře stačí tabulka v README, pro 51 ADR už ne. Práh je v projektu explicitně napsaný (~10 položek). | 6.3, kořenový `CLAUDE.md` | ★ |
| 43 | **A** | **Odděl surový podklad od hotového výstupu pro čtenáře mimo tým** už adresářovou strukturou + explicitní tabulkou „předává se / nepředává se" (dvojí changelog: interní vs. zákaznický). | 5.4 | ★★ |
| 44 | **X** | **Praxe uteče metodice, a nikdo si toho nevšimne.** Sloučené snapshoty `T25+T26`, `T27+28+29` nejsou v README, `tc-katalog/` z něj nezmizel, ačkoli v praxi zanikl; README needitováno od 6/2026, snapshoty jsou z 8/2026. | 5.4, 5.5 | ★★ |
| 45 | **A** | **Rozliš „zdroj tvrdí dvě různé věci" (rozpor) od „zdroj přiznává nejistotu" (otevřená otázka)** — `TODO` v dokumentu pro dodavatele není rozpor a nepatří do konfliktů. | 2.6f | ★ |
| 46 | **A** | **Stejné slovo statusu má v různých typech dokumentů opačný důsledek.** Draft ADR nikoho nezavazuje; **draft FR se implementuje** (33 ze 47, včetně kanonického vlastníka modelu portu). Ověř, nepředpokládej. | 2.6c | ★★ |
| 47 | **A** | **Měř nejen „přišla odpověď", ale „je odpověď použitá".** 58 ze 164 dotazů má odpověď, která se nepropsala do specifikace — největší otevřená položka leží na naší straně, ne u dodavatele. | 3.7 | ★★★ `questions.py --stats` |
| 48 | **A** | **Mlčení dokládej strukturou, ne zápisem.** Když mail vyjmenuje otázky, které měl řešit, a některá nemá `answered_on`, je „přeskočený bod" **dopočítaný** — žádné nové pole netřeba. | 3.7 | ★★ |
| 49 | **A** | **Lokální odchylka od sdíleného standardu nikdy mlčky** — override ADR s odkazem zpět (`overrides:`, `override_type: extension\|replacement\|restriction`). A **musí být doložená z obou stran**, jinak neplatí ani jednosměrně. | 11.3, 2.6e | ★★ |
| 50 | **R** | **Sdílený nástroj centrálně, projektová data lokálně.** `validate.cmd` v projektu je tenký wrapper bez vlastní logiky; validátor i schéma žijí v platformovém repu. Projekt na nástroj **ukazuje, nekopíruje ho**. | 11.2 | ★★ |

## Návrh tří nejsilnějších bloků pro 90minutový workshop

**Blok A — „Brána, ne prompt" (M, ~25 min).** Otevři `validate.py` naživo → 2 errory
v 56 warningech (námět 16 hned vedle 1). Pak `WORD`→`INT` v PLC spec → `[ERROR] B14`,
exit 2 (6). Uzavři dvěma exit kódy u dodavatelů (2). Odnos: *kontrolu, kterou umí skript,
nikdy nepiš jako věty do promptu — a odděl „poškozeno" od „nedokončeno".*

**Blok B — „Citace, která nelže" (K, ~25 min).** Ukaž problém citátem
(`README.md:147-151`: „horší než chyba: tiše ukáže cizí text"), pak `cite.py` živě na tři
verdikty (3), pak G4 + součtovou pojistku (19). Uzavři zdrojem pravdy vs. derivátem (5).
Odnos: *cituj obsah, ne pozici — a vykazuj, co jsi nezkontroloval.*

**Blok C — „Co se neosvědčilo" (X, ~25 min).** ADR-ASK-PROC-009 a iluze pokrytí (9),
tři doklady rozpadlé konvence bez validátoru (10), mez linteru u tučných tabulek (23),
kolize ručně přidělovaných ID (34). Odnos: *artefakt z odhadu je iluze, ne pokrytí; a co
nekontroluje skript, to se rozejde — včetně tvé vlastní šablony.*

Zbytek (R + A náměty) je materiál na druhou půli nebo samostatné pokračování.

---

## Poznámka k metodě a rozsahu

- Zmapováno všech 11 zadaných oblastí; čteno **jen** v `C:\Git\alzask` mimo `temp/`,
  do repozitáře nebylo nic zapsáno.
- Živě spuštěno a ověřeno: `validate.py`, `validate.py --tc`, `questions.py --check`
  a `--stats`, `build.cmd --check`, `audit.py --quiet`, `cite.py`, `reanchor.py --check`,
  `plc-lint.py` (produkční i mezaninová spec).
- Čísla v souboru jsou stav k **2026-08-26** (dokumenty se mění; u počtů FR/TC/ADR/entit
  ověř před workshopem znovu).
- Nesoulady mezi dokumentací a realitou jsou zapsané jako nálezy (drift), ne jako chyba
  autora — pro workshop jsou to nejcennější doklady, protože ukazují **co se stane bez
  brány**.
