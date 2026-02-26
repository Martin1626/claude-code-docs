# Úroveň 1: Začátečník — Základy

> **Časová náročnost:** 7 kapitol, každá 10–15 minut. Celkem cca 1,5–2 hodiny studia rozložené do 1–3 dnů.
> **Co potřebujete:** Počítač s Windows/macOS/Linux, internet, účet u Anthropic.
> **Předpoklady:** Základní znalost příkazové řádky (terminál) a Gitu (commit, diff, checkout). Pokud Git neovládáte, naučte se alespoň `git init`, `git add`, `git commit`, `git diff` a `git checkout` — budete je potřebovat jako záchrannou síť.
> **Projekt k procvičení:** Mějte otevřený vlastní projekt (ideálně Git repozitář). Pokud žádný nemáte, naklonujte si libovolný open-source projekt, např.: `git clone https://github.com/expressjs/express.git`

---

## Než začnete: důležité upozornění

**Claude Code provádí reálné změny ve vašich souborech.** Není to simulace ani sandbox. Když schválíte úpravu, soubor se skutečně změní na disku. Proto:

1. **Pracujte v Git repozitáři.** Pokud něco pokazíte, vrátíte se pomocí Gitu.
2. **Před prvním experimentem commitněte aktuální stav:** `git add -A && git commit -m "stav před experimentem s Claude Code"`
3. **Vždy čtěte, co Claude navrhuje**, než kliknete na Accept/Yes.

---

## 1.1 Co je Claude Code a proč ho používat

**Doba studia:** 10 minut

### Co je Claude Code

Claude Code je **agentní kódovací nástroj** od Anthropic. Běží ve vašem terminálu nebo jako rozšíření ve VS Code. Na rozdíl od nástrojů, které jen doplňují kód (autocomplete), Claude Code je agent — umí samostatně:

- Číst a procházet soubory ve vašem projektu
- Upravovat kód ve více souborech najednou
- Spouštět příkazy v terminálu (testy, build, git, ...)
- Hledat na webu, stahovat dokumentaci
- Vytvářet commity a pull requesty

### Jak se liší od jiných nástrojů

| Nástroj | Přístup | Co vidí | Co umí udělat |
|---------|---------|---------|---------------|
| **ChatGPT** | Konverzace v prohlížeči | Co vložíte + nahrané soubory | Odpovědět textem/kódem, spustit Python v sandboxu |
| **GitHub Copilot Chat** | Chat v editoru | Aktuální workspace (soubory, terminál) | Navrhnout kód, vysvětlit, generovat |
| **Claude Code** | Agent v terminálu/IDE | Všechny soubory, terminál, git, web | Číst, psát, spouštět příkazy, commitovat, vytvářet PR |

Hlavní rozdíl: Copilot a ChatGPT **navrhují** kód, který pak vy aplikujete. Claude Code **sám provádí** změny (s vaším schválením), spouští příkazy, ověřuje výsledky a iteruje — jako by vedle vás seděl kolega.

> **Poznámka k objektivitě:** Každý nástroj má své silné stránky. Copilot exceluje v inline completions. ChatGPT je univerzální. Claude Code je nejsilnější v autonomním řešení celých úkolů napříč více soubory.

### Klíčový mentální model

Claude Code není "chytřejší autocomplete". Je to spíš **junior kolega, kterému dáte přístup k vašemu terminálu.** Můžete mu říct "Oprav ten bug v autentizaci" a on sám najde relevantní soubory, přečte je, pochopí kontext, provede opravu a spustí testy. Ale jako u každého juniora — kontrolujete jeho práci.

### Kde všude Claude Code běží

- **Terminál (CLI)** — plnohodnotné rozhraní, nejvíc funkcí
- **VS Code / Cursor** — grafické rozšíření s diff review, @-zmínkami
- **JetBrains IDE** — plugin pro IntelliJ, PyCharm, WebStorm a další
- **Desktop aplikace** — samostatná aplikace pro macOS a Windows
- **Webový prohlížeč** — na claude.ai/code, bez lokální instalace
- **Slack** — @Claude v kanálech pro týmovou spolupráci

Konfigurace (CLAUDE.md, nastavení, MCP servery) se sdílí napříč všemi prostředími.

### Kolik to stojí

| Varianta | Cena | Limity |
|----------|------|--------|
| **Claude Pro** | $20/měsíc | Zahrnuté použití, omezené množství zpráv |
| **Claude Max** | $100–200/měsíc | Výrazně vyšší limity, vhodné pro celodenní práci |
| **API klíč** | Platba za tokeny | Průměrně ~$6/den (~$100–200/měsíc se Sonnet) |

Při vyčerpání limitu předplatného se musíte buď přepnout na nižší model, počkat na reset, nebo přejít na API klíč.

> **Zdroj:** [Overview](https://code.claude.com/docs/en/overview), [Costs](https://code.claude.com/docs/en/costs)

### Vyzkoušejte

Ještě nic neinstalujte. Zamyslete se:
1. Na jakém projektu chcete Claude Code zkoušet?
2. Jaké tři úkoly vás v tomto projektu nejvíc zdržují? (psaní testů? debugging? code review? dokumentace?)
3. Zapište si je — budou vaší motivací při studiu.

### Shrnutí
- Claude Code je agent, který autonomně čte, píše a spouští příkazy ve vašem projektu
- Liší se od Copilot/ChatGPT tím, že sám provádí změny a iteruje
- Běží v terminálu, VS Code, JetBrains, desktopu i na webu
- Stojí $20–200/měsíc podle varianty

---

## 1.2 Instalace a první spuštění

**Doba studia:** 10–15 minut (včetně samotné instalace)

### Předpoklady

- **Windows:** Nainstalovaný [Git for Windows](https://git-scm.com/download/win) (Claude Code ho vyžaduje)
- **macOS/Linux:** Standardní terminál, žádné speciální předpoklady
- **Účet:** Jedna z následujících možností:
  - Předplatné Claude Pro ($20/měsíc) nebo Max ($100+/měsíc) na [claude.ai](https://claude.ai)
  - API klíč z [console.anthropic.com](https://console.anthropic.com) (s kreditem)

### Instalace CLI

Vyberte postup pro váš systém:

**macOS / Linux / WSL:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD:**
```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

**Alternativní metody:**
```bash
# Homebrew (macOS/Linux) — pozor: neaktualizuje se automaticky
brew install --cask claude-code

# WinGet (Windows) — pozor: neaktualizuje se automaticky
winget install Anthropic.ClaudeCode
```

> **Důležité:** Nativní instalace (curl/irm) se automaticky aktualizuje na pozadí. Homebrew a WinGet vyžadují ruční aktualizaci příkazem `brew upgrade claude-code` resp. `winget upgrade Anthropic.ClaudeCode`.

### Ověření instalace

```bash
claude --version
```
Pokud vidíte číslo verze (např. `1.0.42`) — instalace proběhla úspěšně.

**Pokud se zobrazí "command not found":** Zavřete a znovu otevřete terminál. Pokud problém přetrvává, zkontrolujte PATH — viz [Troubleshooting](https://code.claude.com/docs/en/troubleshooting).

### Instalace VS Code rozšíření

1. Otevřete VS Code
2. Přejděte do Extensions (Ctrl+Shift+X)
3. Vyhledejte **"Claude Code"** (vydavatel: Anthropic)
4. Klikněte **Install**

> **Požadavek:** VS Code verze 1.98.0 nebo novější. Funguje i v **Cursor**.

### Přihlášení

Máte dvě cesty podle typu účtu:

**Cesta A: Předplatné Claude Pro/Max**
```bash
cd vas-projekt
claude
```
Při prvním spuštění se otevře prohlížeč s přihlášením. Přihlaste se svým Anthropic účtem a vraťte se do terminálu.

**Cesta B: API klíč**

Nastavte proměnnou prostředí **před** spuštěním Claude:

```bash
# macOS/Linux — přidejte do ~/.bashrc nebo ~/.zshrc pro trvalé nastavení
export ANTHROPIC_API_KEY=sk-ant-api03-vášklíč

# Windows PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-api03-vášklíč"

# Pak spusťte
cd vas-projekt
claude
```

Ověření přihlášení:
```bash
claude auth status
```

**Ve VS Code:** Otevřete panel Claude Code (ikona ✦ v horním panelu editoru, nebo Ctrl+Shift+P → "Claude Code: Open"). Budete vyzváni k přihlášení stejným způsobem.

> **Zdroje:** [Setup](https://code.claude.com/docs/en/setup), [VS Code](https://code.claude.com/docs/en/vs-code), [Authentication](https://code.claude.com/docs/en/authentication)

### Vyzkoušejte

1. Nainstalujte CLI a ověřte: `claude --version`
2. Nainstalujte VS Code rozšíření
3. Přihlaste se (předplatné nebo API klíč)
4. Spusťte `claude` ve svém projektu — měli byste vidět uvítací obrazovku
5. Zatím nic nepište, to bude v další kapitole

### Shrnutí
- Nativní instalace (curl/irm) je doporučená — automaticky se aktualizuje
- Windows vyžaduje Git for Windows
- Přihlášení funguje přes Anthropic účet (předplatné) nebo API klíč (proměnná prostředí)
- VS Code rozšíření je k dispozici v Marketplace

---

## 1.3 První interaktivní sezení

**Doba studia:** 10–15 minut

### Spuštění sezení

Otevřete terminál v kořenovém adresáři vašeho projektu a napište:

```bash
claude
```

Uvidíte prompt, kam můžete psát. Claude Code nyní vidí soubory ve vašem projektu a čeká na instrukci.

**Ve VS Code:** Otevřete panel Claude Code (ikona ✦ nebo Ctrl+Shift+P → "Claude Code: Open") a pište do textového pole.

### Očekávaná doba odezvy

Claude Code **není instantní jako vyhledávač**. Odpověď trvá typicky 5–60 sekund, protože Claude:
1. Přemýšlí o vaší otázce
2. Čte relevantní soubory (vidíte v reálném čase)
3. Případně spouští příkazy
4. Formuluje odpověď

To je normální. Čím složitější úkol, tím déle trvá. Sledujte indikátor aktivity — uvidíte, co Claude právě dělá.

### Co se děje pod kapotou

Když pošlete zprávu, Claude projde třemi fázemi. Ty se opakují, dokud není úkol hotový:

```
1. SBĚR KONTEXTU     Claude čte soubory, hledá, analyzuje
        ↓
2. AKCE              Claude upravuje kód, spouští příkazy
        ↓
3. OVĚŘENÍ           Claude kontroluje výsledek (testy, build)
        ↓
   (zpět na 1., dokud není hotovo)
```

Toto je **agentní smyčka** — Claude sám rozhoduje, jaké kroky udělá. Vy sledujete průběh v reálném čase a můžete kdykoli zasáhnout.

### Vaše první prompty

Claude Code rozumí česky i anglicky. Pro technické úkoly bývá angličtina přesnější (Claude trénoval převážně na anglických datech), ale pro běžnou komunikaci čeština funguje skvěle. Ukázky v obou jazycích:

**Průzkum projektu:**
```
Vysvětli mi strukturu tohoto projektu. Jaké technologie používá
a jak jsou organizovány hlavní složky?
```
nebo anglicky:
```
Explain the structure of this project. What technologies does it use
and how are the main directories organized?
```

**Ukázka typického průběhu** (co uvidíte v terminálu):

```
You: Vysvětli mi strukturu tohoto projektu.

Claude: Podívám se na soubory v projektu...

  ● Read(package.json)
  ● Read(tsconfig.json)
  ● Read(src/index.ts)
  ● Glob(src/**/*.ts)
  ● Read(README.md)

Toto je TypeScript projekt postavený na Express.js. Struktura:

  src/
  ├── index.ts          - Vstupní bod, konfigurace Express serveru
  ├── routes/           - API endpointy
  │   ├── auth.ts       - Autentizace (login, register, logout)
  │   └── users.ts      - CRUD operace nad uživateli
  ├── middleware/        - Express middleware
  │   └── auth.ts       - JWT ověření tokenu
  ├── models/           - Databázové modely (Prisma)
  └── utils/            - Pomocné funkce

  Používá: TypeScript, Express, Prisma ORM, PostgreSQL, JWT.
  Build: npm run build, Testy: npm test
```

**Vysvětlení kódu:**
```
Co dělá funkce handleLogin v souboru src/routes/auth.ts?
```

**Hledání v kódu:**
```
Kde v projektu se zpracovávají platby? Najdi relevantní soubory.
```

### Konverzační styl

Claude Code je konverzační — nemusíte psát dokonalé prompty. Začněte tím, co chcete, a pak upřesňujte:

```
Vy:     Jak funguje autentizace v tomto projektu?
Claude: [čte soubory, vysvětlí]

Vy:     A kde se ověřuje JWT token?
Claude: [najde a vysvětlí konkrétní místo]

Vy:     Ten token se ale nevaliduje na expiraci. Oprav to.
Claude: [navrhne opravu — tady vás požádá o oprávnění]
```

### Záchranná síť: Escape

Pokud Claude dělá něco, co nechcete:
- **Escape** — zastaví aktuální akci. Claude se zastaví a čeká na další instrukci.
- **Escape × 2** (dvojité stisknutí) — **rewind**: vrátí kód i konverzaci na předchozí stav, jako by se akce nestala. Toto je vaše hlavní záchranná brzda.
- Napište opravu a stiskněte **Enter** — Claude přečte vaši zprávu a změní směr.

> **Zapamatujte si Escape × 2.** Je to nejdůležitější záchranná zkratka a budete ji používat často.

### Co dělat, když něco nefunguje

| Problém | Řešení |
|---------|--------|
| Claude neodpovídá dlouho (>2 min) | Stiskněte Escape a zkuste znovu, nebo `/quit` a nové spuštění |
| Claude čte příliš mnoho souborů | Buďte konkrétnější: "Podívej se jen na src/auth/" |
| Odpověď je příliš obecná | Přidejte kontext: "Konkrétně v kontextu tohoto Express.js projektu..." |
| Claude halucinuje neexistující soubory | Řekněte: "Ověř, že soubor existuje, než ho budeš komentovat." |

> **Zdroj:** [Quickstart](https://code.claude.com/docs/en/quickstart), [How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works)

### Vyzkoušejte

1. Spusťte `claude` ve svém projektu
2. Zeptejte se: "Vysvětli mi strukturu tohoto projektu a jaké technologie používá."
3. Sledujte, jaké soubory Claude čte (zobrazuje se v reálném čase)
4. Zeptejte se na konkrétní funkci nebo soubor
5. Zkuste konverzaci — položte navazující otázku k předchozí odpovědi
6. Zkuste stisknout **Escape** v průběhu odpovědi — Claude se zastaví
7. Ukončete sezení: `/quit` nebo Ctrl+C

### Shrnutí
- Odpověď trvá 5–60 sekund — Claude čte soubory a přemýšlí, to je normální
- Claude rozumí česky i anglicky, pro technické úkoly zvažte angličtinu
- Konverzace je iterativní: začněte obecně, upřesňujte
- **Escape** zastaví akci, **Escape × 2** vrátí vše zpět (rewind)

---

## 1.4 Systém oprávnění — co Claude smí a nesmí

**Doba studia:** 10 minut

### Proč Claude žádá o povolení

Claude Code má přístup k vašemu souborovému systému a terminálu — proto existuje systém oprávnění, který zajišťuje, že Claude neprovede nic bez vašeho vědomí.

**Co Claude dělá BEZ ptaní:**
- Čte soubory
- Prohledává kód
- Analyzuje projekt

**Na co se Claude PTÁ:**
- Upravit/vytvořit soubor → zobrazí diff (rozdíl)
- Spustit příkaz v terminálu → zobrazí příkaz
- Smazat soubor → zobrazí varování

### Jak vypadá dialog oprávnění

**V terminálu:**
```
Claude wants to edit: src/utils.ts

  - function calculate(x) {
  + function calculate(price) {

  Allow? (y = yes, n = no, a = always allow)
```

**Pro příkazy:**
```
Claude wants to run: npm test

  Allow? (y = yes, n = no, a = always allow this command)
```

Vaše možnosti:
| Volba | Co udělá |
|-------|----------|
| **y** (Yes) | Povolí jednou |
| **n** (No) | Zamítne — Claude zkusí jiný přístup |
| **a** (Always) | Povolí vždy tento typ akce (přidá se do trvalého allowlistu) |

### Co se stane, když zamítnete

Nic špatného. Claude dostane zprávu, že akce byla zamítnuta, a:
- Zkusí jiný přístup k problému
- Nebo se zeptá, jak chcete postupovat

**Neváhejte zamítnout cokoliv**, co vám nepřijde správné. Je to bezpečné a je to přesně tak, jak je Claude Code navržen.

### Tři základní režimy

Přepínaní režimů: **Shift+Tab** (v terminálu i VS Code).

| Režim | Co Claude smí bez ptaní | Kdy použít |
|-------|------------------------|------------|
| **Normal** (výchozí) | Číst soubory, hledat | Běžná práce — máte kontrolu nad každou změnou |
| **Auto-accept edits** | Číst + editovat soubory | Důvěřujete Claude s úpravami, chcete schvalovat jen příkazy |
| **Plan Mode** | Jen číst, nic neměnit | Průzkum kódu, plánování — žádné riziko změn |

> **Tip pro začátečníky:** Zůstaňte v **Normal** režimu. Dává vám plnou kontrolu a ukazuje diff před každou změnou. Na ostatní režimy se podíváme v pozdějších úrovních.

### Připomenutí: záchranné zkratky

Pokud schválíte něco, co jste nechtěli:
- **Escape × 2** — rewind: vrátí kód i konverzaci na předchozí bod
- **git checkout -- soubor** — vrátí soubor do posledního commitnutého stavu
- **git diff** — ukáže všechny změny od posledního commitu

> **Zdroj:** [Permissions](https://code.claude.com/docs/en/permissions)

### Vyzkoušejte

1. Spusťte nové sezení (`claude` nebo `/clear`)
2. Požádejte Claude o jednoduchou změnu: "Přidej komentář k první funkci v souboru [vyberte soubor]."
3. Když se zobrazí diff — přečtěte si ho. Rozumíte, co Claude mění?
4. Schvalte změnu (**y**)
5. Podívejte se na soubor — skutečně se změnil
6. Teď požádejte o další změnu a tentokrát ji **zamítněte** (**n**). Co Claude udělá?
7. Zkuste stisknout **Shift+Tab** — vidíte přepínání režimů

### Shrnutí
- Claude se ptá před úpravou souborů a spouštěním příkazů — to je záměrné
- **y** = jednou, **n** = zamítni, **a** = povol vždy
- Zamítnutí je bezpečné — Claude zkusí jiný přístup
- Normal režim (výchozí) je pro začátečníky nejlepší
- **Escape × 2** = rewind — vaše hlavní záchranná brzda

---

## 1.5 Základní slash příkazy

**Doba studia:** 10 minut

### Co jsou slash příkazy

Slash příkazy jsou speciální příkazy začínající lomítkem (`/`), které ovládají samotné Claude Code — na rozdíl od běžných promptů, které jdou k AI modelu. Píšete je do promptu místo instrukce.

### Nejdůležitější příkazy

| Příkaz | Co dělá | Kdy použít |
|--------|---------|------------|
| `/help` | Zobrazí přehled příkazů a zkratek | Když nevíte, co je k dispozici |
| `/clear` | Vymaže konverzaci, začne nový kontext | **Mezi úkoly** — nejdůležitější návyk |
| `/quit` | Ukončí Claude Code | Když chcete skončit |
| `/model` | Přepne AI model | Změna modelu (viz níže) |
| `/cost` | Spotřeba tokenů a náklady sezení | Sledování nákladů |
| `/compact` | Komprimuje kontext konverzace | Když sezení trvá dlouho |
| `/doctor` | Diagnostika instalace | Když něco nefunguje |
| `/init` | Vytvoří CLAUDE.md pro projekt | Jednou na začátku projektu (Úroveň 2) |

### Přepínání modelů

```
/model sonnet
```

Claude Code nabízí tři modely:

| Model | Rychlost | Kvalita | Orientační cena (API) | Vhodný pro |
|-------|----------|---------|----------------------|------------|
| **Haiku** | Nejrychlejší | Dobrá | ~$0.25/mil. vstup. tokenů | Jednoduché dotazy, vysvětlení |
| **Sonnet** | Střední | Velmi dobrá | ~$3/mil. vstup. tokenů | Většina práce — výchozí volba |
| **Opus** | Nejpomalejší | Nejlepší | ~$15/mil. vstup. tokenů | Složitá architektura, debugging |

> **Pravidlo:** Začněte se **Sonnet**. Je to nejlepší poměr cena/výkon. Opus použijte, jen když Sonnet nezvládá složitější problém. Haiku na rychlé jednoduché dotazy.

Model platí pro aktuální sezení. Po `/clear` nebo novém spuštění se vrátí na výchozí.

### Klávesové zkratky

| Zkratka | Akce |
|---------|------|
| **Enter** | Odeslat prompt |
| **Shift+Enter** | Nový řádek v promptu (víceřádkový vstup) |
| **Escape** | Zastavit Claude |
| **Escape × 2** | Rewind — vrátit kód i konverzaci zpět |
| **Shift+Tab** | Přepnout režim (Normal → Accept-Edits → Plan) |
| **↑ / ↓** | Procházení historie předchozích promptů |

### /clear — nejdůležitější návyk

Tento příkaz si zaslouží zvláštní pozornost.

Claude Code pracuje s **kontextovým oknem** — omezeným prostorem (~200 000 tokenů), do kterého se vejde konverzace, přečtené soubory, výstupy příkazů. Čím delší konverzace, tím více se kontext plní. Když je plný:
- Starší informace se ztrácejí
- Kvalita odpovědí klesá
- Claude může "zapomenout" instrukce z počátku konverzace

**Pravidlo:** Nový úkol = `/clear`. Nepřeplňujte kontext nesouvisejícími tématy.

```
[Dokončíte opravu bugu]
/clear
[Začnete psát testy — čistý kontext, lepší výsledky]
```

> **Zdroj:** [Interactive Mode](https://code.claude.com/docs/en/interactive-mode)

### Vyzkoušejte

1. Napište `/help` — projděte si seznam dostupných příkazů
2. Napište `/cost` — kolik stálo sezení zatím?
3. Přepněte model: `/model haiku`, položte otázku. Pak `/model sonnet` a stejnou otázku. Vidíte rozdíl v kvalitě a rychlosti?
4. Napište `/clear` — konverzace zmizí, začínáte od nuly
5. Napište `/doctor` — zkontrolujte, že je vše v pořádku
6. Zkuste šipku **↑** — zobrazí se váš předchozí prompt

### Shrnutí
- Slash příkazy ovládají Claude Code, ne AI model
- `/clear` mezi úkoly je nejdůležitější návyk pro kvalitní výsledky
- Sonnet je výchozí model, Opus pro složité problémy, Haiku pro jednoduché
- Escape = stop, Escape × 2 = rewind, Shift+Tab = přepnutí režimu

---

## 1.6 První úprava kódu a Git commit

**Doba studia:** 15 minut

### Požádejte Claude o změnu

Teď přichází to hlavní — necháme Claude skutečně upravit kód. Vyberte si jednoduchý, bezpečný úkol:

**Příklady dobrých prvních úkolů:**
```
Add a JSDoc comment to the calculateTotal function in src/utils.ts
```
```
Přejmenuj proměnnou "x" na "userId" v souboru src/handlers/auth.js
```
```
Přidej ošetření null v funkci getUser v src/db.ts na řádku 42
```

> **Tip:** Buďte konkrétní — uveďte soubor a funkci. Čím přesnější instrukce, tím lepší výsledek.

### Kontrola diffu

Claude analyzuje kód a navrhne změnu. Uvidíte **diff** — porovnání starého a nového kódu:

**V terminálu:**
```diff
  src/utils.ts

- function calculateTotal(items) {
+ /**
+  * Calculates total price of items including tax.
+  * @param items - Array of items with price property
+  * @returns Total price
+  */
+ function calculateTotal(items) {
```

Červená (se znakem `-`) = odstraněno. Zelená (se znakem `+`) = přidáno.

**Ve VS Code** uvidíte vizuální side-by-side diff — starý kód vlevo, nový vpravo, s barevným zvýrazněním. Pod diffem jsou tlačítka Accept / Reject.

### Checklist: co zkontrolovat v diffu

Než schválíte, ověřte:

1. **Mění se to, co jste chtěli?** — Žádné nechtěné vedlejší změny?
2. **Je kód správný?** — Syntaxe, logika, typové chyby?
3. **Nemění se víc souborů, než čekáte?** — Claude občas "vylepší" i věci, o které jste nežádali
4. **Neodstraňuje se důležitý kód?** — Claude občas smaže kód, který považuje za nepotřebný

Pokud je vše v pořádku → **y** (Yes)
Pokud ne → **n** (No) a řekněte Claude, co má udělat jinak.

### Vytvoření Git commitu

Po schválení změn můžete nechat Claude vytvořit commit:

```
Commitni tyto změny s vhodnou commit message.
```

Claude provede:
1. `git add` — přidá změněné soubory do stage
2. `git commit -m "popis změn"` — vytvoří commit

Claude navrhne commit message na základě provedených změn. Uvidíte ji před schválením. Pokud chcete vlastní:
```
Commitni s message "Add JSDoc to calculateTotal function"
```

### Pull request

Claude umí vytvořit i PR (vyžaduje nainstalované [GitHub CLI](https://cli.github.com/)):
```
Vytvoř pull request s popisem změn.
```

### Když se něco pokazí — záchranné postupy

| Situace | Řešení |
|---------|--------|
| Schválil jsem špatnou editaci | **Escape × 2** (rewind) — vrátí kód i konverzaci |
| Claude změnil víc souborů, než jsem chtěl | `git diff` pro zobrazení všech změn, `git checkout -- soubor` pro vrácení konkrétního souboru |
| Chci vrátit úplně všechno | `git checkout .` vrátí všechny soubory do posledního commitu |
| Commit message se mi nelíbí | `git commit --amend -m "nová message"` (jen pokud jste nepushovali) |

> **Poznámka:** Příkazy `git checkout .` a `git reset --hard` jsou destruktivní — smažou neuložené změny. Používejte je s rozvahou.

> **Zdroj:** [Quickstart](https://code.claude.com/docs/en/quickstart)

### Vyzkoušejte

1. Commitněte aktuální stav projektu (záchranný bod): `git add -A && git commit -m "před experimentem"`
2. Požádejte Claude o přidání komentáře k funkci
3. Přečtěte si diff — rozumíte, co se mění?
4. Schvalte změnu (**y**)
5. Ověřte, že se soubor skutečně změnil (otevřete ho)
6. Řekněte Claude: "Commitni tyto změny." — zkontrolujte commit message
7. Ověřte: `git log --oneline -3`
8. **Bonus:** Požádejte o další změnu, ale tentokrát ji odmítněte (**n**). Pak požádejte o jiný přístup.

### Shrnutí
- Buďte v instrukci konkrétní: soubor, funkce, co přesně udělat
- Vždy čtěte diff — červená = odstraněno, zelená = přidáno
- Claude umí commitovat i vytvářet PR
- **Escape × 2** vrátí kód zpět, `git checkout -- soubor` vrátí konkrétní soubor

---

## 1.7 VS Code rozšíření — základní orientace

**Doba studia:** 10–15 minut

### Kde najít Claude Code ve VS Code

Po instalaci rozšíření máte několik způsobů, jak otevřít panel:

| Metoda | Jak |
|--------|-----|
| **Ikona ✦ (Spark)** | V horním panelu editoru — nejrychlejší |
| **Command Palette** | Ctrl+Shift+P → "Claude Code: Focus on Input" |
| **Klávesová zkratka** | Nastavte si vlastní v Keyboard Shortcuts |

Panel se ve výchozím stavu otevře v **sekundárním postranním panelu** (vpravo). Můžete ho přesunout:
- Do hlavního postranního panelu (vlevo): přetáhněte ikonu
- Do oblasti editoru (jako záložka): pravým klikem → "Open in New Tab"
- Do nového okna: pravým klikem → "Open in New Window"

### Workflow ve VS Code — krok za krokem

**1. Pošlete prompt:**
Napište instrukci do textového pole v panelu a stiskněte Enter.

**2. Sledujte průběh:**
V panelu vidíte v reálném čase, co Claude dělá — jaké soubory čte, co hledá.

**3. Zkontrolujte navržené změny:**
Když Claude navrhne úpravu, otevře se **diff view** přímo v editoru:
- Vlevo: **původní** kód
- Vpravo: **navrhovaný** kód
- Zelené řádky: přidané
- Červené řádky: odebrané

**4. Rozhodněte se:**
Nad diffem (nebo v panelu) uvidíte tlačítka:
- **Accept** — aplikuje změnu do souboru
- **Reject** — zahodí změnu, soubor zůstane beze změny
- Můžete také napsat komentář do panelu (redirect): "Tohle ne, místo toho udělej X" — Claude upraví svůj přístup

### @-zmínky — odkazování na soubory

Klíčová funkce VS Code rozšíření. Napište `@` do promptu a začněte psát:

```
@src/auth.ts Vysvětli, jak funguje validace tokenu v tomto souboru.
```

@-zmínky podporují:
| Typ | Příklad | Co udělá |
|-----|---------|----------|
| Soubor | `@auth.ts` | Přidá soubor jako kontext |
| Složka | `@src/routes/` | Přidá celou složku |
| Terminál | `@terminal:dev` | Zahrne výstup z pojmenovaného terminálu |

> **Tip:** Nemusíte psát celou cestu. Fuzzy matching najde soubor i z části názvu: `@auth` nabídne `src/auth/handler.ts`.

### Výběr kódu + Claude

Označte blok kódu v editoru (myší nebo klávesnicí). Claude ho **automaticky vidí** jako kontext. Stačí napsat:

```
Co dělá tento kód? Má nějaké problémy?
```

Pro přesnější odkaz: označte kód a stiskněte **Alt+K** (macOS: Option+K) — do promptu se vloží @-zmínka s přesnými čísly řádků:
```
@src/auth.ts:42-67
```

### Režimy oprávnění

V dolní části prompt boxu vidíte aktuální režim. Kliknutím nebo Shift+Tab přepnete:
- **Normal** — Claude se ptá před změnami (doporučený)
- **Plan** — Claude jen čte a plánuje
- **Auto-accept** — Claude automaticky edituje soubory

### Více konverzací najednou

Ve VS Code můžete mít **více konverzací** současně:
- Pravý klik na panel → **Open in New Tab** — nová konverzace v záložce
- Pravý klik → **Open in New Window** — nová konverzace v samostatném okně

Každá konverzace má vlastní kontext. Užitečné pro: "v jedné záložce implementuji, ve druhé se ptám na architekturu."

### Historie konverzací

V horní části panelu je dropdown s historií. Můžete:
- Procházet minulé konverzace
- Obnovit a pokračovat v předchozím sezení
- Vyhledávat v historii

### VS Code vs. CLI — kdy co

| Situace | Doporučení |
|---------|------------|
| Editace kódu s review diffů | **VS Code** — vizuální diff je přehlednější |
| Prozkoumávání projektu, dotazy | Obojí funguje stejně |
| Automatizace, skripty, piping | **CLI** — snazší řetězení příkazů |
| Více konverzací paralelně | **VS Code** — více záložek |
| Vzdálený server přes SSH | **CLI** — běží v terminálu |
| Rychlé ad-hoc dotazy | **CLI** — spustíte přímo z terminálu |

> **Zdroj:** [VS Code](https://code.claude.com/docs/en/vs-code)

### Vyzkoušejte

1. Otevřete VS Code se svým projektem
2. Otevřete panel Claude Code (ikona ✦)
3. Napište `@` a začněte psát název souboru — vyberte ho z nabídky
4. Zeptejte se: "Vysvětli, co dělá tento soubor."
5. Označte blok kódu v editoru a zeptejte se: "Má tento kód nějaké problémy?"
6. Požádejte o jednoduchou změnu — prohlédněte si vizuální diff
7. Vyzkoušejte Accept i Reject
8. Zkuste otevřít druhou konverzaci v nové záložce

### Shrnutí
- Panel Claude Code: ikona ✦ nebo Ctrl+Shift+P → "Claude Code"
- @-zmínky pro odkaz na soubory: `@soubor.ts`
- Výběr kódu v editoru → Claude ho automaticky vidí
- Alt+K vloží přesný odkaz na řádky
- Vizuální diff: zelená = přidáno, červená = odebráno, tlačítka Accept/Reject
- Více konverzací: Open in New Tab / New Window

---

## Milník Úrovně 1

Než přejdete na Úroveň 2, ověřte si:

- [ ] **Instalace funguje:** `claude --version` zobrazí číslo verze, VS Code rozšíření je nainstalováno
- [ ] **Umím konverzovat:** Zeptal jsem se Claude na svůj kód a dostal jsem smysluplnou odpověď
- [ ] **Rozumím oprávněním:** Vím, co znamená Allow/Deny dialog, vím o Escape × 2 (rewind)
- [ ] **Znám základní příkazy:** Umím `/help`, `/clear`, `/model`, `/cost`, `/quit`
- [ ] **Provedl jsem úpravu kódu:** Claude upravil soubor, zkontroloval jsem diff a schválil
- [ ] **Vytvořil jsem commit:** Claude vytvořil Git commit s mými změnami
- [ ] **Ovládám VS Code rozšíření:** Umím otevřít panel, @-zmínky, Accept/Reject diff

**Všechny body splněny?** Pokračujte na [Úroveň 2: Produktivní uživatel](./osnova-claude-code.md).

---

> **Zdroje pro tuto úroveň:**
> - [Overview](https://code.claude.com/docs/en/overview) — co je Claude Code
> - [Setup](https://code.claude.com/docs/en/setup) — instalace
> - [Quickstart](https://code.claude.com/docs/en/quickstart) — první kroky
> - [Permissions](https://code.claude.com/docs/en/permissions) — oprávnění
> - [Interactive Mode](https://code.claude.com/docs/en/interactive-mode) — příkazy a zkratky
> - [VS Code](https://code.claude.com/docs/en/vs-code) — rozšíření pro VS Code
> - [How Claude Code Works](https://code.claude.com/docs/en/how-claude-code-works) — jak funguje pod kapotou
> - [Costs](https://code.claude.com/docs/en/costs) — náklady
