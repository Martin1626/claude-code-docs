# FÁZE 0 — inventura existujícího materiálu pro workshop Claude Code pro analytiky

Datum: 2026-08-26. Rozsah: přesně soubory/adresáře zadané v úkolu, nic navíc (Epistema,
OpenClaw a další projekty mimo scope nejsou zmiňovány). Zápisová zóna: pouze `C:\tmp\workshop-namety\`.

---

## A) `C:\Git\shared\docs\claude-code\claude-code-jak-funguje.html`

**Co to je:** Jednostránková interaktivní prezentace/slide-deck (12 slidů, klávesová navigace
šipkami/mezerníkem, progress bar `1/12`) vysvětlující **fundamentální mechaniku Claude Code**
— ne AlzaSk-specifický obsah, ne postupy. Autor zjevně Martin Tomis (styl odpovídá ostatním
materiálům).

**Pro koho:** Netechnický až mírně technický čtenář, který chce pochopit "proč nástroj, co umí
jen psát text, dokáže spouštět příkazy a editovat soubory" (slide 1, `claude-code-jak-funguje.html`
řádky s H1 "Jak funguje Claude Code"). Cílovka = přesně profil analytika bez SW inženýrského
backgroundu.

**Jazyk:** Výrazně laický, s metaforami ("automat na text", "model je mozek bez rukou, harness
jsou ruce"), krátké věty, žádný žargon bez vysvětlení. Číselné demo prvky (token counter,
teplota, cache) naznačují interaktivní/animovaný JS overlay nad statickým textem.

**Struktura (12 slidů dle H1–H3 nadpisů):**
1. Úvod — model je jen f(text)→text
2. Model je bezstavová funkce (žádná paměť mezi voláními)
3. Tokeny — jednotka měření textu (ČJ diakritika = víc tokenů)
4. Text vzniká token po tokenu (autoregrese, smyčka "napiš → přečti → napiš")
5. Proč stejný vstup nedá stejný výstup (teplota, sampling, batching na GPU)
6. Kontext — jediné, co model vidí (kontextové okno, dnes 1M tokenů)
7. Prompt caching (cena 10 %/100 %/+25 %/+100 % dle cache hit/write)
8. Kompaktace (co se stane, když dojde místo v kontextu)
9. Od modelu k agentovi (model vs. harness)
10. Nástroje — tool_use / tool_result jako strukturovaný JSON kontrakt
11. Agentní smyčka (6 kroků: harness→model, model odpoví, harness provede, výsledek zpět,
    model rozhodne, opakuj)
12. Shrnutí — "hloupá funkce + chytrá smyčka = agent"

**Použitelnost jako podklad workshopu:** **Použitelné rovnou** jako modul "jak Claude Code
funguje pod kapotou" — pokrývá přesně tu vrstvu (model/token/kontext/cache/agentní smyčka),
kterou by jinak workshop musel budovat od nuly. Design je hotový, jen je potřeba ověřit, zda
interaktivní JS prvky (počítadla, replay smyčky) fungují offline/v prostředí workshopu.

**Zastaralost:** Kontextové okno "až 1 milion tokenů" (slide 6) — aktuální k datu tvorby;
ověřit při použití, zda platí i pro model/verzi používanou na workshopu. Jinak obsah je
fundamentální/model-agnostický, nízké riziko zastarání.

---

## B) `C:\Git\shared\plugins\docs\ADOPTION-ALZA.md`

**Co to je:** Interní rozhodovací dokument (gain/loss bilance) pro adopci sdíleného pluginu
Spec Factory v repozitáři AlzaSk. Ne workshop materiál — je to procesní/architektonická
dokumentace k jedné konkrétní migraci.

**Pro koho:** Autor pro sebe/tým (Martin Tomis + Claude), ne pro analytiky. Interní.

**Jazyk:** Vysoce technický, plný zkratek a interních referencí (REQ-S7-008, DR2-13, GATE-2,
RULE-GOV-001, spec-schema.yaml…) — nesrozumitelné bez znalosti kontextu Spec Factory.

**Struktura:** 1. Bilance (Gain/Loss tabulky), 2. Adopční kroky, 3. Výjimka guardu, 4. Brány.

**Použitelnost jako podklad workshopu:** **Nepoužitelné** přímo pro analytiky — příliš
technické a úzce zaměřené na jeden interní refaktoring. Může sloužit nanejvýš jako pozadí
pro školitele, ne jako výukový materiál.

**Zastaralost — NALEZENO:** Hlavička (`ADOPTION-ALZA.md:7`) uvádí **„Stav: NÁVRH —
neprovedeno"** a „Cross-repo zápis do `c:\Git\alzask` vyžaduje souhlas… (brána E2)". Ale
tělo dokumentu (`ADOPTION-ALZA.md:31`) už referuje **„Provedeno v Alza repo 2026-07-07
(commit `8e2e927`…)"** — tj. hlavička je nekonzistentní s vlastním obsahem dokumentu.
Navíc dle runbooku (viz níže) a dle projektové paměti (`project_spec_factory_knowledge_loop.md`
— „od 2026-07-07 VÝHRADNĚ plugin spec-factory 1.5.1") byla adopce **dokončena**, takže
status „NÁVRH — neprovedeno" v hlavičce je zastaralý.

---

## C) `C:\Git\shared\plugins\docs\ADOPTION-ALZA-RUNBOOK.md`

**Co to je:** Krokový runbook (A0–A8) pro provedení té samé adopce Spec Factory — přesné
kroky, gates, rollback tabulka. Datováno 2026-07-07.

**Pro koho:** Prováděcí dokument pro toho, kdo dělá migraci (Martin Tomis + Claude session).
Ne pro analytiky.

**Jazyk:** Silně technický (git příkazy, YAML config diffy, JSON hook probe skript).

**Struktura:** Prerekvizity → A0 větev → A1 config → A2 manifest fix → A3 šablona → A4 slug
rekonciliace → A5 instalace + diagnostika guardu → A6 cutover → A7 přesměrování orchestrátoru
→ A8 ověření end-to-end → Rollback tabulka → Pořadí závislostí.

**Použitelnost jako podklad workshopu:** **Nepoužitelné** pro analytiky přímo. Cenné leda
jako ukázka „jak vypadá disciplinovaná migrace s bránami a rollbackem" pro pokročilejší
publikum (ne cílovka analytik).

**Zastaralost:** Runbook je popsán jako aktuální k 2026-07-07 a „ověřený proti reálnému stavu
obou repozitářů". Podle stopy v paměti (`project_spec_factory_knowledge_loop.md`) proběhl
cutover úspěšně — runbook samotný tedy odpovídá historickému kroku, který už je hotový;
nejde o chybu dokumentu, ale o dokument, který **už splnil svůj účel** (čistě archivní hodnota).

---

## D) `C:\Git\shared\plugins\README.md`

**Co to je:** Popis sdíleného marketplace pluginů `C:\Git\shared` — dva pluginy:
`spec-factory` (tvorba specifikací) a `knowledge-loop` (znalostní smyčka). Instalační návod,
struktura repozitáře, dvouvrstvý guard (PROTECT/ALLOW), testy, správa/schvalování.

**Pro koho:** Vývojáři/analytici, kteří instalují nebo spravují tyto pluginy napříč projekty.
Obecnější publikum než A a C výše, ale pořád spíš technicky zdatný uživatel Claude Code.

**Jazyk:** Technický, ale strukturovaný a čitelný — vysvětluje pojmy (`$CLAUDE_PLUGIN_ROOT` vs.
`$CLAUDE_PROJECT_DIR`, config seam, guard vrstvy) v odstavcích, ne jen v kódu.

**Struktura:** Instalace → Struktura (strom souborů) → Nastavení (plugin vs. projekt) →
Dvouvrstvý guard → Testy → Správa a schvalování.

**Použitelnost jako podklad workshopu:** **Potřebuje přepis/výtah**, pokud by workshop chtěl
ukázat "jak fungují sdílené pluginy" obecně (marketplace koncept, guard, instalace) —
konkrétní obsah (spec-factory vnitřnosti) je nad rámec typického analytika, ale koncept
"co je plugin a jak se instaluje" je přenositelný a dobře formulovaný.

**Zastaralost:** `plugins/README.md:26–28` upozorňuje na "port 8443 vs. 443" pro GitLab —
provozní detail, platnost nelze ověřit bez přístupu ke GitLab konfiguraci; nekontroverzní,
neoznačuji jako zastaralé.

---

## E) `C:\Git\shared\.gitlab\CODEOWNERS`

**Co to je:** GitLab CODEOWNERS soubor — vynucuje MR schválení vlastníky (`@martint`,
`@pavelny`) pro citlivé části pluginů (agents/, tools/, hooks/, manifesty).

**Pro koho:** GitLab CI/governance mechanismus, ne dokument pro lidi.

**Jazyk:** Čistě konfigurační (cesty + accounty), s krátkým komentářem nahoře vysvětlujícím
princip "boundary-change vyžaduje MR se schválením".

**Struktura:** Sekce "Celé pluginy (fallback)" → "Citlivé podadresáře" → "Manifesty marketplace".

**Použitelnost jako podklad workshopu:** **Nepoužitelné** jako přímý workshop obsah (je to
konfigurační soubor), ale **dobrý konkrétní příklad** governance principu „agent navrhuje,
promuje jen člověk" (RULE-GOV-001) — může posloužit jako jednořádková ilustrace v modulu o
governance, ne jako samostatný materiál.

**Zastaralost:** Komentář `CODEOWNERS:1` odkazuje na „(C:\Git\shared)" a řádek v
`plugins/README.md:12` říká „Účty v CODEOWNERS (zatím zástupné)" — tj. sám autor označuje
účty jako dočasné/placeholder. Aktuální stav nelze ověřit bez GitLab dotazu.

---

## F) `C:\Git\shared\.githooks\` (4 soubory)

**Co to je:** Git hooks vynucující konvence commit zpráv a formát souborů.

| Soubor | Co dělá |
|---|---|
| `commit-msg` (shell shim) | Volá `commit-msg.ps1` přes PowerShell |
| `commit-msg.ps1` | Kontroluje prefix commit zprávy (`feat/fix/docs/style/refactor/test/merge/trace:`), auto-doplní mezeru za dvojtečkou, lowercase prefix, min. délka zprávy 10 znaků |
| `pre-commit` (shell shim) | Volá `pre-commit.ps1` přes PowerShell |
| `pre-commit.ps1` | Pro vybrané přípony (`.ps1 .txt .sql .cs .rdlc .rdl .rdo .srd .srdmi`): kontrola UTF-8 BOM (jen u DB/report typů), kontrola konce souboru novým řádkem, kontrola zakomentovaných `#ifdef` direktiv v `.sql` (`--!`/`--#` prefixy) |

**Pro koho:** Vývojáři commitující do `C:\Git\shared` — vynucená konvence, ne dokumentace k
učení.

**Jazyk:** Kód (PowerShell), komentáře česky, stručné.

**Použitelnost jako podklad workshopu:** **Nepoužitelné** jako samostatný materiál — je to
mechanismus specifický pro `shared` repo (ne pro `alzask`), navíc řeší formáty souborů
(`.sql`, `.rdl`…), které se v AlzaSk nevyskytují. Nanejvýš ilustrace konceptu "git hooks
vynucují konvence automaticky" pro modul o git workflow.

**Zastaralost:** Bez zjevných problémů; přípony `.rdl/.rdlc/.rdo/.srd/.srdmi` odkazují na
report-designer soubory, které nejspíš patří jinému (staršímu) typu projektu než AlzaSk —
tento hook nemusí být relevantní pro AlzaSk repozitář vůbec (AlzaSk má vlastní `commit-msg`
konvence? — nebylo ověřováno, mimo zadaný rozsah čtení).

---

## G) `C:\Git\shared\.superpowers\sdd\task-*-brief.md` / `task-*-report.md` (5+5=10 souborů) + `progress.md`

**Co to je:** Kompletní pracovní artefakty ze session využívající skill
`superpowers:subagent-driven-development` (TDD workflow) — vytvoření simulace dopravníku
palet v čistém JS (`sim-core.js`). 5 tasků, každý má `brief` (zadání pro sub-agenta: files,
interfaces, kroky RED→GREEN→commit) a `report` (co bylo uděláno, self-review, test evidence).
`progress.md` je jednořádkový log stavu všech 5 tasků + finální review.

**Pro koho:** Byl to reálný vývojářský běh (developer: Martin Tomis dle `task-1-report.md:129`),
ne dokument psaný pro čtenáře — je to **stopa** po použití skillu.

**Jazyk:** Technický (JS kód, test asserty, git příkazy), anglicky psané reporty
(„Summary", „RED Phase", „GREEN Phase"), brief česky/anglicky smíšeně.

**Struktura (vzorek task-1):**
- brief: Files (Create/Test), Interfaces (funkce a konstanty), kroky se šipkami
  (`- [ ] Step N: …`) — init adresáře, failing test, ověření selhání, minimální implementace,
  ověření průchodu, commit.
- report: Summary → What Was Implemented (soubory, adresářová struktura) → Testing & TDD
  Evidence (RED/GREEN fáze s výstupy) → Files Changed → Commits Created → Self-Review Findings
  (Completeness/Code Quality/Test Execution/Git & Commits/Potential Concerns) →
  Architecture Notes → Conclusion (Status/Date/Developer).

`progress.md` (`C:\Git\shared\.superpowers\sdd\progress.md`) potvrzuje: Task 1–5 complete,
finální review „complete (commit `b73318e`, delivery `C:/Temp/simulace-dopravniku.html`)".

**Použitelnost jako podklad workshopu:** **Použitelné jako živý příklad**, ne jako text k
přečtení — je to konkrétní, ověřitelný důkaz, že skill `subagent-driven-development` /
TDD workflow v Claude Code v tomto prostředí **skutečně funguje a byl použit** (autorem
workshopu samotným). Vhodné jako demo case-study ("takhle vypadá TDD smyčka s sub-agenty
krok po kroku") spíš pro pokročilejší modul, ne pro úplný úvod.

**Zastaralost:** Delivery cesta `C:/Temp/simulace-dopravniku.html` (mimo repo) — dle
uživatelské paměti (`feedback_simulace_verzni_razitko.md`) se aktuální simulace dopravníku
vede v `docs/plc/dopravnik-simulace.html` v AlzaSk repu, tzn. tento `.superpowers/sdd` běh
je **historický/experimentální prototyp**, ne totožný se současným PLC simulačním souborem —
nejasné, zda šlo o stejný nebo jiný artefakt; nebylo ověřováno (mimo zadaný rozsah čtení).

---

## H) `C:\Git\alzask\docs\onboarding\` (celý adresář, 11 souborů)

### H1. `project-overview.md`

**Co to je:** Základní přehled projektu AlzaSk/myFABER — navigační mapa "chci vědět o X →
podívej se do Y". Referencováno i z root `CLAUDE.md`.

**Pro koho:** Nový člen týmu jakékoli role (analytik, vývojář, tester) — první čtení.

**Jazyk:** Věcný, tabulkový, žádný žargon bez vysvětlení, hodně odkazů na konkrétní soubory.

**Struktura:** Co je za projekt → Dva repozitáře → Tech stack → Klíčové business procesy
→ Struktura skladu (stanice, zóny, patra) → HW komponenty → Integrace → Datový model →
API architektura → Dokumentační struktura (navigační tabulka).

**Použitelnost:** **Použitelné rovnou** jako referenční modul "co je AlzaSk" — přesně to,
co potřebuje analytik před tím, než se pustí do Claude Code workshopu. Není o Claude Code,
je o doméně.

**Zastaralost:** Nekontrolováno explicitně proti CLAUDE.md (mimo zadání), ale struktura
(`project-overview.md:152–172`) odpovídá aktuální struktuře repozitáře popsané v CLAUDE.md.

### H2. `glossary.md`

**Co to je:** Projektový slovník — skladové pojmy, patra/mezaniny (s upozorněním na
nejednoznačnost číslování a **zjištěnou chybu vstupního dokumentu** — viz níže), business
procesy, HW, systémy/integrace, ContentType, typy objednávek, typy portů, AccessState.

**Pro koho:** Kdokoli potřebuje ujasnit terminologii — analytik i vývojář.

**Jazyk:** Věcný, tabulkový; obsahuje explicitně zdokumentovanou **korekci chyby** v jiném
dokumentu (`glossary.md:58–60`): „Procesní analýza… opakovaně uvádí limit 0,9 m u 1. patra —
to je chyba vstupního dokumentu. Platí `mapData.json`…" — ukázka dobré praxe „cituj zdroj,
označ rozpor", zajímavý příklad pro workshop o groundingu/citacích.

**Struktura:** Skladové pojmy → Patra skladu a mezaniny (se dvěma číselnými řadami a jejich
mapováním) → Business procesy → Hardware → Systémy a integrace → ContentType → Typy
objednávek → Typy portů → Stavy portů (AccessState).

**Použitelnost:** **Použitelné rovnou.** Je to i ukázka `RULE-TERM-001` v praxi (kanonický
zdroj terminologie).

**Zastaralost:** Žádná nalezená v rámci textu samotného — naopak sám dokument opravuje
zastaralost jinde.

### H3. `Setup-novy-clen-tymu.md`

**Co to je:** Kompletní instalační návod (3 části): Část 1 VS Code + Claude Code + Git
(AI účet, PATH, instalace, klonování); Část 2 Bruno + Android Studio; Část 3 online aplikace
(Freelo, myTEAM).

**Pro koho:** Zcela nový člen týmu (analytik/tester/konzultant) — **provozní/IT onboarding**,
ne výuka práce s Claude Code samotnou.

**Jazyk:** Velmi laický, krok-za-krokem, s vysvětlením "proč" u každého technického rozhodnutí
(`Setup-novy-clen-tymu.md:55–56` „Proč potřebujeme Node.js", `:128–139` „Proč PATH a co to je").

**Struktura:** Předpoklady (přístupy) → Instalace (VS Code, Node.js, Git) → PATH vysvětlení →
Ověření instalací (oba účty) → Instalace Claude Code CLI → VS Code pod AI účtem → Claude
rozšíření → Klonování repa → Časté problémy → Checklist → Extensions.

**Použitelnost:** **Použitelné rovnou** jako "den 0" modul (jak se dostat k funkčnímu Claude
Code), ale je to **předstupeň** workshopu, ne workshop samotný — pokud budoucí workshop
předpokládá už fungující prostředí, tenhle dokument řeší krok předtím.

**Zastaralost:** Specifické detaily (jména kontaktních osob — Pavel Nytra, Martin Hamala,
Tonda Vaněček, Radim Tichý, Tomáš Matýsek) mohou zastarat s personální rotací; nelze ověřit
bez HR zdroje. Technický obsah (dvouúčtový model AI/normální účet, System installer,
`setx PATH`) vypadá interně konzistentní a aktuální.

### H4. `testing-onboarding.md`

**Co to je:** Onboarding **specificky pro testery** — přístupy, struktura repa, co se testuje
(API + business procesy), jak jsou organizované FR/TC (Gherkin), init data, autentizace v
Postmanu, idempotency key, typický průběh ručního testu.

**Pro koho:** Testeři (explicitně v nadpisu).

**Jazyk:** Věcný, s praktickými příklady (Gherkin ukázka kódu `testing-onboarding.md:136–161`).

**Struktura:** Přístupy → Struktura projektu v Gitu → Co budeme testovat (API, business
procesy) → Jak jsou organizované testy (FR, TC, Gherkin příklady, Scenario Outline,
automatické vs. ruční testy) → Praktický postup testování (init data, import pořadí,
`clear` parametr, autentizace, idempotency key, typický průběh) → Checklist.

**Použitelnost:** **Použitelné rovnou** jako modul pro roli tester, pokud by workshop měl
i tuto cílovku, ale zadání říká „workshop pro analytiky" — pro analytiky je to **doplňkové
čtení** (FR/TC formát je pro analytiky přímo relevantní; init data/Postman spíš ne).

**Zastaralost:** Bez nálezu v rámci textu.

### H5. `Seznam-prostredi-alzask.md`

**Co to je:** Tabulka všech prostředí (DEV/RC/RC-1..3/RC-sim interní; MOCK/TEST/STAGE/PROD
zákaznická) s URL na Swagger, Management app, baseUrl, DB.

**Pro koho:** Kdokoli potřebuje se připojit na konkrétní prostředí (testeři, konzultanti,
release).

**Jazyk:** Čistě referenční/tabulkový, žádná próza k učení.

**Struktura:** Vysvětlivky → Seznam prostředí (A interní, B zákaznická) → Detail per
prostředí (7 sekcí).

**Použitelnost:** **Nepoužitelné** jako workshop obsah (je to referenční tabulka URL/portů),
ale relevantní jako odkaz "kde najdu prostředí" pokud workshop bude obsahovat praktické
demo proti reálnému API.

**Zastaralost:** Nelze ověřit bez přístupu k infrastruktuře; dokument cituje zdroj
(`Seznam-prostredi-alzask.md:3`) jiný GitLab repo `myfaber2Install` jako zdroj pravdy —
tzn. tento soubor je sám o sobě odvozený/kopie, riziko rozjetí s originálem.

### H6. `Upgrade-a-inicializace-myFaber.md`

**Co to je:** Provozní návod pro upgrade prostředí (DB výmaz, GitLab pipeline upgrade,
inicializace dat, restart služeb, FAQ).

**Pro koho:** Tester/konzultant provádějící upgrade prostředí — role-specifický operační
manuál.

**Jazyk:** Věcný, krok za krokem, s FAQ sekcí.

**Struktura:** Odkazy → Příprava (přístupy, adresy, init soubory) → Vymazání dat z DB
(vč. Bullseye WCS simulátoru, řešení zaseklých stavů) → Upgrade přes GitLab Pipeline →
Inicializace dat a nastavení klientů (import mapy/init dat, heslo klienta, containerData) →
Restart služeb a ověření → Pravidlo pro práci v Alza prostředích (prefix `KV-`) →
Checklist → FAQ.

**Použitelnost:** **Nepoužitelné** pro workshop Claude Code — je to čistě provozní/DevOps
návod nesouvisející s používáním AI nástroje.

**Zastaralost:** Odkaz na utilitku „Git repo AlzaSk utilitka zde" (`Upgrade-a-inicializace-myFaber.md:36`,
odkaz `/GitLab/alzask/docs/tools/alzask-init-data-builder.html`) — cesta vypadá jako
placeholder/nekompletní odkaz (chybí skutečná doména), nebylo ověřováno, zda soubor
`docs/tools/alzask-init-data-builder.html` v repu existuje (mimo zadaný rozsah čtení).

### H7. `AfterUPG-testers.md`

**Co to je:** Krátký checklist "co dělat po UPG prod" — kontrola verze, testování koloběhů
po vydání verze, RC-SIM reset.

**Pro koho:** Testeři/release po produkčním upgrade.

**Jazyk:** Telegrafický, poznámkový styl (odrážky, useknuté věty), s escapovanými
markdown znaky (`1\.`, `\\` v cestách) — vypadá jako přímý copy-paste z Wordu/Teams bez
úpravy formátování.

**Struktura:** Kontrola po UPG prod → Otestovat koloběhy → RC-SIM reset.

**Použitelnost:** **Nepoužitelné** pro workshop — čistě provozní.

**Zastaralost:** Formát dokumentu (escapované zpětná lomítka, tečky) naznačuje, že nebyl
nikdy vyčištěn po vzniku — kandidát na formátovací refresh, ne obsahovou zastaralost.

### H8. `Before UPG Alza prostredi.md`

**Co to je:** Postup přípravy a inicializace dat v prostředích Alza MOCK/TEST (init soubory,
Swagger import, hesla, wesSettings).

**Pro koho:** Tester/konzultant provádějící přípravu upgrade.

**Jazyk:** Věcný, krokový.

**Struktura:** Příprava init souborů → Inicializace dat v prostředích Alzy (adresy
Swaggerů, nahrání JSON, hesla) → WES settings.

**Použitelnost:** **Nepoužitelné** pro workshop — čistě provozní, překrývá se z části
s H6 (Upgrade-a-inicializace-myFaber.md).

**Zastaralost:** Bez nálezu.

### H9. `PROMPT-ontologie-prvku.md`, `PROMPT-plugin-ontology-registry.md`, `PROMPT-ukotveni-ontologie.md`

**Co to je:** Tři rozsáhlé (7–30 KB) **prompt-briefy pro Claude Code** k vybudování registru
ontologie prvků (`docs/ontology/`) — D1–D11 dávkový postup, schéma registru, precedence
zdrojů, kontroly po dávce, antipatterny. Nejde o výukový materiál, ale o **spouštěcí zadání
pro agenta** (podobně jako `.superpowers/sdd/task-*-brief.md`, ale mnohem větší a
projekt-specifické).

**Pro koho:** Claude Code (jako vstupní prompt), ne člověk ke čtení — ačkoli člověk (Martin
Tomis) je autor/reviewer.

**Jazyk:** Vysoce technický, hustý, s formálním schématem (YAML predikáty, invarianty).

**Struktura (dle nadpisů, `PROMPT-ontologie-prvku.md`):** Zadání → Co je "prvek" →
Precedence zdrojů → Cílové artefakty → Schéma registru → Fixní slovník predikátů →
Invarianty → Dávky (D1–D11, každá se zdrojem a cílem) → Rytmus dávky → Kontroly po každé
dávce → Antipatterny → Praktické detaily prostředí.
(`PROMPT-ukotveni-ontologie.md` a `PROMPT-plugin-ontology-registry.md` mají analogickou
strukturu — zadání, otevřené otázky O1–O4, varianty, brány, dávky, antipatterny.)

**Použitelnost jako podklad workshopu:** **Použitelné jako case-study / ukázka dobře
napsaného promptu** pro pokročilý modul "jak zadat velký vícedávkový úkol Claude Code" —
konkrétně vzorec "dávky + kontrola po dávce + explicitní antipatterny + precedence zdrojů"
je přenositelný vzor i mimo ontologii. Není vhodné pro úvodní/laický modul (příliš husté
a projekt-specifické).

**Zastaralost:** Jsou to živé, aktuálně používané provozní prompty (registr ontologie je
aktivně budovaný — viz `project_ontologie_prvku_beh.md` v paměti, D1–D11 proběhlo).
Bez nálezu vnitřní zastaralosti v rámci zadaného rozsahu (jen nadpisy, ne plný obsah čten).

### H10. `prezentace-01-uvod-a-zakladni-kolobeh-predprijem.pptx`

**Co to je:** Existující **prezentace pro onboarding** (11 slidů) — "Procesy skladu ALZA
SKLC3 — díl 1: Úvod do projektu a základní koloběh (Předpříjem, Dekantace)". Extrahováno
textově přes zipfile/regex (dle poznámky v paměti — Read nástroj PPTX nečte přímo).

**Pro koho:** Explicitně (slide 2): „Primárně pro testery; schůzky nahráváme → slouží jako
onboarding pro nové členy." Cílovka = testeři/noví členové, natáčeno jako video-schůzka.

**Jazyk:** Stručné odrážky, doménová terminologie s vysvětlivkami, číslované kroky.

**Struktura (11 slidů):** 1. Titulní → 2. Cíl schůzek → 3. Co je AlzaSk/myFABER →
4. Integrace (kdo co dělá: WMS→WES→RCS/PLC) → 5. Hlavní tok a struktura skladu →
6. Klíčové pojmy → 7. **Dokumentace — kde co hledat** (mapuje docs/analysis, docs/api,
FR/TC, docs/adr, docs/scenarios, docs/onboarding) → 8. Algoritmy WES (ALLOCATION-001,
PERIODIC-001, STACKING-001, RELOCATION-001, DISPATCH-001) → 9. Předpříjem–Dekantace–
Logistické toky → 10. Základní koloběh SCE-DEKANT-01 (9 kroků) → 11. Shrnutí.

**Použitelnost jako podklad workshopu:** **Přímo použitelné jako vzor formátu** — je to
existující, otestovaný formát "krátká schůzka + slide na doménové téma + nahrávka jako
onboarding archiv". Obsahově je o doméně skladu, ne o Claude Code, ale **formát/rytmus**
(9–11 slidů, 1 téma, odkaz na dokumentaci u každého bodu) je přímo přenositelný vzor
pro sérii workshopů o Claude Code ("díl 1, díl 2…" jako zde).

**Zastaralost:** Slide 7 zmiňuje `docs/scenarios/` (SCE) jako existující kategorii — to
odpovídá struktuře v CLAUDE.md. Bez zjevné zastaralosti; je to "díl 1" série — nejasné
(mimo scope), zda díly 2+ existují.

---

## I) `C:\Git\alzask\docs\suppliers\POSTUP-pro-analytiky.md`

**Co to je:** Laický návod **pro analytiky** (výslovně v názvu i textu: „Tento dokument je
návod pro člověka") na práci s evidencí dotazů na dodavatele (BullsEye, BlueSword) přes
slash příkazy `/dodavatele:mail`, `/dodavatele:stav`, `/dodavatele:hotovo`.

**Pro koho:** Analytik — explicitně, nejlaičtější a nejlépe formátovaný dokument z celé
inventury.

**Jazyk:** Velmi přístupný, princip "3 příkazy, které stačí znát", slovníček pojmů,
8 pojmenovaných situací s konkrétním „co uděláš / co řekneš Claude / co dostaneš", reálná
čísla jako motivace („dnes je tam 33 dotazů z 65", „jeden propadlý příslib").

**Struktura:** K čemu to je → Tři příkazy → Slovníček → Situace 1–8 (příchozí e-mail, call
s dodavatelem, posílám otázky, nedostatečná odpověď, nevím jestli mám odpověď, zapsal jsem
odpověď, dodavatel přislíbil, dostal jsem dokument) → Co nedělat → Kontrola evidence.

**Použitelnost jako podklad workshopu:** **Použitelné rovnou jako VZOR** — je to přesně ten
typ dokumentu, který by workshop pro analytiky chtěl produkovat pro DALŠÍ oblasti (FR
tvorba, ADR, ontologie…): jasný "co řekneš Claude Code" vzorec, žádný interní žargon,
konkrétní čísla jako důkaz hodnoty. **Tento dokument samotný je nejlepší dostupný vzor
stylu pro budoucí analytický onboarding.**

**Zastaralost:** Bez nálezu — aktivně udržovaný dokument (datum poslední úpravy souboru
2026-08-25, den před inventurou).

---

## J) `C:\Git\alzask\.claude\rules\README.md`

**Co to je:** Quick-reference k mechanice "znalostní smyčky" (Rules) — jak se pravidla
ukládají, načítají a povyšují mezi zónami (inbox → personal → shared).

**Pro koho:** Primárně Claude (auto-load přes frontmatter `paths:`), sekundárně člověk,
který chce pochopit mechanismus.

**Jazyk:** Technický, hutný — vysvětluje interní mechaniku (git zóny, gitignored zrcadlo,
precedence, path-scoping) v odborných termínech.

**Struktura:** Zóny (tabulka 4 zón: Záchyt/Osobní/Zrcadlo/Sdílená) → Co se načítá v nové
session → Precedence + závaznost → Tok znalosti a příkazy → Validace.

**Použitelnost jako podklad workshopu:** **Potřebuje výrazný přepis**, pokud by měl jít
analytikům — koncept "Claude si pamatuje poučení napříč projekty a lidmi" je hodnotný a
zajímavý (workshop-worthy), ale současný text je psaný pro toho, kdo už rozumí Claude Code
internals (frontmatter, auto-load, path-scoping). Pro analytika by šlo o "jak funguje
paměť/učení Claude Code v tomto projektu" modul, ale je nutné ho zjednodušit na úroveň
slide-decku typu A) výše.

**Zastaralost:** Bez nálezu — aktivně řízený mechanismus (potvrzeno auto-injektovanými
`RULE-*` soubory v této samotné session).

---

## K) `C:\Git\alzask\docs\fr\README.md`

**Co to je:** Rozsáhlá (45 KB, 14 sekcí) **kompletní metodika zadávání FR/TC** pro AlzaSk.
Nejde primárně o "jak používat Claude Code", ale obsahuje samostatnou sekci 8+9 přímo o
práci s Claude Code v kontextu FR a samostatnou sekci 11 o souběžné práci analytiků.

**Pro koho:** Primárně analytik/kurátor FR — explicitně adresováno rolím ("Analytik vytváří
nový FR", sekce 14).

**Jazyk:** Smíšený — sekce o struktuře/konvencích jsou věcné a přístupné, sekce o Gherkin/TC
formátu jsou hodně technické (YAML schema, tag konvence, `@S` identifikátory).

**Struktura (14 sekcí):** 1. Struktura dle PBS → 2. Struktura adresáře `docs/fr` →
3. Životní cyklus FR → 4. Pravidla pro Gherkin testy → 5. Testovací scénáře (TC — princip,
formát, identifikátor, umístění, struktura souboru, formát scénářů, `@scope_id`,
per-scénář status, stabilita `@S`, retired/moved evidence, mapování na C# testy, principy
návrhu TC, doménové kroky) → 6. Mock strategie → 7. Závislosti mezi FR → **8. Práce s
Claude Code** (generování FR, implementace FR, validace FR, aktualizace FR po implementaci)
→ **9. Zpětná vazba z implementace do FR** (kdy/jak aktualizovat, workflow diagram) →
10. Integrace GitLab→Freelo → **11. Souběžná práce analytiků** (princip "jeden analytik =
jedna oblast", workflow cross-area závislostí) → 12. Škálování na tisíce FR (GitLab search,
validační nástroje) → 13. Vztah ADR a FR → 14. Příklad kompletního workflow (analytik →
prompt pro Claude Code → soubor → commit).

**Klíčové konkrétní citace k workshopu:**
- `docs/fr/README.md:1090–1111` (sekce 14) — hotový end-to-end příklad "analytik napíše
  prompt Claude Code → vznikne FR soubor → commit/push" — přímo použitelná ukázka.
- `docs/fr/README.md:813–841` (sekce 8) — tři vzorové prompty (generování/implementace/
  validace FR).
- `docs/fr/README.md:982–996` (sekce 11) — princip "jeden analytik = jedna oblast" pro
  minimalizaci merge konfliktů při souběžné práci — přímo relevantní workshop téma
  ("jak víc analytiků současně používá Claude Code na stejném repu").

**Použitelnost jako podklad workshopu:** **Sekce 8, 9, 11, 14 jsou použitelné rovnou** jako
zdroj příkladů promptů a workflow pro analytickou práci s Claude Code v AlzaSk. Zbytek
dokumentu (sekce 1–7, 10, 12, 13) je **metodika k FR/TC samotné**, ne o Claude Code —
relevantní jako **kontext, ne jako obsah workshopu** (analytik musí znát FR formát, aby
prompty ze sekce 8/14 dávaly smysl).

**Zastaralost:** Sekce 3 (životní cyklus FR — `draft/ready/in_progress/review/blocked/done`)
je framework-level a odpovídá aktuálnímu `docs/fr/.fr-tools/schema.yaml` (ověřeno grepem —
`status` pole existuje v schématu, hodnoty nekontrolovány řádek po řádku). Toto se **neplete**
s per-scénář TC statusem (`draft/done`), který byl redukován 2026-05-12 — jde o dva různé
statusy na dvou různých úrovních (FR vs. jednotlivý `@S` scénář), oba dokumentované správně
a nekonfliktně.

---

## Co je tím pokryté a nemá se hledat znovu

| Téma | Kde je pokryté | Poznámka |
|---|---|---|
| **Jak funguje Claude Code pod kapotou** (model, tokeny, kontext, cache, agentní smyčka, tool_use) | A) `claude-code-jak-funguje.html` | Hotový 12-slide deck, laický jazyk, použitelný rovnou |
| **Instalace a IT onboarding** (VS Code, Node, Git, AI účet, Claude Code CLI, klonování repa) | H3) `Setup-novy-clen-tymu.md` | Kompletní krok-za-krokem, jen personální kontakty mohou zastarat |
| **Přehled projektu AlzaSk/myFABER** (procesy, struktura skladu, integrace, datový model) | H1) `project-overview.md` | Navigační mapa, aktuální |
| **Terminologie/slovník** | H2) `glossary.md` | Kanonický zdroj (RULE-TERM-001), obsahuje i příklad "citace opravuje chybu jinde" |
| **Onboarding pro testery** (přístupy, FR/TC struktura, init data, Postman, idempotency) | H4) `testing-onboarding.md` | Role tester, ne analytik — částečně relevantní (FR/TC formát) |
| **Provozní návody** (prostředí, upgrade, DB výmaz, RC-SIM reset) | H5, H6, H7, H8 | Čistě DevOps/release, mimo scope Claude Code workshopu |
| **Vzorová prezentace o doméně skladu** (formát: krátká schůzka, slide+odkazy, nahrávka jako archiv) | H10) `prezentace-01...pptx` | Vzor formátu pro sérii workshopů, obsahem je doména, ne Claude Code |
| **Jak zadat velký vícedávkový prompt agentovi** (dávky, kontrola po dávce, antipatterny) | H9) tři `PROMPT-*.md` soubory | Case-study pro pokročilý modul, ne pro úvod |
| **Vzor "3 příkazy + situace + co řekneš Claude"** stylu pro analytika bez žargonu | I) `POSTUP-pro-analytiky.md` | **Nejlepší dostupný stylový vzor** pro budoucí analytický materiál |
| **Metodika FR/TC** vč. sekcí přímo o práci s Claude Code a souběžné práci analytiků | K) `docs/fr/README.md` sekce 8, 9, 11, 14 | Hotové vzorové prompty a workflow, přímo použitelné |
| **Znalostní smyčka / paměť Claude Code napříč projekty** | J) `.claude/rules/README.md` | Koncept hodnotný, formulace potřebuje zjednodušit pro laiky |
| **Sdílené pluginy — koncept a instalace** | D) `plugins/README.md` | Instalační mechanika, technická, potřebuje výtah |
| **Git konvence (commit prefix, pre-commit kontroly)** | F) `.githooks/` | Konkrétní pro `shared` repo, ne AlzaSk; ilustrace konceptu |
| **Governance "agent navrhuje, člověk promuje"** | E) `CODEOWNERS`, RULE-GOV-001 (auto-injektováno) | Konkrétní příklad vynucení přes GitLab MR |
| **Reálný TDD/subagent-driven-development běh** (5 tasků, brief+report, RED/GREEN) | G) `.superpowers/sdd/task-*` | Konkrétní, ověřitelný demo-case pro pokročilý modul |

### Co v prohledaném materiálu **chybí** (mezera pro budoucí workshop)

- Žádný z přečtených dokumentů necílí přímo na "analytik používá Claude Code pro **svou
  vlastní** každodenní práci obecně" (psaní FR/ADR, dohledávání, review) jako ucelený
  úvodní modul — nejblíž je `POSTUP-pro-analytiky.md` (I), ale ten je úzce o jedné agendě
  (dodavatelé), ne o Claude Code obecně.
- `A)` (jak Claude Code funguje) a `I)` (jak ho analytik ovládá pro konkrétní agendu) jsou
  na opačných pólech — chybí prostřední vrstva "obecné ovládání: prompty, skilly, slash
  příkazy, kdy se ptát, kdy dát agentovi volnost" pro analytika bez inženýrského backgroundu.
- Nebyl nalezen žádný materiál srovnávající roli/oprávnění analytika vs. vývojáře v Claude
  Code prostředí (guard, PROTECT/ALLOW zóny jsou zdokumentované jen technicky v D/J).
