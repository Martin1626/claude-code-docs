# Plán přípravy školení — postup po krocích

**Stav k:** 2026-09-09 · každý krok se odsouhlasí a teprve pak dělá.
**Zadání:** série školení Claude Code pro analytiky Alza; první sezení = dvouhodinový úvod (rámec z nahrávky 2026-09-02).

## Rozhodnutí z 2026-09-09 (krok 0 uzavřen)

| Otázka | Rozhodnutí | Dopad na plán |
|---|---|---|
| Datum | **čtvrtek 2026-09-11** — za 2 dny | kroky 1–5 se stlačují do 10. 9.; krok 6 až po sezení |
| Publikum | analytici Alza, většina s vlastním předplatným Claude Code; u klávesnice ~20 % času | malá vlastní cvičení (`/context`, `/usage`, vlastní `history.jsonl`), ne generování |
| Rozsah | **varianta (a)** — fundament + ochutnávka K-01; ontologie a struktura pro specifikace → 2. sezení | program v `PROGRAM-01.md` |
| Tokenizace | **bez API klíče**; ukázka na tiktokenizer.vercel.app | bod 1A **uzavřen jako nepotřebný**; 1B zůstává `[předpoklad]`. ⚠ tiktokenizer = tokenizéry OpenAI, ne Claude — říct nahlas, ukázat princip, ne počty |
| Cvičný repozitář | **nepotřebný** — lektor prezentuje na existujícím projektu Alza, účastníci si spouštějí Claude z lokální pomocné složky | krok 3 **zrušen**; bod 1D (hook `matcher: "compact"`) se netestuje, zůstává „netestováno" |
| Styl | zkušenosti a dobrá praxe, ukázka vlastního prostředí, **bez generování** | scénář = výklad + statické ukázky + čísla; žádná živá kompaktace |
| Zpětná vazba | ano, uvítána | 3 otázky na konci, zápis do `ZPETNA-VAZBA-01.md` |

**Stlačený harmonogram:** 9. 9. program (hotovo: `PROGRAM-01.md`) → 10. 9. deck opravit, výřez `history.jsonl`, tabulka kompaktací, ceník ověřit, zkušební průchod → **11. 9. sezení** → po něm krok 6 a 7.

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
| **A** přesné počty tokenů (CZ/EN věty, `PICK_STATION_A2_LOAD`, cesty, `CLAUDE.md`) | ~~API klíč a `count_tokens`~~ **uzavřeno 9. 9. jako nepotřebné** — ukázka principu na tiktokenizeru, žádné konkrétní počty pro Claude se nevyslovují | — | — |
| **B** znaky/token pro češtinu | **zůstává `[předpoklad]` 3,0** — bez měření se neuzavře; ve F-02 a F-05 tak označeno | vlastní měření (neproběhne) | — |
| **C** Sonnet 5 sdílí tokenizér s Opus 5 | **uzavřeno 9. 9.: ano** — Pricing: „Claude 4.7 and later … newer tokenizer; Sonnet 4.6 and earlier … previous" | platform.claude.com — Pricing | — |
| **D** `SessionStart` hook s `matcher: "compact"` | **netestuje se** (krok 3 zrušen); ve F-04 zůstává „netestováno" | code.claude.com — Hooks | — |
| **E** velikost popisků skillů v mé session | `/context` — uzavře se přímo na sezení jako ukázka v bloku 4 | vlastní měření | na místě |

Po rozhodnutích z 9. 9. **nic z A–E neblokuje sezení.** Zbývá jen hlídat, aby předpoklady B a D byly v decku i scénáři označené jako předpoklad / netestováno.

**Výstup:** aktualizovaná tabulka ve `FUNDAMENT.md`; každý bod buď uzavřen s odkazem, nebo explicitně označen `[předpoklad]` tam, kde se v decku/scénáři používá. **Hotovo, když** v Dílu 1 není jediné neoznačené číslo bez zdroje.

---

## Krok 2 — Opravit a doplnit existující deck

**Vstup:** `C:\Git\shared\docs\claude-code\claude-code-jak-funguje.html` (12 slidů, čteno včetně JS).

**Opravy (nalezené, doložené):**
- slide 02, ř. 311: „≈ 3,5 znaku na token" — **PONECHÁNO a doplněn druhý oficiální odhad ≈ 4 / 0,75 slova.** Ověřeno 9. 9.: glosář Anthropic říká 3,5, Pricing FAQ Anthropic říká 4 — dvě oficiální stránky, dvě čísla → rozsah, ne „oprava". Původní závěr FUNDAMENT „deck má chybu" zrušen (zaznamenáno tam). Doplněny zdroje: +30 % tokenů od Opus 4.7 (Token counting, Pricing), 1 M ≈ 2,5 M znaků Unicode (Models overview). **HOTOVO 9. 9.**
- slide 02: „interaktivní" tokenizér jen dělí předpřipravená pole (`TOK_EN`, `TOK_CZ`) — nahradit odkazem na tiktokenizer.vercel.app **s výhradou, že jde o tokenizéry OpenAI, ne Claude** (Anthropic tokenizér nezveřejňuje); ukázka principu, ne počtů. Je to sama o sobě lekce: hezké demo nemusí měřit, co tvrdí
- slide 06: „až 1 milion tokenů" — ověřit proti aktuálnímu modelu; bod 9 už potvrdil `opus[1m]` = 1 000 000 bez příplatku, jen doplnit datum ověření

**Doplnění (z FUNDAMENT.md — druhá polovina pravdy, kterou deck nemá):**
- bezstavovost ⇒ **kvadratický náklad session**, cena tahu nesouvisí s délkou promptu (doklad z 2 671 promptů)
- kompaktace **zahazuje ~97 %** a dá se **řídit instrukcí** `/compact <co zachovat>` (19 měřených kompaktací)
- **co zabírá místo, než začneš psát** — systémový prompt, popisky skillů, výstupy nástrojů; poměry z měření

**Výstup:** opravený deck + changelog změn na konci souboru (co, proč, zdroj). **Hotovo, když** každé číslo na slidech má buď oficiální odkaz, nebo štítek „vlastní měření, datum", nebo „ilustrace".

---

## Krok 3 — Cvičný repozitář (Díl 0, `N-06`) — **ZRUŠEN 9. 9.**

Lektor prezentuje na existujícím projektu Alza, účastníci mají vlastní Claude Code a spouštějí ho z lokální pomocné složky. Nic se negeneruje, takže „repozitář, který se smí rozbít" není potřeba. Kartu `N-06` v katalogu ponechat — pro případný pozdější díl s živými cvičeními. Původní specifikace níže zůstává jen pro ten případ.

**Proč původně první:** „Bez něj polovina dem nejde předvést." A rozhodnutí 0.4 (čisté vs. moje prostředí) na něm stojí.

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

## Otázky ke kroku 0 — zodpovězeno 9. 9.

Viz tabulka „Rozhodnutí z 2026-09-09" nahoře. Nezodpovězeno zůstává jen **počet účastníků** (ovlivňuje formu zpětné vazby: papír vs. sdílený dokument).

## Co je teď na řadě (10. 9.)

Checklist příprav je v `PROGRAM-01.md`, sekce „Co je potřeba připravit do 10. 9.". Pořadí podle rizika:
1. deck — oprava slidu 02 a 06 (krok 2)
2. předfiltrovaný výřez `history.jsonl` jen z projektu Alza (blok 1) — bezpečnostní, ne kosmetické
3. statická tabulka 19 kompaktací (blok 6)
4. ověření ceníku (blok 5) a záložní screenshoty
5. zkušební průchod nahlas (krok 5)
