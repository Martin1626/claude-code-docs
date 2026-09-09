# FÁZE 5 — RED-TEAM draftu katalogu

Cíl: rozbít `katalog-draft.md`, ne ho vylepšit. Každý nález má doklad a AKCI.
Nálezy bez akce jsem zahodil sám.

Ověřovací skripty psané pro tento red-team (v `C:\tmp\workshop-namety\_raw\`):
`rt_absence.py`, `rt_absence2.py`, `rt_kompaktace.py`, `rt_bloky.py`, `rt_history.py`.
Do žádného repozitáře nebylo zapsáno.

**Souhrn: 42 nálezů** — 15 „neosvědčilo se / osobní zvyk / infra" (9+4+2), 11 „chybí",
8 „nepředveditelné", 6 „vadný doklad", 2 o draftu jako celku (RT-01, RT-42).
Každý nález má AKCI (42/42).

**Pět nejtvrdších:** RT-35 (pravidlo „brána, ne prompt" nemá v projektu bránu — CI nespouští
nic, hooky nejsou nainstalované) · RT-14 (vlajkové číslo bloku 1 nadhodnocené o 36 %,
21 kompaktací jsou 19) · RT-01 (okruh `X` je osa, ne téma — 9 duplikátů, −90 min) ·
RT-02 (čtvrtina `CLAUDE.md` nespuštěná ani jednou za 2 678 promptů) · RT-20 (nula zásahů
na citlivá data v korpusu zákazníkových dokumentů, a přitom 4 zveřejněné tokeny).

---

## 0. Nález o draftu jako celku

### RT-01 — Okruh `X` není téma, je to osa. Proto se draft sám duplikuje.
**Typ:** jiné (taxonomická vada)
**Terč:** draft jako celek (okruh `X`, 12 námětů, 121 minut)
**Nález:** Osm okruhů (`F N K R M O A U`) jsou **témata**, `X` je **polarita** (antipattern vs.
praxe). Míchání osy do taxonomie témat vyrábí systematické dvojče: 9 z 12 `X` námětů je
negativní verze existující pozitivní položky, často i s explicitní `dep` na ni:

| `X` námět | je negativní dvojče | poznámka |
|---|---|---|
| X-02 Dlouhý prompt se ořízne | R-01 Prompt do souboru | `dep: R-01` — je to jeho doklad |
| X-03 Autonomní smyčka revize | M-05 Triáž dělá člověk | `dep: M-05` |
| X-04 Iluze pokrytí | M-04 Vykazuj, co jsi NEzkontroloval | tatáž věta obráceně |
| X-06 Artefakt, na který nic neukazuje | R-02 Metodika bez spouštěče | `dep: R-02`, tatáž lekce |
| X-07 Konvence bez validátoru | M-01 Brána, ne prompt | `dep: M-01` |
| X-08 Vrstva pravidel, která neexistuje | K-08 `CLAUDE.md` driftuje | `dep: K-08`, instance téhož |
| X-11 Nástroj kontroluje jen to, co pozná | M-07 + M-04 | tři položky, jedna myšlenka |
| X-12 Ladění modelu bez baseline | O-02 Volba modelu | `dep: O-02` |
| X-05 Ladění screenshoty | A-07 + A-08 | `dep: A-08` |

Zbytek programu je pak nutně přednáška: **21 námětů má roli „příběh", jen 7 z 66 má cvičení**
(`rt_bloky.py`: role „příběh" 13× samostatně + 8× v kombinaci; cvičení K-02, K-03, R-01,
M-02, A-01, A-02, U-01). Publikum, které Claude Code už používá, potřebuje postup a cvik,
ne dvacet jedna historek.
**Doklad:** `rt_bloky.py` výstup — 66 položek, okruhy `{X:12, A:11, M:10, K:8, R:6, F:5, O:5, U:5, N:4}`;
`dep` sloupec v `katalog-draft.md:36–101` (osm `X` položek má `dep` mířící na svého pozitivního dvojčete).
**AKCE:** `vyřadit` okruh `X` jako kategorii. Každý antipattern se stane sekcí „doklad / jak to
selže" **uvnitř** své pozitivní položky (X-02→R-01, X-03→M-05, X-04→M-04, X-06→R-02, X-07→M-01,
X-08→K-08, X-11→M-07, X-12→O-02, X-05→A-08). Samostatně zůstanou jen X-01 (tokeny v chatu —
nemá pozitivní dvojče) a X-10 (regenerace přepíše člověka). X-09 („slepé pokračuj", 5 min,
could) `vyřadit`. Úspora: **9 slotů, ~90 minut**, a poměr cvičení k příběhům se zlepší bez
přidání jediné minuty.

---

## 1. Neosvědčilo se / osobní zvyk / infra (návrhy na vyřazení)

### RT-02 — Celý „Projektový asistent" v `CLAUDE.md` nebyl za 2678 promptů spuštěn ani jednou
**Typ:** neosvědčilo se
**Terč:** K-08, F-05 (a nepřímo R-03, R-06)
**Nález:** `CLAUDE.md` alzask má sekci „Projektový asistent" s režimy UČENÍ/DOHLEDÁNÍ a čtyřmi
příkazy (`/project:learn`, `/project:lookup`, `/project:overview`, `/project:glossary`), ke
kterým existují 4 skilly a 4 soubory v `.claude/commands/`. **Použití: 0×.** Sekce má 3 031
znaků = 12,7 % `CLAUDE.md`, tedy ~1 000 tokenů, které se posílají s **každým** tahem každé
session od dubna. To je nejlepší možný exponát pro K-08 i F-05 — vlastní soubor autora.
**Doklad:** `rt_history.py` nad `~/.claude/history.jsonl` (2 678 promptů):
`/learn 0`, `/lookup 0`, `/overview 0`, `/glossary 0`, `/project: 0`.
Velikost: `C:\Git\alzask\CLAUDE.md` 23 818 znaků, sekce od indexu 20 787 → 3 031 znaků (12,7 %).
**AKCE:** `přeformulovat na` exponát K-08: „ukážu ti čtvrtinu vlastního `CLAUDE.md`, kterou
platím každým promptem a nespustil jsem ji ani jednou." Zároveň `doplnit chybějící` krok do
K-08: **jak drift najít** — `grep` počtu invokací v `history.jsonl` proti seznamu vlastních
příkazů (10 řádků Pythonu, zcela přenositelné).

### RT-03 — Pětiagentní revizní pipeline: postavená, nikdy nespuštěná
**Typ:** neosvědčilo se
**Terč:** M-05, M-06, X-03, O-01
**Nález:** `C:\Git\alzask\.claude\agents\` obsahuje 5 agentů (`review-design`, `review-semantic`,
`review-structural`, `review-fixer`, `review-reporter`) s explicitními `model:` overridy a
`maxTurns`, a příkaz `/review-docs`. **`/review-docs` 0× za celou historii; jméno žádného
z pěti agentů se v 2 678 promptech nevyskytuje ani jednou.** Draft z této pipeline odvozuje
čtyři náměty, z toho dva `must` (M-05, X-03). Doklad o precision 21–31 % je navíc **externí
měření**, ne měření této pipeline.
**Doklad:** `rt_history.py`: `/review-docs 0 / 0`; „zmínky review-* agentů v textu promptu
(pracovní): 0". Definice agentů: `C:\Git\alzask\.claude\agents\` (5 souborů, viz `faze1-inventar.md`
sekce 3). Precision: `katalog-draft.md:120` — „~21–31 % (externí měření)".
**AKCE:** `přeformulovat na` „postavil jsem revizní pipeline a nikdy ji nespustil — proč"
a **snížit prioritu** M-05 a X-03 z `must` na `should`. Lekce, kterou data nesou, není
„triáž dělá člověk", ale **„nástroj bez místa ve rutině se nepoužije"** — což je R-02/X-06,
už v draftu je, a tohle je jeho nejsilnější doklad.

### RT-04 — Znalostní smyčka: 93 % zachyceného nikdy nikdo nepřečte, povýšení 0 za 47 dní
**Typ:** neosvědčilo se
**Terč:** U-02, M-10
**Nález:** Draft ví o „5 z ~63, všech 5 v prvních 6 dnech". Skutečnost je horší ve třech dalších
ohledech: (a) inbox má **1 825 řádků ve 18 souborech / 141 647 znaků**, ale SessionStart hook
injektuje **strop 120 řádků** — už dva nejnovější soubory (56 + 310 řádků) strop přetečou,
takže **6,6 % obsahu** se kdy dostane do kontextu a nic starší než včerejší den se neinjektuje
nikdy; (b) povyšovací příkazy pluginu **`/knowledge-loop:rule-new` 0×** a
**`rules-consolidate` 0×** — těch 5 povýšení proběhlo ručně, mechanismus sám nebyl použit ani
raz; (c) zóna `.claude/rules-personal/martint/` v alzask je **prázdná**, zatímco ve fhb má
2 pravidla — tedy v hlavním projektu (75 % promptů) osobní vrstva neexistuje.
**Doklad:** `DEFAULTS = {"days": 14, "max_lines": 120, ...}` —
`C:\Git\shared\plugins\knowledge-loop\hooks\session-context.py:32`, strop aplikován na :200–203.
Řádky inboxu: měřeno, 1 825 celkem, `2026-08-25.md` 310, `2026-08-26.md` 56.
`rt_history.py`: `/knowledge-loop 0`, `/rule-new 0`, `rules-consolidate 0`.
`ls C:\Git\alzask\.claude\rules-personal\martint` → prázdné; `C:\Git\fhb\...\martint` → 2 soubory.
**AKCE:** `překlasifikovat na` antipattern-námět „záchyt bez povyšovací brány je archiv"
a **M-10 přeformulovat** z „opakovaná korekce se povyšuje na pravidlo" (`must`) na
„proč se moje vlastní povyšování zastavilo" (`should`). Pozitivní přenositelný zbytek je
jednořádkový: *jeden `.md` soubor na kandidáty a týdenní připomínka je celá smyčka; plugin ne.*

### RT-05 — Worktree: vyzkoušeno jeden den, vypnuto, nikdy víc
**Typ:** neosvědčilo se
**Terč:** O-05; a varování proti kandidátu C5 z `faze4b`
**Nález:** Slovo „worktree" má **29 výskytů, 26 z nich v jediném dni 2026-06-19** v alzask
(a 3 ve fhb 2026-06-18), a ten den vypadá jako sekvence zmatku: „NErozumím tomu, co se teď
stalo, protože ve Visual Studio Code nyní nevidím žádné změny", „Jak se dělá pořádek ve
worktrees? Jak je to běžné?", „Chci variantu bez commitu", „worktree už nepotřebuji". Následně
`worktree.bgIsolation: none` v `settings.json` a **0 výskytů v červenci i srpnu**. Přesto
`faze4b` sekce C5 doporučuje worktrees jako netestovanou příležitost („použito aspoň jednou,
ale ne systematicky") — to je nepřesné čtení: mechanismus byl vyzkoušen a odmítnut.
**Doklad:** `rt_absence.py` + kontextový výpis: `prompty-alzask-06.md` 26×, `prompty-fhb-myfaber.md` 3×,
`prompty-alzask-07.md` a `-08.md` **0×**. `faze1-korekce-hooky.md` — `worktree.bgIsolation: none`.
`faze4b-verifikace-a-mezery.md:201–207` (C5).
**AKCE:** `přeformulovat na` O-05 = „izolace, které nerozumíš, tě stojí dopoledne" s doloženým
obloukem jednoho dne, a **C5 nepřijímat** do finálu jako doporučení. Přenositelná lekce:
*než zapneš izolaci, ať víš, kterým příkazem se z ní práce dostane zpátky.*

### RT-06 — N-01 je v samotném podkladu označené „nedoporučuju"
**Typ:** osobní zvyk
**Terč:** N-01 „Nastavení nasazuj na diagnózu, ne na dojem" (`should`, `demo`, 12 min, blok 2)
**Nález:** Zdrojový kandidát N4 má **1 epizodu (~10 promptů)** o diagnostice zatížení vlastního
notebooku a podkladový agent ho explicitně klasifikoval: *„Osobní zvyk / `[infra]` — obsah je
specifický pro stroj uživatele… **Předvedatelnost: Slabá pro workshop analytiků. Nedoporučuju.**"*
Draft ho přesto povýšil na `should` s rolí `demo`. Přenositelné je jen tvar otázky
(„zjisti a rozhodni mezi hypotézami A/B/C"), který zdroj sám odkazuje na A8.
**Doklad:** `faze2b-prompty-alzask-07.md:1263–1271`; souhrnná tabulka tamtéž :1365 —
„N4 | Diagnostika stroje | N | 1 | **osobní zvyk — nedoporučuju** | ★".
**AKCE:** `vyřadit` N-01. Tvar otázky sloučit do A-04 (straw-man) jako jednu větu.

### RT-07 — Blok „Brány a kvalita" je nejdražší a nejméně odnesitelný blok programu
**Typ:** infra
**Terč:** M-01, M-03, M-08, R-05 (+ infra-poloviny M-04, M-09, M-10, R-06)
**Nález:** Z deseti `M` položek funguje u kolegy **den jeden tři** (M-02, M-05, M-06) plus M-07
jako princip. M-01 stálo „půl dne na napsání zadání brány + běh + **2–3 dny doladění**";
M-03 předpokládá už existující skript s exit kódy (referenční `questions.py` má 619 řádků);
M-08 předpokládá validátor **a měsíce dat**, aby měl práh co překračovat. Blok 3 má současně
192 minut (viz RT-08) — tedy nejvíc času věnovaného tomu, co si publikum bez stavby neodnese.
**Doklad:** analýza závislostí položek (fáze 5, podagent „infra"): `faze2e-prompty-shared.md:179–190`
(cena brány), `faze3a-alzask-metodiky.md:579, 720–726` (`questions.py` 619 ř.),
`faze3a-alzask-metodiky.md:102–114` (23 FR v draftu 55–201 dní → práh 30 dní trvale překročen).
**AKCE:** `překlasifikovat na` samostatnou přílohu „pro toho, kdo to bude stavět" — M-01, M-03,
M-08, R-05. V hlavním programu nechat trojici **M-02 + M-05 + M-06**, která dohromady dává
kompletní revizní protokol **bez jediného skriptu**, a M-07 jako princip. Blok 3 tím spadne
z 192 min na ~50.

### RT-08 — R-04 je pravidlo, které autor sám neplní
**Typ:** osobní zvyk
**Terč:** R-04 „Dvě vrstvy dokumentace podle čtenáře" (`should`, 10 min)
**Nález:** Pravidlo zní „stručný `CLAUDE.md` pro agenta, plná metodika v `README`". Vlastní
root `CLAUDE.md` alzask má **23 818 znaků** (~7 800 tokenů) — čtyřnásobek ilustrativní hodnoty
z dokumentace — a obsahuje mimo jiné 12,7% sekci, která se nikdy nepoužila (RT-02).
`docs/fr/README.md` má 1 201 řádků a od 6/2026 needitován. Položka je tedy prezentovaná jako
praxe, ale doklad ukazuje opačný výsledek.
**Doklad:** `doklady-cena-kontextu.md` (23 427 zn., dnes 23 818); `faze3a-alzager…` →
`faze3a-alzask-metodiky.md:18–44` (README 1 201 ř. vs. CLAUDE.md 69 ř. v jiném adresáři),
:1006 (README needitován od 6/2026).
**AKCE:** `přeformulovat na` „dvě vrstvy se rozjedou, když jednu z nich nikdo nečte —
jak to poznám" a **snížit prioritu na** `could`, nebo sloučit do K-08.

### RT-09 — A-10 se v produkční specifikaci autora už porušuje
**Typ:** osobní zvyk
**Terč:** A-10 „Publikum určuje, co smí být odkaz" (`should`, `demo`)
**Nález:** Pravidlo „spec pro externího dodavatele nesmí odkazovat na ADR/FR" má v produkční
PLC specifikaci **dva propuštěné interní odkazy**, které prošly revizí. Zdroj to sám komentuje:
*„pokud není vynucené branou, bude se pomalu porušovat."*
**Doklad:** `faze3a-alzask-metodiky.md:868–886`, konkrétně :875–879.
**AKCE:** `přeformulovat na` doklad pro M-01 („pravidlo bez brány se pomalu poruší") a
samostatnou položku A-10 `vyřadit` — sloučit do A-09 (adresát jako parametr zadání).

### RT-10 — R-02 je sám nepovýšený kandidát z inboxu
**Typ:** neosvědčilo se
**Terč:** R-02 „Metodika bez spouštěče je jen text" (`should`, blok 4)
**Nález:** Námět je v inboxu veden jako kandidát z 2026-08-25 a **nebyl povýšen** — tedy sám
je instancí problému, který popisuje. Podpůrný doklad je navíc destruktivní:
`grep -ri "ontolog"` v metodických souborech dal **0 výskytů**, přestože ontologický registr
existuje a `CLAUDE.md` na něj má celou sekci.
**Doklad:** `faze3c-pravidla-inbox.md:175`.
**Pozor — druhý doklad z podkladu už neplatí:** `faze3a-alzask-metodiky.md:364–369` uvádí
`grep -ri "ontolog"` → 0 výskytů. Dnes je to **19 výskytů na 15 řádcích `CLAUDE.md`** (včetně
nadpisu `## Ontologie prvků` na ř. 308) a **77 výskytů pod `.claude/`**. Ten grep nepoužívat
(viz RT-38).
**AKCE:** `přeformulovat na` sebe-ilustrující položku: „tento námět jsem sám zapsal do inboxu
a nepovýšil" — a spojit s X-06 do jedné (viz RT-01).

### RT-11 — „137 promptů do pluginu" je špatné číslo
**Typ:** vadný doklad
**Terč:** tabulka dokladů `katalog-draft.md:123`; nepřímo U-05, R-05
**Nález:** Číslo 137 je počet **řádků history pro projekt spec-factory**, nikoli promptů
věnovaných pluginu. Zdroj rozpadá: 151 bloků, z toho **93 věcných** a **~56 na vlastní
inženýrství**, koncentrovaných do 9 dní; k tomu ~den na distribuci. Zdroj má i verdikt, který
draft neuvádí: *„postav plugin, až budeš mít druhého uživatele. Do té doby stačí `CLAUDE.md`
a jeden dobře napsaný prompt v souboru."*
**Doklad:** `faze2e-prompty-shared.md:13–33` (rozpad), :107–120 (distribuce), :224 (verdikt).
**AKCE:** `přeformulovat na` „93 věcných + ~56 inženýrských promptů v 9 dnech" a **doplnit
chybějící** citovaný verdikt jako závěr U-05 — to je jediná věta, kterou si z okruhu `U`
odnese i kolega, který plugin nikdy stavět nebude.

### RT-12 — O-02 a X-12 jsou dvě poloviny jednoho nálezu a druhá polovina ruší první
**Typ:** osobní zvyk
**Terč:** O-02 „Volba modelu podle povahy podúlohy", X-12 „Ladění modelu bez srovnávací základny"
**Nález:** `/model` je s **63× (53× pracovní) nejčastější slash příkaz vůbec**, přičemž
`settings.json` má model natrvalo `opus[1m]` a `effortLevel: high`, `/effort` jen 9× (4×
pracovní). Zdroj z července navíc dokládá **5 dvojic doslovně přepsaných promptů** kolem
`/model` („prompt se napíše, pak `/model`, pak se týž prompt naťuká celý znovu", u jedné
dvojice včetně 47 znovu vložených řádků) a kandidát X4 „ladění modelu bez baseline" ~20 výskytů.
Doložená praxe tedy není *volba* modelu, ale *přepínání bez měřítka*. Pozitivní část námětu
drží jen na statických definicích subagentů (`review-*`: opus/opus/sonnet/haiku/haiku) —
a ty nebyly nikdy spuštěny (RT-03).
**Doklad:** `rt_history.py`: `/model 63/53`, `/effort 9/4`. `faze2e-prompty-shared.md:479–487`
(5 doslovných duplikátů po `/model`). `faze2b-prompty-alzask-07.md:1357` (X4, ~20).
`faze1-korekce-hooky.md` — `model: opus[1m]`, `effortLevel: high`.
**AKCE:** `sloučit` O-02+X-12 do jedné položky „přepínám model 63× a neměřím, jestli to k něčemu
je" a `snížit prioritu na` `could`. Přenositelné jádro je jedna věta: *vyber model **dřív**,
než pošleš drahý prompt* — a to už je obsah N-02/K-01.

### RT-13 — R-05 (hook) doporučuje vzor, který autor nikdy nepoužil
**Typ:** infra / nepředveditelné
**Terč:** R-05 „Hook: kontrola, kterou nemusíš spouštět" (`could`, blok 4)
**Nález:** Reálně běží **4 hooky, 2 z ~8 eventů** (`SessionStart`, `PreToolUse`), oba přinesené
pluginy nebo cizí šablonou. Nejužitečnější vzor pro publikum — `SessionStart` s matcherem
`compact`, dokumentovaný Anthropicem přímo pro „zachovat kontext přes kompaktaci" — autor
**nepoužil** (`faze4b` ho vede jako netestovaný kandidát C1). `PreCompact`/`PostCompact` nemá
v dokumentaci ani příklad. Demo v této formě vyžaduje živý `/compact` (177 s, viz RT-24)
a editaci `settings.json` na jevišti.
**Doklad:** `faze1-korekce-hooky.md` (4 hooky, „Použité eventy: 2 ze cca 8");
`faze4b-verifikace-a-mezery.md:172–179` (C1, „netestováno — nemám s tím vlastní zkušenost").
**AKCE:** `přeformulovat na` demo dvou **už běžících** hooků (injekce handle+inboxu při startu,
ontologický `session-check.py`) — 20 sekund, nulová konfigurace — a matcher `compact` uvést
jako „co bych přidal příště", ne jako praxi. Prioritu ponechat `could`.

---

## 2. Vadné doklady (čísla, která publikum přepočítá)

### RT-14 — Vlajkové číslo bloku 1 je nadhodnocené o 36 %, a „21 kompaktací" jsou 19
**Typ:** vadný doklad
**Terč:** F-03, F-04, tabulka dokladů `katalog-draft.md:105–108`
**Nález:** Tři nezávislé defekty v `doklady-kompaktace.md`:
1. **Dvojí započtení.** Řádky 5 a 6 (2026-08-12 19:24, pre 602 574, post 14 075) a řádky 7 a 8
   (2026-08-13 06:26, pre 408 542, post 11 757) jsou **tatáž kompaktace zapsaná ve dvou
   souborech session** (fork/resume kopíruje záznam). Skutečných událostí je **19, ne 21**.
2. **Smíchané metriky.** Řádek 5 má ve sloupci „zahozeno v tomto kroku" hodnotu **2 702 520**,
   ačkoli `pre − post = 588 499` — je tam omylem `cumulativeDroppedTokens`. Rozdíl 2 114 021
   tokenů putuje do součtu.
3. **Součet.** „Celkem zahozeno **11 700 496**" → po opravě řádku 5 a deduplikaci je to
   **8 601 191**. Draft nadhodnocuje o **3 099 305 tokenů = 36 %**.
Navíc formulace „97,3 % (583 578 → 12 127 tok.)" v `katalog-draft.md:106` je **slepený pár**:
tenhle konkrétní pár dává 97,9 %, mediánové pre/post po deduplikaci je 464 352 → 13 344.
**Doklad:** `rt_kompaktace.py` (přepočet celé tabulky): duplikáty `[(5,6),(7,8)]`;
nekonzistentní řádek `#5 pre-post=588499 tabulka=2702520 rozdil=2114021`; součty
`11 700 496 → 8 601 191`; `procenta z páru medianu (583578 → 12127) = 97,9`.
**AKCE:** `přeformulovat na` „**19** kompaktací, medián zahozeného **97,3 %**, souhrnně
**~8,6 milionu** tokenů" a pár v závorce **odstranit** (nebo použít skutečný medián
464 352 → 13 344). Poznámka o podvýběru (21 z 51 `/compact`) v textu ponechat.

### RT-15 — Oprava decku „3,5 → 4 znaky/token" je sama sporná
**Typ:** vadný doklad
**Terč:** F-02, tabulka dokladů `katalog-draft.md:126`
**Nález:** Draft chce v existujícím decku opravit „≈ 3,5 znaku/token" na dokumentované
„≈ 4 znaky/token". Táž ověřená rešerše ale zaznamenala i druhý dokumentovaný fakt: modely
**od Opus 4.7 dál používají novější tokenizér, který dává na stejný text cca o 30 % více
tokenů**. Čtyři znaky/token dělené 1,3 dává **≈ 3,1 znaku/token** — tedy pro model, na kterém
autor pracuje (`opus[1m]`), je původní hodnota 3,5 **blíž skutečnosti než „oprava" na 4**.
Postavit se před publikum s „v decku je chyba" a mít v ruce protichůdnou citaci z týchž
dokumentů je zbytečné riziko.
**Doklad:** `faze4b-verifikace-a-mezery.md:40` (tokenizér od 4.7 „+cca 30 % tokenů") vs. :44
(FAQ „1 token ≈ 4 znaky … v angličtině"); `korekce-pro-syntezu.md` bod 2.
**AKCE:** `přeformulovat na` rozsah se dvěma citacemi: „FAQ říká ≈ 4 znaky/token pro
angličtinu; táž dokumentace říká, že novější tokenizér dává o ~30 % víc tokenů — pro Opus 5
tedy počítej ≈ 3 znaky/token pro AJ a méně pro češtinu. Číslo pro češtinu Anthropic
nepublikuje." Deck neopravovat na „4", ale doplnit poznámku o generaci tokenizéru.

### RT-16 — „11 doložených dvojic" je v podkladu 5
**Typ:** vadný doklad
**Terč:** K-02 (`must`, blok 2), tabulka dokladů `katalog-draft.md:114`
**Nález:** Zdroj tvrdí „11 doložených dvojic + 5 samostatných", ale **v tabulce vypisuje 5
dvojic** (z toho jednu se třemi koly) a pak 5 rozkazů bez opravy. Číslo 11 není ve zdroji
dohledatelné. Je to `must` položka a zároveň ironie: v témže draftu je K-04 „citace se ověřuje,
nevěří".
**Doklad:** `faze2b-prompty-alzask-07.md:1065–1077` — tabulka má 5 řádků, text pod ní tvrdí
„**11 doložených dvojic + 5 samostatných**".
**AKCE:** `přeformulovat na` „5 doložených dvojic (jedna ve třech kolech) + 5 bezcílných
rozkazů bez opravy" — a použít ten spor jako živé cvičení pro K-04 („najdi v mém vlastním
podkladu číslo, které nemá oporu").

### RT-17 — „Kontext před prvním slovem ≈ 13 000 tokenů" je podhodnocené a je to odhad
**Typ:** vadný doklad
**Terč:** F-05, tabulka dokladů `katalog-draft.md:111`
**Nález:** Číslo 12 946 sečítá **jen tři soubory, které umí autor přečíst** (`CLAUDE.md`,
`MEMORY.md`, output style) — a samo si to přiznává. Chybí systémový prompt, definice nástrojů,
metadata skillů a **injekce inboxu SessionStart hookem** (strop 120 řádků, viz RT-04).
Přepočet je navíc při **3,0 znaku/token**, což je autorův vlastní odhad, ne měření — a podle
RT-15 může být pro aktuální tokenizér nízký. Publikum, které si na svém stroji pustí
`/context`, uvidí jiné číslo a bude mít pravdu.
**Doklad:** `doklady-cena-kontextu.md` — hlavička („poměr 3,0 znaku na token … ber jako řádovou
orientaci, ne fakturu") a sekce „Co se načítá automaticky" (součet 38 838 zn. / ~12 946 tok.),
následovaná větou „Ty tři čísla nejsou v souborech, které umím přečíst".
**AKCE:** `přeformulovat na` „**minimálně** ~13 000 tokenů jen ze souborů, které si můžu
přečíst; skutečné číslo dá `/context` a je vyšší" a demo F-05 postavit **na živém `/context`**,
ne na tabulce odhadů.

---

## 3. Chybí (nové náměty)

### RT-18 — Chybí režim plánování (plan mode). Nejlevnější nástroj pro analytika, v datech 1 výskyt.
**Typ:** chybí
**Terč:** chybí — nový (okruh `N` nebo `K`)
**Nález:** Analytik ze všeho nejvíc potřebuje „nejdřív si to rozmysli a napiš plán, teprve
potom sahej na soubory". Claude Code to má vestavěné (plan mode, `Shift+Tab`) a **v 2 678
promptech je `/plan` právě jednou** (2026-07-07 19:03, hned následován `/plugins` — vypadá
to na neúspěšný pokus). Celý draft to nahrazuje ručně postavenými náhradami
(R-01 prompt do souboru, A-04 straw-man, M-02 read-only brána) — což jsou dobré náměty,
ale publikum má zdarma vestavěný mechanismus, o kterém se z programu nedozví.
**Doklad:** `rt_history.py`: `/plan 1 / 1`. Kontextový výpis `rt_absence2.py`:
„2026-07-07 19:02 /plugins ## 19:03 /plan ## 19:03 /plugins".
**AKCE:** `doplnit chybějící` námět „režim plánování: rozhodnutí odděleně od provedení"
do bloku 1 nebo 2, `must`, 10 min, role demo (přepnutí režimu je deterministické a okamžité).
Vedle něj přiznat: *„v mých 1 507 promptech není — tohle je věc, kterou jsem se naučil pozdě."*

### RT-19 — Chybí „jak to vzít zpátky". `/rewind` 0×, checkpointy nikde.
**Typ:** chybí
**Terč:** chybí — nový (okruh `N`)
**Nález:** První otázka kolegy, který se bojí agenta pustit na svá data, je „a co když to
rozbije". Draft na to má **jedinou odpověď** — N-02 (tři `deny` položky), tedy prevenci.
Náprava po škodě v programu není: `/rewind` **0×**, checkpointy 0 výskytů, `git stash/revert`
2 výskyty (a oba jen jako součást jednoho promptu o baseline). Přitom O-05 (smazaná
rozpracovaná práce) je v draftu jako `must` příběh — položíte problém a nedáte lék.
**Doklad:** `rt_history.py`: `/rewind 0 / 0`. `rt_absence2.py`: „rewind/checkpoint 0";
„git stash/revert 2" (týž prompt 2×).
**AKCE:** `doplnit chybějící` námět „tři úrovně zpět: `Esc Esc` / `/rewind` / `git diff`" jako
pár k O-05, blok 1, `must`, 8 min. Deterministické, rychlé, a je to jediná věc, která publiku
sundá strach.

### RT-20 — Chybí citlivá data a GDPR. V celém korpusu 0 zásahů, a je to korpus zákazníkových dokumentů.
**Typ:** chybí
**Terč:** chybí — nový; přesah do X-01, N-02, N-04
**Nález:** Slova „GDPR", „osobní údaj", „anonymizace", „de-identifikace", „NDA", „citlivé"
mají v 286 290 znacích promptů **nula skutečných zásahů** (6 nalezených je falešně pozitivních —
`NDA` uvnitř slova „sta**nda**rdní"). Přitom obsahem téže práce jsou zákaznické specifikace,
přepisy jednání se jmény lidí, e-maily dodavatelů (`.msg`, 26 zmínek) a smluvní příloha.
Jediný doklad, který v korpusu je, je nejostřejší v celém vzorku: **4 GitLab tokeny v plném
znění ve 5 promptech během 45 minut, tři musely být zneplatněny** (X-01, 8 min, blok 1).
Draft z toho dělá jednu osmiminutovou historku a nemá **žádný** námět o klientských datech.
Sekundární problém: dvě demo položky (N-04 `/insights`, A-06 registr dodavatelů) promítají
na projektor jména Alza / BullsEye / BlueSword a otevřené závazky dodavatelů.
**Doklad:** `rt_absence.py` („bezpecnost/GDPR 6" → `rt_absence2.py` ukazuje, že všech 6 je
`NDA` ve „standardní"); „licence 0". `faze2e-prompty-shared.md:460–474` (X1, 4 tokeny,
„Původní tokeny byly smazány").
**AKCE:** `doplnit chybějící` námět **„prompt je zápis, ne rozhovor: co do něj nikdy nepatří"**
— tajemství (tokeny, hesla), osobní údaje třetích stran, a co se stane, když to tam je
(transkript, export, `/insights`, tenhle katalog). Blok 1, `must`, 12 min. X-01 se do něj
vloží jako doklad. Prio `must` — je to jediná položka v celém katalogu, která může někomu
opravdu uškodit.

### RT-21 — Chybí licence a vlastnictví výstupu: 0 výskytů, a výstupy jdou zákazníkovi
**Typ:** chybí
**Terč:** chybí — nový
**Nález:** „licence", „copyright", „autorská" — **0 výskytů** v celém korpusu. Analytik
generuje dokumenty, které jdou do smluvní dokumentace zákazníka, a diagramy/HTML, které se
publikují. Otázka „čí to je a smím to takhle dodat" v datech neexistuje, a v draftu taky ne.
Publikum ji položí a nedostane odpověď.
**Doklad:** `rt_absence.py`: „licence 0 výskytů / 0 souborů"; `rt_absence2.py`: „ZADNY VYSKYT".
**AKCE:** `doplnit chybějící` odstavec (ne celý námět — 5 minut) do bloku 1 vedle RT-20:
co s výstupem smím, co se stane s vloženým vstupem, a kdo v organizaci na to odpovídá.
Pokud odpověď neexistuje, je to úkol pro workshop, ne pro slide.

### RT-22 — Chybí odhady a rozpočet práce: „pracnost / man-day / story point" 0 výskytů
**Typ:** chybí
**Terč:** chybí — nový (a rozšíření otevřené otázky č. 4 draftu)
**Nález:** Draft přiznává, že nemá námět o **ceně tokenů**. Chybí ale i to druhé, co analytik
odhaduje pořád: **pracnost**. Regulární výrazy `pracnost | man-?day | story point |
odhad+pracnosti` dávají **0 zásahů**. Ke ceně: `/usage` **9× (3× pracovní)**, `/cost` **0×**,
slovo „rozpočet" 1× a je to *rozpočet na otázky* (A-03), ne peníze. Zároveň v ruce leží
mimořádný doklad: **~8,6 milionu tokenů prokazatelně zahozeno kompaktacemi** (RT-14) —
při dokumentovaných $5/MTok vstupu Opus 5 je to konkrétní řádová suma zaplacená za text,
který model podruhé nepoužil.
**Doklad:** `rt_absence2.py`: „odhad pracnosti (presne) → ZADNY VYSKYT"; „cena/rozpocet"
jediný zásah = „Rozpočet utrať podle páky". `rt_history.py`: `/usage 9/3`, `/cost 0/0`.
Ceny: `faze4b-verifikace-a-mezery.md:52–56` ($5/$25 MTok Opus 5, batch −50 %).
**AKCE:** `doplnit chybějící` námět „co to stojí a jak to zjistíš" (`/usage`, `/context`,
zahozený kontext jako položka), blok 1, `should`, 10 min — a poctivě říct, že autor to
nesledoval. Odhady pracnosti nechat jako **přiznanou mezeru**, ne vymýšlet praxi bez dokladu.

### RT-23 — Chybí práce s cizím textem a cizí revizí: „code review / merge request" 0 výskytů
**Typ:** chybí
**Terč:** chybí — nový (okruh `A`)
**Nález:** `code review | review kódu | merge request | pull request` — **0 zásahů v 286 290
znacích**. Analytik ale polovinu času čte, co napsal někdo jiný: cizí specifikaci, cizí API
YAML, cizí přepis, připomínky kolegyně. Jediný doklad tohoto druhu v datech je jeden prompt
(„Kolegyně, kterou nemám příliš v oblibě, mi poslala připomínky k diagramu…", 4× přeposlaný
kvůli `/spec`), který draft nepoužívá. Náměty A-01 a K-06/K-07 se cizího textu dotýkají, ale
jen jako *vrstev jednoho dokumentu*, ne jako *cizí práce, kterou mám posoudit*.
**Doklad:** `rt_absence2.py`: „code review → ZADNY VYSKYT". `faze1-statistiky.md`, tabulka
promptů nad 1000 znaků, 2026-06-19 21:57 / 22:04 / 23:48 / 23:51 (tentýž prompt o připomínkách
kolegyně 4×).
**AKCE:** `doplnit chybějící` námět „cizí text: jak z připomínek udělat zadání" do bloku 5,
`should`, 12 min. Doklad je k dispozici a je i vtipný; navíc dobře snáší cvičení
(každý má v mailu připomínky, které nezpracoval).

### RT-24 — Chybí předání kolegovi. Nulová evidence, a přitom je to vlastní obsah série.
**Typ:** chybí
**Terč:** rozšíření otevřené otázky č. 5 draftu; přesah do O-03, U-05
**Nález:** Draft přiznává „nemám nic o práci ve dvojici/týmu". Data to potvrzují tvrdě:
„ve dvojici / pair / společně s kolegou" **0 výskytů**. Ale v datech **je** to, co se dá říct:
**10 z 13 pravidel se mezi projekty přeneslo ruční kopií, 4 bit-shodné**; vrstva
„cross-project shared", která by to řešila, v `CLAUDE.md` **je popsaná a na disku neexistuje**
(`C:\Git\shared\.claude\rules` — adresář chybí). To není námět o týmové práci, to je námět
o **přenosu**: co musí být v repozitáři, aby to fungovalo druhému člověku, když session
nedostane.
**Doklad:** `ls C:\Git\shared\.claude\rules` → „No such file or directory".
`katalog-draft.md:121–122` (10 z 13 ruční kopií). `rt_absence2.py`: „prace ve dvojici →
ZADNY VYSKYT".
**AKCE:** `doplnit chybějící` námět **„co commitnout, aby to fungovalo i kolegovi"**
(`CLAUDE.md`, `.claude/commands/`, validátor, ne session a ne paměť) — blok 6 nebo 2,
`must`, 12 min. X-08 se do něj sloučí jako doklad (viz RT-01). Bez tohohle námětu je celá
série nepřenositelná do praxe týmu, což je její deklarovaný účel.

### RT-25 — Chybí pozitivní námět o výrobě vysvětlovacího artefaktu, přestože ho autor udělal třikrát
**Typ:** chybí
**Terč:** chybí — nový; X-05 je dnes jen jeho antipatternová polovina
**Nález:** Autor postavil **tři netriviální vysvětlovací artefakty pro lidi**: 12-slide deck
„Jak funguje Claude Code", interaktivní simulaci dopravníku (`dopravnik-simulace.html`)
a HTML prezentaci pluginů pro kolegy. Doklady o zadávání jsou v datech („Nyní chci vytvořit
jenom osnovu, až si ji schválíme, tak teprve…", „Prostuduji si tyto dokumenty a nejprve
navrhni principy… abychom nevymýšleli něco, co už je někde vymyšleno"). V draftu z toho není
**ani jedna pozitivní položka** — jen X-05 „ladění screenshoty místo invariantu: 30 promptů",
tedy jeho nejhorší část. Analytik, který má vysvětlit skladový proces netechnickému
zákazníkovi, přitom tohle využije okamžitě.
**Doklad:** `rt_absence2.py`, sekce „prezentace pro publikum" — 6 kontextů z `prompty-shared.md`
a `prompty-alzask-07.md` (osnova → schválení → tvorba; „HTML prezentaci … postupným způsobem
by se člověk mohl seznámit"). `faze0-existujici-material.md:8–48` (deck).
**AKCE:** `doplnit chybějící` námět „vysvětlovací artefakt: osnovu nech schválit, teprve pak
generuj" — blok 4 nebo 5, `should`, 12 min, role demo (deck existuje a otevře se offline).
X-05 se pod něj vloží jako „a takhle to při ladění utíká".

### RT-26 — Chybí cvičný sandbox. 34 dem a 7 cvičení, a nikde se nesmí sáhnout.
**Typ:** chybí
**Terč:** draft jako celek (a všechny položky s rolí `demo`/`cvičení`)
**Nález:** Program má **34 položek s demem a 7 s cvičením**, ale všechna dema se opírají o
produkční repozitáře — a `C:\Git\alzask` má **právě teď 14+ rozpracovaných necommitnutých
souborů**, včetně `CLAUDE.md`, `docs/adr/INDEX.md` a samotných nástrojů `cite.py`/`reanchor.py`,
které jsou zároveň demo-rekvizitou. Paměť projektu navíc zakazuje v alzask commitovat.
Publikum nemůže cvičit v zákazníkově repozitáři a přednášející si nemůže dovolit reflexivní
`git checkout .`. Draft nemá **žádnou** položku o přípravě cvičného prostředí.
**Doklad:** stav pracovního adresáře alzask (dirty, 14+ změněných/smazaných souborů) —
ověřeno v rámci fáze 5; `MEMORY.md` → „NIKDY nedělej commity v AlzaSk".
`rt_bloky.py`: „polozek s demo: 34 = 52 %", „polozek s cvicenim: 7".
**AKCE:** `doplnit chybějící` **nulté** dílo série: malý cvičný repozitář v `C:\tmp`
(3–5 dokumentů, jeden validátor, jeden `CLAUDE.md`, jeden záměrně rozbitý soubor), na kterém
se dají odehrát M-01, M-02, M-09, X-07 i cvičení. Bez něj polovina programu neexistuje.

### RT-27 — Chybí „kdy Claude Code nepoužít": 0 výskytů, a je to nejžádanější slide zkušeného publika
**Typ:** chybí
**Terč:** chybí — nový
**Nález:** `raději ručně | udělám to sám | bez claude | nepoužij` — **0 zásahů**. Katalog má
12 antipatternů typu „takhle to děláš špatně, dělej to jinak" a **ani jeden** typu „tady to
nezkoušej vůbec". Publikum, které nástroj už používá, tuhle otázku má (a odpověď na ni je
důvěryhodnostní test celé série). Materiál pro ni v datech je: 30 promptů / 8 kol ladění
algoritmu screenshoty (X-05), ~25 mikro-iterací UI, 5 doslovných přepsání promptu po `/model`.
**Doklad:** `rt_absence2.py`: „kdy NEpouzit claude → ZADNY VYSKYT".
`faze2b-prompty-alzask-07.md:1355–1358` (X2 oblouk 30, X3 ~25, X5 24).
**AKCE:** `doplnit chybějící` závěrečnou položku „tři situace, kdy jsem měl vypnout terminál"
— blok 6, `must`, 10 min. Postavená čistě z vlastních doložených oblouků, žádná nová teorie.

---

## 4. Nepředveditelné

### RT-28 — F-03: živá kompaktace je 3 minuty spinneru a zabije session, ve které přednášíš
**Typ:** nepředveditelné
**Terč:** F-03 „Kompaktace ti session zachrání, a ty nevíš, co vypadlo" (`must`, `výklad+demo`, 18 min)
**Nález:** Medián **177,5 s**, maximum **224,1 s** — v šedesátiminutovém setkání to je
3–4 minuty čekání, během kterých se nedá mluvit o ničem jiném (kompaktace čte celou
konverzaci). A výsledkem je, že demonstrační session ztratí kontext, který přednášející
možná ještě potřebuje. Tabulka 19 kompaktací je lepší podklad než živý běh.
**Doklad:** `doklady-kompaktace.md`, souhrn: „Medián doby kompaktace 177.5 s", „Nejdelší
224.1 s"; `rt_kompaktace.py` potvrzuje medián.
**AKCE:** `přeformulovat na` `výklad` + tabulka z vlastních transkriptů (`preTokens`/`postTokens`
z `compactMetadata`), 12 min. **A doplnit** to jediné, co je předveditelné a užitečné:
`/compact <instrukce>` — dokumentovaná a v datech použitá **2× ze 67 kompaktací**, tedy
i pro autora nová informace.

### RT-29 — F-02: na tomhle stroji neexistuje způsob, jak spočítat tokeny
**Typ:** nepředveditelné
**Terč:** F-02 „Čeština není dražší, protože je delší" (`must`, `výklad+demo`, 12 min)
**Nález:** Anthropic nezveřejňuje offline tokenizér ani veřejný widget; jediná cesta je
`POST /v1/messages/count_tokens`, která **vyžaduje API klíč** — a ten na stroji není.
Tokenizér ve vlastním decku je **napevno zakódované pole** `TOK_EN`/`TOK_CZ` a poměr se
dopočítává jako `text.length / arr.length`. Pomocný skript `_tok.py` počítá znaky a UTF-8
bajty, ne tokeny. Demo v této podobě by předvedlo přesně tu záměnu, kterou má položka
vyvracet — bajty vydávané za tokeny.
**Doklad:** `faze4b-verifikace-a-mezery.md:82–88` — „**Toto je negativní nález** — pokud stroj
nemá API klíč ani `ant` CLI, oficiální cesta k přesnému počtu tokenů skutečně chybí";
tamtéž analýza JS decku (řádky 595–619, `TOK_EN`/`TOK_CZ` hardcoded).
**AKCE:** `překlasifikovat na` `výklad` (bez dema) s poctivým rozdělením podle RT-15, a
u decku na jevišti **přiznat**: „tohle je ilustrace, ne živý tokenizér". Jediné čestné číslo
z živého stroje dává `/context`, ne tokenizér.

### RT-30 — N-04 `/insights`: nikdy nespuštěno, neměřený běh, a promítne jména zákazníka
**Typ:** nepředveditelné
**Terč:** N-04 „`/insights` — inventura vlastní praxe jedním příkazem" (`should`, `demo`, 8 min)
**Nález:** Tři nezávislé režimy selhání naráz: (a) příkaz **nebyl nikdy spuštěn** (0×
v 2 678 promptech, žádný artefakt v `~/.claude/`), (b) analyzuje až 200 session — u alzask
je to 84 souborů / ~122 MB, doba běhu neznámá a jde o LLM-generovaný výstup, tedy
nedeterministický, (c) report pojmenuje Alza.sk, BullsEye a BlueSword a promítne to na zeď
(viz RT-20). Přitom `korekce-pro-syntezu.md` bod 10 z něj dělá „první věc, kterou si kolega
může spustit sám" — což je dobrý nápad, ale ne v roli živého dema.
**Doklad:** `rt_history.py`: `/insights 0 / 0`. `doklady-kompaktace.md`: alzask 84 sessions /
120,4 MB. `korekce-pro-syntezu.md` bod 10.
**AKCE:** `přeformulovat na` „pusť si to doma na svých datech" (domácí úkol na konec dílu),
a pokud má být na jevišti, tak **předem spuštěné a pročištěné HTML**. Prioritu `should`
ponechat, roli `demo` zrušit.

### RT-31 — M-06 „Slepý recenzent": demo je tvrzení o tom, jak se model zachová
**Typ:** nepředveditelné
**Terč:** M-06 (`should`, `demo`, 10 min); týká se i M-02, A-02, A-04, X-03
**Nález:** Demo musí ukázat, že **slepý** recenzent najde víc než informovaný. To je dvojí
běh modelu, minuty času, a hlavně: **když informovaný recenzent shodou okolností najde totéž,
položka je před publikem vyvrácena**. Táž vada u A-04 (straw-man musí selhat *tím správným
způsobem*), A-02 (seznam bodů je výstup modelu) a M-02 (read-only brána je *prompt* — a její
selhání zapíše do repozitáře; navíc M-01 v témže katalogu tvrdí, že brána je lepší než prompt,
takže demo M-02 argumentuje proti M-01).
**Doklad:** definice agenta `spec-critic` (BLIND, „bez přístupu k cizím verdiktům") —
`faze3b-pluginy.md:833–836`; M-02 doklad „14 výskytů" (`katalog-draft.md:115`) je sám důkaz,
že ta instrukce se musí opakovat, tedy že nedrží.
**AKCE:** `překlasifikovat na` `výklad` + statický exponát (klauzule o slepotě v definici
agenta, věta z manifestu „kdo zná záměr, přestane text zkoumat a začne ho obhajovat").
U M-02 `přeformulovat na` `cvičení` na kopii v `C:\tmp`, ne demo v repozitáři.

### RT-32 — X-02 „Dlouhý prompt se ořízne": nereprodukovatelné, a selhání reprodukce vyvrací tvrzení
**Typ:** nepředveditelné
**Terč:** X-02 (`must`, `příběh+demo`, 10 min)
**Nález:** Jde o jednorázový artefakt terminálu z 8/2026 (3 052 znaků, text zmizel v půlce).
Reprodukce závisí na terminálu, bracketed paste a velikosti bufferu. Pokud se na jevišti
prompt **neořízne** — a to je pravděpodobnější — přednášející právě vyvrátil vlastní `must`
položku. Screenshot transkriptu udělá totéž s nulovým rizikem.
**Doklad:** `katalog-draft.md:117` („3052 znaků, text zmizel v půlce",
`faze2c-prompty-alzask-08.md`). Táž délka 3 052 je zároveň spodní hranice promptu pro A-01 —
tedy vlajkové demo katalogu stojí na délce, o které víme, že se v chatu jednou zlomila.
**AKCE:** `překlasifikovat na` `příběh` se screenshotem transkriptu; demo zrušit.
Po sloučení do R-01 (viz RT-01) je to jeho úvodní slide.

### RT-33 — Dvě dema vypisují závazky dodavatelů a modifikují repozitář
**Typ:** nepředveditelné
**Terč:** A-06 „Eviduj, co v odpovědi CHYBÍ" (`should`, `demo`), přesah do M-04
**Nález:** Vstupní bod dema je `questions.py`. `--build` **zapisuje generované soubory do
produkčního repozitáře**, takže bezpečné je jen `--check`; a výstup (`OTEVRENE.md`,
`QUESTIONS.tsv`) je seznam toho, co dodavatelé ještě dluží, se jmény, daty a přislíbenými
termíny. Doba běhu neměřena. Na projektoru je to obchodně citlivý dokument (viz RT-20).
**Doklad:** `docs/suppliers/.tools/questions.py` — režim `--build` generuje `OTEVRENE.md`
a `QUESTIONS.tsv` (viz `CLAUDE.md` sekce „Dotazy a odpovědi s dodavateli":
„`OTEVRENE.md` a `QUESTIONS.tsv` jsou generované"); `faze3a-alzask-metodiky.md:632–658`
(ISS-004 devět dní veden jako „chybí hodnoty").
**AKCE:** `přeformulovat na` demo nad **anonymizovanou kopií** dvou záznamů v `C:\tmp`
(dodavatel „A", otázka „X"), nebo `překlasifikovat na` `výklad` s ukázkou schématu záznamu.
Princip („eviduj, co v odpovědi chybí, ne jen co v ní je") je přenositelný zdarma a nepotřebuje
registr.

### RT-34 — Generátor dokladů přepisuje sám doklad, na kterém blok 1 stojí
**Typ:** nepředveditelné / provozní riziko
**Terč:** F-03, F-04, X-10
**Nález:** `compact_stats.py` **není report, ale generátor** — spuštění přepíše
`doklady-kompaktace.md`. Pokud by se demo bloku 1 mělo „spustit skript a ukázat čísla",
demo přepíše vlastní podklad. Během fáze 5 se to už jednou stalo (obsah zůstal shodný, změnila
se hlavička a velikost transkriptů). Je to zároveň nejlepší dostupná ilustrace X-10
(„regenerace přepíše ruční editaci") — jenže na podkladu, který má být stabilní.
**Doklad:** `compact_stats.py` (7 086 B, zapisuje `doklady-kompaktace.md`); hlavička dokladu
nese časové razítko odečtu, které se při běhu mění.
**AKCE:** `doplnit chybějící` krok do přípravy: čísla bloku 1 **zmrazit** do statické tabulky
ve finálním materiálu a generátor na workshopu nespouštět. Případ použít jako doklad pro X-10.

---

## 4b. Doplňky po ověření v repozitáři (druhé kolo)

### RT-35 — „Brána, ne prompt" je pravidlo, které v tomto projektu nemá bránu
**Typ:** neosvědčilo se
**Terč:** M-01 (`must`, 18 min), a s ním celá konvergence č. 4 draftu („brána místo instrukce",
5 nezávislých agentů)
**Nález:** Projekt vlastní `RULE-GOV-002 „brána, ne prompt"` a draft z něj dělá nejsilnější
konvergenci celého katalogu. Skutečné vynucení:
- **CI nespouští ani jeden validátor.** `.gitlab-ci.yml` zahrnuje jediný job (`ci/pipelines/daily-changelog.yml`)
  a `workflow.rules` omezuje pipeline na `$CI_PIPELINE_SOURCE == "schedule"`. Vlastní komentář
  souboru: *„CI proto zatim slouzi jen pro denni AI changelog"*. Push na `main` nezakládá nic.
- **Git hooky nejsou nainstalované.** `git config core.hooksPath` → `c:\Git\alzask\.git\hooks`,
  kde není **žádný** non-sample hook. Adresář `.githooks/` má poslední commit **2026-01-20**
  (7,2 měsíce — nejstarší nedotčená cesta v repozitáři).
- **A i kdyby byl nainstalovaný, byl by nefunkční.** `pre-commit.ps1:4` kontroluje jen
  `.ps1 .txt .sql .cs .rdlc .rdl .rdo .srd .srdmi` — v dokumentačním repozitáři, kde těch
  přípon je 8/0/0/0/0/0/0/0/0, a ty 8 `.ps1` jsou samotné CI skripty a hooky.
- **Z pěti validátorových subsystémů je exekučně navěšený jeden** (ontologie, přes `SessionStart`
  v `settings.json` + `spec-config.yaml:47–49`). FR, ADR, PLC a dodavatelé se spouštějí ručně.
**Doklad:** `.gitlab-ci.yml:1–12` (ověřeno přímo); `git config core.hooksPath` + `ls .git/hooks`
bez non-sample souborů; `.githooks/pre-commit.ps1:4`; `faze1-inventar.md` sekce 10 (5 sad nástrojů)
vs. `faze1-korekce-hooky.md` (4 hooky, 2 eventy).
**AKCE:** `přeformulovat na` **„brána, kterou nikdo nespouští, je taky jen prompt"** —
s vlastním projektem jako exponátem. Tohle je nejsilnější a nejčestnější verze M-01 a zároveň
odpověď na M-05 a RT-03. Prioritu `must` **ponechat**, ale roli změnit z `výklad+demo`
na `výklad+příběh+demo` (demo = `spec_lint.py` za 0,34 s, příběh = vlastní CI).

### RT-36 — Zrušená metodika TC pro WES není v draftu vůbec, přes 22 smazaných souborů
**Typ:** chybí
**Terč:** chybí — nový (přesah do M-04, X-04, A-08)
**Nález:** Zadání red-teamu tento případ jmenovalo a **ověření ho potvrdilo do souboru**:
`git log --diff-filter=D --all -- "docs/fr/comp/wes/*/tc/*.feature"` dává **přesně 22 smazaných
cest, všechny v jednom commitu `27ea2b6` z 2026-03-17**, tedy ADR-ASK-PROC-009 se s realitou
shoduje na soubor. Dnes v `docs/fr/comp/wes` **není ani jeden adresář `tc/`**. Draft o tomhle
obloukovi **nemá ani jednu položku**, přestože je to nejlepší doložený příběh celého korpusu
o generování artefaktů, které nemá co ověřit („služby nejsou implementované, pojmenování
a parametry neznámé").
**Doklad:** commit `27ea2b6` (2026-03-17), 22 smazaných `.feature`; ADR-ASK-PROC-009;
`docs/fr/comp/wes/**` bez `tc/`; pro srovnání `docs/fr/comp/api` 19 `.feature` (z 105 v repu).
**AKCE:** `doplnit chybějící` námět **„vygeneroval jsem 22 souborů a pak je smazal"** —
blok 3 nebo 5, `must`, 12 min, role příběh. Lekce: *artefakt, který nemá proti čemu být
ověřen, je jen objem*. Je to zároveň nejlepší úvod k M-04 („vykazuj, kolik jsi nezkontroloval")
a k A-08.

### RT-37 — Mrtvý nástroj s dependencí, která nikdy neexistovala
**Typ:** neosvědčilo se
**Terč:** X-06 „Hotový artefakt, na který nic neukazuje, je mrtvý" (`must`, `příběh+demo`)
**Nález:** X-06 má v repozitáři exponát mnohem lepší, než jaký draft uvádí:
`docs/fr/.fr-tools/export_tc.py` — **376 řádků, poslední commit 2026-02-18 (6,2 měsíce),
nula odkazů kdekoli v repozitáři** (ne v `docs/fr/CLAUDE.md`, ne v `README.md`, ne ve
`validate.cmd`, ne v CI, ne v hookách). Jeho deklarovaný výstup `docs/fr/tc-export.xlsx`
**neexistuje**. Jeho závislost `generate_descriptions.py` **neexistovala nikdy v žádné větvi**
(`git log --all` prázdný). A má latentní chybu rozsahu: `COMP_DIR.rglob("*.feature")` na ř. 350
by minul **všech 37 `.feature` pod `docs/fr/bp/`**. Vedle toho živý sourozenec pro kontrast:
`tc-list.py` → `tc-list.csv` (186 kB) commitnuto **2026-08-24**.
**Doklad:** ověřeno v repozitáři (fáze 5, druhé kolo): `export_tc.py` 376 ř., commit `d68f5fc`
2026-02-18, 0 odkazů; `git log --all -- "**/generate_descriptions.py"` prázdný;
`docs/fr/tc-descriptions-cache.json` 51 897 B, naposledy 2026-05-04, jediný referent je
`export_tc.py`.
**AKCE:** `přeformulovat na` demo X-06 s tímto souborem — je to 30 sekund na jevišti
(`grep -r export_tc . | wc -l` → 1) a zabíjí to argument bezpečně, deterministicky, offline.
Doklad, který draft dnes u X-06 používá (CODEOWNERS pokrývá 2 z 3 pluginů), je slabší.

### RT-38 — Podklad fáze 3a nabízí ★★★ demo, které dnes selže
**Typ:** nepředveditelné
**Terč:** kandidát #18 z `faze3a`, dnes vtělený do R-02 / X-06
**Nález:** `faze3a` uvádí jako ★★★ živé demo tvrzení *„`grep -ri "ontolog"` nad `CLAUDE.md`
a `.claude/` vrací 0 výskytů"*. Dnes je to **19 výskytů na 15 řádcích `CLAUDE.md`** (jeden
z nich je nadpis `## Ontologie prvků`, ř. 308) a **77 výskytů pod `.claude/`**. Tvrzení bylo
historickým odůvodněním ADR-ASK-PROC-020, ne stavem k dnešku — draft (a můj vlastní RT-10)
ho ale přebírá jako spustitelný příkaz. Na jevišti by to vyvrátilo položku, která ho používá
jako důkaz.
**Doklad:** `faze3a-alzask-metodiky.md:364–369` vs. přímé přepočítání dnes (19 / 77).
**AKCE:** `vyřadit` ten grep z jakéhokoli dema. Obecnější AKCE pro syntézu: **každé demo
založené na „grep vrací nulu" má datum expirace** — před finalizací materiálu všechna
taková dema znovu spustit a k číslu připsat datum.

### RT-39 — Prázdná sekce PBS 1.3 (UI) a config, který nekonfiguruje nic
**Typ:** neosvědčilo se
**Terč:** K-08 (`must`, `příběh`, 10 min)
**Nález:** Dva exponáty driftu `CLAUDE.md`, oba lepší než ten, který draft dnes používá:
- **`docs/fr/comp/ui/` obsahuje jen `INDEX.md` a `README.md`, nula FR souborů**, poslední
  dotek 2026-06-11. `CLAUDE.md` ji v tabulce struktury vede jako živou oblast (sekce 1.3 PBS).
- **`.claude/rules-config.yaml` je ze 100 % zakomentovaný** — každý klíč vypnutý, poslední
  commit 2026-07-08. Konfigurace, která nekonfiguruje nic, ale načítá se.
- **Deklarovaný cíl `docs/specs/` neexistuje** (root `CLAUDE.md` i `.gitignore:697`); skutečný
  adresář je `docs/spec/` se 13 dokončenými běhy / 175 soubory, ale bez commitu od 2026-07-12.
- **`.claude/settings.local.json` má `skillOverrides: {"therapy": "name-only"}`** pro skill,
  který v repozitáři není definován; `pruzkum` má v celém repu 1 zásah, a to v archivovaném
  běhu spec-factory.
**Doklad:** `ls docs/fr/comp/ui/` → `INDEX.md`, `README.md`; `ls -d docs/specs` → „No such file
or directory", `docs/spec` existuje; `.claude/rules-config.yaml` (samé komentáře, commit `952d427`);
`.claude/settings.local.json`.
**AKCE:** `přeformulovat na` K-08 s **čtyřmi** exponáty místo jednoho a `doplnit chybějící`
praktický závěr: *jednou za měsíc si přečti vlastní `CLAUDE.md` a u každé cesty zkontroluj,
že existuje* (`ls` na každou cestu = 10 řádků skriptu). Bez toho je K-08 jen historka.

### RT-40 — Stárnutí bez brány: 9 nejstarších ADR je `draft`, 32 z 35 FR nemá `updated`
**Typ:** vadný doklad / posílení
**Terč:** M-08 „Práh, který realita trvale překračuje, není signál" (`should`, 10 min)
**Nález:** M-08 má v draftu slabší doklad, než jaký existuje. Skutečnost: **26 accepted /
14 proposed / 11 draft ADR; devět nejstarších je všech devět `draft`, ve věku 4,3–6,1 měsíce**
(nejstarší `ADR-ASK-API-006` z 2026-02-20). **Žádné z 51 ADR nemá neprázdné `superseded_by:`**
a žádné nemá status `superseded`/`deprecated` — tedy „nahrazená" jako stav neexistuje.
U FR: **35 draft / 10 done / 4 in_progress, status `approved` nepoužívá ani jedno FR**, a
**jen 3 z 35 draftů mají vyplněné `updated:`** — pole, na kterém stojí celý práh svěžesti,
je pro celou draftovou populaci prázdné (včetně všech 19 `FR-COMP-*`).
Naopak dobrá zpráva, kterou je čestné říct: **`docs/adr/INDEX.md` je vedený správně** —
0 rozdílů v ID, 0 nesouladů statusu, 0 nesouladů dat, součty souhlasí (26+24+1=51).
Rozbité není účetnictví, ale stárnutí a vynucení.
**Doklad:** ověření v repozitáři (fáze 5, druhé kolo): census ADR 26/14/11, devět nejstarších
`draft` 4,3–6,1 měsíce, 0 z 51 se `superseded_by`; census FR 35/10/4, 3 z 35 s `updated`;
`docs/adr/INDEX.md:71` (drobnost: `ADR-ASK-OVR-001` je `draft`, ale počítá se pod „Override (1)",
ne pod „Navržených (24)").
**AKCE:** `přeformulovat na` „práh 30 dní překročený 56× a pole, ze kterého se počítá, prázdné
u 32 z 35" — to je o řád silnější doklad. A `doplnit chybějící` půlvětu: *warning, který
nikdo nečte, je horší než chybějící kontrola, protože vypadá jako kontrola.*

### RT-41 — bp-overview: kadence vynechala tři týdny v řadě, objem spadl na sedminu
**Typ:** neosvědčilo se
**Terč:** chybí — nový, nebo doklad pro R-02/X-06
**Nález:** Metodika `docs/bp-overview/` předepisuje **týdenní** snapshot. Dnes je ISO týden 35,
nejnovější snapshot pokrývá **týdny 30–32** a WIP soubor byl naposledy commitnut 2026-08-14
(týden 33). **Týdny 33, 34 a 35 nemají snapshot.** Objem po týdnech: T22 = 34 souborů,
T23 = 6, T24 = 6, T25+26 = 8, T27+28+29 = 5, T30+31+32 = 5 — rozpadá se kadence **i** objem.
Předepsaný artefakt `tc-katalog/` se vyskytuje **ve dvou souborech, oba dokumentace** —
tedy je předepsaný jako pravidlo a vyrobený právě jednou.
**Doklad:** ověřeno v repozitáři: `docs/bp-overview/T{NN}/` — nejnovější T30+31+32,
`Prehled_BP_use_cases.md` poslední commit 2026-08-14; `tc-katalog` 2 zásahy v celém repu
(`bp-overview/CLAUDE.md`, `README.md`).
**AKCE:** `doplnit chybějící` sekci do R-02 (nebo nové položky „periodicita, kterou nikdo
nevynucuje, se rozpadne za tři týdny"), `should`, 8 min. Je to třetí nezávislý doklad téže
věci jako RT-03 a RT-04 — a **tři nezávislé doklady dělají z tvrzení konvergenci**, což je
podle vlastní metody draftu nejsilnější signál. Tohle je kandidát na nosné téma celé série,
ne na jednu položku.

### RT-42 — Co se v repozitáři naopak drží (kontra-doklad, aby red-team nebyl jednostranný)
**Typ:** jiné (kalibrace)
**Terč:** draft jako celek
**Nález:** Aby program nebyl sebemrskačský, je potřeba pojmenovat i to, co obstálo:
**všech 15 pravidel v `.claude/rules/shared/` je někde odkazované, nula sirotků**
(`RULE-GOV-001` odkazuje 55 souborů, `RULE-CL-001` 47, `RULE-AP-002` 37); `RULE-SPEC-003`
je **dokumentovaná záměrná mezera v číslování** (`RULE-SPEC-004:42`) — přesně ta praxe,
kterou draft prodává jako „stabilní ID se nepřečísluje"; oba skilly a příkazy
`/dodavatele:*` i `/ontologie:kotvy` jsou správně navěšené (7–9 odkazujících souborů);
oba dodavatelské inboxy obsahují jen `.gitkeep`, tedy invariant „fronta je prázdná" platí;
`/spec` se používá dodnes (31× celkem, naposledy 2026-08-21), `/body-z-jednani` 34×
(naposledy 2026-08-24), `/dodavatele:*` 7× (2026-08-25 a 26).
**Doklad:** ověření v repozitáři (druhé kolo) + `rt_history.py` (data prvního a posledního
použití vlastních příkazů).
**AKCE:** `doplnit chybějící` protipól do programu: **jeden slide „co z toho po sedmi měsících
skutečně žije"** — tři vlastní příkazy s doloženým použitím ještě tento týden vs. tři
subsystémy s nulou. Bez toho publikum odejde s dojmem, že se nic nevyplatí, což data
neříkají. Zařadit na konec bloku 6, `must`, 8 min.

---

## 5. Co red-team NEZPOCHYBNIL (aby bylo jasné, co drží)

Tyto položky mají doklad, nulovou infrastrukturu a snesou i cvičení. Jsou to nejlepší
kandidáti na jádro série, pokud se má škrtat:

| ID | Proč drží |
|---|---|
| A-02 Číslovaný picklist | konvergence 4 nezávislých agentů, 34 doložených použití, nulová cena |
| A-03 Rozpočet na otázky a páka | dvě věty v promptu, doložený vznik ve 4 iteracích |
| A-05 Sebekritika nákladem na údržbu | 7 výskytů; „LLM tenhle dotaz sám nikdy nepoloží" |
| A-07 Redukce na minimální případ | cena *neu*dělání doložena: 30 promptů / 8 kol |
| A-08 Specifikace invariantem | nulová infrastruktura, doložený dopad na verzování |
| A-09 Adresát jako parametr zadání | publikum + zakázaná slova + pravidlo krácení, zdarma |
| A-11 Vyjednej terminologii dřív | doložený spor + `grep -c` jako měřítko zvyku |
| M-05 + M-06 + M-02 jako **trojice** | dohromady revizní protokol bez jediného skriptu |
| X-07 Konvence bez validátoru | živý doklad: dva reálné chybové nálezy v produkčním FR, běh 0,6 s |
| M-01 jako demo | `spec_lint.py` rc=2 s pojmenovaným polem za 0,34 s — nejrychlejší demo v katalogu |
| F-04 51:1 | čísla ověřena nezávisle (`/compact` 51 vs. `/clear` 1 v pracovních projektech) |
| O-04 Pojmenovaná session | `/rename` 29–35×, deterministické, 30 s |

---

## 6. Rozpad draftu podle přepočtu (podklad pro syntézu)

`rt_bloky.py` nad `katalog-draft.md`:

| Blok | Položek | Minut (přepočet) | Minut (deklarováno draftem) | must / should / could |
|---|---|---|---|---|
| 1 | 7 | **88** | 88 | 6 / 1 / 0 |
| 2 | 13 | **145** | 137 ✗ | 8 / 3 / 2 |
| 3 | 17 | **192** | 175 ✗ | 8 / 8 / 1 |
| 4 | 11 | **125** | 125 | 3 / 6 / 2 |
| 5 | 12 | **145** | 156 ✗ | 8 / 4 / 0 |
| 6 | 6 | **72** | 72 | 2 / 4 / 0 |
| **celkem** | **66** | **767 min = 12,8 h** | 753 | 35 / 26 / 5 |

Tři ze šesti bloků má draft špatně sečtené. Samotné `must` položky dávají **444 minut = 7,4 h**.
Při „kratších setkáních" (60–90 min) je to **9 až 13 dílů série** — tj. víc než jedno čtvrtletí
týdenního rytmu. To v draftu nikde nestojí a je to zásadnější než překročení jednoho bloku.

**Odhad úspory po zapracování red-teamu:** −9 slotů a ~90 min zrušením okruhu `X` (RT-01),
−4 položky do infra přílohy (RT-07), −3 vyřazení (N-01, X-09, A-10 → RT-06/RT-01/RT-09),
−1 sloučení (O-02+X-12 → RT-12); +9 nových položek z mezer (RT-18 až RT-27, RT-36, RT-42,
po sloučení ~9 × 10 min = +90 min).
Výsledek: **~58 položek, ~610 minut = 7–9 dílů.** Stále mnoho; druhý průchod bude muset
škrtat podle tabulky v sekci 5, ne podle okruhů.

### Návrh, kterým se to dá zkrátit na tři díly (pokud syntéza chce ostré řezy)

Tři nezávislé doklady (RT-03 revizní pipeline, RT-04 znalostní smyčka, RT-41 bp-overview)
říkají **jednu a tutéž věc**: postavil jsem to, nenavěsil to na rutinu, přestal jsem to
používat. Podle vlastní metody draftu je trojí nezávislá konvergence nejsilnější možný signál —
takže to není položka, ale **nosné téma série**:

| Díl | Téma | Jádro |
|---|---|---|
| 1 | **Co tě to stojí a co nevidíš** | F-01, F-05 (živý `/context`), F-04, RT-18 (plan mode), RT-19 (zpět), RT-20 (citlivá data), F-03 jako výklad |
| 2 | **Zadání: dokument nese kontext, prompt nese rozhodnutí** | K-01, K-02, K-03, R-01 (+X-02), A-02, A-03, A-04, A-05, A-07, A-08, A-09 |
| 3 | **Proč to, co postavíš, přestaneš používat** | RT-35 (brána bez brány), M-02+M-05+M-06 jako protokol bez skriptu, RT-03, RT-04, RT-36, RT-41, RT-24 (co commitnout kolegovi), RT-42 (co žije) |

Všechno ostatní je příloha „pro toho, kdo to bude stavět" (RT-07) nebo materiál na později.
