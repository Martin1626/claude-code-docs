# Úroveň 4: Pokročilý — Automatizace, CI/CD a orchestrace

> **Časová náročnost:** 7 kapitol, každá 10–20 minut. Celkem cca 2–3 hodiny rozložené do 2–4 týdnů.
> **Předpoklady:** Zvládnutá Úroveň 3 (milník splněn). Máte permission rules, MCP servery, skills, subagenty, hooks.
> **Cíl úrovně:** Používat Claude Code programaticky ve skriptech a CI/CD, ovládat pokročilé hooks, orchestrovat multi-agentní týmy, a zabezpečit prostředí sandboxingem.

---

## 4.1 Headless mode — skriptování a automatizace

**Doba studia:** 15 minut

### Od interaktivního k programatickému

V Úrovni 3 jste poznali `claude -p "prompt"` pro jednoduché piping. Headless mode jde dál — umožňuje plnou programatickou kontrolu: strukturovaný výstup, validace schématem, správu sezení a integraci do skriptů.

### Strukturovaný JSON výstup

```bash
# Základní JSON výstup
claude -p "Shrň tento projekt" --output-format json
```

Výstup obsahuje:
```json
{
  "result": "Textový výsledek Claude...",
  "session_id": "abc123...",
  "structured_output": null
}
```

Klíčové pole: `result` (text odpovědi), `session_id` (pro pokračování), `structured_output` (při použití schématu).

### JSON Schema — validovaný výstup

Potřebujete výstup v konkrétní struktuře? Použijte `--json-schema`:

```bash
claude -p "Extrahuj názvy funkcí z auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

Výstup (ve `structured_output`, ne v `result`):
```json
{
  "result": "...",
  "structured_output": {
    "functions": ["login", "logout", "validate_token", "refresh_token"]
  }
}
```

> **Tip:** Strukturovaný výstup je v poli `structured_output`, ne `result`. Parsujte přes: `jq '.structured_output'`.

### Streaming výstup

Pro real-time zpracování:
```bash
# Stream JSON — každý řádek je JSON event
claude -p "Vysvětli rekurzi" --output-format stream-json --verbose

# Filtr pro textové delty (token po tokenu)
claude -p "Napiš báseň" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

### Auto-schvalování nástrojů

V headless mode neběží interaktivní dialog — musíte explicitně povolit nástroje:

```bash
# Povolení konkrétních nástrojů
claude -p "Spusť testy a oprav selhávající" \
  --allowedTools "Bash,Read,Edit"

# Přesné povolení Git příkazů
claude -p "Commitni staged changes" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

> **Bezpečnost:** Pravidlo `Bash(git diff *)` povolí příkazy začínající `git diff` (mezera před `*` je důležitá). Bez mezery by `Bash(git diff*)` povolil i `git diff-index`.

### Vlastní systémový prompt

```bash
# Přidání instrukcí k výchozím
gh pr diff "$PR_ID" | claude -p \
  --append-system-prompt "Jsi security engineer. Hledej zranitelnosti." \
  --output-format json

# Úplná náhrada systémového promptu
claude -p "Analyzuj kód" \
  --system-prompt "Jsi expert na performance. Hledej bottlenecky."
```

### Správa sezení

```bash
# Pokračování posledního sezení
claude -p "Teď se zaměř na databázové dotazy" --continue

# Obnovení konkrétního sezení (přes session_id)
session_id=$(claude -p "Začni review" --output-format json | jq -r '.session_id')
claude -p "Pokračuj v review" --resume "$session_id"
```

> **Poznámka:** Slash příkazy (`/commit`, `/review`) a user-invocable skills fungují jen v interaktivním režimu, ne s `-p`.

> **Zdroj:** [Headless](https://code.claude.com/docs/en/headless)

### Vyzkoušejte

1. Napište bash skript, který vezme soubor jako argument a přes `claude -p` vygeneruje jeho dokumentaci:
   ```bash
   cat "$1" | claude -p "Vygeneruj dokumentaci pro tento kód" > "$1.docs.md"
   ```
2. Zkuste `--json-schema` — nechte Claude extrahovat strukturovaná data z kódu
3. Použijte `--continue` pro multi-krokový headless workflow
4. Zkuste streaming s `--output-format stream-json`

### Shrnutí
- `claude -p` = headless/non-interactive režim pro skripty
- `--output-format json` + `--json-schema` = validovaný strukturovaný výstup (v poli `structured_output`)
- `--allowedTools` = explicitní povolení nástrojů (nutné pro editace a Bash v headless)
- `--append-system-prompt` / `--system-prompt` = vlastní instrukce
- `--continue` / `--resume <id>` = správa sezení mezi voláními

---

## 4.2 CI/CD integrace

**Doba studia:** 20 minut

### Claude Code v CI — proč a jak

Claude Code může běžet jako součást CI/CD pipeline: automatický code review při PR, opravy bugů, generování dokumentace, nebo plnění issues. Dva oficiální přístupy:

| Platforma | Integrace | Stav |
|-----------|-----------|------|
| **GitHub Actions** | `anthropics/claude-code-action@v1` | GA (v1.0) |
| **GitLab CI/CD** | Nativní `.gitlab-ci.yml` job | Beta (udržuje GitLab) |

### GitHub Actions — rychlý start

Nejrychlejší cesta:
```
/install-github-app
```
Spusťte přímo v Claude Code (vyžaduje admin přístup k repo, jen pro přímé Claude API — ne Bedrock/Vertex).

Manuální instalace:
1. Nainstalujte GitHub app: `https://github.com/apps/claude`
2. Přidejte `ANTHROPIC_API_KEY` do repository secrets
3. Vytvořte workflow soubor

### Základní workflow — @claude v komentářích

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

Kdokoliv napíše `@claude` v issue nebo PR komentáři — Claude odpoví a může provádět změny.

### Automatický code review při PR

```yaml
name: Code Review
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "/review"
          claude_args: "--max-turns 5"
```

### Klíčové parametry akce

| Parametr | Popis |
|----------|-------|
| `anthropic_api_key` | API klíč (povinný pro přímé Claude API) |
| `prompt` | Instrukce nebo skill (např. `/review`) |
| `claude_args` | CLI argumenty: `--max-turns`, `--model`, `--allowedTools`, `--mcp-config` |
| `trigger_phrase` | Fráze pro spuštění (výchozí: `@claude`) |
| `use_bedrock` | Použít AWS Bedrock místo přímého API |
| `use_vertex` | Použít Google Vertex AI |

> **Poznámka:** Výchozí model je Sonnet. Pro Opus: `claude_args: "--model claude-opus-4-6"`.

### Plánovaná automatizace

```yaml
name: Denní report
on:
  schedule:
    - cron: "0 9 * * *"    # Každý den v 9:00
jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Vygeneruj shrnutí včerejších commitů a otevřených issues"
          claude_args: "--model claude-opus-4-6"
```

### GitLab CI/CD

```yaml
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_STRATEGY: fetch
  before_script:
    - apk update && apk add --no-cache git curl bash
    - curl -fsSL https://claude.ai/install.sh | bash
  script:
    - claude -p "${AI_FLOW_INPUT:-'Shrň změny a navrhni vylepšení'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write"
      --debug
```

> **Bezpečnost v CI:** Vždy omezte nástroje (`--allowedTools`), kroky (`--max-turns`), a model. V CI není interaktivní schvalování — přemýšlejte o tom, co Claude smí dělat.

> **Zdroje:** [GitHub Actions](https://code.claude.com/docs/en/github-actions), [GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd)

### Vyzkoušejte

1. Přidejte `claude-code-action@v1` do GitHub Actions workflow vašeho projektu
2. Napište `@claude` komentář v PR — sledujte, jak Claude odpoví
3. Nastavte automatický code review při otevření PR (trigger: `pull_request`)
4. Pro GitLab: přidejte Claude job do `.gitlab-ci.yml`

### Shrnutí
- GitHub Actions: `anthropics/claude-code-action@v1` — GA, produkčně připravené
- GitLab CI/CD: nativní job s `claude -p` — Beta
- Bezpečnost: vždy omezte `--allowedTools`, `--max-turns`, model
- Použití: automatický code review, @claude trigger, plánované reporty, plnění issues

---

## 4.3 Hooks do hloubky

**Doba studia:** 20 minut

### Od command hooks k prompt a agent hooks

V Úrovni 3 jste poznali `command` hooks (shell skripty). Nyní přidáváme dva pokročilé typy:

| Typ | Jak funguje | Rozhodování | Timeout |
|-----|-------------|-------------|---------|
| `command` | Shell příkaz | Exit kódy (0/2) | 600 s |
| `prompt` | LLM vyhodnotí jednorázově (Haiku) | JSON `{ok, reason}` | 30 s |
| `agent` | Subagent s nástroji (Read, Grep, Glob), multi-turn | JSON `{ok, reason}` | 60 s |

### Prompt hook — příklad

Kontrola, zda Claude nekončí předčasně (Stop event):

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Zkontroluj, zda Claude splnil všechny požadavky. Hook vstup (JSON s polem last_assistant_message): $ARGUMENTS. Pokud úkol není dokončený, odpověz {\"ok\": false, \"reason\": \"popis co chybí\"}.",
            "model": "haiku"
          }
        ]
      }
    ]
  }
}
```

Když prompt hook vrátí `{ok: false}`, Claude pokračuje v práci a dostane `reason` jako feedback.

> **Prevence nekonečné smyčky:** Stop hook vstupní JSON obsahuje pole `stop_hook_active: true`, pokud Claude už pokračuje kvůli předchozímu stop hooku. Zkontrolujte toto pole a vraťte `{ok: true}`, aby se předešlo zacyklení.

### Agent hook — příklad

Ověření, že testy procházejí po dokončení:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "agent",
            "prompt": "Spusť testy projektu. Pokud nějaký selhává, odpověz {\"ok\": false, \"reason\": \"Selhávající testy: <detaily>\"}. Pokud prochází, odpověz {\"ok\": true, \"reason\": \"Testy OK\"}."
          }
        ]
      }
    ]
  }
}
```

Agent hook má přístup k read-only nástrojům (Read, Grep, Glob — **bez Bash**) a může provést až 50 kroků.

### Které eventy podporují které typy

| Eventy | command | prompt | agent |
|--------|---------|--------|-------|
| PreToolUse, PostToolUse, PostToolUseFailure | ano | ano | ano |
| PermissionRequest, Stop, SubagentStop | ano | ano | ano |
| UserPromptSubmit, TaskCompleted | ano | ano | ano |
| SessionStart, SessionEnd, Notification | ano | ne | ne |
| SubagentStart, TeammateIdle, PreCompact | ano | ne | ne |
| ConfigChange, WorktreeCreate, WorktreeRemove | ano | ne | ne |

### Pokročilé rozhodovací vzory

**PreToolUse — hookSpecificOutput:**

```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow",
    "permissionDecisionReason": "Automaticky povoleno hook pravidlem",
    "updatedInput": { "command": "npm test -- --coverage" },
    "additionalContext": "Přidán --coverage flag"
  }
}
```

Možnosti `permissionDecision`: `allow` (automaticky povolí), `deny` (zablokuje — feedback jde Claudovi), `ask` (zobrazí dialog uživateli).

Pomocí `updatedInput` můžete **modifikovat vstup nástroje** ještě před provedením — např. přidat flagy k příkazům.

**PostToolUse — rozšíření kontextu:**

```json
{
  "decision": "block",
  "reason": "Nalezen bezpečnostní problém v editovaném souboru",
  "additionalContext": "Soubor obsahuje hardcoded credentials na řádku 42"
}
```

### Async hooks

Neblokující hook, který běží na pozadí:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "node scripts/notify-slack.js",
            "async": true
          }
        ]
      }
    ]
  }
}
```

Async hooks nemohou blokovat ani vracet rozhodnutí. Výstup se doručí při dalším konverzačním tahu.

### SessionStart — injekce prostředí

Speciální proměnná `$CLAUDE_ENV_FILE` je k dispozici **jen v SessionStart** hooks. Zapište `export` příkazy pro nastavení proměnných prostředí pro celé sezení:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'export PROJECT_ENV=production' >> \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ]
  }
}
```

### Hooks ve skills a subagentů

Hooks lze definovat i ve frontmatter skills a subagentů — jsou aktivní jen po dobu běhu komponenty:

```markdown
---
name: deploy
hooks:
  Stop:
    - matcher: ""
      hooks:
        - type: prompt
          prompt: "Ověř, že deploy proběhl úspěšně..."
---
```

Pole `once: true` spustí hook jen jednou za sezení (užitečné pro inicializaci).

### Debugging hooks

```bash
claude --debug    # Detailní logy o provedení hooks
```

Nebo za běhu: **Ctrl+O** pro verbose mode, kde uvidíte hook výstupy.

> **Zdroj:** [Hooks Reference](https://code.claude.com/docs/en/hooks)

### Vyzkoušejte

1. Vytvořte prompt hook na Stop event — kontroluje, zda Claude splnil úkol kompletně
2. Vytvořte agent hook, který po Stop spustí testy
3. Zkuste PreToolUse hook s `updatedInput` — přidejte flag k Bash příkazu
4. Použijte `async: true` pro neblokující notifikaci (Slack, email)
5. Spusťte `claude --debug` a sledujte, jak se hooks provádějí

### Shrnutí
- Tři typy: command (shell), prompt (LLM jednorázově), agent (subagent s nástroji)
- Prompt/agent hooks odpovídají JSON `{ok, reason}` — `ok: false` = pokračuj/zablokuj
- PreToolUse: `permissionDecision` (allow/deny/ask) + `updatedInput` pro modifikaci vstupu
- Async hooks: `async: true` pro neblokující akce
- SessionStart + `$CLAUDE_ENV_FILE` pro injekci proměnných prostředí
- Debugging: `claude --debug` nebo Ctrl+O

---

## 4.4 MCP pokročilé techniky

**Doba studia:** 15 minut

### Claude Code jako MCP server

Claude Code může sloužit jako MCP server pro jiné nástroje:

```bash
claude mcp serve
```

Konfigurace v Claude Desktop:
```json
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"]
    }
  }
}
```

Tím zpřístupníte nástroje Claude Code (View, Edit, LS, ...) jiným MCP klientům.

> **Tip:** Pokud `claude` není v PATH, najděte úplnou cestu: `which claude` (macOS/Linux) nebo `where claude` (Windows).

### OAuth autentizace

Pro MCP servery vyžadující přihlášení (Sentry, Jira, ...):

```bash
# Automatický OAuth flow (server podporuje dynamic client registration)
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
# → /mcp → přihlásit se v prohlížeči

# Předkonfigurovaný OAuth (máte vlastní client ID)
claude mcp add --transport http \
  --client-id your-client-id --client-secret --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

- `--client-secret` vyzve k zadání hesla (maskovaný vstup)
- Alternativně: `MCP_CLIENT_SECRET` env var
- Secret uložen v systémové klíčence (macOS) nebo credentials souboru
- Pro veřejné OAuth klienty (bez secret): jen `--client-id`

### MCP Resources — @zmínky externích zdrojů

```
> Analyzuj @github:issue://123 a navrhni opravu
> Porovnej @postgres:schema://users s @docs:file://database/user-model
```

Formát: `@server:protocol://resource/path`. Resources se automaticky stáhnou a připojí jako přílohy. Fuzzy search v @ autocomplete menu.

### MCP Prompts jako příkazy

MCP servery mohou definovat prompts, které se zobrazí jako slash příkazy:

```
/mcp__github__list_prs
/mcp__github__pr_review 456
/mcp__jira__create_issue "Bug v login flow" high
```

Formát: `/mcp__servername__promptname`. Argumenty se parsují podle parametrů definovaných serverem.

### Tool Search — podrobnosti

| `ENABLE_TOOL_SEARCH` | Chování |
|----------------------|---------|
| `auto` (výchozí) | Aktivuje se při >10 % kontextu |
| `auto:5` | Vlastní threshold (5 %) |
| `true` | Vždy zapnuto |
| `false` | Vypnuto, všechny nástroje se načtou najednou |

> **Omezení:** Tool Search vyžaduje Sonnet 4+ nebo Opus 4+. Haiku modely **nepodporují** tool search.

Deaktivace přes deny pravidlo:
```json
{ "permissions": { "deny": ["MCPSearch"] } }
```

### Řízení velikosti MCP výstupu

| Proměnná | Popis | Výchozí |
|----------|-------|---------|
| `MAX_MCP_OUTPUT_TOKENS` | Max tokenů na výstup MCP nástroje | 25 000 |
| `MCP_TIMEOUT` | Timeout startu MCP serveru (ms) | — |

Varování se zobrazí při >10 000 tokenech.

### Managed MCP — organizační řízení

Pro enterprise týmy: centrální konfigurace MCP serverů.

**Exkluzivní řízení** (`managed-mcp.json`):
- macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- Linux/WSL: `/etc/claude-code/managed-mcp.json`
- Windows: `C:\Program Files\ClaudeCode\managed-mcp.json`

**Allowlist/Denylist** v managed settings:
```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverUrl": "https://mcp.company.com/*" }
  ],
  "deniedMcpServers": [
    { "serverName": "dangerous-server" }
  ]
}
```

Denylist má **absolutní přednost** před allowlistem.

### Windows specifika

Na nativním Windows (ne WSL) vyžadují lokální MCP servery přes `npx` wrapper `cmd /c`:
```bash
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```

> **Zdroj:** [MCP](https://code.claude.com/docs/en/mcp)

### Vyzkoušejte

1. Zkuste `claude mcp serve` — připojte Claude Code jako MCP server k jinému nástroji
2. Nainstalujte MCP server s OAuth (např. Sentry): `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp`
3. Zkuste MCP resources: `@server:protocol://path` v promptu
4. Nastavte `ENABLE_TOOL_SEARCH=auto:5` a sledujte, jak se nástroje načítají on-demand
5. Kombinujte dva MCP servery v jednom úkolu (např. GitHub + databáze)

### Shrnutí
- `claude mcp serve` = Claude Code jako MCP server pro jiné nástroje
- OAuth: `--client-id --client-secret` pro autentizované servery
- MCP Resources: `@server:protocol://path` pro @ zmínky externích zdrojů
- MCP Prompts: `/mcp__server__prompt` jako slash příkazy
- Tool Search: automatický on-demand loading (Sonnet 4+ / Opus 4+, ne Haiku)
- Managed MCP: organizační allowlist/denylist, `managed-mcp.json`

---

## 4.5 Agent Teams — multi-agentní orchestrace

**Doba studia:** 15 minut

### Co jsou Agent Teams

Agent Teams jsou **experimentální funkce** umožňující rozdělit práci mezi více nezávislých Claude Code instancí (teammates), koordinovaných jedním „team leadem".

> **Status:** Experimentální, ve výchozím stavu vypnuté.

### Zapnutí

```json
// settings.json nebo .claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Nebo: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude`

### Architektura

| Komponenta | Role |
|------------|------|
| **Team lead** | Hlavní sezení — vytváří tým, přiděluje úkoly, koordinuje |
| **Teammates** | Samostatné Claude Code instance, každá pracuje na svém úkolu |
| **Task list** | Sdílený seznam úkolů, teammates si je přebírají |
| **Mailbox** | Systém zpráv pro komunikaci mezi agenty |

### Režimy zobrazení

| Režim | Kde funguje | Popis |
|-------|-------------|-------|
| `in-process` | Všude | Všichni v jednom terminálu, **Shift+Down** pro přepínání |
| `tmux` | tmux / iTerm2 | Každý teammate ve vlastním panelu |
| `auto` (výchozí) | — | tmux pokud je dostupný, jinak in-process |

```bash
claude --teammate-mode in-process    # Vynutit in-process
```

> **Omezení:** Split panes (tmux mode) **nefungují** ve VS Code integrovaném terminálu, Windows Terminal ani Ghostty.

### Klávesové zkratky (in-process mode)

| Zkratka | Akce |
|---------|------|
| **Shift+Down** | Přepnout na dalšího teammate |
| **Enter** | Zobrazit sezení teammate |
| **Escape** | Přerušit aktuální tah |
| **Ctrl+T** | Zobrazit/skrýt task list |

### Subagenti vs. Agent Teams

| Aspekt | Subagenti | Agent Teams |
|--------|-----------|-------------|
| Kontext | Vlastní okno, výsledky vrací volajícímu | Vlastní okno, plně nezávislí |
| Komunikace | Reportují jen hlavnímu agentovi | Komunikují mezi sebou (mailbox) |
| Koordinace | Hlavní agent řídí vše | Sdílený task list, sami si přebírají úkoly |
| Vhodné pro | Zaměřené úkoly, potřebujete výsledek | Komplexní práce vyžadující diskusi |
| Token cost | Nižší (sumarizované výsledky) | Vyšší (nezávislé instance) |

### Hooks pro kvalitní kontrolu

```json
{
  "hooks": {
    "TaskCompleted": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "agent",
            "prompt": "Ověř, že úkol '$ARGUMENTS' je skutečně hotový — testy prochází, kód je čistý."
          }
        ]
      }
    ]
  }
}
```

`TeammateIdle` hook (exit 2 = pošle feedback a udrží teammate v práci), `TaskCompleted` hook (exit 2 = zabrání označení úkolu jako hotového).

### Doporučení

- **Velikost týmu:** 3–5 teammates, 5–6 úkolů na teammate
- **Soubory:** Každý teammate pracuje na jiných souborech — minimalizujte konflikty
- **Plánování:** Nechte teammates nejdřív plánovat (Plan Mode), pak schvalte
- **Úklid:** Vždy ukliďte přes lead: „Clean up the team"

### Známá omezení

- Žádné obnovení sezení s in-process teammates (`/resume` a `/rewind` neobnovují)
- Jeden tým na sezení, žádné vnořené týmy
- Lead je fixní po celou dobu života týmu
- Oprávnění se nastaví při spawnu — nelze měnit za běhu

> **Zdroj:** [Agent Teams](https://code.claude.com/docs/en/agent-teams)

### Vyzkoušejte

1. Zapněte experimentální funkci: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 claude`
2. Požádejte Claude o rozdělení úkolu do týmu (např. „Rozděl tento refactoring mezi 3 agenty")
3. Sledujte task list (Ctrl+T) a komunikaci mezi agenty
4. Zkuste `--teammate-mode in-process` a přepínejte Shift+Down
5. Po dokončení: „Clean up the team"

### Shrnutí
- Agent Teams = experimentální multi-agentní orchestrace
- Team lead koordinuje teammates přes sdílený task list a mailbox
- Dva zobrazovací režimy: in-process (Shift+Down) nebo tmux (split panes)
- Subagenti = zaměřené úkoly; Agent Teams = komplexní práce s diskusí
- Hooks: `TaskCompleted` a `TeammateIdle` pro quality gates
- Omezení: experimentální, jeden tým/sezení, split panes ne ve VS Code

---

## 4.6 Sandboxing a bezpečnost

**Doba studia:** 15 minut

### Proč sandbox

Bez sandboxu může Claude (s vašimi oprávněními) spustit libovolný příkaz. Sandbox přidává **OS-level izolaci** — omezuje, kam může zapisovat a kam se připojit po síti.

### Podpora platforem

| Platforma | Technologie | Stav |
|-----------|-------------|------|
| **macOS** | Seatbelt (vestavěný) | Funguje out-of-the-box |
| **Linux** | bubblewrap + socat | Vyžaduje instalaci |
| **WSL2** | bubblewrap + socat | Funguje (stejně jako Linux) |
| **WSL1** | — | **Nepodporováno** (chybí kernel features) |
| **Nativní Windows** | — | **Nedostupné** (plánováno). Použijte WSL2 pro sandbox. |

Instalace na Linux/WSL2:
```bash
# Ubuntu/Debian
sudo apt-get install bubblewrap socat

# Fedora
sudo dnf install bubblewrap socat
```

### Zapnutí

```
/sandbox
```

Nabídne výběr režimu a zobrazí instrukce pro instalaci závislostí.

### Dva režimy

| Režim | Chování |
|-------|---------|
| **Auto-allow** | Sandboxované Bash příkazy se schvalují automaticky. Příkazy, které nelze sandboxovat, prochází standardním schvalováním. |
| **Regular permissions** | Všechny příkazy prochází standardním schvalováním, i když jsou sandboxované. |

> **Důležité:** Auto-allow mode funguje nezávisle na permission mode. I v Default permission mode budou sandboxované příkazy auto-schváleny.

### Filesystem izolace

- **Zápis:** Povolen jen do CWD a podadresářů (výchozí)
- **Čtení:** Povolen z celého systému, kromě zakázaných adresářů
- **Konfigurovatelné:** Vlastní povolené/zakázané cesty v settings

### Network izolace

- Omezení domén přes proxy server běžící **mimo** sandbox
- Nové domény vyžadují schválení uživatelem
- Platí pro **všechny skripty, programy a podprocesy**

### Escape hatch

Když příkaz selže kvůli sandboxu, Claude může zkusit `dangerouslyDisableSandbox`. Takové příkazy pak prochází standardním schvalováním.

Zakázání escape hatch:
```json
{
  "sandbox": {
    "allowUnsandboxedCommands": false
  }
}
```

### Bezpečnostní model — hlavní principy

| Ochrana | Popis |
|---------|-------|
| **Permission system** | Read-only výchozí; explicitní souhlas pro editace a příkazy |
| **Sandbox** | OS-level filesystem + network izolace |
| **Command blocklist** | `curl` a `wget` ve výchozím stavu blokovány |
| **Prompt injection detekce** | Kontext-aware analýza, izolovaná okna pro WebFetch |
| **Command injection detekce** | Podezřelé příkazy vyžadují manuální schválení i pokud jsou v allowlistu |
| **Fail-closed** | Nerozpoznané příkazy = manuální schválení |

### Windows specifika

- **Ne** povolujte WebDAV ani `\\*` cesty — WebDAV může obejít permission systém
- WSL1 nepodporuje sandbox — používejte WSL2
- Nativní Windows sandbox je plánovaný

### Kompatibilita

Některé nástroje jsou nekompatibilní se sandboxem:
- **watchman** (jest): použijte `jest --no-watchman`
- **docker**: zvažte přidání do výjimek (`excludedCommands`)
- Mnoho CLI nástrojů potřebuje přístup k hostiteli — povolujte postupně podle potřeby

### Co sandbox neřeší

1. **Network filtering:** Filtruje domény, ne obsah. Široké domény (github.com) mohou umožnit exfiltraci
2. **Unix sockets:** `allowUnixSockets` dává přístup k systémovým službám (Docker socket = host přístup)
3. **Filesystem escalation:** Příliš široké write oprávnění do `$PATH` nebo shell konfigurací (.bashrc) umožňuje eskalaci

> **Zdroje:** [Sandboxing](https://code.claude.com/docs/en/sandboxing), [Security](https://code.claude.com/docs/en/security)

### Vyzkoušejte

1. Spusťte `/sandbox` a vyberte Auto-allow mode
2. Na Linux/WSL2: nainstalujte bubblewrap: `sudo apt-get install bubblewrap socat`
3. Zkuste editovat soubor mimo CWD — sandbox by měl zablokovat
4. Sledujte network přístupy — nové domény vyžadují schválení
5. Zkuste zakázat escape hatch: `"allowUnsandboxedCommands": false`

### Shrnutí
- `/sandbox` zapne OS-level izolaci (macOS: Seatbelt, Linux/WSL2: bubblewrap)
- Auto-allow mode: sandboxované příkazy bez ptaní, ostatní přes standardní flow
- Filesystem: zápis jen do CWD, čtení odevšad (konfigurovatelné)
- Network: domain-level omezení přes proxy
- **Windows:** WSL2 ano, WSL1 ne, nativní Windows zatím nedostupné — pro sandbox přejděte na WSL2
- Sandbox nezabrání všemu — rozumějte limitacím (sockets, broad domains)

---

## 4.7 Vlastní pluginy a marketplace

**Doba studia:** 15 minut

### Od skills k pluginům

V Úrovni 3 jste vytvořili skills, hooks a subagenty v `.claude/`. Plugin je **distribuovatelný balíček** — zabalí vše do jedné instalovatelné jednotky s manifestem a verzováním.

### Úplná struktura pluginu

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json           # Manifest (JEDINÝ soubor v tomto adresáři)
├── commands/                  # Příkazy (markdown soubory, zobrazí se jako /příkaz)
├── skills/                    # Skills (SKILL.md soubory)
├── agents/                    # Subagenti (markdown s frontmatter)
├── hooks/
│   └── hooks.json             # Hooks konfigurace
├── .mcp.json                  # MCP servery
├── .lsp.json                  # LSP servery (diagnostika, navigace, typy)
├── settings.json              # Výchozí nastavení (jen `agent` sekce)
├── scripts/                   # Pomocné skripty
├── LICENSE
└── CHANGELOG.md
```

### Manifest — plugin.json

```json
{
  "name": "my-team-tools",
  "version": "1.2.0",
  "description": "Sdílené nástroje pro náš tým",
  "author": { "name": "Jan Novák" },
  "keywords": ["review", "deploy", "testing"],
  "homepage": "https://github.com/jannovak/my-team-tools"
}
```

**Povinné pole:** pouze `name` (kebab-case, bez mezer).

Další metadata: `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`.

**Component paths** (volitelné — doplňují výchozí adresáře, nenahrazují je):
```json
{
  "name": "my-plugin",
  "commands": "./custom-commands",
  "agents": ["./agents", "./extra-agents"],
  "hooks": { "PostToolUse": [...] },
  "mcpServers": { "my-server": {...} },
  "lspServers": { "my-lsp": {...} }
}
```

### Hooks v pluginech

```json
// hooks/hooks.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

`${CLAUDE_PLUGIN_ROOT}` = absolutní cesta k adresáři pluginu. Používejte pro skripty a konfigurační soubory.

### LSP servery v pluginech

```json
// .lsp.json
{
  "lspServers": {
    "pyright": {
      "command": "npx",
      "args": ["-y", "pyright-langserver", "--stdio"],
      "extensionToLanguage": { ".py": "python" }
    }
  }
}
```

Hotové LSP pluginy: `pyright-lsp` (Python), `typescript-lsp`, `rust-lsp`.

### Instalace a správa

```bash
# CLI příkazy
claude plugin install my-plugin          # Instalace
claude plugin install my-plugin -s project  # Instalace pro tým
claude plugin uninstall my-plugin        # Odinstalace
claude plugin enable my-plugin           # Zapnout (pokud disabled)
claude plugin disable my-plugin          # Vypnout bez odinstalace
claude plugin update my-plugin           # Aktualizace

# Interaktivně
/plugins
```

### Scopy instalace

| Scope | Settings soubor | Kdy |
|-------|----------------|-----|
| `user` (výchozí) | `~/.claude/settings.json` | Osobní, všechny projekty |
| `project` | `.claude/settings.json` | Tým (commituje se) |
| `local` | `.claude/settings.local.json` | Lokální, gitignored |

### Verzování a caching

- Sémantické verzování: `MAJOR.MINOR.PATCH`, pre-release: `2.0.0-beta.1`
- Pluginy se kopírují do `~/.claude/plugins/cache`
- **Důležité:** Pokud změníte kód ale nezvýšíte verzi, uživatelé aktualizaci nedostanou (kvůli cache)

### Lokální vývoj a testování

```bash
# Načtení z lokálního adresáře
claude --plugin-dir ./my-plugin

# Více pluginů najednou
claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two

# Validace manifestu
claude plugin validate
```

### Debugging

```bash
claude --debug       # Detaily načítání pluginů
/debug               # V TUI režimu
```

Časté chyby:
- Event názvy jsou **case-sensitive**: `PostToolUse`, ne `postToolUse`
- Hook skripty musí být **executable**: `chmod +x script.sh`
- Hook skripty potřebují **shebang**: `#!/bin/bash` nebo `#!/usr/bin/env bash`

> **Zdroj:** [Plugins Reference](https://code.claude.com/docs/en/plugins-reference)

### Vyzkoušejte

1. Vytvořte minimální plugin: `mkdir -p my-plugin/.claude-plugin && echo '{"name":"my-plugin"}' > my-plugin/.claude-plugin/plugin.json`
2. Přidejte skill do `my-plugin/skills/hello/SKILL.md`
3. Testujte: `claude --plugin-dir ./my-plugin` a zkuste `/my-plugin:hello`
4. Přidejte hook do `my-plugin/hooks/hooks.json`
5. Zkuste `claude plugin validate` pro ověření manifestu

### Shrnutí
- Plugin = distribuovatelný balíček (skills + hooks + agents + MCP + LSP)
- `.claude-plugin/plugin.json` = manifest (povinný jen `name`)
- `${CLAUDE_PLUGIN_ROOT}` pro cesty k souborům pluginu
- Verzování: sémantické, cache = nutnost bumpu verze
- CLI: `claude plugin install/uninstall/enable/disable/update`
- Debugging: `claude --debug`, `claude plugin validate`, case-sensitive eventy

---

## Milník Úrovně 4

Než přejdete na Úroveň 5, ověřte si:

- [ ] **Headless mode:** Umím použít `claude -p` ve skriptu s `--output-format json` a `--json-schema`
- [ ] **CI/CD:** Claude Code je integrovaný do mého CI/CD pipeline (GitHub Actions nebo GitLab)
- [ ] **Hooks:** Mám pokročilé hooks — prompt-based nebo agent-based (ne jen command)
- [ ] **MCP pokročilé:** Znám OAuth, MCP Resources, Tool Search, nebo `claude mcp serve`
- [ ] **Agent Teams:** Rozumím konceptu a vím, kdy použít subagenty vs. Agent Teams
- [ ] **Sandbox:** Mám zapnutý sandbox (`/sandbox`) a rozumím jeho limitacím
- [ ] **Plugin:** Vytvořil jsem vlastní plugin s manifestem a umím ho distribuovat

**Všechny body splněny?** Pokračujte na [Úroveň 5: Expert / Platform Engineer](./osnova-claude-code.md) (volitelná).

---

> **Zdroje pro tuto úroveň:**
> - [Headless](https://code.claude.com/docs/en/headless) — programatické použití CLI
> - [GitHub Actions](https://code.claude.com/docs/en/github-actions) — CI/CD integrace
> - [GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd) — GitLab integrace
> - [Hooks Reference](https://code.claude.com/docs/en/hooks) — kompletní hooks reference
> - [MCP](https://code.claude.com/docs/en/mcp) — pokročilé MCP techniky
> - [Agent Teams](https://code.claude.com/docs/en/agent-teams) — multi-agentní orchestrace
> - [Sandboxing](https://code.claude.com/docs/en/sandboxing) — filesystem a network izolace
> - [Security](https://code.claude.com/docs/en/security) — bezpečnostní model
> - [Plugins Reference](https://code.claude.com/docs/en/plugins-reference) — pokročilé pluginy
