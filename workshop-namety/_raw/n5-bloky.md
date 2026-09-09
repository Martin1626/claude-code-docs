---

# Návrh dílů série

**Podmínka, kterou návrh drží:** žádný díl nepřekračuje **90 minut** čistého obsahu.
Součty jsou spočítané skriptem (`_raw/n5-bloky.py`) z minut v souhrnné tabulce, ne
odhadem — draft měl tři ze šesti bloků sečtené špatně a red-team to našel.

**Jak návrh čítat.** Katalog má 56 námětů a 694 minut, což je při kratších setkáních
deset až jedenáct dílů. To je hodně — ale katalog je **zásoba, ne program**. Pokud
série má být kratší, škrtej podle priority (`must` je 37 námětů) nebo vezmi jen díly
1, 3 a 6, které nesou tři hlavní myšlenky. Díl 0 a příloha `P` se nepřednáší.

## Díl 0 — Příprava (nepřednáší se)

**15 minut** · 1 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| N-06 | Cvičný repozitář — nulté dílo série | infra | 15 | must |

**Co si z toho odnesou:** Cvičný repozitář, na kterém se smí rozbíjet. Bez něj polovina dem nejde předvést.

## Díl 1 — Co se pod tím děje a co tě to stojí

**79 minut** · 6 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| F-01 | Claude si tě nepamatuje. Vede si o tobě složku. | výklad+demo | 15 | must |
| F-02 | Čeština není dražší, protože je delší | výklad | 12 | must |
| F-05 | Co tě stojí místo, o kterém nevíš | výklad+demo | 15 | must |
| N-05 | Co to stojí a jak to zjistíš | demo | 10 | should |
| F-03 | Tomu shrnutí můžeš říct, co má zachovat | výklad | 15 | must |
| F-04 | Padesát jedna ku jedné | příběh+demo | 12 | must |

**Co si z toho odnesou:** Model si nic nepamatuje, celá historie se posílá znovu, a proto dlouhá session zdražuje každý další prompt. Kompaktace session zachrání, ale zahodí 97 % — a dá se jí říct, co má nechat.

## Díl 2 — Než pustíš agenta na svá data

**51 minut** · 5 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| N-01 | Tři zákazy, které si nastav dřív než cokoli jiného | demo | 8 | must |
| N-02 | Tři úrovně zpět: `Esc Esc`, `/rewind`, `git diff` | demo | 8 | must |
| N-03 | Režim plánování: rozhodnutí odděleně od provedení | demo | 10 | must |
| M-02 | „Napiš to do chatu, nic neměň" | demo+cvičení | 10 | must |
| N-04 | Prompt je zápis, ne rozhovor | příběh+výklad | 15 | must |

**Co si z toho odnesou:** Tři zákazy, tři úrovně zpět, vestavěný režim plánování a jedna věta („nic neměň"). A jedno pravidlo, které se nedá vzít zpátky: prompt je zápis, ne rozhovor.

## Díl 3 — Zadání: dokument nese kontext, prompt nese rozhodnutí

**84 minut** · 6 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| K-01 | Dokument nese kontext, prompt nese rozhodnutí | výklad+demo | 20 | must |
| R-01 | Zadání do souboru, session ho jen provede | demo+cvičení | 15 | must |
| K-02 | Bezcílný rozkaz | příběh+cvičení | 12 | must |
| X-04 | Dlouhý prompt v chatu se tiše ořízne | příběh | 10 | must |
| K-03 | Co NEčíst — a proč u každé položky | výklad+cvičení | 12 | must |
| A-02 | Číslovaný picklist a odpověď čísly | demo+cvičení | 15 | must |

**Co si z toho odnesou:** Krátký prompt funguje jen nad postaveným kontextem. Dlouhé zadání patří do souboru — dá se revidovat, spustit znovu a je v Gitu.

## Díl 4 — Jak se ptát, aby odpověď byla k něčemu

**64 minut** · 6 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| A-04 | Straw-man: napiš hypotézu, ať ji jen opraví | výklad+demo | 12 | must |
| A-03 | Rozpočet na otázky a páka místo nejasnosti | výklad | 12 | must |
| A-05 | Sebekritika útokem na náklad na údržbu | výklad | 10 | must |
| K-04 | Ticho je nález, ne absence nálezu | výklad | 10 | must |
| A-09 | Vyjednej terminologii dřív, než začneš psát | výklad | 10 | should |
| U-04 | Nech si to vysvětlit laicky a pojmenuj, co nevíš | výklad | 10 | should |

**Co si z toho odnesou:** Hypotéza místo otázky, rozpočet na otázky, páka místo nejasnosti, a útok na náklad údržby — čtyři věty, které z modelu udělají oponenta místo pochlebovače.

## Díl 5 — Když to nejde: zmenši úlohu, ne prompt

**44 minut** · 4 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| A-06 | Redukce na minimální případ | příběh | 12 | must |
| A-07 | Specifikace invariantem místo symptomu | výklad | 12 | must |
| X-03 | Tři situace, kdy jsem měl vypnout terminál | výklad | 10 | must |
| O-05 | Izolace, které nerozumíš, tě stojí dopoledne | příběh | 10 | must |

**Co si z toho odnesou:** Po třetím nepovedeném kole nepiš čtvrtý prompt — zmenši úlohu a napiš invariant. A poznej tři situace, kdy je ruční práce rychlejší.

## Díl 6 — Proč to, co postavíš, přestaneš používat

**82 minut** · 6 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| M-01 | Brána, kterou nikdo nespouští, je taky jen prompt | výklad+demo | 18 | must |
| K-07 | Čtvrtina mého `CLAUDE.md`, kterou nikdo nespustil | příběh+demo | 15 | must |
| X-02 | Postavil jsem pipeline a nikdy ji nespustil | příběh | 12 | must |
| U-02 | Záchyt bez povyšovací brány je archiv | příběh | 15 | must |
| X-01 | Vygeneroval jsem 22 souborů a pak je smazal | příběh | 10 | must |
| M-07 | Práh, který realita překračuje — a prázdné pole | příběh+demo | 12 | should |

**Co si z toho odnesou:** Nejsilnější a nejnepříjemnější díl. Brána, kterou nikdo nespouští, je taky jen prompt — a mezi „postaveno" a „používáno" je propast, kterou je vidět na vlastních datech.

## Díl 7 — Revize a kvalita bez slepé automatiky

**61 minut** · 5 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| M-03 | Triáž dělá člověk. Dva ze tří nálezů jsou falešné. | výklad+příběh | 15 | must |
| M-05 | Vykazuj, kolik jsi toho NEzkontroloval | demo | 12 | must |
| M-06 | Deterministická kontrola vs. sémantická | výklad | 12 | must |
| M-04 | Slepý recenzent | výklad | 10 | should |
| A-08 | Publikum jako parametr — a pravidlo, které se poruší | výklad+demo | 12 | should |

**Co si z toho odnesou:** Dva ze tří nálezů jsou falešné, takže triáž nesmí dělat model. Vykazuj, kolik jsi NEzkontroloval. A nenech sémantickou kontrolu předstírat, že dělá práci deterministické.

## Díl 8 — Orchestrace: kam jde hluk

**47 minut** · 4 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| O-01 | Subagent není o rychlosti, ale o tom, kam jde hluk | výklad+demo | 15 | must |
| O-02 | Model podle povahy úlohy — a měřím to vůbec? | výklad+příběh | 12 | should |
| O-03 | Jak předat práci sobě zítra | demo | 12 | should |
| O-04 | Jedna session = jedno téma, pojmenované | demo | 8 | should |

**Co si z toho odnesou:** Subagent se nepoužívá pro rychlost, ale proto, že jeho hluk zůstane mimo tvůj kontext. Model se vybírá podle povahy úlohy — a stojí za to změřit, jestli to k něčemu bylo.

## Díl 9 — Vlastní výbava a jak ji předat dál

**68 minut** · 6 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| R-02 | Metodika bez spouštěče je jen text | příběh+demo | 12 | must |
| R-04 | Dvě vrstvy se rozjedou, když jednu nikdo nečte | výklad | 10 | should |
| R-03 | Uložený postup místo opakovaného promptu | demo | 12 | should |
| U-05 | Co commitnout, aby to fungovalo i kolegovi | demo | 12 | must |
| U-06 | Vysvětlovací artefakt: osnovu nech schválit první | demo | 10 | should |
| R-05 | Dva hooky, které mi běží, a šest, které neznám | demo | 12 | could |

**Co si z toho odnesou:** Metodika bez spouštěče je jen text. Skill a příkaz jsou to, co postup skutečně spustí — a Git je to, co ho dá kolegovi.

## Díl 10 — Velký audit a co z toho všeho žije

**62 minut** · 4 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| A-01 | Vrstvový audit dokumentace | výklad+cvičení | 25 | must |
| U-01 | Debuguj prompt, ne výstup | výklad+cvičení | 15 | must |
| U-03 | Nástroj cestoval mezi projekty a vyrostl | příběh | 12 | should |
| U-07 | Co z toho po sedmi měsících doopravdy žije | výklad | 10 | must |

**Co si z toho odnesou:** Vrstvový audit jako vrchol série: tytéž skutečnosti ve třech dokumentech, rozpory na hranicích vrstev. A závěr: drží se to, co má spouštěč nebo nulovou cenu vyvolání.

## Díl P — Příloha pro toho, kdo bude stavět nástroje

**37 minut** · 3 námětů

| ID | Námět | Role | Min | Prio |
|---|---|---|---|---|
| K-05 | Citace se ověřuje, nevěří | demo+infra | 15 | should |
| M-08 | Dva exit kódy = dva různé signály | demo+infra | 10 | could |
| K-06 | Hierarchie autority rozhoduje spor, ne datum | výklad | 12 | should |

**Co si z toho odnesou:** Nepatří do hlavní série. Kdo bude stavět validátory a kontrolu citací pro tým, najde tu zásady i cenu.

## Kontrola součtů

| Díl | Námětů | Minut | Do 90 min? |
|---|---|---|---|
| 0 | 1 | 15 | ano |
| 1 | 6 | 79 | ano |
| 2 | 5 | 51 | ano |
| 3 | 6 | 84 | ano |
| 4 | 6 | 64 | ano |
| 5 | 4 | 44 | ano |
| 6 | 6 | 82 | ano |
| 7 | 5 | 61 | ano |
| 8 | 4 | 47 | ano |
| 9 | 6 | 68 | ano |
| 10 | 4 | 62 | ano |
| P | 3 | 37 | ano |

Přednášených dílů 1–10: **642 minut.** Plus příprava (díl 0) a příloha `P`.

Námětů v tabulce: 56 · zařazených do dílů: 56 · nezařazených: 0

---

## Tři možné střihy, kdyby série měla být kratší

| Varianta | Díly | Minut | Co publikum dostane |
|---|---|---|---|
| **Tři díly** | 1, 3, 6 | 245 | mechanika, zadávání, a proč postavené věci umírají |
| **Pět dílů** | 1, 2, 3, 6, 7 | 357 | plus bezpečné pouštění agenta a revizní disciplína |
| **Celá série** | 1–10 | 642 | vše včetně velkého auditu a předání kolegovi |

U každé varianty platí, že **díl 0 (cvičný repozitář) musí existovat předem.**
