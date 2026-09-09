# FÁZE 4b — Verifikace faktů a hledání mezer (Claude Code / Claude API)

> Datum ověření všech faktů: **2026-08-26**. Zdroje: web (`WebSearch`/`WebFetch` na docs.claude.com → přesměrováno na `platform.claude.com` a `code.claude.com`) + skill `claude-api`.
> Zapisováno výhradně do `C:\tmp\workshop-namety\`, nic v žádném repozitáři nebylo měněno.

---

## Sekce A — Ověřená fakta pro výklad tří mechanik LLM

### A1. Velikost kontextového okna

| Tvrzení | Hodnota | Zdroj (URL) | Datum ověření | Jistota |
|---|---|---|---|---|
| Claude Opus 5 — kontextové okno | 1 000 000 tokenů, **výchozí** (žádný beta flag) | [platform.claude.com/docs/en/models/overview](https://platform.claude.com/docs/en/models/overview) | 2026-08-26 | dokumentované |
| Claude Sonnet 5 — kontextové okno | 1 000 000 tokenů, výchozí | [platform.claude.com/docs/en/models/overview](https://platform.claude.com/docs/en/models/overview) | 2026-08-26 | dokumentované |
| Claude Haiku 4.5 — kontextové okno | 200 000 tokenů | [platform.claude.com/docs/en/models/overview](https://platform.claude.com/docs/en/models/overview) | 2026-08-26 | dokumentované |
| Existuje samostatná "1M beta" varianta vyžadující flag/vyšší cenu? | **Ne** u aktuální generace (Opus 5, Sonnet 5, Opus 4.6+, Mythos Preview) — 1M je defaultní kontext bez beta hlavičky. (Starší generace, např. Claude Sonnet 4, měla 1M za beta flagem — to už neplatí.) | [platform.claude.com/.../context-windows](https://platform.claude.com/docs/en/build-with-claude/context-windows) | 2026-08-26 | dokumentované |
| Cena za dlouhý kontext (>200k tokenů) | **Standardní sazba přes celé okno** — "900k-token request je účtován stejnou sazbou za token jako 9k-token request" (žádný cenový skok) | [platform.claude.com/.../pricing#long-context-pricing](https://platform.claude.com/docs/en/about-claude/pricing) | 2026-08-26 | dokumentované |
| Output tokeny — limit zvlášť od kontextu? | Ano. `max_tokens` je samostatný strop: 128K u Opus 5 / Sonnet 5, 64K u Haiku 4.5 (Message API). Na Batch API lze přes beta header `output-300k-2026-03-24` až 300K output tokenů. | [platform.claude.com/.../models/overview](https://platform.claude.com/docs/en/models/overview) | 2026-08-26 | dokumentované |

**Poznámka pro výklad:** starší mentální model "1M kontext = drahá beta funkce" už u aktuální generace neplatí — je to výchozí chování. To je důležitý bod proti zafixované představě analytiků z dřívějška.

### A2. Prompt caching

| Tvrzení | Hodnota | Zdroj (URL) | Datum ověření | Jistota |
|---|---|---|---|---|
| TTL varianty | 5 minut (default) a 1 hodina (explicitní `ttl: "1h"`) | [platform.claude.com/.../prompt-caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | 2026-08-26 | dokumentované |
| Cena zápisu do cache (5 min) | **1,25×** základní ceny vstupních tokenů | [platform.claude.com/.../pricing#prompt-caching](https://platform.claude.com/docs/en/about-claude/pricing) | 2026-08-26 | dokumentované |
| Cena zápisu do cache (1 h) | **2×** základní ceny vstupních tokenů | tamtéž | 2026-08-26 | dokumentované |
| Cena čtení z cache (hit) | **0,1×** základní ceny (tj. 90% úspora) | tamtéž | 2026-08-26 | dokumentované |
| Kdy se caching "vyplatí" | 5min cache: od 1. čtení; 1h cache: od 2. čtení (dle poměru zápis/čtení) | tamtéž (odvozeno z multiplikátorů) | 2026-08-26 | dokumentované |
| Konkrétní čísla Opus 5 | vstup $5/MTok → 5m zápis $6,25 → 1h zápis $10 → cache read $0,50 → výstup $25/MTok | tamtéž | 2026-08-26 | dokumentované |
| Co cache invaliduje | **Prefix match** — jakákoli změna bytu v prefixu zneplatní vše za ním. Hierarchie `tools → system → messages`: změna tool definic zneplatní vše; změna `tool_choice` zneplatní system+messages; přidání/odebrání obrázků zneplatní messages; časová razítka/nedeterministický JSON v system promptu tiše ruší cache | [platform.claude.com/.../prompt-caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) | 2026-08-26 | dokumentované |
| Minimální cachovatelný prefix | ~1024 tokenů (kratší se tiše necachuje) | skill `claude-api` (shared/prompt-caching.md reference) | 2026-08-26 | dokumentované |

### A3. Počítání tokenů

| Tvrzení | Hodnota | Zdroj (URL) | Datum ověření | Jistota |
|---|---|---|---|---|
| Tokenizér | Vlastní (proprietární) tokenizér Anthropic; přesný algoritmus/slovník **není veřejně publikován** jako specifikace. Dokumentace jen říká, že modely od Opus 4.7 dál (a Mythos Preview) používají "novější tokenizér" produkující cca o 30 % více tokenů na stejný text než starší generace | [platform.claude.com/.../pricing](https://platform.claude.com/docs/en/about-claude/pricing), [platform.claude.com/.../token-counting](https://platform.claude.com/docs/en/build-with-claude/token-counting) | 2026-08-26 | dokumentované (jen fakt o změně mezi generacemi, ne detail algoritmu) |
| Zda Sonnet 5 sdílí "nový" tokenizér s Opus 5 | **Nejasné/nepotvrzeno v dokumentaci** — dokumentace explicitně jmenuje jen "Claude 4.7 a novější modely + Mythos Preview" a odděleně Fable 5/Mythos 5; Sonnet 5 v tomto výčtu není jmenovitě potvrzen ani vyvrácen | tamtéž | 2026-08-26 | **nedostupné** — nedohledáno explicitně |
| Veřejné API na počítání tokenů | Ano — `POST /v1/messages/count_tokens` (`client.messages.count_tokens(...)`). Zdarma, limitováno RPM dle usage tier (Start 2000, Build 4000, Scale 8000 req/min). Vrací odhad (`input_tokens`), skutečná fakturace se může mírně lišit | [platform.claude.com/.../token-counting](https://platform.claude.com/docs/en/build-with-claude/token-counting) | 2026-08-26 | dokumentované |
| Poměr znaků/token pro angličtinu | **"1 token ≈ 4 znaky nebo 0,75 slova v angličtině. Přesný počet se liší podle jazyka a typu obsahu."** — doslovná citace z oficiálního FAQ | [platform.claude.com/.../pricing](https://platform.claude.com/docs/en/about-claude/pricing) (sekce FAQ, "How is token usage calculated?") | 2026-08-26 | dokumentované, doslovná citace |
| Poměr pro jiné jazyky (konkrétně jazyky s diakritikou, např. čeština) | **Anthropic nezveřejňuje konkrétní číslo.** Dokumentace pouze říká "přesný počet se liší podle jazyka" bez čísel per-jazyk. Žádná oficiální tabulka poměrů pro non-English jazyky nebyla nalezena | — (negativní nález, ověřeno na pricing i token-counting stránce) | 2026-08-26 | **explicitně nedostupné** |
| Obecný princip, proč diakritika/non-ASCII stojí víc tokenů | Nezávislý zdroj (obecná teorie BPE, ne specifika Claude): tokenizéry typu **byte-level BPE** kódují text jako UTF-8 bajty. ASCII znaky (anglická abeceda) = 1 bajt/znak; znaky s diakritikou (á, č, ř, š, ž…) jsou vícebajtové UTF-8 sekvence. Trénovací data BPE slovníků jsou dominantně anglická/latinková, takže časté anglické bajtové sekvence se sloučí do velkých, efektivních tokenů, zatímco vzácnější vícebajtové sekvence (diakritika, non-latinková písma) se slučují méně — tomu se v literatuře říká **"byte premium effect"**: text v jazycích mimo hlavní trénovací proud vyžaduje více tokenů na stejný "obsah". Toto je obecně zdokumentovaný jev BPE tokenizace, **není to tvrzení specifické pro Claude** | nezávislé zdroje nalezené webem: [arxiv.org/abs/2505.24689 "BPE Stays on SCRIPT"](https://arxiv.org/html/2505.24689v1) a obecné vysvětlující články o byte-level BPE (Sebastian Raschka aj., viz WebSearch výsledky) | 2026-08-26 | **odvozené** — obecný princip, ne dokumentovaný fakt o Claude konkrétně |

**Důležité pro výklad:** rozliš explicitně před publikem: "toto Anthropic píše černé na bílém" (4 znaky/token pro AJ) vs. "toto je obecně platný technický princip, který vysvětluje proč čeština/diakritika stojí víc, ale Anthropic pro češtinu číslo nepublikuje."

### A4. Cena (orientační, pro workshop)

| Model | Vstup (MTok) | Výstup (MTok) | Zdroj | Datum | Jistota |
|---|---|---|---|---|---|
| Claude Opus 5 | $5 | $25 | [platform.claude.com/.../pricing](https://platform.claude.com/docs/en/about-claude/pricing) | 2026-08-26 | dokumentované |
| Claude Sonnet 5 | $2 | $10 | tamtéž (pozn.: šlo o "úvodní cenu" do 31. 8. 2026, dokumentace nyní potvrzuje, že se stala trvalou — plánované zdražení na $3/$15 od 1. 9. 2026 **nenastane**) | 2026-08-26 | dokumentované |
| Claude Haiku 4.5 (pro srovnání) | $1 | $5 | tamtéž | 2026-08-26 | dokumentované |
| Batch API sleva | 50 % z výše uvedených cen (Opus 5: $2,50/$12,50; Sonnet 5: $1/$5) | tamtéž | 2026-08-26 | dokumentované |

---

## Sekce A-doplnění — 11 bodů z paralelní fáze 4a (kolo 2 ověřování)

> Doplněno na výslovnou žádost koordinátora poté, co paralelní agent (fáze 4a) napsal výklad a označil body, které si netroufl domyslet. Řazeno dle zadané priority. Zdroje: `code.claude.com/docs/en` (Claude Code dokumentace — jiná doména než Claude API dokumentace v sekci A výše).

### Blokující body

**1. `/compact` — jak vybírá, co zachová; lze to ovlivnit argumentem?**

**Ano, existuje dokumentovaný syntax `/compact <instrukce>`.** Přesná citace: *"run `/compact` with instructions, like `/compact focus on the auth bug fix`, before starting a long new task. The summary keeps what you choose instead of what the automatic pass guesses is important."* Mechanika: Claude Code pošle samostatný požadavek se stejným systémovým promptem, nástroji a historií jako tvá konverzace, plus **sumarizační instrukci připojenou jako poslední user zpráva** — pokud jí sám dodáš vlastní text, nahradí (resp. doplní) tu výchozí. Přesné znění výchozího sumarizačního promptu Anthropic nezveřejňuje (je to interní, ne API-level dokumentované), ale dokumentace přesně říká, **co shrnutí obsahuje**: záměr a požadavky uživatele, klíčové technické koncepty, soubory (s důležitými úryvky kódu), chyby a jejich opravy, nedokončené úkoly, aktuální stav práce. Zdroj: [code.claude.com/docs/en/context-window](https://code.claude.com/docs/en/context-window) (sekce "When your context fills up") a [code.claude.com/docs/en/prompt-caching](https://code.claude.com/docs/en/prompt-caching) (sekce "Compacting the conversation"). Ověřeno 2026-08-26. **Jistota: dokumentované, doslovná citace syntaxe.**

→ **Důsledek pro výklad:** doporučení pro publikum by mělo znít "řekni `/compact`u, co má zachovat" (`/compact focus on X`), ne jen "vyhýbej se kompaktaci".

**2. Práh auto-kompaktace — při jakém % se spouští, lze vypnout/posunout?**

Není to univerzální jedno číslo — závisí na modelu a konfiguraci:
- **Výchozí chování (bez nastavení):** Claude Code kompaktuje, když konverzace dosáhne limitu kontextového okna modelu — s výjimkami níže.
- **Sonnet 5 konkrétně:** auto-kompaktace **cca při 967 000 tokenech** (výchozí), nastavitelné přes `CLAUDE_CODE_AUTO_COMPACT_WINDOW`.
- **Sonnet 4.6 / Opus 4.6 bez extended context:** kompaktace na hranici 200K.
- **`CLAUDE_CODE_DISABLE_1M_CONTEXT=1`:** modely s nativním 1M oknem (Sonnet 5, Fable 5) kompaktují na hranici 200K.
- **Lze změnit třemi způsoby:** (a) `/autocompact <hodnota>` (např. `/autocompact 500k`) — uloží se do uživatelských nastavení (`autoCompactWindow`); `/autocompact auto` vrátí výchozí; (b) `--autocompact` flag při spuštění (pro jeden běh); (c) env proměnná `CLAUDE_CODE_AUTO_COMPACT_WINDOW` (má nejvyšší prioritu, přebíjí vše ostatní). Rozsah: 100K–1M tokenů, formáty `200000` / `500k` / `1M` / bare `200`→200 000.
- Zdroj: [code.claude.com/docs/en/model-config](https://code.claude.com/docs/en/model-config) (sekce "Extended context", "Sonnet 5 context window", "Default auto-compact thresholds", "Set the auto-compact window"). Ověřeno 2026-08-26. **Jistota: dokumentované.**

**3. Počítání tokenů bez API klíče — existuje veřejně použitelný tokenizér?**

**Anthropic nezveřejňuje samostatný veřejný "widget" ani offline vocab soubor pro počítání tokenů Claude.** Jediná oficiálně dokumentovaná cesta je API endpoint `POST /v1/messages/count_tokens` (`client.messages.count_tokens(...)`), který **vyžaduje autentizaci** (API klíč nebo `ant auth login` profil) — viz sekce A3 výše. Nenalezen žádný hostovaný nástroj v Claude Console ani stažitelný tokenizér soubor v oficiální dokumentaci Claude Code/API, který by fungoval bez přihlášení. **Toto je negativní nález** — pokud stroj nemá API klíč ani `ant` CLI, oficiální cesta k přesnému počtu tokenů skutečně chybí.

**Kontrola místní prezentace `C:\Git\shared\docs\claude-code\claude-code-jak-funguje.html`:** Prošel jsem JS zdrojový kód (řádky 595–619 souboru). Tokenizace tam **není počítána algoritmem** — je to **napevno zakódované pole ukázkových tokenů** (`TOK_EN`, `TOK_CZ`), rozdělené ručně předem (např. `["The", " agent", " runs", ...]` pro AJ a `["Agent", " ob", "íh", "á", " smy", "čku", ...]` pro ČJ). Poměr "znaků/token" v UI (`tokRatio`) se dopočítává jen jako `text.length / arr.length` nad touto pevnou ukázkou — **není to tokenizér, natož tokenizér Claude**; je to ilustrace s předpřipravenými čísly. To je potřeba na workshopu přiznat: "toto je ilustrace, ne živý tokenizér."

Zdroj: přímé čtení `C:\Git\shared\docs\claude-code\claude-code-jak-funguje.html` (2026-08-26) + [code.claude.com/docs/en/build-with-claude/token-counting](https://platform.claude.com/docs/en/build-with-claude/token-counting) (negativní nález o veřejném tokenizéru). **Jistota: dokumentované (že API vyžaduje auth) + přímo ověřený zdrojový kód prezentace.**

### Doplňující body

**4. Poměr znaků na token pro angličtinu — 3,5 nebo 4?**

**Prezentace se mýlí — správná zdokumentovaná hodnota je 4 znaky/token, ne 3,5.** Doslovná citace z oficiálního FAQ (viz sekce A3 výše): *"As a rough estimate, 1 token is approximately 4 characters or 0.75 words in English."* Zdroj: [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing), sekce FAQ. Ověřeno 2026-08-26. Prezentace navíc tvrdí, že jde o "dokumentaci Anthropic" — což je napůl pravda: číslo 4 je dokumentované, ale prezentace uvádí jiné číslo (3,5) a needuje na konkrétní URL. **Doporučená oprava v prezentaci:** `claude-code-jak-funguje.html` řádek 311 — nahradit "≈ 3,5 znaku na token" za "≈ 4 znaky na token" a link/pojmenování zdroje zpřesnit na FAQ v `platform.claude.com/docs/en/about-claude/pricing`.

**5. Co `/resume` obnovuje a co ne**

Dokumentované do detailu (zdroj: [code.claude.com/docs/en/sessions](https://code.claude.com/docs/en/sessions), sekce "What a resumed session restores", ověřeno 2026-08-26):

| Obnovuje se | Neobnovuje se / obnovuje se podmíněně |
|---|---|
| Celá historie konverzace (včetně tool calls a výsledků) | `plan` a `bypassPermissions` permission mode — nikdy se needuje |
| Model (pokud nebyl vyřazen a nebyl vynucen flagem) | `--mcp-config`, `--settings`, `--plugin-dir`, `--fallback-model`, `--add-dir` — nutno zadat znovu |
| Agent (`--agent`) se svým systémovým promptem, nástroji, modelem | `auto` permission mode — jen pokud účet stále splňuje podmínky |
| Permission mode (s výjimkami vlevo) | Adresáře přidané za běhu (`/add-dir`) |
| Aktivní `goal` (ale počítadlo tahů/časovač/token-baseline se resetuje) | — |
| Naplánované úlohy (`/loop`/scheduled tasks), pokud nevypršely (7 dní) | **Background Bash a monitor úlohy se NIKDY neobnoví** |
| Prompt cache | **Ne** — po delší pauze cache vypršela (TTL), první request po `/resume` ji znovu staví od nuly (nejdražší request v dlouhé session) |
| Pracovní adresář | Implicitně dle toho, odkud/jak resumuješ — session je vázaná na projektový adresář |

Speciální případ: na Pro/Max plánu při obnovení session neaktivní > ~1 hodinu a > 100 000 tokenů nabídne Claude Code dialog **"Resume from summary"** (spustí `/compact` ihned) vs. **"Resume full session as-is"** (plná historie, ale draze přebuduje cache). **Jistota: dokumentované, detailní.**

**6. Resetuje `/clear` prompt cache i na serveru, nebo jen lokální kontext?**

**Ani jedno doslovně — `/clear` nic "neresetuje" na serveru, prostě přestane odkazovat na starou historii.** Přesný mechanismus: `/clear` nastartuje **novou, prázdnou konverzaci** (jen systémový prompt + projektový kontext, bez historie zpráv). Protože prompt caching funguje na **prefix match** (viz sekce A2 výše), nová, kratší konverzace přirozeně nesdílí prefix se starou dlouhou historií, takže na starou cache "nesahá" — ale **žádné volání na smazání cache se neděje**. Stará cache prostě vyprší přirozeně po TTL (5 min / 1 h), jako by session pokračovala dál. Klíčový rozdíl oproti `/compact`: `/clear` **neposílá žádný request** (na rozdíl od `/compact`, který posílá sumarizační request čtoucí celou historii) — proto je `/clear` **zdarma** ("When you want a fresh start instead of continuity, `/clear` costs nothing"). Zdroj: [code.claude.com/docs/en/prompt-caching](https://code.claude.com/docs/en/prompt-caching) + [code.claude.com/docs/en/sessions](https://code.claude.com/docs/en/sessions), sekce "Manage context within a session". Ověřeno 2026-08-26. **Jistota: dokumentované (odvozený mechanismus z popsaného chování, ne explicitně větou "toto dělá/nedělá s cache").**

**7. Velikost systémového promptu Claude Code v tokenech**

Přesné číslo **není oficiálně publikováno jako garantovaná hodnota**, ale dokumentace poskytuje **ilustrativní** číslo v interaktivní simulaci "Explore the context window": **systémový prompt ≈ 4 200 tokenů**, explicitně označené jako *"Token counts are illustrative. Actual values vary with your CLAUDE.md size, MCP servers, and file lengths."* Pro srovnání ze stejné simulace: auto memory ≈ 680, environment info ≈ 280, MCP tool names (deferred) ≈ 120, skill descriptions ≈ 450, `~/.claude/CLAUDE.md` ≈ 320, projektové `CLAUDE.md` ≈ 1 800 (vše ilustrativní příklady, ne měřené konstanty). Zdroj: [code.claude.com/docs/en/context-window](https://code.claude.com/docs/en/context-window). Ověřeno 2026-08-26. **Jistota: odvozené/ilustrativní — ne garantovaná dokumentovaná konstanta.** Přesné skutečné číslo pro danou verzi zjistíš jen příkazem `/context` v živé session.

**8. Metadata skillů — v každém requestu, nebo v cachovaném prefixu?**

**Obojí zároveň — a to je přesně ten rozdíl, na který se ptáš.** Popisky (name + description) všech dostupných skillů (kromě těch s `disable-model-invocation: true`, které jsou zcela mimo kontext, dokud je nezavoláš) se načtou **na začátku session jako součást systémového promptu** ("Skill descriptions... one-line descriptions of available skills so Claude knows what it can invoke"). Protože jde o vrstvu systémového promptu, spadá do **cachovaného prefixu** — tedy při opakovaných requestech v téže konverzaci se čte za 10 % ceny (cache read), ne za plnou cenu pokaždé. **Ale pořád to zabírá místo v kontextovém okně** (ilustrativně ~450 tokenů) — cache snižuje cenu za token, ne počet tokenů v okně. Zvláštnost: po `/compact` se tento seznam **nenačte znovu automaticky** ("Unlike the rest of the startup content, this listing is not re-injected after `/compact`. Only skills you actually invoked get preserved") — tzn. po kompaktaci Claude dočasně "neví", jaké další skilly má k dispozici, dokud nezačne nová session/restart. Zdroj: [code.claude.com/docs/en/context-window](https://code.claude.com/docs/en/context-window) a [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) (sekce "Control who invokes a skill" — tabulka s "When loaded into context"). Ověřeno 2026-08-26. **Jistota: dokumentované.**

**9. Kontextové okno `opus[1m]` v Claude Code — skutečně 1M, nebo nižší strop?**

**Skutečně 1 000 000 vstupních tokenů**, ale s podmínkami podle tarifu:
- `opus[1m]` je platný alias/suffix v `/model` (potvrzeno: `/model opus[1m]`, i `claude-opus-4-8[1m]`).
- **Dostupnost podle plánu** (tabulka z dokumentace): Max/Team/Enterprise → Opus s 1M kontextem **je součástí předplatného automaticky** (bez nutnosti konfigurace); Pro → **vyžaduje usage credits**; API/pay-as-you-go → plný přístup bez omezení.
- **Žádný cenový příplatek za dlouhý kontext:** "The 1M context window uses standard model pricing with no premium for tokens beyond 200K."
- **Vypnutí:** `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` — odstraní 1M variantu z model pickeru a drží session na 200K stropu (auto-kompaktace na hranici 200K, nebo tvrdá chyba, pokud je auto-kompaktace vypnutá).
- Zdroj: [code.claude.com/docs/en/model-config](https://code.claude.com/docs/en/model-config), sekce "Extended context". Ověřeno 2026-08-26. **Jistota: dokumentované.**

**10. Hranice kompaktace v `.jsonl` transkriptu — existuje typ záznamu/flag?**

**Nedohledáno v dokumentaci — a dokumentace explicitně varuje, že by se na formát nemělo spoléhat:** *"The entry format is internal to Claude Code and changes between versions, so scripts that parse these files directly can break on any release. To build on session data, use `/export` or the [script interfaces] instead."* Dokumentovaná strukturovaná alternativa: `/export` (čitelný přepis), `claude -p --output-format json/stream-json` (strukturovaný JSON výstup jednoho běhu), pole `transcript_path`, které dostávají hooky a statusline skripty. Žádný z těchto zdrojů explicitně nepopisuje konkrétní typ/flag záznamu pro hranici kompaktace v syrovém `.jsonl`. Zdroj: [code.claude.com/docs/en/sessions](https://code.claude.com/docs/en/sessions), sekce "Where transcripts are stored" a "Access conversations from scripts". Ověřeno 2026-08-26. **Jistota: nedostupné v dokumentaci** (koordinátor si to ověřuje sám na vlastních souborech — to zůstává jediná spolehlivá cesta).

---

## Sekce B — Co nepoužívám (mechanismy Claude Code)

Porovnáno s `faze1-inventar.md` (mám: SessionStart + PreToolUse hooky z pluginů, 1 output style, MCP Notion, 5 review agentů + spec-factory agenti, 5 pluginů, worktree nastavení `bgIsolation: none`) a `faze1-statistiky.md` (top příkazy: `/model` 53×, `/compact` 51×, `/context` 37×, `/resume` 33×, žádné `/loop`, `/rewind`, `/clear`, `/insights` v top 15).

| Mechanismus | Co umí | Používám? | K čemu by mi to bylo | Přínos | Zdroj dokumentace |
|---|---|---|---|---|---|
| **Hook `PreCompact` / `PostCompact`** | Existují jako reálné eventy — `PreCompact`: "Before context compaction"; `PostCompact`: "After context compaction completes" (dle tabulky eventů). **Oficiální praktický příklad ale používá jiný mechanismus** — viz řádek níže | **Ne** — inventář nemá žádný, jen SessionStart/PreToolUse | Nejasné — dokumentace k `PreCompact`/`PostCompact` samotným je jen jednořádková, bez schématu/příkladu v `hooks-guide` | Nízký–střední (nejistota, viz oprava níže) | [code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide) (tabulka eventů) |
| **Hook `SessionStart` s matcherem `"compact"`** (oficiálně doporučený vzor pro "zachovat důležitý kontext přes kompaktaci") | Toto — ne `PreCompact`/`PostCompact` — je **dokumentovaný a s konkrétním příkladem** doporučený způsob, jak po kompaktaci "připomenout" Claudovi důležitý kontext. `SessionStart` hooky dostávají pole `source` s hodnotou `startup`, `resume`, `clear`, `compact` nebo `fork` — matcher `"compact"` odchytí přesně moment po kompaktaci. Doslovný dokumentovaný příklad (`.claude/settings.json`): `{"hooks":{"SessionStart":[{"matcher":"compact","hooks":[{"type":"command","command":"echo 'Reminder: use Bun, not npm...'"}]}]}}` — stdout příkazu se přidá do Claudova kontextu jako plain text | **Ne** — mám SessionStart hook (z pluginu `knowledge-loop`), ale ne s matcherem `compact` | Přímo řeší situaci "51× `/compact` za sledované období, co se ztratí" — po každé kompaktaci automaticky připomenout projektové konvence, aktuální sprint/úkol, poslední commity (`git log --oneline -5`) | **Vysoký** | [code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide), sekce "Re-inject context after compaction". Ověřeno 2026-08-26 |
| **Hook `Stop`** | Po dokončení odpovědi Claude | Ne | Logovat dokončení úkolu, spouštět follow-up (např. validátor po každé odpovědi) | Střední | tamtéž |
| **Hook `SubagentStop`** | Po dokončení subagenta | Ne (mám review agenty, ale bez hooku na jejich dokončení) | Agregace výsledků review agentů automaticky | Střední | tamtéž |
| **Hook `UserPromptSubmit`** | Před zpracováním promptu | Ne | Validace/expanze vstupu, vynucení konvencí (např. TC/FR checklist) | Nízký–střední | tamtéž |
| **Hook `PostToolUse`** | Po úspěšném volání nástroje | Ne | Automatický lint po Edit (FR/PLC validátor rovnou po zápisu, ne až na vyžádání) | Vysoký | tamtéž |
| **Hook `Notification`** | Při odeslání notifikace Claude Code | Ne | Vlastní alerty (např. při dlouhém běhu validace) | Nízký | tamtéž |
| **Output styles — rozšíření** | Vlastní role/tón/formát; `keep-coding-instructions` flag; pluginy je mohou distribuovat | Částečně — mám 1 vlastní ("Feynman CZ"), inventář neukazuje více | Specializované styly pro různé role (review vs. psaní FR vs. schůzky) | Nízký–střední | [code.claude.com/docs/en/output-styles](https://code.claude.com/docs/en/output-styles) |
| **MCP servery — best practice** | Nástrojové definice jsou defaultně "deferred" (načtou se, jen když se použijí), `/context` ukáže spotřebu, `/mcp` vypne nepoužívané servery | Částečně — Notion připojen (inventář 9), ale bez evidence použití `/context`/`/mcp` k auditu overhead | Ověřit, jestli Notion MCP nezabírá kontext zbytečně; CLI nástroj (`gh`, `aws`) je context-efektivnější než MCP tam, kde existuje | Střední | [code.claude.com/docs/en/mcp](https://code.claude.com/docs/en/mcp) |
| **Background tasks (`run_in_background`) + `Monitor` tool** | Bash na pozadí (Ctrl+B), sledování přes `BashOutput`/`/bashes`; `Monitor` streamuje řádky v reálném čase (efektivnější než polling) | **Ne** — v inventáři ani statistice žádná stopa | Dlouhé validátory (`validate.cmd`, `plc-lint.py` na velkých specech) na pozadí, zatímco pokračuji v konverzaci | Střední | [zdroj: search — code.claude.com/docs/en/interactive-mode + Monitor tool docs] |
| **Worktrees (`--worktree`, `isolation: worktree`)** | Izolovaná git worktree pro session nebo subagenta; auto-cleanup bez změn | Částečně — `worktree.bgIsolation: none` v settings, paměť má poznámku "Worktree handoff" (tedy použito aspoň jednou), ale ne systematicky | Bezpečné experimentování se specifikacemi bez rizika pro `dev/martint` větev | Střední | [code.claude.com/docs/en/worktrees](https://code.claude.com/docs/en/worktrees) |
| **`/loop` a scheduled tasks (Routines, Desktop scheduled tasks, GitHub Actions schedule)** | Opakované spouštění promptu na intervalu (session-scoped `/loop`, cloud Routines, lokální Desktop úlohy) | **Ne** — není v top 15 příkazů ani v inventáři | Pravidelná kontrola stavu dodavatelských dotazů (`docs/suppliers/`), pravidelný re-run validátorů | Vysoký (pro dodavatelský workflow) | [code.claude.com/docs/en/scheduled-tasks](https://code.claude.com/docs/en/scheduled-tasks) |
| **`claude plugin eval`** | CLI harness pro psaní eval případů + graderů, běh sad testů, JSON/HTML report, sandbox, CI, early-access | **Ne** — mám 3 pluginy (`knowledge-loop`, `ontology-registry`, `spec-factory`) bez evidence testování | Ověřit, že skilly/agenti pluginů skutečně spouští to, co mají (zvlášť po aktualizaci spec-factory 1.5→1.9) | Střední | (potvrzeno přes WebSearch, přímý docs URL nedohledán — nízká jistota existence konkrétní URL, ale příkaz samotný je zmíněn v oficiálním popisu agenta `claude-code-guide`) |
| **Artifacts (publikované HTML stránky)** | Sdílitelná privátní webová stránka z HTML, s tématizací, diagramy, případně runtime capabilities | **Ne** — inventář neukazuje použití; PLC simulace (`dopravnik-simulace.html`) je psaná jako lokální soubor, ne Artifact | Sdílet PLC simulace, review reporty nebo přehledy s kolegy jedním odkazem místo posílání souboru | Střední | (tento nástroj sám — dokumentace je nástrojový popis, ne samostatná web stránka) |
| **Subagenti — model/effort override, izolace** | `model: sonnet\|opus\|haiku\|fable\|inherit`, `permissionMode`, `isolation: worktree`, tool allow/denylist | Částečně — mám 5 review agentů + spec-factory agenty s definovanými nástroji, ale bez evidence explicitního `model:`/effort overridu (levnější model pro objemné čtení) | Levnější/rychlejší subagent (haiku) pro objemné, mechanické review kroky; dražší jen tam, kde je potřeba úsudek | Střední | [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents) |
| **`/rewind`** | Vrátí konverzaci i kód na předchozí checkpoint (dvojitý Esc) | Ne (chybí v top 15) | Rychlé zrušení špatného směru bez nutnosti `/clear` a ztráty kontextu | Střední | [code.claude.com/docs/en/costs](https://code.claude.com/docs/en/costs) (zmíněno v sekci "Work efficiently on complex tasks") |
| **`/clear`** | Vyčistí session, nulová cena (na rozdíl od `/compact`, který čte celou konverzaci) | Ne (chybí v top 15; `/compact` 51× budí podezření, že `/clear` chybí jako levnější alternativa při přepnutí na nesouvisející úkol) | Přepínání mezi nesouvisejícími úkoly bez zbytečné spotřeby (a bez rizika ztráty kontextu kompaktací) | Vysoký | tamtéž |
| **`/insights`** | Analyzuje posledních až 200 sessions na tomto stroji, HTML report s tím, na čem pracuji, kde vázne komunikace, doporučení | Ne | Sebereflexe vlastního způsobu práce s Claude Code — přímo použitelné jako podklad pro workshop (meta-demo) | Střední (vysoký pro workshop demo) | [code.claude.com/docs/en/costs](https://code.claude.com/docs/en/costs) (sekce "Analyze your usage patterns") |
| **Channels (event-driven vstup)** | MCP server jako kanál, který posílá zprávy do session (Telegram/Discord/webhook) místo pollingu | Ne | Náhrada pollingu (`/dodavatele:stav`) reaktivním kanálem, když dorazí e-mail od dodavatele | Nízký–střední (nejistá dostupnost/komplexita pro netechnického analytika) | zmíněno v [code.claude.com/docs/en/mcp](https://code.claude.com/docs/en/mcp) |

---

## Sekce C — Kandidáti na náměty do katalogu

Všechny položky níže jsou **netestováno — nemám s tím vlastní zkušenost.** Vybráno z mechanismů s vysokým/středním přínosem výše.

### C1. Hook, který po kompaktaci připomene důležitý kontext (`SessionStart` + matcher `"compact"`)
- **Okruh:** `N` nastavení
- **Laicky:** Skript, který se spustí hned **po** tom, co Claude Code shrne starší část rozhovoru (ať už ručně příkazem `/compact`, nebo automaticky, když se kontext moc naplní), a "připomene" Claudovi věci, které by shrnutí mohlo ošidit — např. aktuální úkol, projektové konvence, poslední commity.
- **Oprava vlastního prvního odhadu:** Původně jsem čekal, že správný háček je `PreCompact` (spouští se *před* kompaktací). Dokumentace ale `PreCompact`/`PostCompact` popisuje jen jednořádkově bez příkladu; **oficiálně doporučený a doloženým příkladem podpořený vzor je `SessionStart` hook s `matcher: "compact"`** — spustí se po kompaktaci, `source` pole rozlišuje `compact` od `startup`/`resume`/`clear`/`fork`.
- **Proč by to pomohlo analytikovi:** Kompaktace (`/compact`) je nejpoužívanější netriviální příkaz ve statistice (51× za sledované období) — jasný signál, že se s dlouhými konverzacemi pracuje běžně a riziko ztráty důležitého detailu je reálné.
- **Dá se předvést naživo:** Ano — nastavit přesně dokumentovaný příklad (`echo` s připomínkou konvencí nebo `git log --oneline -5`) a ukázat, že se objeví v kontextu hned po `/compact`.
- **Poznámka:** netestováno — nemám s tím vlastní zkušenost.

### C2. `/clear` místo `/compact` při přepnutí tématu
- **Okruh:** `N` nastavení / `K` kontext
- **Laicky:** Když skončím jedno téma a jdu na úplně jiné, `/clear` smaže kontext zadarmo a nemusím čekat na (placenou) kompaktaci, která se navíc snaží uchovat návaznost, kterou už nepotřebuju.
- **Proč by to pomohlo analytikovi:** Přímo z dokumentace: `/compact` čte celou dosavadní konverzaci (drahé), `/clear` je zdarma. Analytik, který přepíná mezi FR, ADR a schůzkami, pravděpodobně kompaktuje tam, kde by stačilo vyčistit.
- **Dá se předvést naživo:** Ano — jednoduché srovnání `/context` před a po `/compact` vs. po `/clear`.
- **Poznámka:** netestováno — nemám s tím vlastní zkušenost.

### C3. `/loop` pro opakované kontroly
- **Okruh:** `O` orchestrace
- **Laicky:** Řekne se Claudovi "kontroluj tohle každých N minut/hodin", a on to sám opakuje na pozadí session, dokud se nezastaví nebo neuplyne 7 dní.
- **Proč by to pomohlo analytikovi:** V projektu AlzaSk existuje opakovaná potřeba "co se změnilo u dodavatele" (`docs/suppliers/`, příkaz `/dodavatele:stav`) — dnes se to spouští ručně. `/loop` by to mohl dělat samo v pozadí session.
- **Dá se předvést naživo:** Ano — `/loop 5m` na jednoduchý dotaz a ukázat, jak se sám znovu spustí.
- **Poznámka:** netestováno — nemám s tím vlastní zkušenost.

### C4. Background bash + Monitor tool pro dlouhé validace
- **Okruh:** `O` orchestrace
- **Laicky:** Dlouhý běh (validátor, sestavení reportu) se spustí "na pozadí" a člověk může mezitím pokračovat v rozhovoru; `Monitor` navíc streamuje výstup průběžně místo dotazování dokola.
- **Proč by to pomohlo analytikovi:** Validátory (`validate.cmd`, `plc-lint.py`) na velkých specifikacích mohou trvat — dnes se na ně čeká. Přímý dopad na plynulost práce.
- **Dá se předvést naživo:** Ano — spustit validátor na pozadí a mezitím dělat něco jiného.
- **Poznámka:** netestováno — nemám s tím vlastní zkušenost.

### C5. Worktrees pro bezpečné experimentování
- **Okruh:** `O` orchestrace
- **Laicky:** Claude Code si vytvoří "kopii" repozitáře na vedlejší koleji (git worktree), pracuje tam, a hlavní pracovní adresář zůstává nedotčený, dokud se výsledek neschválí.
- **Proč by to pomohlo analytikovi:** Paměť projektu už obsahuje poznámku k worktree handoffu, tedy se to použilo — ale ne systematicky. Systematické použití by snížilo riziko "omylem přepsaných" souborů při experimentálních úpravách specifikací.
- **Dá se předvést naživo:** Ano — vytvořit worktree, provést změnu, ukázat že hlavní adresář je nedotčený.
- **Poznámka:** netestováno — nemám s tím vlastní zkušenost.

### C6. Artifacts pro sdílení výstupů
- **Okruh:** `R` rozšíření
- **Laicky:** Místo posílání HTML souboru e-mailem/Teamsem se vytvoří odkaz na privátní webovou stránku, kterou lze podle potřeby sdílet dál.
- **Proč by to pomohlo analytikovi:** PLC simulace dopravníku (`docs/plc/dopravnik-simulace.html`) i review reporty jsou dnes statické soubory. Artifact by dal okamžitě sdílitelný odkaz bez nutnosti file transferu.
- **Dá se předvést naživo:** Ano — publikovat existující HTML jako artifact a ukázat odkaz.
- **Poznámka:** netestováno — nemám s tím vlastní zkušenost.

### C7. Levnější subagent (model override) pro objemné čtení
- **Okruh:** `O` orchestrace
- **Laicky:** Pomocnému "čtecímu" agentovi (např. review-structural, který jen kontroluje cross-reference) se dá přiřadit levnější/rychlejší model (Haiku) místo automatického zdědění drahého Opusu.
- **Proč by to pomohlo analytikovi:** Snížení nákladů a zrychlení review pipeline (5 review agentů v repozitáři) bez ztráty kvality tam, kde jde o mechanickou kontrolu.
- **Dá se předvést naživo:** Ano — nastavit `model: haiku` u jednoho review agenta a porovnat rychlost/cenu.
- **Poznámka:** netestováno — nemám s tím vlastní zkušenost.

### C8. `/insights` jako sebereflexe
- **Okruh:** `K` kontext
- **Laicky:** Vestavěný příkaz, který se podívá na moje poslední session a vygeneruje report — na čem pracuju, kde váznu, co bych mohl dělat efektivněji.
- **Proč by to pomohlo analytikovi:** Přímo použitelné jako "meta" ukázka na workshopu — je to přesně ten typ analýzy, který teď dělám ručně (fáze 1 statistiky).
- **Dá se předvést naživo:** Ano — spustit `/insights` a ukázat vygenerovaný HTML report.
- **Poznámka:** netestováno — nemám s tím vlastní zkušenost.

### C9. `claude plugin eval` pro ověření vlastních pluginů
- **Okruh:** `N` nastavení
- **Laicky:** Nástroj, který otestuje, jestli skilly/agenti v nainstalovaném pluginu skutečně dělají to, co mají — dřív než se na to spolehnu v ostrém provozu.
- **Proč by to pomohlo analytikovi:** V projektu jsou 3 vlastní/týmové pluginy (`knowledge-loop`, `ontology-registry`, `spec-factory` — verze se posunula 1.5→1.9 během projektu), bez evidence, že se po aktualizaci verze systematicky testují.
- **Dá se předvést naživo:** Nejisté — dokumentační URL se nepodařilo přímo dohledat, jistota existence příkazu je nižší než u ostatních položek (odvozeno z popisu agenta a nezávislých zdrojů, ne z přímé oficiální stránky).
- **Poznámka:** netestováno — nemám s tím vlastní zkušenost; navíc nejnižší jistota zdroje ze všech kandidátů v této sekci.

---

## Metodická poznámka

Web dokumentace (`docs.claude.com` → přesměrováno na `platform.claude.com` pro Claude API a `code.claude.com` pro Claude Code) byla čerpána přímo, ne z paměti modelu. Jeden fakt (`claude plugin eval`) má nižší jistotu, protože se nepodařilo dohledat přímou oficiální URL — je to označeno v tabulkách. Fakt o tokenizéru Sonnet 5 je explicitně označen jako nedohledaný, ne domyšlený.
