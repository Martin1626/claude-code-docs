# Úroveň 5: Expert / Platform Engineer — SDK, Enterprise a Governance

> **Časová náročnost:** 4 kapitoly, každá 15–20 minut. Celkem cca 1–1,5 hodiny.
> **Předpoklady:** Zvládnutá Úroveň 4 (milník splněn). Umíte headless mode, CI/CD, hooks, MCP, sandboxing.
> **Cíl úrovně:** Vytvářet vlastní AI agenty pomocí Agent SDK, nasadit Claude Code v enterprise prostředí (Bedrock, Vertex AI, Foundry), monitorovat využití přes OpenTelemetry a spravovat organizační politiky centrálně.
> **Tato úroveň je volitelná** — je pro vývojáře platforem a enterprise správce. Pokud nebudujete vlastní produkty s AI agenty ani nespravujete Claude Code pro tým/organizaci, klidně ji přeskočte.

---

## 5.1 Agent SDK — programatické agenty

**Doba studia:** 20 minut

### Od CLI k plnohodnotné knihovně

V Úrovni 4 jste používali `claude -p` pro skriptování. Agent SDK jde o úroveň výš — dává vám stejné nástroje, agentní smyčku a správu kontextu, které pohání Claude Code, ale jako **programovatelnou knihovnu** v Pythonu nebo TypeScriptu.

> **Poznámka k přejmenování:** Claude Code SDK byl přejmenován na **Claude Agent SDK**. Funkčně se nic nemění — jen nový název balíčku. Pokud migrujete ze starého SDK, viz [Migration Guide](https://platform.claude.com/docs/en/agent-sdk/migration-guide).

### Instalace

```bash
# Python
pip install claude-agent-sdk

# TypeScript
npm install @anthropic-ai/claude-agent-sdk
```

### Autentizace

SDK používá `ANTHROPIC_API_KEY` (z [Console](https://platform.claude.com/)):

```bash
export ANTHROPIC_API_KEY=your-api-key
```

Podporuje i third-party providery:
- **Bedrock:** `CLAUDE_CODE_USE_BEDROCK=1` + AWS credentials
- **Vertex AI:** `CLAUDE_CODE_USE_VERTEX=1` + GCP credentials
- **Foundry:** `CLAUDE_CODE_USE_FOUNDRY=1` + Azure credentials

> **Důležité:** Anthropic nepovoluje třetím stranám nabízet claude.ai přihlášení nebo rate limity pro produkty postavené na Agent SDK (pokud nemají výslovný souhlas). Používejte API klíče.

### Základní použití — funkce `query()`

Jádrem SDK je funkce `query()`, která vrací asynchronní stream zpráv:

**Python:**
```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Najdi a oprav bug v auth.py",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Bash"]
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

**TypeScript:**
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Najdi a oprav bug v auth.py",
  options: { allowedTools: ["Read", "Edit", "Bash"] }
})) {
  if ("result" in message) console.log(message.result);
}
```

### Rozdíl oproti Anthropic Client SDK

| Vlastnost | Client SDK (`anthropic`) | Agent SDK (`claude-agent-sdk`) |
|-----------|--------------------------|-------------------------------|
| Tool loop | Implementujete sami | Claude řeší autonomně |
| Vestavěné nástroje | Žádné | Read, Edit, Bash, Glob, Grep... |
| Kontext a sezení | Spravujete sami | Automatická správa |
| Ideální pro | Chatboty, RAG, jednoduché API volání | Autonomní agenty, CI/CD, automatizaci |

```python
# Client SDK — musíte implementovat smyčku:
response = client.messages.create(...)
while response.stop_reason == "tool_use":
    result = your_tool_executor(response.tool_use)
    response = client.messages.create(tool_result=result, **params)

# Agent SDK — Claude řeší vše sám:
async for message in query(prompt="Oprav bug v auth.py"):
    print(message)
```

### Vestavěné nástroje

Agent SDK obsahuje stejné nástroje jako Claude Code:

| Nástroj | Co dělá |
|---------|---------|
| **Read** | Čtení souborů v pracovním adresáři |
| **Write** | Vytváření nových souborů |
| **Edit** | Přesné úpravy existujících souborů |
| **Bash** | Spouštění příkazů, skriptů, git operací |
| **Glob** | Hledání souborů podle vzoru (`**/*.ts`) |
| **Grep** | Hledání v obsahu souborů (regex) |
| **WebSearch** | Vyhledávání na webu |
| **WebFetch** | Stahování a parsování webových stránek |
| **AskUserQuestion** | Dotazy na uživatele s multiple choice |

Oprávnění k nástrojům řídíte parametrem `allowed_tools` / `allowedTools`:

```python
# Read-only agent — nemůže nic měnit:
options=ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep"],
    permission_mode="bypassPermissions"
)
```

### Hooks v SDK

Na rozdíl od CLI (kde hooks jsou shell příkazy v settings.json), v SDK hooks definujete jako **callback funkce**:

**Python:**
```python
from datetime import datetime
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher

async def log_file_change(input_data, tool_use_id, context):
    file_path = input_data.get("tool_input", {}).get("file_path", "unknown")
    with open("./audit.log", "a") as f:
        f.write(f"{datetime.now()}: modified {file_path}\n")
    return {}

async def main():
    async for message in query(
        prompt="Refaktoruj utils.py",
        options=ClaudeAgentOptions(
            permission_mode="acceptEdits",
            hooks={
                "PostToolUse": [
                    HookMatcher(
                        matcher="Edit|Write",
                        hooks=[log_file_change]
                    )
                ]
            },
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)
```

Dostupné hook events: `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit` a další.

### Subagenti v SDK

Můžete definovat specializované agenty a delegovat jim práci:

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async def main():
    async for message in query(
        prompt="Použij code-reviewer agenta na review kódu",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Task"],
            agents={
                "code-reviewer": AgentDefinition(
                    description="Expert code reviewer.",
                    prompt="Analyzuj kvalitu kódu a navrhni zlepšení.",
                    tools=["Read", "Glob", "Grep"],
                )
            },
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)
```

> **Důležité:** Aby hlavní agent mohl spouštět subagenty, musí mít v `allowed_tools` nástroj `Task`.

### MCP servery v SDK

Připojení externích nástrojů přes MCP:

```python
options=ClaudeAgentOptions(
    mcp_servers={
        "playwright": {
            "command": "npx",
            "args": ["@playwright/mcp@latest"]
        }
    }
)
```

### Sezení — multi-turn konverzace

Zachycení `session_id` pro pokračování konverzace:

```python
session_id = None

# První dotaz — zachytíme session_id
async for message in query(
    prompt="Přečti autentizační modul",
    options=ClaudeAgentOptions(allowed_tools=["Read", "Glob"]),
):
    if hasattr(message, "subtype") and message.subtype == "init":
        session_id = message.session_id

# Pokračujeme s plným kontextem
async for message in query(
    prompt="Teď najdi všechna místa, která ho volají",
    options=ClaudeAgentOptions(resume=session_id),
):
    if hasattr(message, "result"):
        print(message.result)
```

### Claude Code features v SDK

SDK podporuje i souborovou konfiguraci Claude Code (CLAUDE.md, skills, commands, plugins). Pro aktivaci musíte **explicitně** nastavit `setting_sources`:

```python
options=ClaudeAgentOptions(setting_sources=["project"])
```

> **Důležité (breaking change od v0.1.0):** Od verze 0.1.0 SDK **nenačítá souborové konfigurace automaticky**. Bez `setting_sources=["project"]` agent nebude mít přístup k CLAUDE.md, skills, commands ani plugins. Navíc SDK od v0.1.0 používá minimální system prompt — pokud chcete plné chování Claude Code (včetně všech vestavěných instrukcí), nastavte: `system_prompt={"type": "preset", "preset": "claude_code"}`.

| Feature | Popis | Umístění |
|---------|-------|----------|
| Skills | Markdown instrukce | `.claude/skills/SKILL.md` |
| Slash commands | Vlastní příkazy | `.claude/commands/*.md` |
| Memory | Kontext projektu | `CLAUDE.md` |
| Plugins | Rozšíření | Programaticky přes `plugins` |

### Branding

Pokud integrujete Agent SDK do svého produktu:
- **Povoleno:** „Claude Agent", „{VášAgent} Powered by Claude"
- **Zakázáno:** „Claude Code" nebo „Claude Code Agent", napodobování vizuálního stylu Claude Code

### Vyzkoušejte

1. Nainstalujte `claude-agent-sdk` (Python nebo TypeScript).
2. Napište jednoduchého agenta, který najde všechny TODO komentáře ve vašem projektu a vytvoří z nich souhrnný soubor.
3. Přidejte `PostToolUse` hook, který loguje všechny editace do souboru `audit.log`.
4. Zkuste vytvořit subagenta specialistu na code review.

**Zdroje:**
- [Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Python SDK](https://platform.claude.com/docs/en/agent-sdk/python)
- [TypeScript SDK](https://platform.claude.com/docs/en/agent-sdk/typescript)
- [Example agents](https://github.com/anthropics/claude-agent-sdk-demos)

---

## 5.2 Enterprise nasazení — Bedrock, Vertex AI, Foundry

**Doba studia:** 20 minut

### Proč enterprise provideři?

Při použití Claude Code přes přímé Anthropic API data putují na servery Anthropic. Enterprise provideři (AWS Bedrock, Google Vertex AI, Microsoft Foundry) nabízejí:

- **Data residency** — data zůstávají ve vašem cloudovém prostředí
- **Stávající billing** — platíte přes existující AWS/GCP/Azure fakturu (PAYG)
- **IAM integrace** — řízení přístupu přes stávající identity management
- **Compliance** — CloudTrail, Audit Logs, Azure Monitor
- **Guardrails** — content filtering (Bedrock Guardrails)

### Srovnání možností nasazení

| Vlastnost | Teams/Enterprise | Console API | Bedrock | Vertex AI | Foundry |
|-----------|-----------------|-------------|---------|-----------|---------|
| **Ideální pro** | Většinu org. | Jednotlivce | AWS stack | GCP stack | Azure stack |
| **Billing** | $150/seat Premium, PAYG k dispozici (Teams); [Contact Sales](https://anthropic.com/contact-sales) (Enterprise) | PAYG | PAYG přes AWS | PAYG přes GCP | PAYG přes Azure |
| **Autentizace** | SSO/email | API klíč | API klíč nebo AWS creds | GCP creds | API klíč / Entra ID |
| **Claude na webu** | Ano | Ne | Ne | Ne | Ne |
| **Prompt caching** | Ano | Ano | Ano | Ano | Ano |

> **Doporučení:** Pro většinu organizací je **Claude for Teams / Enterprise** nejjednodušší cesta — jeden účet pro Claude Code i Claude na webu, centralizovaný billing, žádná infrastruktura navíc.

### Amazon Bedrock — setup

**Předpoklady:** AWS účet s Bedrock přístupem, modely povoleny, IAM oprávnění.

**1. Povolení modelu:** Navigujte do [Bedrock Console](https://console.aws.amazon.com/bedrock/) → Chat/Text playground → vyberte Anthropic model → vyplňte use case formulář (jednorázově).

**2. Autentizace** (vyberte jednu metodu):

```bash
# Varianta A: AWS CLI
aws configure

# Varianta B: Environment variables
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
export AWS_SESSION_TOKEN=your-session-token  # volitelné, pro dočasné credentials

# Varianta C: SSO profil
aws sso login --profile=my-profile
export AWS_PROFILE=my-profile

# Varianta D: AWS Management Console credentials
aws login

# Varianta E: Bedrock API keys (nejjednodušší)
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

**3. Aktivace:**

```bash
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1

# Volitelné: Override regionu pro malý/rychlý model (Haiku)
# export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2
```

**4. Pinning verzí modelů (kritické!):**

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

> **Varování:** Bez pinningu Claude Code použije výchozí modely — na Bedrock `global.anthropic.claude-sonnet-4-6` (primární) a `us.anthropic.claude-haiku-4-5-20251001-v1:0` (malý/rychlý). Prefix `global.` znamená globální routování, `us.` cross-region inference v US. Když Anthropic vydá nový model a změní výchozí aliasy, ale model ještě nemáte povolený, přestane to fungovat. Vždy pinujte!
>
> Pro jemnější kontrolu existuje i proměnná `ANTHROPIC_MODEL` (včetně podpory application inference profile ARN). Proměnná `ANTHROPIC_SMALL_FAST_MODEL` je **deprecated** — použijte místo ní `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Viz [Model configuration](https://code.claude.com/docs/en/model-config#pin-models-for-third-party-deployments).

**5. IAM politika:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowModelAndInferenceProfileAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:inference-profile/*",
        "arn:aws:bedrock:*:*:application-inference-profile/*",
        "arn:aws:bedrock:*:*:foundation-model/*"
      ]
    },
    {
      "Sid": "AllowMarketplaceSubscription",
      "Effect": "Allow",
      "Action": [
        "aws-marketplace:ViewSubscriptions",
        "aws-marketplace:Subscribe"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:CalledViaLast": "bedrock.amazonaws.com"
        }
      }
    }
  ]
}
```

> **Poznámka:** Druhý statement (`AllowMarketplaceSubscription`) je potřeba pro první aktivaci modelu přes Bedrock Console.

**Automatický refresh credentials:**

```json
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": { "AWS_PROFILE": "myprofile" }
}
```

Při expiraci credentials Claude Code automaticky spustí `awsAuthRefresh` a zopakuje request.

Alternativně, pokud nemůžete modifikovat `.aws` adresář a potřebujete vrátit credentials přímo, použijte `awsCredentialExport` — příkaz musí vypsat JSON ve formátu `{"Credentials": {"AccessKeyId": "...", "SecretAccessKey": "...", "SessionToken": "..."}}`.

**Bedrock Guardrails** (content filtering):

```json
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

### Google Vertex AI — setup

**Předpoklady:** GCP účet s billingem, Vertex AI API povoleno, přístup k Claude modelům schválen.

**1. Povolení API:**

```bash
gcloud config set project YOUR-PROJECT-ID
gcloud services enable aiplatform.googleapis.com
```

**2. Žádost o přístup k modelům:** [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) → vyhledejte „Claude" → požádejte o přístup (schválení může trvat 24–48 hodin).

**3. Aktivace:**

```bash
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID
```

**4. Pinning verzí:**

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

**5. IAM:** Role `roles/aiplatform.user` obsahuje potřebná oprávnění.

**6. Regionální přepsání pro specifické modely** (pokud `CLOUD_ML_REGION=global`, ale některé modely globální endpoint nepodporují):

```bash
# Příklad — nastavte regiony pro modely, které nepodporují globální endpoint:
export VERTEX_REGION_CLAUDE_3_5_HAIKU=us-east5
export VERTEX_REGION_CLAUDE_3_5_SONNET=us-east5
export VERTEX_REGION_CLAUDE_3_7_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_0_OPUS=europe-west1
export VERTEX_REGION_CLAUDE_4_0_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_1_OPUS=europe-west1
```

Ověřte podporu globálního endpointu pro konkrétní model v [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) → „Supported features".

> **Tip:** Vertex AI podporuje 1M token context window pro Sonnet 4 a Sonnet 4.6 (beta). Vyžaduje beta header `context-1m-2025-08-07`.

### Microsoft Foundry — setup

**Předpoklady:** Azure subscription s přístupem k Foundry, RBAC oprávnění.

**1. Vytvoření resource:** [Microsoft Foundry portal](https://ai.azure.com/) → nový resource → deployments pro Claude modely.

**2. Autentizace:**

```bash
# Varianta A: API klíč
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key

# Varianta B: Microsoft Entra ID (Azure SDK default credential chain)
# Bez API klíče Claude Code automaticky použije default credential chain:
# az login (lokální vývoj), managed identity (Azure VM/AKS), workload identity atd.
az login
```

**3. Aktivace:**

```bash
export CLAUDE_CODE_USE_FOUNDRY=1
export ANTHROPIC_FOUNDRY_RESOURCE=your-resource-name
# Nebo plná URL:
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com/anthropic
```

**4. Pinning verzí:**

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
```

**5. RBAC:** Role `Azure AI User` nebo `Cognitive Services User` postačují.

### LLM Gateway — centrální proxy

Pro pokročilou správu (centralizovaná autentizace, usage tracking, rate limiting, audit logging) můžete nasadit LLM Gateway mezi Claude Code a providera.

**LiteLLM** je populární open-source řešení:

```bash
# Unified endpoint (doporučeno):
export ANTHROPIC_BASE_URL=https://litellm-server:4000

# Bedrock přes LiteLLM:
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1

# Vertex AI přes LiteLLM:
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLOUD_ML_REGION=us-east5
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1

# Foundry přes gateway (viz third-party-integrations docs):
export ANTHROPIC_FOUNDRY_BASE_URL=https://your-llm-gateway.com
export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # pokud gateway řeší Azure auth
export CLAUDE_CODE_USE_FOUNDRY=1
```

> **Poznámka:** LiteLLM je third-party projekt, který Anthropic nespravuje ani neaudituje. Používejte na vlastní odpovědnost.
>
> **Tip pro LLM Gateway s Bedrock/Vertex za Anthropic Messages formátem:** Pokud váš gateway překládá Anthropic Messages API na Bedrock/Vertex interně, nastavte `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` — jinak mohou některé experimentální features způsobovat chyby.

**Autentizace vůči gateway:**

```bash
# Statický klíč:
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

# Dynamický klíč přes helper skript:
# V settings.json:
{ "apiKeyHelper": "~/bin/get-litellm-key.sh" }

# Refresh interval (spouští se periodicky a také po HTTP 401):
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000  # příklad: 1 hodina
```

### Corporate proxy

Pokud organizace vyžaduje, aby veškerý provoz šel přes proxy:

```bash
export HTTPS_PROXY='https://proxy.example.com:8080'
```

Funguje se všemi providery (Bedrock, Vertex, Foundry, přímé API).

### Společná poznámka ke všem providerům

Při použití Bedrock, Vertex AI nebo Foundry:
- Příkazy `/login` a `/logout` jsou **deaktivovány** — autentizace probíhá přes cloud credentials.
- **Server-managed settings** (kapitola 5.4) **nejsou dostupné** — vyžadují přímé spojení s `api.anthropic.com`.
- **Prompt caching** nemusí být dostupný ve všech regionech. Pokud způsobuje problémy: `export DISABLE_PROMPT_CACHING=1`.
- Ověřte konfiguraci příkazem `/status`.

### Vyzkoušejte

1. Pokud máte přístup k AWS/GCP/Azure, zkuste nakonfigurovat jednoho providera podle návodu výše.
2. Ověřte funkčnost: `claude -p "Ahoj, přes jakého providera jsi připojený?"` + `/status`.
3. Nastavte pinning modelů a ověřte, že funguje po „upgrade" (změna aliasu).

**Zdroje:**
- [Enterprise Overview](https://code.claude.com/docs/en/third-party-integrations)
- [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock)
- [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai)
- [Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry)
- [LLM Gateway](https://code.claude.com/docs/en/llm-gateway)

---

## 5.3 Monitoring, analytics a řízení nákladů

**Doba studia:** 20 minut

### Proč monitorovat?

Když Claude Code používá jeden vývojář, stačí `/cost`. Když ho používá tým 50+ lidí, potřebujete:
- Kolik který vývojář/tým spotřebuje tokenů a peněz?
- Kolik PR a řádků kódu Claude Code pomohl vytvořit (ROI)?
- Kde jsou výkonnostní problémy?

Claude Code nabízí dva přístupy: **OpenTelemetry** (metriky a eventy pro váš observability stack) a **Analytics dashboard** (webové rozhraní na claude.ai nebo platform.claude.com).

### OpenTelemetry — metriky a eventy

**Quick start:**

```bash
# 1. Aktivace telemetrie
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. Exportéry (oba volitelné)
export OTEL_METRICS_EXPORTER=otlp          # otlp, prometheus, console
export OTEL_LOGS_EXPORTER=otlp             # otlp, console

# 3. OTLP endpoint
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. Autentizace (pokud vyžadována)
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. Spuštění
claude
```

**Dostupné metriky:**

| Metrika | Popis | Jednotka |
|---------|-------|----------|
| `claude_code.session.count` | Počet spuštěných sezení | počet |
| `claude_code.lines_of_code.count` | Změněné řádky kódu | počet |
| `claude_code.pull_request.count` | Vytvořené PR | počet |
| `claude_code.commit.count` | Vytvořené commity | počet |
| `claude_code.cost.usage` | Cena sezení | USD |
| `claude_code.token.usage` | Spotřebované tokeny | tokeny |
| `claude_code.code_edit_tool.decision` | Accept/reject editací | počet |
| `claude_code.active_time.total` | Aktivní čas | sekundy |

Metriky mají atributy `type` a `model` pro detailní segmentaci. Např. `token.usage` rozlišuje `input`, `output`, `cacheRead`, `cacheCreation`.

**Dostupné eventy** (vyžadují `OTEL_LOGS_EXPORTER`):

| Event | Kdy se loguje |
|-------|---------------|
| `claude_code.user_prompt` | Uživatel zadá prompt |
| `claude_code.tool_result` | Nástroj dokončí vykonání |
| `claude_code.api_request` | API request na Claude |
| `claude_code.api_error` | API request selže |
| `claude_code.tool_decision` | Accept/reject oprávnění |

Eventy jsou propojeny přes `prompt.id` (UUID) — můžete trasovat celý řetězec od promptu přes API cally po výsledky nástrojů.

**Bezpečnost a soukromí:**
- Telemetrie je **opt-in** — vyžaduje explicitní `CLAUDE_CODE_ENABLE_TELEMETRY=1`.
- Obsah promptů se **neloguje** (pouze délka). Pro logování obsahu: `OTEL_LOG_USER_PROMPTS=1`.
- Názvy MCP serverů/nástrojů se nelogují ve výchozím stavu. Pro zapnutí: `OTEL_LOG_TOOL_DETAILS=1`.
- Bash příkazy a file paths se zahrnují do `tool_parameters` — pokud příkazy mohou obsahovat secrets, nakonfigurujte redakci ve vašem backendu.

**Kardinalita metrik:**

| Proměnná | Výchozí | Popis |
|----------|---------|-------|
| `OTEL_METRICS_INCLUDE_SESSION_ID` | `true` | Session ID v metrikách |
| `OTEL_METRICS_INCLUDE_VERSION` | `false` | Verze Claude Code |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | `true` | UUID účtu |

Nižší kardinalita = lepší výkon backendu a nižší storage.

**Dynamické headers** (pro enterprise s rotací tokenů):

```json
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

Skript se spouští při startu a pak každých 29 minut (konfigurovatelné přes `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`).

**Multi-team atributy:**

```bash
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

> **Varování:** `OTEL_RESOURCE_ATTRIBUTES` používá formát `key=value` oddělené čárkami. Hodnoty **nesmí obsahovat mezery** — použijte podtržítka nebo camelCase (např. `org.name=Johns_Organization`, ne `org.name=John's Organization`).

**Administrátorská konfigurace** — centrální nastavení pro celou organizaci přes managed settings:

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.example.com:4317"
  }
}
```

### Analytics dashboard

**Claude for Teams / Enterprise:** [claude.ai/analytics/claude-code](https://claude.ai/analytics/claude-code) (Admin/Owner role)

Obsahuje:
- **Usage metrics:** přijaté řádky kódu, accept rate, denní aktivní uživatelé
- **Contribution metrics:** PR a řádky vytvořené s pomocí Claude Code (vyžaduje GitHub integraci)
- **Leaderboard:** top 10 přispěvatelů
- **CSV export:** kompletní data pro custom reporting

**API (Console):** [platform.claude.com/claude-code](https://platform.claude.com/claude-code) (UsageView oprávnění)

Obsahuje: přijaté řádky, accept rate, aktivita, spend, per-user insights.

### PR attribution — jak funguje

Když aktivujete contribution metrics (vyžaduje [GitHub app](https://github.com/apps/claude)):

1. Při merge PR se extrahují přidané řádky z diffu
2. Claude Code session aktivity se porovnají se soubory v PR
3. Řádky se matchují proti výstupu Claude Code (konzervativní matching)
4. PR obsahující Claude Code řádky dostane label `claude-code-assisted`

**Časové okno:** 21 dní před až 2 dny po merge. Kód přepsaný vývojářem o více než 20 % se nepřipisuje Claude Code.

**Vyloučené soubory:** lock files, generovaný kód, build artefakty, minifikované soubory, řádky přes 1000 znaků.

> **Poznámka:** Contribution metrics vyžadují Claude for Teams/Enterprise. Nejsou dostupné pro organizace se Zero Data Retention.

### Řízení nákladů

**Průměrné náklady:** ~$6/vývojář/den, u 90 % uživatelů pod $12/den. ~$100–200/vývojář/měsíc se Sonnet 4.6.

**Workspace spend limits:** V [Console](https://platform.claude.com/) nastavte limit na workspace „Claude Code" (automaticky vytvořený při prvním přihlášení).

**Rate limit doporučení (TPM per user):**

| Velikost týmu | TPM / uživatel | RPM / uživatel |
|--------------|---------------|----------------|
| 1–5 | 200k–300k | 5–7 |
| 5–20 | 100k–150k | 2.5–3.5 |
| 20–50 | 50k–75k | 1.25–1.75 |
| 50–100 | 25k–35k | 0.62–0.87 |
| 100–500 | 15k–20k | 0.37–0.47 |
| 500+ | 10k–15k | 0.25–0.35 |

TPM per user klesá s velikostí týmu, protože větší organizace mají nižší concurrent usage. Rate limity platí na úrovni organizace, ne per user — jednotlivci mohou dočasně spotřebovat více.

**Na Bedrock/Vertex/Foundry:** Claude Code neposílá metriky z vašeho cloudu. Pro sledování nákladů použijte nativní nástroje (AWS Cost Explorer, GCP Billing, Azure Cost Management) nebo LiteLLM pro [tracking spendu per key](https://docs.litellm.ai/docs/proxy/virtual_keys#tracking-spend).

### Vyzkoušejte

1. Nastavte console exporter pro debugging: `CLAUDE_CODE_ENABLE_TELEMETRY=1 OTEL_METRICS_EXPORTER=console OTEL_METRIC_EXPORT_INTERVAL=5000 claude`
2. Sledujte metriky, které se vypisují do konzole při práci s Claude Code.
3. Pokud máte Teams/Enterprise plán, otevřete analytics dashboard na claude.ai.
4. Projděte [Claude Code ROI Measurement Guide](https://github.com/anthropics/claude-code-monitoring-guide) pro ready-to-use Docker Compose + Prometheus setup.

**Zdroje:**
- [Monitoring](https://code.claude.com/docs/en/monitoring-usage)
- [Analytics](https://code.claude.com/docs/en/analytics)
- [Costs](https://code.claude.com/docs/en/costs)
- [ROI Measurement Guide](https://github.com/anthropics/claude-code-monitoring-guide)

---

## 5.4 Server-managed settings a organizační politiky

**Doba studia:** 15 minut

### Problém: jak řídit Claude Code pro 100+ vývojářů?

Bez centrální správy každý vývojář nastavuje Claude Code po svém. Chcete zakázat `curl` v Bash? Vynutit telemetrii? Blokovat přístup k `.env` souborům? Musíte to řešit na každém stroji zvlášť — nebo použít **server-managed settings**.

### Dva přístupy k centrální konfiguraci

| Přístup | Ideální pro | Bezpečnostní model |
|---------|-------------|-------------------|
| **Server-managed settings** | Organizace bez MDM, nespravovaná zařízení | Nastavení doručeno z Anthropic serverů při autentizaci |
| **Endpoint-managed settings** | Organizace s MDM/endpoint management | Nastavení nasazeno na zařízení přes MDM, registry, managed files |

> **Kdy co:** Máte-li MDM (Intune, Jamf, Ansible), použijte endpoint-managed settings — silnější bezpečnostní garance, protože nastavení je chráněno na úrovni OS. Nemáte-li MDM, server-managed settings jsou jednodušší cesta.

### Server-managed settings (public beta)

**Požadavky:**
- Claude for Teams nebo Enterprise plán
- Claude Code verze 2.1.38+ (Teams) nebo 2.1.30+ (Enterprise)
- Síťový přístup k `api.anthropic.com`

**Konfigurace:**

1. V [claude.ai](https://claude.ai) → **Admin Settings** → **Claude Code** → **Managed settings**
2. Zadejte JSON konfiguraci:

```json
{
  "permissions": {
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "disableBypassPermissionsMode": "disable"
}
```

3. Uložte. Claude Code klienti obdrží nastavení při příštím startu nebo během hodinového polling cyklu.

**Podporované nastavení:** Vše z `settings.json` + managed-only nastavení jako `disableBypassPermissionsMode`.

**Kdo může spravovat:** Primary Owner a Owner.

### Doručování nastavení

- **První spuštění bez cache:** Nastavení se stáhne asynchronně. Existuje krátké okno před načtením, kdy omezení nejsou vynucena.
- **Následná spuštění:** Cached nastavení se aplikují okamžitě. Na pozadí se stahuje aktualizace.
- **Výpadek sítě:** Cached nastavení přetrvávají.
- **Aktualizace bez restartu:** Většina nastavení se aplikuje automaticky. Výjimka: OpenTelemetry vyžaduje plný restart.

### Security approval dialogy

Některá nastavení vyžadují explicitní souhlas uživatele:
- **Shell command settings** (spouštění příkazů)
- **Custom environment variables** (mimo known safe allowlist)
- **Hook konfigurace**

Uživatel vidí dialog s vysvětlením. Pokud odmítne, Claude Code se ukončí.

> **Headless mode:** V `-p` režimu se security dialogy přeskakují a nastavení se aplikují bez souhlasu.

### Aktuální omezení (beta)

- Nastavení se aplikují **uniformně na všechny uživatele** — per-group konfigurace zatím není podporována.
- **MCP server konfigurace** nelze distribuovat přes server-managed settings.

### Platformová dostupnost

Server-managed settings **nejsou dostupné** při použití third-party providerů:
- Amazon Bedrock, Google Vertex AI, Microsoft Foundry
- Custom API endpoints přes `ANTHROPIC_BASE_URL` nebo LLM gateway

### Bezpečnostní aspekty

Server-managed settings fungují jako **client-side kontrola**. Na nespravovaných zařízeních uživatel s admin/sudo přístupem může modifikovat Claude Code binary, filesystem nebo síťovou konfiguraci.

| Scénář | Chování |
|--------|---------|
| Uživatel edituje cached soubor | Poškozený soubor platí do příštího server fetch, kdy se obnoví |
| Uživatel smaže cached soubor | First-launch chování — krátké okno bez omezení |
| API nedostupné | Cached nastavení platí, pokud existují |
| Jiná organizace | Nastavení se nedoručí pro účty mimo managed organizaci |
| Vlastní `ANTHROPIC_BASE_URL` | Server-managed settings jsou obejity |

Pro detekci runtime změn konfigurace použijte [`ConfigChange` hook](https://code.claude.com/docs/en/hooks#configchange).

### Endpoint-managed settings — alternativa s MDM

Pro silnější vynucení na spravovaných zařízeních:

- **macOS:** Managed preferences přes MDM profily
- **Windows:** Registry policies přes Group Policy
- **Linux:** Managed settings file přes Ansible/Chef/Puppet

Endpoint-managed settings mají stejnou prioritu jako server-managed. Když jsou přítomna obě, **server-managed mají přednost** a endpoint-managed se nepoužijí.

### Best practices pro organizace

1. **Investujte do CLAUDE.md** — commitujte do repozitářů. Celý tým bude mít konzistentní instrukce.
2. **Zjednodušte instalaci** — vytvořte „one-click" způsob instalace Claude Code pro maximální adopci.
3. **Začněte s guided usage** — nové uživatele nechte začít s Q&A a malými bug fixy, než přejdou na plně agentní práci.
4. **Pinujte verze modelů** — vždy při Bedrock/Vertex/Foundry nasazení (viz kapitola 5.2).
5. **Využijte MCP pro integrace** — centrální tým nakonfiguruje MCP servery a commitne `.mcp.json`, aby z toho těžili všichni.
6. **Audit logging** — audit log events pro změny nastavení jsou dostupné přes compliance API. Kontaktujte Anthropic pro přístup.

### Vyzkoušejte

1. Pokud máte Teams/Enterprise plán, otevřete Admin Settings → Claude Code → Managed settings.
2. Zkuste přidat deny pravidlo (např. blokování `Bash(rm -rf *)`).
3. Ověřte, že se pravidlo projevilo: restartujte Claude Code a zkuste `/permissions`.
4. Pro endpoint-managed settings vytvořte soubor na správném místě pro váš OS a ověřte, že Claude Code ho načítá.

**Zdroje:**
- [Server-Managed Settings](https://code.claude.com/docs/en/server-managed-settings)
- [Settings](https://code.claude.com/docs/en/settings)
- [Security](https://code.claude.com/docs/en/security)
- [Authentication](https://code.claude.com/docs/en/authentication)

---

## Milník Úrovně 5

- [ ] Umím vytvořit AI agenta pomocí Agent SDK (Python nebo TypeScript)
- [ ] Rozumím rozdílu mezi Client SDK a Agent SDK
- [ ] Znám možnosti enterprise nasazení (Bedrock, Vertex AI, Foundry) a vím, kdy co použít
- [ ] Umím nastavit pinning verzí modelů pro cloud providery
- [ ] Rozumím OpenTelemetry monitoringu a umím ho nakonfigurovat
- [ ] Znám analytics dashboard a PR attribution
- [ ] Umím nastavit server-managed settings pro centrální řízení organizace
- [ ] Vím, jaká omezení mají server-managed settings (uniformní pro všechny, bez MCP, ne pro third-party providery)

---

## Závěr celého průvodce

Gratulujeme! Prošli jste kompletním průvodcem Claude Code od úplného začátku až po expert úroveň:

1. **Začátečník** — instalace, první sezení, základní příkazy
2. **Produktivní uživatel** — CLAUDE.md, Plan Mode, prompt engineering, testy, modely
3. **Středně pokročilý** — oprávnění, MCP, skills, subagenti, hooks, plugins
4. **Pokročilý** — headless mode, CI/CD, hooks deep dive, MCP advanced, Agent Teams, sandboxing
5. **Expert** — Agent SDK, enterprise nasazení, monitoring, organizační politiky

Klíčové principy, které platí na každé úrovni:
- **Git je váš záchranný pás** — vždy commitujte před experimentováním
- **Specifičnost a kontext** — čím konkrétnější prompt, tím lepší výsledek
- **Verifikace** — vždy nechte Claude ověřit svou práci (testy, build, lint)
- **Nový úkol = nové sezení** — `/clear` je váš nejlepší přítel

Sledujte [Changelog](https://code.claude.com/docs/en/changelog) — Claude Code se vyvíjí velmi rychle a nové funkce přibývají téměř každý týden.
