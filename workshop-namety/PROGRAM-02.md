# Program 2. sezení — „Kde to leží a odkud to víš"

**Kdy:** `[TERMÍN ZATÍM NEURČEN]` · **Délka:** 120 min · **Publikum:** analytici Alza, po 1. sezení z 11. 9. 2026
**Rozsah:** struktura projektů Alza a FHB · rejstřík prvků systému · jak se odkazovat na zdroje · precedence při rozporu
**Styl:** **čistý výklad a diskuse — žádná práce u klávesnice, žádné generování.** Ukazují se **jen hotové artefakty**, ne proces jejich vzniku
**Stav:** návrh k odsouhlasení · **Navazuje:** `PROGRAM-01.md` slide 15 („pravidlo, který zdroj vyhrává") · karty: `NAMETY.md` K-08, K-09, K-10, K-05, K-06 · čísla: `DOKLADY.md` část 6

---

## Co si mají odnést (jedna věta na blok, vyslovit na konci)

1. Kostra projektu je u obou zákazníků stejná, liší se výbava. **Nekopíruj cizí výbavu, kopíruj kostru.**
2. Deset pravidel z osmnácti a třinácti je společných. To je jádro, které mezi projekty cestuje.
3. Rejstřík prvků je **index faktů, ne jejich autorita**.
4. Citace je `soubor:řádek` **plus úryvek**. Bez úryvku je to jen adresa.
5. Číslo řádku je adresa, ne identita. Kotva stárne a někdo ji musí opravovat.
6. Při rozporu rozhoduje **vrstva zdroje**, ne přesvědčivost formulace ani počet výskytů.
7. Minimální verze pro zítřek se obejde bez jediného nástroje: jeden soubor s rejstříkem, citace s úryvkem, napsané pořadí vrstev.

---

## Časový plán

> Sezení je bez práce u klávesnice, takže celou váhu nese deck a diskuse. Diskuse je proto rozdělená do bloků 3, 7 a 8, ne odložená na konec.
> Deck: `C:\Git\shared\docs\claude-code\claude-code-struktura-a-zdroje.html` (**GitLab — jen lokálně, nikdy nepushovat**).

| # | Čas | Min | Blok | Karta / deck | Role |
|---|---|---|---|---|---|
| 0 | 0:00 | 5 | Kde jsme skončili minule | deck 00–01 | výklad |
| 1 | 0:05 | 14 | **Dva projekty vedle sebe: co mají stejné** | K-08 · deck 02–04 | výklad |
| 2 | 0:19 | 14 | **Uvnitř `.claude/`: co tam je a co z toho jde do okna** | deck 05–06 | výklad |
| 3 | 0:33 | 12 | **Pravidlo jako artefakt**, sdílená a osobní vrstva | K-08 · deck 07–08 | výklad + diskuse |
| — | 0:45 | 5 | *pauza* | | |
| 4 | 0:50 | 18 | **Rejstřík prvků: co to je a jak se v něm hledá** | K-09 · deck 09–11 | výklad |
| 5 | 1:08 | 14 | **Jak se odkazuje na zdroj** | K-09 · deck 12–13 | výklad |
| 6 | 1:22 | 12 | **Citace stárne: tři verdikty** | K-10 · deck 14–15 | výklad |
| 7 | 1:34 | 14 | **Precedence: rozhoduje vrstva, ne přesvědčivost** | K-06 · deck 16–17 | výklad + diskuse |
| 8 | 1:48 | 12 | **Odkud začít u sebe zítra**, Q&A, zpětná vazba | deck 18–19 | diskuse |
| | 2:00 | | konec | | |

**Součet:** 5 + 14 + 14 + 12 + 5 + 18 + 14 + 12 + 14 + 12 = **120 min.**
**Čas účastníků u klávesnice:** 0 min. Vědomé rozhodnutí — místo toho je 26 minut vyhrazené diskuse (bloky 3, 7, 8).
**Kde ubrat, když se to nevejde:** blok 2 snese vypustit hooky a output styles (deck 05); blok 6 se dá zkrátit na jeden verdikt místo tří (deck 14 bez 15).

---

## Bloky podrobně

### 0 · Kde jsme skončili minule (deck 00–01, 5 min)
- **Výklad:** tři věty z prvního dílu, na kterých tenhle stojí. `CLAUDE.md` a pravidla jdou do okna **pokaždé**. **Dokument nese kontext, prompt nese rozhodnutí.** A poslední věta prvního dílu: *pravidlo, který zdroj vyhrává* — dnes se dozvíte, jak takové pravidlo vypadá napsané.
- **Co dnes není:** datová hranice a bezpečnost, jak psát zadání, revize výstupů. Každé z toho je samostatný díl.
- ⚠ Nepřehrávat celý první díl. Pět minut, tři věty, jdeme dál.

### 1 · Dva projekty vedle sebe (K-08, deck 02–04, 14 min)
- **Výklad:** dva zákazníci, dvě domény, dva různé týmy. A přesto skoro stejný adresářový strom. To není náhoda ani kopie — je to tvar, do kterého to dojde, když má agent v projektu pracovat opakovaně.
- **Ukázka (hotové artefakty):** stromy obou projektů vedle sebe, kořen a `docs/` do druhé úrovně. Nic se neotvírá.
- **Čísla (změřeno 10. 9. 2026):** `docs/` má alzask **16** podadresářů, fhb **12**, **společných 9** — `adr`, `analysis`, `api`, `fr`, `meetings`, `onboarding`, `pbs`, `spec`, `spec-grounding`.
- **Čím se liší:** Alza má navíc registr prvků (`ontology`), PLC vrstvu, dodavatele a přehledy sprintů; FHB má komunikaci se zákazníkem, zpětné vazby po verzích a plány. **Alza 5 revizních agentů, FHB 7 agentů továrny na specifikace.**
- **Ověřitelný výstup:** posluchač do příště najde ve svém projektu, které z těch devíti společných adresářů má, a které mu chybí.
- ⚠ **FHB je jiný zákazník.** Na plátno jde **jen strom adresářů**. Neotvírat žádný dokument FHB, ani `apibluesword-wcs-api.yml`. Rozhodnutí ukázat projekt pod pravým jménem padlo 10. 9.

### 2 · Uvnitř `.claude/` (deck 05–06, 14 min)
- **Výklad:** šest kategorií a u každé jedna věta, k čemu je. `settings.json` je jediné místo, kde se **vynucuje** (zákaz, oprávnění, hook) — všechno ostatní je kontext, který model *přečte a snaží se dodržet*. To je ten rozdíl, který se v prvním dílu jen naznačil.
- **Čím se to plní:** `CLAUDE.md` a pravidla jdou do okna při každém startu. Skill jde napřed **jen popiskem**, tělo až při použití. `docs/` nejde do okna nikdy celé.
- **Čísla (10. 9. 2026):** `CLAUDE.md` alzask **11 884 znaků / 199 řádků**, fhb **14 374 znaků / 367 řádků**.
- ⚠ **Nepoužívat srpnová čísla.** `DOKLADY.md` část 3 uvádí pro alzask 23 818 znaků — soubor se od té doby **zkrátil na polovinu**. Aktuální hodnoty jsou v části 6.
- **Kam dál:** [code.claude.com/docs/en/claude-directory](https://code.claude.com/docs/en/claude-directory), [/docs/en/memory](https://code.claude.com/docs/en/memory).

### 3 · Pravidlo jako artefakt (K-08, deck 07–08, 12 min)
- **Výklad:** pravidlo není odstavec v `CLAUDE.md`. Je to soubor s hlavičkou, která říká **kde platí** (`paths`), **jak silně** (`enforcement`), **odkud pochází** (`source`) a **s čím souvisí** (`related_rules`). Tělo má pevný tvar: *PLATÍ KDYŽ · NEPOUŽÍVAT KDYŽ · Odůvodnění (proč)*. To „nepoužívat když" je tam schválně — pravidlo bez hranice se poruší a pak se přestane brát vážně.
- **Ukázka:** hlavička `RULE-ONT-002_cituj-zdroj-ne-registr.md` doslova.
- **Čísla (10. 9. 2026):** alzask **18** sdílených pravidel, fhb **13**, **společných 10**. Alza navíc 8, FHB navíc 3.
- **Věta k vyslovení:** těch deset je jádro, které cestuje mezi projekty. Zbytek je doménový a nemá smysl ho kopírovat.
- **Diskuse (4 min):** *Máte něco, co říkáte kolegům opakovaně? To je kandidát na pravidlo.*
- **Ověřitelný výstup:** posluchač si do příště zapíše jednu větu, kterou opakuje, a rozhodne, kde by měla být zapsaná.

### 4 · Rejstřík prvků (K-09, deck 09–11, 18 min)
- **Výklad:** rejstřík je seznam všeho, s čím se v projektu pracuje — fyzické prvky, logické entity, číselníky, aktéři — s popisem, vazbami a **odkazem na zdroj, ze kterého to tvrzení pochází**. Přesně to, co bylo v nahrávce z 2. 9. Jde o to, aby si model nemusel doménu domýšlet.
- **Ukázka:** hlavička `INDEX.md` a jedna karta prvku.
- **Čísla (10. 9. 2026):** **176 entit** (fyzických 48 · logických 48 · číselníků 61 · aktérů 19) · **354 vztahů** · **703 atributů** · **97 rozporů**.
- **Jak se v tom hledá, aniž se zaplní okno:** `INDEX.md` 32 kB se přečte celý · karta prvku podle potřeby · termín se hledá grepem v `TERMS.tsv` (183 kB) · vazby v `RELATIONS.tsv` · **`ontology.yaml` 1,7 MB se nečte nikdy celý**. Přímá vazba na slide 14 prvního dílu.
- ⚠ **Nesklouznout do nástrojů.** Že registr někdo generuje, se zmíní jednou větou. Jinak se z dílu stane díl o nástrojích a publikum si odnese, že tohle není pro ně.
- **Kam dál:** blok 8, minimální verze bez nástrojů.

### 5 · Jak se odkazuje na zdroj (K-09, deck 12–13, 14 min)
- **Výklad:** citace má dvě části. **Adresu** `soubor:řádek` a **úryvek toho, co na tom místě stojí**. Karty prvků mají kvůli tomu vlastní sloupec — většinou pak zdroj vůbec nemusíš otevírat.
- **Druhé pravidlo:** *cituj původní zdroj, ne registr.* Registr je index faktů, ne jejich autorita. Kdo cituje registr, založí druhou vrstvu zastarávání: dokument → registr → zdroj. Kotvy hlídají jen jednu z nich.
- **Ukázka:** sloupec „co na tom místě stojí" na kartě prvku a znění `RULE-ONT-002`.
- **Druhý projekt, jiná konvence:** FHB používá u architektury citaci tvarem `[TAG §sekce "3–6 slov doslovně"]` plus značku jistoty. Jiný zápis, tentýž princip — **adresa plus doslovný úryvek**.
- **Ověřitelný výstup:** posluchač najde ve svém posledním dokumentu jedno tvrzení bez citace a doplní k němu zdroj i úryvek.

### 6 · Citace stárne (K-10, deck 14–15, 12 min)
- **Výklad:** **číslo řádku je adresa, ne identita.** Text nad citací se edituje a řádek pak ukazuje jinam. Přečteš cizí místo téhož dokumentu a nemáš jak to poznat. Proto se u citace drží **kotva** — otisk okolí několika řádků — a ověřuje se nástrojem, který vrátí verdikt, ne text.
- **Tři verdikty:** `OK` sedí · `POSUN` text se našel jinde · `ZMIZELA` text tam není a **tvrzení je třeba ověřit znovu**. Kdo opraví zmizelou citaci přepsáním čísla řádku, vyrobí horší stav než zastaralý: *tvar sedí, obsah lže.*
- **Číslo, kvůli kterému se pravidlo změnilo:** měření nad registrem 26. 8. — **z 15 hlášení jich 9 byl šum** (vložený odstavec *vedle* citace ji shodí stejně jako přepsaná věta). Pravidlo, které pošle člověku všechna hlášení, mu naloží devět mechanických případů smíchaných se šesti skutečnými. Člověk pak odklikne všechno, nebo to odloží. Obojí je horší než automatika.
- **Věta k vyslovení:** tohle je doklad, jak se pravidlo opravuje měřením, ne názorem. Původní verze posílala všechno člověku.
- ⚠ Neprodávat to jako hotové řešení. **Bez nástroje si posluchač odnese jen ostražitost** — a to je málo. Vyvážit blokem 8.

### 7 · Precedence (K-06, deck 16–17, 14 min)
- **Výklad:** když si dva dokumenty odporují, potřebuješ pravidlo, které rozhodne **předem**. Jinak rozhodne to, co model přečte první. A pozor: **novější nemusí vyhrát.** Specifikace může prohrát s daty ze skutečného nasazení.
- **Ukázka:** tabulka sedmi vrstev autority z registru a jeden zapsaný rozpor.
- **Věta k vyslovení:** *rozhoduje vrstva zdroje, ne přesvědčivost formulace ani počet výskytů.*
- **Druhé pravidlo, které stojí za vyslovení:** **vstupní dokument se needituje.** Procesní analýza, posouzení rizik a podepsané verze jsou záznam. Nález jde do soupisu rozporů, ne do nich.
- **Nejtěžší případ:** rozpor **uvnitř téže vrstvy**. Tam hierarchie nepomůže a rozhoduje člověk.
- **Diskuse (5 min):** *Který z vašich dokumentů je nejvyšší autorita?* Většinou to nikdo neví — a to je ta pointa.
- ⚠ Hierarchii musí někdo napsat, je to doménová práce. Neslibovat, že to udělá nástroj.

### 8 · Odkud začít u sebe zítra (deck 18–19, 12 min)
- **Výklad — tři kroky, každý bez jediného nástroje:**
  1. **Jeden soubor s rejstříkem.** Seznam prvků, se kterými pracuješ, jedna řádka na prvek. Nemusí být úplný.
  2. **Citace s úryvkem.** Ke každému tvrzení, které přebíráš odjinud, adresu a tři až šest slov doslova.
  3. **Napsané pořadí vrstev.** Který dokument vyhrává. Vejde se to na pět řádků.
- **Věta k vyslovení:** registr se 176 prvky vznikl tak, že někdo začal jedním souborem. Nástroje přišly potom, protože ručně to přestalo stačit — ne obráceně.
- **Zpětná vazba:** formulář `zpetna-vazba-02.html`, tři otázky, dvě minuty.
- **Most k dalšímu dílu:** podle zpětné vazby buď datová hranice (co poslat modelu a co ne), nebo jak psát zadání.

---

## Co je potřeba připravit

- [ ] **Termín a délku doplnit** do hlavičky a do patičky decku
- [ ] **Projít každý výřez, který jde do decku, řádek po řádku** — registr obsahuje jména dodavatelů, zákaznická čísla a zapsané spory. Ukazovat strukturu a metadata, ne věcný obsah sporů
- [ ] **Vytisknout formuláře** podle počtu účastníků + 3 rezervní
- [ ] **Zkušební průchod nahlas s hodinkami** — bez cvičení je 120 minut samotného výkladu hodně, hlídat tempo
- [ ] **Zpětná vazba z 1. sezení vyhodnocena** → pokud z otázky 3 vyjde silně bezpečnost, tenhle díl se posune a jede se Díl 2 z katalogu
- [ ] **Na prezentačním stroji:** zvětšení stránky 100 % (Ctrl+0), celá obrazovka (F11)

---

## Co záměrně vypadlo a kam patří

| Vypadlo | Proč | Kam |
|---|---|---|
| Datová hranice, tři zákazy, rewind, plan mode (N-01–N-04, M-02) | samostatné téma, nemíchat s dohledatelností | Díl 2 katalogu |
| Jak psát zadání, straw-man, rozpočet na otázky | navazuje, ale je toho na celý díl | Díly 3 a 4 |
| Revize výstupů, triáž nálezů, slepý recenzent | Díl 7 | podle zpětné vazby |
| Skills, subagenti, hooky jako vlastní výbava | dnes jen zmíněny jako součást `.claude/` | Díl 9 |
| Jak registr vzniká — generátor, plugin, dávkové přeukotvení | jedna věta, jinak by z toho byl díl o nástrojích | případná dílna pro zájemce |
| Obsahové konvence FR, ADR a specifikací (šablony, changelog, trace) | dnes jen struktura adresářů, ne obsah dokumentů | Díl 3 |
