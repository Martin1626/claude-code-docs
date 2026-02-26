# Úroveň 3: Středně pokročilý — Přizpůsobení a rozšíření

> **Časová náročnost:** 10 kapitol, každá 10–15 minut. Celkem cca 2–3 hodiny rozložené do 2–4 týdnů.
> **Předpoklady:** Zvládnutá Úroveň 2 (milník splněn). Máte CLAUDE.md, umíte Plan Mode, správu kontextu, testy, znáte anti-patterns.
> **Cíl úrovně:** Přizpůsobit si Claude Code na míru: oprávnění bez přerušování, externí nástroje přes MCP, vlastní skills a subagenti, automatizace přes hooks, a začlenění do každodenního workflow.

---

## 3.1 Oprávnění do hloubky

**Doba studia:** 15 minut

### Pět režimů oprávnění

V Úrovni 1 jste poznali Default a Plan. Nyní kompletní přehled:

| Režim | Klíč v settings | Claude smí bez ptaní | Typické použití |
|-------|----------------|---------------------|-----------------|
| **Default** | `default` | Čtení souborů, hledání | Běžná práce s plnou kontrolou |
| **Accept Edits** | `acceptEdits` | Čtení + editace souborů | Důvěřujete editacím, schvalujete jen Bash |
| **Plan** | `plan` | Jen čtení | Průzkum, plánování, žádné změny |
| **Don't Ask** | `dontAsk` | Jen předschválené (allowlist) | Automatizace s minimem interakcí |
| **Bypass** | `bypassPermissions` | Vše | Jen v kontejneru/VM, nebezpečné |

Přepínání: **Shift+Tab** (cyklicky), nebo nastavení výchozího:
```json
// .claude/settings.json
{ "permissions": { "defaultMode": "acceptEdits" } }
```

### Pravidla oprávnění — syntaxe

Formát: `Tool` nebo `Tool(specifier)`. Tři seznamy: `allow`, `ask`, `deny`. Vyhodnocení: **deny → ask → allow** (první shoda vyhrává, deny má vždy přednost).

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(npx tsc --noEmit)",
      "Edit(/src/**/*.ts)",
      "Read"
    ],
    "deny": [
      "Bash(git push *)",
      "Bash(rm *)",
      "Edit(.env)"
    ]
  }
}
```

### Specifikátory pro jednotlivé nástroje

**Bash** — wildcard `*` s word boundary (mezera + `*`):

| Pravidlo | Povolí | Nepovolí |
|----------|--------|----------|
| `Bash(npm run *)` | `npm run build`, `npm run test` | `npm install` |
| `Bash(git *)` | `git status`, `git log` | `gitk` |
| `Bash(* --version)` | `node --version`, `python --version` | `node index.js` |

> **Bezpečnost:** Claude Code rozumí shell operátorům — `Bash(safe-cmd *)` nepovolí `safe-cmd && dangerous-cmd`.

**Read/Edit** — gitignore-style vzory:

| Vzor | Význam |
|------|--------|
| `Edit(/src/**/*.ts)` | Všechny .ts soubory v src/ (relativně k root projektu) |
| `Read(*.env)` | Soubory .env v aktuálním adresáři |
| `Edit(//Users/alice/secrets/**)` | Absolutní cesta |
| `Read(~/Documents/*.pdf)` | Relativně k home adresáři |

`*` = soubory v jednom adresáři, `**` = rekurzivně.

**MCP nástroje:** `mcp__server` (celý server), `mcp__server__tool` (konkrétní nástroj).

**Subagenti:** `Task(Explore)`, `Task(my-custom-agent)`.

### /permissions — interaktivní správa

Napište `/permissions` pro grafické rozhraní, kde vidíte aktuální pravidla a můžete přidávat nová. Často schvalované akce přidejte zde — ušetříte si desítky kliknutí denně.

> **Zdroj:** [Permissions](https://code.claude.com/docs/en/permissions)

### Vyzkoušejte

1. Otevřete `/permissions` a projděte aktuální allowlist
2. Přidejte pravidla pro příkazy, které nejčastěji schvalujete (testy, lint, typecheck)
3. Přidejte deny pravidlo pro `Bash(rm -rf *)` a `Edit(.env)`
4. Vytvořte `.claude/settings.json` s permission rules a commitněte ho — tým je sdílí
5. Zkuste přepnout na Accept Edits (Shift+Tab) a sledujte, jak se změní workflow

### Shrnutí
- **5 režimů**: Default, Accept Edits, Plan, Don't Ask, Bypass
- Pravidla: `Tool(specifier)` s glob/wildcard, vyhodnocení deny → ask → allow
- `/permissions` pro interaktivní správu, `.claude/settings.json` pro sdílení s týmem
- Deny vždy přebije allow — bezpečnostní síť

---

## 3.2 Nastavení a konfigurace

**Doba studia:** 10 minut

### Scopy nastavení (od nejvyšší priority)

| # | Scope | Umístění | Pro koho |
|---|-------|----------|----------|
| 1 | **Managed** | Systémové cesty (MDM, Group Policy) | Celá organizace |
| 2 | **CLI args** | `claude --model opus` | Aktuální sezení |
| 3 | **Local** | `.claude/settings.local.json` | Vy, tento projekt |
| 4 | **Project** | `.claude/settings.json` | Tým (commituje se) |
| 5 | **User** | `~/.claude/settings.json` | Vy, všechny projekty |

Vyšší scope přebíjí nižší. Managed nastavení nelze přepsat.

### Klíčové soubory

```
~/.claude/
├── settings.json     # Uživatelská nastavení (všechny projekty)
├── CLAUDE.md         # Osobní instrukce
└── rules/            # Osobní pravidla

<projekt>/
├── .claude/
│   ├── settings.json       # Projektová nastavení (sdílená)
│   ├── settings.local.json # Lokální nastavení (gitignored)
│   ├── CLAUDE.md           # Projektové instrukce
│   ├── rules/              # Modulární pravidla
│   ├── skills/             # Skills
│   └── agents/             # Subagenti
├── .mcp.json               # MCP servery (sdílené)
└── CLAUDE.md               # Alternativní umístění
```

### Nejdůležitější nastavení

```json
// .claude/settings.json — příklad pro tým
{
  "permissions": {
    "allow": ["Bash(npm test)", "Bash(npm run lint)"],
    "deny": ["Bash(rm -rf *)", "Edit(.env)"],
    "defaultMode": "default"
  },
  "model": "sonnet",
  "hooks": { ... }
}
```

### Důležité proměnné prostředí

| Proměnná | Popis |
|----------|-------|
| `ANTHROPIC_MODEL` | Výchozí model |
| `ANTHROPIC_API_KEY` | API klíč |
| `CLAUDE_CODE_EFFORT_LEVEL` | Effort level (low/medium/high) |
| `MAX_THINKING_TOKENS` | Limit thinking tokenů |
| `BASH_DEFAULT_TIMEOUT_MS` | Timeout Bash příkazů (ms) |

> **Zdroj:** [Settings](https://code.claude.com/docs/en/settings)

### Vyzkoušejte

1. Vytvořte `.claude/settings.json` ve svém projektu s permission rules
2. Vytvořte `~/.claude/settings.json` s osobními preferencemi (model, permissions)
3. Spusťte Claude a ověřte, že nastavení funguje: zkuste příkaz z allowlistu (neměl by se ptát)
4. Commitněte `.claude/settings.json` do Gitu

### Shrnutí
- 5 scopů od Managed (nejvyšší) po User (nejnižší)
- `.claude/settings.json` = sdílená týmová konfigurace, commituje se
- `.claude/settings.local.json` = vaše lokální přepisy, gitignored
- Proměnné prostředí pro model, API klíč, effort level

---

## 3.3 MCP servery — připojení externích nástrojů

**Doba studia:** 15 minut

### Co je MCP

**Model Context Protocol** je standardní protokol, kterým Claude Code komunikuje s externími službami. MCP server = adaptér mezi Claude a konkrétní službou (GitHub, databáze, Sentry, Figma...).

Bez MCP Claude neumí přistoupit k vašemu Jiře, databázi nebo Slacku. S MCP může.

### Instalace MCP serveru

**Vzdálený HTTP server** (pokud server poskytuje URL):
```bash
claude mcp add my-remote-server --transport http https://example.com/mcp
```

**Lokální stdio server** (spouští se lokálně — nejčastější):
```bash
claude mcp add postgres -- npx -y @modelcontextprotocol/server-postgres \
  postgresql://localhost:5432/mydb

claude mcp add github -- npx -y @modelcontextprotocol/server-github
```

> **Tip:** Pokud již používáte MCP servery v Claude Desktop, importujte je: `claude mcp add-from-claude-desktop`.

> **Důležité:** Všechny přepínače (--transport, --scope) musí být **před** názvem serveru. `--` odděluje parametry Claude od parametrů serveru.

### Správa MCP serverů

```bash
claude mcp list           # Seznam nainstalovaných
claude mcp get nazev      # Detail konkrétního
claude mcp remove nazev   # Odinstalovat
```

V sezení: `/mcp` zobrazí stav serverů a spotřebu kontextu.

### Tři scopy

| Scope | Úložiště | Sdílení | Kdy použít |
|-------|----------|---------|------------|
| **Local** (výchozí) | `~/.claude.json` | Jen vy, tento projekt | Osobní nástroje pro jeden projekt |
| **Project** | `.mcp.json` v root projektu | Tým (committuje se) | Sdílené nástroje celého týmu |
| **User** | `~/.claude.json` | Jen vy, všechny projekty | Nástroje, které chcete všude |

**Priorita scopů:** local > project > user (lokální přebíjí projektové a uživatelské).

Nastavení scopu:
```bash
claude mcp add --scope project github-server -- ...
claude mcp add --scope user my-tool -- ...
```

### .mcp.json pro sdílení s týmem

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

Proměnné prostředí se expandují: `${VAR}` a `${VAR:-default}`.

> **Důležité:** Proměnné jako `${GITHUB_TOKEN}` musíte mít nastavené ve svém systémovém prostředí. Claude Code je expanduje při startu MCP serveru — pokud proměnná neexistuje, server se nepřipojí.

### Populární MCP servery

| Server | K čemu | Příklad |
|--------|--------|---------|
| **GitHub** | Issues, PR, code search | "Podívej se na issue #42 a navrhni opravu" |
| **PostgreSQL** | Databázové dotazy | "Kolik uživatelů se registrovalo tento měsíc?" |
| **Sentry** | Monitoring chyb | "Jaké jsou top 5 chyb v produkci?" |
| **Brave Search** | Webové vyhledávání | "Najdi dokumentaci k této knihovně" |
| **Figma** | Designové soubory | "Implementuj UI podle tohoto Figma návrhu" |

### MCP a kontext

Každý MCP server přidává definice nástrojů do kontextu **při každém requestu**, i když ho nepoužíváte. Zkontrolujte spotřebu: `/mcp`. Odpojte nepoužívané servery.

**Tool Search** (automaticky zapnuto): Když MCP nástroje přesáhnou 10 % kontextu, Claude Code je odkládá a načítá on-demand. Konfigurace: `ENABLE_TOOL_SEARCH=auto:5` (5 % threshold).

> **Zdroj:** [MCP](https://code.claude.com/docs/en/mcp)

### Vyzkoušejte

1. Nainstalujte MCP server relevantní pro váš workflow:
   - GitHub: `claude mcp add github -- npx -y @modelcontextprotocol/server-github`
   - Nebo jiný z [MCP registru](https://github.com/modelcontextprotocol/servers)
2. Spusťte `/mcp` — vidíte server a jeho spotřebu kontextu?
3. Zkuste úkol, který server využívá (např. "Podívej se na otevřené issues")
4. Pro sdílení: vytvořte `.mcp.json` a commitněte

### Shrnutí
- MCP = protokol pro připojení externích služeb (GitHub, DB, Sentry, ...)
- `claude mcp add` pro instalaci, `/mcp` pro stav a spotřebu
- Tři scopy: local, project (.mcp.json), user
- Každý server zabírá kontext — odpojte nepoužívané

---

## 3.4 Vlastní skills (SKILL.md)

**Doba studia:** 15 minut

### Co jsou skills

Skills jsou **opakovaně použitelné instrukce** v markdown souborech. Claude je načítá on-demand a vy je vyvoláváte přes `/nazev`. Dva typy:

- **Referenční** — znalosti, které Claude použije, když jsou relevantní (API konvence, style guide)
- **Akční** — workflow, které spustíte příkazem (`/deploy`, `/review`, `/fix-issue`)

### Kde skills žijí

| Umístění | Cesta | Platí pro |
|----------|-------|-----------|
| Osobní | `~/.claude/skills/<nazev>/SKILL.md` | Všechny vaše projekty |
| Projektové | `.claude/skills/<nazev>/SKILL.md` | Tento projekt (sdílí tým) |
| Plugin | `<plugin>/skills/<nazev>/SKILL.md` | Kde je plugin zapnutý |

### Vytvoření skillu

```bash
mkdir -p .claude/skills/fix-issue
```

Soubor `.claude/skills/fix-issue/SKILL.md`:
```markdown
---
name: fix-issue
description: Analyzuje a opraví GitHub issue
disable-model-invocation: true
allowed-tools: Bash(gh *)
---

Analyzuj a oprav GitHub issue: $ARGUMENTS

1. Použij `gh issue view $0` pro detaily issue
2. Pochop problém popsaný v issue
3. Najdi relevantní soubory v kódu
4. Implementuj opravu
5. Napiš a spusť testy
6. Ověř, že prochází lint a typecheck
7. Commitni s popisnou zprávou
8. Pushni a vytvoř PR: `gh pr create`
```

Vyvolání: `/fix-issue 1234`

### Klíčové frontmatter pole

| Pole | Popis |
|------|-------|
| `name` | Identifikátor (malá písmena, pomlčky, max 64 znaků) |
| `description` | Kdy skill použít — Claude rozhoduje na základě popisu |
| `argument-hint` | Nápověda při autocomplete, např. `[issue-number]` |
| `disable-model-invocation` | `true` = Claude ho nenačte automaticky, jen přes `/nazev` |
| `user-invocable` | `false` = nezobrazí se v `/` menu (interní skill) |
| `allowed-tools` | Nástroje povolené bez ptaní při aktivaci skillu |
| `context` | `fork` = běží v izolovaném kontextu (subagent) |
| `agent` | Který subagent použít, když `context: fork` |
| `model` | Specifický model pro tento skill |

### Proměnné v skills

| Proměnná | Popis |
|----------|-------|
| `$ARGUMENTS` | Vše za `/nazev` (celý řetězec) |
| `$ARGUMENTS[0]`, `$ARGUMENTS[1]` | Jednotlivé argumenty (plný tvar, 0-indexed) |
| `$0`, `$1`, `$2` | Zkratka pro `$ARGUMENTS[N]` |
| `` !`command` `` | Výstup shell příkazu (dynamický kontext) |

Příklad dynamického kontextu:
```markdown
---
name: pr-summary
description: Shrne aktuální PR
context: fork
---
## Kontext PR
- Diff: !`gh pr diff`
- Komentáře: !`gh pr view --comments`

Shrň tento pull request...
```

### Referenční skill — příklad

```markdown
---
name: api-conventions
description: REST API konvence pro naše služby
---
# API Conventions
- URL cesty: kebab-case
- JSON properties: camelCase
- Seznam endpointy: vždy s paginací
- Verze v URL: /v1/, /v2/
```

Claude tento skill načte automaticky, když pracuje na API kódu.

> **Tip:** Použijte `disable-model-invocation: true` pro skills s vedlejšími efekty (deploy, push). Tím zajistíte, že je spustíte jen vy, ne Claude automaticky.

> **Zdroj:** [Skills](https://code.claude.com/docs/en/skills)

### Vyzkoušejte

1. Vytvořte jednoduchý skill (např. `/review` pro code review checklist)
2. Vytvořte akční skill s `$ARGUMENTS` (např. `/explain $0` pro vysvětlení souboru)
3. Vyzkoušejte `disable-model-invocation: true` — skill je neviditelný pro Claude, dokud nenapíšete `/nazev`
4. Commitněte `.claude/skills/` — tým sdílí skills

### Shrnutí
- Skills = opakovaně použitelné instrukce v `.claude/skills/<nazev>/SKILL.md`
- Vyvolání: `/nazev [argumenty]`
- `disable-model-invocation: true` pro skills se side effects
- `$ARGUMENTS` / `$0` / `$1` pro parametrizaci, `` !`cmd` `` pro dynamický kontext

---

## 3.5 Subagenti — delegování práce

**Doba studia:** 15 minut

### Co jsou subagenti

Subagent = samostatná instance Claude s **vlastním kontextovým oknem**. Výhody:
- **Izolace kontextu** — verbose výstupy nezaplní váš hlavní kontext
- **Specializace** — vlastní instrukce, omezené nástroje, jiný model
- **Paralelizace** — background subagenti pracují souběžně

### Vestavění subagenti

| Agent | Model | Nástroje | Kdy ho Claude použije |
|-------|-------|---------|----------------------|
| **Explore** | Haiku | Read-only (Glob, Grep, Read) | Rychlé hledání souborů a kódu |
| **Plan** | Zdědí | Read-only | V Plan Mode pro průzkum |
| **General-purpose** | Zdědí | Všechny | Složité úkoly vyžadující změny |

Claude sám deleguje na subagenty, nebo je požádejte explicitně:
```
Use a subagent to investigate how our auth system handles token refresh.
```

### Vytvoření vlastního subagenta

Soubor `.claude/agents/security-reviewer.md`:
```markdown
---
name: security-reviewer
description: Kontroluje kód z hlediska bezpečnostních zranitelností. Použij proaktivně po změnách kódu.
tools: Read, Grep, Glob, Bash
model: sonnet
---

Jsi senior security engineer. Při review kódu hledej:
- Injection zranitelnosti (SQL, XSS, command injection)
- Chyby v autentizaci a autorizaci
- Secrets nebo credentials v kódu
- Nezabezpečené zacházení s daty

Uveď konkrétní řádky a navrhni opravy.
```

Použití: "Use the security-reviewer to check the auth module" nebo Claude ho může použít automaticky (díky popisu "Použij proaktivně po změnách kódu").

### Klíčové frontmatter pole

| Pole | Popis |
|------|-------|
| `name` | Identifikátor |
| `description` | **Kdy** má Claude tohoto agenta použít |
| `tools` | Povolené nástroje (omezení = bezpečnost) |
| `disallowedTools` | Nástroje k odepření (přebije `tools`) |
| `model` | `haiku`, `sonnet`, `opus` nebo `inherit` (výchozí) |
| `permissionMode` | Režim oprávnění pro subagenta (default, acceptEdits, ...) |
| `skills` | Skills, které se předčtou do kontextu |
| `mcpServers` | MCP servery dostupné subagentovi |
| `isolation` | `worktree` = pracuje v izolované kopii repozitáře |
| `background` | `true` = vždy běží na pozadí |
| `maxTurns` | Limit kroků (ochrana před nekonečnou smyčkou) |

### Foreground vs. background

| Typ | Chování | Kdy |
|-----|---------|-----|
| **Foreground** | Blokuje hlavní konverzaci, čekáte na výsledek | Potřebujete výsledek hned |
| **Background** | Běží paralelně, vy pokračujete v práci | Nezávislý úkol, výsledek není urgentní |

**Ctrl+B** přesune běžící foreground úkol na pozadí.

Background subagenti: oprávnění se schvalují předem. Pokud potřebují oprávnění, které nemají, akci přeskočí a pokračují.

### Praktický vzor: Writer + Reviewer

```
Session 1: Implementuj rate limiter pro naše API endpointy.
Session 2 (subagent): Zkontroluj implementaci rate limiteru —
hledej race conditions, edge cases, konzistenci s existujícím middleware.
```

> **Zdroj:** [Subagents](https://code.claude.com/docs/en/sub-agents)

### Vyzkoušejte

1. Požádejte Claude o složitější úkol a sledujte, zda sám spustí subagenta (např. "Investigate how routing works in this project")
2. Vytvořte vlastní subagent v `.claude/agents/` (např. code-reviewer)
3. Explicitně požádejte: "Use the code-reviewer to check my recent changes"
4. Zkuste Ctrl+B pro přesunutí běžícího úkolu na pozadí

### Shrnutí
- Subagent = izolovaný Claude s vlastním kontextem, nástroji a instrukcemi
- Vestavění: Explore (rychlé hledání), Plan, General-purpose
- Vlastní: `.claude/agents/<nazev>.md` s YAML frontmatter
- Foreground (blokující) vs. background (paralelní, Ctrl+B)
- Klíčové pro ochranu kontextu — verbose operace delegujte na subagenta

---

## 3.6 Hooks — automatizace reakcí na události

**Doba studia:** 15 minut

### Co jsou hooks

Hooks jsou **deterministické skripty**, které se automaticky spouští při určitých událostech Claude Code. Na rozdíl od CLAUDE.md instrukcí (které Claude může ignorovat) hooks se **vždy** provedou.

### Kdy použít hooks místo CLAUDE.md

| Situace | CLAUDE.md | Hook |
|---------|-----------|------|
| "Po editaci spusť prettier" | Může zapomenout | **Hook** — vždy se spustí |
| "Neupravuj .env" | Může porušit | **Hook** — zablokuje s exit 2 |
| "Notifikuj mě, když Claude potřebuje schválení" | Neumí | **Hook** — pošle notifikaci |
| "Používej camelCase" | **CLAUDE.md** — soft pravidlo | Přehnané pro hook |

**Pravidlo:** Hooks pro deterministické akce. CLAUDE.md pro návody a konvence.

### Klíčové hook eventy pro začátek

Claude Code má celkem **17 hook eventů**. Pro začátek stačí znát tyto:

| Event | Kdy se spustí | Typické použití |
|-------|---------------|-----------------|
| **PreToolUse** | Před provedením akce | Blokování nebezpečných akcí, validace |
| **PostToolUse** | Po provedení akce | Auto-formátování, lint po editaci |
| **Stop** | Claude dokončil odpověď | Ověření, že úkol je kompletní |
| **Notification** | Claude posílá notifikaci | Vlastní notifikace (zvuk, Slack, ...) |
| **UserPromptSubmit** | Po odeslání promptu | Pre-processing vstupů |
| **SessionStart** | Start/resume sezení | Inicializace, re-inject kontextu po kompakci |

> Další eventy: `SubagentStart/Stop`, `PreCompact`, `SessionEnd`, `PermissionRequest`, `ConfigChange`, `WorktreeCreate/Remove`, `TeammateIdle`, `TaskCompleted` a další. Kompletní seznam: [Hooks Guide](https://code.claude.com/docs/en/hooks-guide).

### Nastavení přes /hooks

Nejsnadnější cesta:
```
/hooks
```
→ vyberte event → přidejte příkaz. Uloží se do settings.

### Příklad 1: Auto-formátování po editaci

```json
// .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

Po každé editaci/zápisu souboru Claude automaticky spustí prettier.

### Příklad 2: Blokování úprav chráněných souborů

Skript `.claude/hooks/protect-files.sh`:
```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

PROTECTED=(".env" "package-lock.json" ".git/" "migrations/")
for pattern in "${PROTECTED[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blokováno: $FILE_PATH odpovídá chráněnému vzoru '$pattern'" >&2
    exit 2  # Exit 2 = zablokovat akci
  fi
done
exit 0  # Exit 0 = povolit
```

Hook konfigurace:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
          }
        ]
      }
    ]
  }
}
```

### Příklad 3: Notifikace

**Windows (PowerShell):**
```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "powershell -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code potřebuje pozornost')\""
          }
        ]
      }
    ]
  }
}
```

**macOS:**
```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude Code potřebuje pozornost\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

> **Poznámka k platformám:** Hook příkazy jsou shell příkazy — na Windows se spouští přes `bash` (Git Bash). Pokud potřebujete nativní Windows příkazy, použijte `powershell -Command "..."`. Složitější skripty doporučujeme psát v Node.js nebo Pythonu pro přenositelnost.

> **Debugging hooks:** Pokud hook nefunguje podle očekávání, otestujte příkaz nejdřív manuálně v terminálu. Hook stdin simulujte: `echo '{"tool_name":"Edit","tool_input":{"file_path":".env"}}' | ./vas-hook.sh`. Zkontrolujte exit code: `echo $?`. Stderr zprávy se zobrazí Claudovi (při exit 2) nebo se zalogují.

### Jak hooks komunikují

- **stdin** — JSON s informacemi o události (tool_name, tool_input, ...)
- **exit 0** — akce pokračuje; stdout se přidá do kontextu
- **exit 2** — akce zablokována; stderr se ukáže Claude jako feedback
- **jiný exit** — akce pokračuje; stderr se zaloguje

### Tři typy hooks

| Typ | Jak funguje | Kdy použít |
|-----|-------------|------------|
| `command` | Spustí shell příkaz | Formátování, validace, notifikace |
| `prompt` | LLM vyhodnotí podmínku (Haiku) | Kontrola, zda je úkol kompletní |
| `agent` | Subagent s nástroji ověří výsledek | Spuštění testů po dokončení |

> **Zdroj:** [Hooks Guide](https://code.claude.com/docs/en/hooks-guide)

### Vyzkoušejte

1. Spusťte `/hooks` a nastavte PostToolUse hook pro auto-formátování (prettier/black/gofmt)
2. Editujte soubor přes Claude a ověřte, že se automaticky naformátoval
3. Vytvořte PreToolUse hook, který blokuje editaci `.env`
4. Zkuste editovat `.env` — Claude by měl dostat feedback o blokaci

### Shrnutí
- Hooks = deterministické skripty na lifecycle events — vždy se provedou
- 17 eventů, klíčové: PreToolUse (blokování), PostToolUse (formátování), Stop (ověření), Notification
- Exit 0 = povolit, exit 2 = zablokovat
- `/hooks` pro interaktivní nastavení, `settings.json` pro sdílení s týmem
- Tři typy: command (shell), prompt (LLM ověření), agent (subagent s nástroji)

---

## 3.7 Plugins — rozšíření ekosystému

**Doba studia:** 10 minut

### Co jsou plugins

Plugin = **balíček**, který kombinuje skills, hooks, subagenty a MCP servery do jedné instalovatelné jednotky. Sdílení s týmem nebo komunitou.

| Přístup | Skill namespace | Kdy |
|---------|----------------|-----|
| Standalone (`.claude/`) | `/hello` | Osobní, projektové, experimenty |
| Plugin | `/plugin-name:hello` | Sdílení, distribuce, verze |

### Instalace a správa

```
/plugins
```

Ve VS Code se otevře grafické rozhraní. V CLI interaktivní menu:
- Browse marketplace
- Install / uninstall
- Scope: user, project, local

### Plugin marketplace

Plugin marketplace je registr pluginů. Anthropic provozuje výchozí, ale týmy si mohou vytvořit vlastní.

Po instalaci se plugin automaticky stáhne a jeho skills, hooks, agents a MCP servery se aktivují.

### Vytvoření vlastního pluginu

Struktura:
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json       # Manifest (povinný — jediný soubor v tomto adresáři!)
├── commands/             # Příkazy (markdown soubory)
├── skills/               # Skills (SKILL.md soubory)
├── agents/               # Subagenti
├── hooks/
│   └── hooks.json        # Hooks konfigurace
├── .mcp.json             # MCP servery
├── .lsp.json             # LSP servery (code intelligence)
├── settings.json         # Výchozí nastavení pluginu
└── README.md
```

Manifest `.claude-plugin/plugin.json`:
```json
{
  "name": "my-plugin",
  "description": "Popis pluginu",
  "version": "1.0.0"
}
```

> **Důležité:** Adresáře `commands/`, `agents/`, `skills/`, `hooks/` patří do **kořene** pluginu, nikoli do `.claude-plugin/`. Uvnitř `.claude-plugin/` je **pouze** `plugin.json`.

Testování lokálně:
```bash
claude --plugin-dir ./my-plugin
```

> **Zdroj:** [Plugins](https://code.claude.com/docs/en/plugins), [Discover Plugins](https://code.claude.com/docs/en/discover-plugins)

### Vyzkoušejte

1. Spusťte `/plugins` a projděte marketplace
2. Nainstalujte plugin, který vás zaujme
3. Vyzkoušejte jeho skills (budou mít prefix `/plugin-name:skill-name`)
4. Pokud chcete sdílet vlastní setup: vytvořte jednoduchý plugin z vašich existujících skills

### Shrnutí
- Plugin = balíček skills + hooks + agents + MCP
- `/plugins` pro marketplace, instalaci a správu
- Namespace: `/plugin-name:skill-name`
- Lokální testování: `claude --plugin-dir ./plugin`

---

## 3.8 VS Code rozšíření — pokročilé funkce

**Doba studia:** 10 minut

### Více konverzací najednou

- **Open in New Tab** — nová konverzace v záložce editoru
- **Open in New Window** — nová konverzace v samostatném okně VS Code

Každá konverzace má vlastní kontext. Vzorové použití:
- Tab 1: implementace feature
- Tab 2: code review / dotazy na architekturu
- Tab 3: debugging

### Chrome integrace

Propojí Claude Code s prohlížečem Chrome pro testování webových aplikací:

```bash
claude --chrome   # Spuštění s Chrome podporou
# nebo v sezení:
/chrome
```

Prerekvizity:
- Google Chrome nebo Microsoft Edge (Brave, Arc a jiné Chromium prohlížeče **nejsou** podporovány)
- Rozšíření „Claude in Chrome" (v1.0.36+) z Chrome Web Store
- **Přímý plán Anthropic** (Pro, Max, Teams, Enterprise) — nefunguje přes Bedrock, Vertex AI ani Foundry
- **Nepodporováno ve WSL** (Windows Subsystem for Linux) — použijte nativní Windows

Použití v promptu:
```
Otevři localhost:3000, zkus odeslat formulář s nevalidními daty
a zkontroluj, zda se zobrazí chybové hlášky.
```

Claude otevírá nové taby, interaguje s DOM, čte konzoli, sdílí vaše přihlášení.

> **Pozor na kontext:** Zapnutí Chrome by default (přes `/chrome` → "Enabled by default") zvyšuje spotřebu kontextu, protože browser nástroje se načítají vždy. Doporučení: zapínejte Chrome jen když ho potřebujete (`--chrome` flag nebo `/chrome` v sezení).

### Git worktrees

Pro paralelní práci na více věcech:
```bash
claude --worktree feature-auth     # Pojmenovaný worktree
claude --worktree                  # Auto-generovaný název
```

Worktree = izolovaná kopie repozitáře s vlastní větví. Po dokončení se worktree nabídne k úklidu.

> **Tip:** Přidejte `.claude/worktrees/` do `.gitignore`.

### Resuming vzdálených sezení

Sezení spuštěné na claude.ai/code můžete obnovit lokálně ve VS Code:
- Otevřete historii sezení → záložka "Remote"
- Vyberte vzdálené sezení → pokračujte lokálně

### @terminal:name

Zahrnutí výstupu z terminálu do promptu:
```
@terminal:dev  Proč server spadl? Podívej se na error log.
```

> **Zdroj:** [VS Code](https://code.claude.com/docs/en/vs-code), [Chrome](https://code.claude.com/docs/en/chrome)

### Vyzkoušejte

1. Otevřete dvě konverzace (Open in New Tab) — v jedné implementujte, ve druhé se ptejte
2. Pokud máte webovou aplikaci: zkuste Chrome integraci (`/chrome`)
3. Zkuste worktree: `claude --worktree experiment`
4. Použijte `@terminal:nazev` pro zahrnutí výstupu z terminálu

### Shrnutí
- Multi-tab konverzace pro paralelní práci
- Chrome integrace: `/chrome` pro testování webapps v reálném prohlížeči
- Worktrees: izolované kopie repo pro paralelní úkoly
- `@terminal:name` pro kontext z terminálu

---

## 3.9 Piping a CLI jako unix nástroj

**Doba studia:** 10 minut

### Claude Code jako součást pipeline

`claude -p "prompt"` je neinteraktivní režim (print mode) — přijme vstup, vrátí výstup, skončí. Skvělé pro řetězení s dalšími nástroji.

### Piping dat dovnitř

```bash
# Analýza chyb z logů
cat error.log | claude -p "Vysvětli root cause této chyby"

# Git diff jako commit message
git diff --staged | claude -p "Napiš commit message pro tyto změny"

# Vysvětlení souboru
cat src/complex-module.ts | claude -p "Vysvětli tento kód"

# Shrnutí projektu z git logu
git log --oneline -20 | claude -p "Shrň, na čem se pracovalo"
```

### Piping dat ven

```bash
# Uložení výstupu
claude -p "Vypiš všechny API endpointy v projektu" > endpoints.txt

# Strukturovaný výstup pro zpracování
claude -p "Vypiš endpointy jako JSON" --output-format json | jq '.'

# Řetězení
claude -p "Najdi TODO komentáře" | claude -p "Roztřiď podle priority"
```

### Výstupní formáty

| Formát | Flag | Použití |
|--------|------|---------|
| Plain text | `--output-format text` (výchozí) | Lidsky čitelný výstup |
| JSON | `--output-format json` | Strojové zpracování |
| Stream JSON | `--output-format stream-json` | Real-time zpracování |

### Claude jako linter v package.json

```json
{
  "scripts": {
    "lint:claude": "claude -p 'Jsi linter. Podívej se na changes vs main a hlásí problémy s překlepy. Formát: soubor:řádek — popis.'"
  }
}
```

> **Zdroj:** [Common Workflows](https://code.claude.com/docs/en/common-workflows)

### Vyzkoušejte

1. `git log --oneline -20 | claude -p "Shrň, na čem se v projektu pracovalo"`
2. `git diff --staged | claude -p "Napiš commit message"` (pokud máte staged changes)
3. `cat [váš soubor] | claude -p "Najdi potenciální bugy"` > review.txt
4. Zkuste `--output-format json` a zpracujte výstup přes `jq`

### Shrnutí
- `claude -p "prompt"` = neinteraktivní režim pro skripty a piping
- Pipe in: `cat soubor | claude -p "..."`, pipe out: `claude -p "..." > výstup`
- Tři výstupní formáty: text, json, stream-json
- Kombinujte s git, jq, a dalšími CLI nástroji

---

## 3.10 Začlenění Claude Code do každodenního workflow

**Doba studia:** 10 minut

### Typický pracovní den s Claude Code

**Ráno — start:**
```bash
claude -c                    # Pokračovat ve včerejším úkolu
# nebo
claude                       # Nové sezení pro dnešní práci
```

**Průběžně — implementace:**
```
[Plan Mode] Analyzuj, jak přidat feature X. Navrhni postup.
[/clear, Normal Mode] Implementuj krok 1. Spusť testy.
[/clear] Implementuj krok 2. Spusť testy.
[/clear] Implementuj krok 3. Commitni a vytvoř PR.
```

Klíčový vzorec: **jeden úkol = jedno sezení**. `/clear` mezi kroky.

**Code review:**
```
Zkontroluj diff oproti main. Hledej bugy, edge cases, bezpečnostní problémy.
```
Nebo přes piping: `git diff main | claude -p "Code review, hledej bugy"`

**Debugging:**
```
Při spuštění npm test dostávám tento error: [vložte error].
Najdi příčinu a oprav.
```

**Dokumentace:**
```
Zdokumentuj modul src/payments/. Přidej JSDoc ke všem exportovaným funkcím.
```

### Kdy Claude Code používat — a kdy ne

| Silné stránky (používejte) | Slabé stránky (zvažte jiný přístup) |
|----------------------------|--------------------------------------|
| Boilerplate kód, opakující se vzory | Velmi kreativní architektonická rozhodnutí |
| Debugging s chybovými hláškami | Extrémně doménově specifická logika |
| Psaní a opravování testů | Kód, kde nerozumíte výstupu |
| Code review a refactoring | Ultra-citlivý bezpečnostní kód |
| Dokumentace | Práce s daty, která nesmíte sdílet |
| Git workflow (commit, PR) | |
| Vysvětlení cizího kódu | |

### Měření produktivity

Po týdnu s Claude Code si odpovězte:
- Kolik úkolů jsem delegoval na Claude?
- U kolika jsem musel výrazně korigovat výstup?
- Kde mi Claude ušetřil nejvíc času?
- Kde naopak Claude zdržoval?

Odpovědi vám pomohou doladit, na co Claude Code používat a na co ne.

### Vyzkoušejte

Po dobu jednoho pracovního dne se u **každého úkolu** zastavte a zvažte:
1. Může to Claude Code udělat rychleji než já?
2. Pokud ano — delegujte.
3. Na konci dne vyhodnoťte: kde pomohl, kde překážel.

### Shrnutí
- Jeden úkol = jedno sezení, `/clear` mezi nimi
- Claude Code exceluje: debugging, testy, boilerplate, review, dokumentace, git
- Nevhodný pro: ultra-citlivý kód, doménově specifická logika, data, která nesmíte sdílet
- Po týdnu vyhodnoťte, kde pomáhá a kde ne

---

## Milník Úrovně 3

Než přejdete na Úroveň 4, ověřte si:

- [ ] **Oprávnění:** Mám nastavená permission rules v `.claude/settings.json`, nemusím opakovaně schvalovat běžné příkazy
- [ ] **MCP:** Používám alespoň jeden MCP server (GitHub, DB, Sentry, ...)
- [ ] **Skill:** Vytvořil jsem vlastní skill a umím ho vyvolat přes `/nazev`
- [ ] **Subagent:** Vytvořil jsem vlastní subagent nebo používám delegování na vestavěné
- [ ] **Hook:** Mám nastavený alespoň jeden hook (auto-formátování nebo blokování)
- [ ] **Plugins:** Prozkoumal jsem marketplace a vím, jak nainstalovat plugin
- [ ] **VS Code:** Používám multi-tab konverzace a další pokročilé funkce
- [ ] **Piping:** Umím použít `claude -p` v pipeline s dalšími CLI nástroji
- [ ] **Denní workflow:** Claude Code je běžnou součástí mého pracovního dne

**Všechny body splněny?** Pokračujte na [Úroveň 4: Pokročilý](./osnova-claude-code.md).

---

> **Zdroje pro tuto úroveň:**
> - [Permissions](https://code.claude.com/docs/en/permissions) — oprávnění do hloubky
> - [Settings](https://code.claude.com/docs/en/settings) — konfigurace
> - [MCP](https://code.claude.com/docs/en/mcp) — externí nástroje
> - [Skills](https://code.claude.com/docs/en/skills) — vlastní skills
> - [Subagents](https://code.claude.com/docs/en/sub-agents) — delegování práce
> - [Hooks Guide](https://code.claude.com/docs/en/hooks-guide) — automatizace
> - [Plugins](https://code.claude.com/docs/en/plugins) — rozšíření ekosystému
> - [VS Code](https://code.claude.com/docs/en/vs-code) — pokročilé VS Code funkce
> - [Chrome](https://code.claude.com/docs/en/chrome) — Chrome integrace
> - [Common Workflows](https://code.claude.com/docs/en/common-workflows) — piping a CLI
