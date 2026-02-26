# Úroveň 2: Produktivní uživatel

> **Časová náročnost:** 11 kapitol, každá 10–15 minut. Celkem cca 2,5–3 hodiny rozložené do 1–2 týdnů.
> **Předpoklady:** Zvládnutá Úroveň 1 (milník splněn). Máte fungující instalaci, umíte konverzovat, provádět editace, commitovat.
> **Cíl úrovně:** Přejít od "umím to spustit" k "používám to efektivně každý den". Naučíte se, jak Claude Code funguje pod kapotou, jak s ním komunikovat tak, aby výsledky byly spolehlivé, a jak se vyhnout typickým pastem.

---

## 2.1 Mentální model: Jak přemýšlet o spolupráci s AI agentem

**Doba studia:** 10 minut

> Tato kapitola se zaměřuje na **principy myšlení** — jak přistupovat ke spolupráci s agentem. Kapitola 2.5 pak přidává **konkrétní techniky a šablony** promptů.

### Proč na tom záleží

Většina frustrací z Claude Code nepramení z technických omezení nástroje, ale z nesprávného mentálního modelu. Pokud k němu přistupujete jako k vyhledávači nebo textovému editoru, budete zklamaní. Claude Code je **agent s vlastní iniciativou** — sám rozhoduje, jaké kroky podnikne.

### Tři klíčové principy

**1. Buďte konkrétní — delegujte jako seniornímu kolegovi**

Srovnání přístupu:

| Vágní (slabý výsledek) | Konkrétní (silný výsledek) |
|------------------------|---------------------------|
| "Oprav ten bug." | "V souboru src/auth.ts funkce validateToken na řádku 42 neošetřuje expiraci tokenu. Přidej kontrolu a napiš test." |
| "Udělej to rychlejší." | "Funkce getUsers v src/db.ts dělá N+1 query. Refaktoruj na single query s JOIN." |
| "Přidej testy." | "Napiš unit testy pro NotificationService v tests/. Pokryj edge cases: prázdný vstup, null user, expired token. Použij existující styl z tests/auth.test.ts." |

Není nutné vždy psát román — ale čím víc kontextu poskytnete, tím méně iterací budete potřebovat.

**2. Poskytněte kontext — nechtějte, aby Claude hádal**

Claude vidí váš projekt, ale nevidí váš záměr, historii rozhodnutí ani byznys kontext. Řekněte mu:
- **Co** chcete (cíl, ne jen kroky)
- **Kde** hledat (soubory, moduly, řádky)
- **Jak** to má vypadat (odkaz na existující vzor: "Udělej to stejně jako v UserService")
- **Jak ověřit** (příkaz na spuštění testů, build, lint)

**3. Vždy ověřujte — důvěřuj, ale prověřuj**

Klíčová zásada: **řekněte Claude, JAK má ověřit svou práci**. Bez verifikačních kritérií Claude vytvoří něco, co vypadá správně, ale nemusí fungovat.

```
# Slabé — žádná verifikace
Implementuj funkci validateEmail.

# Silné — s verifikací
Implementuj funkci validateEmail.
Test cases: "user@example.com" → true, "invalid" → false, "user@.com" → false.
Po implementaci spusť testy a ověř, že projdou.
```

Verifikace může být: test suite, linter, build příkaz, screenshot (přes Chrome integraci), nebo prostě `npm run lint && npm test`.

> **Zdroj:** [Best Practices](https://code.claude.com/docs/en/best-practices)

### Vyzkoušejte

1. Vyberte úkol ve svém projektu (ideálně bug nebo malá feature)
2. Napište prompt dvěma způsoby: (A) vágně, (B) konkrétně s kontextem a verifikací
3. Spusťte oba (s `/clear` mezi nimi) a porovnejte výsledky
4. Zapište si, co fungovalo lépe

### Shrnutí
- Claude Code je agent, ne vyhledávač — dávejte mu cíle, ne jen příkazy
- Tři principy: buďte konkrétní, poskytněte kontext, vždy ověřujte
- Čím přesnější prompt, tím méně korekcí

---

## 2.2 Jak Claude Code funguje pod kapotou

**Doba studia:** 15 minut

### Agentní smyčka

Když Claude dostane úkol, rozhodne se, jaké **nástroje** použije. Každý nástroj vrátí informaci, která ovlivní další krok. Tak Claude řetězí desítky akcí za sebou:

```
Váš prompt: "Oprav selhávající testy"
  │
  ├─ 1. Spustí npm test (Bash)          → zjistí, co selhává
  ├─ 2. Přečte chybový výstup            → pochopí příčinu
  ├─ 3. Hledá relevantní zdrojáky (Grep) → najde soubory
  ├─ 4. Čte soubory (Read)               → pochopí kód
  ├─ 5. Edituje soubory (Edit)           → opraví chybu
  ├─ 6. Spustí npm test znovu (Bash)     → ověří opravu
  │     └─ Stále selhává?
  │         ├─ Ano → zpět na krok 4
  │         └─ Ne → hotovo
  └─ 7. Odpoví vám výsledkem
```

### Pět kategorií nástrojů

| Kategorie | Co Claude umí | Příklady |
|-----------|--------------|---------|
| **Souborové operace** | Čtení, editace, vytváření, přejmenování | Read, Edit, Write |
| **Vyhledávání** | Hledání souborů a obsahu | Glob, Grep |
| **Spouštění** | Shell příkazy, servery, testy, git | Bash |
| **Web** | Vyhledávání, stahování dokumentace | WebSearch, WebFetch |
| **Orchestrace** | Subagenti, dotazy na uživatele | Task, AskUserQuestion |

Claude sám volí, který nástroj použít. Vy ho nemusíte instruovat "použij Grep" — stačí říct "najdi, kde se to volá" a Claude sám zvolí správný nástroj.

### Context window — nejdůležitější omezení

Context window je **omezený prostor** (~200 000 tokenů, s rozšířeným kontextem až 1M), do kterého se musí vejít:

| Co zabírá kontext | Řádový odhad |
|---|---|
| Systémový prompt + CLAUDE.md | Tisíce tokenů |
| Definice MCP nástrojů | Stovky až tisíce tokenů/server |
| Každý přečtený soubor | Stovky až tisíce tokenů (záleží na délce) |
| Výstup příkazu (npm test apod.) | Stovky až desetitisíce tokenů |
| Každá zpráva v konverzaci | Desítky až stovky tokenů |
| Skills (popisy) | Stovky tokenů/skill |

> **Tip:** Přesné čísla závisí na obsahu. Použijte `/context` pro zobrazení reálné spotřeby ve vašem sezení.

Kontextové okno se plní **kumulativně** — každý přečtený soubor, každý spuštěný příkaz, každá vaše zpráva přidává tokeny. Proto:

- **Dlouhé sezení = horší výsledky** (kontext se zaplní, starší informace se ztrácejí)
- **`/clear` mezi úkoly** je nejdůležitější návyk (viz kapitola 2.8)

### Auto-kompakce

Když se kontext blíží limitu, Claude Code automaticky:
1. Odstraní starší výstupy nástrojů
2. Sumarizuje starší části konverzace
3. Zachová vaše požadavky a klíčové fragmenty kódu

Dřívější instrukce se ale mohou ztratit — proto důležitá pravidla patří do CLAUDE.md (viz kapitola 2.3), ne do konverzace.

### /compact a /context

- **`/compact`** — vynutí kompresi kontextu. Můžete přidat instrukce, co zachovat:
  ```
  /compact Zachovej informace o API změnách a testových příkazech
  ```
- **`/context`** — zobrazí, co zabírá místo v kontextu. Užitečné pro diagnostiku.

> **Zdroj:** [How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works)

### Vyzkoušejte

1. Spusťte sezení a postupně zadejte 10+ promptů (prozkoumávání kódu, dotazy, editace)
2. Napište `/cost` — kolik tokenů jste spotřebovali?
3. Napište `/context` — co zabírá nejvíc místa?
4. Napište `/compact Zachovej jen klíčové informace` — pozorujte, jak se kontext zmenší
5. Po kompakci položte otázku z dřívějška — pamatuje si Claude odpověď?

### Shrnutí
- Claude řetězí nástroje v agentní smyčce: čte → jedná → ověřuje → opakuje
- Context window (~200k tokenů) se plní kumulativně — proto krátká sezení = lepší výsledky
- `/compact` komprimuje kontext, `/context` ukazuje, co zabírá místo
- Trvalé instrukce patří do CLAUDE.md, ne do konverzace

---

## 2.3 Paměť: CLAUDE.md a auto-memory

**Doba studia:** 15 minut

### Co je CLAUDE.md

CLAUDE.md je soubor, který Claude čte **na začátku každého sezení**. Je to vaše "příručka pro AI kolegu" — obsahuje pravidla, konvence a kontext specifický pro projekt, které Claude nemůže odvodit ze samotného kódu.

### Vytvoření pomocí /init

Nejrychlejší cesta ke CLAUDE.md:

```
/init
```

Claude prozkoumá váš projekt a vygeneruje CLAUDE.md s: build příkazy, testovacími příkazy, kódovacím stylem, strukturou projektu. Pak ho můžete upravit.

### Co do CLAUDE.md patří (a co ne)

| Patří | Nepatří |
|-------|---------|
| Build/test/lint příkazy (`npm test`, `pytest`) | Cokoliv, co Claude zjistí čtením kódu |
| Nestandardní kódovací konvence | Obecné best practices ("piš čistý kód") |
| Architektonická rozhodnutí specifická pro projekt | Podrobná API dokumentace (odkažte na docs) |
| Konvence Git workflow (naming, PR formát) | Informace, které se často mění |
| Proměnné prostředí a dev environment specifika | Popis každého souboru v projektu |
| Věci, které Claude dělá špatně opakovaně | Samozřejmé praktiky |

### Příklad dobrého CLAUDE.md

```markdown
# Build & Test
- Build: `npm run build`
- Test: `npm test -- --watch=false`
- Lint: `npm run lint`
- Typecheck: `npx tsc --noEmit`

# Code Style
- ES modules (import/export), nikoli CommonJS (require)
- Destructuring importů: `import { foo } from 'bar'`
- Pojmenování: camelCase pro proměnné, PascalCase pro typy/třídy

# Architecture
- API endpointy v src/routes/, middleware v src/middleware/
- Databázové modely přes Prisma (src/models/)
- Autentizace: JWT tokeny, refresh v src/auth/

# Testing
- Testovací framework: Vitest
- Po sérii změn vždy spusť `npm test`
- Preferuj spuštění jednoho testu, ne celé sady

# Git
- Commit messages v angličtině, imperativ ("Add feature", ne "Added")
- Branch naming: feature/popis, bugfix/popis
```

> **Pravidlo:** Udržujte CLAUDE.md pod ~500 řádků. Pokud roste, přesuňte referenční materiál do skills (Úroveň 3). Pokud Claude ignoruje některá pravidla, soubor je příliš dlouhý a pravidlo se ztrácí.

### Hierarchie paměti

CLAUDE.md soubory existují na více úrovních. Všechny se načtou do kontextu:

| Umístění | Sdílení | Příklad použití |
|----------|---------|----------------|
| `~/.claude/CLAUDE.md` | Jen vy, všechny projekty | "Preferuji TypeScript strict mode" |
| `./CLAUDE.md` (projekt root) | Tým (přes Git) | Build příkazy, architektura |
| `./CLAUDE.local.md` | Jen vy, tento projekt | Vaše osobní sandbox URL |
| `./.claude/rules/*.md` | Tým (přes Git) | Modulární pravidla po tématech |
| Vnořené `podslozka/CLAUDE.md` | Tým | Pravidla specifická pro modul |

Vnořené CLAUDE.md (v podsložkách) se načítají **on demand** — až když Claude pracuje se soubory v dané složce.

### Importy v CLAUDE.md

CLAUDE.md může importovat další soubory pomocí syntaxe `@cesta`:

```markdown
Viz @README.md pro přehled projektu.

# Další instrukce
- Git workflow: @docs/git-instructions.md
- Osobní nastavení: @~/.claude/my-project-instructions.md
```

Cesty jsou relativní vůči souboru, ne working directory. Při prvním setkání s importy Claude zobrazí dialog ke schválení.

### Modulární pravidla: .claude/rules/

Pro větší projekty je lepší rozdělit pravidla do souborů:

```
.claude/rules/
├── code-style.md       # Kódovací styl
├── testing.md          # Testovací konvence
├── security.md         # Bezpečnostní požadavky
└── frontend/
    ├── react.md        # React specifika
    └── styles.md       # CSS konvence
```

Pravidla můžete omezit na konkrétní soubory pomocí YAML frontmatter:

```markdown
---
paths:
  - "src/api/**/*.ts"
---
# API Rules
- Všechny endpointy musí mít input validaci
- Používej standardní formát error response
```

### Auto-memory

Claude si sám ukládá naučené vzory do `~/.claude/projects/<projekt>/memory/`:

```
memory/
├── MEMORY.md          # Index (prvních 200 řádků se načte do kontextu)
├── debugging.md       # Poznámky k debuggingu
└── api-conventions.md # API konvence
```

**Jak auto-memory funguje:**
- Zapnuto ve výchozím stavu. Přepínání: `/memory`
- Claude sám zapisuje, co se naučil (build příkazy, řešení problémů, vaše preference)
- Přetrvává mezi sezeními
- Prvních 200 řádků MEMORY.md se načte do každého sezení automaticky
- Tematické soubory se načítají on demand

**Ruční uložení:** Řekněte Claude "Zapamatuj si, že používáme pnpm, ne npm" — Claude zapíše do paměti.

> **Zdroj:** [Memory](https://code.claude.com/docs/en/memory)

### Vyzkoušejte

1. Spusťte `/init` ve svém projektu
2. Otevřete vygenerovaný CLAUDE.md a přidejte 3–5 pravidel specifických pro váš projekt
3. Vytvořte `~/.claude/CLAUDE.md` (uživatelský) s 2–3 osobními preferencemi
4. Spusťte nové sezení a ověřte, že Claude respektuje vaše pravidla (řekněte mu "Jaká pravidla máš z CLAUDE.md?")
5. Commitněte CLAUDE.md do Gitu

### Shrnutí
- CLAUDE.md = instrukce, které Claude čte na začátku každého sezení
- `/init` vygeneruje základní verzi, pak upravte ručně
- Udržujte pod ~500 řádků, jen to, co Claude nemůže zjistit sám
- Hierarchie: uživatelský → projektový → lokální → modulární rules
- Auto-memory: Claude si sám ukládá naučené vzory mezi sezeními

---

## 2.4 Plan Mode — prozkoumej, pak jednej

**Doba studia:** 10 minut

### Co je Plan Mode

V Plan Mode Claude **jen čte a analyzuje** — neprovádí žádné změny v kódu. Je to bezpečný režim pro průzkum a plánování.

### Čtyřfázový workflow

Pro složitější úkoly (nová feature, refactoring, neznámý kód) používejte tento postup:

**Fáze 1 — Explore (Plan Mode):**
```
Přečti src/auth/ a vysvětli, jak fungují sessions a login.
Podívej se taky na proměnné prostředí.
```

**Fáze 2 — Plan (stále Plan Mode):**
```
Chci přidat Google OAuth. Jaké soubory se musí změnit?
Jaký bude flow? Vytvoř detailní plán.
```

**Ctrl+G** otevře plán ve vašem výchozím textovém editoru, kde ho můžete přímo upravit a uložit. Claude pak pokračuje s upraveným plánem.

**Fáze 3 — Implement (přepněte na Normal Mode):**
```
Implementuj OAuth flow podle plánu. Napiš testy
pro callback handler, spusť test suite a oprav selhání.
```

**Fáze 4 — Commit:**
```
Commitni s popisnou zprávou a vytvoř PR.
```

### Kdy Plan Mode použít

| Použijte Plan Mode | Přeskočte Plan Mode |
|--------------------|--------------------|
| Nová feature zasahující více souborů | Oprava překlepu |
| Neznáte kód, který budete měnit | Přidání log řádku |
| Nejste si jistí přístupem | Přejmenování proměnné |
| Složitý refactoring | Změna popsatelná jednou větou |

### Jak přepínat

- **Shift+Tab** — cyklicky přepíná Normal → Auto-accept → Plan → Normal
- **Start v Plan Mode:** `claude --permission-mode plan`
- **VS Code:** Kliknutí na režim v dolní části prompt boxu

> **Tip:** Nepoužívejte Plan Mode na jednoduchý úkol. Přidává overhead. Pokud dokážete popsat diff jednou větou, dělejte to rovnou v Normal Mode.

> **Zdroj:** [Common Workflows](https://code.claude.com/docs/en/common-workflows)

### Vyzkoušejte

1. Přepněte do Plan Mode (Shift+Tab dvakrát)
2. Řekněte: "Analyzuj architekturu tohoto projektu. Jak bys přidal [novou feature, kterou opravdu chcete]?"
3. Sledujte, jak Claude čte soubory, ale nic nemění
4. Přepněte zpět do Normal Mode (Shift+Tab)
5. Řekněte: "Implementuj první krok z plánu."

### Shrnutí
- Plan Mode = bezpečný read-only režim pro průzkum a plánování
- Workflow: Explore → Plan → Implement → Commit
- Shift+Tab přepíná režimy
- Používejte jen na složitější úkoly — na jednoduché věci je overhead

---

## 2.5 Efektivní prompt engineering pro Claude Code

**Doba studia:** 15 minut

> Kapitola 2.1 vysvětlila principy (buďte konkrétní, dejte kontext, ověřujte). Tato kapitola přidává **praktické techniky a šablony**, které tyto principy uvádějí do praxe.

### Proč je prompt engineering pro Claude Code jiný

Na rozdíl od běžného ChatGPT, kde formulujete otázky, v Claude Code **delegujete úkoly agentovi**. Agent pak sám rozhoduje o desítkách kroků. Kvalita prvního promptu proto dramaticky ovlivňuje kvalitu celého řetězce akcí.

### Čtyři techniky efektivních promptů

**1. Scoping — ohraničte úkol**

```
# Slabé
Přidej testy pro foo.py

# Silné
Napiš test pro foo.py pokrývající edge case, kdy je uživatel odhlášený.
Nepoužívej mocky. Spusť testy po napsání.
```

**2. Pointing — ukažte na zdroje**

```
# Slabé
Proč má ExecutionFactory tak zvláštní API?

# Silné
Podívej se na git historii ExecutionFactory a shrň, jak se jeho API vyvinulo.
```

**3. Pattern matching — odkažte na existující vzory**

```
# Slabé
Přidej calendar widget.

# Silné
Podívej se, jak jsou implementovány widgety na home page.
HotDogWidget.php je dobrý příklad. Následuj stejný vzor
pro nový calendar widget, který umožní vybrat měsíc
a stránkovat dopředu/dozadu po rocích.
```

**4. Verification — dejte kritéria úspěchu**

```
# Slabé
Oprav login bug.

# Silné
Uživatelé hlásí, že login selhává po session timeout.
Zkontroluj auth flow v src/auth/, zejména token refresh.
Napiš test, který reprodukuje problém, pak ho oprav.
Spusť npm test a ověř, že projde.
```

### Poskytování bohatého kontextu

| Metoda | Kdy použít |
|--------|------------|
| `@soubor.ts` | Odkaz na konkrétní soubor |
| Vložení screenshotu (drag & drop, Ctrl+V) | UI bugs, design review |
| URL dokumentace | API reference, specifikace |
| `cat error.log \| claude -p "..."` | Analýza logů, chybových výstupů |
| "Přečti si @README.md" | Kontext projektu |

### Nechte Claude, ať se vás zeptá

Pro větší features: místo perfektního promptu nechte Claude klást otázky:

```
Chci přidat [stručný popis]. Polož mi detailní otázky ohledně
technické implementace, UI/UX, edge cases a tradeoffs.
Ptej se, dokud nepokryjeme všechno. Pak napiš kompletní specifikaci do SPEC.md.
```

Po vytvoření specifikace spusťte `/clear` a nové sezení pro implementaci — specifikace bude v souboru a Claude ji přečte.

> **Zdroj:** [Best Practices](https://code.claude.com/docs/en/best-practices)

### Vyzkoušejte

1. Vyberte reálný úkol ve vašem projektu
2. Napište prompt, který kombinuje všechny čtyři techniky: scoping + pointing + pattern matching + verification
3. Sledujte, jak Claude pracuje — dělá méně kroků, než když zadáte vágní prompt?
4. Zkuste "interview" přístup: "Chci přidat X. Kladeš mi otázky, dokud nepokryjeme vše."

### Shrnutí
- Čtyři techniky: scope (ohranič), point (ukaž zdroje), pattern (odkaz na vzor), verify (kritéria úspěchu)
- Kontext: @soubory, screenshoty, URL, piping dat
- Pro velké features: nechte Claude klást otázky, specifikaci uložte do souboru

---

## 2.6 Práce s testy

**Doba studia:** 10 minut

### Proč jsou testy klíčové pro Claude Code

Testy jsou **nejlepší verifikační mechanismus**, který můžete Claude poskytnout. Když Claude vidí, že test prochází, má jistotu, že implementace funguje. Bez testů "doufá".

### Tři workflow s testy

**1. Napsat testy k existujícímu kódu:**
```
Najdi funkce v NotificationService.swift, které nemají testy.
Napiš testy pro tyto funkce. Přidej edge cases:
prázdný vstup, null user, expired token.
Spusť testy.
```

Claude prozkoumá existující testovací soubory, **napodobí styl a framework**, který už používáte, a vytvoří konzistentní testy.

> **Nemáte v projektu testy?** Claude vám pomůže nastavit testovací framework od nuly. Řekněte: "Nastav testovací framework pro tento projekt. Použij [Jest/Vitest/pytest/...]. Vytvoř konfiguraci a jeden ukázkový test." Po nastavení pokračujte obvyklým workflow.

**2. Test-first (TDD s Claude):**
```
Napiš selhávající test pro funkci, která validuje emailové adresy.
Případy: "user@example.com" → true, "invalid" → false, "user@.com" → false.
Pak implementuj funkci tak, aby testy prošly.
```

**3. Smyčka test-fix-test:**
```
Spusť npm test. Pokud něco selhává, oprav to a spusť znovu.
Opakuj, dokud vše neprojde.
```

Toto je extrémně efektivní — Claude sám iteruje opravy, dokud nejsou testy zelené.

### Jak Claude přistupuje k testům

- Prozkoumá existující testy (framework, assertion style, helper funkce)
- Napodobí existující konvence
- Pokryje hlavní cesty i edge cases (pokud o to požádáte)
- Po napsání testů je spustí a opraví selhání

### Best practice: Verifikace po každé změně

Do CLAUDE.md přidejte:
```markdown
# Testing
- Po sérii změn vždy spusť testy: `npm test`
- Preferuj spuštění jednoho testu místo celé sady (rychlejší zpětná vazba)
```

Nebo řekněte přímo v promptu:
```
Implementuj X. Po implementaci spusť relevantní testy a ověř, že projdou.
```

> **Zdroj:** [Common Workflows](https://code.claude.com/docs/en/common-workflows)

### Vyzkoušejte

1. Vyberte funkci ve svém projektu, která nemá testy
2. Řekněte Claude: "Napiš unit testy pro [funkce]. Zahrň edge cases. Spusť je."
3. Sledujte, jak Claude analyzuje existující testovací soubory a napodobí styl
4. Pokud některý test selže, řekněte: "Oprav selhávající testy a spusť znovu."
5. Zkuste TDD: "Napiš selhávající test pro [nová funkce], pak ji implementuj."

### Shrnutí
- Testy jsou nejlepší verifikace pro Claude — vždy žádejte "spusť testy po změně"
- Claude napodobí styl a framework existujících testů
- Smyčka test-fix-test: Claude sám iteruje opravy, dokud testy projdou
- Do CLAUDE.md přidejte testovací příkazy a konvence

---

## 2.7 Checkpointy a /rewind

**Doba studia:** 10 minut

### Jak checkpointy fungují

Každý váš prompt vytvoří **checkpoint** — snímek stavu souborů a konverzace. Claude Code automaticky sleduje všechny editace, které provádí. Checkpointy:

- Vznikají automaticky (nemusíte nic dělat)
- Přetrvávají mezi sezeními
- Automaticky se čistí po 30 dnech

### /rewind — vaše hlavní záchranná síť

Stiskněte **Escape × 2** nebo napište `/rewind`. Zobrazí se seznam vašich promptů v sezení. Vyberte bod, kam se chcete vrátit, a zvolte akci:

| Akce | Co udělá |
|------|---------|
| **Restore code and conversation** | Vrátí kód i konverzaci na vybraný bod |
| **Restore conversation** | Vrátí konverzaci, ale ponechá aktuální kód |
| **Restore code** | Vrátí kód, ale ponechá konverzaci |
| **Summarize from here** | Komprimuje konverzaci od vybraného bodu (šetří kontext) |
| **Never mind** | Zrušit, nic se nestane |

**Restore** vrací stav zpět (destruktivní). **Summarize** zachová vše, jen komprimuje text (nedestruktivní).

### Typické scénáře použití

**Zkoušení alternativ:**
```
1. Implementujete řešení A → nefunguje
2. /rewind → vrátí kód zpět
3. Zkusíte řešení B → funguje
```

**Oprava po chybě:**
```
1. Claude udělá rozsáhlou editaci → rozbije build
2. Escape × 2 → vyberete stav před editací
3. Restore code and conversation → zpět na funkční stav
```

**Úspora kontextu:**
```
1. Dlouhá debugging session → kontext se plní
2. /rewind → vyberete bod po dokončení debuggingu
3. Summarize from here → debugging se zkomprimuje do shrnutí
```

### Omezení checkpointů — důležité

> **Pozor:** Checkpointy sledují POUZE editace provedené Claude nástrojem Edit/Write. **Bash příkazy jako `rm`, `mv`, `cp`, `sed` checkpoint NEVRÁTÍ.** Pokud Claude smaže soubor přes `rm`, rewind ho neobnoví. Proto je Git vaše skutečná záchranná síť.

- **Nesledují Bash příkazy** — `rm soubor.txt`, `mv a.txt b.txt`, `sed -i ...` atd.
- **Nesledují externí změny** — pokud jste vy (nebo jiný proces) editovali soubor mimo Claude Code
- **Nejsou náhrada za Git** — vždy commitujte důležité stavy

> **Zdroj:** [Checkpointing](https://code.claude.com/docs/en/checkpointing)

### Vyzkoušejte

1. Nechte Claude provést editaci ve vašem projektu (třeba přidání funkce)
2. Stiskněte **Escape × 2** → zobrazí se rewind menu
3. Vyberte stav před editací → zvolte "Restore code and conversation"
4. Ověřte, že soubor se vrátil do původního stavu
5. Zkuste znovu, tentokrát zvolte "Restore code" (kód se vrátí, konverzace zůstane)

### Shrnutí
- Každý prompt vytváří checkpoint automaticky
- **Escape × 2** nebo `/rewind` otevře menu pro návrat
- Možnosti: vrátit kód, konverzaci, obojí, nebo sumarizovat
- Nenahrazuje Git — checkpoint nesleduje Bash příkazy ani externí změny

---

## 2.8 Správa kontextu a sezení

**Doba studia:** 10 minut

### Proč je toto nejdůležitější kapitola Úrovně 2

Správa kontextu je **klíčová dovednost** pro práci s Claude Code. Jakmile se kontext zaplní, Claude začíná:
- Zapomínat dřívější instrukce
- Dělat víc chyb
- Opakovat kroky, které už udělal
- Ignorovat pravidla z CLAUDE.md

### Zlaté pravidlo: nový úkol = /clear

```
[Dokončíte opravu bugu]
/clear
[Začnete psát testy — čistý kontext, plný výkon]
/clear
[Refaktorujete modul — opět čistý kontext]
```

Stará konverzace nezůstane — ale lze se k ní vrátit (viz resuming).

### Resuming: pokračování v předchozích sezeních

```bash
# Pokračovat v posledním sezení (v aktuálním adresáři)
claude --continue    # nebo zkráceně: claude -c

# Vybrat ze seznamu předchozích sezení
claude --resume      # nebo: claude -r

# Pojmenovat sezení pro snadné nalezení
/rename auth-refactor

# Pokračovat pojmenovaného sezení
claude --resume auth-refactor
```

**Ve VS Code:** Historie sezení je v dropdown menu v horní části Claude panelu.

**Klávesové zkratky v session picker (CLI):**

| Zkratka | Akce |
|---------|------|
| ↑/↓ | Navigace mezi sezeními |
| Enter | Obnovit vybrané sezení |
| P | Náhled obsahu sezení |
| R | Přejmenovat sezení |
| / | Vyhledávání |
| A | Přepnout mezi aktuálním adresářem a všemi projekty |
| B | Filtrovat na sezení z aktuální Git větve |
| Esc | Zavřít |

### Fork sezení

Pokud chcete vyzkoušet alternativní přístup bez ztráty původního sezení:

```bash
claude --continue --fork-session
```

Vytvoří kopii sezení s novým ID. Originál zůstane beze změny.

### /compact — inteligentní komprese

Když chcete pokračovat v dlouhém sezení, ale kontext se plní:

```
/compact                                    # Obecná komprese
/compact Zachovej API změny a test příkazy  # S instrukcí, co zachovat
```

**Summarize from /rewind** je ještě cílenější:
```
/rewind → vyberte bod → Summarize from here
```
Komprimuje jen část konverzace, starší kontext zůstane v plném znění.

### Praktická pravidla

| Situace | Akce |
|---------|------|
| Přecházíte na jiný úkol | `/clear` |
| Chcete se vrátit k včerejšímu úkolu | `claude -c` nebo `claude -r` |
| Sezení je dlouhé, Claude začíná chybovat | `/compact` nebo `/clear` |
| Chcete zkusit dvě varianty řešení | `claude --continue --fork-session` |
| Potřebujete investigovat bokem, aniž byste zaplnili kontext | "Use a subagent to investigate X" (Úroveň 3) |

> **Zdroj:** [How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works), [Common Workflows](https://code.claude.com/docs/en/common-workflows)

### Vyzkoušejte

1. Vytvořte pojmenované sezení: pracujte na úkolu, pak `/rename pokusný-úkol`
2. Spusťte `/clear` → čistý kontext
3. Pracujte na jiném úkolu
4. Obnovte předchozí: `claude --resume pokusný-úkol` — vše je zpět
5. Zkuste fork: `claude --continue --fork-session` — experimentujte, aniž byste ovlivnili originál

### Shrnutí
- `/clear` mezi úkoly = nejdůležitější návyk pro kvalitní výsledky
- `claude -c` pokračuje, `claude -r` vybere sezení, `/rename` pojmenuje
- `/compact` komprimuje kontext, `/rewind` + Summarize cíleně
- Fork pro alternativní přístupy bez ztráty originálu

---

## 2.9 Výběr modelu a řízení nákladů

**Doba studia:** 10 minut

### Modely a kdy který použít

| Model | Alias | Kdy použít | Orientační cena (API, vstup) |
|-------|-------|-----------|------------------------------|
| **Opus 4.6** | `opus` | Složitá architektura, multi-file refactoring, záludné bugy | ~$15/mil. tokenů |
| **Sonnet 4.6** | `sonnet` | Většina práce — výchozí a doporučený | ~$3/mil. tokenů |
| **Haiku 4.5** | `haiku` | Jednoduché dotazy, vysvětlení, dokumentace | ~$0.25/mil. tokenů |

**Speciální režimy:**
- **`opusplan`** — Opus v Plan Mode, Sonnet při implementaci. Nejlepší z obou světů pro plan-then-code workflow. Nastavení: `/model opusplan` nebo `claude --model opusplan`.
- **`sonnet[1m]`** / **`opus[1m]`** — 1M tokenů kontextu (beta). Pro velmi dlouhá sezení. Nastavení: `/model sonnet[1m]`.

### Effort levels (Opus 4.6)

Opus podporuje nastavení hloubky přemýšlení:

| Level | Chování | Kdy |
|-------|---------|-----|
| **high** (výchozí) | Maximální hloubka reasoning | Složité problémy |
| **medium** | Vyvážený | Běžná práce |
| **low** | Rychlé, mělké | Jednoduché úkoly |

Nastavení: v `/model` šipkami vlevo/vpravo, nebo `CLAUDE_CODE_EFFORT_LEVEL=medium`.

### Fast Mode

`/fast` — stejný model, ale rychlejší výstup. Neztratíte kvalitu, získáte rychlost. Přepíná se toggle příkazem.

### Extended thinking

Ve výchozím stavu zapnuto. Claude "přemýšlí" před odpovědí — spotřebovává thinking tokeny, které jsou účtovány jako výstupní tokeny (dražší). Pro jednoduché úkoly můžete:

- Snížit effort level v `/model`
- Vypnout thinking: **Alt+T** (nebo Option+T na macOS) — toggle
- Omezit budget: `MAX_THINKING_TOKENS=8000`
- Zobrazit reasoning v reálném čase: **Ctrl+O** (verbose mode — reasoning se zobrazuje jako šedý kurzivní text). Užitečné pro pochopení, jak Claude přemýšlí o vašem problému.

### Sledování nákladů

```
/cost    # Zobrazí spotřebu aktuálního sezení
```

Výstup:
```
Total cost:            $0.55
Total duration (API):  6m 19.7s
Total duration (wall): 6h 33m 10.2s
```

**Tipy pro úsporu:**
- Sonnet místo Opus pro běžnou práci (5× levnější)
- `/clear` mezi úkoly (menší kontext = méně tokenů za zprávu)
- Konkrétní prompty (méně explorativních kroků)
- Odpojte nepoužívané MCP servery (zabírají kontext)
- Subagenty pro verbose operace (výstup testů zůstane v izolovaném kontextu)

> **Zdroje:** [Model Config](https://code.claude.com/docs/en/model-config), [Costs](https://code.claude.com/docs/en/costs)

### Vyzkoušejte

1. Zkontrolujte aktuální model: `/model` — co je nastaveno?
2. Přepněte na `opusplan` a vyzkoušejte plan-then-implement workflow
3. Zapněte/vypněte thinking: Alt+T (sledujte rozdíl v rychlosti)
4. `/cost` po sérii interakcí — kolik jste utratili?
5. Porovnejte cenu za stejný úkol s Sonnet vs. Haiku

### Shrnutí
- Sonnet = výchozí a nejlepší poměr cena/výkon, Opus pro složité problémy
- `opusplan` = Opus pro plánování, Sonnet pro implementaci
- Effort levels a thinking kontrolují hloubku a cenu reasoning
- `/cost` sleduje náklady; `/clear` a konkrétní prompty šetří tokeny

---

## 2.10 Časté chyby a jak se jim vyhnout (anti-patterns)

**Doba studia:** 10 minut

### 1. Kitchen sink sezení

**Problém:** Začnete opravou bugu, pak se zeptáte na něco nesouvisejícího, pak se vrátíte k bugu. Kontext je plný nepotřebných informací.

**Řešení:** `/clear` mezi nesouvisejícími úkoly. Vždy.

### 2. Opakované opravování dokola

**Problém:** Claude udělá chybu, řeknete "ne, takhle ne", Claude zkusí znovu, stále špatně, opravíte znovu... Kontext se zanesde selhanými pokusy.

**Řešení:** Po dvou neúspěšných korekcích `/clear` a napište lepší prompt od nuly. Zahrňte to, co jste se naučili z předchozích pokusů.

```
# Špatně — třetí korekce ve znečištěném kontextu
Ne, to stále nefunguje. Zkus to jinak.

# Správně — čistý start s lepším promptem
/clear
Implementuj validaci emailu. Klíčové požadavky:
- Regex validace formátu
- Kontrola MX záznamu domény
- Nepoužívej knihovnu třetích stran
Test cases: [konkrétní případy]
```

### 3. Přeplněný CLAUDE.md

**Problém:** CLAUDE.md má 800+ řádků. Claude ignoruje většinu pravidel, protože se ztrácejí v šumu.

**Řešení:** Max ~500 řádků. Pokud Claude dělá něco správně i bez instrukce, smažte ji. Referenční materiál přesuňte do skills (Úroveň 3). Pravidelně CLAUDE.md revidujte.

**Test:** Pokud Claude opakovaně ignoruje pravidlo v CLAUDE.md, soubor je příliš dlouhý. Zkraťte ho nebo pravidlo zdůrazněte ("IMPORTANT: ...").

### 4. Slepá důvěra (trust-then-verify gap)

**Problém:** Claude vygeneruje kód, který vypadá přesvědčivě, ale neošetřuje edge cases. Přijmete bez kontroly.

**Řešení:** Vždy poskytněteverifikaci. Pokud nemůžete ověřit, nešipujte.

```
# Přidejte do každého implementačního promptu:
...po implementaci spusť npm test a ověř, že projde.
```

### 5. Nekonečná explorace

**Problém:** "Prozkoumej, jak funguje autentizace" — Claude přečte stovky souborů, kontext se zaplní, a vy nemáte použitelný výsledek.

**Řešení:** Ohraničte průzkum: "Prozkoumej JEN src/auth/ a shrň do 10 vět." Nebo delegujte na subagenta (Úroveň 3): "Use a subagent to investigate how authentication works."

### Shrnutí všech anti-patterns

| Anti-pattern | Signál | Řešení |
|-------------|--------|--------|
| Kitchen sink | Nesouvisející témata v jednom sezení | `/clear` mezi úkoly |
| Korekce dokola | 2+ neúspěšné opravy | `/clear`, lepší prompt |
| Přeplněný CLAUDE.md | Claude ignoruje pravidla | Zkrátit pod 500 řádků |
| Slepá důvěra | Kód bez testů/verifikace | Vždy přidejte verifikaci |
| Nekonečná explorace | Claude čte 100+ souborů | Ohraničit, nebo subagent |

> **Zdroj:** [Best Practices — Avoid Common Failure Patterns](https://code.claude.com/docs/en/best-practices)

### Vyzkoušejte

1. Zamyslete se: kterého anti-patternu se dopouštíte nejčastěji?
2. Zkuste úmyslně vyvolat "kitchen sink" sezení — promíchejte 3 nesouvisející úkoly. Pak zkuste totéž ve 3 oddělených sezeních. Porovnejte kvalitu.
3. Záměrně otestujte "korekci dokola" — po 2 neúspěšných opravách udělejte `/clear` a přeformulejte prompt.

### Shrnutí
- 5 pojmenovaných anti-patterns: kitchen sink, korekce dokola, přeplněný CLAUDE.md, slepá důvěra, nekonečná explorace
- Klíčový vzorec: pokud něco nefunguje → `/clear` a lepší prompt od nuly
- Verifikace (testy, build, lint) je nejlepší ochrana proti slepé důvěře

---

## 2.11 Základní troubleshooting

**Doba studia:** 10 minut

### /doctor — první krok při problémech

Kdykoli něco nefunguje, začněte:

```
/doctor
```

Provede kontrolu: instalace, auto-update, nastavení, MCP serverů, klávesových zkratek, kontextu, pluginů, agentů. Výstup ukáže, co je v pořádku a co ne.

### Nejčastější problémy a řešení

**Claude neodpovídá / visí:**
1. Stiskněte Escape
2. Pokud nepomůže: `/quit` a spusťte `claude` znovu
3. Pokud přetrvává: zkontrolujte internet a `claude auth status`

**Příkaz `claude` nenalezen:**
1. Zavřete a znovu otevřete terminál
2. Zkontrolujte: `which claude` (macOS/Linux) nebo `where claude` (Windows)
3. Pokud chybí v PATH: přeinstalujte nativní instalací

**Opakované žádosti o oprávnění:**
- `/permissions` → přidejte často schvalované příkazy do allowlistu
- Příklad: povolte `npm test`, `git status`, `eslint` natrvalo

**VS Code rozšíření nefunguje:**
1. Zkontrolujte verzi VS Code (min. 1.98.0)
2. Přeinstalujte rozšíření
3. Zkontrolujte, zda CLI funguje v terminálu (`claude --version`)

**Claude "zapomíná" instrukce uprostřed sezení:**
- Kontext se zaplnil → starší instrukce se ztratily
- Řešení: `/compact` nebo `/clear` a nové sezení
- Trvalé instrukce patří do CLAUDE.md, ne do konverzace

**Claude mění víc, než jste chtěli:**
- Claude někdy "vylepšuje" okolní kód nebo přidává nepožadované změny
- Řešení: buďte v promptu konkrétnější ("Změň JEN funkci X, nic jiného.")
- Nebo přidejte do CLAUDE.md: "Měň pouze to, o co žádám. Neupravuj okolní kód bez výslovného svolení."
- Případně zamítněte změnu (n) a upřesněte instrukce

**Pomalé odpovědi:**
- Velký projekt bez `.gitignore` → Claude indexuje příliš mnoho souborů
- Řešení: aktualizujte `.gitignore`, vyloučte `node_modules`, `dist`, velké binárky
- Nebo přepněte na Haiku pro rychlé dotazy

**Chyby autentizace (403, token expired):**
```bash
claude auth logout
claude auth login
```

> **Zdroj:** [Troubleshooting](https://code.claude.com/docs/en/troubleshooting)

### Vyzkoušejte

1. Spusťte `/doctor` — projděte výstup, opravte případné problémy
2. Spusťte `/permissions` — přidejte 2–3 příkazy, které nejčastěji schvalujete
3. Zkontrolujte `.gitignore` vašeho projektu — jsou tam velké adresáře jako `node_modules`?

### Shrnutí
- `/doctor` = první krok při jakémkoli problému
- "Zapomínání" = plný kontext → řešení: `/compact` nebo `/clear`
- `/permissions` pro allowlist často schvalovaných příkazů
- Aktualizujte `.gitignore` pro rychlejší odpovědi

---

## Milník Úrovně 2

Než přejdete na Úroveň 3, ověřte si:

- [ ] **CLAUDE.md:** Mám CLAUDE.md ve svém projektu s pravidly pro build, testy a styl kódu
- [ ] **Plan Mode:** Umím přepnout do Plan Mode a použít explore→plan→implement workflow
- [ ] **Efektivní prompty:** Formuluji konkrétní prompty s kontextem a verifikačními kritérii
- [ ] **Testy:** Nechal jsem Claude napsat testy a opravit selhání ve smyčce test-fix-test
- [ ] **Checkpointy:** Umím použít `/rewind` a vrátit kód/konverzaci na předchozí stav
- [ ] **Správa kontextu:** Používám `/clear` mezi úkoly, umím `claude -c` a `/compact`
- [ ] **Modely:** Umím zvolit správný model pro úkol, znám `/cost`
- [ ] **Anti-patterns:** Znám 5 pojmenovaných chyb a aktivně se jim vyhýbám

**Všechny body splněny?** Pokračujte na [Úroveň 3: Středně pokročilý](./osnova-claude-code.md).

---

> **Zdroje pro tuto úroveň:**
> - [Best Practices](https://code.claude.com/docs/en/best-practices) — jak pracovat efektivně
> - [How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works) — agentní smyčka a kontext
> - [Memory](https://code.claude.com/docs/en/memory) — CLAUDE.md a auto-memory
> - [Common Workflows](https://code.claude.com/docs/en/common-workflows) — Plan Mode, testy, PR
> - [Checkpointing](https://code.claude.com/docs/en/checkpointing) — checkpointy a /rewind
> - [Model Config](https://code.claude.com/docs/en/model-config) — výběr a konfigurace modelů
> - [Costs](https://code.claude.com/docs/en/costs) — náklady a optimalizace
> - [Troubleshooting](https://code.claude.com/docs/en/troubleshooting) — řešení problémů
