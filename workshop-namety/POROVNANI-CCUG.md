# Porovnání pokrytí: naše materiály vs. Claude Code Ultimate Guide

**Datum:** 2026-09-08
**Porovnávané na naší straně:** `osnova-claude-code.md` (5 úrovní) + `workshop-namety/NAMETY.md` (56 námětů, 11 přednášených dílů)
**Porovnávané na druhé straně:** [claude-code-ultimate-guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide), verze **3.43.0** — čteno přes MCP server `claude-code-guide` a přes raw GitHub

---

## Než začneme — co se vlastně porovnává

Ty dva materiály **nestojí na stejné ose** a to je nejdůležitější zjištění celého porovnání.

| | osa členění | jednotka | adresát |
|---|---|---|---|
| **CCUG** | podle mechanismu (instalace → smyčka → paměť → agenti → skills → hooky → orchestrace) | funkce nástroje | vývojář |
| **naše osnova** | podle zralosti v čase (Den 1–3 → Týden 1–2 → … → Průběžně) | úroveň uživatele | vývojář/pokročilý uživatel |
| **naše série (NAMETY)** | podle **selhání a rozhodnutí** („než pustíš agenta na data", „když to nejde", „proč to, co postavíš, přestaneš používat") | situace, do které se člověk dostane | analytik |

Z toho plyne:

- **Osnova vs. CCUG je srovnání jablek s jablky** — obojí je feature tour, jen jinak nakrájený. Tady dává smysl hledat díry v pokrytí.
- **Série vs. CCUG je srovnání jablek s hruškami** — série záměrně nepokrývá funkce, ale návyky. Tady nemá smysl hledat díry v pokrytí; má smysl ptát se, jestli nějaká **funkce nechybí natolik, že bez ní návyk nedává smysl**.

Zbytek dokumentu drží tohle rozdělení.

---

## Rozsah druhé strany (pro kalibraci)

Měřeno, ne převzato z jejich README:

- `guide/ultimate-guide.md` — **26 662 řádků**, 11 částí, ~120 podkapitol
- `guide/learning-path/` — 7 modulů, 8–11 h, tři tracky (Fundamentals / Skill-focused / **Team Adoption**)
- `guide/workflows/` — **34 souborů** (best-of-n, spec-first, tdd-with-claude, plan-pipeline, code-review, agent-teams, production-reliability, talk-pipeline, …)
- `guide/core/` — 18 souborů · `guide/security/` — 6 · `guide/ops/` — 7 · `guide/ecosystem/` — 14 · `guide/roles/` — 4
- `examples/` — **84 šablon**: 10 agentů, 11 hooků, 52 skillů, 10 skriptů
- `quiz/questions/` — banka otázek se schématem (`category`, `category_id`, `source_file`, `questions[]`)
- `machine-readable/reference.yaml` — 3 980 řádků, mj. **onboarding matrix** se šesti cíli: `get_started`, `optimize`, `build_agents`, `learn_security`, `fix_problem`, `learn_everything` — každý ve variantách 5/15/30/60 min s adaptivními triggery
- MCP server hlásí **1 809 indexovaných záznamů ve 29 kategoriích**

Licence: CC BY-SA 4.0 na průvodce, CC0 na šablony. Přebírání textu tedy vyžaduje uvedení autora a stejnou licenci; **šablony (CC0) se přebírat dají volně**.

---

# ČÁST A — Osnova (5 úrovní) vs. CCUG

## A1. Co máme a oni taky (pokryto oboustranně)

Bez komentáře, jen pro úplnost: instalace, první session, oprávnění a jejich režimy, slash příkazy, CLAUDE.md a hierarchie paměti, Plan Mode, rewind/checkpointy, správa kontextu a `/clear`, výběr modelu a `/cost`, skills, subagenti, hooky, MCP, pluginy, headless, CI/CD, sandboxing, Agent SDK, enterprise provideři, OTel monitoring, server-managed settings.

To je **jádro a je pokryté**. Níže jsou jen rozdíly.

## A2. Co máme navíc než oni (naše převaha — nepřebírat, chránit)

| Téma | U nás | U nich |
|---|---|---|
| **VS Code rozšíření** | kap. 1.7 a 3.8 — panel, @-zmínky, diff, multi-tab, `@browser`, `/worktree`, `@terminal:name` | jen 9.4 „IDE Integration", zlomek rozsahu |
| **Dvě cesty na start (GUI vs. CLI)** | explicitní volba v úvodu osnovy | nemá; CCUG je čistě CLI-first |
| **„Kdy Claude Code NEPOUŽÍVAT"** | soustředěná sekce s pěti kritérii | rozptýleno (1.7 Trust Calibration, 9.11 Pitfalls) |
| **Čeština** | celý materiál + `F-02` tokenizace CS | nemá vůbec (EN/FR) |
| **Role analytika** | celá série NAMETY | nemá — CCUG je od začátku do konce dev-centric |
| **Milníkové checklisty po úrovni** | 5× checklist | má `/self-assessment`, ale bez pevných milníků |
| **Odkaz na oficiální školení Anthropic (Skilljar)** | ano | nenašel jsem |

**Závěr A2:** VS Code linka a čeština jsou dvě věci, které z jejich materiálu nedoplníme, protože tam nejsou. To je současně důvod, proč naše materiály nejde nahradit odkazem na cizí repozitář.

## A3. Co jim chybí u nás — díry v osnově

Seřazeno podle toho, jak moc to vadí. `[!]` = doporučuji doplnit, `[?]` = zvážit, `[–]` = zaznamenat a nechat být.

### `[!]` Data flow & privacy je u nás pozdě

CCUG to má jako **2.12** — tedy v Core Concepts, hned po kontextu, ještě před CLAUDE.md. My to máme roztroušené: zmínka v „Kdy NEPOUŽÍVAT" (kam data putují) a Bedrock/Vertex/Foundry až v **Úrovni 5**.

Pro firemní publikum je to obrácené pořadí. Člověk, který zítra pustí agenta na interní repozitář, potřebuje vědět, kam jdou data, **v den 1**, ne v měsíci třetím. Série to řeší lépe (Díl 2 je hned druhý), ale osnova ne.

→ **Návrh:** přesunout do Úrovně 1 jako novou kapitolu 1.8 „Kam tvoje data tečou", odkázat na [Data Usage](https://code.claude.com/docs/en/data-usage) a firemní politiku KVADOS.

### `[!]` Strukturované promptování a schéma výstupu chybí úplně

CCUG 2.8–2.11: XML tagy, sémantické kotvy, prompt engineering patterns, **structured outputs & schema design**. U nás je prompt engineering jedna kapitola (2.5) o specifičnosti a kontextu.

Pro analytika, který chce z modelu dostat **tabulku, picklist nebo JSON, se kterým dál pracuje**, je schéma výstupu klíčové. Máme `A-02` (číslovaný picklist a odpověď čísly) v sérii, což je speciální případ téže věci, ale obecné pravidlo v osnově není.

→ **Návrh:** rozšířit 2.5 nebo přidat 2.5b „Když potřebuješ výstup, se kterým se dá dál pracovat". CCUG má i `--json-schema` (my to máme až v 4.1 headless, kde to analytik nenajde).

### `[!]` Rozlišení skill / subagent / MCP / hook jako rozhodnutí

CCUG má na to samostatnou epizodu (`docs/distribution/quick-win-video-series.md`, Episode 2) s explicitním kritériem:

> skill = opakovaně použitelné instrukce a lokální assety · subagent = izolovaný kontext nebo paralelní analýza mění výsledek · MCP = Claude musí volat trvalou externí schopnost

a přidává: *„uveď oprávnění, hranici dat a failure mode ještě před instalací."* Plus `guide/ecosystem/mcp-vs-cli.md` k otázce „MCP server, nebo prostě CLI?".

U nás jsou tyto čtyři mechanismy ve čtyřech oddělených kapitolách (3.4, 3.5, 3.3, 3.6) a **nikde není věta, podle které si člověk vybere**. To je přesně ta chyba, po které lidé staví MCP server na něco, co měl být třířádkový skill.

→ **Návrh:** doplnit do Úrovně 3 krátkou rozhodovací kapitolu před 3.3. V sérii to částečně nese `R-02`/`R-03`/`O-01`, ale rozhodovací kritérium tam taky není explicitní (viz B3).

### `[?]` Vlastní slash příkazy jako samostatné téma

CCUG má na příkazy celou část 6 (slash commands, vytváření vlastních, šablona, příklady) oddělenou od skillů (část 5). My máme skills (3.4) a slash příkazy jen jako **spotřebu vestavěných** (1.5). Vlastní příkaz se v osnově nevytváří nikde.

Rozdíl skill vs. příkaz je pro tvorbu vlastní výbavy podstatný a v sérii ho neseme (`R-02` „metodika bez spouštěče je jen text"). V osnově chybí.

### `[?]` Konfigurace pro tým — chybí mezistupeň

Máme `.claude/settings.json` (3.2) a pak skok rovnou na **server-managed settings + MDM/Group Policy/Ansible** (5.4). CCUG má mezi tím **3.5 „Team Configuration at Scale"** a `examples/scripts/sync-claude-config.sh`.

Většina týmů v KVADOS bude přesně v tom mezistupni: sdílený `.mcp.json` a `.claude/` v repu, ne MDM. Tenhle stupeň v osnově není.

### `[?]` Migrace z jiných AI nástrojů

CCUG 1.6. Pokud část publika přichází z Copilotu nebo z webového ChatGPT, je to užitečná vstupní kapitola („co z vašich návyků platí a co ne"). U nás máme jen srovnání v 1.1 na úrovni „čím se to liší", ne „co si přenést".

### `[?]` Trust calibration

CCUG 1.7 — *kdy a kolik* ověřovat, ne jen „vždy ověřuj". Naše osnova říká „vždy zkontrolujte diff" (2.10), což je správně, ale v praxi neudržitelné a lidé to po týdnu vzdají. Série to řeší dobře (`M-03`, `M-05`), osnova ne.

### `[?]` Slovníček pojmů

CCUG má `guide/core/glossary.md`. Pro školení analytiků, kde půjde o tokeny, kontextové okno, kompaktaci, agenta, subagenta, harness, hook, MCP — slovníček na jedné stránce ušetří opakované vysvětlování. My ho nemáme.

### `[–]` Zaznamenat, nedoplňovat

Tyhle věci CCUG má a my ne, ale pro naše publikum a náš záběr je nechávám stranou — jsou buď příliš dev-specifické, příliš čerstvé, nebo příliš okrajové:

- **Output styles** (9.7)
- **Session teleportation** (9.16), **cross-session messaging** (9.27), **remote control / mobil** (9.22)
- **Codebase design for agent productivity** (9.18) — jak upravit repozitář, aby v něm agent fungoval
- **Harness engineering** (9.25), **loop-graph-engineering**, **permutation frameworks** (9.19)
- **Legacy codebase modernization** (9.21)
- **Computer Use** (`guide/core/computer-use.md`)
- **Claude Cowork pro nevývojáře** (11, `guide/cowork.md`) — *tohle jediné bych sledoval*; pokud se ukáže jako použitelné pro analytiky bez terminálu, mění to vstupní bránu celého školení
- **Ekonomika na úrovni týmu** — `ops/ai-unit-economics.md`, `ops/subscription-strategy.md`, `ops/team-metrics.md`; relevantní pro toho, kdo školení schvaluje, ne pro účastníka
- **Agent evaluation** (`roles/agent-evaluation.md`) — jak měřit, že agent funguje

---

# ČÁST B — Série (11 dílů) vs. CCUG

## B1. Kde má CCUG hotový materiál k tématu, které přednášíme

Tohle **není** seznam mezer. Je to seznam míst, kde si můžeme ověřit tvrzení druhým zdrojem nebo si půjčit hotové cvičení. U každého uvádím, co konkrétně tam je.

| Náš námět | Co k tomu má CCUG | K čemu to použít |
|---|---|---|
| `F-01` bezstavovost · `F-05` kontextové okno | 2.2 Context Management, 2.13 Under the Hood, `core/context-engineering.md` | druhý zdroj k mechanice; naše čísla z DOKLADŮ zůstávají naše |
| `F-03` kompaktace s instrukcí | 2.2 | ověření, že `/compact <instrukce>` je dokumentovaná praxe, ne náš trik |
| `N-01`–`N-03` zákazy, rewind, plan mode | 1.4, 2.4, 2.3 | — |
| `K-01` dokument nese kontext | 3.1, `core/context-engineering.md` | — |
| `K-03` co NEčíst | 9.26 Review-Driven Context Optimization | jejich formulace téhož; stojí za přečtení před finalizací karty |
| `R-01` zadání do souboru | `workflows/spec-first.md`, `workflows/plan-driven.md` | hotová cvičení |
| `R-02`/`R-03` metodika se spouštěčem | část 5 Skills, část 6 Commands, `core/skill-design-patterns.md` | — |
| `M-01` brána, kterou nikdo nespouští | `examples/hooks/bash/verification-gate.sh`, `security-gate.sh`, 7.4 | **hotový hook k demu** |
| `M-03` triáž falešných nálezů | `workflows/code-review.md`, `workflows/multi-provider-code-review.md` | — |
| `M-04` slepý recenzent | `workflows/best-of-n.md`, `workflows/dual-instance-planning.md` | — |
| `M-06` deterministická vs. sémantická | Episode 3 video briefu: tři fixtures (pass/fail/malformed) | **hotová struktura cvičení** |
| `O-01` kam jde hluk | část 4 Agents, `workflows/agent-teams.md` | — |
| `O-03` předání práce sobě zítra | `examples/skills/handoff-create|resume|update/` | **tři hotové skilly** |
| `A-04` straw-man | 2.10 Prompt Engineering Patterns, 9.15 Named Prompting Patterns | — |
| `U-01` debuguj prompt, ne výstup | 9.24 Instinct-Based Continuous Learning | — |
| `U-02` záchyt bez povyšovací brány | `examples/hooks/bash/learning-capture.sh` | **hotový hook**; přesně náš problém |
| `X-02` pipeline, kterou jsem nespustil | 9.23 Configuration Lifecycle & The Update Loop | jediné místo, kde se blíží našemu nosnému tématu |

**Dvacet jedna z 56 námětů** (17 řádků tabulky) má u nich zpracovaný protějšek. To je dost na to, aby stálo za to je před finalizací karet projít — a málo na to, aby to sérii ohrozilo.

## B2. Co nemají a my ano — nosná témata série

Tohle jsou věci, které v jejich 26 tisících řádcích **nejsou**, a jsou to shodou okolností nejsilnější karty:

1. **„Postaveno vs. používáno"** jako centrální teze s doklady (12 karet označených ⚑). Nejblíž je 9.23 Configuration Lifecycle, ale je to procedurální kapitola, ne teze podložená vlastními daty.
2. **Tokenizace češtiny** (`F-02`). Nikde. CCUG má FR překlad, ale otázku ceny neanglického textu neřeší.
3. **Vlastní měření** — 51:1, 97 % zahozeno kompaktací, 22 vygenerovaných a smazaných souborů, „čtvrtina CLAUDE.md, kterou nikdo nespustil". CCUG má u tvrzení `Research support` s poctivě uvedenou hranicí platnosti, ale **žádná vlastní čísla**.
4. **Antipattern jako odvrácená strana pozitivního námětu** — náš red-team sloučil 9 z 12 antipatternů do příslušných karet. CCUG má „8 Beginner Mistakes" jako oddělený seznam. Náš postup je metodicky lepší a nemá tam obdobu.
5. **Analytik jako role.** `guide/roles/ai-roles.md` má role, ale všechny vývojářské.

## B3. Skutečné mezery v sérii

Prošel jsem CCUG proti našim 11 dílům a hledal jsem jen to, **bez čeho některý náš návyk nedává smysl**. Našel jsem tři.

### `[!]` Díl 2 se jmenuje „Než pustíš agenta na svá data", ale o datech není

Díl 2 (51 min) obsahuje: tři zákazy, tři úrovně zpět, plan mode, „nic neměň", prompt je zápis. To je **bezpečnost změn** — jak nerozbít repozitář. Není tam nic o tom, **kam data odcházejí**, co je a není v pořádku poslat, co dělá sandbox a co ne, ani prompt injection.

CCUG má na to šest souborů (`guide/security/`: data-privacy, enterprise-governance, production-safety, sandbox-isolation, sandbox-native, security-hardening) plus `examples/commands/resources/threat-db.yaml`. Onboarding matrix má od verze 3.43.0 samostatný cíl `learn_security` a v `beginner_5min` řadí **sandbox před příkazy** s poznámkou „SECURITY FIRST".

Pro publikum, které bude pouštět agenta na interní data KVADOS, je to nejvážnější nález celého porovnání. Buď díl přejmenovat („Než něco rozbiješ"), nebo doplnit 2–3 náměty o datové hranici. Díl 2 je s 51 minutami druhý nejkratší, prostor tam je.

### `[?]` Rozhodovací kritérium mechanismu chybí i v sérii

Totéž jako A3 výše. `R-02`, `R-03`, `R-05`, `O-01` popisují jednotlivé mechanismy, ale žádná karta neříká **podle čeho si vybrat**. Díl 9 („Vlastní výbava a jak ji předat dál") je na to přirozené místo — chybí tam úvodní karta typu „Skill, subagent, nebo MCP?".

### `[–]` Měření přínosu je jen kvalitativní

`U-07` („co po sedmi měsících doopravdy žije") je nejlepší závěr, jaký série může mít, ale je to introspekce. CCUG má `ops/team-metrics.md` a `roles/agent-evaluation.md`. Pro sérii to nechávám stranou — kvantifikace přínosu AI v týmu je vlastní téma a do 90minutového dílu se nevejde. **Zaznamenat pro případ, že se na to management zeptá.**

---

# ČÁST C — Co si vzít z jejich formátu (a co ne)

Tady je hodnota největší, protože formát se přebírá bez licenčního problému.

## C1. Vzít: „Observable check" do každé karty

Jejich `docs/distribution/quick-win-video-series.md` má u každé epizody rubriku:

```
Outcome          — jeden konkrétní výsledek
Target length    — 3–7 minut
Sequence         — 5 kroků
Observable check — pozorovatelné kritérium, že to člověk umí
Guide route      — kam číst dál
Research support — s explicitní hranicí platnosti citovaného zdroje
```

Příklad jejich observable check (Epizoda 1): *„proof record uvádí přesný příkaz a jeho výsledek. Zelený příkaz bez uvedení prostředí a hranice pokrytí je neúplný."* Epizoda 3 (hook): tři fixtures — pass, fail, malformed — a nepokryté runtime chování se zapisuje jako `UNKNOWN`.

To je **naše `[K OVĚŘENÍ]` disciplína, jen aplikovaná na výstup účastníka místo na naše tvrzení.** Naše karty mají `Role`, `Min`, `Prio`, `dep` a per-díl „Co si z toho odnesou" — což je bohatší na plánování, ale chudší na ověření. Účastník po dílu neví, podle čeho pozná, že to umí.

→ **Návrh:** doplnit do každé karty dvě pole: `Ověřitelný výstup` (co má účastník na konci ukázat) a `Kam dál` (odkaz do osnovy nebo do dokumentace). U 56 karet je to práce na jeden večer a je to jediná změna formátu, kterou bych z CCUG přebíral bez váhání.

## C2. Vzít: druhá osa členění pro firemní nasazení

CCUG má vedle sedmi modulů ještě **tracky** (Fundamentals / Skill-focused / Team Adoption) a **onboarding matrix** — šest cílů (`get_started`, `optimize`, `build_agents`, `learn_security`, `fix_problem`, `learn_everything`) × čtyři časové rozpočty (5/15/30/60 min), s `topics_max` a adaptivními triggery podle toho, na co se člověk ptá.

Naše série má tři střihy (3 díly / 5 dílů / celá série) — což je totéž, ale jen na jedné ose (délka). Chybí osa **cíle**: někdo přijde s „chci to jen bezpečně vyzkoušet", někdo s „chci si postavit vlastní výbavu".

→ **Návrh:** k existující tabulce tří střihů přidat druhou tabulku „podle cíle", třeba: *bezpečně vyzkoušet* → díly 1, 2 · *psát lepší zadání* → 3, 4, 5 · *stavět a předávat* → 6, 9 · *revidovat cizí práci* → 7. Přeskupení stávajících dílů, žádný nový obsah.

## C3. Zvážit: sledování postupu s doložením

`examples/skills/learning-path/scripts/progress.py` — nabízí jen moduly se splněnými prerekvizitami, **vyžaduje neprázdný evidence note** a zapisuje stav do `.claude/learning/*.json`. Review schedule 1/3/7/14/30/60/90 dní.

My máme v tabulce sloupec `dep`, tedy graf závislostí už existuje — chybí jen běhová část. Pro firemní školení by to znamenalo doložitelný postup účastníka místo prezenčky.

→ Ale pozor: přesně tohle je `X-02` („postavil jsem pipeline a nikdy ji nespustil"). Stavět to má smysl jen tehdy, když někdo ty evidence notes bude číst. Jinak to bude naše vlastní ilustrace vlastního antipatternu.

## C4. Nevzít

- **Obsah kapitol** — EN/FR, dev-centric, licence CC BY-SA vyžaduje uvedení a stejnou licenci. Náš text je jinak zacílený.
- **Sedmimodulové členění** — je to feature tour. Naše členění podle selhání je pro analytiky lepší a je to náš rozdíl.
- **`.pptx` slidy** (`docs/distribution/claude-code-learning-path-slides.pptx`) — jen jako referenční členění, ne k převzetí.
- **Nárok „use as PRIMARY source before web search"** z instrukcí jejich MCP serveru. Je to komunitní materiál, ne oficiální dokumentace. Na tvrzení o chování Claude Code používat `search_official_docs()` (ten samý server nabízí lokální snapshot oficiálních docs) nebo přímo code.claude.com.

---

# Shrnutí — co s tím

**Osnova** (`osnova-claude-code.md`) — tři doplnění, která bych udělal:

1. Data flow & privacy přesunout do Úrovně 1 *(dnes je fakticky až v Ú5)*
2. Doplnit strukturovaný výstup / schéma do Úrovně 2 *(dnes chybí úplně)*
3. Doplnit rozhodovací kapitolu „skill vs. subagent vs. MCP vs. hook" do Úrovně 3 *(dnes jsou to čtyři oddělené kapitoly bez kritéria volby)*

Volitelně: mezistupeň týmové konfigurace (Ú3), slovníček pojmů, trust calibration.

**Série** (`NAMETY.md`) — dvě věci:

1. Díl 2 buď přejmenovat, nebo doplnit datovou hranici *(dnes název slibuje data, obsah řeší změny)*
2. Do dílu 9 přidat úvodní kartu s rozhodovacím kritériem mechanismu

**Formát** — jedna změna, největší poměr přínos/práce:

3. Doplnit do každé z 56 karet pole `Ověřitelný výstup` a `Kam dál`

**Nepřebírat:** obsah, členění, ani jejich nárok na to být primárním zdrojem. Naše převaha — čeština a její tokenizace, VS Code linka, role analytika, vlastní měřená data a teze „postaveno vs. používáno" — v jejich materiálu není a nedá se odtud doplnit.

---

## Poznámka k platnosti

Porovnáváno proti CCUG **3.43.0** (stav k 2026-09-08). Repozitář se mění týdně (mají RSS a changelog). Čísla rozsahu jsem měřil, ne převzal z jejich README — jejich README uvádí u `ultimate-guide.md` „25K lines", naměřeno 26 662. Struktura `guide/` a `examples/` je čtená z GitHub API, ne z jejich indexu.

Co jsem **neověřoval:** kvalitu jednotlivých kapitol CCUG. Porovnání je na úrovni pokrytí témat a formátu, ne obsahové správnosti. U kapitol, které bychom chtěli použít jako druhý zdroj (viz B1), je potřeba přečíst je celé — jejich vlastní `Research support` sekce jsou v tomhle ohledu poctivé (uvádějí hranice platnosti citovaných studií), což je dobrá známka, ale není to důkaz.
