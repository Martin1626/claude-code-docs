# FÁZE 2e — Destilace praxe z promptů: repozitář `C:\Git\shared` (marketplace `kvados-plugins`)

Vstup: `C:\tmp\workshop-namety\_raw\prompty-shared.md` (151 bloků, 2026-07-05 → 2026-08-25).
Analytické skripty: `an_shared.py`, `an_shared2.py` (+ výpis `an_shared2_out.txt`).
Kontext k dohledání artefaktů: `C:\Git\shared` git log, `plugins/*/.claude-plugin/plugin.json`,
`plugins/spec-factory/README.md`. **Do žádného repozitáře nebylo zapsáno.**

Tento vzorek je jediný, kde se Claude Code používá k **postavení nástroje pro Claude Code**.
Proto je hlavní hodnota v tom, co to stálo — a v tom, které chyby se opakovaly.

---

## 0. Nejdřív oprava čísel: „137 promptů" neplatí

| Kategorie | Počet | % z 151 |
|---|---|---|
| **Celkem bloků v souboru** | 151 | 100 % |
| Jen příkaz harnessu (`/model` 20×, `/plugins` 8×, `/compact` 6×, `/context` 5×, `/rename` 3×, ostatní 6×) | **48** | 32 % |
| Jednoslovné potvrzení / šum (`A`, `OK`, `a`, `test`, `pokračuj` 2×, `Uprav`, `push hotov`, `Prezentace`, `Prověření 3`) | **10** | 7 % |
| **Věcné prompty** | **93** | 61 % |
| … z toho mimo téma pluginů (simulace dopravníku, 2026-07-13) | 3 | |
| … z toho prezentace / dokumentace pro kolegy | ~20 | |
| … z toho marketplace / tokeny / instalace / git | ~13 | |
| **Vlastní inženýrství pluginů** | **≈ 56** | 37 % |

Rozložení délek věcných promptů: **< 100 znaků 52 ×** (56 %), 100–300 znaků 32 ×,
300–1000 znaků 6 ×, **nad 1000 znaků jen 3 ×** — a dva z těch tří nejsou vývoj pluginu
(prezentace o Claude Code 1 679 zn., simulace dopravníku 1 767 zn.). Na plugin samotný
existuje v celém vzorku **jediný dlouhý strukturovaný prompt** (2026-07-05 13:16, 1 384 zn.).

**Proč je to důležité pro workshop:** to nevypadá jako „137 pečlivých promptů". Vypadá to jako
**jeden dobrý prompt, pár desítek krátkých korekcí a hodně ověřování** — plus dvě velká zadání,
která do chatu nikdy nešla (viz P10). Kolega, který si řekne „to je moc práce", měří špatnou věc.

Časové rozložení: **138 bloků v červenci** (soustředěně 5.–13. 7., 9 dní) a **13 v srpnu**.
Nejhustší den je 2026-07-10 (31 bloků) — a nešlo o návrh, ale o **rozchození marketplace a tokenů**.

---

## 1. Jak vypadá vývoj pluginu v promptech (odpověď na otázku 1)

Klasifikace 93 věcných promptů (mírně se překrývá, proto přibližná %):

| Typ práce | Počet | Podíl | Příklad |
|---|---|---|---|
| **Návrh** (nová schopnost, nový invariant, změna workflow) | ~20 | 22 % | 07-10 22:05 „Nebylo by efektivnější, aby se nejprve provedl research a teprve po něm planner?" |
| **Audit / verifikace** (funguje to opravdu?) | ~18 | 19 % | 07-08 20:24 „Proveď audit, že pravidla … jsou správně zohledňovaná" |
| **Opravy** (konkrétní vada) | ~18 | 19 % | 08-19 22:14 „review-spec se mi v nové session nenabízí. Proč?" |
| **Dokumentace / srozumitelnost / prezentace** | ~20 | 22 % | 07-10 20:15 „Uprav dokumentaci, aby byla srozumitelná i pro méně zasvěcené lidi" |
| **Infrastruktura distribuce** (marketplace, tokeny, git) | ~13 | 14 % | 07-10 14:23 „Marketplace chci nainstalovat z gitu nově. Napiš přesný postup." |
| Mimo téma | 3 | 3 % | — |

**Hrubý poměr: návrh 1 : (audit + opravy) 2 : dokumentace 1.**

Odůvodnění poměru — tři nezávislé indicie ukazují na totéž:
1. Slovník: „audit / prověř / zkontroluj / ověř / reviduj" je v **19 promptech**, kdežto slova
   navrhující novou funkci jsou v ~10.
2. Git log pluginů: z 27 commitů v repu je **`feat:` 5×**, zbytek `fix:` a `docs:`.
3. Nejhustší den (07-10, 31 bloků) neobsahuje ani jeden návrhový prompt — je celý o instalaci.

**Nejvíc kontraintuitivní zjištění: dokumentace „pro lidi" spolykala stejně promptů jako návrh.**
Pět promptů řeší jen to, aby popis pluginu nebyl žargon (019, 031, 060, 061, 065), šest promptů
jen vysvětlení instalace pro kolegyni (070–075), pět promptů prezentaci. Postavit nástroj je
polovina práce; **druhá polovina je udělat ho převzatelným**. To by na workshopu mělo padnout
explicitně, protože se to při plánování nikdy nezapočítá.

---

## 2. Kde jsem narazil — opakované chyby v mechanice (odpověď na otázku 2)

### E2 — „V nové session se to nenačte / nenabídne" · **NEJCENNĚJŠÍ NÁLEZ VZORKU**
- **Co to je:** cokoli, co se zavádí na startu session (hook, pravidla, slash příkaz),
  nefunguje — a **nelze to zjistit v té session, ve které se to staví**. Vada se ukáže až
  po otevření nové session, často až v jiném repozitáři.
- **Doklad:**
  - 2026-07-08 20:24 — „Proveď audit, že pravidla uložená v `plugins\spec-factory\rules\shared` jsou správně zohledňovaná. Například v projektu `C:\Git\alzask` se v nové session zobrazuje: [Image #1]"
  - 2026-07-08 22:52 — „Pohlídej, aby se v nových sessions správně načítala nejen sdílená pravidla, ale i osobní pravidla a pravidla z osobního inboxu."
  - 2026-07-09 08:24 — „Cizí pravidla se sice ukládají do Gitu, ale **nesmí se nikdy načítat** ostatním uživatelům."
  - 2026-08-19 22:14 — „review-spec se mi v nové session nenabízí. Proč? Přitom mám verzi 1.8.0 [Image #1]"
- **Kolikrát:** **4 výskyty, ve dvou různých pluginech, 6 týdnů od sebe.** Jasný vzor, ne nehoda.
- **Přenositelné?** **Přenositelný poznatek**, i bez pluginů: platí pro každý hook, `CLAUDE.md`,
  skill i příkaz. Pravidlo do workshopu: *co se načítá na startu, se testuje jen novou session —
  a nejlépe v jiném repu, než ve kterém to vzniklo.* Samotná náprava je `[infra]`.
- **Okruh:** `N` nastavení (+ `M` mechanika kvality)
- **Předvedatelnost:** výborná. Přidat řádek do `CLAUDE.md`, zeptat se v téže session (model
  o něm neví), otevřít druhý terminál, zeptat se znovu. Dvě minuty, aha-moment zaručený.

### E1 — Zdrojový projekt prosakuje do generického artefaktu
- **Co to je:** při vytahování hotové věci z jednoho projektu do sdíleného pluginu zůstanou
  v textu jména projektů, absolutní cesty, konkrétní data a čísla platná jen tam.
- **Doklad:**
  - 2026-07-05 01:13 — „Zároveň chci, aby při prvním použití na novém projektu nemusel mít uživatel v lokálním adresáři projekt FHB ani Alza."
  - 2026-07-05 01:41 — „V Spec Factory nepotřebuji nikde zmínku o projektech FHB ani Alza. Ani o změnách, které byly postupně do pluginu prováděné."
  - 2026-07-10 20:51 — „PLuginy se netýkají jen FHB a Alza. Vůbec je nezmiňuj. V budoucnu to budou další projekty."
  - 2026-08-24 23:01 — „V souborech pro ontology-registry se objevuje datum 2026-08-24 nebo informace o aktuální kontrole registru. To se ale týká konkrétního projektu Alzask, ale tento plugin má být obecný."
- **Kolikrát:** **4 výskyty, 2 pluginy, rozestup 7 týdnů** — a git log to potvrzuje dvěma
  samostatnými opravnými commity (`fix: ontology-registry — odstraneni vazeb na konkretni projekt`,
  `fix: … zrušení zbytečných číselných údajů`, oba 08-24/25).
- **Přenositelné?** **Přenositelná praxe.** Platí pro každou šablonu, každý sdílený `CLAUDE.md`,
  každý vzorový dokument pro tým. Kolega si odnese kontrolní otázku: *co v tomhle textu je pravda
  jen u mě?* — a to, že si ji **musí položit sám**, protože model prosáknutí sám neoznačí (čtyřikrát
  ho na to musel poslat člověk).
- **Okruh:** `X` antipatterny (+ `R` rozšíření)
- **Předvedatelnost:** dobrá. Vzít reálný projektový `CLAUDE.md`, dát úkol „udělej z toho obecnou
  šablonu", a pak hledat, co v ní zůstalo. Vždycky něco zůstane.

### E3 — Vrstva distribuce (marketplace, tokeny, cesty) je vlastní projekt
- **Co to je:** plugin funguje lokálně, ale rozchodit jeho instalaci pro tým je samostatná úloha —
  jméno marketplace, port, URL, cesty, přístupová práva.
- **Doklad:** 2026-07-09 09:14 — „Provedl jsem instalaci. A proč v marketplace vidím stále
  kvados-spec-factory? [Image #1]"; 2026-07-10 14:23 — „Marketplace chci nainstalovat z gitu nově.
  Napiš přesný postup."
- **Kolikrát:** ~13 promptů + v git logu pět samostatných `fix:` commitů (`Oprava cest`,
  `Oprava umístění souborů`, `Oprava url a verze`, `Oprava portu`, `Přejmenování marketplace`).
  Den 07-10 je celý o tomhle (31 bloků).
- **Přenositelné?** **`[infra]`.** Kolega, který plugin jen používá, se s tím nikdy nesetká —
  právě proto, že to už někdo odbyl. Do workshopu patří jen jako **položka rozpočtu**: „počítej
  s tím, že rozdat nástroj týmu stojí přibližně jeden pracovní den, i když nástroj už funguje."
- **Okruh:** `N` nastavení
- **Předvedatelnost:** slabá (nudné). Stačí ukázat výpis git logu.

### E4 — Audit, který nic nenašel (a co s tím)
- **Co to je:** Claude dostal zadání „reviduj / prověř", odvedl povrchní práci a chyby neodhalil.
  Nešlo o chybu modelu, ale o **chybu zadání** — a autor to tak i pojmenoval.
- **Doklad:** 2026-07-05 12:14 — „V předchozích turnech jsem chtěl, abys přesně tyto a podobné
  věci odhalil a navrhnul způsoby opravy. **Proč jsi to neudělal a jak bych musel zadat příště
  prompt, abys to správně udělal?**"
- **Kolikrát:** jednorázová diagnóza — ale se **zásadním následkem**: 12:23 „Napiš kompletní lepší
  prompt včetně smyčky *co dalšího je takhle*" → 12:24 „Nyní to podle tohoto promptu proveď" →
  13:16 vzniká jediný dlouhý strukturovaný prompt vzorku → 07-05 21:38 „Proveď postupně všechny
  opravy" → git commit 07-07 `feat: SpecFactory — optimalizace a opravy přes Fable 5`.
- **Přenositelné?** **Přenositelná praxe, nejsilnější ve vzorku.** Nepotřebuje nic než chat.
- **Okruh:** `U` učení (+ `M`)
- **Předvedatelnost:** **ideální ukázka na workshop.** Naživo: slabý prompt → chabý výsledek →
  meta-otázka → vylepšený prompt → spustit → porovnat. Celý oblouk je ve vzorku dohledatelný
  po minutách (12:14 → 13:16).

### Poznámka k tomu, co ve vzorku NENÍ (a je to důležité)
Zadání této fáze čekalo doklady o **config seamu** (union-merge listových klíčů, override přes
`_remove`), o **guardu na zápisové zóny** a o **bránách `spec_lint.py --intake/--dod`**.
Ve vzorku nejsou: grep přes všech 151 bloků dává `lint` 0×, `intake` 0×, `guard` 0×, `union` 0×,
`_remove` 0×, `config` 0×, `brána` 0×, `coverage` 0×.

Vysvětlení: **metoda i její brány vznikly dřív a jinde** — spec-factory byl do sdíleného repa
překlopen commitem 2026-07-04 (`feat: Sdílený Spec Factory plugin`), tedy den před začátkem
vzorku; předtím žil jako lokální orchestrátor v projektovém repu. Tenhle vzorek zachycuje
**fázi „udělej z toho produkt pro tým"**, ne fázi vynálezu.

Co ve vzorku je, jsou **dvě věty, ze kterých ta vynucovací vrstva vyrostla**:
- 2026-07-05 01:13 — „…aby při prvním použití na novém projektu nemusel mít uživatel v lokálním
  adresáři projekt FHB ani Alza." → *požadavek, který si vynutil konfigurační vrstvu.*
- 2026-07-05 21:38 — „Cílem je, aby skutečně byla **respektována specifika každého projektu**
  a **dodržování pravidel bylo kontrolováno a vynucováno**." → *požadavek, který z konfigurace
  udělal bránu.* Odpovídající commit: 07-07 `feat: SpecFactory — optimalizace a opravy`.

**Pro workshop je poučení tvrdší než doklad:** dokumentované gotchas (union-merge, `_remove`)
**nejsou vidět v promptech, protože se na ně narazí až při použití na druhém projektu.**
Kolega je nemá jak předvídat — proto musí být napsané v `CLAUDE.md`, ne v hlavě.

---

## 3. Kolik stálo postavit bránu (odpověď na otázku 3)

Ve vzorku je **jedna brána postavená celá od zadání k funkčnímu stavu**: brána na kvalitu nálezů
(`findings_rejected_ratio_max`) v spec-factory 1.8.0, spolu s příkazem `/review-spec`.

Doložený průběh — pět promptů, tři dny:

| Kdy | Prompt (zkráceně) | Co se stalo |
|---|---|---|
| 08-19 21:39 | „Přečti `C:\tmp\review-spec-zadani.md` a proveď ho celý" (52 zn.) | vznikla verze 1.8.0; commit 08-19 `feat: spec-factory 1.8.0 — /review-spec a brána na kvalitu nálezů` |
| 08-19 22:00 | „Rozšiř description. Dále připrav název a popis pro commit" | dokončení |
| 08-19 22:14 | „review-spec se mi v nové session nenabízí. Proč? Přitom mám verzi 1.8.0" | vada registrace příkazu (třída E2) |
| 08-20 14:48 | „Zjisti zpětnou vazbu k review-spec na základě Session ID: … Mají poslední úpravy v pluginu pozitivní dopad?" | **měření na reálném běhu** |
| 08-20 15:03 | „aplikovat pravidlo :159 i na už přijaté nálezy před eskalací" | commit 08-21 `docs: Zastavení falešných nálezů v /review-spec` |
| 08-21 19:04 | „Mám dojem, že AI má tendenci produkovat více, než úlohy skutečně potřebují. Proveď proto posouzení, zda přístup YAGNI … Můžeš přitom analyzovat nedávné sessions." | commit 08-21 `docs: Do /review-spec přidány principy YAGNI` |

**Skutečná cena, střízlivě:**
- **1 prompt na dispatch** — ale za ním **12,8 kB předem napsaného zadání** (`review-spec-zadani.md`,
  ověřená velikost). To je ta práce; chat je jen spouštěč.
- **+ 4 korekční prompty ve třech dnech**, z toho jedna vada mechaniky (E2) a dvě sémantická
  dolaďování, která nešla vymyslet u stolu.
- **+ jeden reálný produkční běh použitý jako testovací stolice.** Brána nebyla hotová, když
  kód běžel — byla hotová, až když se změřilo, co dělá na skutečném dokumentu.

**Realistický odhad pro kolegu: půl dne na napsání zadání brány + jeden běh + 2–3 dny doladění
podle toho, co brána reálně propustí a co zbytečně zastaví.** Rozhodně ne „hodina, napíšu si skript".
A druhá polovina odhadu je nepříjemnější: **brána bez měření vlastní falešné pozitivity je horší
než žádná** — přesně to řešily prompty z 08-20 a 08-21 (příliš mnoho odmítnutých nálezů neznamená
špatný dokument, ale špatně formulované zadání pro recenzenty).

---

## 4. Je 137 promptů na plugin dobrá investice? (odpověď na otázku 4)

**Ano — ale ne z důvodu, který by kolega čekal, a čísla se musí přerovnat.**

Co se za to koupilo (doloženo git logem a `plugin.json`):
- tři pluginy (`spec-factory` 1.9.0, `knowledge-loop` 2.0.0, `ontology-registry` 1.0.2),
- dva příkazy (`/spec`, `/review-spec`), osm agentů, hook-guard, dvě sady kontrolních skriptů,
- distribuce přes marketplace, kterou tým instaluje jedním příkazem,
- HTML prezentace, kterou lze pustit kolegům bez autora.

Proti tomu: **93 věcných promptů, z toho ~56 na vlastní inženýrství, koncentrovaných do 9 dní.**
To je řádově týden a půl soustředěné práce na trvalý nástroj pro celý tým. V téhle kalkulaci
to je jednoznačně dobrá investice.

**Co z toho kolega zvládne za desetinu — protože plugin už existuje:**
- **Použít ho.** `/spec` a `/review-spec` = 2 prompty. Veškerá cena 56 promptů je zaplacená.
- Zavedení na svém projektu: jeden příkaz (`spec_config.py --init`, resp. `/ontology-registry:init`).
  Ve vzorku to autora stálo celý plán adopce (07-07 12:03) — protože tehdy `--init` neexistoval.
- Instalace: 1 prompt. Autora stálo **den** (E3) a šest promptů na vysvětlení kolegyni (070–075).

**Co ale kolega nezdědí a stejně ho to bude stát:**
- Chyby třídy **E2** (nenačte se v nové session) — narazí na ně u prvního vlastního hooku.
- Chyby třídy **E1** (prosáknutý projekt) — narazí u první šablony, kterou dá týmu.
- Kalibraci brány, pokud si ji bude psát (kap. 3).

**Střízlivý závěr do workshopu:** 137 (reálně 93) promptů je dobrá investice do **produktu pro tým**
a špatná investice do **osobního nástroje jednoho člověka**. Zlomový bod je počet uživatelů:
Spec Factory se vyplatil, protože se překlopil do marketplace a používají ho i jiné projekty.
Kdyby zůstal lokálním skriptem, těch 56 promptů na inženýrství + den na distribuci se nevrátí.
Věta pro kolegu, který si řekne „taky si postavím plugin": **postav ho, až budeš mít druhého
uživatele. Do té doby stačí `CLAUDE.md` a jeden dobře napsaný prompt v souboru** (P10).

---

## 5. Přenositelná praxe zadávání — kandidáti

### P10 — Dlouhé zadání nepatří do chatu, ale do souboru · **NEJSILNĚJŠÍ KANDIDÁT**
- **Co to je:** zadání se napíše jako verzovaný Markdown dokument mimo chat; prompt v chatu je
  jen ukazatel na něj. Vypadá to jako lakonický prompt, ale je to obráceně — je to nejdelší zadání.
- **Doklad:**
  - 2026-08-19 21:39 — „Přečti `C:\tmp\review-spec-zadani.md` a proveď ho celý" (52 zn. → **12,8 kB zadání**)
  - 2026-08-24 11:32 — „Přečti si celý a proveď `…\docs\onboarding\PROMPT-plugin-ontology-registry.md`" (88 zn. → **7,3 kB zadání**)
- **Anatomie ověřená v obou souborech** (nadpisy, ne domněnka):
  `Proč (podklad — neměň závěry, můžeš je doplnit)` → dekompozice na části
  (`Část A1`, `Část A2`, `Část B`), každá s pevnou strukturou *Problém / Vstup / Návrhové
  rozhodnutí, které dodrž / Fáze* → `Mantinely (platí pro celý úkol)` → `Definition of done`.
  Druhý soubor má navíc `Krok 0 — ověření předpokladů (brána běhu, bez ní nepokračuj)`,
  `Antipatterny` a `Historie revizí`.
- **Kolikrát:** 2 čisté výskyty + 3 slabší varianty téhož (07-06 19:38 „Zohledni při tom studie:
  `C:\Temp\Studie-spec-factory`" + vložených 47 řádků; 07-07 17:43 odkaz na čtyři adresáře pravidel;
  07-07 12:03 `@..\docs\ADOPTION-ALZA.md`). Vzor, a navíc **vzor, který v čase silní** — oba
  nejčistší výskyty jsou nejnovější (srpen).
- **Přenositelná praxe? ANO, bez výhrad.** Nepotřebuje plugin, jen soubor. Řeší tři věci
  najednou: zadání se dá revidovat před spuštěním, dá se spustit znovu v jiné session/repu,
  a je v Gitu — takže se z něj stane dokumentace.
- **Okruh:** `K` kontext a grounding (+ `O` orchestrace)
- **Předvedatelnost:** výborná a efektní. Vedle sebe promítnout jednořádkový prompt a 12,8 kB
  soubor za ním. To je nejnázornější slide celé fáze.

### P1 — „Nejdřív napiš prompt, spustím ho pak" (prompt jako artefakt)
- **Co to je:** samostatný krok, kdy se nechá vyrobit prompt, ten se přečte a schválí, a teprve
  potom se spustí — často v jiné session, jiném repu nebo v úplně jiném nástroji.
- **Doklad:**
  - 2026-07-05 12:23 — „NApiš kompletní lepší prompt včetně smyčky *co dalšího je takhle*." → 12:24 „Nyní to podle tohoto promptu proveď."
  - 2026-07-06 19:12 — „Napiš prompt, který následně spustím na alphaxiv.org. Chci tam vyhledat studie, které pomohou vylepšit … mou Spec Factory. **Nic neměň, prompt do chatu.**"
  - 2026-07-09 13:28 — „Vytvoř prompt pro opravu FHB, který pak spustím v nové session v FHB repu."
  - 2026-08-24 12:14 — „napiš do chatu prompt, který mám spustit v repu Alzask."
- **Kolikrát:** **8 výskytů** (12:23, 18:48, 18:49, 19:12, 21:54, 13:28, 16:39, 12:14). Silný vzor.
- **Přenositelná praxe? ANO.** Nulová infrastruktura. Zvlášť cenné pro analytika: prompt
  napsaný pro jinou session je zároveň **předávka práce kolegovi**.
- **Okruh:** `O` orchestrace (+ `U`)
- **Předvedatelnost:** výborná. „Napiš mi prompt, který spustím v jiném repu" a pak ho vážně
  spustit ve druhém okně — publikum vidí, že prompt je přenosný artefakt, ne konverzace.

### P3 — Smyčka „co dalšího je takhle"
- **Co to je:** explicitní příkaz nezastavit se u prvního výskytu vzoru — u každého nálezu se
  aktivně hledá, jestli totéž není i jinde, a kola se opakují, dokud kolo nepřinese nový nález.
- **Doklad (2026-07-05 13:16, doslova):** „SMYČKA „CO DALŠÍHO JE TAKHLE": u každého nálezu se
  před jeho uzavřením zeptej, jestli stejný vzor není i jinde — a aktivně to prohledej (grep,
  křížové odkazy, opačný směr závislosti). Opakuj kola, dokud kolo nepřinese žádný nový nález.
  **Nikdy se nezastavuj u prvního výskytu vzoru.**"
- **Kolikrát:** 1× formulováno, ale je to **výsledek meta-otázky E4** a autor si o něj sám řekl
  jménem (12:23). Zapracovaná formulace, ne nápad.
- **Přenositelná praxe? ANO — nejlépe přenositelný odstavec celého vzorku.** Je to hotový
  copy-paste fragment. Funguje na cokoli, kde jde o konzistenci: FR, ADR, API kontrakt,
  přejmenování napříč dokumentací.
- **Okruh:** `M` mechanika kvality
- **Předvedatelnost:** výborná a měřitelná. Pustit revizi bez odstavce a s ním, ukázat počet nálezů.

### P5 — Formát výstupu předepsaný v promptu, včetně kanálu pro nejistotu
- **Co to je:** prompt určuje podobu reportu (číslování, řazení, povinná pole u nálezu) a navíc
  dává nejistotě legální kolonku, aby ji model nezametl.
- **Doklad (2026-07-05 13:16):** „VÝSTUP: očíslovaný seznam nálezů, seřazený od nejzávažnějšího.
  U každého: co to je (`soubor:řádek`), proč je to problém, návrh opravy — u nejednoznačných
  2–3 varianty s doporučením a důvodem." + „Pokud jsi na problém narazil, ale nevešel se do
  rozsahu nebo **si nejsi jistý, jestli to problém je — stejně ho uveď, označený jako
  „mimo rozsah / nejistý**"."
- **Kolikrát:** předepsaný formát 1× v plné podobě, ale **struktura se propisuje do všech
  navazujících promptů** (viz P6) a do off-chat zadání (P10, `Definition of done`).
- **Přenositelná praxe? ANO.** Ta druhá věta je to cenné: bez ní model nejisté nálezy tiše
  vypustí, protože „nemá být hlučný".
- **Okruh:** `M` mechanika kvality
- **Předvedatelnost:** dobrá. Ukázat report bez kolonky „nejistý" a s ní.

### P4 — Diagnóza oddělená od opravy
- **Co to je:** zákaz zapisovat, dokud člověk nerozhodl. V promptech velkými písmeny.
- **Doklad:** 2026-07-05 13:16 — „**NEAPLIKUJ ŽÁDNOU OPRAVU. Jen nahlas a navrhni.** … O opravách
  rozhodnu já."; 2026-07-06 18:48 — „**Nic nemodifikuj.**"; 2026-07-10 14:09 — „OK, oprav, ale
  **necommituj**. Potřebuji pak vyzkoušet reinstalaci."
- **Kolikrát:** **7 výskytů** (13:16, 18:48, 18:49, 19:12, 21:54, 14:09, 14:40).
- **Přenositelná praxe? ANO.** A stojí za to říct nahlas i souvislost: **stejné pravidlo autor
  zabudoval i do pluginu** („agenti navrhují, nikdy nerozhodují sami" — README pluginu).
  Způsob, jakým zadává, a způsob, jakým navrhl nástroj, je jedno a totéž pravidlo. To je dobrá
  pointa na konec workshopu.
- **Okruh:** `M` mechanika kvality (+ `N`)
- **Předvedatelnost:** výborná. Stejný audit s a bez té věty; ve druhém případě se soubory změní.

### P6 — Očíslované nálezy → výběr po číslech
- **Co to je:** protože si report vynutil číslování (P5), další prompt je jednoslovný výběr.
- **Doklad:** 2026-07-05 01:34 — „zapracuj nálezy 1, 2, 3"; 2026-07-05 12:35 — „Postupně vyřeš 1 až 7".
- **Kolikrát:** 3 výskyty (+ 07-05 21:38 „Proveď postupně všechny opravy").
- **Přenositelná praxe? ANO.** Nejlevnější existující trik: číslování v prvním promptu si
  vynutí, že desítka dalších promptů budou tři slova.
- **Okruh:** `M` mechanika kvality
- **Předvedatelnost:** výborná, triviální.

### P7 — Stálé rozhodovací pravidlo místo rozhodování případ od případu
- **Co to je:** místo odpovídání na každou dílčí volbu se předá kritérium.
- **Doklad:** 2026-07-05 21:38 — „Pokud je na výběr více variant, **vyber to kvalitnější,
  dlouhodobější a spolehlivější řešení.** Cílem je, aby skutečně byla respektována specifika
  každého projektu a dodržování pravidel bylo kontrolováno a vynucováno."
- **Kolikrát:** 1× čistě, ale spojený s největší dávkou oprav ve vzorku (a s commitem 07-07).
- **Přenositelná praxe? ANO.** Deleguje se vkus, ne odpovědnost. Pozor na protiváhu: viz X5 —
  právě tohle pravidlo je nejspíš spoluviníkem toho, že o šest týdnů později musel autor
  dopisovat YAGNI (08-21 19:04).
- **Okruh:** `O` orchestrace (+ `X`)
- **Předvedatelnost:** střední — je to jedna věta, efekt se ukáže až na objemu.

### P2 — „Zeptej se mě na dalších 10 věcí a já si vyberu"
- **Co to je:** model rozšíří kontrolní seznam za hranici toho, co zadavatele napadlo; člověk
  z něj vybere. Řeší „nevím, co nevím".
- **Doklad:** 2026-07-06 18:48 — „Vytvoř prompt k prověření efektivity Spec Factory. … **Zeptej
  se mě na další 10 věcí, které by bylo vhodné prověřit a já si vyberu**, co chci do promptu
  zahrnout. Nic nemodifikuj."
- **Kolikrát:** 2× (18:48 a 18:49 — druhý je přepis po `/model`), navazuje 19:00 vložením
  112 řádků výsledku zpět do chatu. Jednorázovka s velkým dopadem.
- **Přenositelná praxe? ANO.** Nejlepší poměr cena/výkon pro analytika, který začíná v neznámé
  oblasti. Číslo („10") je podstatné — bez něj model nabídne tři a skončí.
- **Okruh:** `A` analytické postupy (+ `U`)
- **Předvedatelnost:** výborná, hraje se to naživo za minutu.

### P11 — Vágní požadavek na kvalitu → jmenný seznam zakázaných slov
- **Co to je:** „ať je to srozumitelné" nefunguje. Funguje výčet konkrétních výrazů, které
  se nesmí použít.
- **Doklad:** 2026-07-10 20:11 — „Uprav dokumentaci, aby byla srozumitelná i pro méně zasvěcené
  lidi." → **nestačilo** → 20:15 — „… Například nepoužívej: *Paměť je cross-session / Rules jsou
  path-scoped / precedence vč. cizí-personal-informativní / Preflight / scaffoldne / skalár přepíše
  jádro / operacionalizuje / protichůdný enforcement* atd."
- **Kolikrát:** téma srozumitelnosti **5 výskytů** (07-06 20:28, 07-08 21:15, 07-10 20:11, 20:15,
  20:56). Dvojice 20:11 → 20:15 je učebnicová ukázka, jak se obecný požadavek zkonkretizuje.
- **Přenositelná praxe? ANO — a pro cílovou skupinu (analytici píšící pro business) mimořádně
  relevantní.** Doplňkový vzor tamtéž: 07-10 20:56 „Uprav styl podle nějakého oblíbeného
  popularizátora AI … **Nepřeháněj to se žargónem.**" — zadání stylu přes vzor, ne přes adjektiva.
- **Okruh:** `R` rozšíření (+ `A`)
- **Předvedatelnost:** výborná. Dvakrát tentýž odstavec, podruhé se zákazníkovým slovníkem.

### P9 — Reálný běh jako testovací stolice (zpětná vazba ze session)
- **Co to je:** hotový nástroj se neposuzuje čtením kódu, ale rozborem konkrétního běhu —
  Claude dostane ID session nebo cestu k pracovní složce a hodnotí, co se v ní skutečně dělo.
- **Doklad:**
  - 2026-07-06 21:54 — „Spustil jsem plugin v `…\docs\spec\2026-07-06_faktorial`. Chci zkontrolovat, zda plugin zafungoval správně, respektuje pravidla, funguje vynucování pravidel, jsou používány validační funkce ze správných zdrojů (cest) apod. Chci prozkoumat journal dané session."
  - 2026-08-20 14:48 — „Zjisti zpětnou vazbu k review-spec na základě Session ID: … **Mají poslední úpravy v pluginu pozitivní dopad?**"
  - 2026-08-21 19:04 — „… Můžeš přitom analyzovat nedávné sessions, kde se review-spec používalo."
- **Kolikrát:** **4 výskyty** (07-06 21:54, 07-09 16:39, 08-20 14:48, 08-21 19:04) — a vždy
  u milníku. Vzor.
- **Přenositelná praxe? ČÁSTEČNĚ — a hranice je poučná.** Rozebrat vlastní starou session umí
  každý (transkripty jsou lokálně). Ale **to, co dělá rozbor čitelným — journal běhu, pracovní
  složka, evidované nálezy — dodává plugin.** Bez něj se rozbor scvrkne na „přečti si, co jsme
  si povídali". Označuji jako **přenositelný princip + `[infra]` pro plnou verzi**.
- **Okruh:** `M` mechanika kvality (+ `O`)
- **Předvedatelnost:** střední. Dá se ukázat na `--resume` staré session; efektní verze
  potřebuje plugin.

### P8 — Screenshot jako doklad vady
- **Co to je:** místo popisu symptomu se přiloží obrázek obrazovky.
- **Doklad:** 2026-07-08 20:24 — „… Například v projektu `C:\Git\alzask` se v nové session
  zobrazuje: [Image #1]"; 2026-08-19 22:14 — „review-spec se mi v nové session nenabízí. Proč?
  Přitom mám verzi 1.8.0 [Image #1]"; 2026-07-09 09:56 — „Co mám nyní udělat před merge do main?
  [Image #2]".
- **Kolikrát:** **7+ výskytů** s `[Image #N]` (07-06 20:28, 07-08 20:24, 07-09 09:14, 09:56, 10:04,
  07-10 14:47 vložený text, 07-12 16:14, 08-19 22:14).
- **Přenositelná praxe? ANO.** Zajímavý detail k předvedení: **sekvence 20:22 → 20:22 → 20:24** —
  týž prompt třikrát, poprvé bez zmínky o symptomu, podruhé se slovem „zobrazuje:" a prázdnem,
  potřetí s reálně připojeným obrázkem. Autor se to naučil za tři minuty pokusem a chybou.
- **Okruh:** `K` kontext a grounding
- **Předvedatelnost:** výborná a okamžitá.

### P12 — Vysvětli variantu, pak rozhodnu
- **Co to je:** na rozcestí se nejdřív vyžádá srozumitelné vysvětlení důsledků, pak padne příkaz.
- **Doklad:** 2026-07-08 21:15 — „Vysvětli srozumitelně, co by obnášela varianta A." → 21:28 —
  „OK, proveď variantu A. Zároveň zruš ze Spec Factory tato pravidla…"
- **Kolikrát:** 2 čisté (21:15→21:28; 07-07 11:18 „odchylka 2: Je možné efektivně ošetřit pro
  Windows i MacOS?"). Doplňuje P5 („u nejednoznačných 2–3 varianty s doporučením").
- **Přenositelná praxe? ANO.** Levné, a bezprostředně po tomhle promptu padlo nejzásadnější
  architektonické rozhodnutí ve vzorku (viz M1).
- **Okruh:** `O` orchestrace
- **Předvedatelnost:** dobrá.

### P13 — Nápad do backlogu, ne do rozsahu
- **Co to je:** vedlejší nápad se zaparkuje s důvodem, místo aby rozšířil právě běžící úkol.
- **Doklad:** 2026-07-10 15:28 — „Napiš do backlogu, Přepsat prompty do angličtiny, protože
  šetří tokeny."
- **Kolikrát:** 1× — jednorázovka, ale čistá a dobře čitelná.
- **Přenositelná praxe? ANO.** Levná obrana proti rozšiřování rozsahu uprostřed běhu.
  Poznámka: nápad sám (angličtina kvůli tokenům) je legitimní, ale ve vzorku nikdy neproveden —
  což je zároveň důkaz, že backlog funguje jako brzda, ne jako plán.
- **Okruh:** `O` orchestrace
- **Předvedatelnost:** slabá (nudné, ale zaslouží jeden řádek na slidu).

### P14 — „Ještě tomu nerozumím" jako legitimní prompt
- **Co to je:** série dotazů, která nekončí správnou odpovědí, ale **uzavřením vlastního
  mentálního modelu** — a pak přechází k praktickému nasazení.
- **Doklad:** 2026-07-11 08:12 — „**Ještě tomu nerozumím.** Stačí pro kolegu, když má přístup
  pro čtení do …? Pak už může jen spustit instalaci?"; 08:16 — „MY se přihlašujeme všichni přes
  kerberos. Jak to s tím souvisí?"; 08:17 — „Když jsem totiž zprovozňoval instalaci … kolega
  mi vygeneroval nějaký token … Takže mě zajímá, zda bude muset správce takový token generovat
  i ostatním kolegům."; 08:22 — „Jak si mají kolegové vložit ten klíč do GITLAB_TOKEN?"
- **Kolikrát:** jeden souvislý blok **6 promptů** (070–075), plus 07-05 07:54 („V pravidlech mám
  „Stopa použití". Jak se toto v pluginu bude využívat?") a 08-25 08:40 („Co by znamenalo dorovnat
  Alzask ze šablony?"). Vzor.
- **Přenositelná praxe? ANO.** Pro workshop zvlášť užitečné, protože publiku dovoluje se ptát.
  Klíčový rys: v 08:17 autor **dodá vlastní protipříklad ze zkušenosti** („přes kerberos jsem
  přístup měl") — tím vyloučí vysvětlení, které mu nesedí. To je dovednost, ne povaha.
- **Okruh:** `U` učení
- **Předvedatelnost:** výborná. Vyloženě vhodné jako živý dialog na jevišti.

### P15 — Zadej hypotézu a přikaž, aby ji model opravil
- **Co to je:** v dlouhém zadání se vlastní představa označí jako **domněnka** a modelu se uloží
  povinnost ji doplnit ověřenými fakty a upozornit na rozpory.
- **Doklad (2026-07-12 15:17, uvnitř nejdelšího promptu vzorku):** „Teď ti popisuji vlastně
  jenom takovou svou vizi jak by to mohlo vypadat, ale **chci aby si to doplnil podloženými
  a ověřenými znalostmi. Pokud mé doporučení s tím nesouvisí nebo jsou v rozporu, tak mě na to
  upozorni.**" Podobně 07-13 21:47 — „Ten algoritmus není vůbec jednoduchý. Je potřeba to
  pořádně promyslet a inspirovat se na internetu, jak se obvykle takové úlohy řeší."
- **Kolikrát:** 2 výskyty, oba v promptech nad 1 600 znaků. Vzor u dlouhých zadání.
- **Přenositelná praxe? ANO — a je to jádro toho, proč dlouhé diktované prompty vůbec fungují.**
  Zadavatel nemusí mít pravdu; musí jen jasně označit, co je jeho dohad. Souvislost s nástrojem:
  totéž dělá straw-man ve fázi INTAKE pluginu — nejdřív hypotéza, pak otázky na její slabiny.
- **Okruh:** `K` kontext a grounding (+ `A`)
- **Předvedatelnost:** výborná. Tentýž nápad zadaný jako fakt vs. jako označená domněnka.

### P16 — Volba modelu před vypuštěním těžkého promptu
- **Co to je:** před nákladným úkolem se přepne model; poznávacím znakem je `/model` přímo před
  velkým promptem.
- **Doklad:** `/model` **20 ×** ve 151 blocích; 2026-07-05 12:22 `/model fable`, o hodinu později
  vzniká velký audit (13:16), jehož výsledkem je commit `feat: SpecFactory — optimalizace
  a opravy **přes Fable 5**`. Vzorec `/model` → dlouhý prompt se opakuje 5 × (viz X2).
- **Kolikrát:** 20 výskytů příkazu; 5 doložených párů „přepni a pošli".
- **Přenositelná praxe? ANO** (samotná volba modelu). Provedení má ale antipattern — X2.
- **Okruh:** `N` nastavení
- **Předvedatelnost:** dobrá. Tentýž audit na slabém a silném modelu, porovnat počet nálezů.

---

## 6. Antipatterny

### X1 — Přístupové tokeny vlepené do chatu · **nejostřejší poučení vzorku**
- **Co to je:** čtyři různé GitLab project tokeny v plném znění přímo v textu promptu.
- **Doklad (maskováno):** 2026-07-10 13:22 — „Otestuj, že pluginy jsou přístupní nově již
  i přes project token `glpat-o-EKU…`"; 13:41 — „Vyzkoušej tento token: `glpat-YKzz…`";
  13:52 — „Prověř ještě tento: `glpat-2LcG…`"; 14:06 — „**Původní tokeny byly smazány.**
  Vyzkoušej proto tento nový: `glpat-6pVH…`"
- **Kolikrát:** **4 tokeny v 5 promptech během 45 minut.** Vzor, ne uklouznutí.
- **Proč je to antipattern:** prompt není rozhovor, **prompt je zápis**. Skončí v transkriptu
  session, v journalu, v případném exportu — a jak tenhle dokument dokazuje, i v pozdější
  analýze, kterou dělá někdo jiný. Tři z těch tokenů musely být zneplatněny (14:06).
- **Přenositelný? Přenositelný antipattern.** Náprava je jednořádková a nic nestojí: token dát
  do proměnné prostředí nebo do souboru mimo repo a v promptu na něj jen odkázat („token je
  v `GITLAB_TOKEN`"). Autor k tomu sám dospěl — o den později se ptá „Jak si mají kolegové
  vložit ten klíč do `GITLAB_TOKEN`?" (07-11 08:22). Správný vzor je tedy ve vzorku taky.
- **Okruh:** `X` antipatterny (+ `N`)
- **Předvedatelnost:** výborná a nezapomenutelná — ukázat vlastní transkript s maskovaným
  tokenem a říct „tohle je teď v Gitu / v logu".

### X2 — Přepisování téhož promptu ručně po `/model`
- **Co to je:** prompt se napíše, pak `/model`, pak **se týž prompt naťuká celý znovu**.
- **Doklad:** 5 doslovných duplikátů: 07-05 12:14 / 12:16 · 07-06 18:48 / 18:49 ·
  07-06 19:38 / 19:39 (oba i s vloženými 47 řádky) · 07-08 20:22 / 20:24 · 07-10 22:05 / 22:06.
- **Kolikrát:** **5 výskytů** — vzor.
- **Přenositelný? Osobní zvyk (spíš neefektivita).** Přenositelná je jen ta myšlenka pod tím
  (P16 — vyber model dřív, než pošleš drahý prompt). Samotné přepisování je čistá režie:
  u dvojice 19:38/19:39 to znamená znovu vložit 47 řádků textu.
- **Okruh:** `X` antipatterny
- **Předvedatelnost:** dobrá jako odlehčení — „nejdřív model, pak prompt; a šipka nahoru existuje".

### X3 — Diktovaný prompt bez přečtení
- **Co to je:** nejdelší prompty vzorku jsou zjevně nadiktované a neopravené: „prezentaci,
  **jack** funguje Claude Code", „hmm nějaký script", „**planeta** odjede" (místo „paleta"),
  „pokud jim něco nejasnýho tak jsem je na to zeptej předem".
- **Doklad:** 2026-07-12 15:17 (1 679 zn.), 2026-07-13 21:47 (1 767 zn.), 2026-07-11 08:04.
- **Kolikrát:** 3 dlouhé prompty + jeden doložený případ, kdy to **selhalo významově**:
  07-11 08:04 „**Vysvětlím jí** princip instalace…" bylo o minutu později přepsáno na
  „**Vysvětli mi** princip instalace…" — přeslech změnil zadání z výkladu na pověření.
- **Přenositelný? Nuancovaný verdikt — a právě proto stojí za to ho na workshopu říct.**
  Diktovat je legitimní a **funguje to**: z prompt 15:17 vznikla prezentace, která je
  v repu (commit 07-12 `docs: Prezentace Jak Claude Code funguje`). Model překlepy ustojí,
  protože prompt nese **záměr, publikum, formát a označenou hypotézu** (P15). Antipattern je
  jen v tom nekontrolovat **první větu a klíčová slovesa** — na těch záleží, kdo co komu dělá.
- **Okruh:** `X` antipatterny (+ `R`)
- **Předvedatelnost:** výborná a lidsky vděčná — publikum si oddechne, že to nemusí být krásné.

### X4 — Prompt čitelný jen v rozjeté session
- **Co to je:** zadání, které je bez okamžitého kontextu nedešifrovatelné.
- **Doklad:** 2026-08-20 15:03 — „aplikovat pravidlo :159 i na už přijaté nálezy před eskalací"
  (60 znaků, odkaz na číslo řádku bez uvedení souboru); 07-07 11:18 — „odchylka 1: rozšiř regex
  i na tabulku".
- **Kolikrát:** ~4 (15:03, 11:18, 07-05 01:34, 07-05 12:35).
- **Přenositelný? Osobní zvyk — a uvnitř session legitimní.** Přenositelné je jen rozhraničení:
  **v běžící session zkratky ano, v promptu určeném k uložení nebo pro kolegu ne.** Jinak vznikne
  „knihovna promptů", ze které nikdo nic nepustí. Číslo řádku je navíc adresa, ne identita —
  po jedné editaci souboru míří jinam.
- **Okruh:** `X` antipatterny (+ `O`)
- **Předvedatelnost:** dobrá jako kontrast k P10.

### X5 — Delegovaný vkus („vyber to kvalitnější a dlouhodobější") plodí nadprodukci
- **Co to je:** obecné pobídky ke kvalitě vedou k tomu, že model postaví víc, než úloha
  potřebuje. Autor to o šest týdnů později musel léčit zvlášť.
- **Doklad:** 2026-08-21 19:04 — „**Mám dojem, že AI má tendenci produkovat více, než úlohy
  skutečně potřebují.** Proveď proto posouzení, zda přístup YAGNI (You Aren't Gonna Need It) je
  vhodné více aplikovat do review-spec a spec. Můžeš přitom analyzovat nedávné sessions."
  → commit 08-21 `docs: Do /review-spec přidány principy YAGNI`.
  Zdroj problému: 07-05 21:38 — „vyber to kvalitnější, dlouhodobější a spolehlivější řešení".
- **Kolikrát:** 1 doložený opravný zásah, ale zasahuje celý nástroj (dva příkazy) a autor jej
  formuluje jako **systémové pozorování**, ne jako jednu chybu.
- **Přenositelný? Přenositelný antipattern, a nepříjemně užitečný.** Kvalitativní adjektiva
  („robustní", „dlouhodobé", „důkladné") jsou pro model pobídka k objemu. Protilék je
  jmenovitý: **YAGNI napsat do zadání**, nebo dát rozsahu strop. Autor to ostatně sám zabudoval
  do off-chat zadání jako sekci `Mantinely`.
- **Okruh:** `X` antipatterny (+ `M`)
- **Předvedatelnost:** výborná. Tentýž úkol s „vyber nejrobustnější řešení" a s „nejmenší
  změna, která splní DoD" — porovnat objem diffu.

---

## 7. Momenty vzniku (prompt → artefakt), doloženo git logem

| Prompt | Vzniklo | Poznámka |
|---|---|---|
| 07-05 12:14 „Proč jsi to neudělal a jak bych musel zadat příště prompt…" → 12:23 → **13:16 velký audit** → 21:38 „Proveď postupně všechny opravy" | commit 07-07 `feat: SpecFactory — optimalizace a opravy přes Fable 5` | **Jediný dlouhý prompt vzorku vznikl z meta-otázky, ne z nápadu.** |
| **07-08 21:28** — „Zároveň zruš ze Spec Factory tato pravidla a jejich přenášení v rámci pluginu. **Je to mimo doménovou oblast Spec Factory a nepatří to sem. Možná později uděláme jiný plugin.**" | commit 07-08 `feat: Plugin knowledge-loop` (téhož dne) | **Nový plugin vznikl z rozhodnutí o rozsahu, ne z požadavku na funkci.** Nejlepší ukázka, že „vyříznout, co tam nepatří" je návrhový krok. |
| **07-09 08:24** — „Cizí pravidla se sice ukládají do Gitu, ale nesmí se nikdy načítat ostatním uživatelům." (87 znaků) | commit 07-09 `feat!: knowledge-loop 2.0.0 — cizí osobní pravidla se nikdy nenačítají` | **Jedna věta = breaking change a major verze.** Invariant formulovaný zákazem je nejsilnější druh zadání. |
| 07-09 09:14 — „A proč v marketplace vidím stále kvados-spec-factory?" | commit 07-09 `fix: Přejmenování marketplace kvados-spec-factory → kvados-plugins` | Otázka „proč vidím…" jako plnohodnotné hlášení vady. |
| 07-10 22:05 otázka → 22:12 „Ano, navrhni znění outline-revision kroku" → 22:14 „Ano, zapiš to" | commit 07-10 `docs: Po research možnost vrátit k plánování` | **Nový krok workflow za 9 minut, odstartovaný otázkou** („Nebylo by efektivnější…"), ne příkazem. |
| 08-19 21:39 — „Přečti … a proveď ho celý" | commit 08-19 `feat: spec-factory 1.8.0 — /review-spec a brána na kvalitu nálezů` | Nový příkaz + nová brána z off-chat zadání (P10). |
| 08-20 15:03 · 08-21 19:04 | commity 08-21 `Zastavení falešných nálezů` · `Do /review-spec přidány principy YAGNI` | Doladění brány podle reálných běhů (P9). |
| 08-24 11:32 — „Přečti si celý a proveď `PROMPT-plugin-ontology-registry.md`" | commit 08-24 `feat: Plugin ontology-registry` | Třetí plugin z jediného promptu + 7,3 kB zadání. |

---

## 8. Liší se zadávání u SW vývoje od zadávání u analýzy? (ano, doložitelně)

| | Vývoj pluginu | Analýza / dokument / prezentace |
|---|---|---|
| Typická délka | krátká — **56 % věcných promptů pod 100 znaků** | dlouhá — všechny 3 prompty nad 1 000 zn. a 4 ze 6 v pásmu 300–1000 zn. jsou dokumentační/analytické |
| Kde je kontext | **v repu** — cesty, `soubor:řádek`, `:159`, jméno commitu | **v promptu** — publikum, formát, tón, zakázaná slova, vlastní hypotéza |
| Jak se ověřuje | skriptem, novou session, opakovaným během | člověkem: „třetí odrážka je špatně formátovaná [Image #1]" (07-12 16:14) |
| Iterace | audit → očíslované nálezy → výběr po číslech | osnova → schválení → obsah → vzhled (07-12 15:17 → 15:31 → 16:02 → 16:10 → 16:14) |
| Společné oběma | volba modelu předem (P16), „nic neměň" (P4), screenshot jako doklad (P8), zadání do souboru u velkých úloh (P10) | |

Nejlépe viditelný rozdíl je **schvalovací brána u analytické práce**: 07-12 15:17 — „Nyní chci
vytvořit **jenom osnovu, až si ji schválíme, tak teprve budeš pokračovat dále**." U vývoje pluginu
se nic takového nevyskytuje — tam bránu dělá skript, ne věta v promptu. To je mimochodem přesně
princip, který si autor zapsal i do vlastní paměti („vynucuj bránou, neinstruuj v promptu").

---

## 9. Souhrn kandidátů

| ID | Kandidát | Verdikt | Okruh |
|---|---|---|---|
| P10 | Dlouhé zadání do souboru, prompt jen ukazatel | přenositelná | K, O |
| P1 | „Nejdřív napiš prompt, spustím ho pak" | přenositelná | O, U |
| P3 | Smyčka „co dalšího je takhle" | přenositelná | M |
| P5 | Předepsaný formát reportu + kanál pro nejistotu | přenositelná | M |
| P4 | Diagnóza oddělená od opravy („NEAPLIKUJ") | přenositelná | M, N |
| P6 | Očíslované nálezy → výběr po číslech | přenositelná | M |
| P7 | Stálé rozhodovací pravidlo | přenositelná (pozor na X5) | O |
| P2 | „Zeptej se mě na dalších 10 věcí" | přenositelná | A, U |
| P11 | Vágní kvalita → jmenný seznam zakázaných slov | přenositelná | R, A |
| P9 | Reálný běh jako testovací stolice | přenositelná zásada + `[infra]` na plnou verzi | M, O |
| P8 | Screenshot jako doklad vady | přenositelná | K |
| P12 | Vysvětli variantu, pak rozhodnu | přenositelná | O |
| P13 | Nápad do backlogu, ne do rozsahu | přenositelná | O |
| P14 | „Ještě tomu nerozumím" jako legitimní prompt | přenositelná | U |
| P15 | Zadej hypotézu a přikaž ji opravit | přenositelná | K, A |
| P16 | Volba modelu před těžkým promptem | přenositelná | N |
| E1 | Zdrojový projekt prosakuje do šablony | přenositelný poznatek | X, R |
| E2 | „V nové session se to nenačte" | přenositelný poznatek (náprava `[infra]`) | N, M |
| E3 | Distribuce nástroje je vlastní projekt (~den) | `[infra]` | N |
| E4 | Audit, který nic nenašel → meta-otázka | přenositelná | U, M |
| X1 | Tokeny v chatu | antipattern, přenositelný | X, N |
| X2 | Přepisování promptu po `/model` | osobní zvyk | X |
| X3 | Diktovaný prompt bez přečtení | antipattern s výhradou (funguje, když nese záměr) | X, R |
| X4 | Prompt čitelný jen v rozjeté session | osobní zvyk | X, O |
| X5 | Delegovaný vkus plodí nadprodukci | antipattern, přenositelný | X, M |

**Celkem 25 kandidátů: 18 přenositelných (vč. 3 antipatternů a 2 poznatků z chyb),
5 osobních zvyků / antipatternů bez přenosu, 2 `[infra]`.**

Tři nejcennější pro workshop, pokud by se muselo vybírat: **P10** (zadání do souboru — nejvyšší
pákový efekt a nejlepší slide), **E4 + P3** (meta-otázka „jak jsem to měl zadat" a smyčka „co
dalšího je takhle" — hotový copy-paste odstavec) a **X1** (tokeny v chatu — jediná věc ve vzorku,
která může někomu opravdu ublížit).
