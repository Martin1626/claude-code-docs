# FÁZE 2d — Destilace praxe z promptů: fhb + myfaber

**Vstup:** `C:\tmp\workshop-namety\_raw\prompty-fhb-myfaber.md` — 218 promptů (fhb 212, myfaber 6), 2026-02-11 → 2026-08-25
**Kontext pro rozpoznání „co se stalo pravidlem":** `C:\Git\fhb\CLAUDE.md`, `C:\Git\fhb\.claude\rules\shared\` (13 pravidel) + `arch-spec\` (1), `C:\Git\alzask\.claude\rules\shared\` (15) — čteno, **nic nezapsáno**
**Analytické skripty:** `analyza_fhb.py`, `analyza_fhb2.py`, `analyza_fhb3.py` (+ `*_out.txt`) v `_raw\`

---

## 0. Tvar vzorku — čti nejdřív, mění to výklad všeho ostatního

| Metrika | fhb+myfaber | pro srovnání alzask (celek) |
|---|---|---|
| Počet promptů | 218 | 1138 |
| Medián délky | **43 znaků** | 65 znaků |
| P75 / P90 | 107 / 193 | 166 / 365 |
| Promptů > 500 znaků | **6** (2,8 %) | — |
| Promptů > 1000 znaků | **2** (6240 a 3344) | 31 v celém logu |
| Slash příkazy | 64 (29 %) | — |
| Unikátních sessions | 39 (fhb) + 2 (myfaber) | 176 |
| Dní s aktivitou | **21** | — |

**Rozložení do dnů je extrémně nerovné.** Dva dny — 2026-06-26 (52) a 2026-06-27 (47) — nesou **99 promptů, tj. 45 % celého vzorku**. Další shluky: 07-04/05 (27), 07-07 (14), 08-20/21 (18).

**Tematické rozdělení (vlastní klasifikace, překryvy možné):**

| Typ | Počet | Podíl |
|---|---|---|
Doménová práce (nosiče, dopravníky, porty, WMS/WES/WCS, API) | 25 | 11 % |
| Meta/nástroje (plugin, marketplace, git, worktree, settings, outputStyle, session) | 51 | 23 % |
| Učící dotazy („co je", „jak funguje", „vysvětli") | 20 | 9 % |
| Slash příkazy a šum (`test`, `exit`, `a`, `2`) | ~85 | 39 % |

> **Nejdůležitější zjištění o vzorku:** fhb **není v promptech doménový projekt**. Je to **laboratoř, kde se stavěly nástroje** (Spec Factory → plugin, knowledge loop, outputStyle) **a kde se vynalezla praxe komunikace s dodavatelem**. Doménového obsahu je v promptech jedenáct procent. To je pro workshop dobrá zpráva — přenositelné jsou právě ty postupy, ne doména.

**Limity vzorku (přiznávám je, protože mění dvě odpovědi):**
1. **Prompty nejsou úplný záznam vzniku praxe.** `RULE-ARCH-001` má `date: 2026-06-10`, `RULE-API-002/003/005` mají `source: schůzka 2026-06-15`. Ve vzorku **není ani jeden fhb prompt z 06-11 až 06-17**. Nejsilnější metodika fhb (grounding disciplína arch-spec, konvence API) vznikla mimo zachycený log — z jednání a ze sessions, které se do `history.jsonl` nedostaly. Kdo bude soudit praxi jen z promptů, tuhle vrstvu neuvidí.
2. **Které 6 promptů je `myfaber` není v souboru vyznačeno.** Z měsíčních součtů (myfaber 2026-02 = 1, 2026-06 = 5; 2 sessions) vychází jednoznačně: `2026-02-11 13:24 /resume` + pětice na `2026-06-10` a `2026-06-18 09:19`. Označuji to jako **odvození, ne doklad**.

---

## 1. Co se přeneslo z AlzaSk do fhb

### 1.1 Přeneslo se celé lešení projektu — a to beze zbytku jediného promptu

`C:\Git\fhb\CLAUDE.md` (366 řádků) je **strukturní klon** `C:\Git\alzask\CLAUDE.md`: stejné sekce, stejné tabulky, stejné formulace. Doslovně shodné pasáže:

- „Oba repozitáře musí ležet jako sourozenci ve stejném nadřazeném adresáři." + tabulka cest
- „Při práci s ADR nebo dokumentací **vždy zohledni oba repozitáře**. Čti kontext z obou, zapisuj do toho správného."
- celá sekce **Práce s ADR** — kategorie DB/API/INT/PROC/HW/OVR, tabulka „Kdy vytvořit ADR zde vs. v myFABER", override postup s `overrides:` / `override_type:`, „Postup při zpracování přepisu jednání" (5 kroků), „Sekvenční čísla" (projdi → najdi nejvyšší → +1 → tříciferný)
- **Pravidla:** „Nikdy nezapisuj globální ADR (ADR-MF-*)", „Nikdy automaticky nesupersedeuj bez potvrzení uživatele", „Pokud si nejsi jistý scope → zeptej se", „Changelog je povinný"
- celá sekce **Hygiena repozitáře** (`temp/`, soubor `nul`)
- celá sekce **Projektový asistent** — „NIKDY neodpovídej na dotazy k projektu z vlastních znalostí", detekce režimu UČENÍ vs. DOHLEDÁNÍ včetně seznamů trigger frází, `soubor:řádek` u každého tvrzení
- **Terminologie:** „Nosiče/carriers = containers, Svozy = transports"
- FR metodika: identifikátory `FR-COMP-{KATEGORIE}-{OBLAST}-{SEQ}`, `.fr-tools/validate.py`, „Scope: FR metodika je čistě projektová"

**Doklad, že to nešlo přes prompty:** ve vzorku není žádný prompt typu „založ mi CLAUDE.md" ani „převezmi metodiku z alzask". Přenos byl **kopie souborů rukou**, mimo Claude. Nejbližší prompt, který na to ukazuje, je až doménový: *„V API chybí POST DELETE na container. Chtěl bych to udělat obdobně, jako v C:\Git\alzask\docs\api. Je potřeba doplnit i do diagramu."* (2026-06-23 12:34).

### 1.2 Přenesla se pravidla — batch kopií 10.–11. 7.

Průnik `shared/` obou repozitářů = **10 pravidel**: AP-001, AP-002, CL-001, DIAG-001, GOV-001, GOV-002, META-001, SPEC-001, SPEC-002, TERM-001.
U čtyř z nich je **velikost souboru bit-shodná** (AP-002 3343 B, GOV-002 2390 B, META-001 2049 B, SPEC-001 2871 B) → doslovná kopie.
Časové značky: alzask `shared/` = 2026-07-10 14:49, fhb `shared/` = 2026-07-11 21:08. **Jedna akce, dva repozitáře, do 32 hodin.**

U šesti se soubory rozešly a **v obou směrech**: `DIAG-001` je v alzask výrazně větší (3084 vs 1914 B — alzask ho dál rozvíjel po Mermaid nálezech), `GOV-001` je naopak větší v fhb (2828 vs 1979 B), `SPEC-002` větší v alzask (1899 vs 1081 B). To znamená: **kopie se po rozdělení už nikdy nesladily.**

### 1.3 Přenesl se způsob zadávání — a to prokazatelně

Nejstarší alzask prompt (2026-01-29 23:25) končí trojicí:
> „Uprav všechna související místa, včetně webhooků. … Inkrementuj verzi a popiš všechny změny. / Jsou nějaká další obdobná místa? / Otázky?"

Tři návyky, které se v fhb objevují znovu:
- **„a promítni to i do navazujícího artefaktu"** → fhb 2026-06-23 12:34: „Je potřeba doplnit i **do diagramu**."; 2026-07-07 15:37: „Doplň do odpovědí, **kde to není jednoznačně zřejmé**."
- **„Otázky?" / „zeptej se"** → fhb 2026-07-07 10:59: „**Pokud jsou nějaké otázky, zeptej se.**"; 2026-08-14 20:13: „Když si nejsi jistý, zda jde o rozpor nebo o mé nepochopení, napiš to a **zeptej se** — nedomýšlej si výklad, aby rozpor vyšel."
- **verze + popis změn** → fhb 2026-06-27 17:31: „proveď bump verze v yaml souboru na 2.1.1"; 18:12: „V yml chci změnu ve verzích popisovat pomocí `changes: - feature:`"

### 1.4 Přenesl se i směrem OPAČNÝM — a to je nejsilnější doklad celého vzorku

**Šablona „N vrstev jednoho popisu" vznikla ve fhb a za 16 minut byla nasazená na alzask.**

| Čas | Projekt | Co |
|---|---|---|
| 2026-08-14 19:36 | fhb | 1. verze, 3052 znaků (dle `faze1-statistiky.md`) |
| 2026-08-14 20:13 | **fhb** | 2. verze, **3344 znaků** — tři vrstvy: KONCEPT / KONTRAKT / NÁVOD (ve vzorku) |
| 2026-08-14 20:29 | **alzask** | **5280 znaků** — dvě vrstvy: TOK / KONTRAKT, + přidané bloky `CO NEČÍST` a `ROZHODČÍ`, + rozpočet otázek |

Šablona se při přenosu **nezkopírovala, ale vyrostla**. To je jiná kvalita přenosu než u pravidel: tady se metodika vylepšila tím, že prošla druhým projektem.

### 1.5 Přenesla se Spec Factory — z fhb do pluginu, tedy ke všem

Explicitní prompt, kterým to začalo (2026-06-26 23:46):
> „/spec Analyzuj vytvoření Spec Factory pluginu. Myslím, že **v projektu FHB mám komplexnější schopnosti spec factory než v Alza, ale Alza může mít něco, co FHB nemá. Chci najít rozdíly a rozumně sjednotit.**"

a předtím (2026-06-26 22:02): „Jaké jsou rozumné možností **sdílení Spec Factory mezi projekty FHB, Alza a dalšími**?"

Tohle je učebnicový moment: dva projekty se rozešly, autor si toho všiml, **nechal si rozdíl vypátrat a sjednotit**, a výsledek vytáhl z projektu do pluginu. Výsledek je doložený i v metadatech pravidel: `RULE-API-002/003/005` mají `source_project: FHB` a v tabulce Stopa použití řádek „2026-07-07 | spec-factory | generalizace draftu z _personal do pluginu".

---

## 2. Co se NEpřeneslo — a jestli to má důvod

**Doložený mechanismus přenosu = ruční kopie souborů.** Ověřeno: `C:\Git\shared\` obsahuje `plugins/` a `docs/`, **žádnou složku `rules`**. Přesto obě CLAUDE.md v precedenci uvádějí vrstvu „cross-project `shared`". Ta vrstva **na disku neexistuje**. Plugin `knowledge-loop` nese jen mechaniku (`commands/rule-new.md`, `templates/RULE-template.md`) — žádná obsahová pravidla, a to úmyslně („Mechaniku vlastní plugin; tento repozitář vlastní obsah"). Důsledek: **obsahová pravidla mezi projekty neprotékají, dokud je člověk nezkopíruje.**

### 2.1 Nepřeneslo se do fhb (a je to nedotažené, ne odůvodněné)

| Co | Kde žije | Proč to ve fhb chybí |
|---|---|---|
| **Registr dotazů dodavatelů** (`docs/suppliers/`, ID `PRE-*`/`PORT-*`, `questions.yaml`, skill, 3 slash příkazy) | alzask | **Nejbolestivější případ. Praxe se ZRODILA VE FHB** (viz 3.1), alzask ji zprůmyslnil na registr — a fhb registr nikdy nedostal zpět. Bez důvodu, jen nedotaženo. |
| **VTT → MD konverze přepisů** + `docs/meetings/CLAUDE.md` | alzask | fhb CLAUDE.md stále říká „Formát názvu souboru: `YYYY-MM-DD název schůzky.vtt`". Přitom fhb prompty se o přepisy opírají (`@docs/meetings/2026-06-26_...md` — **soubor už je .md**, dokumentace lže). Čistý drift. |
| **Ontologie prvků** (`docs/ontology/`, `ADR-ASK-PROC-020`, skill, 3× RULE-ONT) | alzask | Vzniklo 2026-08-22, fhb má v srpnu 27 promptů — nestihlo se. Obhajitelné mládím, ne rozhodnutím. |
| **PLC specifikace + `plc-lint.py`** | alzask | **Legitimní doménový důvod.** fhb má rozhraní na dodavatele přes API (WCS/MCS, ASRS v2), ne přes datové bloky PLC. Kolegovi bych to jako „nepřenesené" nepředkládal. |
| **`docs/pbs/pozadavky.md`** (mapování PBS ↔ `ALZA.SK-R000XX` ↔ FR) | alzask | Není doloženo, že fhb má PBS ve stejné podobě. Nerozhodnuto. |
| **`bp-overview/T{NN}`** týdenní snapshoty | alzask | fhb má **funkční ekvivalent jinak** — `arch-spec/snapshots/` + `freeze-snapshot.py` (SHA pin před předáním zákazníkovi). Stejná potřeba, dvě řešení. |
| **RULE-SPEC-004** (model před hromadnou aplikací), **RULE-TC-001** | alzask | Nepřeneseno; SPEC-004 je přitom čistě metodické a fhb by ho použil stejně. |

### 2.2 Nepřeneslo se z fhb do alzask (opačný směr, stejná diagnóza)

| Co | Proč to stojí za pozornost |
|---|---|
| **arch-spec: arc42 v9.0 + C4 + DDD Event Storming** s vlastní **grounding disciplínou** | fhb-only. Alzask nikdy nepotřeboval architektonický deliverable — obhajitelné. |
| **Snippet-based citace `[TAG §sekce "3–6 slov doslovně"]`** (RULE-ARCH-001) | **Tady je vidět rozvětvení cesty.** fhb zvolil citaci obsahem — „content-based (stabilní vůči line/rename rot)". Alzask zvolil `soubor:řádek` a k tomu si musel postavit `cite.py` + `reanchor.py --check/--apply` na dorovnávání posunutých čísel řádků. **Dvě odpovědi na stejný problém: fhb ho obešel návrhem, alzask ho vyřešil nástrojem.** Pro workshop je to nejlepší dvojice na diskusi. |
| **Allow-list grounding zdrojů + zakázané zdroje s datem rozhodnutí** (`arch-spec/CLAUDE.md`: „`docs/api/BlueSword/` — rozhodnutí architekta 2026-04-18") | Zákaz **s datem a autorem rozhodnutí** je lepší než pouhý zákaz. Do alzask se nedostal. |
| **„Jeden prompt = jedna arc42 sekce; nikdy »přečti celý repo a napiš spec«"** | Nejpřenositelnější věta z celého fhb. V alzask CLAUDE.md nikde. |
| **`RULE-API-002/003/005`** | Vznikly ve fhb, v metadatech mají „generalizace do pluginu" — ale **v pluginu na disku nejsou** a v alzask `shared/` také ne. Stopa použití tvrdí povýšení, které nedoputovalo. **A pozor:** `RULE-API-005` říká „Žádný `oneOf` ani `discriminator`", zatímco alzask API je na `oneOf` + discriminator postavené (`ContainerUpsertRequest` = oneOf 6 variant). Kdyby se to povýšení bylo povedlo, shodilo by sesterský projekt. |

### 2.3 Verdikt na otázku 2

Kromě **PLC** (doména) a **arch-spec** (jiný deliverable) není za nepřenesenými věcmi žádný důvod. Je za nimi **absence mechanismu**: kopie souborů rukou, jednorázově, bez záznamu směru a bez pozdější synchronizace. Přenos proběhl 10.–11. 7. jedním nárazem a od té doby už nikdy.

---

## 3. Bylo zadávání v fhb od začátku lepší?

**Ano, a měřitelně — ale ne proto, že by se autor „naučil promptovat". Proto, že do fhb vstoupil s hotovým lešením.**

### 3.1 Vůbec neproběhla fáze rozkoukávání

Rané prompty alzask (2026-01-29, prvních 14 promptů celého H1):
- `/help`, `/agents` — orientace v nástroji
- „Uprav @API/API-myFABER-WES-AlzaSk.yml" — **prázdné zadání**, 28 znaků, žádný cíl
- pak 3× **doslovně tentýž** 700znakový prompt (23:25, 23:52, 23:52) — opakované odesílání téhož
- „JAk změním barvu prostředí v terminálovém režimu claude code?"

Rané prompty fhb (2026-04-27, první doménový den):
> „**Varianta A**: Volání Wh orderUnloadRequest a navazující operace jsou povinné pouze v případě, že dopravník je řízený WMS a ne WES. Varianta A však popisuje situaci, kdy předávání nosiče z robota na dopravník řídí WES (toto předávací místo ještě není portem). Port je až na konci dopravníku, kde nosič odebírá operátor. **Uprav proto variantu A tak, že** povolování vyložení nosiče na dopravník ještě řídí WES."

To není začátečnický prompt. Má **stav světa → rozpor → cílenou opravu**, odkazuje na pojmenovaný artefakt (Varianta A/C), rozlišuje předávací místo od portu. **Ve fhb chybí prompt typu „Uprav X" bez cíle úplně.** Chybí i orientační `/help`, `/agents`.

### 3.2 Co se ale nezlepšilo ani přenosem

Praxe **se nepřenesla lineárně** — tři konkrétní návyky z alzask v fhb chybí nebo jsou slabší:

| Návyk | alzask | fhb |
|---|---|---|
| Uzavírací „Otázky?" | nejstarší prompt vůbec | **2 výskyty ze 218** |
| Požadavek na citace | v CLAUDE.md jako závazné pravidlo | **1 prompt** (08-14 20:13) |
| Dlouhé strukturované zadání | 31 promptů > 1000 zn. v celém logu | **2 promptů** ze 218 |

A jeden návyk se přenesl i s vadou: **opakované odesílání téhož promptu**. alzask 2026-01-29 (3× tentýž), fhb 2026-07-04 22:12/22:13 (dvě verze o 60 s) a 2026-07-09 16:24 dvakrát („Napiš potenciální námitky, které Zdeněk může mít" — poprvé bez přílohy, podruhé s 122řádkovým vloženým textem). Za osm měsíců praxe se to nezměnilo.

### 3.3 Odpověď na otázku 3

Zadávání v fhb bylo od začátku lepší **na startu** (přeskočená fáze rozkoukávání, hotové lešení, doménová přesnost) a **horší v průběhu** (kratší prompty, méně struktury, minimum uzavíracích a groundingových instrukcí). Nejlepší prompty vzorku vznikly až v srpnu (08-14) — a ty se okamžitě vrátily do alzask. **Kvalita necestuje s člověkem plynule, cestuje ve skocích s konkrétní šablonou.** To je pro workshop klíčové: kolegovi nepomůže „nabraná praxe", pomůže mu **konkrétní přenositelný artefakt**.

---

## 4. Práce v produktovém repozitáři (myfaber)

**6 promptů, 2 sessions, nula doménového obsahu.** Odvozený seznam (viz limit v §0):
- `2026-02-11 13:24` — `/resume`
- `2026-03-03 22:23/22:25/22:27` (pozn.: v měsíčním rozpadu jde o fhb, uvádím kvůli povaze) — „Je claude instalovaný nativně? (curl/irm)?" / „Co je potřeba udělat pro přeinstalaci a jaké to bude mít důsledky?" / `exit`
- `2026-06-10 10:27/10:31/10:31` — `/memory`, `exit`, `exit`
- `2026-06-18 09:19` — `/resume` + „Co znamená přesune editace do worktrees?"

**Povaha: čistá domácnost.** Ani jeden prompt nesahá na obsah produktu — žádné ADR, žádný datový model, žádný kód.

**Jak se tedy s myfaber pracuje?** Křížovým čtením z projektového sezení, ne vlastní session. Doklad:
- obě CLAUDE.md: „Oba repozitáře musí ležet jako sourozenci… **Čti kontext z obou, zapisuj do toho správného.**"
- alzask CLAUDE.md: `../myfaber/Docs/adr/`, `../myfaber/yamlModels/Wes/`, `../myfaber/WesApp/` jako **zdroje pro čtení**
- alzask prompty (grep na „myfaber"): 50 výskytů, opakovaně `myfaber\Projects\Instalation\Alza\DEV\initData` a `../myfaber/DbModels/Wes/Tables/` — **cesty pro čtení kontextu**
- validace ADR se z projektu volá **do** produktu: `python ../myfaber/Docs/adr/.adr-tools/validate.py --config docs/adr/.adr-tools/config.yaml --project alzask`

**Zapisovací zóna je oddělená hranou, ne důvěrou v opatrnost.** Pravidlo je v CLAUDE.md tvrdé: „Nikdy nezapisuj globální ADR (ADR-MF-*) do tohoto repozitáře — ta patří do myFABER", plus rozhodovací tabulka „Kdy vytvořit ADR zde vs. v myFABER" se čtvrtým řádkem „Nejsi si jistý → **Zeptej se uživatele**".

**Přenositelný závěr pro kolegu (klidně nejlepší z celé fáze):**
> Produktový (sdílený) repozitář drž jako **read-only kontext**, otevřený cestou `../`, ne jako pracoviště. Zápis do něj nech projít lidským rozhodnutím o scope. Konkrétní tvar: v projektovém CLAUDE.md tabulka „platí jen pro projekt / platí pro platformu / projekt potřebuje jinak / nejsi si jistý → zeptej se" a k tomu prefix ID (`ADR-ASK-*` vs. `ADR-MF-*`), který nedovolí splést zónu.

---

## 5. Kandidáti — přenositelná praxe

Značení: **[P]** = přenositelné (kolega si odnese bez mých validátorů, pluginů a repozitáře) · **[P/i]** = přenositelné jádro + moje infrastruktura jako nadstavba · **[infra]** = bez mé výbavy nefunguje · **[Z]** = osobní zvyk

---

### K1 — Vrstvový audit: „přečti tyto N dokumenty jako N vrstev popisu jedné a téže věci" ⭐ hlavní artefakt
**Co to je.** Místo „zkontroluj konzistenci" pojmenuješ každému dokumentu **roli ve výkladu jedné věci** a necháš hledat rozpory **na hranicích mezi rolemi**, ne uvnitř textů.
**Doklad (2026-08-14 20:13, 3344 zn.):** „Přečti tyto tři dokumenty … jako tři vrstvy popisu jedné a téže věci: KONCEPT — záměr: co a proč to má dělat / KONTRAKT — tvar dat: co skutečně projde / NÁVOD — jak to má druhá strana použít"
**Opakování:** 3× během 53 minut, s růstem: 19:36 (3052 zn., fhb) → 20:13 (3344 zn., fhb) → 20:29 (5280 zn., **alzask**, dvě vrstvy TOK/KONTRAKT).
**[P]** — je to čistý text promptu. Role si kolega pojmenuje sám podle svých dokumentů (např. ZADÁNÍ / SMLOUVA / MANUÁL). Nepotřebuje nic z mé výbavy.
**Okruh:** A (jádro) + K + M
**Předvedatelnost:** ★★★★★ Pusť naživo na dva libovolné dokumenty účastníka. Ukaž kontrast: nejdřív „zkontroluj, jestli si ty dokumenty neodporují" (dostaneš seznam překlepů), pak vrstvovou verzi (dostaneš tři rozhodnutí).

---

### K2 — Blok `CO NEČÍST` — zakázané zdroje, s důvodem u každé položky
**Co to je.** Výslovný negativní seznam. Ne „ignoruj staré verze", ale položkový výčet, kde u každé stojí **proč** a kdy se do ní přesto smí sáhnout.
**Doklad (2026-08-14 20:13):** „Složku snapshots/ ignoruj — **jsou to starší verze, ne platný stav**; sáhni tam jen když potřebuješ doložit, kdy se něco změnilo." — alzask varianta (20:29) je ještě lepší: „`podepsaná-verze\**` — zmražený baseline z 2026-01-30; **rozdíl proti němu NENÍ nález, je to vývoj.**"
**Opakování:** 2× (obě verze šablony) + strukturně totéž v `arch-spec/CLAUDE.md` jako allow-list se zákazy: „`docs/api/BlueSword/` (rozhodnutí architekta 2026-04-18)".
**[P]** — čistý text. Věta „rozdíl proti X není nález, je to vývoj" ušetří půl reportu falešných nálezů a nepotřebuje nic než vědět, co ve svém repu člověk má.
**Okruh:** K
**Předvedatelnost:** ★★★★★ Nejlepší demo celého workshopu: pusť audit **bez** bloku (Claude nahlásí 10 „rozporů", 7 z nich proti zmražené staré verzi), pak **s** blokem.

---

### K3 — Blok `ROZHODČÍ` — než se mě zeptáš, ověř, jestli to už není rozhodnuté
**Co to je.** Vyjmenuješ zdroje, které mají autoritu rozhodnutí (ADR, zápis, testy). Nález, který je v nich pokrytý, **není otázka, ale porušení rozhodnutí** — a Claude to má rovnou napsat, ne se ptát.
**Doklad (2026-08-14 20:13):** „Jako **rozhodčí** měj po ruce ADR-ASRS-API-001-design-decisions.md. … Verdikt ADR: je to už rozhodnuté? Pokud ano, **není to otázka pro mě, ale nesoulad s rozhodnutím** — označ, která vrstva rozhodnutí porušuje, a rovnou to napiš. **Otázku pokládej jen tam, kde rozhodnutí chybí.**"
**Opakování:** 2× ve šablonách. V alzask verzi rozšířeno o důmyslný signál: „existence TC je signál, že chování je dotažené, jeho absence u bohatě rozepsané pasáže signál opačný."
**[P]** — pojmenování rozhodčího je text. „Rozhodčím" může být zápis z porady, e-mail, smlouva.
**Okruh:** K + M
**Předvedatelnost:** ★★★★☆ Ukázat na dvojici nálezů: jeden se vrátí jako otázka, druhý jako „porušuje rozhodnutí XY, oprav takto".

---

### K4 — Výstupní kontrakt: „u každé vrstvy citace, nebo výslovně »mlčí«"
**Co to je.** Formát odpovědi vynucuje, že se **žádná vrstva nesmí vynechat**. Nemluví-li o věci, musí to být napsané.
**Doklad (2026-08-14 20:13):** „Stav ve VŠECH TŘECH vrstvách — u každé buď citace `soubor:řádek` s doslovným úryvkem, nebo explicitně »mlčí«. **Nikdy nevynech vrstvu proto, že o věci nemluví; to je součást nálezu.**"
**Opakování:** 2× (obě šablony). Sesterská instrukce: „Nic z paměti ani z obecné znalosti ASRS/WMS/OpenAPI. **Každé tvrzení citací.**"
**[P]** — čistě formátový požadavek. Funguje s jakýmikoli dokumenty.
**Okruh:** M + K
**Předvedatelnost:** ★★★★☆ Ukaž tabulku výstupu se sloupcem „mlčí" — vizuálně okamžitě čitelné.

---

### K5 — „Ticho je nález, ne absence nálezu"
**Co to je.** Zvláštní kategorie zjištění: dvě vrstvy věc řeší, třetí o ní neví. A druhá polovina věty: **ověř, jestli není mlčení záměrné.**
**Doklad (2026-08-14 20:13):** „D) MLČENÍ JEDNÉ VRSTVY — dvě vrstvy věc řeší, třetí o ní neví. **Ticho je nález, ne absence nálezu; ověř, zda není mlčení záměrné.**" A vedle ní: „E) NEDOURČENÍ — chování je otevřené (TODO/OQ), ale ostatní vrstvy na něm už staví jako na rozhodnutém."
**Opakování:** 2× (v alzask verzi jako kategorie G a H z osmi).
**[P]** — nejcennější **myšlenkový** nástroj vzorku. Nepotřebuje nic.
**Okruh:** A
**Předvedatelnost:** ★★★★★ Skvěle se vysvětluje bez počítače: „nejhorší chyba ve specifikaci není špatná věta, je to chybějící věta — a tu nenajdeš tím, že budeš čtený text porovnávat."

---

### K6 — Uzavřené otázky s variantami (a)/(b)/(c), s doporučením a s rozpočtem
**Co to je.** Neptej se otevřeně. Každá otázka má varianty, u každé varianty **jednu větou důsledek**, jedna je doporučená, a celkový **počet otázek je rozpočet**, který se rozděluje podle páky.
**Doklad (2026-08-14 20:13):** „Otázka pro mě: max 2 na nález, **uzavřené, s variantami (a) / (b) / (c)**. U každé varianty jednou větou, co se změní ve které vrstvě, když ji zvolím. Označ, kterou doporučuješ a proč. **Chci umět odpovědět písmenem.**"
Alzask verze (20:29) přidává rozpočtování: „nejvýš 5 CELKEM za všechny tři nálezy. **Nerozděluj je rovnoměrně. Rozpočet utrať podle páky** … Nález, u kterého je odpověď zřejmá z citací, otázku nepotřebuje vůbec."
**Opakování:** 2× jako instrukce; **a v praxi zpětně 6×** — autor pak skutečně odpovídá jen čísly/písmeny: „Proveď: 1, 3" (08-24 12:31), „otázky 20, 21" (06-26 23:14), „10 a 16 vyřaď" (06-26 23:15).
**[P]** — nejrychlejší návratnost z celého seznamu. Jedna věta v promptu („chci umět odpovědět písmenem") zkrátí kolo o desítky minut.
**Okruh:** A + U
**Předvedatelnost:** ★★★★★ Naživo: stejná analýza dvakrát, jednou s otevřenými otázkami (dostaneš esej), jednou s (a)/(b)/(c) (odpovíš třemi znaky).

---

### K7 — Řadit podle páky, páku definovat, a přebytek nezahodit
**Co to je.** Ne „najdi problémy", ale „najdi 3 s nejvyšší pákou", **kde páka je v promptu definovaná výčtem toho, co se změní** — plus záchranná síť na to, co se do trojice nevešlo.
**Doklad (2026-08-14 20:13):** „Vytipuj 3 body s **nejvyšší pákou** … Páka = kolik konkrétních věcí se změní podle toho, jak odpovím (schémata, endpointy, enum hodnoty, povinná pole, stavové přechody, chybové kódy, pasáže README). **Ne »co je nejasné«, ale »co drží nejvíc navazujícího«.**" … „Seřaď nálezy podle páky, ne podle pořadí v dokumentech." … „Pokud najdeš víc než 3 takové body, uveď na konci jednořádkový seznam těch, které se do trojice nevešly, **ať mi nezmizí**."
**Opakování:** 2×.
**[P]** — a je to zároveň nejlepší lék na „dostal jsem 40 nálezů a nevím, kde začít".
**Okruh:** A + M
**Předvedatelnost:** ★★★★☆ Ukázat výčet „co z toho vychází" u nálezu #1 (14 dotčených míst) vs. #3 (2 místa) — pořadí se obhájí samo.

---

### K8 — Read-only režim: „Nesahej na žádný soubor"
**Co to je.** Explicitní zákaz zápisu v analytickém promptu, ne spoléhání na to, že Claude sám nezasáhne.
**Doklad (2026-08-14 20:13):** „**Nesahej na žádný soubor. Žádné návrhy oprav, žádné editace.**"
**Opakování:** 2× (obě šablony) + tři varianty téhož jinými slovy: „Vysvětlí **nejprve jen zde do chatu** co dělá kontejnerRemoved" (06-27 18:09), „Formuluj závěry … **zde do chatu**" (07-07 14:58), „**Připrav jen návrh, vyberu co implementovat**" (08-21 11:34). **Celkem 5 výskytů.**
**[P]** — jedna věta, nulová infrastruktura. (Moje verze má za sebou guardy a `protect_list` — to je **[infra]** nadstavba, ne podmínka.)
**Okruh:** M + N
**Předvedatelnost:** ★★★★★ Přesvědčivé demo: pusť analytický prompt bez té věty, ukaž `git diff` po analýze.

---

### K9 — Návrh → picklist → „Proveď: 1, 3"
**Co to je.** Dvoutakt. Nejdřív **jen návrh** s číslovanými body, člověk vybere čísla, pak se implementuje jen vybrané. Nikdy „navrhni a udělej".
**Doklad (2026-08-21 11:34):** „Zkontroluj a navrhni, které z těchto závěrů by bylo potřeba podchytit do @…koncept.md. **Připrav jen návrh, vyberu co implementovat.**" → a skutečné vyzvednutí: „Zapracuj tyto body včetně mého upřesnění … 1) … 2) OK 3) OK 4) OK 8) OK 9) OK 12) …" (08-21 12:24), „**Proveď: 1, 3**" (08-24 12:31), „Formuluj … závěry …, které budou zahrnovat tyto body: 1, 2, 3, 4, 5, 7, 10, 11, 22, 30, 31, 32, 33, 34, 38, 39, 41" (08-21 10:58)
**Opakování:** **6×** — nejčastější strukturní vzor vzorku po slash příkazech.
**[P]** — jádro je čistá praxe. `/body-z-jednani` (4× ve vzorku) je moje **[infra]** zkratka k témuž; kolega vystačí s „vypiš to jako číslovaný seznam, vyberu si".
**Okruh:** O + A
**Předvedatelnost:** ★★★★★ Nejsnáz předvedeníhodná věc vůbec. Zápis z porady → číslovaný picklist → „Proveď: 2, 5, 9".

---

### K10 — Dvoufázový překlad: nejprve česky, po odsouhlasení přeložíme
**Co to je.** U textu pro cizojazyčného adresáta se **nejdřív schválí obsah v rodném jazyce** a teprve pak se překládá. Nikdy se nedebatuje nad anglickým/čínským draftem.
**Doklad (2026-07-07 10:59):** „**Odpovědi mi připrav nejprve v češtině. Po odsouhlasení teprve přeložíme.**"
**Opakování:** doložený vzor napříč 6 překladovými prompty: 06-26 21:44 („Potom přelož zároveň otázku do čínštiny" — tedy až po opravě formulace), 06-26 19:04, 07-07 15:22, 08-19 (alzask), 08-25 09:08 („Přelož do angličtiny … Nové md soubory označ dnešním datem").
**[P]** — a v prostředí, kde se komunikuje s cizím dodavatelem, uspoří kolo revizí na každé otázce.
**Okruh:** A
**Předvedatelnost:** ★★★★☆ Ukázat na jedné otázce, jak jinak se opravuje česká věta než anglická.

---

### K11 — Adresát jako omezení stylu + krátký název ke každé otázce
**Co to je.** Do promptu patří, **kdo to bude číst** — a z toho plyne požadavek na jazyk. Plus: každá otázka dostane krátký identifikační název.
**Doklad (2026-06-26 21:24):** „Potřebuji je formulovat **jednoduše, přesně a srozumitelně, aby jim rozuměli čínští dodavatelé**." + (21:44) „**Ke každé otázce vytvoř stručný název, podle kterého se dá otázku srozumitelně identifikovat.**"
**Opakování:** „stejně jako minule" ve 07-07 10:59 to potvrzuje jako ustálený vzor; 3 výskyty. Doplňkově 07-07 10:59: „Poznámky: **náš systém WES je u BlueSword označován jako WMS. Jejich systém MCS my označujeme jako WCS.**" — mapování terminologie mezi stranami dodané rovnou v promptu.
**[P]** — dvě věty, žádná infrastruktura. „Mapa pojmů obou stran" je mimořádně užitečná u každé integrace.
**Okruh:** A + K
**Předvedatelnost:** ★★★★☆ Stejná otázka pro „vývojáře v týmu" vs. „dodavatele, který nemá kontext" — rozdíl je drastický.

---

### K12 — Doslovné znění + stav u každé otázky v jednom promptu
**Co to je.** Největší prompt vzorku (6240 zn.) nese **26 otázek roztříděných do stavů PENDING / NEW / ANSWERED / CLOSED**, každou v doslovném znění, u částečně odpovězených s poznámkou, **co konkrétně chybí**.
**Doklad (2026-06-26 21:24):** „14. In inbound process, how does WCS inform WMS that … could not be read? — **PARTIAL** — We need the webhook with the error (ALARM), so send it WCS->WMS via whErrorReport."
**Opakování:** 1× v této podobě, ale **je to zárodek celého alzask registru dodavatelů** (`questions.yaml`, ID `PRE-*`/`PORT-*`, „co konkrétně v odpovědi chybí", `landed_in`). Praxe se pak v témže vlákně 25× iterovala (viz §7).
**[P/i]** — **stavová disciplína je přenositelná okamžitě** (stačí markdown se čtyřmi nadpisy) a je to přesně ta hodnota. `questions.yaml` + `questions.py --check --build` + skill je **[infra]** — pro workshop ukázat jako „kam to dojde, když se to vyplatí", ne jako vstupní požadavek.
**Okruh:** A + K (registr do R)
**Předvedatelnost:** ★★★★☆ Ukázat markdown se 4 stavy vedle `OTEVRENE.md` z alzask — je vidět, že je to totéž o rok později.

---

### K13 — Vlastní paměť jako podklad, ale s příkazem ji ověřit
**Co to je.** Autor napíše, co si pamatuje, **označí to jako paměť** a výslovně nařídí verifikaci proti zdroji. Nezamlčí nejistotu, ani ji nenechá projít.
**Doklad (2026-06-27 17:15):** „isActive=false by mělo být v situaci, kdy nosič je mimo storage zone … **Myslím že aspoň takto jsme se na tom domlouvali, ale ověř to ještě v zápisech ze schůzek.**"
Druhý výskyt (2026-07-07 14:58): „Formuluj závěry … **Co si pamatuji:** WMS se musí vždy dozvědět o tom, co bylo načteno. …"
**Opakování:** 3×.
**[P]** — a je to protipól k pravidlu „neodpovídej z paměti", tentokrát aplikovaný **na sebe**. Silný didaktický moment: disciplína platí pro oba účastníky rozhovoru.
**Okruh:** K + U
**Předvedatelnost:** ★★★★☆ Ukázat, jak Claude paměť opraví („v zápisu z 15. 6. je to jinak, cituji…").

---

### K14 — Handoff mezi sessions přes soubor
**Co to je.** Když má práce přesáhnout jedno okno nebo jeden repozitář: **nechej si napsat plán/prompt do souboru** a spusť ho v samostatné session.
**Doklad (2026-07-09 14:58):** „Chci rozdělit do striktně oddělených bloků … Pokud zjistíš, že je potřeba provést úpravy i v C:\Git\shared\plugins, tak **připrav pro to plán a ulož jej, abych jej mohl spustit v samostatné session**."
Druhá strana téhož: „**Implementuj podle @docs/spec/2026-06-26_spec-factory-plugin-sjednoceni/implementation-prompt.md**. Plugin dočasně ulož do C:\GitHub\SpecFactory" (06-27 09:06). Předtím ještě: „**napiš prompt** pro vyhledání studie pro objektivní verifikátor specifikací" (06-26 09:53) a „**Připrav prompt, na kterém to nejlépe otestovat**" (06-26 11:25).
**Opakování:** 4× (2× uložení plánu/promptu, 2× spuštění z uloženého).
**[P]** — soubor jako předávka mezi sessions je nativní chování, nepotřebuje nic. Nejlepší lék na „vyčerpal se kontext".
**Okruh:** O
**Předvedatelnost:** ★★★★★ Živě: session A napíše `plan.md`, session B ho vykoná. Ukázat, že B nepotřebuje historii A.

---

### K15 — Audit cizí session (i podle Session ID)
**Co to je.** Práci udělanou v jednom okně nechá zkontrolovat **jiné okno**, které do ní nebylo zataženo.
**Doklad (2026-08-14 20:16):** „**Reviduj, zda změny provedené v Session ID: 3b4f64bf-8ffd-419c-a080-b3050285f79a byly provedeny správně.**"
Další výskyty: „Spustil jsem v nové session test1-spec-draft-lint-critique. Zkontroluj reasoning podle journals a vyhodnoť, zda Spec Factory pracuje dle očekávání" (06-26 15:02), „Prostuduj journal reasoningu z session alza-fhb-review-system-diff a **kriticky ji zhodnoť**" (06-27 08:44), „/spec-factory:review-spec Reviduj řešení provedené v této session" (08-20 12:04).
**Opakování:** 4×.
**[P/i]** — „reviduj práci z jiné session podle Session ID" je nativní a přenositelné. Čtení `journals` je **[infra]** Spec Factory.
**Okruh:** O + M
**Předvedatelnost:** ★★★★☆ Ukázat, že recenzent bez historie najde věci, které autor přehlédl (to je zároveň důkaz principu RULE-SPEC-002 „kritik hodnotí cizí výstup").

---

### K16 — Odmítnutí návrhu s uvedeným důvodem
**Co to je.** Korekce, která nese **kritérium**, ne jen zamítnutí. Claude se z ní naučí třídu případů, ne jeden případ.
**Doklad (2026-07-07 15:47):** „Pro vnucení čísla nosiče **nenabízej možnost odpověď na webhook WhErrorReport. Je to nekoncepční.**"
Další: „Proč v containerDelete je 4xx a 5xx? **To je zbytečné ne?**" (06-27 18:15), „Tuto poslední změnu vrať prosím zpět." (04-27 12:56).
**Opakování:** 3× odmítnutí s důvodem, 3× „proč" (viz K17).
**[P]**
**Okruh:** U + X
**Předvedatelnost:** ★★★☆☆ Nejlépe jako dvojice vedle sebe: „ne, tohle nechci" vs. „nenabízej X, je to nekoncepční".

---

### K17 — Sokratovská otázka místo zadání (Claude jako oponent návrhu)
**Co to je.** Autor nezadává úkol, ale **nabídne vlastní variantu jako otázku** a nechá si ji rozebrat. Vede to k návrhu, který by sám nenapsal.
**Doklad (2026-07-08 16:49):** „**Proč** u vychystávání **nepovažovat** za okamžik, kdy už WMS nosič nepotřebuje tak, že WMS nechá uzavřít port a to je signál pro WES, že jej může odvézt zpět do skladu? Jak při příjmu nového nosiče WES pozná, že na port byl umístěný operátorem nový nosič?"
Navazuje vzápětí (17:00): „**Jak ale** WES bude vědět, jaké číslo nosiče položil operátor na zabezpečený port, když na portu obvykle není čtečka?" a (08-20 11:42) „**Co by znamenalo** odpověď formulovat v obecnější rovině — pokud není možné detekovat vložení i odjezd nosiče …, tak pak tyto webhooky nejsou posílané?"
**Opakování:** 4× (a je to vidět jako řetěz — každá odpověď plodí přesnější otázku).
**[P]** — nejvíc „analytická" praxe vzorku a nejméně nástrojová.
**Okruh:** A + U
**Předvedatelnost:** ★★★★☆ Předvést tříkrokový řetěz otázek na jednom návrhu. Ukazuje, že Claude umí být oponent, ne jen písař.

---

### K18 — Red team na lidského adresáta: „napiš, jaké námitky bude mít"
**Co to je.** Před odesláním e-mailu / dokumentu si necháš vygenerovat **námitky konkrétního člověka**, který ho dostane.
**Doklad (2026-07-09 16:24):** „**Napiš potenciální námitky, které [kolega] může mít, jakmile obdrží tuto moji odpověď na jeho e-mail.**" + vložený 122řádkový text odpovědi.
**Opakování:** 2× (týž prompt, druhý už s přílohou — viz antipattern X4). Příbuzné: „**Proveď ještě adversiální test na provedené řešení**" (06-27 17:42).
**[P]** — nulová infrastruktura, obrovská hodnota. Pro analytika, který posílá specifikace zákazníkovi, možná nejužitečnější trik vzorku.
**Okruh:** A + M
**Předvedatelnost:** ★★★★★ Naživo na skutečném (anonymizovaném) e-mailu účastníka. Vždycky to najde nejméně jednu námitku, kterou autor nečekal.

---

### K19 — Formátová instrukce ukázkou, ne popisem
**Co to je.** Chceš-li formát, **vlož vzorek** místo jeho popisu.
**Doklad (2026-06-26 22:26):** „Pro větší přehlednost přidávej volné řádky **takto**: [Pasted text #4 +36 lines]"
Druhý výskyt tentýž den v dvojici: nejprve popis — „V yml chci změnu ve verzích popisovat pomocí `changes: - feature:`" (06-27 18:12) — a **hned po něm doplnění ukázkou**, protože popis nestačil: „**Například takto:** [Pasted text #1 +6 lines]" (06-27 18:13).
**Opakování:** 3× (z toho jednou jako demonstrace, že popis sám nezabral).
**[P]**
**Okruh:** M
**Předvedatelnost:** ★★★★★ Ta dvojice 18:12 → 18:13 je hotové demo. Popis → nezabralo → ukázka → zabralo. Minuta a půl.

---

### K20 — Vzor z jiného repozitáře jako reference: „obdobně jako v C:\Git\alzask\docs\api"
**Co to je.** Když už jednu instanci věci máš, neopisuj konvenci — **ukaž na ni cestou** a nech si ji odečíst.
**Doklad (2026-06-23 12:34):** „V API chybí POST DELETE na container. Chtěl bych to udělat **obdobně, jako v C:\Git\alzask\docs\api**. Je potřeba doplnit i do diagramu."
Ještě lépe tentýž mechanismus s doménovým pravidlem (06-27 17:15): „A co se týká dead, tak **jich chci stejně jako v alza** — to znamená pokud je provedený delete, tak už nosič není dostupný pro get. Zároveň není možné provést delete, pokud nosič není v outside zone, **obdobně jako v alza**."
**Opakování:** 3×.
**[P]** — funguje s libovolnými dvěma repozitáři na disku (u mě via `additionalDirectories`; u kolegy stačí, že jsou vedle sebe).
**Okruh:** R + K
**Předvedatelnost:** ★★★★☆ Ukázat cross-repo čtení naživo. Bývá to pro lidi překvapení, že to jde.

---

### K21 — Screenshot a vložený výstup jako doklad, ne jako popis chyby
**Co to je.** Místo popisování, co se stalo, se **vloží obrazovka nebo výstup terminálu**.
**Doklad (2026-08-20 11:48):** „**Proč došlo ke zrušení popisu nového POST DELETE?** [Image #1]" a (07-04 23:33) „Spustil jsem /plugin marketplace add C:\Git\shared\plugins, ale marketplace kvados se mi nenabízí. [Image #2]"
**Opakování:** 5× obrázek, **11× vložený text** — dohromady 16 promptů (7 % vzorku).
**[P]**
**Okruh:** K
**Předvedatelnost:** ★★★☆☆ Krátká ukázka, spíš zmínka než blok.

---

### K22 — Grounding disciplína: citace obsahem, allow-list, jeden prompt = jedna sekce
**Co to je.** Balík čtyř pravidel z fhb `arch-spec` (RULE-ARCH-001): (a) citace **snippetem 3–6 slov doslovně**, ne číslem řádku; (b) TAG **jen z allow-listu**; (c) **žádné vymýšlené identifikátory** — místo nich `TODO` k rozhodnutí architektem; (d) **jeden prompt = jedna sekce**.
**Doklad (RULE-ARCH-001, `date: 2026-06-10`, `source_project: FHB`):** „MUSÍŠ u každého konkrétního tvrzení uvést citaci `[TAG §sekce \"3–6 slov doslovně\"]` … **Snippet 3–6 slov, doslovně** … Nikdy parafráze." / „**NESMÍŠ** vymýšlet identifikátory (endpoint / tabulka / komponenta / field) mimo zdroje" / „**Incremental disclosure:** jeden prompt = jedna arc42 sekce; nikdy »přečti celý repo a napiš spec«."
A odůvodnění, které stojí za odcitování na workshopu: „Fabrikované identifikátory se propašují do spec, WMS je implementuje, a při integraci se zjistí, že WES je neexponuje → **rework**."
**Opakování:** ustálené pravidlo, ne prompt. **Poznámka k dokladu:** ve vzorku promptů pro tohle **není doklad** (žádný fhb prompt z 06-10 až 06-17) — je to doloženo artefaktem, ne promptem. Přiznávám to.
**[P]** — (a)–(d) jsou principy, které si kolega odnese jako čtyři věty. `validate-citations.py` a `freeze-snapshot.py` jsou **[infra]**.
**Okruh:** K + M
**Předvedatelnost:** ★★★★★ Ukázat obě cesty vedle sebe: **fhb** citace snippetem (odolná vůči editaci) vs. **alzask** `soubor:řádek` + `reanchor.py` na dorovnávání. Jeden problém, dvě řešení — jedno návrhem, druhé nástrojem. To je nejlepší diskusní bod celé fáze.

---

### K23 — Sjednocení dvou rozešlých projektů jako zadání
**Co to je.** Když se dva projekty rozejdou, **nechej si najít rozdíl a navrhnout sjednocení** — a přiznej v promptu vlastní odhad, aby ho Claude mohl vyvrátit.
**Doklad (2026-06-26 23:46):** „/spec Analyzuj vytvoření Spec Factory pluginu. **Myslím, že v projektu FHB mám komplexnější schopnosti spec factory než v Alza, ale Alza může mít něco, co FHB nemá. Chci najít rozdíly a rozumně sjednotit.**"
**Opakování:** 1× jako zadání, ale s doloženým výsledkem (session `alza-fhb-review-system-diff`, plugin, migrace 07-04/05) — a odstartované předchozím dotazem 22:02 „Jaké jsou rozumné možností sdílení Spec Factory mezi projekty FHB, Alza a dalšími?"
**[P]** — jádro („najdi rozdíl mezi dvěma repozitáři a navrhni sjednocení, můj odhad je X, klidně ho vyvrať") je čistý prompt. Plugin je **[infra]**.
**Okruh:** R + O
**Předvedatelnost:** ★★★★☆ Pro workshop ideální, protože to je **přesně situace kolegů** — mám metodiku tady, chci ji tam.

---

### K24 — Rozhodnutí o zóně zápisu (projekt vs. produkt) patří do CLAUDE.md, ne do hlavy
**Co to je.** Sdílený produktový repozitář se drží jako **kontext ke čtení**; zápis do něj se rozhoduje podle tabulky a při nejistotě se ptá.
**Doklad (fhb i alzask CLAUDE.md, shodně):** „Nikdy nezapisuj globální ADR (ADR-MF-*) do tohoto repozitáře — ta patří do myFABER" + tabulka se čtvrtým řádkem „Nejsi si jistý → **Zeptej se uživatele**". Podpůrně 6 myfaber promptů = nula obsahové práce (§4) a 50 zmínek `../myfaber` v alzask promptech jako čtené cesty.
**Opakování:** systémové, ve dvou projektech.
**[P]** — tabulka + prefix ID. Žádný nástroj.
**Okruh:** N + O
**Předvedatelnost:** ★★★★☆ Otevřít obě CLAUDE.md vedle sebe a ukázat identickou tabulku a různý prefix (`ADR-ASK-*` / `ADR-FHB-*` / `ADR-MF-*`).

---

## 6. Osobní zvyky a [infra] — nepatří na workshop jako praxe

### Z1 — `/rename` každé session (11×)
„/rename test1-spec-draft-lint-critique", „/rename spec-patch-delete-order", „/rename GIT konflikty". Užitečné (K15 na tom staví — bez názvu se session nedohledá), ale je to **[Z] zvyk**. Do okruhu **N** patří jako 30sekundová zmínka, ne jako blok.

### Z2 — Monitoring kontextu: `/context` 10×, `/model` 6×, `/compact` 5× (21 promptů, 10 % vzorku)
Doklad hustoty: 06-27 mezi 09:03 a 09:26 čtyřikrát `/context`. **[Z]** — sledování spotřeby okna je osobní tik, který si kolega vypěstuje sám. Přenositelné je z toho jen zjištění, **kdy** je čas na K14 (handoff přes soubor).

### Z3 — Hledání „osobnosti" odpovědi (18 stylových promptů, ~8 % vzorku)
Doklad průběhu: 09:25 „Jazyk, jakým se v promptech Claude Code vyjadřuje je pro mě příliš technicky. Udělej průzkum na internetu … cca 5 kandidátů" → 13:20 procentní posuvníky „Formální → Neformální: 50 %, Věcný → Nadšený: 40 %…" → 14:56 „Stále mám pocit, že těmto vyjádřením chybí »osobnost«. Najdi 3 veřejně známé osobnosti…" → 14:57 „Která z těchto osobností je považována za nejzábavnější?" → 14:59 Marek Eben → 15:02 Attenborough → 15:04 Feynman → 15:07 „Jaká je nyní doslovnost → obraznost? Chtěl bych tak na 30 %."
**[Z] osobní vkus**, a z velké části i **antipattern X7**. Přenositelný **zbytek** je ale reálný a patří do **N**: *pro netechnického adresáta nastav `outputStyle`, ať to nemusíš psát do každého promptu* — doloženo cílem „Navrhni mi custom styl, komunikace česky, **zachovat odborné termíny, kódovat normálně**" (15:47) a výsledkem `outputStyle: Feynman CZ` v settings. Tři minuty na workshopu, ne třicet.

### Z4 — Instalační sága plugin/GitLab/Kerberos (07-04 22:12 → 07-05 01:00, ~27 promptů)
„Do Gitu se hlásím přes KRB5", „Z důvodu bezpečnosti do gitu přistupuji pod uživatelem martint, ale claude spouštím pod ai_martint", „Pokud používám deploy token, jak probíhá aktualizace?" **[infra]**, navíc svázané s naší GitLab instalací. Na workshop nepatří vůbec — jen jako varování (X6).

### Z5 — Validátory a registry (`fr-tools`, `plc-tools`, `ontology-tools`, `questions.py`, guardy, `spec_lint.py`)
**[infra]**. Kolega si je neodnese. Přenositelné je jen **RULE-GOV-002 „vynucuj bránou, neinstruuj v promptu"** jako *myšlenka* — s poctivým dodatkem, že brána vyžaduje někoho, kdo ji napíše a udržuje.

### Z6 — Šum: 24 promptů ≤ 20 znaků bez slashe
`test` (4×), `exit` (3×), `a`, `2`, `OK` (2×), `implementuj`, `Otázky`, `revize`, `Body z jednání`, `chci 1`. **[Z]** — a část z toho je X2/X5.

---

## 7. Iterační smyčky — kde je rozdíl mezi „vyjasňuje se" a „zadal jsem špatně"

Tohle je podle mě nejcennější část pro workshop, protože oba typy vypadají v logu identicky.

### S1 — Formulace otázek pro dodavatele: **26 promptů, 4 hodiny (06-26 21:24 → 06-27 00:23)** — legitimní vyjasňování ✔
Průběh: velký vstup (6240 zn., 26 otázek se stavy) → „Budeme řešit postupně. Formuluj nyní správně otázky 6a a 6b." → „Navrhované názvy míst na dopravníku doplň do závorky. Ke každé otázce vytvoř stručný název…" → „Chci ponechat označení PICK_STATION_A1_LOAD … Máme je takto použité už v obrázku. [Image]" → „Napiš otázku do markdown souboru. Z něj si budu kopírovat do e-mailu." → „Pokračuj další otázkou" → „**Tato otázka se kryje s 6b. Je to tak nebo je v ní něco nového?**" → „otázky 10, 14, 15, 16" → „10 a 16 vyřaď" → „Otázky 20 až 27 jsou nové. Chci je mít tedy na konci uvedené společně." → „**Otázka 24 se kryje s nějakou předchozí otázkou, ne?**" → „ano, 24 a 25 chci zúžit. Místo 27 chci otázku, jaký je postup při spouštění skladu…" → „Ke které otázce se nejvíce hodí tento obrázek? [Image]" → „OK".
**Proč je to legitimní:** každý prompt přináší **novou informaci** (další obrázek, další rozhodnutí o názvech, zjištěný překryv otázek). Zadání nebylo špatné — **předmět se tvořil**. Kdyby autor napsal jeden dokonalý prompt, dostal by 26 otázek, které si navzájem odporují.
**Poučení pro kolegu:** dlouhá iterace není selhání, pokud každé kolo něco **uzavře**. Kontrolní otázka: *přinesl jsem v tomhle promptu informaci, kterou předtím nikdo neměl?*

### S2 — Nečitelný kód nosiče: **6 promptů, 50 minut (07-07 14:58 → 15:47)** — postupné dořešení ✔
„Formuluj závěry … zde do chatu. Co si pamatuji: …" → „Souhlasím s tímto popisem. Tento popis se promítá do odpovědí na více otázek. Uprav odpovědi tak, aby odpovídaly …" → „Chci, aby i v případě, že kód je čitelný, tak aby WCS o tom informoval WMS … **Doplň do odpovědí, kde to není jednoznačně zřejmé.**" → „A prověř, zda je uveden explicitní dotaz, přes jaké rozhraní …" → „Pro vnucení čísla nosiče nenabízej … Je to nekoncepční."
**Proč je to legitimní a navíc vzorové:** autor si nejdřív nechal **napsat svůj vlastní závěr do chatu** (K8+K13), teprve po vlastním schválení ho nechal **propsat do všech dotčených odpovědí**. To je RULE-SPEC-004 („model před hromadnou aplikací") v praxi, aniž by na něj kdokoli odkázal.
**Poučení:** *nejdřív jeden model, po odsouhlasení hromadná aplikace.* Nejpřenositelnější iterační vzor vzorku.

### S3 — Šablona vrstvového auditu: **3 prompty za 53 minut** — legitimní zdokonalování ✔
19:36 (3052) → 20:13 (3344) → 20:29 (5280, jiný projekt). Každá verze přidává blok, ne opravu. **Iterace na nástroji, ne na zadání.**

### S4 — Instalace pluginu: **~27 promptů, 3 hodiny v noci (07-04 22:12 → 07-05 01:00)** — částečně špatné zadání ✘
„SpecFactory mám nyní uloženou v C:\GitHub\SpecFactory … chci přesunout do C:\Git" (22:12) → **o 60 s znovu, doplněno** „…do C:\Git\shared … **Možná by bylo vhodné vytvořit ještě podsložku plugins.**" (22:13) → … → „Nyní mi již instalace z adresáře funguje. **Použil jsi ale správný postup?** Jaký je správný postup pro instalaci z URL?" (00:12).
**Diagnóza:** dvě příčiny. (a) Zadání odesláno nedopsané (22:12 vs 22:13). (b) Cíl se během tří hodin **měnil** — z „přesuň složku" na „nainstaluj z URL přes deploy token pod jiným uživatelem". To už není vyjasňování, to je práce bez zadání.
**Poučení pro kolegu:** infrastrukturní úlohy si vyžádají cíl a hranici **předem** (viz K14 — plán do souboru), jinak se roztečou.

### S5 — Hledání komunikačního stylu: **18 promptů, 9 hodin (06-27 09:25 → 18:03)** — špatně formulovaný cíl ✘
Skutečná potřeba („chci, aby to pochopil i neprogramátor") byla vyslovena hned v prvním promptu. Následujících 17 promptů ji hledalo přes průzkum internetu, procentní posuvníky, tři osobnosti a čtyři různá místa nastavení. Definitivní tečka až „**Vysvětli mi princip nastavení stylu komunikace.**" (18:03) — tedy naučit se mechanismus, což mělo být krokem druhým, ne osmnáctým.
**Diagnóza:** cíl nebyl vyjádřen jako **kritérium** („pochopí to člověk, který nikdy neviděl OpenAPI"), ale jako **preference** („je to na mě moc technické"). Preference se nedá splnit, jen dolaďovat.
**Poučení:** *cíl formuluj jako kritérium, na kterém se dá poznat, že jsi hotov.*

### S6 — POST DELETE na container: **06-23 → 06-27 17:15–18:18 → 08-20 11:48** — návrat po dvou měsících ✘
06-23: „V API chybí POST DELETE na container … obdobně jako v alzask" → 06-27 17:15–18:18: sedm promptů dolaďování (autor, changelog, verze, 4xx/5xx, `containerRemoved`) → **08-20 11:48: „Proč došlo ke zrušení popisu nového POST DELETE? [Image #1]"**
**Diagnóza:** práce z června byla později přepsaná a přišlo se na to **lidským okem z obrázku po dvou měsících**. Nebyla brána, která by to zachytila. Viz X2.

---

## 8. Anatomie dlouhých zadání

Ve vzorku jsou **jen dva** prompty nad 1000 znaků. Oba mají jasnou anatomii a jsou to opačné typy.

### 8.1 Analytické zadání — 2026-08-14 20:13, 3344 znaků (a jeho alzask sourozenec, 5280)

Devět bloků, v tomto pořadí:

| # | Blok | Obsah | Nadpis v promptu |
|---|---|---|---|
| 1 | **Role zdrojů** | 3 dokumenty, u každého jednořádkový účel | (bez nadpisu, v úvodu) |
| 2 | **Jak číst** | „celé, včetně poznámek pod sekcemi, otevřených otázek, TODO … právě tam bývá věta, která ruší platnost mechanismu popsaného nad ní" | (v úvodu) |
| 3 | **Rozhodčí** | ADR jako autorita; do config nahlédni jen když… | (v úvodu) |
| 4 | **Nečíst** | `snapshots/` + důvod + kdy přesto | (v úvodu) / `CO NEČÍST` v alzask verzi |
| 5 | **Úkol** | 3 body s nejvyšší pákou + **definice páky** | `ÚKOL` |
| 6 | **Taxonomie hledání** | A–E (alzask: A–H), včetně „mlčení" a „nedourčení" | `CO HLEDAT` |
| 7 | **Výstupní kontrakt** | 5 bodů: kategorie / stav ve všech vrstvách s citací nebo „mlčí" / verdikt ADR / jmenovitý výčet dotčených míst / otázky | `PRO KAŽDÝ NÁLEZ UVEĎ` |
| 8 | **Formát otázek** | uzavřené, (a)/(b)/(c), důsledek na variantu, doporučení, „chci umět odpovědět písmenem" | (bod 5 kontraktu) / vlastní blok `OTÁZKY PRO MĚ` v alzask verzi |
| 9 | **Pravidla** | nic z paměti / pravidlo vs. instance / ptej se místo domýšlení / nesahej na soubor / řaď podle páky / co se nevešlo nezahazuj | `PRAVIDLA` |

**Pořadí má logiku:** zdroje → jak s nimi zacházet → co je zakázané → co chci → jak to hledat → jak to podat → jak se mě ptát → čeho se držet. Cíl (blok 5) je **až v polovině** — nejdřív je postavené hřiště.
**Co v něm NENÍ:** žádná zdvořilost, žádné vysvětlování, proč je úkol důležitý, žádná role („jsi expert na…"), žádné příklady výstupu.

### 8.2 Věcné zadání — 2026-06-26 21:24, 6240 znaků

Anatomie je úplně jiná: **krátká hlava (2 věty) + 96 % vloženého materiálu**.
- **Hlava:** „Na základě závěrů schůzky @docs/meetings/… prověř, zda jsou správně formulované následující otázky. Potřebuji je formulovat jednoduše, přesně a srozumitelně, aby jim rozuměli čínští dodavatelé." — zdroj pravdy + úkol + kritérium kvality + adresát, ve dvou větách.
- **Tělo:** 26 otázek v doslovném znění, roztříděné do `PENDING` / `NEW` / `ANSWERED` / `CLOSED`, u částečných poznámka co chybí.

**Poučení pro workshop:** dlouhý prompt není dlouhý proto, že je v něm dlouhá instrukce. Je dlouhý proto, že v něm **je materiál**. Instrukce je krátká; roste jen tam, kde jde o **analytický** úkol, který potřebuje pravidla hry (8.1).

---

## 9. Korekce a antipatterny (okruh X)

**Metodická poznámka:** heuristika na začátek věty tady prakticky nefunguje — `^ne|proč jsi|špatně|znovu` dá 2 zásahy ze 218. Následující nálezy jsou z čtení obsahu.

### X1 — Nevratná editace bez zálohy ⭐ nejlepší antipattern vzorku
**Doklad (2026-04-27 12:56):** „**Tuto poslední změnu vrať prosím zpět. Nemůžeš ale k tomu použít Git.**"
**Co se stalo:** dva prompty předtím (12:28, 12:40) proběhly úpravy Varianty A a Varianty C. Pak si autor jednu rozmyslel — a jediná cesta zpět je, že si Claude pamatuje, co změnil. Git je nepoužitelný (nezacommitováno / nechtěné vedlejší dopady).
**Formulace je zajímavá tím, čím není:** není to výtka Claudovi. Je to **přiznání, že chybí záchranný bod**.
**Předvedatelnost:** ★★★★★ Živé demo: tři úpravy bez commitu → „vrať tu druhou" → sledovat, jak se to nedaří přesně. Pak totéž s commitem/worktree před každým krokem.
**Okruh:** X (+ N)

### X2 — Tichá regrese odhalená lidským okem po dvou měsících
**Doklad (2026-08-20 11:48):** „**Proč došlo ke zrušení popisu nového POST DELETE?** [Image #1]"
**Co se stalo:** práce z 06-23/06-27 (osm promptů) byla někdy během dvou měsíců přepsána. Nikdo si toho nevšiml — až autor při čtení dokumentu narazil a přiložil screenshot. Žádný test, žádná brána, žádný changelog to nezachytil.
**Souvislost:** je to přesně důvod pro `RULE-CL-001` (changelog povinný) a `RULE-SPEC-001` (trace akceptace) — pravidla existují a stejně to prošlo. **Pravidlo bez brány je přání.**
**Předvedatelnost:** ★★★★☆ Ukázat časovou osu 06-23 → 08-20 na dvou slidech.
**Okruh:** X + M

### X3 — Nahé „implementuj"
**Doklad:** „**implementuj**" (2026-06-26 09:57), „**Implementuj**" (2026-06-27 09:05).
**Kontrast v tomtéž vzorku, o minutu později:** „Implementuj **podle @docs/spec/2026-06-26_spec-factory-plugin-sjednoceni/implementation-prompt.md**. Plugin dočasně ulož do C:\GitHub\SpecFactory" (09:06).
**Předvedatelnost:** ★★★★★ Dvojice 09:05 / 09:06 je hotový slide: totéž slovo, jednou bez ukotvení, jednou s ním, minuta rozdílu. Sám autor si to opravil.
**Okruh:** X

### X4 — Odesílání nedopsaného promptu
**Doklad:** 2026-07-04 **22:12** vs **22:13** — dvě verze téhož, druhá doplněná o „…do složky C:\Git\shared … Možná by bylo vhodné vytvořit ještě podsložku plugins."; 2026-07-09 **16:24 dvakrát** — týž prompt, podruhé s přílohou „[Pasted text #1 +122 lines]" (poprvé odeslán **bez textu, o kterém se ptá**).
**Historická souvislost:** týž návyk je v nejstarších alzask promptech (2026-01-29: 3× doslovně týž 700znakový prompt). Za osm měsíců se nezměnil.
**Léčba:** psát prompt v editoru, vkládat hotový. (Souvisí s K19 — vkládaný materiál patří do promptu **spolu s** otázkou.)
**Předvedatelnost:** ★★★☆☆ Zmínit, ne předvádět.
**Okruh:** X

### X5 — Otázka slepená se slash příkazem
**Doklad (2026-06-19 15:07):** „`/rename \"GIT konflikty\"` Jak mám vyřešit GIT konflikty v tomto repu, když chci u všech přijmout změny, které přicházejí ze serveru?"
Následuje 15:08 `/rename GIT konflikty` a 15:08 znovu celá otázka — tedy **otázka se ztratila** a musela se poslat zvlášť.
**Předvedatelnost:** ★★★☆☆ Rychlá ukázka, praktická, každý to udělá.
**Okruh:** X + N

### X6 — Nástrojová a stylová odbočka místo práce
**Doklad (poměr):** 2026-06-26 a 06-27 = **99 promptů = 45 % celého vzorku fhb**, a jsou to dva dny věnované z většiny pluginu, journalům, průzkumu stylů a personám. Doménových promptů je v celém vzorku 25 (11 %).
**Konkrétní projev:** 18 stylových promptů (§Z3), 27 instalačních (§S4).
**Nejsem k sobě fér, kdybych to zamlčel:** ty odbočky **měly** výstup (plugin, `outputStyle`, marketplace). Ale cena byla dva pracovní dny a jedna noc, a kolega na workshopu tuhle investici dělat nemá — dostane plugin hotový.
**Formulace pro workshop:** *nástroj si postav, až tě táž ruční práce potřetí naštve. Ne dřív.*
**Předvedatelnost:** ★★★★☆ Graf promptů po dnech (mám ho v `analyza_fhb3_out.txt`) — dva pilíře 52 a 47, zbytek pod 20. Mluví sám.
**Okruh:** X

### X7 — Preference místo kritéria
**Doklad (2026-06-27 09:25):** „**Jazyk, jakým se v promptech Claude Code vyjadřuje, je pro mě příliš technicky.** Udělej průzkum na internetu, jaké jsou preferované atraktivní formy stylizace odpovědí … cca 5 kandidátů, ukázky jejich stylizace a já si z nich chci vybrat."
Konec cesty 9 hodin a 18 promptů později: „Jaká je nyní doslovnost → obraznost? Chtěl bych tak na 30 %." (15:07) a „Vysvětli mi princip nastavení stylu komunikace." (18:03).
**Diagnóza:** „je to na mě moc technické" je preference — nedá se splnit, jen dolaďovat. „Pochopí to člověk, který nikdy neviděl OpenAPI" je kritérium — dá se ověřit. Zajímavé je, že autor **kritérium umí** a použil ho jinde: „aby jim rozuměli čínští dodavatelé" (06-26 21:24), „vysvětli mi to **laicky**" (08-21 15:48).
**Předvedatelnost:** ★★★★☆ Dvě formulace téhož požadavku vedle sebe.
**Okruh:** X + U

### X8 — Nastavení, které se nechytlo, a nikdo si toho nevšiml
**Doklad (2026-07-08 17:08):** „**Jakým stylem máš odpovídat?**" — jedenáct dní po nastavení `outputStyle: Feynman CZ`. Předtím už 2026-06-27 18:02 „Jakým stylem aktuálně komunikuješ?"
**Diagnóza:** nastavení bez ověření. Dvě kontrolní otázky na totéž s odstupem = poprvé se to nepotvrdilo.
**Léčba:** po každé změně konfigurace **jeden verifikační prompt** hned, ne za jedenáct dní.
**Předvedatelnost:** ★★★☆☆
**Okruh:** X + N

### X9 — Dokumentace, kterou nikdo znovu nepřečetl (drift CLAUDE.md) ⭐
**Doklad — tři konkrétní nesoulady v `C:\Git\fhb\CLAUDE.md` k dnešnímu dni:**
1. Sekce **Přepisy schůzek**: „Formát názvu souboru: `YYYY-MM-DD název schůzky.vtt`" — přitom fhb prompty odkazují `@docs/meetings/2026-06-26_...md` a `@docs/meetings/2026-07-07_...md`. **Soubory jsou `.md`, dokumentace tvrdí `.vtt`.**
2. Sekce **Spec Factory (`/spec`)**: popisuje **lokální** implementaci — „agenti `spec-*`, orchestrátor `/spec`, hook", „HARD mantinel: `.claude/hooks/spec-guard.py`", „Workspace běhu: `docs/spec/<YYYY-MM-DD_slug>/`". Přitom migrace na plugin proběhla 07-04/05 **a vznikla právě ve fhb** (06-26 23:46). Alzask CLAUDE.md už má „od 2026-07-07 VÝHRADNĚ plugin". **fhb dokumentuje stav, který sám překonal.**
3. Sekce **Znalostní smyčka** uvádí v precedenci vrstvu „cross-project `shared`". Ověřeno: `C:\Git\shared\` obsahuje `plugins/` a `docs/`, **žádné `rules/`**. Ta vrstva neexistuje.
**Proč je to antipattern a ne drobnost:** CLAUDE.md se načítá **automaticky do každé session**. Nepravdivé instrukce nejsou neutrální — aktivně vedou špatně.
**Léčba:** po každé migraci nástroje projít CLAUDE.md; ideálně brána, která ověří, že cesty zmíněné v CLAUDE.md na disku existují.
**Předvedatelnost:** ★★★★★ Nejlepší demo mechaniky kvality: otevřít fhb CLAUDE.md a `ls C:\Git\shared` vedle sebe. Tři nesoulady za dvě minuty.
**Okruh:** X + M + N

### X10 — Povýšení konvence, které nedoputovalo (a bylo by rozbilo sousední projekt)
**Doklad:** `RULE-API-005_zadny-oneof-discriminator.md` v `C:\Git\fhb\.claude\rules\shared\`, `layer: shared`, `source_project: FHB`, Stopa použití: „2026-07-07 | spec-factory | **generalizace draftu z _personal do pluginu**".
**Dvě zjištění:**
1. **V pluginu to není.** `find C:\Git\shared\plugins -iname "RULE-*"` → jen `commands/rule-new.md` a `templates/RULE-template.md`. Stopa použití tvrdí povýšení, které se nestalo (a stát se ani nemělo — plugin drží mechaniku, obsah patří repu).
2. **Kdyby doputovalo, rozbilo by alzask.** Pravidlo říká „nepoužívej `oneOf` ani `discriminator`", alzask API je na `oneOf` + discriminator postavené (`ContainerUpsertRequest` = oneOf 6 variant, `Container` = oneOf 8 variant).
**Poučení pro kolegu:** než konvenci povýšíš na „platí všude", **ověř ji na sesterském projektu**. A stopa použití je záznam, ne důkaz.
**Předvedatelnost:** ★★★★☆ Vedle sebe věta pravidla a schéma alzask API.
**Okruh:** X + M

---

## 10. Momenty vzniku — kdy se z promptu stalo pravidlo

| Datum | Prompt / stopa | Co z toho vzniklo |
|---|---|---|
| 2026-06-10 | *(ve vzorku promptů chybí)* | `RULE-ARCH-001_grounding.md`, `date: 2026-06-10`, „seed z grounding-disciplina.md" — grounding disciplína arch-spec |
| 2026-06-15 | *(ve vzorku promptů chybí — jednání)* | `RULE-API-002` / `-003` / `-005`, `source: 'FHB — konvence a názvosloví API (schůzka 2026-06-15)'`, seedy „odstraněn jednočlenný oneOf, text »diskriminátor« → »typové pole«" |
| 2026-06-26 22:02 | „Jaké jsou rozumné možností **sdílení Spec Factory mezi projekty** FHB, Alza a dalšími?" | zadání pro plugin |
| 2026-06-26 23:46 | „/spec Analyzuj vytvoření Spec Factory pluginu. Myslím, že v FHB mám komplexnější … Chci najít rozdíly a rozumně sjednotit." | session `alza-fhb-review-system-diff` → `docs/spec/2026-06-26_spec-factory-plugin-sjednoceni/implementation-prompt.md` |
| 2026-06-27 09:06 | „Implementuj podle @…/implementation-prompt.md. Plugin dočasně ulož do C:\GitHub\SpecFactory" | první existence pluginu |
| 2026-06-27 15:47 | „Navrhni mi custom styl, komunikace česky, zachovat odborné termíny, kódovat normálně. Blízký je mi Richard Feynman, ale **analyzuj journal z mých sessions** a zkus přizpůsobit stylu mé komunikace." | `outputStyle: Feynman CZ` v settings |
| 2026-07-04/05 | „SpecFactory … chci přesunout … do C:\Git\shared … Možná by bylo vhodné vytvořit ještě podsložku plugins" + 27 promptů | `C:\Git\shared\plugins\` + marketplace `kvados-plugins` |
| 2026-07-09 13:44–14:58 | „FHB Znalostní smyčka" + `[Pasted text #1 +84 lines]` → „**spec-grounding se týká SpecFactory, ne? … Potřebuji ty dvě věci od sebe striktně oddělit.**" → „Chci rozdělit do striktně oddělených bloků … připrav plán a ulož jej" | znalostní smyčka zavedená ve fhb; **oddělení Spec Factory od knowledge-loop** jako dvou domén |
| **2026-07-10 14:49 / 07-11 21:08** | *(bez promptu ve vzorku)* | **batch kopie pravidel** — alzask `shared/` a fhb `shared/` upravené do 32 hodin, 4 soubory bit-shodné. Toto je ten okamžik přenosu. |
| 2026-08-14 19:36 → 20:13 → **20:29** | vrstvová šablona, tři verze, poslední **v alzask** | přenositelná šablona auditu (K1–K8) |

**Co z toho plyne pro workshop:** ze 13 shared pravidel fhb se **ani jedno nerodí v promptu, který bych umel ukázat**. Rodí se z **jednání** (API-002/003/005 — schůzka 06-15), z **dokumentu** (ARCH-001 — seed z `grounding-disciplina.md`) nebo z **kopie ze sesterského projektu** (10 pravidel, 07-10/11). Prompt je místo, kde se pravidlo **použije**, ne kde se vymyslí. To je docela dobrá zpráva pro kolegy: nemusí umět promptovat, aby měli pravidla — musí umět zapsat, na čem se dohodli.

---

## 11. Souhrn kandidátů

| # | Kandidát | Výskyty | Klasifikace | Okruh | Demo |
|---|---|---|---|---|---|
| K1 | Vrstvový audit „N vrstev jedné věci" | 3 | **[P]** | A K M | ★★★★★ |
| K2 | Blok `CO NEČÍST` s důvodem u položky | 2+ | **[P]** | K | ★★★★★ |
| K3 | Blok `ROZHODČÍ` — už rozhodnuté ≠ otázka | 2 | **[P]** | K M | ★★★★☆ |
| K4 | „citace, nebo výslovně »mlčí«" | 2 | **[P]** | M K | ★★★★☆ |
| K5 | „Ticho je nález" | 2 | **[P]** | A | ★★★★★ |
| K6 | Uzavřené otázky (a)/(b)/(c) + rozpočet | 2 + 6 užití | **[P]** | A U | ★★★★★ |
| K7 | Řadit podle páky, páku definovat | 2 | **[P]** | A M | ★★★★☆ |
| K8 | „Nesahej na žádný soubor" / do chatu | 5 | **[P]** | M N | ★★★★★ |
| K9 | Návrh → picklist → „Proveď: 1, 3" | 6 | **[P]** | O A | ★★★★★ |
| K10 | Nejprve česky, po odsouhlasení přeložit | 6 | **[P]** | A | ★★★★☆ |
| K11 | Adresát jako omezení + názvy otázek + mapa pojmů | 3 | **[P]** | A K | ★★★★☆ |
| K12 | Doslovné znění + stavy PENDING/NEW/ANSWERED/CLOSED | 1 (→registr) | **[P/i]** | A K R | ★★★★☆ |
| K13 | Vlastní paměť + příkaz ji ověřit | 3 | **[P]** | K U | ★★★★☆ |
| K14 | Handoff mezi sessions přes soubor | 4 | **[P]** | O | ★★★★★ |
| K15 | Audit cizí session (Session ID) | 4 | **[P/i]** | O M | ★★★★☆ |
| K16 | Odmítnutí s důvodem („je to nekoncepční") | 3 | **[P]** | U X | ★★★☆☆ |
| K17 | Sokratovská otázka místo zadání | 4 | **[P]** | A U | ★★★★☆ |
| K18 | Red team na lidského adresáta | 2 (+1 adversariální) | **[P]** | A M | ★★★★★ |
| K19 | Formát ukázkou, ne popisem | 3 | **[P]** | M | ★★★★★ |
| K20 | Vzor z jiného repozitáře cestou | 3 | **[P]** | R K | ★★★★☆ |
| K21 | Screenshot / vložený výstup jako doklad | 16 | **[P]** | K | ★★★☆☆ |
| K22 | Grounding disciplína (snippet, allow-list, 1 prompt = 1 sekce) | pravidlo | **[P]** jádro | K M | ★★★★★ |
| K23 | Sjednocení dvou rozešlých projektů jako zadání | 1 | **[P]** jádro | R O | ★★★★☆ |
| K24 | Zóna zápisu projekt vs. produkt v CLAUDE.md | systémové | **[P]** | N O | ★★★★☆ |
| Z1 | `/rename` každé session | 11 | **[Z]** | N (zmínka) | ★★☆☆☆ |
| Z2 | `/context` `/model` `/compact` monitoring | 21 | **[Z]** | N (zmínka) | ★★☆☆☆ |
| Z3 | Hledání „osobnosti" odpovědi | 18 | **[Z]** (zbytek → N) | N / X | ★★★☆☆ |
| Z4 | Instalační sága plugin/GitLab/KRB5 | ~27 | **[infra]** | — | ✘ |
| Z5 | Validátory, registry, guardy | — | **[infra]** | M (jen myšlenka) | ★★☆☆☆ |
| Z6 | Šum (`test`, `exit`, `a`, `2`) | 24 | **[Z]** | — | ✘ |
| X1 | Nevratná editace bez zálohy | 1 | antipattern | X N | ★★★★★ |
| X2 | Tichá regrese odhalená po 2 měsících | 1 | antipattern | X M | ★★★★☆ |
| X3 | Nahé „implementuj" | 2 (+1 kontrast) | antipattern | X | ★★★★★ |
| X4 | Nedopsaný prompt odeslán | 2 (+3 v alzask) | antipattern | X | ★★★☆☆ |
| X5 | Otázka slepená se slash příkazem | 1 | antipattern | X N | ★★★☆☆ |
| X6 | Nástrojová odbočka místo práce (45 % vzorku ve 2 dnech) | vzor | antipattern | X | ★★★★☆ |
| X7 | Preference místo kritéria | 18 | antipattern | X U | ★★★★☆ |
| X8 | Nastavení bez ověření | 2 | antipattern | X N | ★★★☆☆ |
| X9 | Drift CLAUDE.md (3 doložené nesoulady) | 3 | antipattern | X M N | ★★★★★ |
| X10 | Povýšení, které nedoputovalo (a rozbilo by sousedy) | 1 | antipattern | X M | ★★★★☆ |

**Počty:** 24 kandidátů na přenositelnou praxi (z toho 21 čistě **[P]**, 3 **[P/i]**), 6 položek osobní zvyk / **[infra]**, 10 antipatternů.

---

## 12. Doporučené jádro pro workshop z tohoto vzorku

Kdybych z 218 promptů měl zachránit **jedinou věc**: šablonu **K1–K8** (vrstvový audit). Je to jeden textový blok, funguje na libovolných dokumentech, nepotřebuje nic z mé výbavy, dá se předvést naživo za deset minut a **je doloženo, že přežila přenos mezi dvěma projekty a přitom se zlepšila**. Všechno ostatní je k ní příloha.

Kdybych měl zachránit **jedinou větu**: „**Ticho je nález, ne absence nálezu.**"

Kdybych měl zachránit **jediný antipattern**: **X9 — drift CLAUDE.md**. Protože je to jediná chyba z celého seznamu, kterou udělá **každý** účastník workshopu do měsíce od chvíle, kdy si CLAUDE.md založí.
