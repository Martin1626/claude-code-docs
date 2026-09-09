# DRAFT katalogu námětů — vstup pro red-team

Sestaveno v hlavní session z 12 agentních výstupů (~267 kandidátů) deduplikací.
**Toto je draft, ne finál.** Red-team ho má rozbít.

## Metoda deduplikace

Prioritu dostaly **konvergence** — věci, které našlo víc agentů nezávisle na sobě
z jiných dat. Konvergence je nejsilnější signál, že nejde o můj osobní zvyk.

| Konvergující nález | Kdo to našel nezávisle | Počet |
|---|---|---|
| Dlouhé zadání patří do souboru, ne do chatu | 2c (P16, X02), 2e (P10), 2b (nepřímo) | 3 |
| Číslovaný picklist + odpověď čísly | 2a (P9), 2b (M4), 2c (P02), 2e (P6) | 4 |
| Read-only brána „nic neměň, jen vypiš" | 2b (M1, M2), 2c (P01), 2e (P4) | 3 |
| Brána místo instrukce v promptu | 3a (1), 3b (1), 3c (5), 2b (M7), 2a (X4) | 5 |
| Meta-analýza vlastních běhů kvůli lepšímu zadávání | 2a (P6), 2b (U1, U2, U5), 2c (P33) | 3 |
| Negativní kontext — co NEčíst / co neřešit | 2a (P3, P4), 2c (P07) | 2 |
| Triáž nálezů dělá člověk, ne model | 2c (P19), 3b (13), 3c (7) | 3 |
| Vágní pokyn bez jednoznačného cíle = škoda | 2a (X1), 2b (X1) | 2 |
| Volba modelu podle povahy podúlohy | 2b (O3, N2), 2c (P21), 3a (14) | 3 |
| Grounding: citace se ověřuje, nevěří | 2b (K1, K2), 2c (P09, P10), 3a (3), 3b (9) | 4 |
| Stabilní ID se nepřečísluje | 3a (8) | 1 (ale silný doklad) |
| Konvence bez validátoru se rozpadne | 3a (10), 3c (11), 2d (X9) | 3 |

## Souhrnná tabulka draftu

| ID | Okruh | Název | Role | Min | Prio | Blok | dep |
|---|---|---|---|---|---|---|---|
| F-01 | F | Claude si tě nepamatuje, vede si o tobě složku | výklad+demo | 15 | must | 1 | — |
| F-02 | F | Čeština není dražší, protože je delší | výklad+demo | 12 | must | 1 | F-01 |
| F-03 | F | Kompaktace ti session zachrání, a ty nevíš, co vypadlo | výklad+demo | 18 | must | 1 | F-01 |
| F-04 | F | Padesát jedna ku jedné (`/compact` vs `/clear`) | příběh+demo | 10 | must | 1 | F-03 |
| F-05 | F | Co tě stojí místo, o kterém nevíš | výklad+demo | 15 | should | 1 | F-01 |
| N-01 | N | Nastavení nasazuj na diagnózu, ne na dojem | demo | 12 | should | 2 | F-05 |
| N-02 | N | Tři zákazy, které si nastav dřív než cokoli jiného | demo | 8 | must | 2 | — |
| N-03 | N | Output style: jak si nastavit, jak s tebou Claude mluví | demo | 10 | could | 2 | — |
| N-04 | N | `/insights` — inventura vlastní praxe jedním příkazem | demo | 8 | should | 2 | — |
| K-01 | K | Dokument nese kontext, prompt nese rozhodnutí | výklad+demo | 20 | must | 2 | — |
| K-02 | K | Bezcílný imperativ: 11× tentýž prompt, jednou bez cesty | příběh+cvičení | 12 | must | 2 | — |
| K-03 | K | Co NEčíst, a proč | výklad+cvičení | 12 | must | 2 | K-01 |
| K-04 | K | Citace se ověřuje, nevěří | demo | 15 | should | 3 | K-01 |
| K-05 | K | Ticho je nález, ne absence nálezu | výklad | 10 | must | 3 | K-03 |
| K-06 | K | Hierarchie autority zdrojů rozhoduje spor | výklad | 12 | should | 3 | — |
| K-07 | K | Vrstva zdroje: souhrn není transkript | výklad | 10 | should | 3 | K-04 |
| K-08 | K | `CLAUDE.md` driftuje od skutečnosti | příběh | 10 | must | 2 | — |
| R-01 | R | Prompt do souboru, session ho jen provede | demo+cvičení | 15 | must | 2 | K-01 |
| R-02 | R | Metodika bez spouštěče je jen text | příběh+demo | 12 | should | 4 | R-01 |
| R-03 | R | Uložený postup místo opakovaného promptu | demo | 12 | should | 4 | R-02 |
| R-04 | R | Dvě vrstvy dokumentace podle čtenáře | výklad | 10 | should | 4 | — |
| R-05 | R | Hook: kontrola, kterou nemusíš spouštět | demo | 12 | could | 4 | — |
| R-06 | R | Skill nemá nést znalost, ale navigaci ke znalosti | výklad | 10 | could | 4 | R-03 |
| M-01 | M | Brána, ne prompt | výklad+demo | 18 | must | 3 | — |
| M-02 | M | Read-only brána: „napiš do chatu, nic neměň" | demo+cvičení | 10 | must | 1 | — |
| M-03 | M | Dva exit kódy = dva různé signály | demo | 10 | should | 3 | M-01 |
| M-04 | M | Vykazuj, kolik jsi toho NEzkontroloval | demo | 12 | must | 3 | M-01 |
| M-05 | M | Triáž nálezů dělá člověk. Dva ze tří jsou falešné. | výklad+příběh | 15 | must | 3 | M-02 |
| M-06 | M | Slepý recenzent | demo | 10 | should | 3 | M-05 |
| M-07 | M | Deterministická vs. sémantická kontrola | výklad | 12 | must | 3 | M-01 |
| M-08 | M | Práh, který realita trvale překračuje, není signál | příběh+demo | 10 | should | 3 | M-03 |
| M-09 | M | Kontrolní součet jako past na utečenou číslici | demo | 8 | could | 3 | M-07 |
| M-10 | M | Opakovaná korekce se povyšuje na pravidlo | příběh | 10 | must | 5 | M-01 |
| O-01 | O | Subagent není o rychlosti, ale o tom, kam jde hluk | výklad+demo | 15 | must | 4 | F-05 |
| O-02 | O | Volba modelu podle povahy podúlohy | výklad+demo | 12 | should | 4 | O-01 |
| O-03 | O | Handoff: jak předat práci sobě zítra | demo | 12 | should | 4 | F-04 |
| O-04 | O | Jedna session = jedno téma, pojmenované | demo | 8 | should | 2 | — |
| O-05 | O | Vágní izolační pokyn smazal rozpracovanou práci | příběh | 10 | must | 4 | — |
| A-01 | A | Vrstvový audit dokumentace | výklad+cvičení | 25 | must | 5 | K-03, K-05 |
| A-02 | A | Číslovaný picklist a odpověď čísly | demo+cvičení | 15 | must | 2 | — |
| A-03 | A | Rozpočet na otázky a páka místo nejasnosti | výklad | 12 | must | 5 | A-01 |
| A-04 | A | Straw-man: napiš hypotézu, ať ji jen opraví | výklad+demo | 12 | must | 5 | — |
| A-05 | A | Sebekritika útokem na náklad na údržbu | výklad | 10 | must | 5 | — |
| A-06 | A | Eviduj, co v odpovědi CHYBÍ | demo | 12 | should | 5 | — |
| A-07 | A | Redukce na minimální případ po sérii selhání | příběh | 12 | must | 5 | — |
| A-08 | A | Specifikace invariantem místo symptomu | výklad | 12 | must | 5 | A-07 |
| A-09 | A | Adresát dokumentu jako parametr zadání | výklad | 10 | should | 5 | — |
| A-10 | A | Publikum určuje, co smí být odkaz | demo | 8 | should | 5 | A-09 |
| A-11 | A | Vyjednej terminologii dřív, než začneš psát | výklad | 10 | should | 5 | — |
| U-01 | U | Debuguj prompt, ne výstup | výklad+cvičení | 15 | must | 6 | — |
| U-02 | U | Znalostní smyčka, která se zasekla | příběh | 15 | must | 6 | M-10 |
| U-03 | U | Paměť vs. pravidlo: kdy co | výklad | 10 | should | 6 | U-02 |
| U-04 | U | Nech si vysvětlit laicky a pojmenuj, co nevíš | výklad | 10 | should | 6 | — |
| U-05 | U | Nástroj cestoval mezi projekty a vyrostl | příběh | 12 | should | 6 | — |
| X-01 | X | Tokeny v chatu | příběh | 8 | must | 1 | — |
| X-02 | X | Dlouhý prompt v chatu se tiše ořízne | příběh+demo | 10 | must | 2 | R-01 |
| X-03 | X | Autonomní smyčka revize → oprava → revize | příběh | 12 | must | 3 | M-05 |
| X-04 | X | Iluze pokrytí je horší než jeho absence | příběh | 10 | must | 3 | — |
| X-05 | X | Ladění screenshoty místo invariantu: 30 promptů | příběh | 12 | must | 5 | A-08 |
| X-06 | X | Hotový artefakt, na který nic neukazuje, je mrtvý | příběh+demo | 10 | must | 4 | R-02 |
| X-07 | X | Konvence bez validátoru se rozpadne | demo | 10 | must | 3 | M-01 |
| X-08 | X | Vrstva pravidel, která neexistuje | příběh | 10 | should | 6 | K-08 |
| X-09 | X | Slepé „pokračuj" | výklad | 5 | could | 2 | — |
| X-10 | X | Regenerace přepíše ruční editaci člověka | příběh | 8 | should | 3 | — |
| X-11 | X | Nástroj kontroluje jen to, co pozná | příběh+demo | 10 | should | 3 | M-07 |
| X-12 | X | Ladění modelu bez srovnávací základny | příběh | 10 | should | 4 | O-02 |

**Počet: 66 námětů.** F 5 · N 4 · K 8 · R 6 · M 10 · O 5 · A 11 · U 5 · X 12

## Klíčové doklady, na které se draft opírá

| Doklad | Hodnota | Zdroj |
|---|---|---|
| Kompaktací zaznamenaných | 21, všech 21 ručních | `doklady-kompaktace.md` |
| Medián zahozeného kontextu | 97,3 % (464 352 → 13 344 tok.) | tamtéž |
| Medián doby kompaktace | 180,7 s | tamtéž |
| Celkem zahozeno | 8 601 191 tokenů | tamtéž |
| `/compact` vs. `/clear` (pracovní projekty) | 51× vs. 1× | `doklady-statistiky.md` |
| Medián délky promptu | 65 znaků (pracovní), 75 (celá historie) | tamtéž |
| Promptů nad 1000 znaků | 31 z 1507 (2,1 %) | tamtéž |
| `CLAUDE.md` alzask | 23 427 znaků ≈ 7 800 tok. (4× ilustrativní příklad z docs) | `doklady-cena-kontextu.md` |
| Kontext před prvním slovem | ≈ 13 000 tokenů | tamtéž |
| Hooky: použité eventy | 2 z ~8 | `faze1-korekce-hooky.md` |
| Inbox: povýšeno na pravidlo | 5 z ~63, všech 5 v prvních 6 dnech | `faze3c-pravidla-inbox.md` |
| Bezcílný imperativ | 11 doložených dvojic promptů | `faze2b-prompty-alzask-07.md` |
| „nic neměň, jen vypiš" | 14 výskytů | tamtéž |
| Tokeny vlepené do chatu | 4 tokeny / 5 promptů / 45 minut, 3 zneplatněny | `faze2e-prompty-shared.md` |
| Poškozený dlouhý prompt | 3052 znaků, text zmizel v půlce | `faze2c-prompty-alzask-08.md` |
| Ladění algoritmu screenshoty | 30 promptů, 8 kol | `faze2b-prompty-alzask-07.md` |
| Precision nálezů revizora | ~21–31 % (externí měření) | `faze3c-pravidla-inbox.md` |
| Přenos mezi projekty | 10 z 13 pravidel ruční kopií, 4 bit-shodné | `faze2d-prompty-fhb-myfaber.md` |
| Vrstva cross-project rules | v `CLAUDE.md` uvedená, ve skutečnosti neexistuje | tamtéž |
| Vrstvový audit: přenos fhb→alzask | 16 minut, a vyrostl | tamtéž |
| Investice do pluginu | 137 promptů, ~56 na inženýrství | `faze2e-prompty-shared.md` |
| Cena postavení brány | půl dne zadání + běh + 2–3 dny doladění | tamtéž |
| Chyba v existujícím decku | „3,5 znaku/token" místo dokumentovaných 4 | `korekce-pro-syntezu.md` |
| Tokenizér v decku | falešný — hardcoded pole | `faze4b-verifikace-a-mezery.md` |
| `/compact <instrukce>` | funguje a je dokumentované | tamtéž |

## Návrh dílů série (draft)

| Blok | Téma | ID | Min |
|---|---|---|---|
| 1 | Jak to pod tím funguje | F-01…F-05, M-02, X-01 | 88 |
| 2 | Kontext je něco, co se staví | K-01, K-02, K-03, K-08, R-01, A-02, N-01…N-04, O-04, X-02, X-09 | 137 |
| 3 | Brány a kvalita | M-01, M-03…M-09, K-04…K-07, X-03, X-04, X-07, X-10, X-11 | 175 |
| 4 | Rozšíření a orchestrace | R-02…R-06, O-01…O-03, O-05, X-06, X-12 | 125 |
| 5 | Analytické postupy | A-01, A-03…A-11, M-10, X-05 | 156 |
| 6 | Učení ze vlastní praxe | U-01…U-05, X-08 | 72 |

**Bloky 2, 3, 4, 5 překračují 90 minut — draft je potřeba rozdělit nebo proškrtat.
To je hlavní úkol pro red-team a syntézu.**

## Otevřené otázky, které si uvědomuji sám

1. **66 námětů je pravděpodobně moc.** Které vypadnou?
2. **Několik námětů je `[infra]`** — kolega si je neodnese bez toho, aby někdo postavil
   nástroj. Které to jsou a mají v programu být, nebo do samostatného „pro toho, kdo to
   bude stavět"?
3. **Okruh `A` a `M` se překrývá** — brány jsou mechanika i analytický postup.
4. **Chybí námět o ceně a rozpočtu.** Mám čísla ($5/$25 za MTok Opus 5), ale nemám
   z vlastní praxe doklad, kolik mě to reálně stálo — nesbíral jsem to.
5. **Nemám nic o práci ve dvojici / týmu.** Všechna data jsou moje sólo praxe.
