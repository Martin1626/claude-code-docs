# Fáze 3c — Pravidla, znalostní inbox a paměti (podklad pro workshop)

Zdroje: `C:\Git\alzask\.claude\rules\`, `C:\Git\alzask\.claude\rules-personal\martint\`,
`C:\Git\alzask\.claude\knowledge-inbox\martint\`, `C:\Git\fhb\.claude\rules\`,
`C:\Git\fhb\.claude\rules-personal\martint\`, `C:\Git\fhb\.claude\knowledge-inbox\martint\`,
paměti `C:\Users\ai_martint\.claude\projects\c--Git-alzask\memory\`,
`...\c--Git-fhb\memory\`. Datum inventury: 2026-08-26.

---

## 0. Mechanika smyčky (z READMEs, oba repo identické)

Čtyři zóny: **inbox** (`.claude/knowledge-inbox/<handle>/`, committed, syrové kandidáty,
auto-load jen posledních 14 dní) → **osobní** (`.claude/rules-personal/<handle>/`, committed,
promuje se příkazem `/knowledge-loop:rule-new`) → **zrcadlo** (`.claude/rules/personal/<handle>/`,
gitignored, generuje SessionStart hook, auto-load) → **sdílená** (`.claude/rules/shared/`,
committed, kurátorováno CODEOWNERS, promuje `/knowledge-loop:rules-consolidate`).
Precedence: `accepted-ADR > shared > cross-project shared > rules-personal > ZVAŽ`.
Princip: **"agent navrhuje, promuje jen člověk"** — konsolidace vyrábí návrh (MR), originály
se nemění automaticky.

**Přenositelná zásada č. 0:** Znalostní smyčka má čtyři formální patra, ale ani jedno patro
mezi nimi není vynucené branou — postup vpřed je vždy manuální lidský příkaz
(`/knowledge-loop:rule-new`, `/knowledge-loop:rules-consolidate`). To je ironické vzhledem
k tomu, že jedno z nejsilněji opakovaných pravidel v celé smyčce je "vynucuj bránou, ne
promptem/úmyslem" (RULE-GOV-002) — na vlastní mechaniku smyčky se to pravidlo neaplikuje.

---

## 1–2. Sdílená pravidla (`rules/shared/`) — AlzaSk (15) a FHB (13)

Formát tabulky: **ID | co říká (1 věta) | konkrétní problém, který ho vyvolal | soubor**.

### AlzaSk (`C:\Git\alzask\.claude\rules\shared\`)

| ID | Co říká | Konkrétní problém (doklad) | Soubor |
|----|---------|------------------------------|--------|
| RULE-AP-001 | Antipatterny: neodpovídej z paměti, necituj `temp/`, nehádej PBS mapování | Seed přímo z `CLAUDE.md` (základní pravidlo projektu), ne z inboxu — nejstarší, "ústavní" pravidlo | `RULE-AP-001_antipatterns.md:1` |
| RULE-AP-002 | Pokrytí výstupu odvoď ze zdroje (top-down), ne z vlastního rámce úlohy | Spec startup-sekvence 2026-06-16: vynechané palubní skenery AGV + servisní dveře, protože "rámec úlohy" je tiše vyloučil za hranici | `RULE-AP-002_pokryti-ze-zdroje.md:62` |
| RULE-CL-001 | Changelog vždy na konec tabulky (append-only, vzestupně) | "Opakovaná korekce pořadí" — mechanická chyba, co se vrací dodnes (viz sekce 6) | `RULE-CL-001_changelog.md:113` |
| RULE-DIAG-001 | Mermaid: zakázané znaky (`;`,`()`,`+`), max 1 dvojtečka v přechodu, žádné `rect rgb`, segmenty ~40–60 znaků | Merge zkušeností z renderu + dvou inbox kandidátů (rect rgb, zalamování, 2026-06-12) | `RULE-DIAG-001_diagramy.md:144` |
| RULE-GOV-001 | Agent navrhuje, promuje jen člověk — žádné samoschválené rozšíření mantinelu | Princip ze spec-factory návrhu, seed přímo (ne z inboxu) | `RULE-GOV-001_boundary-promoce.md:203` |
| RULE-GOV-002 | Invariant pipeline vynucuj **bránou** (exit-kód), ne větou v promptu | Retrofit startup-sekvence: 4 "miny" nepokryté intake bránou == přesně místa pozdějších critical nálezů | `RULE-GOV-002_brana-ne-prompt.md:252` |
| RULE-META-001 | Autoři plným jménem; u externích dokumentů reální spoluautoři bez "+ Claude"; jen `TODO` jako placeholder | Import z FHB (oprava architekta 2026-05-28) | `RULE-META-001_metadata-styl.md:309` |
| RULE-ONT-001 | Nový prvek systému → záznam do registru ontologie v témže cyklu | `ADR-ASK-PROC-020`, rozhodnutí 5 (obousměrná smyčka) | `RULE-ONT-001_novy-prvek-do-registru.md:361` |
| RULE-ONT-002 | Cituj původní zdroj z karty prvku, ne registr samotný | Tamtéž — registr je index, ne autorita | `RULE-ONT-002_cituj-zdroj-ne-registr.md:422` |
| RULE-ONT-003 | Verdikt `ZMIZELA` u citace řeší člověk; `POSUN` je rutina `reanchor.py --apply` | Tamtéž, rozhodnutí 3 | `RULE-ONT-003_zmizela-resi-clovek.md:478` |
| RULE-SPEC-001 | Každý požadavek má ID, prioritu, zdroj/trace, důvěru, akceptační kritérium | Sloučení AlzaSk+FHB, T1 linter | `RULE-SPEC-001_trace-akceptace.md:533` |
| RULE-SPEC-002 | Kritik posuzuje sekci jako **cizí** výstup, ne pokračování vlastního myšlení | Self-Correction Illusion — princip spec-factory návrhu §2 | `RULE-SPEC-002_kritik-cizi-vystup.md:592` |
| RULE-SPEC-004 | U změny kontraktu nejdřív tabulka proces×událost k odsouhlasení, pak red-team PŘED hromadnou aplikací | Změna webhook kontraktu (containerPrepared/Departed): 3 kritické nedostatky odhalila až adversariální revize, PŘED rozkopírováním do 21 TC | `RULE-SPEC-004_model-pred-hromadnou-aplikaci.md:637` |
| RULE-TC-001 | TC konvence: neměnné `@S`, per-scénář status/datum, doménové kroky, žádný `<<internal>>` | Seed z MEMORY.md (starší evoluce, ne z inboxu) | `RULE-TC-001_tc-konvence.md:691` |
| RULE-TERM-001 | Kanonická terminologie AlzaSk (nosič, typ obsahu, svoz=přeprava) | Seed z `docs/onboarding/glossary.md` | `RULE-TERM-001_terminologie.md:749` |

### FHB (`C:\Git\fhb\.claude\rules\shared\`)

| ID | Co říká | Konkrétní problém (doklad) | Soubor |
|----|---------|------------------------------|--------|
| RULE-AP-001 | Totéž jako AlzaSk, FHB verze | `CLAUDE.md` + `grounding-disciplina.md §4` | `RULE-AP-001_antipatterns.md:1` |
| RULE-AP-002 | Totéž jako AlzaSk (cross-project shared) | — | `RULE-AP-002_pokryti-ze-zdroje.md` |
| RULE-API-002 | Cizí klíče (`*Id`) nikdy `default: ""` — nech `null`/vynech | Revize `API-myFABER-ASRS-v2.yaml` 2026-06-15 (Pavel Nytra) — odstranění FK defaultů napříč kontraktem | `RULE-API-002_fk-bez-defaultu.md:1` |
| RULE-API-003 | `maxLength` z DB domén hostitele; nedůvěryhodné vstupy vždy omez | Tamtéž — vstupy omezeny (`clientSecret`→255), výstupy bez limitu | `RULE-API-003_maxlength-limity.md:1` |
| RULE-API-005 | Žádný `oneOf`/`discriminator` — plochý model s enum "typovým polem" | Tamtéž + `ADR-MF-DB-008`, odstraněn jednočlenný oneOf | `RULE-API-005_zadny-oneof-discriminator.md:1` |
| RULE-CL-001 | Totéž jako AlzaSk | spec-factory konvence | `RULE-CL-001_changelog.md:1` |
| RULE-DIAG-001 | Mermaid bezpečné znaky (FHB verze — bez dvojtečky/wrap bodů, ty jsou jen v AlzaSk verzi) | Opravy renderu 2026-04-18/19/24 | `RULE-DIAG-001_diagramy.md:1` |
| RULE-GOV-001 | Totéž jako AlzaSk, plná verze s popisem `spec-guard` hooku | spec-factory princip | `RULE-GOV-001_boundary-promoce.md:1` |
| RULE-GOV-002 | Totéž jako AlzaSk — **povýšeno z AlzaSk inboxu 2026-07-07** | Přenos mezi projekty přes plugin | `RULE-GOV-002_brana-ne-prompt.md:1` |
| RULE-META-001 | Totéž jako AlzaSk — toto je **originál**, AlzaSk ho převzalo | Oprava architekta 2026-05-28 | `RULE-META-001_metadata-styl.md:1` |
| RULE-SPEC-001 | Totéž jako AlzaSk | sloučení obou projektů | `RULE-SPEC-001_trace-akceptace.md:1` |
| RULE-SPEC-002 | Totéž jako AlzaSk — toto je **originál** | `docs/superpowers/specs/2026-06-15-spec-factory-design.md` | `RULE-SPEC-002_kritik-cizi-vystup.md:1` |
| RULE-TERM-001 | Kanonická terminologie FHB (nosič, WMS ne VMS, rezervace portu, AMR) | `arch-spec/12-glossary.md` + opravy architekta 04-17/04-20 | `RULE-TERM-001_terminologie.md:1` |

**Pozorování:** 8 z 13 FHB pravidel a 8 z 15 AlzaSk pravidel jsou **doslovně identická** (sdílená
přes cross-project vrstvu) — signál, že smyčka funguje mezizákaznicky, ne jen v rámci projektu.
Zbytek je projekt-specifický (terminologie, TC konvence, ontologie, API detaily FHB).

---

## 3. Osobní zóna (`rules-personal/martint/`) — srovnání

| Projekt | Obsah | Git historie |
|---|---|---|
| **AlzaSk** | Prázdná (jen `.gitkeep`) | `git log` na adresář ukazuje jediný commit — založení prázdné struktury při přechodu na knowledge-loop v2 (`f060341`). Nikdy zde nic neleželo. |
| **FHB** | 2 pravidla, obě `status: draft`, `layer: shared` (tj. míří do shared, ale zůstávají) | Založena 2026-07-11 |

**FHB `RULE-API-001` (stavové přechody trigger-based, ne intent-based)** — zdroj MTG-2026-05-21,
řeší nejednoznačnost stavů (`cancelled` znamenalo 3 různé věci ve 3 variantách). **Vědomě
zůstává mimo shared** — `RULE-API-005` to výslovně píše: *"ID 001 a 004 proto v pluginu záměrně
chybí"*, protože návrh stavových/enum polí je **doménové** pravidlo hostitele, ne generalizovatelné
do pluginu spec-factory.

**FHB `RULE-API-004`** (webhook prefix `Wh*`, ne suffix `*Event`) — ze schůzky 2026-06-15,
stejný důvod ponechání v personal (konvence specifická pro FHB/Alza pojmenování, ne univerzální).

**Přenositelná zásada:** Osobní zóna není jen "čekárna před shared" — legitimně drží pravidla,
která jsou **správná, ale příliš doménová/projektová** na to, aby se generalizovala. AlzaSk ale
tuhle vrstvu vůbec nepoužívá — všechno, co se povýšilo, šlo přímo `inbox → shared` (viz RULE-AP-002,
GOV-002, SPEC-004, DIAG-001 — všechny mají `source: 'AlzaSk knowledge-inbox …'` nebo `'spec-factory
— zobecněná zkušenost'` bez mezistanice v `rules-personal`). AlzaSk osobní pravidlo, které by
zůstalo jen projektové (analogie FHB API-001/004), zatím žádné nevzniklo.

---

## 4. README metodika (oba repo, identický text)

`C:\Git\alzask\.claude\rules\README.md` a `C:\Git\fhb\.claude\rules\README.md` jsou byte-identické
(stejný frontmatter, stejné sekce Zóny / Co se načítá / Precedence / Tok znalosti / Validace).
Rozpočtová disciplína: aktivní Rules po scopingu drž ~80–150 řádků, ověř `/memory`. Validace:
`python "$CLAUDE_PLUGIN_ROOT/tools/validate.py"` (`--strict` pro striktní režim).

**De-identifikace už při záchytu** — obsah jde do Gitu, takže NDA vyžaduje anonymizaci (typ
zákazníka, ne jméno) hned v inboxu, ne až při konsolidaci.

---

## 5. Knowledge inbox — kandidáti (bez doslovného obsahu)

### AlzaSk (17 souborů, 2026-06-12 → 2026-08-25, cca 63 pojmenovaných kandidátů)

| Datum | Název kandidáta | Destilovaná zásada | Povýšeno? |
|---|---|---|---|
| 2026-06-12 | Model k odsouhlasení + red-team před hromadnou aplikací | Kontrakt/model má neviditelné provázanosti; tabulka k odsouhlasení + adversariální revize PŘED aplikací na desítky artefaktů | **Ano** → RULE-SPEC-004 |
| 2026-06-12 | Žádné barevné pozadí v Mermaid | `rect rgb(...)` škodí čitelnosti | **Ano** → merge do RULE-DIAG-001 |
| 2026-06-12 | Zalamování dlouhých řádků v Mermaid | Segmenty ~40–60 znaků, zalom na hranici informace | **Ano** → merge do RULE-DIAG-001 |
| 2026-06-17 | Pokrytí ze zdroje, ne z rámce úlohy | Rámec úlohy tiše vylučuje "mimo rozsah"; pokrytí se musí odvodit ze zdroje top-down | **Ano** → RULE-AP-002 |
| 2026-06-18 | Vynucuj bránou, neinstruuj v promptu | Instrukce v promptu se u velkého kontextu ztrácí; brána běží pokaždé a vrací číslo | **Ano** → RULE-GOV-002 |
| 2026-07-10 | Stavový efekt nové akce odvoď z entity a precedentu, ne z názvu akce | Akce pojmenovaná po jednom poli může měnit stav JINÉ entity, na kterou se nikdo neptal | Ne (návrh na rozšíření AP-002/SPEC-004, nerealizováno) |
| 2026-07-11 | Vnořený template literal shazuje Workflow parser | Konkatenace místo vnořeného backticku; chyba parseru ukazuje na jiné místo, než je příčina | Ne (mechanický poznatek, zůstal v inboxu) |
| 2026-07-11 | Read-only agent nemá Write — obsah vrací přes schema, zapisuje orchestrátor z journalu | Fan-out agent bez Write nástroje nemůže "WRITE" — návrat strukturou + parsing journalu | Ne |
| 2026-07-11 | Pole "Důvěra" musí být jen enum token, ne próza | Opakovaná chyba napříč iteracemi — kandidát na auto-strip v linteru | Ne |
| 2026-07-11 | Kontraktní rozpory řeš ukotvením v kanonickém dokumentu, ne od stolu | Cross-section rozpory se řeší "mirror-the-canon" + citací, ne diskusí | Ne (návrh na konkretizaci SPEC-004) |
| 2026-08-03 | Výtah z podkladů třetí strany drž čistý od vlastní interpretace | Míchání "co řekl dodavatel" s "co si myslíme my" znehodnotí obojí | Ne |
| 2026-08-11 | Changelog popisuje aktuální stav, ne historii obratů rozhodnutí | Narativ "nejprve X, pak zrušeno, znovu X" je šum — stačí co platí teď | Ne (otevřená otázka k RULE-CL-001) |
| 2026-08-13 | Kardinalitu vztahu ověř ze schématu, ne z diagramu, před formulací pravidla | Plurál pole (`xIds[]`) je signál M:N, který se čte jako pouhý název | Ne |
| 2026-08-13 | Changelog vkládej indexově, ne substitucí kolem anchoru | Substituce `replace(last, new+last)` vloží NAD, ne ZA — porušuje vlastní RULE-CL-001 | Ne (implementační dodatek k CL-001, nerealizován) |
| 2026-08-13 | Vracející se rozhodnutí drž v jednom kanonickém artefaktu | Cena obratu roste s počtem míst, kde je zapsané odůvodnění, ne s počtem artefaktů | Ne |
| 2026-08-14 | Než popíšeš mechanismus jako platný, dočti odstavec "k dořešení" pod ním | Citovaná, formálně bezvadná odpověď může popisovat neaktivní/vyloučené chování | Ne |
| 2026-08-14 | Sladění dle vzoru z jiného projektu — ověř každý přenesený prvek zvlášť | Mandát "sjednoť podle B" je mandát pro pravidla, ne pro příklady/HW/topologii | Ne |
| 2026-08-14 | Pravidlo v accepted ADR bez brány je pravidlo, které se poruší | Brána kontrolovala jen start pole, ne konec — governance jako věta má autoritu, ne sílu | Ne |
| 2026-08-14 | Výjimku v bráně neodůvodňuj "dnes to nerozbije" | Výjimka se musí ověřit proti budoucím stavům artefaktu, ne dnešnímu obsahu | Ne |
| 2026-08-14 | Mezi analýzou a exekucí ověř znovu stav souboru — cizí ruka ho mohla přepsat | Zadání s "natvrdo" čísly řádků je pro agenta příkaz, ne hypotéza s expirací | Ne |
| 2026-08-14 | Cyklus oprava→revize nekonverguje, když nález je chybějící rozhodnutí, ne chyba textu | Po 2. kole roztřídit nálezy na "chyba textu" vs. "chybí rozhodnutí" a druhé eskalovat na člověka | Ne |
| 2026-08-15 | Než napíšeš "nemá vlastníka", přečti kandidátní dokument celý (Rozhodnutí+Validace, ne jen Rizika) | "Nikde není rozhodnuto" je nejsilnější tvrzení analýzy — nesmí stát na grepu | Ne |
| 2026-08-15 | Rozpor ohlášený třetím dokumentem ověř v OBOU dokumentech, které si mají odporovat | Převzatý rozpor je hypotéza s hotovým příběhem, ne nález | Ne |
| 2026-08-15 | Kontrakt s release-notes nahoře necituj čísly řádků — kotvi na jméno | Soubory rostoucí SHORA dělají čísla řádků strukturálně zastaralá hned první změnou | Ne |
| 2026-08-15 | Nedohledatelná kotva má dvě příčiny (posun vs. změna obsahu) — rozliš je před zápisem | Posunutou kotvu přečísluj; změněný obsah je věcný nález, ne údržba | Ne |
| 2026-08-17 | Subagent zablokovaný governance zámkem ho obchází delegací — zadávej roli "navrhni" | Zámek na zápisu je rozdělení rolí, ne překážka k vyřešení; explicitní zákaz delegace v promptu | Ne |
| 2026-08-17 | "Verified, already correct" od subagenta ověř vždy sám | Jediná kategorie výsledku bez diffu — nejméně spolehlivé tvrzení | Ne |
| 2026-08-17 | GOTCHA: `locationId` jako podřetězec `processLocationId` dá falešný poplach v grepu | Ověřovací grep potřebuje ohraničení hranice slova | Ne (technický gotcha) |
| 2026-08-17 | Vyvrácení JEDNÉ opory neopravňuje k výroku o VŠECH oporách tvrzení | "A a B" jsou dvě samostatná tvrzení; kvantifikátor "ani jedna" vyžaduje ověřit obě | Ne |
| 2026-08-17 | Grep na vlastní nález dřív, než ho prohlásíš za nový | Dřívější nezávislý záznam nálezu posiluje důkaz, ne ostudu | Ne |
| 2026-08-17 | GOTCHA: kategoriální ADR INDEX nesmí zmínit cizí ID ani v prostém textu | Validátor bere jakýkoli regex-match ID jako odkaz na soubor ve stejném adresáři | Ne (technický gotcha) |
| 2026-08-19 | Nález revizora je hypotéza — externí měření: precision jen ~21–31 %, druhé kolo je HORŠÍ | Bez triáže loop "oprav vše" systémově aplikuje mylné patche | Ne (silný kandidát, s externí citací arXiv) |
| 2026-08-19 | Číslo verze v changelogu urči z MAXIMA existujících, ne z pozice vkládání | Lexikografické čtení (3.10 vs 3.9) klame; 4 z 9 souborů kolidovaly | Ne |
| 2026-08-19 | GOTCHA: `@S<číslo>` v changelog komentáři TC hlásí validátor jako duplicitní scénář | Validátor hledá `@S` i v `#` komentářích | Ne (technický gotcha) |
| 2026-08-19 | Po opravě požadavku dorovnej i prozaické sekce TÉHOŽ dokumentu, které z něj vycházejí | Dílčí přepis seznamu (3 z 5 odrážek) zůstává plauzibilní a projde validátorem | Ne |
| 2026-08-19 | Po přečíslování verze dohledej křížové odkazy v JINÝCH souborech | Odkaz na starou verzi mimo editovaný soubor diff neukáže | Ne |
| 2026-08-19 | Neopravuj podle vlastní dřívější věty — přečti zdroj i když jsi ho psal ty | Vlastní parafráze zdroje v repu vypadá jako doklad, ale je jen tvrzení | Ne |
| 2026-08-19 | Ověř i ODŮVODNĚNÍ pravidla, ne jen pravidlo samo | Kauzalita se šíří rychleji než norma — nedoložené "proč" skončí v kontraktu i u zákazníka | Ne |
| 2026-08-21 | Autoritativní zdroj označíš explicitně → normativní tvrzení VŽDY z něj, ne z AI souhrnu jednání | AI souhrn přepisu je "rozcestník", ne citovatelný zdroj — otočil vlastníka rozhodnutí o 180° | Ne |
| 2026-08-21 | Edit vkládající řádek: pořadí v `new_string` rozhoduje směr vložení | Mechanická past bez ohledu na znalost pravidla — potřebuje mechanický vzor, ne jen paměť | Ne |
| 2026-08-21 | Frekvence výskytu v próze není autorita — u topologie/konfigurace rozhoduje init data nasazení | 12 dokumentů vs. 1 — většina byla špatně; strojová data nasazení měla pravdu | Ne |
| 2026-08-21 | Merge dvou dokumentačních větví: čísla changelogu kolidují tiše, git o tom mlčí | Prázdný řádek v tabulce a duplicitní verze nejsou v mergi vidět jako konflikt | Ne |
| 2026-08-21 | `sed -i` v Git Bash na Windows zahodí CRLF, `autocrlf` to schová v diffu | Working-tree efekt neviditelný v `git diff --cached` | Ne (technický gotcha) |
| 2026-08-22 | Anomálii ve strojových datech čti nejdřív jako záměr autora (4 z 5 "chyb" byly správně) | Data psaná odborníkem obsahují vědomé výjimky — vypadají zvenčí jako chyby | Ne |
| 2026-08-22 | Náhledový režim (`--apply` explicitní) jako výchozí u skriptu měnícího zdroj pravdy | Obrácené pořadí = první spuštění je ostré; kontrolní součty před/po jako pojistka | Ne |
| 2026-08-22 | Odolnost otisku/kotvy měř do budoucna (min. obsahu), ne jen jednoznačnost dnes | 95 %→99 % jednoznačnosti jednou podmínkou navíc — jednoznačnost dnes ≠ odolnost | Ne |
| 2026-08-23 | Filtr ve validátoru, který nic nehlásí o odmítnutém vstupu, hlásí "0" místo "nekontrolováno" | 5 % citací (79 z 1572) v souborech s mezerou v názvu nikdy nedostalo kotvu — ticho ve dvou vrstvách | Ne |
| 2026-08-24 | Co harness naservíroval do kontextu, není inventář, je výběr — počty ověřuj proti disku | 6 pravidel v kontextu vs. 12 na disku — vzorek k nerozeznání od úplného seznamu | Ne (silný, obecný kandidát) |
| 2026-08-24 | Globální metadata v hlavičce KAŽDÉHO derivátu poráží pojistku write-if-changed | 348 z 350 kopií hashe nikdy nikdo nečetl — "samopopisný soubor" je hypotéza | Ne |
| 2026-08-24 | Akční seznam v evidenci nese rámec dávky, ve které vznikl — ověř ho, neprováděj automaticky | Seznam přežil změnu rozhodovacího kritéria a vypadal nejautoritativněji právě proto | Ne |
| 2026-08-24 | Verdikt nástroje s uloženým otiskem je slepý ke všemu PŘED výrobou otisku | Otisk vznikl 10 minut po mergi, který měl zachytit — čerstvý otisk je nejnebezpečnější | Ne |
| 2026-08-24 | Číslo v dokumentu potřebuje generátor NEBO datum — jinak je to vzpomínka v hávu faktu | Drift: 4× mimo, dva dokumenty s různou velikostí téhož souboru | Ne |
| 2026-08-25 | Příloha e-mailu není dekorace — otevři a přečti, ne jen vypiš seznam | Odpověď "neurčitá" v textu byla konkrétní ve screenshotu přílohy (9 dní vedená jako chybějící) | Ne |
| 2026-08-25 | Existující evidenci hledej AKTIVNĚ dřív, než navrhneš novou (i mimo repozitář) | 3 plánovací větve zbytečné — kolega už měl hotový Excel model, v něčem lepší | Ne |
| 2026-08-25 | Metodika bez spouštěče (skill/command) je jen text, který se nepoužije | README+CLAUDE.md+návod nikdo nespustí — chybí skill s `description` a slash command | Ne |
| 2026-08-25 | Když technický argument mluví proti přehlednosti, hledej TŘETÍ variantu | "Nemůže se přesouvat" platí jen pro ruční přesun — skript podle záznamu dá obojí | Ne |
| 2026-08-25 | Časové razítko ve zdroji nemusí být ve stejné zóně jako evidence (UTC vs. lokální) | Rozdíl přesně o 1 den je typický projev zónového posunu, snadno se plete s překlepem | Ne |
| 2026-08-25 | Konvenci zápisu ověř proti validátoru a datům, ne proti žurnálu, který zaznamenává i úmysly | Žurnál popisoval nedokončený návrh jako by platil — validátor+data (653:0) řekly opak | Ne |
| 2026-08-25 | Rozdělení odpovědností mezi dodavateli PLC nededukuj z HW sousedství — ověř u vlastníka | Hranice vede podle FUNKCE (bezpečnost×pohyb), ne podle pracoviště; 2× špatná dedukce po sobě | Ne |
| 2026-08-25 | Soupis prvků nejdřív uzavři ("pokud jsem nezapomněl" = přiznaná neúplnost), pak se ptej na sémantiku | Otázka na chování neúplné množiny se opakuje — 2× dostal další čidlo místo odpovědi | Ne |
| 2026-08-25 | Jeden verdikt nástroje může slepovat dvě různé situace — rozděl ho dřív, než jde k člověku | 15 "zmizelých" kotev = 9 mechanika (okolí se posunulo) + 6 skutečné rozhodnutí; jméno verdiktu slibovalo víc, než měřil | Ne |

**Bilance AlzaSk:** z ~63 kandidátů povýšeno **5** (přímo nebo mergem) — všechny z prvních dvou
týdnů (2026-06-12 až 2026-06-18). **Od 2026-07-10 dodnes (2026-08-25, přes 6 týdnů, ~58 kandidátů)
nebyl povýšen ani jeden.** Personal zóna zůstává prázdná celou dobu.

### FHB (4 soubory, 2026-06-15 → 2026-08-24, 9 kandidátů)

| Datum | Název kandidáta | Destilovaná zásada | Povýšeno? |
|---|---|---|---|
| 2026-06-15 | Cizí klíče bez `default: ""` | FK pole nikdy neplň prázdným stringem, nech null/vynech | **Ano** → RULE-API-002 |
| 2026-06-15 | `maxLength` z DB domén; vstupy vždy omez | Limit odvoď z datového modelu; nedůvěryhodný vstup vždy ohraničit | **Ano** → RULE-API-003 |
| 2026-06-15 | Webhook payloady: prefix `Wh`, žádný suffix `Event` | Sjednocení s Alzou, "event" je interní pojem | **Ano** → personal RULE-API-004 (draft, nepovýšeno do shared) |
| 2026-06-15 | Žádný `oneOf`/`discriminator` — plochý model | Klient nesmí deserializovat 2× | **Ano** → RULE-API-005 |
| 2026-06-15 | Identifikátory s možnou multiplicitou → pole | Jeden callback může nést víc hodnot (více nosičů/tranzitů) | Ne (zůstalo jako ZVAŽ, nerealizováno) |
| 2026-06-18 | Vynucuj bránou, neinstruuj v promptu | Stejná zásada jako AlzaSk 06-18, potvrzena NEZÁVISLE ve 2. projektu | **Ano** → RULE-GOV-002 (přenos z AlzaSk, ale FHB výskyt posílil signál) |
| 2026-08-21 | Vrstvení dokumentů API kontraktu: koncept ⊃ README ⊃ YAML | Oprava se dělá v pořadí koncept→README→YAML, jinak se pravidlo napíše 2× | Ne |
| 2026-08-21 | Definici v dokumentaci měň jen na definičních místech, ne v popisných zmínkách | Rozlišení snížilo rozsah revize z ~20 míst na 6 | Ne |
| 2026-08-24 | Verzní bump kontraktu: stupeň z precedentu v souboru, historie append-only i v přehozeném pořadí | `x-release-notes` roste NAHORU, Markdown historie DOLŮ — stejné pravidlo aplikované naslepo by rozbilo jedno z nich | Ne |

**Bilance FHB:** z 9 kandidátů povýšeno **5** (4 do shared, 1 do personal draft) — výrazně vyšší
konverzní poměr než AlzaSk (56 % vs. 8 %), ale FHB inbox je i o řád menší a méně aktivní
(4 zápisy za 2 měsíce vs. 17 za AlzaSk).

---

## 6. Paměti (`~/.claude/projects/.../memory/`)

### AlzaSk (27 souborů + MEMORY.md index)

| Soubor | Typ | O čem |
|---|---|---|
| MEMORY.md | index | Rozcestník se stručným popisem + odkazy na všechny níže |
| feedback_changelog_order.md | feedback | Changelog na konec tabulky (předchůdce RULE-CL-001) |
| feedback_gate_not_prompt_pipeline.md | feedback | Brána>prompt (předchůdce RULE-GOV-002) |
| feedback_git_amend_pushed.md | feedback | Amend pushnutého commitu — ověřit `git status -sb` před destruktivní operací |
| feedback_mermaid_diagram_syntax.md | feedback | Mermaid syntaxe (žádné `;`, druhá `:`, `\n` jen ve state description) |
| feedback_no_commits_alzask.md | feedback | Nikdy nedělej commity v AlzaSk — commit/push dělá uživatel |
| feedback_plain_language_docs.md | feedback | Lidský jazyk v BACKLOG dokumentech, netechnický čtenář |
| feedback_plc_diagram_counter_last.md | feedback | `XCounter++` na konci řádku, publikační bariéra |
| feedback_plc_spec_external_audience.md | feedback | PLC spec je pro externího PAC — self-contained, žádné interní odkazy |
| feedback_pruzkum_criteria_auto_confirm.md | feedback | Kritéria kalibrace auto-potvrzena, pokračuj rovnou |
| feedback_review_workflow.md | feedback | Auto-fix bez schvalování, scope per oblast |
| feedback_simulace_verzni_razitko.md | feedback | Aktualizovat `.ver` razítko při změně PLC simulace |
| feedback_small_steps_one_question.md | feedback | Malé kroky, jedna otázka u doménových úloh |
| feedback_tc_no_delays.md | feedback | Žádné delay kroky v TC |
| feedback_tc_per_scenario_status.md | feedback | Per-scénář `@status`/`@updated` (předchůdce RULE-TC-001 rozšíření) |
| feedback_tc_read_full_methodology.md | feedback | Před tvorbou TC přečíst celou metodiku |
| feedback_worktree_handoff.md | feedback | Jasně sdělit git stav po práci ve worktree |
| project_ontologie_prvku_beh.md | project | Dávkový běh D1–D11 stavby registru ontologie |
| project_spec_factory_knowledge_loop.md | project | Historie Spec Factory + knowledge-loop v2, přechod na plugin |
| reference_bash_heredoc_backslash.md | reference | Bash heredoc žere zdvojené backslashe |
| reference_dodavatele_hw_terminologie.md | reference | Kdo je BullsEye/TMT/BlueSword/PAC |
| reference_mermaid_render_svg.md | reference | Kontrolovat diagramy jen textově, SVG jen na vyžádání |
| reference_pdf_pptx_extrakce.md | reference | Read nefunguje na PDF, použij pdftotext/PyMuPDF |
| reference_plc_ciselniky_linter_gap.md | reference | Číselníky, AccessState, linter mezera (mezaninové tabulky) |
| reference_polycamerapro_idle_burn.md | reference | Lokální perf issue — MSIX StartupTask |
| reference_posouzeni_rizik_clony.md | reference | EUCHNER posouzení rizik, SF 37 rozhraní |
| reference_statusline_npx_leak.md | reference | Statusline `npx -y @latest` zaplavilo stroj procesy |

### FHB (11 souborů + MEMORY.md)

| Soubor | Typ | O čem |
|---|---|---|
| MEMORY.md | index | Rozcestník |
| project_intake_coverage_gate.md | project | Intake coverage gate (FHB instance RULE-GOV-002) |
| project_spec_factory_plugin.md | project | Sjednocení Spec Factory do CC pluginu |
| feedback_terminologie_nosic.md | feedback | Terminologie (předchůdce RULE-TERM-001) |
| feedback_mermaid_semicolons.md | feedback | Mermaid znaky (předchůdce RULE-DIAG-001) |
| feedback_autori_plna_jmena.md | feedback | Plná jména autorů (předchůdce RULE-META-001) |
| feedback_vms_wms.md | feedback | WMS ne VMS |
| feedback_vms_objednavky.md | feedback | Objednávka na vyskladnění, ne požadavek |
| feedback_rezervace_portu.md | feedback | Rezervace výstupního portu |
| feedback_git_identita_commity.md | feedback | Git identita commitů (`tomis@kvados.cz`) |
| feedback_oddeleni_domen_spec_kl.md | feedback | Oddělovat Spec Factory od knowledge-loop |
| reference_cc_plugin_packaging.md | reference | Balení CC pluginů (`.claude-plugin/`, manifest) |

**Co patří do paměti vs. do pravidla — je v tom systém?** Ano, docela čistý:

- **`project_*`** = historie/stav jedné iniciativy (jak vznikl Spec Factory, jak proběhl běh D1–D11
  ontologie) — nečitatelné pro `paths:` glob, je to vyprávění o průběhu, ne pravidlo o chování
  v budoucích souborech.
- **`reference_*`** = fakta o prostředí/nástroji/dodavateli, která se nemají opakovat jako chování,
  jen si je připomenout (kdo je BullsEye, jak funguje PDF extrakce, že `npx -y` zabíjí stroj).
  Typicky jednorázová provozní znalost, ne konvence pro dokumenty.
- **`feedback_*`** = **předchůdce pravidla** — a to je hlavní pozorování: většina `feedback_*` souborů
  založených před zavedením knowledge-loop (do 2026-06-11) později **dostala pravidlo-dvojče**
  v `rules/shared/` (changelog, mermaid, terminologie, autoři, TC status). Po zavedení inboxu
  (od 2026-06-12) nové `feedback_*` soubory **skoro přestaly vznikat** — MEMORY.md je psal
  hlavně pro věci mimo dokumentační doménu (git, worktree, review workflow), zatímco dokumentační
  poznatky teď míří primárně do inboxu. To je zdravé dělení: **paměť = provozní/nástrojová
  poznámka pro mě; pravidlo = konvence vynutitelná přes `paths:` na dokument.**

**Kde systém drhne:** několik `feedback_*` položek v paměti (`feedback_small_steps_one_question`,
`feedback_plain_language_docs`, `feedback_review_workflow`) je svým obsahem **stejného druhu**
jako inbox kandidáti — obecná pracovní zásada, ne provozní detail — a přesto nikdy neprošly
inboxem ani nemají `paths:` scoping. Nejde o systém, ale o to, že vznikly PŘED zavedením
mechanismu (2026-03 až 2026-06) a nikdo je zpětně neopravil do nového formátu.

---

## 7. Životní cyklus: chyba → inbox → osobní → shared

**Reálná trasa u pravidel, která cyklus prošla:**

| Pravidlo | Inbox datum | Shared datum | Doba | Přes personal? |
|---|---|---|---|---|
| RULE-DIAG-001 (rect/wrap) | 2026-06-12 | 2026-07-07 | 25 dní | Ne (AlzaSk personal prázdné) |
| RULE-SPEC-004 | 2026-06-12 | 2026-07-07 | 25 dní | Ne |
| RULE-AP-002 | 2026-06-17 | 2026-06-17 (seed) | 0 dní | Ne |
| RULE-GOV-002 | 2026-06-18 (AlzaSk) | 2026-07-07 | 19 dní | Ne |
| FHB RULE-API-002/003/005 | 2026-06-15 | 2026-07-07 (generalizace do pluginu) | 22 dní | Ne (přímo do shared FHB, pak do pluginu) |
| FHB RULE-API-004 | 2026-06-15 | — (draft v personal, 2026-07-11) | 26 dní, **zaseklo se v personal** | Ano — jediný doložený případ použití personal vrstvy |

**Zjištění č. 1 — vrstva "osobní" se v praxi téměř nepoužívá.** V obou projektech dohromady
existují jen 2 osobní pravidla (obě FHB), obě `status: draft`. Cesta `inbox → shared` je
mnohem častější než `inbox → personal → shared`. Osobní vrstva slouží (podle FHB precedentu)
spíš jako **trvalé úložiště pro vědomě neuniverzální pravidlo**, ne jako povinná mezistanice.

**Zjištění č. 2 — konverze se v čase zastavila, ne zrychlila.** Prvních 5 povýšení AlzaSk proběhlo
během prvních 6 dní provozu inboxu (12.–18. 6.). Od 10. 7. do 25. 8. (46 dní, ~58 kandidátů,
nejhutnější a nejpropracovanější zápisy z celé kolekce) neprošel dál **ani jeden**. Mechanismus
degradoval na jednosměrný archiv: píše se do něj svědomitě, ale nikdo (ani člověk, ani agent)
nespustil `/knowledge-loop:rule-new` na nashromážděný materiál z posledních dvou měsíců.

**Zjištění č. 3 — doba mezi chybou a zápisem do inboxu je řádově minuty, doba mezi zápisem
a pravidlem je týdny až nikdy.** Samotný záchyt (psaní kandidáta) je rychlý a disciplinovaný —
kvalita a hustota textu roste (viz sekce 8). Bottleneck je **výhradně v kroku promoce**, který
vyžaduje samostatný lidský/agentní zásah a nikdo si ho nenaplánoval jako rutinu.

---

## 8. Typy opakujících se chyb (kategorizace napříč pravidly i kandidáty)

### A. "Měřím jiný jev, než jaký popisuji" — nejsilnější a nejexplicitnější rodina

Autor tuto rodinu sám pojmenoval a explicitně provazuje čtyřikrát v řadě (08-22 → 08-23 → 08-24
→ 08-25): diagnóza z agregátu místo z konkrétních položek (08-22), filtr, který mlčky zahazuje
vstup (08-23), harnessem vybraný kontext prezentovaný jako úplný inventář (08-24), verdikt
nástroje s otiskem starším než změna, kterou má zachytit (08-24), doslovný grep místo pokrytí
faktu (08-24 vedlejší nález). Společné jádro: **číslo/verdikt vypadá jako odpověď na otázku, ale
odpovídá na jinou, blízkou otázku.**

### B. "Rámec úlohy řídí retrieval, ne zdroj" (rodina RULE-AP-002)

Frame-first-then-evidence: 06-17 (bezpečnostní subsystémy odsunuté "mimo rozsah"), 07-10
(stavový efekt na entitu mimo rámec akce), 08-14 (sladění dle vzoru — přenos instance místo
pravidla), 08-21 (frekvence v próze bije data nasazení). Tohle je jediná rodina, která se
skutečně stala pravidlem (RULE-AP-002) — a přesto produkuje nové varianty i po povýšení, protože
každá nová doména (state efekty, cross-project sladění, topologická data) je nová instance téhož
kořene, kterou obecné znění pravidla nepokrylo předem.

### C. "Nezkontroloval jsem, co už existuje" (duplicitní práce)

RULE-AP-001 to má jako pravidlo od začátku ("nevytvářej nové entity tam, kde existuje
znovupoužitelné řešení"), ale kandidáti ukazují, že se to dál děje jinde: 08-25 (3 plánovací
větve místo dotazu na existující Excel), 08-17 (grep na vlastní nález — objev, který už měsíc
a půl ležel v repu).

### D. "Vynucuj mechanikou, ne textem/úmyslem" (rodina RULE-GOV-002)

Nejšíře rozkročená rodina: brána v pipeline (06-18), pravidlo v accepted ADR bez brány (08-14),
globální metadata bez čtenáře (08-24), metodika bez skillu/commandu (08-25), verdikt nástroje bez
diskriminátoru (08-25). Zásadní pro workshop: pravidlo samo o sobě (psané, schválené, "rozhodnuté")
má nulovou vynucovací sílu — až mechanismus, který ho testuje/spouští, dělá rozdíl.

### E. "Ověřený fakt má expiraci" (časová platnost citace/kotvy)

08-14 (cizí ruka přepsala soubor mezi čtením a editací), 08-15 (release notes posunují všechny
řádkové citace), 08-24 (kotva vyrobená PO mergi, který má zachytit, je slepá), 08-25 (časové
razítko v jiné zóně). Objevuje se výhradně od poloviny srpna — souvisí s prací na registru
ontologie, kde je citační kázeň nejvyšší a nejvíc testovaná.

### F. Mechanické/skriptovací "gotchas" (nekoncepční, ale opakované)

Changelog insert pozice (2×: 08-13, 08-21), číslo verze z pozice místo maxima (08-19), grep
substring bez ohraničení (08-17), `@S` v komentáři (08-19), `sed -i` a CRLF (08-21). Tahle
kategorie se **nikdy nepovýšila** navzdory tomu, že RULE-CL-001 (append-only changelog) existuje
od 2026-06-11 — viz sekce 9.

---

## 9. Vývoj v čase — zlepšila se kvalita?

**Ano, výrazně, ve dvou rozměrech:**

1. **Hustota a struktura.** Červnové zápisy (06-12 až 06-18) mají 1–3 odstavce na kandidáta.
   Srpnové (08-14 a dál) mají pravidelnou strukturu **Kontext → Kandidát na pravidlo → MUSÍŠ/
   NESMÍŠ/POZOR/ZVAŽ odrážky s "Detekovatelný signál" → Proč → Souvisí** — tedy sám formát
   zkonvergoval k šabloně, která odpovídá výslednému tvaru pravidla, ještě než pravidlo vzniklo.
2. **Typ chyby.** Červen–červenec: převážně **pipeline/governance** úroveň (jak má fungovat
   Spec Factory, brány, red-team). Od poloviny srpna: převážně **epistemické/verifikační** úroveň
   — "jak poznám, že tvrzení, které jsem právě podložil citací, je vůbec pravdivé" (podložil jsem
   ho špatnou vrstvou zdroje, zastaralou kotvou, vlastní dřívější parafrází, agregátem místo
   konkrétní položky). To je jemnější a těžší třída chyby než mechanická nebo procesní — vývoj
   od "jak stavět proces" k "jak nedůvěřovat vlastnímu závěru".

**Co se nezlepšilo:** frekvence promoce do pravidla (viz sekce 7) a mechanické "gotchas" v kategorii F
— tytéž typy skriptovacích chyb (pozice vkládání, číslování verzí) se vrací opakovaně v rozestupu
týdnů, přestože jsou zdokumentované.

---

## 10. Co se NEDODRŽUJE — doklady

### A. RULE-CL-001 (changelog append-only) — dodržováno formulačně, porušováno mechanicky

Pravidlo existuje od 2026-06-11 a jeho *znalost* autor nezpochybňuje ("znal jsem ho a v téže
session jsem podle něj jednou opravoval" — 08-21). Přesto se objevuje **minimálně čtyřikrát**
jako čerstvá chyba PO datu vzniku pravidla: 08-13 (`replace(anchor, new+anchor)` vloží před, ne
za), 08-19 (číslo verze z pozice místo maxima, 4 z 9 souborů kolidovaly), 08-21 (pořadí řádků
v `Edit new_string` — "dvakrát v jedné session"), 08-21 (merge dvou větví, kolize čísel, které
git nenahlásí). **Antipattern pro workshop:** pravidlo formulované jako věta ("na konec tabulky")
nepokrývá mechaniku nástroje (Edit, sed, skript), kterou se pravidlo provádí — potřebovalo by
vlastní **bránu** (`grep -n "^| [0-9]"` po dávce, kontrola posloupnosti verzí), přesně podle
RULE-GOV-002, které "vedle" existuje, ale nebylo na RULE-CL-001 aplikováno.

### B. RULE-AP-001 (grounding `soubor:řádek`) — základní princip dodržen, ale nová vrstva chyby
nezachycená

Autor cituje soustavně a diligentně (RULE-AP-001 samo je nejstarší a nejpoužívanější). Přesto
srpnové kandidáty ukazují **novou třídu selhání pod stejným pravidlem**: citace je formálně
správná (odkazuje na existující, ověřený text), ale **zdroj sám je špatná vrstva** — AI souhrn
místo transkriptu (08-21), vlastní dřívější parafráze místo originálu (08-19), próza místo
strojových init dat (08-21), kotva starší než merge (08-24). RULE-AP-001 v aktuálním znění tohle
nepokrývá (mluví o "existuje/neexistuje", ne o "je to ta správná vrstva/verze zdroje") — jasný
kandidát na rozšíření pravidla, ne jen na nový kandidát v inboxu.

### C. Samotná znalostní smyčka — vlastní princip "brána, ne prompt" na sebe neaplikovaný

Viz sekce 0 a 7. Postup `inbox → shared` je čistě manuální ("navrhuje agent/analytik, promuje
člověk" příkazem) — bez metriky, termínu nebo připomínky. Výsledek: 46denní, ~58položkový
backlog nikdy nezpracovaný. Kdyby existovala byť jen měkká brána (např. SessionStart hook
hlásící "N kandidátů v inboxu starších než X dní bez rozhodnutí"), věc, kterou RULE-GOV-002 sama
předepisuje pro každý JINÝ pipeline, by se aplikovala i tady.

---

## Kandidáti na náměty workshopu

**U — učení a znalostní smyčka**
1. Celý životní cyklus inbox→shared na živém příkladu (RULE-AP-002, 0 dní vs. RULE-DIAG-001,
   25 dní) — ukázat rozdíl "kandidát rovnou hotový" vs. "kandidát čekající na merge".
2. Antipattern: smyčka bez brány na sebe sama — 58 nepovýšených kandidátů za 46 dní. Diskuse:
   jak by měla vypadat brána/připomínka na promoci, aby se to týmu nestalo.
3. Osobní vs. sdílená zóna — kdy je pravidlo správně "navždy osobní" (FHB RULE-API-001/004),
   ne nedodělané sdílené.
4. Rozdíl paměť (`~/.claude/.../memory/`) vs. pravidlo (`.claude/rules/`) — kdy co, na živém
   srovnání `feedback_*` souborů, které mají pravidlo-dvojče, vs. těch, co ho nemají a proč.

**M — mechanika kvality**
5. Rodina "vynucuj bránou, ne promptem" (RULE-GOV-002) na 4 různých doménách (pipeline gate,
   ADR bez brány, metadata bez čtenáře, metodika bez skillu) — jeden princip, čtyři velmi
   odlišné projevy.
6. Mechanické changelog/verzovací gotchas (pozice vkládání, max vs. pozice, merge kolize) jako
   ukázka "znám pravidlo, přesto ho porušuju nástrojem" — proč pravidlo-věta nestačí.
7. Triáž nálezů revizora podle externě měřené precision (~21–31 %, arXiv citace 08-19) — silný,
   kvantifikovaný argument proti slepé aplikaci "oprav všechny nálezy".

**K — kontext a grounding**
8. Rodina "měřím jiný jev, než jaký popisuji" (08-22 až 08-25) — čtyři různé konkrétní pasti
   (agregát, filtr co mlčí, harness výběr, časově slepý otisk) spojené jedním kořenem; dobrý
   materiál na "jak si položit správnou kontrolní otázku".
9. Vrstva zdroje (AI souhrn vs. transkript, próza vs. init data, vlastní parafráze vs. originál)
   — RULE-AP-001 grounding nestačí, když je citovaná vrstva špatná.
10. "Ověřený fakt má expiraci" — kotvy/citace/verdikty nástrojů jsou platné jen vůči okamžiku
    vzniku, ne navždy; ukázat na příkladu kotvy vyrobené 10 minut po mergi.

**X — antipatterny**
11. RULE-CL-001 existuje 2,5 měsíce a dál se porušuje mechanicky — konkrétní doklad, že
    "psané pravidlo" ≠ "dodržované pravidlo" bez mechanického vynucení.
12. Subagent obchází governance zámek delegací, když dostane roli "oprav" místo "navrhni" —
    ukázka, jak formulace zadání může přímo podkopat existující bránu.
13. Kvantifikátorová přegeneralizace ("ani jedna opora neplatí", "nemá vlastníka") — jedna
    ověřená položka z více se generalizuje na celý výrok; opakuje se ve třech nezávislých
    kandidátech.

**N — nastavení a prostředí**
14. AlzaSk personal zóna je od založení prázdná (git log potvrzuje) — celá smyčka jede
    inbox→shared napřímo; diskuse, jestli je to úmysl nebo jen nevyužitá možnost.
15. `sed -i` na Windows/Git Bash tiše zahazuje CRLF a `autocrlf` to schová v diffu — praktický
    nástrojový gotcha nezávislý na doméně dokumentace.
