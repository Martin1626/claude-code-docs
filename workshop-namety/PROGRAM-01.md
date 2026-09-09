# Program 1. sezení — „Co se pod tím děje a co tě to stojí"

**Kdy:** čtvrtek **2026-09-11** · **Délka:** 120 min · **Publikum:** analytici Alza, většina s vlastním předplatným Claude Code
**Varianta rozsahu:** (a) — fundament (Díl 1 z NAMETY) + ochutnávka „dokument nese kontext" (K-01) · ontologie prvků a struktura pro specifikace → další sezení
**Styl:** výklad a zkušenost z praxe, ukázka mého pracovního prostředí (projekt Alza) **bez generování**; účastníci si ~20 % času zkouší jednoduché věci ve vlastním Claude Code
**Stav:** návrh k odsouhlasení · **Navazuje:** `PLAN.md` krok 0 · karty: `NAMETY.md` okruh F, N-05, K-01 · výklad: `FUNDAMENT.md` · čísla: `DOKLADY.md`

---

## Co si mají odnést (jedna věta na blok, vyslovit na konci)

1. Model si nic nepamatuje — celá historie se posílá znovu, proto dlouhá session zdražuje každý další prompt.
2. Platí se za tokeny, ne za slova; čeština se seká na víc kousků — šetři v souborech, které jdou pokaždé, ne v promptu.
3. Nástroj kolem modelu (harness) dělá práci; model jen píše, co udělat.
4. V okně je spousta věcí, které tam nikdo vědomě nedal — `/context` to ukáže za pár sekund.
5. Kompaktace zahodí ~97 % a dá se jí říct, co má nechat. `/clear` je zdarma, `/compact` ne.
6. **Dokument nese kontext, prompt nese rozhodnutí** — krátké prompty fungují jen nad postaveným kontextem.

---

## Časový plán

| # | Čas | Min | Blok | Karta | Role | Účastníci si zkusí |
|---|---|---|---|---|---|---|
| 0 | 0:00 | 5 | Úvod: kdo jsem, co dnes je a co není, jak budeme pracovat | — | výklad | — |
| 1 | 0:05 | 15 | **Claude si tě nepamatuje. Vede si o tebe složku.** | F-01 | výklad + ukázka | otevřít vlastní `~/.claude/history.jsonl` a `~/.claude/projects/` (3 min) |
| 2 | 0:20 | 10 | **Tokeny: čeština není dražší, protože je delší** | F-02 | výklad + ukázka | vložit vlastní větu CZ/EN do tiktokenizeru (3 min) |
| 3 | 0:30 | 8 | **Harness: model píše, nástroje dělají** — sessions, turns, agentní smyčka | deck 08–11 | výklad | — |
| 4 | 0:38 | 15 | **Co tě stojí místo, o kterém nevíš** | F-05 | výklad + ukázka | `/context` ve vlastní session (4 min) |
| 5 | 0:53 | 7 | **Co to stojí a jak to zjistíš** | N-05 | výklad + ukázka | `/usage` (2 min) |
| — | 1:00 | 5 | *pauza* | | | |
| 6 | 1:05 | 12 | **Tomu shrnutí můžeš říct, co má zachovat** | F-03 | výklad | — |
| 7 | 1:17 | 8 | **Padesát jedna ku jedné** | F-04 | příběh | — |
| 8 | 1:25 | 20 | **Dokument nese kontext, prompt nese rozhodnutí** + jak vypadá moje prostředí | K-01 | výklad + ukázka | podívat se, zda mají ve svém projektu `CLAUDE.md` a co v něm je (3 min) |
| 9 | 1:45 | 15 | **Q&A, sdílení zkušeností, zpětná vazba** | — | diskuse | zpětná vazba (3 otázky) |
| | 2:00 | | konec | | | |

**Součet:** 5 + 15 + 10 + 8 + 15 + 7 + 5 + 12 + 8 + 20 + 15 = **120 min.**
**Čas účastníků u klávesnice:** 3 + 3 + 4 + 2 + 3 = 15 min + Q&A 15 = 30 min ≈ **25 %.** Bez Q&A 12,5 % — pokud chceš víc, prodluž blok 4 (`/context` je nejcennější věc, kterou si odnesou).

---

## Bloky podrobně

### 0 · Úvod (5 min)
- Kdo jsem, z čeho čerpám: 7 měsíců, 2 671 promptů, 4 pracovní projekty — **vlastní data, ne teorie**.
- Co dnes **není**: návod „jak napsat prompt", ontologie prvků, struktura pro specifikace (příště).
- Jak pracujeme: já ukazuji své prostředí, vy si u sebe zkoušíte pět malých věcí. Nic negenerujeme.
- Zdroje: kde říkám číslo, je buď z oficiální dokumentace (řeknu odkud), nebo z mých dat (řeknu jak měřeno), nebo je to odhad (řeknu to).

### 1 · Claude si tě nepamatuje (F-01, 15 min)
- **Výklad:** model = funkce text → text, mezi voláními nic. „Paměť" vytváří okolí tím, že posílá celou historii znovu. Důsledek: „už jsem ti to říkal" není argument; každý další prompt v dlouhé session stojí víc než předchozí, i když je kratší.
- **Ukázka (moje prostředí):** `~/.claude/history.jsonl` — řada JSON řádků na mém disku; adresář transkriptů projektu Alza. Slide 01 decku (model jako automat na text).
- **Účastníci:** otevřou si vlastní `history.jsonl`. Vidí, že jejich konverzace je soubor u nich na disku.
- **Číslo:** 2 671 promptů (vlastní data k 2026-08-26).
- **Výhrada:** nesklouznout k „model je hloupý" — bezstavovost je vlastnost, díky které funguje `/resume` i subagent.
- ⚠ **Před sezením:** `history.jsonl` obsahuje prompty ze **všech** projektů včetně jiných klientů (fhb, myfaber) a přinejmenším jeden s přístupovým tokenem (N-04). Neotvírat naživo celý soubor — ukázat **předfiltrovaný výřez** jen z projektu Alza, nebo screenshot.

### 2 · Tokeny (F-02, 10 min)
- **Výklad:** model nevidí písmena ani slova, ale tokeny; platí se za ně a plní kontext. Čeština s diakritikou se seká na víc kousků → tatáž informace stojí víc tokenů. Praktický důsledek: šetři v tom, co jde pokaždé (`CLAUDE.md`, pravidla), ne v promptu napsaném jednou.
- **Ukázka:** [tiktokenizer.vercel.app](https://tiktokenizer.vercel.app/) — tatáž věta česky a anglicky, vidět rozpad na tokeny a rozdíl v počtu.
- **Účastníci:** vloží vlastní větu.
- ⚠ **Nutné říct nahlas:** tiktokenizer používá **tokenizéry OpenAI (tiktoken, výchozí gpt-4o), ne Claude**. Anthropic svůj tokenizér nezveřejňuje (ověřeno, negativní nález). Ukázka tedy předvádí **princip** — jak se text seká a že čeština se seká víc — **ne konkrétní počty pro Claude**. Vlastní karta F-02 dokumentuje, že tiktoken vůči Claude podhodnocuje o 15–20 %, „mnohem víc na neanglickém vstupu". Nevyslovovat žádné „česká věta má v Claude N tokenů".
- **Čísla, která lze říct (ověřeno 9. 9. 2026 v oficiální dokumentaci):** pro angličtinu **≈ 3,5 znaku/token** ([glosář](https://platform.claude.com/docs/en/about-claude/glossary)) **až ≈ 4 znaky / 0,75 slova** ([Pricing FAQ](https://platform.claude.com/docs/en/about-claude/pricing)) — **dvě oficiální stránky Anthropic, dvě čísla; uvádět rozsah**; tokenizér od Opus 4.7 — tedy i Opus 5 a Sonnet 5 (Sonnet 4.6 a starší mají předchozí) — dává na tomtéž textu **≈ 30 % víc tokenů** ([Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting), Pricing); **1 M tokenů ≈ 555 tis. slov / 2,5 M znaků Unicode** na aktuálním tokenizéru ([Models overview](https://platform.claude.com/docs/en/models/overview)). Pro češtinu **žádné oficiální číslo neexistuje** — říct to jako fakt, je to sama o sobě informace.
- ⚠ **Oprava vlastní přípravy:** FUNDAMENT.md tvrdil, že deck má na slidu 02 chybu (3,5 místo 4). **Nemá** — obě čísla jsou oficiální, každé na jiné stránce Anthropic. Správně je rozsah, jak říká karta F-02. Dobrá ilustrace pro publikum: **i oficiální dokumentace si na dvou stránkách odporuje** — proto se citace ověřuje, nevěří (K-05), a proto rozsah místo jednoho čísla.
- ⚠ Tvrzení „tiktoken podhodnocuje o 15–20 %" nemá dohledaný oficiální zdroj — **nevyslovovat s číslem**; stačí „tiktokenizer používá tokenizéry OpenAI, ne Claude, ukazuje princip".

### 3 · Harness (deck 08–11, 8 min)
- **Výklad:** model vs. harness (mozek bez rukou / ruce); nástroje jako dohodnutý JSON (`tool_use` → `tool_result`); agentní smyčka: harness → model → harness provede → výsledek zpět → model rozhodne → opakuj. Pojmy **session** (celá relace) a **turn** (jedna výměna).
- **Ukázka:** slidy 08–11 existujícího decku; v mém terminálu ukázat, jak vypadá jeden turn s voláním nástroje (na hotovém transkriptu, ne živě).
- **Zdroj:** deck je ověřený; čísla cache na slidu 06 souhlasí s dokumentací.

### 4 · Co tě stojí místo, o kterém nevíš (F-05, 15 min)
- **Výklad:** v okně je systémový prompt, definice nástrojů, popisky všech skillů, `CLAUDE.md`, paměti — všechno **znovu s každým promptem**. Cache zlevní na desetinu ceny, ale **místo v okně zabírá pořád** — cache snižuje cenu za token, ne počet tokenů.
- **Ukázka:** `/context` naživo v mé session projektu Alza — rozpad zaplnění po složkách. Jediné skutečné měření, které mám, a je okamžité.
- **Účastníci:** `/context` u sebe. Porovnat: kolik mají zaplněno, než napsali první slovo.
- **Čísla:** dokumentace uvádí ilustrativně projektový `CLAUDE.md` ≈ 1 800 tokenů; můj má 23 427 znaků → odhadem ~7 800 tokenů (**přepočet 3,0 znaku/token je předpoklad**, říct to). Formulace: „**minimálně** 13 000 tokenů, než napíšu první slovo — a to je jen to, co si můžu změřit ze souborů".

### 5 · Co to stojí (N-05, 7 min)
- **Výklad:** tři složky ceny: vstup (roste s délkou session), výstup (dražší, méně), cache (čtení za desetinu, zápis dráž). Dlouhý kontext bez cenového příplatku.
- **Ukázka:** `/usage`; oficiální ceník na obrazovce ([platform.claude.com — Pricing](https://platform.claude.com/docs/en/about-claude/pricing)) — **ceny ověřit 10.9., ne říkat z hlavy**.
- **Účastníci:** `/usage`.
- **Přiznat:** kolik mě 7 měsíců stálo, nevím — nesbíral jsem to. Poučení: „nezkoumej ceník, změř si to".

### 6 · Kompaktace (F-03, 12 min)
- **Výklad:** když se okno plní, starší část se shrne — nevratná ztráta neznámé části. Zůstane záměr a rozhodnutí, zmizí doslovné výstupy nástrojů, čísla řádků, přesné citace. Analytik opřený o `soubor:řádek` pak pracuje s vyprávěním o zdroji. **A:** `/compact` přijímá instrukci — `/compact zachovej rozhodnutí o pojmenování a čísla řádků u citací`.
- **Ukázka:** **statická tabulka** 19 kompaktací (`preTokens` → `postTokens`) z `DOKLADY.md` část 2. Ne živě.
- **Čísla:** medián **97,3 %** zahozeno; **0 z 19** mělo instrukci. Popisky skillů se po kompaktaci nenačtou znovu (dokumentováno).
- ⚠ Živou kompaktaci nepředvádět (medián 181 s, zabije session).

### 7 · Padesát jedna ku jedné (F-04, 8 min)
- **Příběh:** `/compact` 51× vs. `/clear` 1×. `/clear` neposílá request — je zdarma; `/compact` posílá celou historii. 8,6 mil. tokenů zahozeno; 19 z 19 kompaktací ručních, nikdy strop — zasahoval jsem sám při mediánu ~46 % okna.
- **Na tabuli:** **51 / 1 / 8 600 000.**
- **Podání:** přiznání vlastní chyby, ne best practice.

### 8 · Dokument nese kontext, prompt nese rozhodnutí (K-01, 20 min)
- **Výklad:** medián mého promptu 65 znaků, nad 1 000 znaků 2 %. Vypadá to jako „piš krátce" — znamená to, že **kontext leží v souborech**. Nejdelší prompt měsíce (2 106 znaků) nese 15 odpovědí a ani jednu otázku; otázky žijí v `BACKLOG.md`.
- **Ukázka mého prostředí (projekt Alza):** vedle sebe ten prompt a `BACKLOG.md`; pak struktura: kde je `CLAUDE.md`, `.claude/` (pravidla, settings, skills), kde leží dokumenty, které Claude čte. Odpovídá bodu „struktura projektového adresáře" z nahrávky 2026-09-02.
- **Účastníci:** mají ve svém projektu `CLAUDE.md`? Co v něm je? (3 min)
- **Výhrada — říct nahlas:** funguje to jen tam, kde ten dokument někdo vede. Pro kolegu bez backlogu je první krok „**založ si soubor**", ne „piš krátce". Kdo si odnese jen „krátké prompty", dostane špatný výsledek.
- **Most k příštímu sezení:** jak ty soubory strukturovat pro specifikace a analýzy, ontologie prvků, precedence zdrojů.

### 9 · Q&A + zpětná vazba (15 min)
- Otevřené otázky, vlastní zkušenosti účastníků.
- **Zpětná vazba — tři otázky** (papír / sdílený dokument / krátký formulář):
  1. Co jedno si odnášíš a použiješ zítra?
  2. Co bylo nejméně jasné?
  3. Co chceš příště: struktura souborů pro specifikace / ontologie prvků / bezpečné pouštění agenta na data / jiné?
- Odpovědi → `ZPETNA-VAZBA-01.md` (krok 7 v PLAN.md).

---

## Co je potřeba připravit do 10. 9. (checklist)

- [x] **Předfiltrovaný výřez `history.jsonl`** jen z projektu Alza (blok 1) → `vyrez-history-2026-08-19.jsonl` (14 řádků, session se 4× `/compact`) + `vyrez-history-2026-07-09-K01.txt` (blok 8); popis a kontrola citlivého obsahu ve `VYREZ-HISTORY.md`
- [x] **Statická tabulka 19 kompaktací** (blok 6) → `slide-kompaktace.html` + `slide-kompaktace.png` (záložní obrázek); čísla přepočítána proti `DOKLADY.md`
- [x] **Deck** (`C:\Git\shared\docs\claude-code\claude-code-jak-funguje.html`, lokálně upraveno 9. 9., **necommitováno, nepushováno — GitLab**): slide 02 = rozsah 3,5 (glosář) až 4 / 0,75 slova (Pricing FAQ) + „+30 % od Opus 4.7" + „1 M ≈ 2,5 M znaků" + falešný poměr skryt, štítek „ilustrace, ne měření", odkaz na tiktokenizer s výhradou; slide 06 = konkrétní modely + datum ověření; changelog se zdroji na konci souboru. Záloha originálu v `$CLAUDE_JOB_DIR/tmp/deck-backup.html`
- [x] **Ceník** ověřen 9. 9. 2026 na [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing): Opus 5 **$5 / $25** za MTok (vstup / výstup), cache čtení $0,50 (0,1×), cache zápis 5 min $6,25 (1,25×), 1 h $10 (2×); Sonnet 5 $2 / $10 (od 1. 9. 2026 standardní cena, ne zaváděcí); Haiku 4.5 $1 / $5. Dlouhý kontext bez příplatku („900k-token request is billed at the same per-token rate as a 9k-token request"). Čísla v kartě N-05 sedí. **Znovu zkontrolovat 10. 9.** (stránka se mění)
- [x] **Věty do tiktokenizeru** → `tiktokenizer-vety.md`: 5 vložení v pořadí, s předpočítanými počty (tiktoken `o200k_base` = gpt-4o, výchozí model tiktokenizeru), rozpady, zadání pro účastníky, „co neříkat", záloha bez sítě. Klíčový pár: EN 53 znaků = 8 tokenů, CZ 47 znaků = **18** tokenů
- [ ] **Session projektu Alza** rozjetá před sezením, aby `/context` ukázal reálný stav (blok 4) — zkontrolovat, že v ní není nic, co nemá být na plátně
- [ ] **Záložní screenshoty** pro `/context`, `/usage`, tiktokenizer — kdyby síť nebo terminál
- [x] **Formulář zpětné vazby** → `zpetna-vazba-formular.html` + `zpetna-vazba-formular.pdf` (A4, 1 strana, tisk): řádek „používám: ne / < měsíc / > měsíc" + 3 otázky (Q3 = zaškrtávací témata dalších dílů + poznámka). Pro online variantu stačí tytéž otázky přepsat do MS Forms. **Vytisknout podle počtu lidí + 3 rezervní**
- [ ] **`claude --version`** na prezentačním stroji zapsat do scénáře
- [ ] **Zkušební průchod nahlas s hodinkami** (10. 9.) — blok, který přeteče o >20 %, škrtnout, ne zrychlit

## Co záměrně vypadlo a kam patří

| Vypadlo | Proč | Kam |
|---|---|---|
| Ontologie prvků, precedence zdrojů (K-05, K-06) | varianta (a); bez infrastruktury jen cíl | 2. sezení |
| Struktura souborů pro specifikace a analýzy, Markdown | navazující téma z nahrávky | 2. sezení |
| Tři zákazy, rewind, plan mode (N-01–N-03), „nic neměň" (M-02) | Díl 2 | 2. nebo 3. sezení podle zpětné vazby |
| Prompt je zápis, ne rozhovor (N-04) — tokeny v promptech, klientská data | silné, ale patří k datové hranici (Díl 2) | 2. sezení — **zvážit přesun sem, pokud Q&A ukáže zájem o bezpečnost** |
| Cvičný repozitář (N-06) | nepotřebný — účastníci mají vlastní Claude Code, já prezentuji na projektu Alza | zrušeno |
