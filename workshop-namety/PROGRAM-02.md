# Program 2. sezení — „Kde to leží a odkud to víš"

**Kdy:** `[TERMÍN ZATÍM NEURČEN]` · **Délka:** 120 min · **Publikum:** analytici Alza, po 1. sezení z 11. 9. 2026
**Rozsah:** osm druhů dokumentů, které v projektu Alza vznikly — u každého **proč** a **jaký má princip**
**Styl:** výklad ze snímků + **živá ukázka lektora** u každého tématu. Účastníci u klávesnice nepracují.
**Stav:** přestavěno 2026-09-11 podle zadání vlastníka · **Navazuje:** `PROGRAM-01.md` slide 15 („pravidlo, který zdroj vyhrává")
**Deck:** `C:\Git\shared\docs\claude-code\claude-code-struktura-a-zdroje.html` (**GitLab — jen lokálně, nikdy nepushovat**)
**Čísla:** `DOKLADY.md` části 6 a 7 · kontrola `_raw/overit-deck-02.py`

---

## Jak je díl postavený

Od snímku 03 jde **osm témat, každé po dvou snímcích**:

| Snímek | Co na něm je |
|---|---|
| **A — proč** | jaká bolest ten artefakt vyvolala. Bez čísla z projektu se ten snímek nedá odvyprávět |
| **B — princip** | jak to vypadá a proč zrovna takhle. Jeden zkrácený výřez a tři až pět vět |

**Praktické ukázky nejsou na snímcích.** Po každé dvojici otevře lektor skutečný soubor v editoru.
Snímek nese důvod a princip, obrazovka nese realitu. Kdyby se ukázka nestihla, snímky dávají smysl samy o sobě.

**Rozpočet na blok:** zhruba 5 minut snímky + 5 až 7 minut živá ukázka a otázky.
Kdo mluví ze snímků déle než pět minut, nestihne ukázku — a ukázka je to, co si publikum zapamatuje.

---

## Co si mají odnést (jedna věta na téma, vyslovit na konci bloku)

1. **Rejstřík** odpovídá na „existuje to a mám to otevírat", ne na „co v tom je".
2. **Zápis ze schůzky** není přepis. Rozhodnutí nahoře, doklad dole.
3. **ADR** neodpovídá na „co platí", ale na „proč to tak je". Nahrazené se nemaže.
4. **FR** má hodnotu ve dvou vazbách: nahoru na rozpad produktu, dolů na testy.
5. **TC** je jediné místo, kde se pozná, že specifikace je dvojznačná.
6. **Rejstřík prvků** je index faktů, ne jejich autorita. Citace je adresa *plus* úryvek.
7. **Registr dotazů** má cenu až s místem dopadu — kde je odpověď zapsaná ve specifikaci.
8. **Skill** je postup jako soubor. V okně je z něj jen jméno a popis; podle popisu se model rozhoduje.

---

## Časový plán

| # | Čas | Min | Blok | Deck | Role |
|---|---|---|---|---|---|
| 0 | 0:00 | 10 | Kde jsme skončili · dva projekty vedle sebe | 00–02 | výklad |
| 1 | 0:10 | 12 | **Indexové soubory** | 03–04 | výklad + ukázka |
| 2 | 0:22 | 12 | **Zápisy ze schůzek** | 05–06 | výklad + ukázka |
| 3 | 0:34 | 14 | **ADR** | 07–08 | výklad + ukázka + diskuse |
| — | 0:48 | 5 | *pauza* | | |
| 4 | 0:53 | 12 | **FR** | 09–10 | výklad + ukázka |
| 5 | 1:05 | 12 | **TC** | 11–12 | výklad + ukázka |
| 6 | 1:17 | 14 | **Ontologie prvků** | 13–14 | výklad + ukázka + diskuse |
| 7 | 1:31 | 12 | **Komunikace s dodavateli** | 15–16 | výklad + ukázka |
| 8 | 1:43 | 12 | **Skilly a pluginy** | 17–18 | výklad + ukázka |
| 9 | 1:55 | 5 | Shrnutí, Q&A, zpětná vazba | 19 | diskuse |
| | 2:00 | | konec | | |

**Součet:** 10 + 12 + 12 + 14 + 5 + 12 + 12 + 14 + 12 + 12 + 5 = **120 min.**
**Čas účastníků u klávesnice:** 0 min. Diskuse je vyhrazená v blocích 3, 6 a 9 (celkem 13 min) a vejde se i do otázek u ukázek.

**Kde ubrat, když se to nevejde.** Bloky jsou nezávislé dvojice, takže se škrtá celé téma, ne půlka:
vypustit **TC** (blok 5) nebo **skilly a pluginy** (blok 8). Obojí ušetří 12 minut a nic dalšího se nerozsype.
**Neškrtat ontologii** — na ni navazuje minimální verze ve shrnutí.

---

## Bloky podrobně

### 0 · Kde jsme skončili · dva projekty vedle sebe (deck 00–02, 10 min)
- **Výklad:** tři věty z prvního dílu. Model si nic nepamatuje. **Dokument nese kontext, prompt nese rozhodnutí.** A poslední věta minula: *pravidlo, který zdroj vyhrává.*
- **Slide 02 — dva projekty:** dva zákazníci, dvě domény, skoro stejný adresářový strom. Přepínačem zvýraznit společné adresáře. **Devět z šestnácti a dvanácti** je stejných.
- **Věta k vyslovení:** kopírujte kostru, ne cizí výbavu. Výbava odpovídá tomu, co ten projekt bolelo. Dnešní díl je o té výbavě — kus po kuse.
- ⚠ **FHB je jiný zákazník.** Na plátno jde **jen strom adresářů**. Neotvírat žádný dokument FHB. Rozhodnutí ukázat projekt pod pravým jménem padlo 10. 9. 2026.
- ⚠ **Korekce prvního dílu.** Deck dílu 1 na slidu 15 říká, že `CLAUDE.md` a `rules/` jdou do okna pokaždé. Přesně: **pravidlo bez uvedené cesty jde do okna vždy, pravidlo s cestou až na vyžádání.** Všech 18 sdílených pravidel alzask i 13 fhb má `paths:`, takže se při startu session nenačte ani jedno. Vyslovit jednou větou, nerozebírat — viz `DOKLADY.md` 6.4.
- ⚠ Nepřehrávat celý první díl. Deset minut i s tím stromem.

### 1 · Indexové soubory (deck 03–04, 12 min)
- **Snímek A — proč:** v jedné složce 66 zápisů, ve vedlejší 54 rozhodnutí. Bez rejstříku existují jen dvě odpovědi: otevřít všechno, nebo se zeptat kolegy. **Tři soubory, tři adresáti:** README pro člověka na vyžádání, INDEX jako registr, `CLAUDE.md` pro agenta a automaticky.
- **Snímek B — princip:** hlavička `docs/adr/INDEX.md`. Práh zhruba **deset položek**. Stav v rejstříku musí odpovídat frontmatteru zdroje. Z té trojice zastarává rejstřík nejrychleji.
- **Živá ukázka:** otevřít `docs/adr/INDEX.md` celý, ukázat tabulku kategorií a proklik do `api/INDEX.md`. Pak `docs/fr/README.md` vedle toho — jiná role, jiný obsah.
- **Čísla (11. 9. 2026):** 54 ADR / 28 aktivních / 25 navržených / 1 override; kategorie process 20, api 16, hw 10, db 4, integration 3. Rejstříků v `docs/adr` je **sedm**.
- **Zdroj pravidla:** `.claude/rules/shared/RULE-DOC-001_orientacni-soubory.md` — včetně věty, proč se do `CLAUDE.md` nepíšou adresářové stromy.
- **Ověřitelný výstup:** posluchač řekne, který ze svých adresářů už překročil práh deseti položek a rejstřík nemá.

### 2 · Zápisy ze schůzek (deck 05–06, 12 min)
- **Snímek A — proč:** hodinový přepis má tisíce slov a pět rozhodnutí, která nejsou označená. **V přepisu zní obě strany sporu stejně sebevědomě.** Model z něj závěr nepozná, člověk po měsíci taky ne.
- **Snímek B — princip:** hlavička (datum, účastníci, jméno zdrojového přepisu) → *Klíčová rozhodnutí* číslovaná → *Operační body (bez ADR)* → celý přepis doslova pod tím.
- **Živá ukázka:** `docs/meetings/2026-03-05 … idempotency.md` — projet prvních dvacet řádků, pak sjet dolů k přepisu a ukázat, z čeho ten souhrn vznikl.
- **Věta k vyslovení:** přepis je doklad, zápis je rozhodnutí. Nejsou to dva formáty téhož.
- **Věta, která patří nahlas:** souhrn navrhne agent, **rozhodnutí za něj potvrzuje člověk**. Tohle je místo, kde se delegovat nedá.
- **Čísla:** 66 zápisů v `docs/meetings/`.
- ⚠ Zápis obsahuje jména účastníků a věcný obsah jednání. **Vybrat dopředu jeden, který se dá promítnout** — ten o idempotency je bezpečný, je čistě technický.

### 3 · ADR (deck 07–08, 14 min)
- **Snímek A — proč:** „Proč se u GET nevyžaduje hlavička s ID požadavku?" Bez záznamu žije odpověď v hlavě jednoho člověka. Za půl roku se rozhodne opačně a **nikdo neví, že se něco měnilo**.
- **Snímek B — princip:** hlavička `ADR-ASK-API-008`. ID je trvalé. **Nahrazení se zapisuje na obě strany** — staré ADR zůstane s odkazem na nástupce. Recenzenti jmenovitě, se stavem. Tělo: kontext → rozhodnutí → důsledky.
- **Živá ukázka:** otevřít to ADR celé a ukázat, jak je dlouhý kontext oproti samotnému rozhodnutí. Pak jedno `accepted` vedle jednoho `draft`.
- **Věta k vyslovení:** ADR neodpovídá na „co platí" — na to je specifikace. Odpovídá na „proč to tak je".
- **Diskuse (4 min):** *Kde je u vás zapsané rozhodnutí, na které se ptáte nejčastěji?* Většinou nikde, nebo v mailu — a to je ta pointa.
- **Ověřitelný výstup:** posluchač jmenuje jedno rozhodnutí ze svého projektu, které nikde napsané není, a řekne, kdo je jeho vlastníkem.

### 4 · FR (deck 09–10, 12 min)
- **Snímek A — proč:** věta ze zápisu se nedá odškrtnout. **Požadavek říká, co má systém umět. Rozhodnutí říká, proč jsme zvolili tuhle cestu.** Když se to smíchá, nedá se revidovat ani jedno.
- **Snímek B — princip:** hierarchie sekce → kategorie → oblast → požadavek. Tvary ID `FR-COMP-{WES|API|UI}-…` a `FR-BP-…`. **Z ID se pozná umístění bez otevření souboru.**
- **Živá ukázka:** strom `docs/fr/` do druhé úrovně a jeden FR otevřený — ukázat, na co se odkazuje nahoru a dolů.
- **Čísla:** 52 požadavků, dvě sekce.
- **Věta k vyslovení:** struktura složek je pro agenta stejná informace jako text — a je o řád levnější. Vypsat adresář stojí pár desítek tokenů, přečíst padesát dokumentů stojí celé okno.
- **Ověřitelný výstup:** posluchač řekne, podle čeho jsou pojmenované jeho požadavky a jestli z názvu poznat, kam patří.

### 5 · TC (deck 11–12, 12 min)
- **Snímek A — proč:** **z dvojznačné věty se scénář napsat nedá.** Kdo píše scénáře, čte specifikaci pozorněji než kdokoli jiný a najde v ní díry dřív než vývojář.
- **Snímek B — princip:** `TC-BP-DECANT-002-01.S03` — případ tečka scénář. **`@S` se nikdy nepřečísluje ani nerecykluje**, smazaný nechá mezeru. Tagy nesou klasifikaci, stav a datum má každý scénář zvlášť. Kroky mluví doménou, ne názvy služeb.
- **Živá ukázka:** jeden `.feature` soubor a vedle něj řádek z `tc-list.csv` — dokument pro čtení, tabulka pro filtr.
- **Čísla (11. 9. 2026):** 946 scénářů ve 108 případech, 109 souborů `.feature`, hotových 862, rozepsaných 84, negativních **409 z 946**.
- **Zdroj konvence:** `RULE-TC-001_tc-konvence.md`.
- **Věta k vyslovení:** stabilní identifikátor je jediné, co drží dohledatelnost přes refaktoring. Přečíslování je ztráta vazby.
- ⚠ Tohle je blok, který se škrtá první, když se čas nevejde.

### 6 · Ontologie prvků (deck 13–14, 14 min)
- **Snímek A — proč:** dopravník, conveyor, `CONV_01`, „ta pásovka u dekantace". **Model si doménu domýšlí, když ji nemá kde vzít — a domyslí ji věrohodně.** To je horší, než kdyby odpověď odmítl.
- **Snímek B — princip:** tabulka souborů registru a způsobu čtení. `INDEX.md` celý, karta na vyžádání, TSV grepem, **`ontology.yaml` 1,7 MB nikdy celý**. Citace je adresa *plus* úryvek. **Cituj zdroj, ne rejstřík.**
- **Živá ukázka:** hlavička `INDEX.md`, jedna karta prvku se sloupcem „co na tom místě stojí", a grep v `TERMS.tsv` na jeden termín.
- **Čísla (10. 9. 2026):** 176 prvků · 354 vazeb · 703 atributů · 97 rozporů.
- **Diskuse (5 min):** *Kolik jmen má u vás ta samá věc?* Odpověď bývá tři a je to nejrychlejší cesta k tomu, proč registr vůbec vznikl.
- ⚠ **Nesklouznout do nástrojů.** Že registr někdo generuje, se zmíní jednou větou. Jinak se z toho stane díl o nástrojích a publikum si odnese, že tohle není pro ně. **Vyvážit shrnutím** — minimální verze je jeden soubor.
- ⚠ Registr obsahuje jména dodavatelů a zákaznická čísla. Kartu prvku vybrat dopředu a projít řádek po řádku.

### 7 · Komunikace s dodavateli (deck 15–16, 12 min)
- **Snímek A — proč:** stav býval v Excelu a v mailboxu a dal se vyčíst jen ručním čtením. **„Odpověděli" a „odpověděli dost" nejsou totéž** — a ten rozdíl v mailu vidět není.
- **Snímek B — princip:** trvalé ID převzaté z registru dodavatele, **nepřejmenovává se**, odkazuje na ně i on. Odpověď doslova. U „částečně" je napsané, co konkrétně chybí. A `landed_in` — kde je odpověď zapsaná ve specifikaci.
- **Živá ukázka:** `OTEVRENE.md` s otevřenými otázkami a proklik z jednoho `landed_in` do místa ve specifikaci. Případně prohlížeč `questions-view.html`.
- **Čísla (11. 9. 2026):** 152 otázek (bullseye 126, bluesword 26) · zodpovězeno 58 · částečně 52 · bez odpovědi 32 · odmítnuto 10 · vyplněné `landed_in` u **61**.
- **Věta k vyslovení:** bez místa dopadu je registr jen hezčí mailbox.
- ⚠ Otázky jsou v angličtině a obsahují **jména dodavatelů a technické detaily zakázky**. Vybrat dopředu dva až tři záznamy, které se dají promítnout.

### 8 · Skilly a pluginy (deck 17–18, 12 min)
- **Snímek A — proč:** postup v hlavě funguje, dokud je u toho ten člověk. Postup v `CLAUDE.md` se načte pokaždé, tedy se za něj **platí kontextem i ve dnech, kdy se nepoužije**. Skill je třetí možnost: v okně je jen jméno a popis, tělo až při použití.
- **Snímek B — princip:** **skill** je soubor s postupem · **příkaz** je tenká obálka, která ho vyvolá s určitým vstupem · **plugin** je balík skillů, příkazů, agentů a kontrol s číslem verze.
- **Živá ukázka:** `SKILL.md` skillu na dotazy dodavatelům — hlavička s popisem a tabulka situací. Pak příkaz `/dodavatele:mail`, který je proti němu krátký. A nakonec `/plugin` se seznamem nainstalovaných balíků.
- **Čísla:** alzask 2 skilly, 9 příkazů, 5 agentů. Skill na rejstřík prvků je **generovaný** z `ontology.yaml`.
- **Věta k vyslovení:** popis je jediné, co model vidí předem. Špatný popis = skill, který se nikdy nespustí.
- **Věta, která patří nahlas:** tohle je poslední krok, ne první. Balí se postup, který se osvědčil.
- **Doklad z dokumentace:** skill descriptions se načítají do okna, tělo až při vyvolání — [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills), ověřeno 11. 9. 2026.

### 9 · Shrnutí, Q&A, zpětná vazba (deck 19, 5 min)
- **Věta, na které to celé stojí:** *každý z těch osmi souborů vznikl z jedné otázky, která přišla potřetí.* Žádný z nich nevznikl proto, že to tak má být.
- **Čtyři věci, které jdou udělat bez nástroje:** rejstřík místo otevírání všeho · trvalé ID místo přejmenovávání · citace s úryvkem místo paměti · napsané pořadí vrstev.
- **Zpětná vazba:** formulář `zpetna-vazba-02.html`, tři otázky, dvě minuty.
- **Most k dalšímu dílu:** podle formuláře buď datová hranice (co poslat modelu a co ne), nebo jak psát zadání.

---

## Co je potřeba připravit

- [ ] **Termín doplnit** do hlavičky programu a do patičky decku
- [ ] **Vybrat dopředu soubory pro živé ukázky** a projít je řádek po řádku — zápis, karta prvku a záznamy dodavatelů obsahují jména a zákaznická čísla
- [ ] **Otevřít si je předem ve dvou oknech editoru**, aby se během bloku jen přepínalo; hledání souboru na plátně sežere celou ukázku
- [ ] **Vytisknout formuláře** podle počtu účastníků + 3 rezervní
- [ ] **Zkušební průchod nahlas s hodinkami** — osm ukázek za sebou svádí k tomu mluvit u každé o dvě minuty déle, což je šestnáct minut přes čas
- [ ] **Zpětná vazba z 1. sezení vyhodnocena** → pokud z otázky 3 vyjde silně bezpečnost, tenhle díl se posune a jede se Díl 2 z katalogu
- [ ] **Na prezentačním stroji:** zvětšení stránky 100 % (Ctrl+0), celá obrazovka (F11)
- [ ] **Spustit `_raw/overit-deck-02.py`** těsně před sezením — projekty žijí a čísla na snímcích se hýbou

---

## Co záměrně vypadlo a kam patří

| Vypadlo | Proč | Kam |
|---|---|---|
| Kostra vs. výbava obou projektů podrobně, obsah `.claude/`, co jde do okna při startu | přestavba 11. 9. — bylo to příliš podrobné, zůstal z toho slide 02 a jedna věta | materiál je v `DOKLADY.md` 6.1–6.4 |
| Pravidlo jako artefakt, deset společných pravidel | totéž | `DOKLADY.md` 6.3, karta K-08 |
| Kotvy citací, tři verdikty, sedm vrstev autority, zápis rozporu | totéž — vrstvy autority dnes zazní jen jako jedna ze čtyř věcí ve shrnutí | `DOKLADY.md` 6.6–6.7, karty K-06 a K-10 |
| Datová hranice, tři zákazy, rewind, plan mode | samostatné téma | Díl 2 katalogu |
| Jak psát zadání, straw-man, rozpočet na otázky | je toho na celý díl | Díly 3 a 4 |
| Revize výstupů, triáž nálezů, slepý recenzent | samostatné téma | Díl 7 |
| Jak registr vzniká — generátor, dávkové přeukotvení | jedna věta, jinak by z toho byl díl o nástrojích | dílna pro zájemce |
| Obsahové šablony dokumentů (co přesně má být v které sekci) | dnes jde o **důvod a princip**, ne o šablonu | Díl 3 |

---

## Poznámka k historii tohoto programu

První verze (10. 9. 2026) vedla souvislý oblouk od struktury projektů přes rejstřík prvků
k precedenci zdrojů — devět bloků, deck o dvaceti snímcích. Vlastník po revizi rozhodl,
že **od snímku 3 je to příliš podrobné**, a zadal osm témat po dvou snímcích s tím,
že praktické ukázky dělá živě. Deck i program jsou přestavěné 11. 9. 2026.
Původní měření nejsou zahozená — leží v `DOKLADY.md` část 6 a v kartách `K-08` až `K-10`.
