# Osnova: Jak se naučit Claude Code od nuly k expertovi

> **Formát:** Krátké kapitoly (5–15 minut studia). Každá úroveň staví na předchozí.
> **Primární zdroj:** Oficiální dokumentace na [code.claude.com/docs](https://code.claude.com/docs/en/)
> **Datum vytvoření:** Únor 2026. Claude Code se vyvíjí velmi rychle — před studiem konkrétní kapitoly ověřte aktuálnost odkazovaného zdroje.

---

## Jak s touto osnovou pracovat

- **Tempo:** Studujte 1–3 kapitoly denně. Nepospíchejte. Lepší je jednu techniku zvládnout pořádně než přelétnout pět.
- **Praxe nad teorií:** Každá kapitola obsahuje praktické cvičení (**Vyzkoušejte**). Udělejte ho. Samotné čtení dokumentace nestačí.
- **Vlastní projekt:** Ideálně si zvolte jeden svůj reálný projekt, na kterém budete všechno zkoušet. Tím vzniknou přirozené kontexty.
- **Poznámky:** Po každé kapitole si zapište 1–2 věty o tom, co jste se naučili a co vás překvapilo.
- **Milníky:** Na konci každé úrovně je checklist. Pokud ho splníte, jste připraveni na další úroveň.
- **Dvě cesty na start:** Pokud preferujete grafické rozhraní, začněte kapitolou 1.7 (VS Code) a CLI se doučte později. Pokud jste zvyklí na terminál, sledujte osnovu lineárně.
- **Úroveň 5 je volitelná** — je pro vývojáře platforem a enterprise správce. Pokud vytváříte vlastní produkty s AI nebo spravujete Claude Code pro tým, pokračujte. Jinak ji přeskočte.

---

## Úroveň 1: Začátečník — Základy (Den 1–3)

### 1.1 Co je Claude Code a proč ho používat
- Rozdíl oproti ChatGPT, GitHub Copilot a dalším nástrojům
- Klíčový koncept: agentní přístup — Claude čte soubory, spouští příkazy, provádí změny autonomně
- Není to "chytřejší autocomplete", je to "junior kolega s přístupem k vašemu terminálu"
- **Zdroj:** [Overview](https://code.claude.com/docs/en/overview)
- **Vyzkoušejte:** Přečtěte si Overview a zapište si tři věci, na které chcete Claude Code použít ve svém projektu.

### 1.2 Instalace a první spuštění
- Instalace CLI (Windows: PowerShell/CMD, macOS/Linux: curl)
- Instalace VS Code rozšíření z Marketplace
- Přihlášení (Anthropic účet nebo API klíč)
- **Zdroje:** [Setup](https://code.claude.com/docs/en/setup), [VS Code](https://code.claude.com/docs/en/vs-code)
- **Vyzkoušejte:** Nainstalujte CLI i VS Code rozšíření. Spusťte `claude --version` v terminálu a ověřte, že funguje.

### 1.3 První interaktivní sezení
- Spuštění `claude` v terminálu (nebo otevření panelu ve VS Code)
- Základní konverzace: zeptejte se na kód, nechte si vysvětlit funkci
- Pochopení cyklu: prompt → Claude čte/přemýšlí/jedná → výsledek
- **Zdroj:** [Quickstart](https://code.claude.com/docs/en/quickstart)
- **Vyzkoušejte:** Otevřete svůj projekt a zeptejte se Claude: "Vysvětli mi strukturu tohoto projektu a jaké technologie používá." Sledujte, jaké soubory Claude čte.

### 1.4 Systém oprávnění — co Claude smí a nesmí
- Porozumění dialogům Allow/Deny — proč se objevují
- Proč Claude žádá o povolení před úpravami (bezpečnostní model)
- Základní režimy: Normal (ptá se), Plan (jen čte)
- **Zdroj:** [Permissions](https://code.claude.com/docs/en/permissions)
- **Vyzkoušejte:** Požádejte Claude o jednoduchou změnu (přejmenování proměnné). Sledujte, na co se vás ptá a co dělá po schválení.

### 1.5 Základní slash příkazy
- `/help` — nápověda, `/clear` — nová konverzace, `/compact` — komprese kontextu
- `/model` — přepínání modelů, `/cost` — kolik jste utratili, `/quit` — konec
- Jak přepínat modely (Opus = nejchytřejší/nejdražší, Sonnet = rovnováha, Haiku = nejrychlejší/nejlevnější)
- **Zdroj:** [Interactive Mode](https://code.claude.com/docs/en/interactive-mode)
- **Vyzkoušejte:** Spusťte sezení, použijte `/model` pro přepnutí na Haiku, položte otázku, pak přepněte na Sonnet a porovnejte odpovědi.

### 1.6 První úprava kódu a Git commit
- Požádejte Claude o konkrétní změnu v kódu
- Kontrola diffu před přijetím (ve VS Code: vizuální side-by-side diff)
- Vytvoření commitu přes Claude — řekněte "Commitni tyto změny"
- **Zdroj:** [Quickstart](https://code.claude.com/docs/en/quickstart)
- **Vyzkoušejte:** Požádejte Claude o přidání komentáře ke složité funkci ve vašem projektu. Zkontrolujte diff a přijměte. Pak řekněte "Vytvoř commit."

### 1.7 VS Code rozšíření — základní orientace
- Kde najít panel Claude Code (ikona Spark v panelu editoru, Command Palette: "Claude Code")
- Jak poslat prompt, vidět diff, přijmout/odmítnout změny
- @-zmínky: napište `@nazev-souboru` pro odkázání na konkrétní soubor
- Výběr kódu v editoru → Claude ho automaticky vidí
- **Zdroj:** [VS Code](https://code.claude.com/docs/en/vs-code)
- **Vyzkoušejte:** Označte blok kódu ve VS Code, otevřete Claude panel a zeptejte se "Co dělá tento kód a jak by se dal zlepšit?"

### Milník Úrovně 1
- [ ] Umím spustit Claude Code (CLI nebo VS Code)
- [ ] Umím se zeptat na kód a dostat vysvětlení
- [ ] Umím požádat o úpravu kódu a zkontrolovat diff
- [ ] Rozumím, proč Claude žádá o oprávnění
- [ ] Znám základní slash příkazy (/help, /clear, /model, /cost)
- [ ] Vytvořil jsem alespoň jeden commit přes Claude

---

## Úroveň 2: Produktivní uživatel (Týden 1–2)

### 2.1 Mentální model: Jak přemýšlet o spolupráci s AI agentem
- Claude Code není vyhledávač ani textový editor — je to agent s vlastní iniciativou
- Klíčové principy: buďte konkrétní, poskytněte kontext, vždy ověřujte výstup
- Anti-pattern: "oprav to" bez kontextu vs. "V souboru auth.ts na řádku 42 funkce validateToken neošetřuje expiraci tokenu. Přidej kontrolu."
- Princip verifikace: vždy řekněte, JAK má Claude ověřit svou práci (testy, lint, build)
- **Zdroj:** [Best Practices](https://code.claude.com/docs/en/best-practices)
- **Vyzkoušejte:** Zvolte bug ve svém projektu. Formulujte prompt dvěma způsoby: vágně a konkrétně. Porovnejte výsledky.

### 2.2 Jak Claude Code funguje pod kapotou
- Agentní smyčka: model přemýšlí → zvolí nástroj → spustí ho → přečte výsledek → opakuje
- Context window: omezený prostor (~200k tokenů), plní se historií konverzace
- Auto-kompakce: Claude automaticky komprimuje starší kontext
- `/compact` pro manuální kompresi s instrukcemi
- **Zdroj:** [How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works)
- **Vyzkoušejte:** Spusťte delší sezení (10+ promptů). Pak použijte `/cost` a sledujte, kolik kontextu se spotřebovalo. Zkuste `/compact`.

### 2.3 Paměť: CLAUDE.md a auto-memory
- CLAUDE.md = instrukce pro Claude v kořeni projektu (jako README, ale pro AI)
- Spuštění `/init` vytvoří základní CLAUDE.md z vašeho projektu
- Hierarchie paměti: projekt root → podadresáře → uživatel (`~/.claude/CLAUDE.md`) → `.claude/rules/`
- Auto-memory: Claude si sám ukládá naučené vzory do `~/.claude/projects/`
- **Zdroj:** [Memory](https://code.claude.com/docs/en/memory)
- **Vyzkoušejte:** Spusťte `/init` ve svém projektu. Otevřete vygenerovaný CLAUDE.md, přidejte 2–3 pravidla specifická pro váš projekt (např. "Vždy používej TypeScript strict mode" nebo "Testy piš s pytest").

### 2.4 Plan Mode — prozkoumej, pak jednej
- Aktivace: Shift+Tab nebo výběr režimu ve VS Code
- Claude v Plan Mode jen čte a analyzuje — neprovádí změny
- Čtyřfázový workflow: Explore (Plan Mode) → Plan → Implement (Normal Mode) → Commit
- Kdy Plan Mode použít: nové features, neznámý kód, složité refactoring
- Kdy přeskočit: jednořádkové opravy, jednoduché úkoly
- **Zdroj:** [Common Workflows](https://code.claude.com/docs/en/common-workflows)
- **Vyzkoušejte:** Přepněte do Plan Mode a řekněte: "Jak bys přidal [feature] do tohoto projektu? Analyzuj kód a navrhni postup." Sledujte, jak Claude prozkoumává kód, aniž by cokoliv měnil.

### 2.5 Efektivní prompt engineering pro Claude Code
- Buďte konkrétní: uveďte soubory, řádky, symptomy, očekávané chování
- Poskytněte kontext: @-zmínky souborů, vložení obrázků, URL, piping dat
- Odkazujte na existující vzory: "Implementuj to stejným způsobem jako v souboru X"
- Dejte Claude kritéria úspěchu: "Testy musí projít", "Build nesmí selhat"
- **Zdroj:** [Best Practices](https://code.claude.com/docs/en/best-practices)
- **Vyzkoušejte:** Požádejte Claude o novou funkci. V promptu uveďte: konkrétní soubor, vzor z existujícího kódu, a verifikační příkaz. Porovnejte s výsledkem, kdy tyto informace neuvedete.

### 2.6 Práce s testy
- "Napiš testy pro funkci X" — Claude analyzuje kód a vytvoří testy
- "Spusť testy a oprav, co selhává" — smyčka test-fix-test
- Verifikace jako klíčový princip: vždy řekněte Claude, ať po změně spustí testy
- **Zdroj:** [Common Workflows](https://code.claude.com/docs/en/common-workflows)
- **Vyzkoušejte:** Vyberte funkci bez testů. Řekněte Claude: "Napiš unit testy pro [funkce] a spusť je. Pokud nějaký selže, oprav ho."

### 2.7 Checkpointy a /rewind
- Claude automaticky sleduje stav kódu i konverzace
- `/rewind` vrátí kód, konverzaci, nebo obojí na předchozí bod
- Ve VS Code: vizuální checkpoint UI s možností forku konverzace
- **Zdroj:** [Checkpointing](https://code.claude.com/docs/en/checkpointing)
- **Vyzkoušejte:** Nechte Claude provést nějakou změnu. Pak zkuste `/rewind` a vraťte se zpět. Ověřte, že soubory se skutečně vrátily.

### 2.8 Správa kontextu a sezení
- `/clear` mezi úkoly — nejdůležitější návyk pro produktivitu
- Resuming: `claude -c` (pokračuj poslední), `claude -r` (vyber sezení)
- `/compact <instrukce>` pro inteligentní kompresi (např. `/compact Zapamatuj si jen architekturu, zahoď detaily`)
- Pravidlo: nový úkol = nové sezení. Nepřeplňujte kontext nesouvisejícími tématy.
- **Zdroj:** [How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works)
- **Vyzkoušejte:** Udělejte dva nesouvisející úkoly v jednom sezení. Pak totéž ve dvou oddělených sezeních (s `/clear`). Porovnejte kvalitu výstupů.

### 2.9 Výběr modelu a řízení nákladů
- **Opus:** Nejchytřejší, nejdražší. Pro architektonické rozhodnutí, složitý debugging, rozsáhlý refactoring.
- **Sonnet:** Dobrý poměr cena/výkon. Pro většinu každodenní práce.
- **Haiku:** Nejrychlejší, nejlevnější. Pro jednoduché dotazy, vysvětlení, generování dokumentace.
- Fast Mode (`/fast`): stejný model, rychlejší výstup
- Effort levels: řídí hloubku přemýšlení
- `/cost` pro sledování nákladů v sezení
- **Zdroje:** [Model Config](https://code.claude.com/docs/en/model-config), [Costs](https://code.claude.com/docs/en/costs)
- **Vyzkoušejte:** Dejte stejný úkol Haiku i Sonnet. Porovnejte rychlost, kvalitu a cenu (použijte `/cost`).

### 2.10 Časté chyby začátečníků (anti-patterns)
- **"Kitchen sink" sezení:** Příliš mnoho nesouvisejících úkolů v jednom sezení → kontext se zaplní → kvalita klesá. **Řešení:** `/clear` mezi úkoly.
- **Opakované opravování dokola:** Claude dělá chybu, řeknete "ne, takhle ne", Claude zkouší znovu... **Řešení:** `/clear` a formulujte prompt lépe od začátku.
- **Přehnaně dlouhý CLAUDE.md:** Stovky řádků instrukcí → plýtvání kontextem. **Řešení:** Max ~500 řádků (dle doporučení Anthropic), referenční materiál přesuňte do skills.
- **Slepá důvěra:** Přijímání změn bez kontroly diffu. **Řešení:** Vždy zkontrolujte diff a nechte spustit testy.
- **Žádná verifikace:** Neřeknete Claude, jak ověřit výsledek. **Řešení:** Přidejte "Spusť testy/build/lint po změně."
- **Zdroj:** [Best Practices — Avoid Common Failure Patterns](https://code.claude.com/docs/en/best-practices)

### 2.11 Základní troubleshooting
- Claude neodpovídá → restartujte sezení, zkontrolujte připojení
- Příkaz `claude` nenalezen → ověřte PATH (`Setup` doc)
- Opakované žádosti o oprávnění → nastavte allowlist (`/permissions`)
- VS Code rozšíření nefunguje → přeinstalujte, zkontrolujte verzi VS Code (min. 1.98.0)
- `/doctor` — diagnostika instalace a konfigurace
- **Zdroj:** [Troubleshooting](https://code.claude.com/docs/en/troubleshooting)
- **Vyzkoušejte:** Spusťte `/doctor` a projděte si výstup. Opravte případné problémy.

### Milník Úrovně 2
- [ ] Mám CLAUDE.md ve svém projektu s pravidly specifickými pro mě/tým
- [ ] Umím používat Plan Mode pro průzkum kódu
- [ ] Umím formulovat konkrétní, kontextově bohaté prompty
- [ ] Nechal jsem Claude napsat a spustit testy
- [ ] Zvládám `/clear`, `/compact`, `/rewind` a vím, kdy co použít
- [ ] Umím zvolit správný model pro daný úkol
- [ ] Znám hlavní anti-patterns a vyvaruji se jich

---

## Úroveň 3: Středně pokročilý (Týden 2–4)

### 3.1 Oprávnění do hloubky
- Čtyři režimy: Normal (ptá se), Plan (jen čte), Accept-Edits (auto-přijímá editace), Bypass (vše povoleno)
- Pravidla oprávnění: syntaxe `Tool(specifier)` s glob vzory
- `/permissions` pro správu allowlistů — klíč k plynulé práci
- Příklad: `allow: ["Edit(src/**/*.ts)", "Bash(npm test)"]`
- **Zdroj:** [Permissions](https://code.claude.com/docs/en/permissions)
- **Vyzkoušejte:** Otevřete `/permissions` a přidejte 2–3 pravidla pro příkazy, které často schvalujete.

### 3.2 Nastavení a konfigurace
- Scopy (od nejvyšší priority): Managed → CLI args → Local → Project → User
- Klíčové soubory: `~/.claude/settings.json` (uživatel), `.claude/settings.json` (projekt), `.claude/settings.local.json` (lokální)
- Důležité proměnné prostředí: `ANTHROPIC_MODEL`, `CLAUDE_CODE_EFFORT_LEVEL`
- **Zdroj:** [Settings](https://code.claude.com/docs/en/settings)
- **Vyzkoušejte:** Vytvořte `.claude/settings.json` ve svém projektu s vlastními pravidly oprávnění.

### 3.3 MCP servery — připojení externích nástrojů
- MCP (Model Context Protocol) = standardní protokol pro připojení externích nástrojů k Claude
- Instalace: `claude mcp add nazev-serveru --transport http URL` nebo stdio
- Populární servery: GitHub, Brave Search, PostgreSQL, Sentry, Figma
- Tři scopy: local (jen pro vás), project (.mcp.json, sdíleno s týmem), user (všechny projekty)
- **Zdroj:** [MCP](https://code.claude.com/docs/en/mcp)
- **Vyzkoušejte:** Nainstalujte si jeden MCP server relevantní pro váš workflow (např. GitHub, pokud používáte GitHub).

### 3.4 Vlastní skills (SKILL.md)
- Skills = opakovaně použitelné instrukce v `.claude/skills/`
- YAML frontmatter pro metadata a auto-discovery
- Vyvolání přes `/nazev-skillu` v konverzaci
- Příklad: skill pro code review, deploy, migrace DB
- **Zdroj:** [Skills](https://code.claude.com/docs/en/skills)
- **Vyzkoušejte:** Vytvořte jednoduchý skill pro svůj nejčastější workflow (např. "vytvoř PR s popisem").

### 3.5 Subagenti — delegování práce
- Vestavění subagenti: Explore (rychlé hledání), Plan (architektura), general-purpose (složité úkoly)
- Vlastní subagenti: markdown soubory v `.claude/agents/` s YAML frontmatter
- Foreground (čekáte na výsledek) vs. background (paralelní práce)
- **Zdroj:** [Subagents](https://code.claude.com/docs/en/sub-agents)
- **Vyzkoušejte:** Požádejte Claude o složitější úkol a sledujte, zda sám spustí subagenta. Pak zkuste vytvořit vlastního agenta v `.claude/agents/`.

### 3.6 Hooks — automatizace reakcí na události
- Hooks = skripty, které se spouští při určitých událostech Claude Code
- Klíčové události: PreToolUse (před akcí), PostToolUse (po akci), Stop (Claude skončil), SessionStart
- Příklady: auto-formátování kódu po editaci, blokování úprav chráněných souborů, notifikace
- Konfigurace v settings.json pod klíčem `hooks`
- **Zdroj:** [Hooks Guide](https://code.claude.com/docs/en/hooks-guide)
- **Vyzkoušejte:** Nastavte hook, který automaticky spustí váš formátovač (prettier, black, gofmt) po každé editaci.

### 3.7 Plugins — rozšíření ekosystému
- Instalace a správa pluginů přes `/plugins` (ve VS Code graficky)
- Plugin marketplace a komunitní pluginy
- Pluginy mohou přidávat skills, hooks, MCP servery a subagenty najednou
- **Zdroje:** [Plugins](https://code.claude.com/docs/en/plugins), [Discover Plugins](https://code.claude.com/docs/en/discover-plugins)
- **Vyzkoušejte:** Otevřete `/plugins`, projděte marketplace a nainstalujte plugin, který vás zaujme.

### 3.8 VS Code rozšíření — pokročilé funkce
- Více konverzací v tabulkách/oknech (Open in New Tab/Window)
- Chrome integrace: `@browser` pro automatizaci testování webapps
- Git worktrees: `/worktree` pro paralelní práci na více věcech najednou
- Resuming vzdálených sezení spuštěných na Claude.ai
- `@terminal:name` pro zahrnutí výstupu terminálu do promptu
- **Zdroj:** [VS Code](https://code.claude.com/docs/en/vs-code)
- **Vyzkoušejte:** Otevřete dvě konverzace najednou — jednu pro implementaci, druhou pro review.

### 3.9 Piping a CLI jako unix nástroj
- `cat soubor | claude -p "vysvětli tento kód"` — zpracování dat přes pipe
- `git diff | claude -p "napiš commit message"` — řetězení s Git
- `claude -p "..." | jq '.result'` — strukturovaný výstup
- **Zdroj:** [Common Workflows](https://code.claude.com/docs/en/common-workflows)
- **Vyzkoušejte:** Zkuste `git log --oneline -20 | claude -p "Shrň, na čem se v projektu pracovalo"`.

### 3.10 Začlenění Claude Code do každodenního workflow
- **Ráno:** `claude -c` pro pokračování včerejšího úkolu nebo nové sezení pro dnešní práci
- **Během práce:** Plan Mode pro analýzu, Normal pro implementaci, `/clear` mezi úkoly
- **Code review:** "Zkontroluj tento PR/diff" nebo použití jako CI reviewer
- **Dokumentace:** "Zdokumentuj tuto funkci/modul/API"
- **Debugging:** Vložte chybovou hlášku a řekněte "Najdi příčinu a oprav"
- **Vyzkoušejte:** Po dobu jednoho pracovního dne se u každého úkolu zastavte a zvažte: "Byl by na toto Claude Code rychlejší než já?" Zkoušejte.

### Milník Úrovně 3
- [ ] Mám nastavená permission rules pro plynulou práci
- [ ] Používám alespoň jeden MCP server
- [ ] Vytvořil jsem vlastní skill nebo subagenta
- [ ] Mám nastavený alespoň jeden hook
- [ ] Zvládám VS Code multi-tab konverzace
- [ ] Claude Code je běžnou součástí mého pracovního dne

---

## Úroveň 4: Pokročilý (Měsíc 1–2)

### 4.1 Headless mode — skriptování a automatizace
- `claude -p "instrukce"` — neinteraktivní režim pro skripty
- Strukturovaný JSON výstup: `--output-format stream-json`
- `--json-schema` pro validovaný výstup odpovídající schématu
- Integrace do build skriptů, nočních jobů, automatizace
- **Zdroj:** [Headless](https://code.claude.com/docs/en/headless)
- **Vyzkoušejte:** Napište bash skript, který vezme soubor a přes `claude -p` vygeneruje jeho dokumentaci.

### 4.2 CI/CD integrace
- GitHub Actions: `claude-code-action` — Claude jako CI reviewer
- GitLab CI/CD integrace
- Bezpečnost v CI: `--allowedTools` pro omezení dostupných nástrojů, `--max-turns` pro limit kroků
- **Zdroje:** [GitHub Actions](https://code.claude.com/docs/en/github-actions), [GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd)
- **Vyzkoušejte:** Přidejte `claude-code-action` do GitHub Actions workflow vašeho projektu pro automatické code review.

### 4.3 Hooks do hloubky
- Všechny lifecycle events (16+ typů): SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PermissionRequest, Stop, SubagentStart/Stop, ConfigChange...
- Prompt-based hooks: LLM vyhodnotí podmínku a rozhodne
- Agent-based hooks: subagent s nástroji (Read, Grep, Glob) pro ověření
- Async hooks: neblokující, běží na pozadí
- Hook input/output schémata: exit kódy, JSON výstup, decision control
- **Zdroj:** [Hooks Reference](https://code.claude.com/docs/en/hooks)
- **Vyzkoušejte:** Vytvořte prompt-based hook, který kontroluje, zda Claude nemodifikuje soubory v adresáři `/config/`.

### 4.4 MCP pokročilé techniky
- Claude Code jako MCP server: `claude mcp serve` — integrujte ho do jiných nástrojů
- MCP Tool Search: automatická správa velkých sad nástrojů (10+ nástrojů)
- OAuth autentizace vzdálených MCP serverů
- MCP Resources: `@server:protocol://resource/path`
- MCP Prompts jako slash příkazy: `/mcp__server__prompt`
- **Zdroj:** [MCP](https://code.claude.com/docs/en/mcp)
- **Vyzkoušejte:** Nastavte dva MCP servery a zkuste úkol, který je kombinuje (např. GitHub + databáze).

### 4.5 Agent Teams — multi-agentní orchestrace
- Experimentální funkce: "team lead" koordinuje "teammates"
- Tmux-based paralelní provádění úkolů
- Každý agent pracuje ve vlastním kontextu a worktree
- **Zdroj:** [Agent Teams](https://code.claude.com/docs/en/agent-teams)
- **Vyzkoušejte:** Aktivujte experimentální funkci a zkuste rozdělit úkol mezi agenty (pokud je dostupná ve vaší verzi).

### 4.6 Sandboxing a bezpečnost
- Filesystem izolace: omezení přístupu na pracovní adresář
- Network izolace: kontrola síťových požadavků
- Ochrana proti prompt injection: jak Claude detekuje a brání se
- Bezpečné zacházení s nedůvěryhodným kódem
- **Zdroje:** [Sandboxing](https://code.claude.com/docs/en/sandboxing), [Security](https://code.claude.com/docs/en/security)
- **Vyzkoušejte:** Nakonfigurujte sandbox pro projekt s citlivými daty (`/sandbox`).

### 4.7 Vlastní pluginy a marketplace
- Manifest schéma (plugin.json) a adresářová struktura
- Plugin může obsahovat: skills, hooks, MCP servery, subagenty
- Distribuce: npm, GitHub, Git, URL
- Vytvoření vlastního marketplace pro tým
- **Zdroj:** [Plugins Reference](https://code.claude.com/docs/en/plugins-reference)
- **Vyzkoušejte:** Vytvořte minimální plugin, který zabalí váš nejpoužívanější skill a hook.

### Milník Úrovně 4
- [ ] Umím použít headless mode ve skriptu
- [ ] Claude Code je integrovaný do mého CI/CD pipeline
- [ ] Mám pokročilé hooks (prompt-based nebo agent-based)
- [ ] Ovládám MCP na pokročilé úrovni
- [ ] Rozumím bezpečnostnímu modelu a umím nastavit sandbox

---

## Úroveň 5: Expert / Platform Engineer (Průběžně, volitelná)

> Tato úroveň je pro vývojáře, kteří budují produkty s AI agenty nebo spravují Claude Code pro celý tým/organizaci. Pokud to není váš případ, klidně ji přeskočte.

### 5.1 Agent SDK — programatické agenty
- Python a TypeScript SDK pro vytváření vlastních AI agentů
- Vestavěné nástroje, permissions, hooks v kódu
- Produkční nasazení a hosting
- **Zdroje:** [Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview), [Python](https://platform.claude.com/docs/en/agent-sdk/python), [TypeScript](https://platform.claude.com/docs/en/agent-sdk/typescript)

### 5.2 Enterprise nasazení
- Provideři: Amazon Bedrock, Google Vertex AI, Microsoft Foundry
- LLM Gateway (LiteLLM) pro routing a caching
- Network a proxy konfigurace (custom CA certs, mTLS)
- Dev containers pro izolované vývojové prostředí
- **Zdroje:** [Bedrock](https://code.claude.com/docs/en/amazon-bedrock), [Vertex AI](https://code.claude.com/docs/en/google-vertex-ai), [Foundry](https://code.claude.com/docs/en/microsoft-foundry)

### 5.3 Monitoring, analytics a řízení nákladů
- OpenTelemetry metriky a eventy
- PR attribution a adoption metrics
- Řízení rate limits a nákladových stropů pro týmy
- **Zdroje:** [Monitoring](https://code.claude.com/docs/en/monitoring-usage), [Analytics](https://code.claude.com/docs/en/analytics)

### 5.4 Server-managed settings a organizační politiky
- Centrální konfigurace pro celou organizaci
- Managed hooks, MCP servery, permissions — řízeno z jednoho místa
- Distribuce přes MDM (macOS), Group Policy (Windows), Ansible (Linux)
- **Zdroj:** [Server-Managed Settings](https://code.claude.com/docs/en/server-managed-settings)

---

## Kdy Claude Code NEPOUŽÍVAT

Naučit se, kdy nástroj NEPOUŽÍVAT, je stejně důležité jako naučit se ho používat:

- **Ultra-citlivý kód (kryptografie, bezpečnostní jádro):** Claude může zavést subtilní chyby, které jsou těžké k odhalení. Vždy mějte lidský review.
- **Kód, který nesmíte sdílet:** Data jdou na servery Anthropic (pokud nepoužíváte Bedrock/Vertex/Foundry). Ověřte firemní politiku. Viz [Data Usage](https://code.claude.com/docs/en/data-usage).
- **Projekt bez verzovacího systému:** Claude provádí reálné změny v souborech. Bez Gitu nemáte záchrannou síť.
- **Když nerozumíte výstupu:** Pokud nemůžete posoudit, zda je vygenerovaný kód správný, nepřijímejte ho slepě.
- **Extrémně velké monorepo bez konfigurace:** Claude bude pomalý a nepřesný. Nejdřív nastavte CLAUDE.md, `.gitignore` a permission rules.

---

## Doporučení — co dalšího zvážit

### Akční kroky
1. **Nastavte si rozpočet.** Opus stojí ~$15/milion vstupních tokenů. Pro začátek používejte Sonnet a Opus šetřete na složité problémy. Sledujte `/cost`.
2. **Přečtěte si Security a Data Usage.** Pochopte, kam data putují, zejména pokud pracujete s firemním kódem: [Security](https://code.claude.com/docs/en/security), [Data Usage](https://code.claude.com/docs/en/data-usage).
3. **CLAUDE.md commitujte do repozitáře.** Celý tým bude mít konzistentní instrukce.
4. **Sledujte Changelog.** Nové funkce přibývají téměř týdně: [Changelog](https://code.claude.com/docs/en/changelog).
5. **Git je váš záchranný pás.** Před experimentováním vždy commitněte aktuální stav. Claude provádí reálné změny.
6. **Naučte se prompt engineering specifický pro Claude Code.** Je jiný než obecný. Klíčové: specifičnost, kontext, verifikace, vzory z existujícího kódu.
7. **Poznejte limitace.** Context window ~200k tokenů, občasné halucinace, pomalejší u velkých projektů. Přečtěte si [Best Practices — Avoid Common Failure Patterns](https://code.claude.com/docs/en/best-practices).

### Průběžné vzdělávání
8. **Blog Anthropic:** [anthropic.com/news](https://www.anthropic.com/news) — novinky a strategie.
9. **Jak týmy Anthropic používají Claude Code:** [claude.com/blog/how-anthropic-teams-use-claude-code](https://claude.com/blog/how-anthropic-teams-use-claude-code) — reálné use cases.
10. **Komunita:** [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code) — kurátorský seznam nástrojů, pluginů a skills.

---

## Doplňkové zdroje

### Oficiální
| Zdroj | URL |
|-------|-----|
| Dokumentace (hlavní) | [code.claude.com/docs](https://code.claude.com/docs/en/) |
| Best Practices (článek) | [anthropic.com/engineering/claude-code-best-practices](https://www.anthropic.com/engineering/claude-code-best-practices) |
| Jak týmy Anthropic používají CC | [claude.com/blog/how-anthropic-teams-use-claude-code](https://claude.com/blog/how-anthropic-teams-use-claude-code) |
| Oficiální školení | [anthropic.skilljar.com/claude-code-in-action](https://anthropic.skilljar.com/claude-code-in-action) |
| Agent SDK | [platform.claude.com/docs/en/agent-sdk](https://platform.claude.com/docs/en/agent-sdk/overview) |
| Changelog | [code.claude.com/docs/en/changelog](https://code.claude.com/docs/en/changelog) |
| Blog Anthropic | [anthropic.com/news](https://www.anthropic.com/news) |

### Komunita
| Zdroj | URL |
|-------|-----|
| Awesome Claude Code | [github.com/hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) |
| SFEIR Institute (kurz) | [institute.sfeir.com/en/claude-code](https://institute.sfeir.com/en/claude-code/) |
| Complete Tutorial (Sid Bharath) | [siddharthbharath.com/claude-code-the-complete-guide](https://www.siddharthbharath.com/claude-code-the-complete-guide/) |
| Cheatsheet (Shipyard) | [shipyard.build/blog/claude-code-cheat-sheet](https://shipyard.build/blog/claude-code-cheat-sheet/) |
| Claude Code Guide (auto-updated) | [github.com/Cranot/claude-code-guide](https://github.com/Cranot/claude-code-guide) |
| Video tutoriály Anthropic | [support.claude.com/en/collections/10548294](https://support.claude.com/en/collections/10548294-video-tutorials) |
