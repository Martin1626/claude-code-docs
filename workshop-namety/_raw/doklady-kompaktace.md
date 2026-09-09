# Doklady o kompaktaci kontextu — z transkriptů

Zdroj: `~/.claude/projects/c--Git-alzask/*.jsonl` a `...c--Git-fhb/*.jsonl`, odečteno 2026-08-26 09:35.

Kompaktace se v transkriptu značí záznamem s `isCompactSummary: true` a klíčem
`compactMetadata`, doplněným systémovým záznamem `system/compact_boundary`. Metadata
nesou přesná čísla, takže se nemusí nic odhadovat.

## Tři výhrady, které patří k těmto číslům

**1. Deduplikace.** Fork a obnovení session kopírují záznam o kompaktaci do dalšího
souboru, takže tatáž událost je v datech vícekrát. Identita události je zde určena
trojicí (čas, tokeny před, tokeny po). Nalezeno **2 duplikátů**, které
jsou z počtů vyřazené. První verze tohoto souboru je vykazovala jako samostatné
kompaktace — chyba nalezená red-teamem.

**2. Krok se počítá jako `před − po`,** ne jako rozdíl kumulativních součtů. Původní
verze skriptu odečítala `cumulativeDroppedTokens` proti předchozímu záznamu **téže
session** — a protože fork má jiné ID session, první záznam ve forku dostal celý
kumulativ jako jeden krok. Součet tím byl nadhodnocený o 36 %.

**3. Je to podvýběr, ne úplný počet.** Historie příkazů zná 51× `/compact` v pracovních
projektech, ale transkriptů na disku je jen 84 souborů (historie zná 175 sessions jen
pro alzask). Čísla níže tedy popisují **vzorek**, ne všechny kompaktace.

**A ještě jedna, obecnější.** Dokumentace parsování těchto souborů výslovně
nedoporučuje — formát je interní a mění se mezi verzemi. Doporučená cesta je `/export`
nebo `claude -p --output-format json`. Tato čísla platí pro tuto verzi.

| Projekt | Sessions | MB transkriptů |
|---|---|---|
| alzask | 84 | 122.6 |
| fhb | 8 | 10.2 |

## Co obsahuje `compactMetadata`

| Klíč | Význam |
|---|---|
| `trigger` | `manual` (napsal jsem `/compact`) nebo `auto` (harness zasáhl sám před stropem) |
| `preTokens` | kolik tokenů měl kontext **před** kompaktací |
| `postTokens` | kolik tokenů zůstalo **po** ní |
| `cumulativeDroppedTokens` | kolik se v této session zahodilo celkem (POZOR: kumulativ, ne krok) |
| `durationMs` | jak dlouho kompaktace trvala |
| `preservedSegment` | ukazatel na část konverzace zachovanou doslovně |

## Všechny zaznamenané kompaktace (po deduplikaci)

| # | Datum | Projekt | Session | Trigger | Před | Po | Zahozeno | Ubylo | Trvalo |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-08-09 18:17 | alzask | `8671e215` | manual | 579 010 | 8 244 | 570 766 | 98.6 % | 196.4 s |
| 2 | 2026-08-10 15:26 | alzask | `8671e215` | manual | 440 617 | 9 506 | 431 111 | 97.8 % | 186.2 s |
| 3 | 2026-08-11 05:32 | alzask | `8671e215` | manual | 544 395 | 7 100 | 537 295 | 98.7 % | 171.5 s |
| 4 | 2026-08-11 13:55 | alzask | `8671e215` | manual | 586 517 | 11 668 | 574 849 | 98.0 % | 224.1 s |
| 5 | 2026-08-12 19:24 | alzask | `84d16ec6` | manual | 602 574 | 14 075 | 588 499 | 97.7 % | 159.7 s |
| 6 | 2026-08-13 06:26 | alzask | `84d16ec6` | manual | 408 542 | 11 757 | 396 785 | 97.1 % | 159.9 s |
| 7 | 2026-08-13 10:27 | alzask | `84d16ec6` | manual | 419 004 | 11 950 | 407 054 | 97.1 % | 201.7 s |
| 8 | 2026-08-13 20:58 | alzask | `fe6ed3f5` | manual | 356 334 | 9 488 | 346 846 | 97.3 % | 191.4 s |
| 9 | 2026-08-18 20:16 | alzask | `c72f51b9` | manual | 583 578 | 12 127 | 571 451 | 97.9 % | 180.7 s |
| 10 | 2026-08-19 13:26 | alzask | `e8e214bb` | manual | 572 770 | 13 344 | 559 426 | 97.7 % | 119.3 s |
| 11 | 2026-08-19 17:45 | alzask | `740e5808` | manual | 422 833 | 18 885 | 403 948 | 95.5 % | 200.7 s |
| 12 | 2026-08-19 19:06 | alzask | `740e5808` | manual | 416 445 | 16 927 | 399 518 | 95.9 % | 193.9 s |
| 13 | 2026-08-19 20:32 | alzask | `740e5808` | manual | 521 073 | 15 372 | 505 701 | 97.0 % | 184.9 s |
| 14 | 2026-08-19 20:43 | alzask | `740e5808` | manual | 136 471 | 20 495 | 115 976 | 85.0 % | 183.5 s |
| 15 | 2026-08-20 10:01 | fhb | `dd923fb6` | manual | 214 931 | 13 372 | 201 559 | 93.8 % | 177.5 s |
| 16 | 2026-08-21 14:17 | alzask | `aa5edff8` | manual | 618 390 | 15 342 | 603 048 | 97.5 % | 173.8 s |
| 17 | 2026-08-22 21:21 | alzask | `90d8b6e7` | manual | 575 151 | 15 666 | 559 485 | 97.3 % | 162.2 s |
| 18 | 2026-08-24 06:06 | alzask | `70e84664` | manual | 464 352 | 10 248 | 454 104 | 97.8 % | 172.8 s |
| 19 | 2026-08-25 10:09 | alzask | `d02c3695` | manual | 392 015 | 18 245 | 373 770 | 95.3 % | 168.6 s |

## Souhrn

| Metrika | Hodnota |
|---|---|
| Zaznamenaných kompaktací (po deduplikaci) | **19** |
| Vyřazených duplikátů | 2 |
| Ručních (`/compact`) / automatických | **19 / 0** |
| Medián kontextu před kompaktací | 464 352 tokenů |
| Maximum před kompaktací | 618 390 tokenů |
| Medián kontextu po kompaktaci | 13 344 tokenů |
| **Medián podílu zahozeného kontextu** | **97.3 %** |
| Rozsah zahozeného podílu | 85.0 % – 98.7 % |
| Medián doby kompaktace | 180.7 s |
| Nejdelší kompaktace | 224.1 s |
| **Celkem zahozeno tokenů** | **8 601 191** |

Medián páru před/po je 464 352 → 13 344. Pozor: to nejsou
dvě hodnoty téže kompaktace, jsou to dva nezávislé mediány — proto se z nich nemá
počítat procento. Mediánový **podíl** je uvedený zvlášť výše.

### Sessions s nejvíc zahozeným kontextem

| Projekt | Session | Kompaktací | Zahozeno tokenů |
|---|---|---|---|
| alzask | `8671e215` | 4 | 2 114 021 |
| alzask | `740e5808` | 4 | 1 425 143 |
| alzask | `84d16ec6` | 3 | 1 392 338 |
| alzask | `aa5edff8` | 1 | 603 048 |
| alzask | `c72f51b9` | 1 | 571 451 |
| alzask | `90d8b6e7` | 1 | 559 485 |
| alzask | `e8e214bb` | 1 | 559 426 |
| alzask | `70e84664` | 1 | 454 104 |
| alzask | `d02c3695` | 1 | 373 770 |
| alzask | `fe6ed3f5` | 1 | 346 846 |

## Jak to čítat na workshopu

Medián zahozeného podílu je **97.3 %.** Po typické kompaktaci
zůstane z konverzace zlomek; zbytek je nahrazený shrnutím. Shrnutí drží záměr a
rozhodnutí, ale doslovné výstupy nástrojů, čísla řádků a přesné citace v něm nejsou.
Analytik, který se opírá o `soubor:řádek`, po kompaktaci pracuje s vyprávěním o zdroji.

Druhá, méně zjevná cena je čas: medián **180.7 s**,
nejdéle 224.1 s. Kompaktace není okamžitá operace — je to
další volání modelu, které musí přečíst celou dosavadní konverzaci.

A třetí věc, nejdůležitější: **ani jedna z těch kompaktací nebyla vyvolaná automaticky**
a **ani jedna neměla instrukci.** `/compact` přijímá argument (`/compact zachovej …`),
kterým se dá říct, co má souhrn udržet. Nevyužil jsem to ani jednou.
