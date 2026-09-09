# Fáze 3b — Inventura tří vlastních pluginů Claude Code

Zdroj: `C:\Git\shared\plugins\{spec-factory,knowledge-loop,ontology-registry}\` + governance
marketplace v `C:\Git\shared\`. Čistě READ-ONLY průzkum (4 paralelní subagenti), nic nebylo
zapsáno mimo `C:\tmp\workshop-namety\`. Publikum workshopu: analytici, kteří Claude Code
používají, ale nikdy nepsali plugin — cíl je přenositelná zásada, ne návod na tento konkrétní
plugin.

---

# 1. spec-factory (verze 1.9.0)

`plugins/spec-factory/.claude-plugin/plugin.json:3` — autor „Martin Tomis + Claude" (`plugin.json:6-7`).
Registruje 2 příkazy (`/spec`, `/review-spec`), 8 agentů, 1 hook (guard). Klíčová slova
`guard`, `lint` v manifestu (`plugin.json:11`) prozrazují těžiště: není to jen sada promptů,
je to vynucovací mechanismus.

Popis v manifestu je sám o sobě kondenzovaná zásada (`plugin.json:4`): recenzent je záměrně
BLIND, protože „kdo zná záměr, přestane text zkoumat a začne ho obhajovat"; nález se
nedostane k člověku, dokud se ho někdo nezávislý nepokusí vyvrátit.

## 1.1 Osm agentů — dělba rolí

### spec-intake — příjem oddělený od exekuce
**Co to je.** Než se cokoli zeptá uživatele, sám navrhne hrubé řešení („straw-man") a z jeho
slabin odvodí konkrétní otázky. Technika „default inventory": nejdřív vlastní hypotéza,
teprve z jejích domněnek (`DOMNĚNKA:` + confidence, `agents/spec-intake.md:25`) otázky.
Bezchybná hypotéza je podezřelá — „obvykle znamená, že málo hledáš" (`agents/spec-intake.md:51`).

**Scope.** `tools: [Read, Grep, Glob]` — bez Write (`agents/spec-intake.md:4`). „Straw-man i
seznam otázek vracíš; persistuje orchestrátor... Jsi čistě analytik, oddělený od exekuce."
(`agents/spec-intake.md:12-13`). Zákaz: „NESMÍŠ... promovat straw-man do reálné specifikace
(osnovu a sekce píší planner/author, ne ty)" (`agents/spec-intake.md:15-16, 36`).

**Proč oddělený.** Straw-man je jednorázové lešení — kdyby ho psal stejný agent, co pak píše
finální sekce, hrozí tiché prosáknutí nepotvrzené hypotézy do specifikace.

**Přenositelná zásada.** Než se ptáte na požadavky, napište vlastní odpověď — teprve její
slabá místa řeknou, na co se skutečně zeptat; a kdo napíše hypotézu, nesmí být tentýž, kdo ji
promuje do finálního díla bez schválení.

**Předvedení naživo.** Dvěma kolegům dát stejné vágní zadání. Jeden nejdřív navrhne řešení a
označí nejistoty, druhý rovnou sepíše otázky. Porovnat konkrétnost otázek.

### spec-planner — architekt osnovy
**Co to je.** Sestaví osnovu — sekce, POI, sketch scénářů. WRITE jen do `outline.md`
(`agents/spec-planner.md:4,12-13`), sekce obsahu psát nesmí (`:15`).

**Klíčová mechanika — „Společné kontrakty".** Povinný blok sdílených entit, terminologie,
rozhraní a invariantů, „na kterých se sekce potkávají... jediný source-of-truth proti
divergenci fan-outu" (`agents/spec-planner.md:21-24`). Zásada dekompozice: „1 akceptační
kritérium = 1 úzká ověřitelná vlastnost" (`:31-32`).

**Přenositelná zásada.** Když více lidí píše paralelně části jednoho díla, napište napřed
jeden sdílený „slovník pravd" — jinak si každý dopíše vlastní verzi a rozpory se objeví až
při skládání.

**Předvedení.** Dva lidé píší kapitolu stejné zprávy bez domluvy vs. s předem dohodnutým
společným kontraktem na jedné stránce — porovnat konzistenci pojmů.

### spec-researcher — jediný agent s webem, web vypnutý defaultně
**Co to je.** Sbírá grounding z ≥3 nezávislých zdrojů, každé tvrzení s citací a mírou důvěry.
`tools: [Read, Grep, Glob, WebSearch, WebFetch]` (`agents/spec-researcher.md:5`) — jediný z
osmi s webem, a i ten defaultně vypnutý: „použij jen když ti orchestrátor v zadání předá
`web: enabled`" (`:11-12`).

**Systém důvěry.** `[C:high]` = ověřeno ≥2 nezávislými zdroji, oba citované inline. „Dvojí
citace téhož dokumentu (jiný řádek téhož souboru) = pořád jeden zdroj → `[C:med]`.
Self-certifikace bez druhého zdroje neprochází jako `[C:high]`" (`:33-34`). Povinný
`dropped_sources` log — „prázdné ≠ vynechané" (`:41-42`).

**Přenositelná zásada.** Míra důvěry v tvrzení je počitatelná vlastnost počtu *nezávislých*
zdrojů, ne subjektivní pocit — proces musí bránit „upgradu" důvěry bez druhého zdroje jen
proto, že to zní jistě.

**Předvedení.** Ověřit jedno tvrzení z interní dokumentace — ukázat rozdíl mezi „cituji
dvakrát tentýž dokument" (stále `C:med`) a dvěma skutečně nezávislými zdroji.

### spec-author — píše, ale smí formálně nesouhlasit (REBUTTAL)
**Co to je.** Píše jednu sekci, WRITE jen do `sections/<id>.draft.md` (`agents/spec-author.md:13-14`).
Vázán „Společnými kontrakty" — „nedomýšlej si vlastní variantu; mezeru v kontraktu nahlas
jako otevřenou, nezaplňuj" (`:16-17`).

**REBUTTAL.** „Nesouhlasíš-li s nálezem — patch by zanesl chybu, nebo nález odporuje
zdroji/ADR/šabloně — neaplikuj ho. Vrať `REBUTTAL: <id nálezu> — <důkaz citací zdroje>`...
o sporu rozhodne rozhodčí dispatch, ne ty. Slepá aplikace mylného patche je horší než spor"
(`:31-35`). Tvrdé pravidlo: `Priorita: MUSÍŠ` nesmí mít `Důvěra: C:low` (`:41-42`, vynuceno
DoD prahem `confidence_low_must_max: 0`).

**Přenositelná zásada.** Tvůrce obsahu musí mít legitimní právo formálně nesouhlasit s
revizní připomínkou — ale jen s důkazem, a spor rozhoduje třetí strana, ne autor sám.

**Předvedení.** Simulovat: recenzent dá autorovi připomínku odporující zdroji. Bez REBUTTAL
mechanismu se autor obvykle „poslušně" podřídí a text se zhorší.

### spec-critic — rubrikový soudce, BLIND
**Co to je.** Hodnotí sekci podle pevné rubriky (5 dimenzí, 1–5), jako by ji viděl poprvé.

**BLIND — přesná formulace.** „NESMÍŠ číst quality-report.md ani verdikty jiných soudců či
předchozích iterací... BLIND platí i pro metadata původu: nedozvíš se, kolikátá je to
iterace, zda je sekce 'revidovaná/opravená', kdo nebo jaký model ji psal — vědomí
'vylepšeného draftu' či jména autora systematicky posouvá hodnocení (refinement-aware /
compassion-fade bias)" (`agents/spec-critic.md:12-16`).

**Nejdřív zdůvodnění, pak číslo.** „Skóre generované současně s vysvětlením je měřitelně
méně přesné (zdůvodnění pak racionalizuje číslo místo aby ho určilo)" (`:22-24`).

**Proč oddělený od red-teamu.** „Adversariální red-team a holistiku dělá spec-redteam; ty
držíš ukotvenou rubriku" (`:7`) — dvě různé optiky se nemísí do jednoho posudku.

**Přenositelná zásada.** Hodnotitel, který ví, že hodnotí „vylepšenou verzi" nebo zná jméno
autora, hodnotí systematicky mírněji — objektivitu vynucuje záměrné odstínění kontextu
původu, ne dobrá vůle.

**Předvedení.** Dvě skupiny recenzentů, stejný text; jedné říct „toto je opravená verze od
seniorního kolegy", druhé nic — porovnat posudky (i na fiktivním příkladu jde ukázat efekt
formulace zadání).

### spec-redteam — má „zuby" (TEETH), je i rozhodčí
**Co to je.** Jediný agent, který vidí celou specifikaci najednou (HOLISTIC) a snaží se ji
rozbít; zároveň rozhoduje spory.

**TEETH.** „Každý nález MUSÍ mít konkrétní reprodukci (scénář / vstup / dvě protichůdná
čtení), ne obecnou obavu. Nález bez reprodukce VYŘAĎ... Ke každému ponechanému
major/critical nálezu navrhni právě jednu požadovanou akci: (a) revize požadavku, (b) nový
požadavek/akceptační kritérium, (c) explicitní rozhodnutí. 'Pouze zaznamenat / rozšířit
popis' NENÍ validní akce (kosmetika). Nález je vyřešený teprve konkrétní změnou — to
vynucuje DoD (`redteam_major_max`, 'otevřený' = bez akce)" (`agents/spec-redteam.md:46-55`).
„Každý nález = 'failující test'" (`:33`).

**Rozhodčí při neshodě.** Při neshodě soudců dostane jen spornou sekci + rubriku, BEZ
verdiktů a ostatních artefaktů; finální skóre = medián tří hlasů, ne průměr ani „lepší"
verdikt (`:57-63`).

**Rebuttal-search.** Dostane tvrzení bez kontextu, musí ho buď doslovně vyvrátit citací, nebo
napsat, kde hledal a nenašel — „chybějící potvrzení tvrzení NENÍ rozpor... to je umlčení, ne
rebuttal" (`:79-82`).

**Přenositelná zásada.** Nález, který nejde reprodukovat a nemá navrženou konkrétní akci,
není nález, je to obava — systém ho musí explicitně odmítnout, ne tiše zaznamenat jako
„vyřešený".

**Předvedení.** Vzít reálný komentář typu „tohle by mohl být problém" bez scénáře, nechat
účastníky navrhnout reprodukci + akci — kolik takových komentářů se rozpustí.

### spec-fix-verifier — mechanická verifikace, ne úsudek
**Co to je.** Levný (haiku) agent, jen mechanicky ověřuje, že se stalo přesně to, co mělo.
„Neděláš úsudek o kvalitě... Kvalitu posuzují spec-critic a spec-redteam, ne ty"
(`agents/spec-fix-verifier.md:7-8`). Verdikt opírá o **diff baseline → aktuální sekce**, ne o
dojem z finálního textu (`:20-21`).

**DIFF-CHECK syntézy.** „Vyjmenuj tvrzení/požadavky, které jsou ve finálu NAVÍC (syntéza
skládá, nesmí přidávat obsah). Navigace, obsah, formulační sjednocení nevadí; nové věcné
tvrzení ano" (`:24-26`).

**Přenositelná zásada.** Ne každou kontrolu musí dělat drahý expertní úsudek — mechanickou
otázku „stalo se přesně tohle, ano/ne" zvládne levný nástroj a je spolehlivější, protože
nemá prostor pro racionalizaci.

**Předvedení.** Porovnat před/po opravě — subjektivní posouzení kvality vs. mechanické
ověření přesné věty.

### spec-synthesizer — skládá, nepíše nový obsah
**Co to je.** Poslední krok, skládá schválené sekce do finálu + implementační prompt. „NESMÍŠ:
měnit význam požadavků, doplňovat nezdrojovaná tvrzení, kontaktovat web" (`agents/spec-synthesizer.md:15`).
Kontrolován hned fix-verifierem přes diff-check.

**Přenositelná zásada.** Krok „poskládat finální verzi z už schválených částí" musí zůstat
čistě mechanický — jakmile do něj vklouzne tvůrčí přidávání obsahu, obchází to celý
předchozí schvalovací proces.

## 1.2 Orchestrace — `/spec` a `/review-spec`

`/spec`: SETUP → INTAKE → PLAN → RESEARCH → DRAFT↔CRITIQUE (iterativní) → HUMAN GATE → SYNTH
(`commands/spec.md:60-241`), s bránami mezi fázemi:
- brána pokrytí před PLAN: `spec_lint.py --intake`, exit 2 = pokračuj v doptávání
  (`commands/spec.md:76-78`);
- CHECKPOINT po PLAN — osnovu schvaluje člověk (`:82`);
- BRÁNA DoD po každé iteraci: `spec_lint.py --dod`; exit 0 → další krok, exit 2 a iterace <
  max → další iterace, jinak eskalace na člověka (`:214-215`);
- HUMAN GATE — „Vyžádej explicitní souhlas uživatele. Bez něj nepokračuj." (`:229`).

Model matice: „Každé Workflow `agent()` volání MUSÍ nést explicitní `opts.model`... bez něj
agent dědí model hlavní session... a celý fan-out tiše jede na dražším modelu" (`:51-53`) —
konkrétní opakovaně zmiňovaná past.

`/review-spec` záměrně nepřidává nového agenta — skládá existující díly (`README.md:161-163`).
Sedm fází, klíčová TRIÁŽ dělá orchestrátor, NE agent: „Tato fáze se nesmí delegovat — je to
jediné místo, kde se dá zastavit falešný nález dřív, než někdo 'opraví' zdravý text. Ze tří
nálezů je pravý zhruba jeden i v nejlepším režimu; smyčka, která bere každý nález jako fakt,
ve dvou třetinách případů zanese chybu." (`commands/review-spec.md:130-132`).

**Přenositelná zásada (orchestrace).** Mezikroky víceagentového procesu potřebují ne
instrukci „prosím zkontroluj", ale měřitelnou bránu s binárním exit kódem — jinak se
pravidlo v dlouhém kontextu ztratí.

**Předvedení.** Rozdíl mezi „review checklist v hlavě" (snadno se přeskočí) a skriptem, co
spočítá pokrytí a vrátí exit 2.

## 1.3 Guard — technické vynucení „agent navrhuje, promuje jen člověk"

PreToolUse hook nad `Write|Edit|NotebookEdit` (`hooks/hooks.json:5`). Zkusí `python3`, pak
`python` (Windows Store alias problém, `hooks/spec-guard.py:18-20`).

Logika v `spec_guard_core.py`, funkce `decide()`:

**Rozpoznání člověk vs. agent.** `data.get("agent_type")` — chybí/prázdné nebo v
`guard.human_agent_types` (default `["claude"]`) → projde bez kontroly, „Hlavní (lidská)
session — píše volně" (`tools/spec_guard_core.py:118-120`).

**VRSTVA 1 — PROTECT.** Governance soubory (`CLAUDE.md`, `.claude/*`, `spec-config.yaml`,
plus `governance.adr_path|fr_path|analysis_path`, `grounding.pack_path`) chráněny pro
všechny automatické agenty:
```python
if _match(path, protect) and not _match(path, exceptions):
    return {"block": True,
            "reason": f"spec-guard: '{path}' — zápis do PROTECT zóny blokován "
                      "(governance/read-only). Agent navrhuje, promuje jen člověk."}
```
(`tools/spec_guard_core.py:130-133`) — doslovná citace principu je přímo v chybové hlášce.

**VRSTVA 2 — ALLOW.** Workspace běhu (`docs/spec/<task>/*`) smí zapisovat jen agent, jehož
typ začíná `spec-`:
```python
def _is_spec_agent(agent):
    return agent.split(":")[-1].startswith(SPEC_AGENT_PREFIX)
```
(`:55-59`) — funguje i pro kvalifikovaný `spec-factory:spec-author`.

**Přiznané limity.** „Fail-closed: chybný/neúplný vstup automatického agenta => block"
(`:18`), ale „i SystemExit/ImportError z jádra... lidská session se pouští fallbackem —
fail-closed platí jen pro automatické agenty" (`hooks/spec-guard.py:9-10,46-51`). Guard
přiznává mezery: „hook kryje jen Write|Edit|NotebookEdit... agent s Bash pokryt není" a
„agent_type 'claude' nelze odlišit od hlavní session... dispatchovaný catch-all subagent
typu 'claude' proto guardem projde" (`tools/spec_guard_core.py:20-25`).

**Přenositelná zásada.** „Agent navrhuje, člověk rozhoduje" není vynutitelné promptem ani
konvencí — potřebuje technickou bránu na úrovni nástroje, a ta musí čestně přiznat vlastní
meze, místo aby předstírala plný perimetr.

**Předvedení.** Spustit `spec_guard_core.decide()` dvakrát — s `agent_type: null` (projde) a
s `agent_type: "spec-author"` + cesta mimo workspace (zablokuje s konkrétní hláškou).

## 1.4 Tři brány `tools/spec_lint.py` (bez LLM)

Skript je „hloupý" — žádný model, jen regex a tabulky (`tools/spec_lint.py:1`). Rozlišuje
`[MECH]` (mechanická chyba, levný model opraví) vs. `[SUBST]` (věcná, autor musí doplnit
obsah/zdroj) (`:10-15`).

**T1 lint** (`lint_text`, `:111-188`) nad `sections/*.md`: placeholdery `TODO/FIXME/TBD/XXX`
jako celé slovo (`:66-68,115-121`), volitelně prázdné sekce, povinná pole požadavku
(`Priorita`, `Zdroj`, `Důvěra`, `Akceptační kritérium` — `:74,164-166`), enumy (`Priorita` ∈
`MUSÍŠ|MĚL_BY|MŮŽE`, `Důvěra` ∈ `C:high|C:med|C:low` — `:167-172`), vazby mezi poli
(`Důvěra: C:high` vyžaduje ≥2 zdroje, `:173-179`; `MUSÍŠ` + `C:low` zakázáno, `:180-185`).
Exit 2 i na prázdný glob (fail-closed — překlep v cestě se netváří jako „lint OK",
`:575-578`).

**Brána `--intake`** (`run_intake_gate`, `:273-301`): kontroluje pokrytí povinných bodů
rozsahu („miny": `SCOPE-IN`, `SCOPE-OUT`, `BOUNDARIES`, `ENTITIES-STATES`, `EXCEPTIONS`,
`NFR`, `OUTPUT-FORM` — `tools/spec-schema.yaml:29-35`), čtených primárně z grounding packu
projektu (`completeness.md`), config seam jen fallback (`:208-227`). Tabulka `Mina`/`Stav` v
`decisions.md`; pokrytá = `decided` nebo `deferred`. Chybí-li cokoli nebo je nepokrytá byť
jedna mina → exit 2, blokuje fázi PLAN (`:230-299`).

**Brána `--dod`** (`run_dod_gate`, `:343-430`): porovnává scorecard v `quality-report.md`
proti prahům `dod.*` (`redteam_critical_max: 0`, `grounding_ungrounded_max: 0`,
`rubric_min_per_dimension: 4` atd., `tools/spec-schema.yaml:209-262`). Chybějící řádek =
selhání (fail-closed, `:399-401`), nečíselná hodnota = selhání (`:407-410`), směr prahu se
pozná z názvu klíče (`_min`/`_max`, `:412-419`). Rozpozná LIGHT MODE a REVIZNÍ BĚH ze
`state.md`; při konfliktu vyhrává revizní podmnožina (`:370-392`, test
`test_dod_gate_review_mode_wins_over_light`). Exit 2 blokuje HUMAN GATE.

Brána vynucuje úplnost a aritmetiku prahů, ne pravdivost čísel — to zůstává na orchestrátorovi
(`:352-354`).

**Přenositelná zásada.** Co jde ověřit deterministicky, nikdy nesvěřuj posouzení modelem —
udělej z toho bránu s exit kódem, ne odstavec v promptu.

**Předvedení.** `python tools/spec_lint.py sections/priklad.draft.md` na sekci s chybějícím
`Zdroj` a `Důvěra: C:high` u jednoho zdroje → exit 2 s přesnou hláškou. Pak `--intake` na
workspace bez `decisions.md` → chyba, doplnit neúplnou tabulku → stále exit 2 s konkrétní
chybějící minou, doplnit poslední řádek → exit 0.

## 1.5 Config seam — `spec_config.py` + `spec-schema.yaml` (nejzajímavější mechanika)

Dvě vrstvy: jádrová `spec-schema.yaml` (výchozí hodnoty, v pluginu) a per-projekt
`.claude/spec-config.yaml` (v hostitelském repu). `load_config()` je slije při každém běhu
(`tools/spec_config.py:178-182`) — v kódu nástrojů není jediný natvrdo zadaný literál (`tools/spec_lint.py:16`).

**Merge (`_merge`, `spec_config.py:142-176`):**
- skalár: projekt přepíše jádro (`:173`);
- seznam: **union** — `list(dict.fromkeys([*base, *add]))`, zachová pořadí, bez duplicit
  (`:157-160`);
- odebrání ze seznamu: **jen** přes explicitní klíč `<klíč>_remove` (`:161-164`);
- imunní seznamy: `guard.protect_list` a `guard.human_agent_types` — i po `_remove` se
  jádrové záznamy vrátí zpět (`:55-58,165-168`).

Implementace:
```python
rm = project.get(k + "_remove")
if isinstance(rm, list):
    rmset = set(rm)
    merged = [x for x in merged if x not in rmset]
    if path + (k,) in IMMUTABLE_LIST_PATHS:
        for x in base:
            if x not in merged:
                merged.append(x)
```
(`spec_config.py:161-164`). Klíč `<klíč>_remove` sám nikdy nevstupuje do výsledku jako
svébytný klíč (`:150-151`).

**Proč union + explicitní remove, ne prostý override.** Prostý override by mohl tiše ztratit
jádrový bezpečnostní záznam, kdyby projekt „zapomněl" ho zopakovat celý seznam znovu —
ochranu proti tomu kryje i to, že `spec-config.yaml` je sám v jádrovém `protect_list`
(`:52-54`). Explicitní `_remove` dělá odebrání viditelným úmyslným úkonem v diffu configu.

**Ukázka.** Jádro (`tools/spec-schema.yaml:169-186`) definuje `review.brief_forbidden_patterns`
s ~10 regexy (mj. `(?i)(?<![\w-])iterac\w*`). Projekt (`templates/spec-config.example.yaml:42-52`)
přidá `review.linters` (jádro má prázdné `[]`) a odebere jeden vzor přes
`brief_forbidden_patterns_remove: ['(?i)(?<![\w-])iterac\w*']`. Výsledek: `review.linters` =
jen projektový přídavek; `brief_forbidden_patterns` = 9 z 10 jádrových vzorů, o zbylém
odebrání projekt nemusel ani vědět u ostatních devíti.

Test `test_protect_list_core_immutable` (`tools/tests/test_spec_config.py:24-30`) demonstruje
nejčistěji: jádro `protect_list = ["CLAUDE.md", ".claude/*"]`; projekt pošle
`protect_list: ["x/*"]` a `protect_list_remove: [".claude/*", "x/*"]` → `.claude/*` **zůstává**
(immutable), `x/*` **mizí** (byl přidán a odebrán ve stejném YAML).

**Přenositelná zásada.** Rozšiřitelnost per-projekt configu neznamená „projekt smí cokoli
přepsat" — bezpečnostně kritické položky drž jako union s explicitním viditelným
odebráním, jádrové minimum udělej fyzicky neodstranitelným.

**Předvedení.** `python tools/spec_config.py --dump` bez a s projektovým `spec-config.yaml` —
porovnat výsledný seznam vedle sebe. Pak `pytest tools/tests/test_spec_config.py -k
protect_list_core_immutable -v`.

## 1.6 Workspace mechanika — `spec/<YYYY-MM-DD_slug>/`

Každý běh dostane vlastní adresář (`workspace.base_path`, default `docs/spec`,
`tools/spec-schema.yaml:44-46`) s `research/`, `sections/`, a kanonickými soubory
(`state.md`, `decisions.md`, `outline.md`, `straw-man.md`, `cost-ledger.md`,
`quality-report.md`, `commands/spec.md:226-228`).

Proč izolace:
1. **Bezpečnostní hranice pro guard** — ALLOW zóna je odvozená přesně z `workspace.base_path`
   (`tools/spec-schema.yaml:121-124` — přepis base_path per-projekt nevyžaduje ruční úpravu
   allow_list).
2. **RESUME** — `state.md` nese fázi/iteraci/run_id, přerušený běh se dá obnovit z disku
   (`commands/spec.md:35-39,243-250`).
3. **Náklady per běh** — `cost-ledger.md` řádek za fázi/iteraci s modelem (`:54-58`).
4. **Regresní pojistka** — draft se před opravou kopíruje do `sections/.history/<id>.it<N>.md`,
   protože kvalita přes iterace není monotónní (`:188-191`).
5. **Úklid** — v HUMAN GATE se smaže vše necanonické, po syntéze i `.history/` snapshoty
   (`:226-228,236-237`).

Výstup SYNTH: `final-spec.md` + `implementation-prompt.md` uvnitř téhož workspace (`:232`) —
kam se hotový dokument natrvalo přesune (v AlzaSk `docs/specs/`), plugin sám nepředepisuje,
je to konvence hostitele.

**Přenositelná zásada.** Dej každému běhu vlastní adresář s vlastním strojově čitelným
stavem — omezuje, kam smí automatický agent zapisovat, umožňuje bezpečné přerušení/návaznost,
drží náklady i historii jedné úlohy pohromadě.

## 1.7 Researcher schema a grounding pack

`tools/researcher-schema.json` — verzovaný JSON Schema kontrakt výstupu spec-researcher,
předávaný jako `opts.schema` (`commands/spec.md:106-109`). Vynucuje povinná auditní pole
`web_mode` a `dropped_sources` (s hodnotou „nic nezahozeno" místo prázdna) —
strukturálně, ne prosbou v promptu (`researcher-schema.json:31-46`).

`templates/grounding/completeness.md` — manifest scoping-min (zdroj pravdy pro `--intake`) +
doménový checklist úplnosti, ze kterého planner odvozuje POI. `rubric.md` — 5D rubrika
(D1 Jednoznačnost, D2 Konzistence, D3 Úplnost, D4 Trasovatelnost/důvěra, D5 Testovatelnost;
D3+D5 high-stakes, dva soudci + rozhodčí). `spec-requirement.md`/`spec-section.md` — šablony,
explicitně vázané na `lint.required_labels/priority_values/confidence_values` z configu —
„linter vynucuje config, ne šablonu" (`spec-requirement.md:3-4`).

**Přenositelná zásada.** Šablona k vyplnění a pravidlo, které stroj kontroluje, musí být
odvozené ze stejného zdroje configu — jinak šablona slibuje flexibilitu, kterou linter
odmítne.

## 1.8 Co odhalují testy — fail-closed jako systematický vzor

`tools/tests/test_spec_lint.py` (~55 testů), `test_spec_config.py` (~20 testů). Vybrané
edge-case testy:
- `test_dod_gate_review_mode_wins_over_light` — dva protichůdné signály ve `state.md`,
  revizní vyhrává.
- `test_protect_list_core_immutable`, `test_human_types_core_immutable` — imunita jádrových
  seznamů; komentář přiznává, že `guard.protect_exceptions` dřív imunní byl a přestal být,
  když znalostní smyčka opustila plugin (historická stopa).
- `test_intake_gate_unparseable_manifest_fails_closed` — neparsovatelný manifest ⇒ tvrdé
  selhání, ne tiché přeskočení.
- `test_placeholder_exclude_is_real_glob` — vyloučení placeholderů je opravdový glob, ne
  substring match.
- `test_dod_gate_findings_rejected_decimal_comma` — brána zvládá českou desetinnou čárku.
- `test_dod_gate_findings_rejected_missing_row_fails_closed` — chybějící řádek metriky ≠
  automatická nula.

**Zastřešující zásada z testů.** Design „raději zablokuj, než pusť nejistotu" se musí ověřovat
testem na každou hranu (chybějící soubor, chybějící sloupec, dva protichůdné signály), jinak
zůstane jen prohlášením v komentáři.

## 1.9 README a historie — co se v provozu neosvědčilo

README nemá formální Changelog, ale obsahuje de facto changelog v textu — tři konkrétní
příběhy „zkusili jsme, nefungovalo, nahradili jsme":

1. **Druhé kolo stejného soudce nepomáhá.** „Druhé kolo soudu ve stejném rámci nepomáhá
   vůbec (21,0 % precision; SR vs. SR2 p = 0,11). Proto se po opravě nedělá nový soud, ale
   mechanická kontrola proti diffu." (`README.md:50-51`) — přímé zdůvodnění existence
   spec-fix-verifier místo dalšího kola spec-critic.

2. **Rubrikové skórování v revizním režimu selhalo naprázdno.** „V produkčním běhu jen
   zablokovala bránu (skóre 3 proti prahu 4), aniž přinesla jediný nález — všechny věcné
   nálezy dodaly adversariální optiky." (`README.md:56-59`) — proto `/review-spec`
   rubriku nepoužívá.

3. **Eskalace bez pokusu o vyvrácení se v praxi neprovedla.** „V produkčním běhu se pokus o
   vyvrácení neprovedl ani jednou a dva ze tří nejzávažnějších nálezů se pak rozpadly až na
   dotaz člověka. Pravidlo napsané do dlouhého promptu se v běhu ztratí; brána se spustí
   pokaždé." (`README.md:88-91`) — nahrazeno tvrdým prahem 0 v DoD.

4. **Znalostní smyčka byla z pluginu vyjmuta.** Git commit `f6cd048` (2026-07-08): „docs:
   Znalostní smyčka vyjmuta ze SpecFactory a vrácená do projektů" — mechanika, která byla
   uvnitř spec-factory, se ukázala jako projektová záležitost a stala se samostatným
   pluginem knowledge-loop. Nejsilnější doklad zrušené/přepracované mechaniky.

**Vědecké kotvení jako princip.** README cituje konkrétní studie s arXiv identifikátory jako
zdůvodnění designu (`README.md:46-54`) — design rozhodnutí je odolnější, když je podložené
měřením nebo produkčním incidentem, ne obecným tvrzením.

**Rekonstruovaná historie verzí (git log `plugins/spec-factory/`):**

| Datum | Commit | Co a proč |
|---|---|---|
| 2026-07-04 | `f24f5f8` | Vznik sdíleného pluginu (přesun z projektové kopie) |
| 2026-07-04–05 | `b8a2946,3801089,66d3f88` | Technické doladění po přesunu |
| 2026-07-07 | `ce0625e` | Optimalizace přes Fable 5 |
| 2026-07-08 | `d787f3e` | Přidání obecných pravidel |
| 2026-07-08 | `f6cd048` | **Znalostní smyčka vyjmuta** — vrácena do projektů |
| ~2026-08 | `d5d001a,4c28b90` | Srozumitelnější README, instalace |
| ~2026-08 | `99d01dd` | OUTLINE-REVISION zpětná smyčka po research |
| 2026-08-19 | `af00b5e` | **v1.8.0** — přidán `/review-spec` + `findings_rejected_ratio_max` |
| 2026-08-21 | `31517cd` | Zastavení falešných nálezů v `/review-spec` |
| nejnovější | `79368d3` | YAGNI principy do `/review-spec` |

**Shrnutí spec-factory jednou větou.** Kvalita procesu nestojí na snaze účastníků — stojí na
oddělení rolí, které by se jinak kontaminovaly (autor/recenzent, hypotéza/exekuce,
návrh/schválení), a na vynucení klíčových pravidel měřitelnou bránou s binárním výsledkem,
ne instrukcí v promptu; co se v provozu neosvědčilo, se skutečně odstraní.

---

# 2. knowledge-loop

Cíl: opakovaná lidská zpětná vazba se nemá odříkávat pořád dokola — zachytit jednou, stát se
pravidlem, objevit se agentovi přesně tam, kde je relevantní, bez nafukování kontextu a bez
prozrazení cizích poznatků.

## 2.1 Čtyři zóny a tři vrstvy

| Zóna | Cesta | V Gitu? | Auto-load? |
|---|---|---|---|
| Záchyt (inbox) | `.claude/knowledge-inbox/<handle>/` | ano | ne (jen hook na startu) |
| Osobní (zdroj) | `.claude/rules-personal/<handle>/` | ano | **ne** |
| Zrcadlo (kopie) | `.claude/rules/personal/<handle>/` | **ne (gitignored)** | ano, jen vlastní |
| Sdílená | `.claude/rules/shared/` | ano | ano |

(`README.md:29-34`) Tohle je nosná kostra — všechny ostatní mechaniky existují, aby tuto
tabulku udržely pravdivou.

## 2.2 Tok: inbox → rules-personal → shared

**Krok 1 — záchyt.** Claude sám za běhu, když v lidské zpětné vazbě rozpozná *opakovaný*
vzor (ne jednorázovou úpravu), tiše připíše blok do
`.claude/knowledge-inbox/<handle>/<YYYY-MM-DD>.md` (`README.md:98-100`). Žádné přerušení
práce.

**Krok 2 — `/rule-new`.** (`commands/rule-new.md`): zjistí handle (`git config --local --get
knowledge-loop.user`, případně zeptá), doptá se na téma/druh/závaznost/`paths:` (v osobní
zóně povinné, `:18-19`), založí soubor **do osobní zóny**, nikdy přímo do `rules/shared/` ani
do generovaného zrcadla (`:21-26`), přidělí ID `RULE-{OBLAST}-{SEQ}` (nejvyšší SEQ napříč
zónami + 1, `:27-34`), spustí validátor, a **zkopíruje soubor i do zrcadla**, aby platilo
hned v běžící session bez restartu (`:37-40`).

**Krok 3 — `/rules-consolidate`.** Na vyžádání přečte cizí inboxy a cizí osobní zóny — jediné
sankcionované cross-author čtení v systému (`commands/rules-consolidate.md:12-15`). Shoda
napříč autory (stejný vzor u ≥2 lidí = silný kandidát na shared, `:23-25`), slučuje
duplicity, u nerozhodnutelných konfliktů eskaluje člověku (`:27-29`), výsledek je MR-friendly
diff do `shared/` (`:34`). Originály se nemění, povýšené pravidlo v osobní zóně autora je jen
označeno ke smazání — maže si ho autor sám (`:36`).

**Přenositelná zásada.** Odděl rychlost zachycení poznatku od váhy jeho důsledku — čím dražší
je pravidlo prosadit na všechny, tím vyšší schvalovací bariéra, ale zachycení musí zůstat
bezbariérové.

**Předvedení.** Ukázat existující `.claude/knowledge-inbox/<handle>/2026-08-*.md` v repu
AlzaSk; spustit `/knowledge-loop:rule-new` na vymyšleném opakovaném poznatku; ukázat vznik
souboru v `rules-personal/` i jeho promítnutí do `rules/personal/` (zrcadlo).

## 2.3 SessionStart hook — dodávka do session, zjištění handle

`hooks/session-context.py` — přesynchronizuje zrcadlo a vloží do kontextu identitu, index
vlastních pravidel a čerstvý obsah vlastního inboxu.

**Zjištění handle** — primárně `git config --local --get knowledge-loop.user`, fallback
`KNOWLEDGE_LOOP_USER`:
```python
def _handle(project):
    try:
        r = subprocess.run(
            ["git", "config", "--local", "--get", "knowledge-loop.user"],
            cwd=str(project), capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    return os.environ.get("KNOWLEDGE_LOOP_USER") or None
```
(`hooks/session-context.py:54-63`). `git config --local` píše do `.git/config` daného klonu —
mimo pracovní strom, nejde omylem commitnout, nutně per-vývojář-per-klon (`README.md:45-47`).

**Co přesně dodává** (`session-context.py:230-256`): identita + cesty zón vždy; sync-hláška
pokud relevantní; **index** vlastních pravidel (1 řádek/pravidlo, strop `personal_index_max`
default 15, `:171-176`); obsah vlastního inboxu za posledních `days` (default 14), strop
`max_lines` (default 120, `:179-207`). Plný text pravidel nedodává hook — ten přijde
přirozeně přes nativní path-scoped auto-load. Fail-safe: chybějící handle/Python/`.claude/rules/`
→ tichý no-op, session neselže (`:20-23,213-222,259-267`).

**Přenositelná zásada.** Identitu odvozuj z mechanismu, který nejde omylem sdílet nebo
commitnout (per-clone git config), a kontext na startu dávkuj podle skutečné potřeby — index
hned, plný obsah až na vyžádání.

**Předvedení.** `git config --local --get knowledge-loop.user` v terminálu; `echo {} | python
hooks/session-context.py` a ukázat přesný blok textu, který vidí Claude na startu.

## 2.4 Zrcadlo `.claude/rules/personal/` — proč kopie, ne přímé čtení

Nativní auto-load Claude Code funguje nad `.claude/rules/` plošně podle cesty, nerozlišuje
„moje" od „cizí". Kdyby `rules-personal/` ležela uvnitř `.claude/rules/`, načítal by se
obsah všech autorů. Řešení: `rules-personal/` je záměrně **mimo** `.claude/rules/`
(`README.md:32-33`, `templates/personal-README.md:6-7`); auto-load čte jen
`.claude/rules/personal/` (zrcadlo), do kterého hook kopíruje výhradně soubory patřící
danému handle (`_sync_mirror`, `session-context.py:119`; `_clear_dir` smaže vše, co není v
`keep`, `:91-106,122-123`).

Doslovně: „Jen zrcadlo se nativně auto-loaduje → cizí osobní pravidla se do session NIKDY
nenačtou — fyzicky tam nejsou." (`session-context.py:8-9`).

Pojistka: pokud je pod zrcadlem něco git-tracked (přechodný stav „v1"), sync se celý
přeskočí, nic se nemaže (`:79-88,112-114`; test `test_mirror_sync_skips_tracked_interim`,
`tools/tests/test_session_context.py:89-106`). Zrcadlo je vyloučeno z validace, jinak by
vznikaly falešné duplicitní konflikty se zdrojem (`validate.py:262-263`; test
`test_mirror_zone_is_skipped`).

**Přenositelná zásada.** Když potřebuješ „viditelné pro tým, ale závazné jen pro autora",
nefiltruj přístup logikou — polož zdroj mimo dosah automatického mechanismu a do jeho
dosahu generuj jen výslovně povolenou podmnožinu.

**Předvedení.** `git status` — zrcadlo se v něm neobjeví (gitignore blok
`## Knowledge-loop-mirror-Start/End`, `tools/loop_config.py:72-79`). Ručně upravit soubor v
zrcadle a restartovat session — přepíše se zpět podle `rules-personal/`.

## 2.5 CODEOWNERS napojení

Dvě role: (1) ochrana vlastní zóny — doporučený řádek `/.claude/rules-personal/<handle>/
@<handle>` (generuje `--init` jako TODO, `tools/loop_config.py:282-283`); (2) schvalování
povýšení do `shared/` — `rules-consolidate.md:34-35`: „produktové MUSÍŠ/NESMÍŠ → architekt;
implementační → senior analytik domény; ZVAŽ → lehčí režim" — konsolidační agent bere v
úvahu, kdo bude podle CODEOWNERS reálně schvalovat.

**Přenositelná zásada.** Slib „agent jen navrhuje, člověk schvaluje" je věrohodný pouze
tehdy, když ho vynucuje nástroj mimo agenta (branch protection + CODEOWNERS), ne jen
formulace v promptu.

## 2.6 Precedence pravidel

**Project accepted-ADR > project shared > cross-project shared > vlastní personal >
doporučení (ZVAŽ).** Nejexplicitněji `README.md:70-79` a `templates/rules-README.md:40-45`
(kopíruje se do každého hostitelského projektu). **Není** vynucené číselnou prioritou v
`schema.yaml` — je to konvence pro čtenáře (agenta), ne mechanická kontrola. Mechanicky
vynucené je jen: (a) cizí osobní pravidla se fyzicky nenačtou (zrcadlo); (b) konflikt
shared×shared je `ERROR`, konflikt s osobní stranou jen `WARNING` (`validate.py:180-205`) —
nepřímé posílení precedence shared > personal.

**Přenositelná zásada.** Precedenci mezi zdroji pravdy napiš jako jednu jasnou větu na
jednom místě a zopakuj na všech vstupních branách — a kde to jde, dorovnej mechanickou
kontrolou, protože textová instrukce sama slibuje méně než brána.

**Předvedení.** Vytvořit protichůdná pravidla v `shared/` a `rules-personal/<handle>/` na
stejné `paths:`, spustit `validate.py` — ukázat `WARNING`, ne `ERROR` (na rozdíl od
shared×shared).

## 2.7 `validate.py` a `loop_config.py`

**`validate.py`** nad `rules/` + `rules-personal/`, přeskakuje zrcadlo a legacy `_personal/`
(`:250-263`): povinná pole frontmatteru (`validate.py:96-99`, `schema.yaml:7-16`), enum
hodnoty (`:102-104`), regex `id`/`date` (`:106-110`), konvence názvu souboru (warning,
`:112-116`), `paths:` povinné v osobní zóně (`:118-123`), povinné sekce a marker `PLATÍ
KDYŽ:` (`:125-131`), detekce konfliktů (protichůdný `enforcement` ve stejné oblasti na
překrývajícím se scope, pokud dvojice nemá `related_rules` — `:180-205`), rozpočet (víc než
`budget.personal_max_rules`, default 10, `:208-220`). Exit 0/1/2, `--strict` počítá i
varování jako 2 (`:296-301`).

**`loop_config.py`** — stav/topologie: `--init` bootstrapuje zóny, **nikdy nepřepíše
existující soubory** (`:243-288`); `--migrate` zvládá legacy v0/v1 stavy idempotentně
(`:314-391`); `--check` preflight (chybí `.claude/rules/`, chybí handle, zbytky staré
smyčky, zrcadlo git-tracked bez gitignore bloku — což by způsobilo auto-load cizích pravidel,
`:435-464`); `--dump` (`:535-537`). Merge configu: skalár přepíše, list = union
(`_merge`, `:174-196`), s výjimkou `personal_root`/`mirror_zone`, které se nesmí přepisovat
per-projekt (`schema.yaml:64-69`).

**Přenositelná zásada.** Odděl bránu na *obsah* (formát, konflikty pravidel) od brány na
*stav instalace mechaniky samotné* (zbytky staré verze, porušená neviditelnost) — obě řeší
různé třídy chyb.

## 2.8 Historie a evoluce (zjištěno z komentářů v kódu, žádný CHANGELOG.md)

- **v0 (legacy)** — gitignorovaná `_personal/`, žádné sdílení v Gitu (`loop_config.py:65-66`).
- **v1 (mezistav)** — osobní pravidla přímo v `.claude/rules/personal/<autor>/`, tedy
  **committed přímo v auto-load stromu** — cizí osobní pravidla se reálně auto-loadovala
  všem (bezpečnostní díra, `loop_config.py:339-341`, `session-context.py:10-11`).
- **v2 (současné jádro)** — oddělení zdroje od gitignored zrcadla (bod 2.4).
- **v3** — přidán rozpočet a `inbox_inject` limity.
- **v4 (aktuální)** — konflikty osobní zóny = warning ne error; `personal_root`/`mirror_zone`
  neopravitelné konstanty.

`--migrate --force` umí smazat starou hostitelskou duplicitu mechaniky (`.rules-tools/`,
`_templates/`) — stopa doby, kdy validace a šablony ještě nebyly plugin (`:375-387`).

**Zásada z historie.** Bezpečnostně citlivá vlastnost („cizí věci se nenačtou") se nesmí
spoléhat jen na konvenci umístění v jedné verzi — potřebuje mechanickou pojistku (`--check`
detekující tracked mezistav) i bezpečný idempotentní migrační skript.

---

# 3. ontology-registry

## 3.1 Co dělá `/init`

Instalátor, ne běhové prostředí. Založí v cílovém repu kostru `docs/ontology/`
(`ontology.yaml`, `conflicts.md`, `coverage.md`, `NAVRHY.md`), zkopíruje devět nástrojových
skriptů do `docs/ontology/.ontology-tools/`, založí
`docs/onboarding/PROMPT-ontologie-prvku.md`. **Do žádného konfiguračního souboru projektu
sám nezapisuje** — governance soubory mají vlastníka:

„[4/4] Integracni radky -- VLOZTE RUCNE (governance soubory patri cloveku)"
(`tools/ontology_init.py:139-141`). Čtyři integrační místa: `review.linters` +
`guard.protect_list` v `spec-config.yaml`, SessionStart hook v `settings.json`, sekce v root
`CLAUDE.md`, tři pravidla `RULE-ONT-001..003` do `.claude/rules/shared/` (`:161-199`,
`commands/init.md:56-64`). Nezakládá data (`commands/init.md:95`) a necommituje
(`commands/init.md:77`).

Timing pojistka: `review.linters` se přidává **až po dávce D1**, jinak by prázdný registr
shodil `reanchor.py --check` na exit 2 a shodil každé `/review-spec` (`README.md:83-84`).

**Přenositelná zásada.** Instalátor smí *vypsat*, co se má do cizí konfigurace vložit, nikdy
to nesmí vložit sám — vlastnictví governance souborů je důležitější než pohodlí jednoho
příkazu.

**Předvedení.** `python tools/ontology_init.py --init C:\tmp\demo-projekt --project Demo` na
testovacím adresáři — ukázat, že vypíše 4 bloky k ručnímu vložení a `git status` v cílovém
adresáři ukáže, že `.claude/` zůstal nedotčený.

## 3.2 Jaký problém řeší

README: „znalost o systému je rozsypaná do desítek dokumentů, které vznikaly nezávisle a
místy si odporují." Tři funkce v pořadí důležitosti: (1) jedno místo pravdy, (2) **seznam
rozporů** s určením, který zdroj platí — označeno jako nejcennější výstup, (3) čitelný
přehled pro člověka (`README.md:8-11`). Manifest dokládá číslem: „79 % citací se za třicet
dní posune" (`.claude-plugin/plugin.json:4`).

Plugin registr **nespravuje, jen zavádí** — registr žije celý v projektu, kdokoli repo
naklonuje, má vše funkční bez pluginu (`README.md:14-27`): údržba kotev běží nad daty
projektu; atomicita (schéma+nástroj+data v jednom commitu); brány spec-factory očekávají
cesty relativně ke kořeni projektu.

**Přenositelná zásada.** Když je znalost rozptýlená do desítek nezávisle vznikajících
dokumentů, nejcennější artefakt registru není přehled „co víme", ale seznam „kde si zdroje
odporují a proč vyhrává tenhle".

**Předvedení.** Otevřít reálný `docs/ontology/conflicts.md` na AlzaSk, ukázat jeden zápis
`Cxxx` se dvěma citovanými tvrzeními a rozhodnutím, které platí.

## 3.3 Mechanika kotev (anchors)

Kotva = otisk (SHA1) *obsahu* na místě, ne číslo řádku. `anchors.py` (jádro, adaptivní okno
±2 až ±6 řádků), `reanchor.py` (`--build`/`--check`/`--apply`), `cite.py` (ověří jednu
citaci, nikdy nezapisuje).

„Soubor existuje, řádek existuje, tvar sedí. To je horší než chyba: tiše ukáže cizí text."
(`README.md:148-153`, `anchors.py:4-11`). Tři verdikty `cite.py` (`:28-33`): `OK` (kotva
sedí), `POSUN/MOVED` (jiný řádek, exit 0, rutina), `ZMIZELA/GONE` (text se změnil, nutné
ověřit člověkem, exit 1, blokuje). Adaptivní okno: základní ±2 řádky, rozšiřuje se, když
kotva nenese aspoň 10 slov nebo se okno opakuje v souboru — „nejtenčí nalezená kotva měla 4
slova, z toho dvě generická" (`anchors.py:29-33`). `reanchor.py --check` hlásí i úplnost
kontroly (G4): kolik citací kotvu nemá vůbec vs. kolik je záměrně vyloučeno — „bez toho je
'nic jsem nenašel' k nerozeznání od 'nic jsem neměřil'" (`README.md:104-105`).

**Přenositelná zásada.** Citace se ověřuje obsahem citovaného místa, ne existencí souboru a
čísla řádku — jinak validace jen potvrzuje formu a tiše propouští ukazatele na cizí text.

**Předvedení.** `python docs/ontology/.ontology-tools/cite.py docs/<soubor>.md:<řádek>` —
verdikt místo ručního čtení 20 řádků; pak posunout odstavec o pár řádků → OK→POSUN; přepsat
text úplně → ZMIZELA.

## 3.4 Guard `session-check.py`

SessionStart hook (matcher `startup|clear`), ~2s, volá `build.py --check` (G1+G5) a
`reanchor.py --check` (G3+G4). Zachycuje zastarání registru mimo review běhy — jinak
dokumentace mimo `/review-spec` obejde smyčku doplňování prvků (`README.md:174-176`).

„VZDY konci exit 0 — nic neblokuje... Tvrde vynuceni delaji tytez nastroje jako brany
review.linters ve /review-spec." (`templates/ontology-tools/session-check.py:5-13`). Try/except
kolem obou volání, aby ani vlastní pád nezablokoval start session (`:37-38,55-56,68-69`).

**Přenositelná zásada.** Kontrola aktuálnosti při startu session má varovat, ne blokovat —
blokující vynucení patří do explicitně vyvolané brány, ne do vstupního bodu, který nesmí
nikdy shodit.

**Předvedení.** Ukázat `SessionStart` konfiguraci v `.claude/settings.json`; spustit ručně,
ukázat exit 0 i s varováním; kontrast proti samostatnému `reanchor.py --check` s nenulovým
exit kódem.

---

# 4. Governance marketplace

## 4.1 `.claude-plugin/marketplace.json`

Manifest se 3 pluginy (`spec-factory`, `knowledge-loop`, `ontology-registry`), každý s
`name`, `source`, `description`, `version` (semver), `category`. Standardní mechanismus
Claude Code pro `/plugin marketplace add <git-url>`.

**Přenositelná zásada.** Verzování a popis pluginu patří do jednoho centrálního, strojově
čitelného manifestu, ne do rozptýlené dokumentace.

**Zajímavý nález.** Verze v `marketplace.json` (`1.0.1`) neodpovídá verzi v
`ontology-registry/plugin.json` (`1.0.2`) — reálný příklad driftu, který jinde v projektu
řeší právě mechaniky jako kotvy/reanchor.

## 4.2 Git hooky — pre-commit / commit-msg

`.githooks/pre-commit` volá `pre-commit.ps1`: kontroluje staged soubory s příponami
`.ps1,.txt,.sql,.cs,.rdlc,.rdl,.rdo,.srd,.srdmi` (`:4`); u `.rdl,.sql,.rdlc,.rdo,.srd,.srdmi`
vynucuje UTF-8 BOM (`:35-42`); u všech vynucuje newline na konci souboru (`:52-59`); u `.sql`
hledá zapomenuté zakomentované direktivy preprocesoru (`--!`, `--#`, `FOREACHATRIBUT(`,
`ENDFOR[`, `:64-79`).

`.githooks/commit-msg` volá `commit-msg.ps1`: vynucuje prefix z `feat, fix, docs, style,
refactor, test, merge, trace` + „: " (regex case-insensitive, `:9-14`), prefix/mezeru
**automaticky doplní/opraví** přepisem souboru zprávy (`:20-37`), vynucuje min. délku 10
znaků (`:47-50`).

**Přenositelná zásada.** Formátová pravidla, která jdou mechanicky ověřit, patří do
commit-time hooku, ne do code review checklistu.

**Předvedení.** `git config core.hooksPath .githooks`; commit bez prefixu → odmítnut; commit
s `Fix: oprava` (špatný case/mezera) → hook potichu opraví na `fix: oprava` a commit projde —
ilustrace rozdílu blokující vs. samoopravné brány.

## 4.3 `.gitlab/CODEOWNERS`

22 řádků (18 neprázdných). Fallback pro celé pluginy, užší pravidla pro `agents/`, `tools/`,
`hooks/`, explicitní vlastnictví manifestů. Vlastníci `@martint @pavelny` všude.

„Boundary-change v jádře pluginu... vyžaduje MR s alespoň jedním schválením vlastníka —
vynucuje GitLab (RULE-GOV-001: 'promuje jen člověk')." (`:3-4`).

**Zajímavý nález.** `ontology-registry` v CODEOWNERS **chybí** — pravidla vlastnictví jsou
napsaná jen pro `spec-factory` a `knowledge-loop`, ačkoli marketplace obsahuje tři pluginy.
Konkrétní živý příklad rozjeté pravdy mezi governance soubory.

**Přenositelná zásada.** Kritické cesty mají mít vlastníka vynuceného platformou
(CODEOWNERS), ne jen zapsaného v dokumentaci.

**Předvedení.** MR měnící `hooks/spec-guard.py` v GitLabu — ukázat zablokovaný merge do
schválení vlastníkem.

## 4.4 `plugins/README.md`

Instalace, adresářová struktura, `$CLAUDE_PLUGIN_ROOT` vs. `$CLAUDE_PROJECT_DIR`,
dvouvrstvý guard, testy. Nemá formální „jak vytvořit plugin", nejbližší je sekce „Správa a
schvalování": „Zásah do hranic systému... = MR + schválení CODEOWNERS (GOV-001: 'agent
navrhuje, povyšuje jen člověk'). Verzování semver + Git tag." (`:98-101`).

Implicitní vzor struktury: `.claude-plugin/plugin.json`, `commands/` (orchestrátor),
`agents/` (namespace `<plugin>:*`), `hooks/` (guard), `tools/` (config seam + testy).
Dvouvrstvý guard obecně: VRSTVA 1 PROTECT (čtou všichni, nemění automaticky nikdo), VRSTVA 2
ALLOW (pracovní složka jen pro jmenované agenty), lidská session píše volně (`:90-96`).

**Přenositelná zásada.** I bez formální šablony funguje README jako implicitní vzor — nová
komponenta má následovat strukturu už zavedených sourozenců, ne si vymýšlet vlastní
konvenci.

**Předvedení.** Postavit vedle sebe strukturu `spec-factory/` a `knowledge-loop/` (oba mají
`agents/`+`hooks/`+`tools/`) proti `ontology-registry/` (jen instalátor, bez `agents/`
a `hooks/`) — diskuse o tom, kdy je odchylka od vzoru oprávněná.

---

# Shrnutí šesti přenositelných zásad napříč vším

1. Citace se ověřují obsahem, ne adresou (číslem řádku) — adresa se posouvá, obsah buď
   platí, nebo signalizuje potřebu ověření.
2. Instalátor smí vypsat, co se má vložit do cizí konfigurace; nikdy to nesmí vložit sám.
3. Kontrola spuštěná automaticky při startu má varovat; kontrola spuštěná explicitně smí
   blokovat.
4. Nekonzistence mezi zdroji je cennější artefakt než přehled shody.
5. Mechanicky ověřitelná pravidla patří do hooku/brány s exit kódem; „agent navrhuje, člověk
   schvaluje" je věrohodné jen s technickou bránou (guard, CODEOWNERS) mimo agenta samotného.
6. Co jde ověřit deterministicky, nikdy nesvěřuj posouzení modelem — a design „raději
   zablokuj než pusť nejistotu" se musí testovat na každou hranu, jinak zůstane jen
   prohlášením v komentáři.

---

# Kandidáti na náměty workshopu

Okruhy: `R` rozšíření (skills/commands/subagenti/hooks) · `M` mechanika kvality (brány,
validátory) · `O` orchestrace (subagenti, paralelizace) · `A` analytické postupy · `U` učení a
znalostní smyčka · `X` antipatterny.

U každého: `[infra]` = musí postavit/spravovat někdo pro celý tým (sdílený repo, CODEOWNERS,
plugin marketplace), jinak zvládne jednotlivec sám ve vlastním projektu.

1. **`M` Brána místo instrukce v promptu** — spec_lint.py (`--intake`, `--dod`, T1 lint) jako
   ukázka, že binární exit kód přežije v procesu déle než odstavec v systémovém promptu.
   Doklad z provozu: eskalace bez pokusu o vyvrácení se nikdy neprovedla, dokud nebyla brána
   (`README.md:88-91`). Jednotlivec si totéž může postavit jako malý validační skript nad
   vlastním dokumentem. **Ne-infra** (skript lze psát sám), ale sdílená verze je `[infra]`.

2. **`O` BLIND recenzent** — spec-critic nesmí vidět verdikty jiných ani metadata původu
   (iterace, autor). Přenositelné i bez pluginu: kdykoli žádáte model o druhý názor na
   vlastní práci, nezmiňujte, že jde o „opravenou verzi" nebo kdo ji psal. **Ne-infra** —
   funguje jako osobní návyk při psaní promptů.

3. **`O` Nález musí mít reprodukci + akci (TEETH)** — spec-redteam odmítá nálezy bez
   konkrétního scénáře a bez navržené akce. Přenositelné do jakéhokoli code/doc review:
   komentář „tohle by mohl být problém" bez příkladu se nepočítá. **Ne-infra.**

4. **`M` Config seam (union + explicitní `_remove`)** — jak bezpečně rozšiřovat sdílenou
   konfiguraci per projekt, aniž by tichý override ztratil bezpečnostní minimum. Přenositelné
   do jakéhokoli sdíleného nastavení týmu (ne jen pluginy). **`[infra]`** — vyžaduje návrh
   schématu a testy, dělá se jednou pro celý tým.

5. **`X` Co se v provozu neosvědčilo a bylo odstraněno** — druhé kolo stejného soudce,
   rubrika v revizním režimu, znalostní smyčka uvnitř spec-factory. Cenná ukázka, že
   design se má měřit a mrtvé mechaniky mazat, ne hromadit „pro jistotu". **Ne-infra** jako
   téma diskuse, `[infra]` jako proces měření v týmu.

6. **`R` Guard = PreToolUse hook nad Write/Edit** — technické vynucení „agent navrhuje, člověk
   schvaluje" přes rozpoznání `agent_type` a dvě zóny (PROTECT/ALLOW). Ukazuje, že zákaz
   zápisu nejde vynutit promptem. **`[infra]`** — hook musí nastavit a udržovat správce
   repozitáře/projektu.

7. **`U` Tři stanice znalostní smyčky (inbox → personal → shared)** — princip odděleného
   tempa zápisu od váhy schválení. Jednotlivec si může postavit „svůj" inbox i bez pluginu
   (poznámkový soubor + `/rule-new`-like příkaz), ale sdílená vrstva `shared/` s CODEOWNERS
   je `[infra]`. Dobrý most mezi „co zvládnu sám" a „co musí zavést tým".

8. **`R` Zrcadlo jako technika izolace přístupu** — gitignored generovaná kopie místo čtení ze
   zdroje, aby cizí (nedozrálá) data fyzicky nebyla v dosahu automatického načítání.
   Přenositelné do jakékoli situace „viditelné pro audit, ale ne závazné pro všechny".
   **`[infra]`** pro implementaci hooku, ale princip je použitelný i v jednodušší podobě
   jednotlivcem.

9. **`M` Kotvy: citace ověřená obsahem, ne řádkem** — ontology-registry `anchors.py`/`cite.py`.
   Přenositelné do každé dokumentace, která cituje `soubor:řádek` a časem se rozjíždí.
   **`[infra]`** pro plný nástroj, ale princip „needituj čísla řádků ručně, ověř obsahem" je
   použitelný i bez nástroje.

10. **`M` SessionStart warn-only vs. explicitní blokující brána** — stejná kontrolní logika
    (`build.py --check`, `reanchor.py --check`) běží jednou neblokující (na startu) a jednou
    blokující (v review). Ukázka, jak rozdělit „upozorni" od „zastav" bez duplikace kódu.
    **`[infra]`** — vyžaduje hook infrastrukturu.

11. **`A` Straw-man dřív než otázky (spec-intake)** — než se ptát na požadavky, napsat vlastní
    hypotetickou odpověď a z jejích slabin odvodit otázky; bezchybná hypotéza je podezřelá.
    Přenositelný analytický postup nezávislý na nástroji. **Ne-infra** — čistě metoda práce
    jednotlivce.

12. **`A` Confidence markers vázané na počet nezávislých zdrojů** — `[C:high]` vyžaduje dva
    různé dokumenty, ne dvě citace téhož. Přenositelné do každého research/groundingového
    kroku. **Ne-infra.**

13. **`O` Triáž nesmí být delegovaná** — v `/review-spec` triáž nálezů dělá orchestrátor, ne
    agent, protože „ze tří nálezů je pravý zhruba jeden". Princip: krok, který filtruje šum
    od signálu, musí zůstat u toho, kdo nese odpovědnost za rozhodnutí. **Ne-infra** jako
    princip, `[infra]` jako součást pluginové pipeline.

14. **`X` Chybějící CODEOWNERS řádek pro ontology-registry** — živý příklad rozjeté pravdy
    mezi governance soubory (marketplace má 3 pluginy, CODEOWNERS pokrývá 2). Dobrý úvodní
    „najděte chybu" cvičení pro workshop. **`[infra]`** — týká se údržby sdíleného repa.

15. **`M` Fail-closed jako testovaný, ne jen deklarovaný princip** — spec_lint.py testy na
    každou hranu (prázdný glob, neparsovatelný manifest, chybějící řádek metriky). Zásada:
    „radši zablokuj" se musí ověřit testem, jinak je to jen komentář. **`[infra]`** pro
    testovací sadu, ale princip platí i pro jednoduchý osobní skript.
