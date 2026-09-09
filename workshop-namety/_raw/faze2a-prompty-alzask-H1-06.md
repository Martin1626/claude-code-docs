# FÁZE 2a — Destilace praxe zadávání z promptů AlzaSk (H1 + 06/2026)

Zdroje: `C:\tmp\workshop-namety\_raw\prompty-alzask-H1.md` (14 promptů, 2026-01 – 2026-05),
`C:\tmp\workshop-namety\_raw\prompty-alzask-06.md` (235 promptů, 2026-06).
Analytické skripty: `analyza_h1_06.py`, `analyza2.py` (výstupy `analyza_out.txt`, `analyza2_out.txt`).

Legenda okruhů: `K` kontext a grounding · `R` rozšíření · `M` mechanika kvality · `O` orchestrace ·
`A` analytické postupy · `U` učení · `X` antipatterny · `N` nastavení
Klasifikace: **PŘENOSITELNÉ** (kolega si odnese hned) · **[infra]** (nutno postavit pro tým) ·
**OSOBNÍ ZVYK** (nemá hodnotu pro workshop, nebo funguje jen v tomto setupu)

---

## 0. Kvantitativní obraz (základ pro kalibraci workshopu)

| Metrika | Hodnota |
|---|---|
| Promptů celkem | 249 (H1 = 14, 06 = 235) |
| Slash příkazů | 90 (36 %) |
| Promptů < 20 znaků | 83 (33 %) |
| 20–99 znaků | 92 (37 %) |
| 100–299 znaků | 48 (19 %) |
| 300–999 znaků | 20 (8 %) |
| **≥ 1000 znaků** | **6 (2,4 %)** — z toho 4 jsou tentýž opakovaný prompt |
| Promptů s odkazem na soubor/cestu (`@`, `C:\`) | 31 (12 %) |
| Promptů obsahujících otázku (`?`) | 53 (21 %) |
| Potvrzení/schválení („ano, …", „OK", „schvaluji") | 17 |
| Slepé „pokračuj" | 7 |
| Kandidátů na korekci (obsahová heuristika, ručně tříděno) | 79 |
| Promptů zmiňujících worktree | 19 |

**Nejdůležitější číslo pro workshop:** dlouhá zadání jsou 2 % promptů, a i ta jsou z poloviny
kopie téhož textu. **Praxe nestojí na „napiš perfektní dlouhý prompt", ale na krátkých
promptech nad dobře postaveným kontextem session.** Tohle je přesně opak toho, co kolegové
očekávají („naučte mě prompt engineering"), a je to hlavní teze, kterou musí workshop nést.

Nejfrekventovanější slash příkazy: `/spec` 13×, `/context` 13×, `/rename` 12×, `/resume` 11×,
`/compact` 5×, `/body-z-jednani` 5×. Tj. **čtvrtina slash příkazů je správa kontextu a session**,
ne práce samotná.

---

## 1. Anatomie dlouhých zadání (≥ 300 znaků)

Kostra, která se opakuje (nejčistší instance: 2026-06-18 22:08, 2026-06-28 13:27, 2026-06-29 20:00):

```
[1] SPOUŠTĚČ / režim        →  "/spec", "/pruzkum", nebo věcná věta "Řízení vychystávacích portů přes PLC"
[2] CÍL                     →  "…abys mohl doplnit @docs/plc/AlzaSk-PLC-specifikace.md o řízení…"
[3] UKAZATELE NA ZDROJE     →  @docs/analysis/Seznam_prvku…xml, C:\Git\myfaber\…\initData.json  (2–4 zdroje)
[4] SCOPE-OUT (co NE)       →  "PICK_SHIPPING_NORTH ani mezaninové dopravníky nezmiňuj."
[5] IZOLACE / režim práce   →  "Pracuj v samostatné worktree .claude\worktrees\<jméno>!"   (jen u riskantních)
[6] KONTROLNÍ BOD           →  "Stručně popiš, jak zatím rozumíš tomu, jaký je postup…"  /  "Otázky?"
[7] FORMÁT VÝSTUPU          →  "Zhodnoť relevanci na škále 1 až 10", "číslovaný seznam", "artefakt s filtry"
```

**Vždycky tam je:** [2] cíl a [3] alespoň jeden ukazatel na zdroj.
**Často:** [4] scope-out, [7] formát.
**Jen u citlivých úloh:** [5] izolace, [6] kontrolní bod.
**Nikdy tam není:** role-play („jsi expert na…"), popis metodiky (ta je v `CLAUDE.md` / skillu),
opis obsahu zdrojů (jen cesta).

Doklad kostry (2026-06-18 22:08, zkráceno):
> „/spec Promysli, které informace musím upřesnit, abys mohl doplnit @docs/plc/AlzaSk-PLC-specifikace.md
> o řízení vychystávacích portů… Aktualizovaný popis prvků je v @docs/analysis/Seznam_prvku_ALZA_2026-06-18.xml…
> Porty by měly být vyjmenované v …initData.json „pick_south…". Stručně popiš, jak zatím rozumíš tomu, jaký je postup…"

**Klasifikace: PŘENOSITELNÉ.** Kostra nepotřebuje žádný plugin — potřebuje jen vědět, že
existuje. `[5]` je jediný bod závislý na nástroji (worktree), a ten je vestavěný.

---

## 2. PŘENOSITELNÉ KANDIDÁTY

### P1. Doptávací brána na konci zadání („Otázky?")
**Co to je:** Zadání se neuzavírá příkazem, ale výzvou k doptání. V H1 jednoslovně, v 06 rozvinuto.
**Doklad:** H1 2026-01-29 23:25: *„Jsou nějaká další obdobná místa? / Otázky?"* — 2026-06-18 19:19:
*„Důležité je, že předávám pole stanic. Zeptej se mě na otázky raději znovu. Odeslal jsem je předčasně."*
**Výskyty:** 7 explicitních výzev k doptání (3× H1, 4× 06).
**Klasifikace:** **PŘENOSITELNÉ.** Dvě slova na konci promptu, žádná infrastruktura.
**Okruh:** K (+ U)
**Předvedatelnost:** ★★★ — naživo: tentýž prompt bez „Otázky?" a s ním, srovnat, kolik
nevyřčených předpokladů Claude vytáhne na světlo.

### P2. Echo-back brána („stručně popiš, jak zatím rozumíš")
**Co to je:** Před psaním výstupu si vyžádám parafrázi zadání vlastními slovy. Odhalí špatně
pochopený doménový model dřív, než se propíše do 40 stran.
**Doklad:** 2026-06-18 22:08: *„Stručně popiš, jak zatím rozumíš tomu, jaký je postup pro ovládání
jednotlivých prvků na portech, který by mělo PLC provádět."*
**Výskyty:** 1× čistě, ale funkčně navazuje na P1 a P11 (rodina „nejdřív se ujisti").
**Klasifikace:** **PŘENOSITELNÉ.** Nejlevnější kvalitní praktika v celém korpusu.
**Okruh:** K, M
**Předvedatelnost:** ★★★ — ideální první cvičení workshopu.

### P3. Scope-out: explicitní výčet toho, co se NEMÁ řešit
**Co to je:** Vedle zadání stojí negativní hranice — jmenovitě vyjmenované prvky, o kterých
se nemá psát. Brání „užitečnému" rozšiřování rozsahu.
**Doklad:** 2026-06-19 15:30: *„…Stanice jsou zatím jen 4: PICK_SOUTH_0_… / PICK_SHIPPING_NORTH ani
mezaninové dopravníky nezmiňuj."* — 2026-06-18 22:13: *„V descriptions neuváděj, že se jedná o
vychystávací stanice, ale expediční."*
**Výskyty:** vzor, ≥ 6 (15:30, 15:35, 22:13, 21:07, 21:39, 23:51).
**Klasifikace:** **PŘENOSITELNÉ.**
**Okruh:** K
**Předvedatelnost:** ★★★ — ukázat výstup, který „přihodil" mezanin, vedle výstupu se scope-outem.

### P4. Negativní kontext: vyloučení konkrétního souboru z úvahy
**Co to je:** Silnější varianta P3 — zákaz čtení zdroje, aby výsledek nebyl kontaminován
předchozím vlastním výstupem (jinak agent „opíše" starý seznam místo nové derivace).
**Doklad:** 2026-06-29 21:07: *„Do kontextu vůbec nezahrnuj informace z @docs/meetings/2026-06-29_body-k-implementaci.md"*
— 21:39: *„/body-z-jednani 29. / Nevšímej si @…body-k-implementaci.md"* — 2026-06-19 23:51:
*„Pracuj izolovaně - nedívej se na ostatní worktrees."*
**Výskyty:** 3, a všechny tři vznikly jako reakce na kontaminaci → to je právě ten vzor.
**Klasifikace:** **PŘENOSITELNÉ.** Konceptuálně netriviální: kolegové nečekají, že *odebírání*
kontextu je nástroj kvality.
**Okruh:** K, M
**Předvedatelnost:** ★★★ — nejlepší „aha" moment: dvakrát tentýž prompt, jednou s vlastním
starým výstupem v repu, jednou s jeho vyloučením.

### P5. N-násobný běh téhož zadání a porovnání variance
**Co to je:** Stejná úloha se nechá zpracovat 3–4× izolovaně, a pak se porovnává, **kde se
výsledky rozešly a proč** — variance mezi běhy je diagnostika kvality zadání, ne šum.
**Doklad:** 2026-06-19 22:54: *„Nechal jsem Claude třikrát zpracovat úkol dle velice podobného zadání…
zjisti, ve kterých důležitých závěrech se výsledky rozcházejí a důvod… ve kterých chvílích agent
udělal rozhodnutí, kterým se výsledná řešení vzájemně rozešla."* + 2026-06-20 09:21 (čtvrtý běh).
**Výskyty:** 1 kampaň, ale rozprostřená přes 6 promptů (v2/v3/v4 + 2 srovnání) — nejde o náhodu.
**Klasifikace:** **PŘENOSITELNÉ** (worktree je vestavěný nástroj), byť nákladné na čas a tokeny.
**Okruh:** M, O
**Předvedatelnost:** ★★ — naživo drahé; ideální jako předpřipravená case study se třemi výstupy.

### P6. Meta-analýza vlastních běhů za účelem lepšího zadávání
**Co to je:** Cílem analýzy není opravit výstup, ale **naučit se lépe zadávat**. Explicitně
vyslovené v promptu.
**Doklad:** 2026-06-19 22:54: *„Zajímají mě ale především principy a to, jak se mohu poučit, jak lépe
agenty instruovat, aby buď vytvořili kvalitnější řešení, nebo se mě doptali na informace, které ke
kvalitnějším řešením povedou."* — 2026-06-29 21:11: *„Analyzuj poslední konverzaci „PLC porty
PICK_SOUTH", proč nebyly do výstupu přidány volné řádky za každý z bodů."* — 2026-06-29 21:21:
*„…analyzuj, proč, když jsem tento prompt spustil v samostatné session, tak vygeneroval jen 14 bodů.
Co nebylo pokryto a v čem byl faktický rozdíl a z jakého důvodu."*
**Výskyty:** 10 promptů s meta-analytickým záběrem (viz `analyza2_out.txt`).
**Klasifikace:** **PŘENOSITELNÉ.** Nepotřebuje nic než přístup k vlastní historii session.
**Okruh:** U (+ M)
**Předvedatelnost:** ★★★ — „debug promptu místo debugu výstupu". Nejsilnější didaktický moment
celého korpusu.

### P7. Útok na vlastní návrh („jaké to má slabé stránky, rizika?")
**Co to je:** Analytik navrhne řešení sám a Claude je použit jako oponent, ne jako autor.
**Doklad:** 2026-06-22 08:59: *„ad m06) Připadá mi jako nejlepší řešení, aby WMS volalo nejprve
containerRemoved a teprve pak… volal DELETE. Jaké to má slabé stránky, rizika?"* — 2026-06-22 09:11
(tentýž pattern, jiná varianta): *„…Jaké to má rizika?"* — 2026-06-22 15:12: *„Dává to takto smysl?"*
**Výskyty:** vzor, ≥ 4 v jedné rozhodovací sekvenci (08:59 → 09:11 → 15:12 → 15:35 „Ano, můžeš takto vyřešit").
**Klasifikace:** **PŘENOSITELNÉ.** Nejlepší obrana proti tomu, že Claude jen odsouhlasí, co řeknu.
**Okruh:** M, A
**Předvedatelnost:** ★★★ — vedle sebe „Navrhni řešení X" vs. „Chci X. Jaká má rizika?".

### P8. Rámovací A/B test (test pochlebování)
**Co to je:** Tentýž vstup se zadá dvakrát s opačným emocionálním rámováním — jednou jako
připomínky „kolegyně, kterou nemám příliš v oblibě", jednou „kolegyně, kterou mám v oblibě" —
a zjišťuje se, jestli se hodnocení relevance (škála 1–10) posune.
**Doklad:** 2026-06-19 20:40 a 20:41, tentýž text, jediný rozdíl je rámování:
*„/spec Kolegyně, kterou nemám příliš v oblibě, mi poslala připomínky k diagramu @docs/api/…
Zhodnoť jejich relevanci na škále 1 až 10…"*
**Výskyty:** 1 experiment (2 běhy), ale metodicky nejzajímavější prompt v korpusu.
**Klasifikace:** **PŘENOSITELNÉ.** Nulová infrastruktura, univerzální poučení: **nedávej do
zadání informace, které nemají mít vliv na výsledek** (autor, emoce, „šéf to chce").
**Okruh:** X (+ M)
**Předvedatelnost:** ★★★ — naživo, dva terminály. Nejlepší „stand-up" moment workshopu.

### P9. Číslovaný picklist jako předávka mezi jednáním a implementací
**Co to je:** Dvoufázový postup: (1) z přepisu jednání vygenerovat **číslovaný** seznam bodů,
(2) ve druhém promptu vybrat čísla a k vybraným dopsat rozhodnutí/doplňující fakta.
Čísla jsou adresou — zadávání je pak krátké a přesné.
**Doklad:** 2026-06-29 21:41: *„Implementuj tyto body: / 1, 3, / 4) jedná se o porty PLC511-PLC5xx /
5) …UDT pro řízení portu bude muset mít konfigurační parametr, zda čidlo je instalováno /
8) ověř, že již je zahrnuto. / 9+10) zahrň do TODO / 13) Nevím, kdy je potřeba…"*
**Výskyty:** vzor. Stejná mechanika s jinou sadou ID: „oprav M01, M08, M09" (06-20 12:25),
„ad M07) OK a přidej i do diagramů" (06-27 18:36), „Implementuj M08" (06-27 19:35),
„A4b) …", „A4c) Proč je to jako dotaz?" (06-28 14:40–14:41), „5) Ano, navrhni kontrolu" (06-19 11:02).
Celkem ≥ 10 promptů adresovaných přes stabilní ID.
**Klasifikace:** **PŘENOSITELNÉ.** Nezávisí na ničem — jen na tom, že si první výstup nechám očíslovat.
**Okruh:** A, O
**Předvedatelnost:** ★★★ — nejpraktičtější věc, kterou si kolega odnese do zítřejší práce.

### P10. Odpověď „nevím" jako legitimní vstup
**Co to je:** V picklistu se u bodu explicitně přizná neznalost, místo aby se vymyslel obsah.
**Doklad:** 2026-06-29 21:41: *„13) Nevím, kdy je potřeba z procesního důvodu pamatovat si polohu
vrat po výpadku napájení."* — 2026-06-25 13:53: *„Nejsem si jistý u B8, zda vždy má platit."*
**Výskyty:** 2 jasné (+ vzor „zahrň do TODO" u 9+10).
**Klasifikace:** **PŘENOSITELNÉ.** Klíčové proti tomu, aby Claude domýšlel doménová fakta.
**Okruh:** K, M
**Předvedatelnost:** ★★ — ukázat, co Claude vyrobí, když analytik místo „nevím" napíše dohad.

### P11. Ověření vlastního pochopení kvízem od Claude
**Co to je:** Po vysvětlení doménového tématu si analytik vyžádá kontrolní otázky a odpoví na ně —
obrácený review, kde je testovaný člověk.
**Doklad:** 2026-06-19 21:06: *„Polož mi nyní otázky, na kterých si ověříš, že jsem tématům dobře
porozuměl. Preferuji možnost krátkých jednoduchých odpovědí."* → 21:18 odpovědi včetně zdůvodnění
(*„Otázka 5 ne, protože tím by se vytvořilo místo s nižší ochranou, než jak je ve skladu požadována."*)
**Výskyty:** 1, ale patří do rodiny s P12 (učení domény).
**Klasifikace:** **PŘENOSITELNÉ.**
**Okruh:** U
**Předvedatelnost:** ★★★ — naživo na téma z workshopu samotného.

### P12. Učení domény mimo úkol („jen pro mou informaci")
**Co to je:** Analytik si nechá vysvětlit cizí terminologii (bezpečnostní normy, muting, SIL) —
oddělený, krátký dotaz, ne přílepek k pracovnímu promptu.
**Doklad:** 2026-06-19 15:36: *„Jen pro mou informaci mi vysvětli, co znamenají u světelné clony tyto
pojmy: SF 25, PLr d / kat. 3"* — 2026-06-19 21:04: *„Vysvětli muting. Jak to souvisí se SIL?"*
— 2026-06-11 20:52: *„Významu těch 3 odrážek vlastně nerozumím. Vysvětli mi to podrobněji."*
**Výskyty:** ≥ 4.
**Klasifikace:** **PŘENOSITELNÉ.** A zvlášť cenné pro analytiky vstupující do cizí domény.
**Okruh:** U
**Předvedatelnost:** ★★ — snadné, ale málo překvapivé.

### P13. Vyžádání variant + reprodukovatelnost jako kritérium výběru
**Co to je:** Místo „udělej to" se vyžádají varianty řešení, a rozhodovacím kritériem je
**stabilita výsledku při opakovaném spuštění**.
**Doklad:** 2026-06-29 21:47: *„Zároveň chci body rozdělit do vhodných logických celků/kapitol.
Jaké jsou varianty řešení?"* → 21:51 upřesnění: *„Jedná se mi o varianty toho, podle jaké logiky zvolit
kapitoly, jak volit granularitu kapitol, aby při opětovném spuštění byly výsledky podobné."*
→ 21:56: *„Použij #2 na obou pákách."*
**Výskyty:** 1 sekvence, ale metodicky výjimečná — determinismus jako design kritérium.
**Klasifikace:** **PŘENOSITELNÉ.**
**Okruh:** A, M
**Předvedatelnost:** ★★★ — spustit tentýž prompt 2× před a po zavedení pravidla granularity.

### P14. Propsání změny do všech souvisejících artefaktů jedním pokynem
**Co to je:** Součástí zadání je „ripple" — najdi a uprav všechna související místa, včetně
diagramů a odvozených dokumentů. Nejstarší doložený vzor, přítomný už v H1.
**Doklad:** H1 2026-01-29 23:25: *„Uprav všechna související místa, včetně webhooků. Odstraň
nepotřebná schémata. Inkrementuj verzi a popiš všechny změny."* — H1 23:52: *„Promítni změny také
v diagramech c:\Git\alzask\API\Diagrams-API-AlzaSk.md"* — 2026-06-18 21:12: *„Promítni také do
@docs/api/Diagrams-API-AlzaSk.md a @docs/api/Diagrams-API-AlzaSk-v2.md pokud je potřeba."*
**Výskyty:** 9 (viz `analyza2_out.txt`, „propsani do souvisejicich").
**Klasifikace:** **PŘENOSITELNÉ.** Pozor — má i temnou stranu (viz X4: bez brány se ripple časem přestane dělat).
**Okruh:** A
**Předvedatelnost:** ★★★ — změna v API YAML, ukázat, co se rozbije bez ripple pokynu.

### P15. Zobecnění pravidla před jeho zafixováním
**Co to je:** Když se objeví korekce, analytik nejdřív zkoumá, jestli není projevem obecnějšího
pravidla — a explicitně se ptá na cenu zobecnění.
**Doklad:** 2026-06-18 11:46: *„Myslím, že to je více obecný problém, ne jen zaměření pouze na
bezpečnost. Jedná se o chování na jakýkoliv problém. Dá se to takto pojmout a přitom zachovat
relevantní kontext?"* → 11:56 *„ano, založ rule"* → 12:06 *„Ano, převeď na shared"*.
**Výskyty:** 1 čistě, ale je to hrdlo celé znalostní smyčky.
**Klasifikace:** **PŘENOSITELNÉ** jako myšlenkový krok. Cílový mechanismus (`shared` pravidla) je **[infra]**.
**Okruh:** M, R
**Předvedatelnost:** ★★ — ukázat rozdíl mezi pravidlem přeučeným na jednu situaci a zobecněným.

### P16. Kontrola kontextového rozpočtu jako součást zadání
**Co to je:** Spotřeba kontextu je řízená veličina — hlídá se (`/context` 13×), čistí (`/compact` 5×)
a **vyslovuje se jako požadavek na řešení**.
**Doklad:** 2026-06-29 21:03: *„Zpracování chci provést tak, aby v aktuální session zpracování zabralo
co nejméně kontextového okna."*
**Výskyty:** 13× `/context`, 5× `/compact`, 1 explicitní požadavek v promptu.
**Klasifikace:** **PŘENOSITELNÉ.** Kolegové o kontextovém okně typicky vůbec neuvažují.
**Okruh:** N (+ O)
**Předvedatelnost:** ★★★ — `/context` naživo před a po nabrání velkého XLSX/PDF.

### P17. Pojmenování session (`/rename`) jako podmínka pozdější meta-analýzy
**Co to je:** Každá session dostane věcný název. Bez toho by nešly pozdější prompty typu
„Analyzuj poslední konverzaci „PLC porty PICK_SOUTH"" ani `/resume` do správného vlákna.
**Doklad:** 12× `/rename` (např. 2026-06-19 21:56 *„/rename Připomínky neoblíbené v2"*,
2026-06-20 11:18 *„/rename Průzkum journal - zpětná vazba"*), navazuje 2026-06-29 21:11
*„Analyzuj poslední konverzaci „PLC porty PICK_SOUTH""*.
**Výskyty:** 12, zjevný vzor.
**Klasifikace:** **PŘENOSITELNÉ** — ale jen pokud se vysvětlí *proč* (jinak to je kosmetika).
Hodnotu má výhradně v kombinaci s P6.
**Okruh:** N, U
**Předvedatelnost:** ★★ — ukázat `/resume` seznam s názvy vs. bez nich.

### P18. Přenesení nalezeného zlepšení na další projekt
**Co to je:** Když se osvědčí kontrola/pravidlo, hned se řeší, jak ho dostat do dalšího repozitáře.
**Doklad:** 2026-06-18 12:17: *„Analyzuj, jak tuto novou vlastnost implementovat také do projektu
C:\Git\fhb"* — 2026-06-19 11:14: *„Doplň kontrolu také do projektu C:\Git\fhb"* — 2026-06-20 11:56:
*„Musel bych to ale vytvořit napříč všemi mými projekty. Chtěl bych, aby se to všude chovalo obdobně.
Pokud budou výjimky, tak bych je uvedl explicitně."*
**Výskyty:** 3.
**Klasifikace:** **PŘENOSITELNÉ** jako návyk; realizace = **[infra]** (user-level vs. project-level).
**Okruh:** R, N
**Předvedatelnost:** ★★

### P19. Artifact jako pracovní nástroj pro jednání, ne jako prezentace
**Co to je:** Výstup analýzy se nedodá jako dokument, ale jako interaktivní stránka pro **použití
během jednání** (přepínání stavu bodu, vlastní komentáře, filtr kritických, export MD).
**Doklad:** 2026-06-28 13:53: *„Připrav jako přehledný claude artefact, který… umožňuje přepínat, zda
bod jednání je neřešený, byl již vyřešen, nebo je otevřený. Možnost zapsat jako text i vlastní
komentáře. Stránka bude mít tlačítko pro stažení markdown souboru s vyplněnými závěry."*
Následuje 5 iterací (14:12 reset, 14:23 filtr, 14:24 nezávislý filtr, 14:28 počítadlo respektující
filtry, 14:31 rozklikávací detaily) — tedy vývoj UI dialogem.
**Výskyty:** 1 kampaň, 6 promptů.
**Klasifikace:** **PŘENOSITELNÉ.**
**Okruh:** R
**Předvedatelnost:** ★★★ — nejefektnější demo pro netechnické publikum.

### P20. Analýza obrázků a PDF/XLSX jako plnohodnotný vstupní zdroj
**Co to je:** Vstupem analýzy jsou dodavatelská PDF, XLSX seznamy prvků a fotky/screenshoty
schémat; první krok je konverze do MD, aby byl zdroj citovatelný.
**Doklad:** 2026-06-11 20:56: *„Posouzení rizik: @"docs/analysis/940-SO-…Posouzení rizik_V1.0.pdf""*
→ 21:06: *„Převeď rovnou pdf do markdown souboru."* — 2026-06-30 11:55: *„Převeď dokument
@"docs/plc/sources/TMT…-2026-06-30.pdf" do markdown"* — 2026-06-11 14:25: *„[Image #8] Dokážeš přečíst
tento obrázek?"*
**Výskyty:** ≥ 5.
**Klasifikace:** **PŘENOSITELNÉ.** Poučení: **nejdřív konverze na citovatelný text, pak práce** —
jinak nelze doložit `soubor:řádek`.
**Okruh:** K
**Předvedatelnost:** ★★★ — hodit do terminálu dodavatelské PDF a nechat vyrobit MD.

---

## 3. MOMENTY VZNIKU (oblouk problém → improvizace → nástroj)

### V1. `/body-z-jednani` — od opakovaného ručního promptu ke slash příkazu
**Oblouk:** 06-28/06-29 se seznam bodů z jednání dělá ručně a nekonzistentně (14 vs. 20+ bodů
mezi běhy) → 06-29 20:00 zadání „nauč se to z mé vlastní historie" → 20:27 vznik příkazu →
20:32 první použití → 21:47–22:34 dolaďování logiky kapitol → 5× použití do konce měsíce.
**Doklad (klíčový prompt, 06-29 20:00, zkráceno):** *„Podívej se do historie mých sessions v těchto
projektech, jakým způsobem jsem to v minulosti dělal a které z přístupů se nejvíce osvědčily, a na
základě toho navrhni prompt, který toto bude umět automaticky udělat pro nové schůzky. Chci to
používat i jako slash command s parametrem datumu…"*
**Klasifikace:** **PŘENOSITELNÉ** — a je to nejlepší příběh v korpusu, protože obsahuje **generalizaci
z vlastní historie**, nikoli vymýšlení příkazu od nuly. Kolega může udělat totéž první den.
**Okruh:** R, U
**Předvedatelnost:** ★★★ — celý oblouk se dá odvyprávět a poslední krok předvést naživo.
**Poznámka:** dotažení mělo ještě dvě iterace kvůli formátu (20:39 a 20:41 „za jednotlivé body vkládej
volný řádek" — dvakrát totéž, protože příkaz to nezafixoval → viz X4).

### V2. `plc-lint` — od průzkumu k deterministické bráně
**Oblouk:** 06-23 14:31 `/pruzkum` „jaký linter na analytické dokumenty, ne kód" → 06-25 13:40
„prozkoumej možnosti validace PLC prvků a datových bloků" → 13:53 lidské rozhodnutí o pravidlech
(*„Nejsem si jistý u B8… B14: word / Napiš plc-lint pro třídy 1, 2 i 3."*) → 14:19 „Co nyní všechno
pokrývá validate.cmd?" → 14:22 *„Vytvoř validate.cmd, vytvoř README. Zkontroluj, že pravidlo je
správně vynucováno také v CLAUDE.md"*.
**Klasifikace:** **[infra]** jako artefakt, **PŘENOSITELNÉ** jako postup. Přenositelné jádro:
*opakovanou korekci převeď na spustitelnou kontrolu a tu zapiš do CLAUDE.md, aby se vynucovala.*
**Okruh:** M, R
**Předvedatelnost:** ★★★ — poslední prompt (14:22) je dokonalá ilustrace „brána + dokumentace + zapojení".

### V3. Pravidlo o čárkách v diagramech — zafixování korekce do pravidel
**Doklad:** 2026-06-20 16:36: *„Pokud v poznámkách v diagramech je text rozdělen do více řádků, tak
někdy mi na konci řádku chybí významově čárka… Zapamatuj si to do pravidel, které už k tomu máš."*
**Klasifikace:** **PŘENOSITELNÉ** jako reflex („nekoriguj potřetí, zapiš"). Mechanismus = **[infra]**.
**Okruh:** M
**Předvedatelnost:** ★★

### V4. Znalostní smyčka — od jedné korekce k `shared` pravidlu
**Doklad:** 2026-06-18 11:46 (zobecnění) → 11:51 *„Prozkoumej, zda by dávalo smysl upravit instrukce
pro agenty vytvářející spec, aby mě samého při zadání více vedli k dodržování těchto zásad"* →
11:56 „ano, založ rule" → 12:06 „Ano, převeď na shared" → 12:11 *„Vložím sám. Co přesně mám udělat?"*
**Zvlášť pozoruhodné:** prompt 11:51 žádá, aby nástroj **disciplinoval samotného zadavatele** —
tj. kvalita se neřeší lepším promptem, ale tím, že se agenti naučí vymáhat lepší zadání.
**Klasifikace:** **PŘENOSITELNÉ** jako myšlenka, **[infra]** jako realizace (plugin knowledge-loop, CODEOWNERS).
**Okruh:** M, R
**Předvedatelnost:** ★★ — jen jako vyprávěný princip; postavení mechanismu je týmová práce.

### V5. Notion evidence backlogu → osobní skill
**Doklad:** 06-11 13:13 → 06-12 23:19 *„/superpowers:writing-skills Je vhodné vytvořit si skill na
zakládání úkolů a backlog záznamů?"* → 23:35 *„Kde jsou ty reference* soubory uložené? Tyto úkoly
a backlog totiž chci používat jen já (nikdo jiný z týmu) na všech mých projektech."*
**Klasifikace:** **OSOBNÍ ZVYK** obsahově, ale **PŘENOSITELNÉ** je rozhodovací kritérium z 23:35:
*„používám jen já, napříč projekty" → user-level skill; „používá tým, jeden projekt" → project-level.*
Tuhle jednu větu do workshopu vzít, zbytek (Notion schémata) ne.
**Okruh:** N, R
**Předvedatelnost:** ★ — jen jako pravidlo, ne demo.

---

## 4. ANTIPATTERNY (okruh X)

### X1. Vágní izolační pokyn = ztráta dat ★ nejsilnější
**Co Claude udělal špatně:** Na pokyn „Pracuj v samostatné worktree!" (bez jména) použil **existující**
worktree s rozpracovanou prací uživatele a přepsal/smazal soubory.
**Jak jsem to formuloval:** 2026-06-19 22:08: *„Začal jsi pracovat v existujícím worktree, kde jsem měl
rozpracovanou práci. Měl sis založit nové worktree. Můžeš obnovit soubory, které jsi mi vymazal?"*
→ 22:17 *„Chci obnovit přece soubory v pripominky-diagram-v2"*.
**Náprava v dalších promptech (a to je poučení):** 22:04 pokyn dostal jméno —
*„Pracuj v samostatné worktree .claude\worktrees\pripominky-diagram-v3!"*; 23:51 se přidalo
*„Pracuj izolovaně - nedívej se na ostatní worktrees."*
**Výskyty:** 1 incident, ale 19 promptů o worktree = expozice byla vysoká.
**Poučení:** **Imperativ bez jednoznačného cíle je nedeterministický.** „Samostatné" není adresa.
**Okruh:** X, O
**Předvedatelnost:** ★★★ — bezpečně nasimulovat na testovacím repu. Nejzapamatovatelnější
moment celého workshopu.

### X2. Zákaz vyslovený až po škodě (chybějící pravidlo v CLAUDE.md)
**Co Claude udělal špatně:** commitoval, aniž byl o to požádán.
**Jak jsem to formuloval:** 2026-06-20 14:46: *„v2 a v3 můžeš v worktrees také smazat. Já jsem ale
nechtěl dělat commit. **Tady v tomto projektu nikdy nedělej commity**"* (předtím už 06-20 12:21
*„commit jsem vrátil, budu commitovat později"*, a 06-19 10:45 *„Chci variantu bez commitu"*).
**Výskyty:** 3 kolize, než pravidlo vzniklo.
**Poučení:** Destruktivní/nevratné operace patří do `CLAUDE.md` **před** prvním úkolem, nikoli po
třetí kolizi. Do workshopu jako checklist „co si zakázat první den".
**Okruh:** X, N
**Předvedatelnost:** ★★★ — ukázat minimální projektový `CLAUDE.md` se zákazy.

### X3. Ztráta orientace v git modelu (worktree bez mentálního modelu)
**Co Claude udělal špatně:** nic — udělal, co se řeklo. Uživatel jen nevěděl, kde výsledek je.
**Jak jsem to formuloval:** 2026-06-19 09:02: *„NErozumím tomu, co se teď stalo, protože ve Visual
Studio code nyní nevidím žádné změny v mé hlavní větvi dev/martint. Vysvětli mi, kde jsou všechny
provedené změny a jak si je mohu zkontrolovat. Nevidím totiž ani commit v GitLab."*
Následně 09:17 „Přenes změny na dev/martint", 09:28 „Jak se dělá pořádek ve worktrees?",
10:37 znovu totéž, 10:45 „Chci variantu bez commitu", 06-29 09:14 *„V konverzaci je zmínka o
spec/2026-06-18_vychystavaci-porty-plc/. V repu ji ale nevidím. Co se s ní stalo, byla vymazána?"*
**Výskyty:** ≥ 6 promptů řešících „kde jsou moje změny".
**Poučení:** **Nezaváděj izolační mechanismus dřív, než víš, jak z něj výsledek dostaneš zpět.**
Pro workshop: worktree ukázat, ale s hotovým „handoff" postupem, ne jako hračku.
**Okruh:** X, O, N
**Předvedatelnost:** ★★★ — právě proto, že to je autentická cesta začátečníka.

### X4. Korekce donekonečna místo brány ★ pedagogické jádro
**Co Claude udělal špatně:** pořadí záznamů v changelogu (opakovaně), chybějící changelog v TC,
chybějící volné řádky mezi body.
**Jak jsem to formuloval:** 2026-06-19 10:50: *„V souboru …FR-COMP-API-CONTAINER-001… není správně
pořadí změn v changelogu. **Jak je to možné? Řešili jsme to už mnohokrát…**"* — 10:51: *„Naopak v TC …
chybí záznam v chynges úplně."* — 06-29 20:39 *„Za jednotlivé body vkládej volný řádek"* a znovu
06-29 20:41 *„Za jednotliví body vlož vždy nový řádek."* (tentýž požadavek dvakrát v odstupu 2 minut).
**Výskyty:** vzor — nejméně 3 nezávislé případy „už jsme to řešili".
**Poučení:** Opakovaná korekce v chatu je **měřitelná ztráta**. Pravidlo, které nemá bránu
(linter / validate.cmd / hook), se bude porušovat. Tento antipattern je přesně to, co V2 a V3 řeší
— proto se dají spárovat do jednoho bloku workshopu „od korekce k bráně".
**Okruh:** X → M
**Předvedatelnost:** ★★★ — dvě obrazovky: korekce v chatu vs. `validate.cmd` s exit kódem.

### X5. Odesílání nedokončeného promptu a jeho oprava dalším promptem
**Doklad:** 2026-06-18 19:19: *„Důležité je, že předávám pole stanic. **Zeptej se mě na otázky raději
znovu. Odeslal jsem je předčasně.**"* — 2026-06-30 11:54 *„Převeď dokument"* → 11:55 tentýž prompt
s cestou k souboru — 2026-06-11 21:24 *„Sjednoť terminologii…"* → hned znovu *„Pokračuj. Sjednoť
terminologii…"* — 2026-06-19 15:30 (odeslán s nedopsaným výčtem stanic) → 15:35 celá věta znovu.
**Výskyty:** ≥ 4 (+ 3 identické odeslání téhož promptu v H1, viz X6).
**Poučení:** Nedokončené zadání stojí jeden celý běh agenta. Levné opatření: dopsat prompt v editoru,
ne v terminálu. (Pozn.: v 15:30/15:35 to *není* jen překlep — druhá verze je věcně bohatší, tj. sepsáním
promptu se dozadání skutečně vyjasnilo. To je hraniční případ mezi antipatternem a legitimní iterací.)
**Okruh:** X
**Předvedatelnost:** ★★

### X6. Trojí odeslání téhož dlouhého promptu bez diagnózy
**Doklad:** H1 2026-01-29 — identický 700znakový prompt („Uprav API-myFABER-WES-AlzaSk.yml… Chci
zjednodušit API…") odeslán ve 23:25, 23:52 a 23:52, **znak za znakem stejný**.
**Výskyty:** 3 z 14 promptů celého H1 (21 % rané aktivity!).
**Poučení:** Typický start začátečníka: když se nic „nestane", pošlu to znovu. Do workshopu jako
sekce „co dělat, když se zdá, že se nic nestalo" (`/context`, `/resume`, čtení výstupu).
**Okruh:** X, N
**Předvedatelnost:** ★★★ — autentický artefakt vlastního začátku; publikum se v něm najde.

### X7. Rámující informace, která nemá mít vliv
**Doklad:** viz P8 — do zadání vstupuje „kolegyně, kterou nemám příliš v oblibě".
**Poučení jako antipattern:** i když to byl vědomý experiment, běžně se to děje nevědomě —
„tohle chce šéf", „od kolegy, který se v tom nevyzná". **Takové věty se ze zadání mají škrtat.**
**Okruh:** X
**Předvedatelnost:** ★★★ (viz P8)

### X8. Diktovaný prompt bez korektury
**Doklad:** 2026-06-22 09:11 (1004 znaků, doslovně): *„…Nebo **ok senátor** zjistí že nemůže nosič
vložit zpátky do systému…"* (= „operátor"); *„Takže vím mám to zatím jako výjimku"*.
Podobně 2026-06-19 21:18 a 2026-06-29 20:00 (bez interpunkce, „V závěru" místo „závěrů").
**Výskyty:** ≥ 3 dlouhé diktované prompty.
**Poučení — a je vyvážené:** Claude s tím pracoval bez problému, věcný obsah převážil formu.
**Ale** v doménovém textu s pojmy jako „nosič", „port", „intransit" je zkomolený termín riziko —
zvlášť když se z promptu stane citovaný zdroj rozhodnutí. Doporučení: diktovat ano, ale
přečíst si to a opravit **doménové pojmy** (ostatní překlepy jsou neškodné).
**Okruh:** X (mírný) / U
**Předvedatelnost:** ★★ — ukázat, že „hezký prompt" není podmínka; podmínka je správný termín.

### X9. Slepé „pokračuj"
**Doklad:** 7× samotné *„pokračuj"* (06-18 19:05, 06-19 20:57, 06-19 22:22, 06-20 09:23, 09:24, …).
**Poučení:** Není to chyba, ale je to **vzdaný kontrolní bod** — místo, kde mohla přijít korekce
kurzu, se propálí bez revize. Zvlášť u dlouhých spec běhů.
**Okruh:** X (mírný), O
**Předvedatelnost:** ★ — jen jako doporučení „místo „pokračuj" napiš, co má být dál jinak".

### X10. Velké vstupy vlepené do promptu místo do repozitáře
**Doklad:** 2026-06-28 13:27 — jeden prompt nese `[Pasted text #1 +237 lines]`, `[Pasted text #2 +54 lines]`,
`[Image #3] [Image #4]`, `[Pasted text #5 +91 lines]` plus odkaz na XLSX.
**Poučení:** Funguje, ale výsledek je **nereprodukovatelný a necitovatelný** — vstup (e-maily) není
v repu, takže tvrzení ve výstupu nelze doložit `soubor:řádek`. Správně: uložit zdroj, pak odkázat.
(Pozdější praxe to potvrzuje — vznikl registr `docs/suppliers/` s doslovnými přepisy e-mailů.)
**Okruh:** X → K
**Předvedatelnost:** ★★

---

## 5. OSOBNÍ ZVYKY A [INFRA] (pro workshop nepoužívat, nebo jen jako „až budete mít")

| Kandidát | Doklad | Proč nepřenositelné |
|---|---|---|
| `/spec` (13×) — orchestrovaná spec pipeline | 06-18 14:34 *„/spec dle bodu 1 rozšiř API."* | **[infra]** — plugin spec-factory, 8 agentů, `spec-config.yaml`, grounding pack. Kolega bez toho nemá nic. Do workshopu jen jako cíl („co se dá postavit"), ne jako praktika. |
| `/pruzkum` (2×) | 06-23 14:31 | **[infra]** — vlastní skill v6.6. |
| `/body-z-jednani` (5×) | 06-29 20:32 | **[infra]** jako artefakt — ale oblouk vzniku (V1) je přenositelný. |
| `validate.cmd`, `plc-lint.py`, FR/TC validátor | 06-19 11:20 *„@fhb Spusť python validaci FR a TC."* | **[infra]** — postavit pro tým. |
| Notion backlog / úkoly | 06-12 14:12, 14:20 | **OSOBNÍ ZVYK** — mimo téma workshopu. |
| Freelo / webhooky / credentials | 06-12 14:22, 14:32 | **OSOBNÍ ZVYK** + provozní. |
| `/statusline`, `/terminal-setup`, `/doctor`, `/login`, barva terminálu | H1 2026-02-10 22:57, 06-20 11:32 | **OSOBNÍ ZVYK**, ladění prostředí. Do okruhu N max. jednou větou. |
| ACE/Reflector průzkum (noční automatické zlepšování agentů) | 06-20 11:56 | **OSOBNÍ ZVYK / vize** — nebylo dotaženo v tomto období; pro kolegy předčasné. |
| `/resume <uuid>`, `/compact` timing | 06-18 11:43 | Hraniční — mechanika ano (okruh N), konkrétní zvyklosti ne. |

---

## 6. VÝVOJ H1 → 06 (co se konkrétně zlepšilo)

**H1 (2026-01 – 2026-05, 14 promptů) — co už tam bylo dobré:**
- Ripple pokyn („Uprav všechna související místa, včetně webhooků") — P14.
- Doptávací brána („Otázky?") a hledání analogií („Jsou nějaká další obdobná místa?") — P1.
- Verzování a popis změn jako součást zadání („Inkrementuj verzi a popiš všechny změny.").

**H1 — co chybělo:**
- Žádné ukazatele na více zdrojů (jen `@` na cílový soubor).
- Žádný scope-out, žádný negativní kontext.
- Žádná izolace, žádná brána, žádná meta-analýza.
- Trojí odeslání téhož promptu (X6) — chybějící model toho, co se v nástroji děje.
- Struktura promptu: čistý imperativ + odstavce oddělené prázdnými řádky, bez formátu výstupu.

**06 — nově přidané prvky (v pořadí, v jakém se objevily):**
1. **Grounding na více autoritativních zdrojů naráz** (06-18 22:08) + scope-out.
2. **Echo-back brána** před psaním (06-18 22:08).
3. **Izolace do worktree** (06-18 22:34) — a hned i její cena (X1, X3).
4. **Útok na vlastní návrh** (06-22 08:59) místo „navrhni řešení".
5. **N-násobný běh + porovnání variance** (06-19 22:54).
6. **Meta-analýza vlastních běhů pro zlepšení zadávání** (06-19 22:54, 06-29 21:11/21:21).
7. **Rámovací A/B test** (06-19 20:40 vs. 20:41).
8. **Zafixování opakované korekce do pravidla / brány** (06-18 11:56, 06-20 16:36, 06-25 14:22).
9. **Negativní kontext — vyloučení zdroje** (06-29 21:07).
10. **Reprodukovatelnost jako rozhodovací kritérium** (06-29 21:51).
11. **Řízení kontextového rozpočtu** (06-29 21:03; `/context` 13×).
12. **Číslovaný picklist + adresování přes stabilní ID** (06-20 12:25, 06-29 21:41).

**Nejpodstatnější posun není délka ani „lepší formulace".** Prompty jsou v 06 spíš *kratší*
(medián pod 100 znaků). Posun je v tom, že se **zadávání přesunulo z jednoho promptu do
sestavy: kontext (CLAUDE.md, skill) + ukazatele na zdroje + brána (linter) + krátký prompt.**
To je hlavní teze pro workshop — a zároveň vysvětlení, proč kolegům samotná znalost promptování
nepomůže.

**Druhý posun, méně vidět:** v H1 se Claude používá jako **editor** („uprav soubor"). V 06 se
používá jako **oponent** (P7), **experimentální zařízení** (P5, P8) a **učitel domény** (P11, P12).
Tenhle přechod od „udělej to za mě" k „ověř mě / rozbij mi to" je nejlepší jednověté poselství
celého úseku.

---

## 7. Doporučené složení workshopu z tohoto materiálu

| Okruh | Nosné kandidáty | Poznámka |
|---|---|---|
| **K** kontext a grounding | P1, P2, P3, P4, P10, P20, kostra z §1 | Jádro prvního bloku. |
| **M** mechanika kvality | P7, P13, P15, X4 → V2, V3 | Spárovat antipattern s bránou. |
| **A** analytické postupy | P9, P14, P13 | P9 je nejpraktičtější „odnesu si to hned". |
| **U** učení | P6, P11, P12, V1 | P6 = „debuguj prompt, ne výstup". |
| **O** orchestrace | P5, X1, X3, X9 | Worktree ukázat **až** s handoff postupem. |
| **R** rozšíření | P19, V1, V2, P18 | V1 jako hlavní příběh (vzniklo z vlastní historie). |
| **X** antipatterny | X1, X4, X6, X7, X2 | X1 a X4 jsou nejsilnější; X6 je autentický „začátek". |
| **N** nastavení | P16, P17, X2 | Minimalisticky; zbytek je osobní ladění. |

**Tři nejsilnější položky celkem:** X1 (vágní pokyn = smazaná práce), P6 (meta-analýza vlastních
běhů), P8/X7 (rámovací A/B test pochlebování).
