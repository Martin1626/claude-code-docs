# Plán přípravy školení — postup po krocích

**Stav k:** 2026-09-09 · **Toto je návrh**, každý krok se odsouhlasí a teprve pak dělá.
**Zadání:** série školení Claude Code pro analytiky Alza; první sezení = dvouhodinový úvod (rámec z nahrávky 2026-09-02).

---

## Zásada zdrojů (platí pro všechny kroky)

Pořadí autority, když se tvrzení liší — stejné pravidlo, jaké nese karta `K-06`:

| Pořadí | Zdroj | Na co |
|---|---|---|
| 1 | **Oficiální dokumentace** — [code.claude.com/docs](https://code.claude.com/docs/en/), [platform.claude.com/docs](https://platform.claude.com/docs/) (ceny, tokeny, prompt caching, `count_tokens`), Anthropic engineering blog | jakékoli tvrzení o chování produktu, cenách, limitech |
| 2 | **Vlastní měření** — `DOKLADY.md`, `_raw/*.py` | naše čísla; vždy označit jako vlastní data, s datem a verzí |
| 3 | **Komunitní materiály** — CCUG přes MCP `claude-code-guide`, awesome-listy | jen křížová kontrola a formátové vzory; **nikdy jako zdroj faktu** |

Pracovní nástroje pro (1): agent `claude-code-guide` (čte oficiální docs), přímý WebFetch na code.claude.com. MCP nástroj `search_official_docs()` je lokální snapshot — před citací ověřit čerstvost (`diff_official_docs`). Co nejde doložit z (1) ani (2), zůstává v textu jako **`[předpoklad]`**, nikdy jako fakt.

---

## Přehled kroků

```
0  Zafixovat rámec 1. sezení  ──┐  (rozhodnutí — tvoje)
                                 ├─► 3  Cvičný repozitář (Díl 0)
1  Uzavřít [K OVĚŘENÍ] A–E  ───┤
                                 ├─► 4  Scénář 1. sezení ──► 5  Zkušební průchod ──► 1. SEZENÍ
2  Opravit existující deck  ────┘                                                        │
                                                                                         ▼
6  Zapracovat nálezy z POROVNANI do katalogu (Díl 2, karta „skill/subagent/MCP/hook", pole karet)
7  Po sezení: zpětná vazba → korekce → další díl (opakuje se 4 → 5 pro každý díl)
```

Kroky 0, 1, 2 jsou na sebe nezávislé a dají se dělat souběžně. Krok 4 na nich všech stojí.

**Hned, mimo pořadí:** `workshop-namety/` je celý untracked. Commitnout dřív, než se do něj sáhne.

---

## Krok 0 — Zafixovat rámec 1. sezení

**Typ:** rozhodnutí, ne práce. Bez něj se nedá psát scénář.

**Co je potřeba rozhodnout:**

1. **Datum a délka** — nahrávka říká „zhruba dvě hodiny". Čistý obsah 90 min + Q&A 20 + rezerva 10?
2. **Publikum** — kolik analytiků, mají už Claude Code nainstalovaný a licenci? Můžou během sezení něco spustit sami, nebo je to čistě demo z plátna?
3. **Rozpor rozsahu.** Nahrávka (2026-09-02) chce v 1. sezení: LLM základy + harness + účtování/cache **+ struktura projektu + velké soubory + ontologie prvků + Q&A**, a sama říká, že ontologie je „téma na celé první sezení". NAMETY (2026-08-26) má Díl 1 = 79 min čistého fundamentu (`F-01`–`F-05`, `N-05`) a ontologii (`K-05`, `K-06`) odsouvá do přílohy `P` jako „bez postavené infrastruktury si z toho kolega odnese jen cíl". **Obojí do dvou hodin nejde.** Tři možnosti:
   - **(a)** 1. sezení = Díl 1 (fundament) + ochutnávka struktury projektu (`K-01`, 20 min); ontologie samostatně později
   - **(b)** 1. sezení = fundament zkrácený na 45 min (deck už existuje) + struktura projektu + ontologie jako výklad bez nástrojů
   - **(c)** dvě úvodní sezení místo jednoho
4. **Prostředí dema** — moje session s mými pluginy a 23 KB `CLAUDE.md`, nebo čistá instalace na cvičném repozitáři (krok 3)? Čistá je poctivější k publiku, které moje věci nemá; moje ukazuje víc.

**Výstup:** `PROGRAM-01.md` — bloky, minuty, kdo co dělá (výklad / demo / cvičení / Q&A). **Hotovo, když** součet minut sedí a každý blok má odkaz na kartu v NAMETY.

---

## Krok 1 — Uzavřít otevřené `[K OVĚŘENÍ]` A–E

**Vstup:** `FUNDAMENT.md`, sekce „Stav bodů `[K OVĚŘENÍ]`" — deset uzavřených, pět otevřených.

| Bod | Co je potřeba | Zdroj pravdy | Kdo |
|---|---|---|---|
| **A** přesné počty tokenů (CZ/EN věty, `PICK_STATION_A2_LOAD`, cesty, `CLAUDE.md`) | API klíč a volání `count_tokens` s `claude-opus-5` | platform.claude.com — Token counting | **ty:** klíč; **já:** skript a měření |
| **B** znaky/token pro češtinu | plyne z A; do té doby 3,0 zůstává `[předpoklad]` | vlastní měření | já |
| **C** Sonnet 5 sdílí tokenizér s Opus 5 | ověřit v docs; nízký dopad | platform.claude.com — Models | já |
| **D** `SessionStart` hook s `matcher: "compact"` | otestovat na cvičném repu (krok 3) | code.claude.com — Hooks + vlastní test | já |
| **E** velikost popisků skillů v mé session | `/context` — uzavře se přímo na sezení jako demo 3a | vlastní měření | na místě |

**A je jediný, který blokuje demo** (F-02 „Čeština není dražší, protože je delší"). Bez něj musí F-02 skončit u měřených znaků. Rozhodnutí: seženeš klíč, nebo F-02 přepíšeme na „znaky" variantu?

**Výstup:** aktualizovaná tabulka ve `FUNDAMENT.md`; každý bod buď uzavřen s odkazem, nebo explicitně označen `[předpoklad]` tam, kde se v decku/scénáři používá. **Hotovo, když** v Dílu 1 není jediné neoznačené číslo bez zdroje.

---

## Krok 2 — Opravit a doplnit existující deck

**Vstup:** `C:\Git\shared\docs\claude-code\claude-code-jak-funguje.html` (12 slidů, čteno včetně JS).

**Opravy (nalezené, doložené):**
- slide 02, ř. 311: „≈ 3,5 znaku na token" → **4** (doslovná citace FAQ Anthropic); doplnit odkaz na konkrétní stránku
- slide 02: „interaktivní" tokenizér jen dělí předpřipravená pole (`TOK_EN`, `TOK_CZ`) — buď nahradit skutečnými čísly z kroku 1A, nebo nadpis změnit na „ilustrace" a říct to publiku nahlas (je to sama o sobě lekce: hezké demo nemusí měřit, co tvrdí)
- slide 06: „až 1 milion tokenů" — ověřit proti aktuálnímu modelu; bod 9 už potvrdil `opus[1m]` = 1 000 000 bez příplatku, jen doplnit datum ověření

**Doplnění (z FUNDAMENT.md — druhá polovina pravdy, kterou deck nemá):**
- bezstavovost ⇒ **kvadratický náklad session**, cena tahu nesouvisí s délkou promptu (doklad z 2 671 promptů)
- kompaktace **zahazuje ~97 %** a dá se **řídit instrukcí** `/compact <co zachovat>` (19 měřených kompaktací)
- **co zabírá místo, než začneš psát** — systémový prompt, popisky skillů, výstupy nástrojů; poměry z měření

**Výstup:** opravený deck + changelog změn na konci souboru (co, proč, zdroj). **Hotovo, když** každé číslo na slidech má buď oficiální odkaz, nebo štítek „vlastní měření, datum", nebo „ilustrace".

---

## Krok 3 — Cvičný repozitář (Díl 0, `N-06`)

**Proč první:** „Bez něj polovina dem nejde předvést." A rozhodnutí 0.4 (čisté vs. moje prostředí) na něm stojí.

**Co v něm musí být, aby fungovala dema Dílu 1:**
- `CLAUDE.md` s krátkou, čitelnou instrukcí (ne 23 KB) — demo `F-01`, `F-05`
- pár dokumentů různé velikosti (jeden nad 1 000 řádků) — demo „agent nečte celé soubory"
- `.claude/settings.json` s třemi zákazy (`N-01`) — připraveno i pro Díl 2
- jeden hook `SessionStart` s `matcher: "compact"` — uzavře bod 1D
- žádná data Alzy ani KVADOS; anonymizovaná doména (sklad? e-shop katalog?) — musí být bezpečné ho rozbít a sdílet

**Výstup:** repozitář (kde? nový pod `C:\Git\`? nebo v tomto repu jako `cvicny-repo/`?), s `README` „jak ho použít na sezení". **Hotovo, když** na čisté instalaci Claude Code proběhnou všechna dema Dílu 1 podle scénáře z kroku 4.

---

## Krok 4 — Scénář 1. sezení

**Vstup:** `PROGRAM-01.md` (krok 0), karty NAMETY pro vybrané náměty, opravený deck, cvičný repo.

**Formát bloku** — naše karta + dvě pole převzatá z formátu CCUG (jen formát, ne obsah):

```
## Blok N — <název karty>                          <min> · <role>
Co říct       — 3–5 vět, kostra výkladu
Co ukázat     — přesný postup dema: příkaz, soubor, na co ukázat na obrazovce
Číslo/doklad  — s odkazem (oficiální docs / DOKLADY.md / [předpoklad])
Ověřitelný výstup — podle čeho účastník pozná, že to pochopil / umí
Kam dál       — jeden odkaz do oficiální dokumentace
Když demo selže — záložní screenshot / co říct místo něj
```

**Výstup:** `SCENAR-01.md`. **Hotovo, když** každý blok má všech sedm polí a součet minut = program.

---

## Krok 5 — Zkušební průchod a revize

- **Časování:** projít nahlas s hodinkami; každý blok, který přeteče o >20 %, škrtnout nebo zkrátit (ne zrychlit)
- **Zdrojová revize:** každé tvrzení ve scénáři → oficiální odkaz / vlastní měření / `[předpoklad]`; co nemá nic, ven. Tohle bych udělal jako oddělený adversariální průchod, stejně jako u katalogu — najde, co autor už nevidí
- **Technická zkouška** dem na cvičném repu, na tom stroji a s tou verzí Claude Code, která bude na sezení (`claude --version` do scénáře)
- **Záložní plán** pro každé demo (screenshot, nebo výklad bez dema)

**Výstup:** `SCENAR-01.md` v2 + seznam škrtů. **Hotovo, když** průchod skončí do času a revize nemá otevřený nález.

---

## Krok 6 — Zapracovat nálezy z `POROVNANI-CCUG.md` do katalogu

Netýká se 1. sezení, ale série. Tři věci, každá samostatně:

1. **Díl 2** — název „Než pustíš agenta na svá data" slibuje datovou hranici, obsah řeší bezpečnost změn. Doplnit 2–3 náměty: kam data tečou ([Data Usage](https://code.claude.com/docs/en/data-usage)), co dělá a nedělá sandbox ([Sandboxing](https://code.claude.com/docs/en/sandboxing)), prompt injection ([Security](https://code.claude.com/docs/en/security)). Prostor je: díl má 51 min.
2. **Nová karta do Dílu 9** — „Skill, subagent, MCP, nebo hook?" s rozhodovacím kritériem. Zdroj: oficiální stránky Skills / Subagents / MCP / Hooks; kritérium formulovat vlastními slovy.
3. **Pole `Ověřitelný výstup` + `Kam dál`** do všech 56 karet. Práce na jeden večer; dá se dělat po dílech, jak přicházejí na řadu.

**Hotovo, když** `NAMETY.md` má aktualizovanou souhrnnou tabulku a součty přepočítané skriptem (`_raw/n5-bloky.py`), ne ručně.

---

## Krok 7 — Po každém sezení

1. Zápis Q&A a co lidé řekli o vlastní praxi → `ZPETNA-VAZBA-NN.md`
2. Co se nepovedlo (demo, časování, otázka bez odpovědi) → korekce karty nebo `[K OVĚŘENÍ]`
3. Výběr dalšího dílu podle střihu (3 / 5 / 10 dílů) a podle toho, na co se ptali
4. Krok 4 → 5 pro další díl

---

## Co potřebuji od tebe, abychom mohli začít

Krok 0 je celý tvůj. Konkrétně:

- **datum 1. sezení** a počet lidí
- **mají účastníci Claude Code** (instalace + licence), nebo je sezení čisté demo?
- **rozsah:** varianta (a), (b), nebo (c) výše?
- **API klíč** pro `count_tokens` (bod 1A) — seženeš, nebo F-02 přepíšeme na variantu bez přesných tokenů?
- **kde má žít cvičný repozitář** (krok 3)

Kroky 1C, 1D, 2 a přípravu skriptu pro 1A můžu začít hned, nezávisle na odpovědích.
