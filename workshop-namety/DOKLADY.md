> **Tento dokument je příloha katalogu námětů na workshop.**
> Hlavní katalog: [NAMETY.md](NAMETY.md) · výklad fundamentu: [FUNDAMENT.md](FUNDAMENT.md) ·
> vyřazené náměty: [VYRAZENO.md](VYRAZENO.md).

# Doklady — statistiky a inventář výbavy

Všechno v tomto dokumentu je **měřené**, ne odhadnuté, pokud u toho není napsáno „odhad".
Skripty, které to spočítaly, zůstaly v `_raw/` (`verify_counts.py`, `doklady_gen.py`,
`compact_stats.py`, `context_cost.py`) — čísla jsou tedy přepočitatelná.

## Jak to čítat

Tři nezávislé zdroje dat, každý měří něco jiného:

| Zdroj | Co v něm je | K čemu je dobrý |
|---|---|---|
| `~/.claude/history.jsonl` | 2 671 promptů zadaných člověkem, 7 měsíců, 0,84 MB | Jak zadávám. Délky promptů, slash commandy, rozložení v čase. |
| `~/.claude/projects/*/*.jsonl` | 84 sessions, 120 MB transkriptů | Co se v session skutečně stalo. **Kompaktace s přesnými čísly.** |
| Soubory v repozitářích | `CLAUDE.md`, pravidla, paměti, skilly | Kolik místa zabere kontext, než začnu psát. |

**Pozor na dvě sady čísel.** Statistiky se liší podle toho, jestli měřím celou historii
zadávání, nebo jen projekty v rozsahu tohoto workshopu (alzask, fhb, myfaber, shared).
Rozdíl není kosmetický — u `/compact` je to 67× proti 51×. Kde to hraje roli, jsou
uvedené obě.

**Jedna metodická poznámka, která se hodí i jako námět.** Když jsem tato čísla měřil,
historie mezi dvěma běhy skriptu povyrostla — o moje vlastní prompty z toho měření.
`history.jsonl` je soubor, který roste s každým zadáním. Proto se drobné odchylky
v kontrolních součtech (1503 → 1507 → 1508) nevysvětlují chybou, ale tím, že měřím
běžící systém.

---


# Část 1 — Statistiky zadávání

### Statistiky z history.jsonl — ověřený podklad

Zdroj: `C:/Users/ai_martint/.claude/history.jsonl`, odečteno 2026-08-26 08:55.
Jeden řádek = jeden prompt zadaný člověkem. Normalizace cesty: lowercase + zpětná lomítka na dopředná (cesty v souboru mají nekonzistentní velikost písmen).

#### Základní rozsah

| Celek | Promptů | Období |
|---|---|---|
| Celá historie (všechny projekty) | 2671 | 2026-01-19 → 2026-08-26 |
| Jen pracovní projekty (v rozsahu) | 1508 | 2026-01-29 → 2026-08-26 |

> **Pozor na dvě sady čísel.** Většina statistik níže je uvedena dvakrát — pro celou historii a jen pro pracovní projekty. Rozdíl je podstatný (např. `/compact` 67× vs. 51×) a záměna vede k nesprávně atribuovanému tvrzení.

#### Prompty per projekt (pracovní projekty)

| Projekt | Promptů | % z pracovních |
|---|---|---|
| `c:/git/alzask` | 1139 | 75.5 % |
| `c:/git/fhb` | 212 | 14.1 % |
| `c:/git/shared/plugins/spec-factory` | 137 | 9.1 % |
| `c:/git/shared` | 14 | 0.9 % |
| `c:/git/myfaber` | 6 | 0.4 % |
| **Celkem** | **1508** | **100 %** |

#### Prompty per měsíc

| Měsíc | Celá historie | Pracovní | alzask | fhb | spec-factory | shared | myfaber |
|---|---|---|---|---|---|---|---|
| 2026-01 | 20 | 7 | 7 | 0 | 0 | 0 | 0 |
| 2026-02 | 34 | 8 | 7 | 0 | 0 | 0 | 1 |
| 2026-03 | 9 | 3 | 0 | 3 | 0 | 0 | 0 |
| 2026-04 | 50 | 7 | 0 | 7 | 0 | 0 | 0 |
| 2026-05 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2026-06 | 419 | 357 | 235 | 117 | 0 | 0 | 5 |
| 2026-07 | 935 | 628 | 432 | 58 | 137 | 1 | 0 |
| 2026-08 | 1203 | 498 | 458 | 27 | 0 | 13 | 0 |

#### Slash commandy

##### Vestavěné — vypovídají o praxi řízení kontextu a modelu

| Příkaz | Celá historie | Pracovní projekty | Co to říká |
|---|---|---|---|
| `/compact` | 67× | 51× | tolikrát mi kontext došel a musel se destruktivně shrnout |
| `/model` | 63× | 53× | tolikrát jsem přepínal model — volba modelu je vědomá operace, ne nastavení jednou navždy |
| `/resume` | 58× | 33× | tolikrát jsem se vracel do staré session místo psaní nové |
| `/context` | 42× | 37× | tolikrát jsem si šel ručně zkontrolovat zaplnění okna |
| `/effort` | 9× | 4× | reasoning effort přepínám řádově méně často než model |
| `/clear` | 6× | 1× | čistý reset s předáním — proti 51 kompaktacím prakticky nepoužívaný |

**Klíčový poměr:** `/compact` 51× proti `/clear` 1× v pracovních projektech. Kontext jsem nechával dojet do kompaktace místo řízeného resetu s předáním.

##### Vlastní commandy a skilly

| Příkaz | Celá historie | Pracovní projekty |
|---|---|---|
| `/body-z-jednani` | 34× | 33× |
| `/spec` | 22× | 21× |
| `/spec-factory:spec` | 6× | 4× |
| `/btw` | 8× | 7× |
| `/dodavatele:mail` | 4× | 4× |
| `/dodavatele:stav` | 3× | 3× |
| `/pruzkum` | 5× | 4× |

##### Kompletní pořadí (pracovní projekty, vše nad 2×)

| Příkaz | Počet |
|---|---|
| `/model` | 53× |
| `/compact` | 51× |
| `/context` | 37× |
| `/resume` | 33× |
| `/body-z-jednani` | 33× |
| `/rename` | 29× |
| `/plugins` | 27× |
| `/spec` | 21× |
| `/reload-plugins` | 12× |
| `/status` | 10× |
| `/config` | 8× |
| `/plugin` | 8× |
| `/btw` | 7× |
| `/new` | 5× |
| `/exit` | 5× |
| `/effort` | 4× |
| `/pruzkum` | 4× |
| `/spec-factory:spec` | 4× |
| `/dodavatele:mail` | 4× |
| `/memory` | 3× |
| `/usage` | 3× |
| `/spec-factory:review-spec` | 3× |
| `/dodavatele:stav` | 3× |

#### Délka promptu

| Metrika | Celá historie | Pracovní projekty |
|---|---|---|
| minimum | 1 | 1 |
| p25 | 19 | 15 |
| medián | 75 | 66 |
| p75 | 174 | 167 |
| p90 | 283 | 365 |
| p99 | 1549 | 1775 |
| maximum | 22386 | 7213 |

Hodnoty ve znacích.

##### Histogram (pracovní projekty)

| Pásmo (znaků) | Promptů | % | Co to typicky je |
|---|---|---|---|
| 0–50 | 652 | 43.2 % | jednoslovné dodatky, potvrzení, slash commandy |
| 50–100 | 269 | 17.8 % | krátký dodatek v rozjeté konverzaci |
| 100–250 | 346 | 22.9 % | jedna konkrétní otázka nebo úkol |
| 250–500 | 139 | 9.2 % | úkol s kontextem |
| 500–1000 | 71 | 4.7 % | úkol s kontextem a omezeními |
| 1000+ | 31 | 2.1 % | strukturované zadání — kontext, úkol, omezení, formát výstupu |

**Napětí, které stojí za pozornost:** medián 66 znaků, ale 31 promptů nad 1000 znaků (celá historie: medián 75, 44 nad 1000). Zadávání má dva režimy: velké strukturované zadání na začátku úlohy a pak desítky krátkých dodatků. Ty krátké dodatky jsou levné na napsání, ale každý z nich přeposílá celou historii znovu.

#### Nejdelší prompty (pracovní projekty, nad 1000 znaků)

| # | Datum | Znaků | Projekt | Začátek |
|---|---|---|---|---|
| 1 | 2026-08-24 12:18 | 7213 | alzask | # PROMPT — Zpětné dorovnání nástrojů registru ze šablony pluginu (AlzaSk) > **Jak to použít:** vlož obsah do čerstvé session v repozitáři `C:\Git\alza |
| 2 | 2026-06-26 21:24 | 6240 | fhb | Na základě závěrů schůzky @docs/meetings/2026-06-26_06-26_FHB_Sjednocení_terminologie_a_procesy_dopravníku.md prověř, zda jsou správně formulované nás |
| 3 | 2026-08-14 20:29 | 5280 | alzask | Porovnej dvě vrstvy popisu jednoho API v repozitáři C:\Git\alzask: TOK docs\api\Diagrams-API-AlzaSk-v3.md — chování v čase: kdo koho volá, v jakém poř |
| 4 | 2026-08-25 19:38 | 4502 | alzask | Naléhavě potřebuju propsat doložené odpovědi dodavatele BullsEye do PLC specifikací. Kontext: v předchozí session jsem ukotvil dodavatelskou korespond |
| 5 | 2026-08-14 20:13 | 3344 | fhb | Přečti tyto tři dokumenty ve složce C:\Git\fhb\docs\api\asrs-v2\ jako tři vrstvy popisu jedné a téže věci: KONCEPT ASRS-v2-API-koncept.md — záměr: co  |
| 6 | 2026-08-14 19:36 | 3052 | alzask | Přečti tyto tři dokumenty ve složce C:\Git\fhb\docs\api\asrs-v2\ jako tři vrstvy popisu jedné a téže věci: KONCEPT ASRS-v2-API-koncept.md — záměr: co  |
| 7 | 2026-08-04 19:48 | 2445 | alzask | Co se týká těch majáků tak tam došlo k nějakému nedorozumění. Ty věci se týkají 2 různých portů. V okamžiku vkládání nosiče na vstupní dopravník operá |
| 8 | 2026-08-19 11:21 | 2175 | alzask | Přelož do angličtiny tento text: Zápis ze společného jednání KVADOS – BullsEye Datum: 19. 8. 2026 / Téma: Integrace WES (KVADOS) se systémem WCS (Bull |
| 9 | 2026-07-09 21:54 | 2106 | alzask | Zapracuj odpovědi požadované v @docs/plc/BACKLOG.md 1. Kdo dodává bezpečnostní a řídicí prvky portů? Předpokládáme TMT — potvrdit. [PAC/TMT] U mezanin |
| 10 | 2026-08-12 13:48 | 1905 | alzask | Pomoz mi formulovat krátký, cílený dotaz na upřesnění konkrétního chování. Zatím BullsEye odpovídá příliš v obecné rovině. Napiš zatím dotazy v češtin |
| 11 | 2026-07-13 20:48 | 1886 | alzask | Připrav html stránku, která bude demonstrovat pohyb palet po dopravníku. jedná se o dopravník s 10 paletovými lokaci. Dopravník má první dva segmenty  |
| 12 | 2026-06-19 23:51 | 1879 | alzask | /spec Kolegyně, kterou nemám příliš v oblibě, mi poslala připomínky k diagramu @docs/api/Diagrams-API-AlzaSk-v2.md Zhodnoť jejich relevanci na škále 1 |
| 13 | 2026-07-13 20:47 | 1875 | alzask | Připrav html stránku, která bude demonstrovat pohyb palet po dopravníku. jedná se o dopravník s 10 paletovými lokaci. Dopravník má první dva segmenty  |
| 14 | 2026-06-19 22:04 | 1821 | alzask | /spec Kolegyně, kterou nemám příliš v oblibě, mi poslala připomínky k diagramu @docs/api/Diagrams-API-AlzaSk-v2.md Zhodnoť jejich relevanci na škále 1 |
| 15 | 2026-06-19 23:48 | 1821 | alzask | /spec Kolegyně, kterou nemám příliš v oblibě, mi poslala připomínky k diagramu @docs/api/Diagrams-API-AlzaSk-v2.md Zhodnoť jejich relevanci na škále 1 |
| 16 | 2026-06-19 21:57 | 1775 | alzask | /spec Kolegyně, kterou nemám příliš v oblibě, mi poslala připomínky k diagramu @docs/api/Diagrams-API-AlzaSk-v2.md Zhodnoť jejich relevanci na škále 1 |
| 17 | 2026-07-13 21:47 | 1767 | spec-factory | Nosiče přijíždějí z pravé strany jsou odebírané z levé strany. Simulace musí umožnit z levé strany odebrat paletu , například kliknutím. Zároveň z pra |
| 18 | 2026-07-12 15:17 | 1679 | spec-factory | Prezentace Mým cílem je vytvořit přehlednou intuitivní prezentaci, jack funguje Claude Code. Nyní chce vytvořit jenom osnovu až si ji schválíme tak te |
| 19 | 2026-07-12 16:47 | 1611 | alzask | Dokuemnty @docs/plc/AlzaSk-PLC-specifikace.md a @docs/plc/AlzaSk-PLC-specifikace-mezanin.md jsou obsáhlé a složité. Chci proto vytvořit HTML prezentac |
| 20 | 2026-08-10 19:43 | 1607 | alzask | Upozorňuji, že ERROR_PRE_RECEIPT_0_1_P01 je dopravníkový port na dopravníkové stanici ERROR_PRE_RECEIPT_0_1 a je u něj instalovaný HMI panel! Robot zd |
| 21 | 2026-07-11 12:53 | 1598 | alzask | Signalizace majáku, které jsou u portů, jsou pro operátora. Musí tedy odpovídat této konvenci. 9.1, 9.2, 9.3, 9.14: Posouzení rizik musí provést KVADO |
| 22 | 2026-06-29 20:38 | 1535 | alzask |  Architektura zastavení a PLC 1. LED pásky (Pick-to-Light) ven z PLC spec → do WES dokumentace Proč: LED pásky neovládá PLC, ale kontroler připojený p |
| 23 | 2026-07-05 13:16 | 1384 | spec-factory | Proveď kompletní audit pluginu spec-factory. ROZSAH: celý plugin — agenti, orchestrátor (commands/spec.md), hooky, tools, rules, templates, konfigurac |
| 24 | 2026-08-24 20:47 | 1371 | alzask | Formuluj v češtině následující otázky tak, aby jim dodavatel správně rozuměl. Dotaz na BullsEye, jaké jsou možnosti zastavení 1., 3., 4. nebo 5. patra |
| 25 | 2026-08-19 19:41 | 1216 | alzask | 1. Spusť docs/plc/.plc-tools/validate.cmd (nebo fr-tools/validate.py). Chyby lintru oprav hned, bez LLM. 2. Ulož baseline: git stash list nech být, je |
| 26 | 2026-08-19 19:45 | 1216 | alzask | 1. Spusť docs/plc/.plc-tools/validate.cmd (nebo fr-tools/validate.py). Chyby lintru oprav hned, bez LLM. 2. Ulož baseline: git stash list nech být, je |
| 27 | 2026-08-11 08:20 | 1211 | alzask | Proveď změnu ADR-ASK-API-011. Pořadí volání je nyní již platné. Rozšiř ADR-ASK-HW-005 , aŤ je to jasné. Zda budou HMI u error portů je ještě stále ote |
| 28 | 2026-08-18 15:13 | 1086 | alzask | Vytvoř pracovní markdown dokument který bude sloužit pro jako podklad k jednání s bullseye . Nejprve do něj vytvoř sekvenční diagram který bude popiso |
| 29 | 2026-07-30 09:21 | 1049 | alzask | Proveď následující úpravy v @docs/api/API-myFABER-WES-AlzaSk.yml a v @docs/api/Diagrams-API-AlzaSk-v2.md: 1, 2, 5, 6, 9, 30, uprav popis, kdy lze obje |
| 30 | 2026-08-07 18:13 | 1012 | alzask | Při ochranném zaststavení by se muselo také sjednotit. PAC na tom ještě nezačala pracovat. Je proto ještě čas vytvořit kvalitnější specifikaci. 3) S t |
| 31 | 2026-06-22 09:11 | 1004 | alzask | Myslím, že tuto situaci mu budeme muset řešit jako výjimku. Pokud se nepletu tak můžou nastat 2 situace . Buď operátor paletu s dopravníků odebere vyř |

#### Sessions a vložený obsah

| Projekt | Sessions | Promptů | Promptů na session |
|---|---|---|---|
| alzask | 176 | 1139 | 6.5 |
| fhb | 39 | 212 | 5.4 |
| spec-factory | 19 | 137 | 7.2 |
| shared | 6 | 14 | 2.3 |
| myfaber | 2 | 6 | 3.0 |

Promptů s vloženým obsahem (`pastedContents`): **29** z 1508.
Velikost vloženého obsahu ve znacích: medián 67, maximum 1876.

#### Poznámka k reprodukovatelnosti

Když jsem tato čísla měřil, historie mezi dvěma běhy povyrostla o 4 prompty — o moje vlastní prompty z toho měření. `history.jsonl` je soubor, který roste s každým zadáním. Je to drobnost, ale dobře ilustruje, že „paměť" Claude Code je soubor na disku, ne vlastnost modelu.


---

# Část 2 — Kompaktace kontextu

Tohle je nejtvrdší doklad celé inventury, protože si ho **harness zapsal sám**.
U každé kompaktace ukládá do transkriptu přesná čísla — nemusím nic odhadovat.

> **Výhrada, kterou je nutné uvést.** Dokumentace parsování transkriptů výslovně
> nedoporučuje: formát záznamů je interní a mění se mezi verzemi. Doporučená cesta je
> `/export` nebo `claude -p --output-format json`. Čísla níže jsou platná pro tuto verzi.
> A těch 21 kompaktací je **podvýběr** — historie zná 175 sessions jen pro alzask, ale
> transkriptů na disku je 84.


### Doklady o kompaktaci kontextu — z transkriptů

Zdroj: `~/.claude/projects/c--Git-alzask/*.jsonl` a `...c--Git-fhb/*.jsonl`, odečteno 2026-08-26 09:35.

Kompaktace se v transkriptu značí záznamem s `isCompactSummary: true` a klíčem
`compactMetadata`, doplněným systémovým záznamem `system/compact_boundary`. Metadata
nesou přesná čísla, takže se nemusí nic odhadovat.

#### Tři výhrady, které patří k těmto číslům

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

#### Co obsahuje `compactMetadata`

| Klíč | Význam |
|---|---|
| `trigger` | `manual` (napsal jsem `/compact`) nebo `auto` (harness zasáhl sám před stropem) |
| `preTokens` | kolik tokenů měl kontext **před** kompaktací |
| `postTokens` | kolik tokenů zůstalo **po** ní |
| `cumulativeDroppedTokens` | kolik se v této session zahodilo celkem (POZOR: kumulativ, ne krok) |
| `durationMs` | jak dlouho kompaktace trvala |
| `preservedSegment` | ukazatel na část konverzace zachovanou doslovně |

#### Všechny zaznamenané kompaktace (po deduplikaci)

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

#### Souhrn

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

##### Sessions s nejvíc zahozeným kontextem

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

#### Jak to čítat na workshopu

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


---

# Část 3 — Co zabírá místo v kontextu

### Co zabira misto v kontextu, nez vubec zacnu psat

Merene znaky jsou presne (velikost textu souboru). Prepocet na tokeny je **ODHAD**
pri konzervativnim poměru 3,0 znaku na token pro cesky text — presny tokenizer
Anthropic pro cestinu nezverejnuje, takze cislo ber jako radovou orientaci, ne fakturu.

| Co | Souboru | Znaku | Tokenu (odhad) |
|---|---|---|---|
| CLAUDE.md projektu alzask | 1 | 23 818 | ~7 939 |
| CLAUDE.md podadresaru alzask | 5 | 36 604 | ~12 201 |
| pravidla shared alzask | 15 | 34 840 | ~11 613 |
| pravidla shared fhb | 13 | 25 581 | ~8 527 |
| pamet alzask (MEMORY.md) | 1 | 13 426 | ~4 475 |
| pamet alzask (vsechny soubory) | 27 | 60 836 | ~20 278 |
| knowledge-inbox alzask martint | 18 | 127 067 | ~42 355 |
| skilly projektove alzask | 2 | 12 391 | ~4 130 |
| output style Feynman CZ | 1 | 3 998 | ~1 332 |

#### Co se nacita automaticky pri kazdem startu session v alzask

| Zdroj | Znaku | Tokenu (odhad) |
|---|---|---|
| CLAUDE.md projektu alzask | 23 818 | ~7 939 |
| pamet alzask (MEMORY.md) | 13 426 | ~4 475 |
| output style Feynman CZ | 3 998 | ~1 332 |
| **Soucet** | **41 242** | **~13 747** |

K tomu se pridava systemovy prompt harness, definice vsech nastroju, metadata vsech
dostupnych skillu a obsah znalostniho inboxu za 14 dni (dodava SessionStart hook).
Ty tri cisla nejsou v souborech, ktere umim precist — jsou uvnitr harness.

#### Proc na tom zalezi

Kazdy z tehle tokenu je v kontextu **pred prvnim mym slovem** a posila se znovu
s kazdym dalsim promptem v session. Neni to jednorazova investice — je to konstantni
rezie kazdeho tahu. Prompt cache ji zlevni, ale misto v okne zabira porad.


---

# Část 4 — Inventář výbavy

### PART A — Inventář výbavy
#### 1. SKILLS
| Jméno | Zdroj | Popis |
|-------|-------|-------|

#### 2. COMMANDS
| Jméno | Zdroj | Popis |
|-------|-------|-------|
| glossary | .claude/commands/ | N/A |
| hotovo | .claude/commands/ | Zapíše, že odpověď dodavatele je propsaná do specifikace |
| learn | .claude/commands/ | N/A |
| lookup | .claude/commands/ | N/A |
| mail | .claude/commands/ | Zpracuje e-mail od/pro dodavatele do registru dotazů |
| overview | .claude/commands/ | N/A |
| review-docs | .claude/commands/ | N/A |
| stav | .claude/commands/ | Vypíše, na co se u dodavatele čeká a co už víme |

#### 3. AGENTS
| Jméno | Soubor | Description |
|-------|--------|-------------|
| review-design | .claude/agents/ | Designová kontrola — soulad ADR, API spec, procesní analýzy a FR |
| review-fixer | .claude/agents/ | Automatická oprava auto-fixable nálezů z review reportu (kromě ARCH-DECISION) |
| review-reporter | .claude/agents/ | Agregace nálezů a generování centrálního review reportu |
| review-semantic | .claude/agents/ | Sémantická kontrola FR/TC — konzistence s API schématem, ADR, procesní analýzou |
| review-structural | .claude/agents/ | Strukturální kontrola FR/TC — cross-reference, metodika, init data |

#### 4. HOOKS (ze settings.json)
| Event | File | Popis |
|-------|------|-------|
| (žádné hooks nalezeny v settings.json) |

#### 5. RULES

##### Shared rules
| ID | Název | Paths glob |
|----|----|----------|
| RULE-AP-001_antipatterns | RULE-AP-001_antipatterns | (viz soubor) |
| RULE-AP-002_pokryti-ze-zdroje | RULE-AP-002_pokryti-ze-zdroje | (viz soubor) |
| RULE-CL-001_changelog | RULE-CL-001_changelog | (viz soubor) |
| RULE-DIAG-001_diagramy | RULE-DIAG-001_diagramy | (viz soubor) |
| RULE-GOV-001_boundary-promoce | RULE-GOV-001_boundary-promoce | (viz soubor) |
| RULE-GOV-002_brana-ne-prompt | RULE-GOV-002_brana-ne-prompt | (viz soubor) |
| RULE-META-001_metadata-styl | RULE-META-001_metadata-styl | (viz soubor) |
| RULE-ONT-001_novy-prvek-do-registru | RULE-ONT-001_novy-prvek-do-registru | (viz soubor) |
| RULE-ONT-002_cituj-zdroj-ne-registr | RULE-ONT-002_cituj-zdroj-ne-registr | (viz soubor) |
| RULE-ONT-003_zmizela-resi-clovek | RULE-ONT-003_zmizela-resi-clovek | (viz soubor) |
| RULE-SPEC-001_trace-akceptace | RULE-SPEC-001_trace-akceptace | (viz soubor) |
| RULE-SPEC-002_kritik-cizi-vystup | RULE-SPEC-002_kritik-cizi-vystup | (viz soubor) |
| RULE-SPEC-004_model-pred-hromadnou-aplikaci | RULE-SPEC-004_model-pred-hromadnou-aplikaci | (viz soubor) |
| RULE-TC-001_tc-konvence | RULE-TC-001_tc-konvence | (viz soubor) |
| RULE-TERM-001_terminologie | RULE-TERM-001_terminologie | (viz soubor) |

##### Personal rules (martint)
| Soubor |
|--------|

#### 6. KNOWLEDGE-INBOX
| Autor | Soubor | Datum | Počet kandidátů |
|------|--------|-------|----------------|

#### 7. OUTPUT STYLES
| Jméno | Popis |
|-------|-------|
| Feynman CZ | Český, intuitivní výklad |

#### 8. PLUGINY (installed_plugins.json)
| Jméno | Verze | InstallPath (zkráceno) |
|-------|--------|----------------------|
| frontend-design@claude-plugins-official | b819188d2eea | ~/.claude/plugins/cache/... |
| knowledge-loop@kvados-plugins | 2.0.0 | ~/.claude/plugins/cache/... |
| ontology-registry@kvados-plugins | 1.0.0 | ~/.claude/plugins/cache/... |
| spec-factory@kvados-plugins | 1.9.0 | ~/.claude/plugins/cache/... |
| superpowers@claude-plugins-official | 6.3.0 | ~/.claude/plugins/cache/... |

#### 9. SETTINGS.JSON (klíčové položky)
| Položka | Hodnota |
|---------|--------|
| model | opus[1m] |
| effort | high |
| language | Čeština |
| outputStyle | Feynman CZ |
| worktree.bgIsolation | none |
| statusLine | command (ccstatusline) |
| enabledPlugins | superpowers, knowledge-loop, spec-factory, frontend-design, ontology-registry |
| permissions.allow | 157 pravidel (read, bash, webfetch, websearch, design) |
| permissions.deny | 18 pravidel (git force, rm destructive, format) |
| permissions.additionalDirectories | 7 lokací (tmp, documents, projects, choco) |

#### 10. VALIDÁTORY A NÁSTROJE
| Lokace | Nástroje |
|--------|----------|
| .adr-tools | config.yaml, validate.cmd |
| .claude/rules/shared | README.md |
| .fr-tools | validate.py, config.yaml, schema.yaml, validate.cmd |
| .ontology-tools | audit.py, build.cmd, cite.py, reanchor.py, README.md |
| .plc-tools | validate.cmd, plc-lint.py, README.md |
| docs/suppliers/.tools | questions.py, msg_extract.py |

#### 11. PLUGINS V C:/Git/shared/plugins/
| Plugin | Verze |
|--------|-------|
| knowledge-loop | 2.0.0 |
| ontology-registry | 1.0.0 |
| spec-factory | 1.9.0 |


---

# Část 5 — Korekce inventáře: hooky a nastavení

První průchod inventářem nahlásil **nula hooků**. To bylo nesprávné — hooky nejsou jen
v `settings.json`, ale hlavně v pluginech (`<plugin>/hooks/hooks.json`). Doklad, že aspoň
jeden fakticky běží: knowledge-loop `SessionStart` hook dodal na startu session handle
autora a obsah jeho znalostního inboxu.

Je to samo o sobě použitelné poučení pro workshop: **inventář, který se dívá jen na jedno
místo, vykáže nulu tam, kde je čtyřka.**


### Korekce inventáře — hooky a nastavení (ověřeno hlavní session)

Fáze 1 nahlásila **0 hooků**. To je nesprávné: hooky nejsou jen v `settings.json`, ale hlavně
v pluginech (`<plugin>/hooks/hooks.json`), a ty se do session načtou taky. Doklad, že aspoň
jeden fakticky běží: knowledge-loop SessionStart hook dodal na startu této session handle
`martint` a obsah znalostního inboxu.

#### Reálně aktivní hooky (4)

| Event | Matcher | Co spouští | Zdroj | Co to dělá |
|---|---|---|---|---|
| `SessionStart` | `startup\|clear` | `hooks/session-context.py` | `C:/Git/shared/plugins/knowledge-loop/hooks/hooks.json` | Dodá do session handle autora + obsah jeho knowledge-inboxu za 14 dní; generuje gitignored zrcadlo `.claude/rules/personal/` |
| `PreToolUse` | `Write\|Edit\|NotebookEdit` | `hooks/spec-guard.py` | `C:/Git/shared/plugins/spec-factory/hooks/hooks.json` | Blokuje zápis spec-agentů mimo workspace; governance zóny jsou PROTECT pro automatické agenty |
| `SessionStart` | `startup\|clear` | `docs/ontology/.ontology-tools/session-check.py` | `C:/Git/alzask/.claude/settings.json` | Warning-only kontrola, jestli jsou deriváty ontologie a kotvy citací aktuální |
| `PreToolUse` | `Write\|Edit\|NotebookEdit` | `.claude/hooks/spec-guard.py` | `C:/Git/fhb/.claude/settings.json` | Totéž jako spec-factory guard, ale projektová kopie (starší způsob — v alzask už je nahrazený pluginem) |

**Pozorování pro katalog:** ve fhb je guard nasazený jako projektový hook, v alzask jako
pluginový. Tentýž mechanismus ve dvou vrstvách — doklad, že cesta „nejdřív si to postav
v projektu, pak to povyš do pluginu" je reálná, ne teoretická.

**Použité eventy: 2 ze cca 8** (`SessionStart`, `PreToolUse`). Nepoužívám `PostToolUse`,
`UserPromptSubmit`, `Stop`, `SubagentStop`, `PreCompact`, `Notification` — zejména
`PreCompact` je nápadná mezera při 51 kompaktacích v pracovních projektech.

#### Klíčové nastavení (`~/.claude/settings.json`)

| Klíč | Hodnota | Poznámka pro workshop |
|---|---|---|
| `model` | `opus[1m]` | Nejsilnější model s 1M kontextovým oknem jako výchozí |
| `effortLevel` | `high` | Reasoning effort natrvalo vysoký; `/effort` jen 4× v pracovních projektech |
| `outputStyle` | `Feynman CZ` | Vlastní output style — čeština, tykání, vysvětlování od podstaty |
| `language` | `Čeština` | |
| `permissions` | 154 allow / 28 deny / 0 ask, `defaultMode: auto` | 154 ručně odklikaných povolení je doklad, že allowlist se buduje postupně |
| `worktree` | `bgIsolation: none` | Background joby pracují v working tree, ne v izolovaném worktree |
| `statusLine` | `node <dist>/ccstatusline.js`, `refreshInterval` | Volá se node přímo, ne přes `npx` — viz paměť o statusline leaku |
| `enabledPlugins` | superpowers, knowledge-loop, spec-factory, frontend-design + další | Mix oficiálních a vlastních |
| `extraKnownMarketplaces` | `kvados-plugins` → GitLab | Vlastní marketplace jako git repozitář |
| `skipDangerousModePermissionPrompt`, `skipAutoPermissionPrompt` | `true` | |

#### Projektová nastavení (alzask i fhb, identická)

`permissions.deny`: `Bash(rm *)`, `Bash(git push*)`, `Bash(git reset --hard*)`

Tři zákazy na úrovni projektu jsou mechanická pojistka proti tomu, aby agent smazal soubory,
pushnul nebo zahodil rozpracovanou práci. To je přenositelná zásada v čisté podobě: nebezpečná
operace se nezakazuje větou v `CLAUDE.md`, ale položkou v `deny`.

---

# Část 6 — Struktura dvou pracovních projektů (2026-09-10)

Odečteno skriptem `_raw/merit-projekty.py` přímo ze souborů na disku 10. 9. 2026.
Podklad pro 2. sezení (`PROGRAM-02.md`) a pro deck `claude-code-struktura-a-zdroje.html`.

> ⚠ **Čísla v částech 1–5 jsou z 26. 8. a část z nich už neplatí.** Projekty se mezitím změnily.
> Kde se hodnoty rozcházejí, platí tato část.

### 6.1 Adresáře `docs/`

| | alzask | fhb |
|---|---:|---:|
| podadresářů `docs/` | 16 | 12 |
| **společných** | **9** | **9** |

Společné: `adr`, `analysis`, `api`, `fr`, `meetings`, `onboarding`, `pbs`, `spec`, `spec-grounding`.
Jen alzask: `bp-overview`, `export`, `external-sources`, `ontology`, `plc`, `suppliers`, `tools`.
Jen fhb: `communications`, `feedback`, `superpowers`.

Kostra je stejná, přestože ji nikdo neopisoval a jde o jiné zákazníky i jiné domény.

### 6.2 Výbava v `.claude/`

| | alzask | fhb |
|---|---|---|
| agenti | 5 revizních (návrh, sémantika, struktura, report, oprava) | 7 na psaní specifikace (záměr, plán, autor, kritik, red team, rešerše, syntéza) |
| příkazy | 7 | 5 |
| hooky | `guard-myfaber.py` + testy | `spec-guard.py` |
| skilly | 2 (registr prvků, dotazy na dodavatele) | 1 |
| styl výstupu | Feynman CZ | — |
| validátory v `docs/` | 4 (`.adr-tools`, `.fr-tools`, `.ontology-tools`, `.plc-tools`) | 2 (`.adr-tools`, `.fr-tools`) |

Dvě různé odpovědi na dvě různé bolesti: u alzask je problém **dohledat, co platí**, u fhb **napsat to tak, aby to obstálo**.

### 6.3 Sdílená pravidla a jejich průnik

| | počet | znaků |
|---|---:|---:|
| alzask `rules/shared/` | **18** | 50 367 |
| fhb `rules/shared/` | **13** | 25 581 |
| **průnik** | **10** | — |

**Společných 10:** `RULE-AP-001` antipatterny · `RULE-AP-002` pokrytí ze zdroje · `RULE-CL-001` changelog ·
`RULE-DIAG-001` diagramy · `RULE-GOV-001` hranice a promoce · `RULE-GOV-002` brána místo promptu ·
`RULE-META-001` metadata · `RULE-SPEC-001` trasování akceptace · `RULE-SPEC-002` kritik cizího výstupu ·
`RULE-TERM-001` terminologie.

**Jen alzask (8):** `RULE-ONT-001`, `-002`, `-003` (registr prvků), `RULE-DOC-001`, `RULE-GOV-003`,
`RULE-SIM-001`, `RULE-SPEC-004`, `RULE-TC-001`.
**Jen fhb (3):** `RULE-API-002`, `-003`, `-005`.

To je doložený tvar zásady „kostra cestuje, výbava zůstává doma".

### 6.4 Co se načte při startu session

| alzask | znaků |
|---|---:|
| `CLAUDE.md` | 11 884 |
| `MEMORY.md` (paměť projektu) | 3 345 |
| styl výstupu | 4 685 |
| **celkem při startu** | **19 914** |

**Pravidla se při startu nenačtou.** Všech 18 souborů v `alzask/.claude/rules/shared/` má ve frontmatteru
`paths:`, takže se načítají teprve tehdy, když Claude sáhne na pasující soubor. U fhb je to 13 ze 13.
Kdyby cestu neměla, přidala by 50 367 znaků ke každému startu — víc než dvojnásobek.

> **Korekce prvního sezení.** Deck dílu 1, slide 15 říká „`CLAUDE.md` a `rules/` jdou do okna pokaždé".
> Přesná formulace zní: **pravidlo bez uvedené cesty jde do okna vždy, pravidlo s cestou až na vyžádání.**
> V obou mých projektech mají cestu všechna. Zdroj chování: code.claude.com/docs/en/memory, oddíl o pravidlech
> vázaných na cesty (ověřeno 10. 9. 2026).

### 6.5 Registr prvků projektu alzask

| | hodnota |
|---|---|
| prvků | **176** — 48 fyzických, 48 logických, 61 číselníků, 19 aktérů |
| vazeb | **354** |
| atributů | **703** |
| zapsaných rozporů | **97** |
| karet prvků | 176 (+ 174 souborů poznámek) |

| soubor | velikost | řádků | jak se používá |
|---|---:|---:|---|
| `INDEX.md` | 32 kB | 192 | čte se celý |
| `TERMS.tsv` | 183 kB | 2 585 | hledá se v něm |
| `RELATIONS.tsv` | 33 kB | 711 | hledá se v něm |
| `conflicts.md` | 349 kB | 4 713 | otevírá se jen u sporu |
| `coverage.md` | 279 kB | 1 719 | pokrytí zdrojů |
| `anchors.tsv` | 170 kB | 1 228 | jen pro nástroj |
| `ontology.yaml` | **1,7 MB** | 10 108 | **zdroj pravdy, nikdy se nečte celý** |

Nástroje v `.ontology-tools/`: `build.py`, `cite.py`, `reanchor.py`, `anchors.py`, `audit.py`,
`fix.py`, `render_md.py`, `render_html.py`, `session-check.py` (+ `build.cmd`).

### 6.6 Sedm vrstev autority

Z `docs/ontology/conflicts.md`, oddíl „Jak se rozpor rozhoduje". Rozhoduje **vrstva zdroje**, ne přesvědčivost
formulace ani počet výskytů.

| Vrstva | Co to je |
|---|---|
| 1a | konfigurace nasazení a datový model — co systém opravdu má |
| 1b | *popis* datového modelu; ve sporu s 1a **prohrává** |
| 2 | schéma rozhraní |
| 3 | přijatá rozhodnutí (ADR) |
| 4 | požadavky (FR) |
| 5 | řídicí systém a seznamy fyzických prvků; u fyzických prvků předbíhá vrstvu 4 |
| 6 | procesní analýza, posouzení rizik, zápisy z jednání, onboarding |

Doplňující zásada odtamtud: **vstupní dokument se needituje.** Procesní analýza, posouzení rizik a podepsané
verze jsou záznam — nález jde do soupisu rozporů, ne do nich.

### 6.7 Kotvy citací: kolik hlášení je šum

Z `RULE-ONT-003_kotvy-tri-tridy.md`, měření nad registrem **26. 8. 2026**: kotva je otisk okna ±2 až ±6 řádků
kolem citace, takže ji shodí i odstavec vložený *vedle* citovaného místa. **Z 15 hlášení bylo 9 tento případ,
tedy šum**, a jen 6 skutečných rozhodnutí.

Pravidlo se kvůli tomu přepsalo: dřív šla člověku všechna hlášení, dnes mechanické případy opraví nástroj
se stopou v úpravě a člověku zbyde jen nerozhodnutelný případ. Doklad, že se pravidlo mění měřením, ne názorem.

Verdikty ověření citace: `OK` · `POSUN` · `POSUN TEXTU` · `ZMIZELA`.

### 6.8 Co se od 26. 8. posunulo

| Údaj | Část 3 a 4 (26. 8.) | Část 6 (10. 9.) |
|---|---|---|
| `CLAUDE.md` alzask | 23 818 znaků | **11 884** |
| sdílených pravidel alzask | 15 | **18** |
| název `RULE-ONT-003` | `_zmizela-resi-clovek` | `_kotvy-tri-tridy` |

Instrukční soubor se zkrátil na polovinu, pravidel přibylo a jedno se přejmenovalo, protože se změnilo jeho
zadání. **Kdo cituje čísla z části 3, cituje srpen.** Sama tahle tabulka je použitelný doklad: dokumentace
o vlastní práci zastarává stejně rychle jako dokumentace o systému.

---

# Část 7 — Osm druhů dokumentů projektu alzask (2026-09-11)

**Metoda.** Odečteno přímo ze souborů v `C:\Git\alzask` 11. 9. 2026. Kontrolní skript
`_raw/overit-deck-02.py` srovnává každé číslo níže s tím, co je napsané na snímcích
decku 2. sezení — spouštět před sezením znovu, projekt žije.

**Proč tahle část vznikla.** Vlastník po revizi rozhodl, že deck 2. sezení je od snímku 3
příliš podrobný, a zadal osm témat po dvou snímcích: **proč ta věc vznikla** a **jaký má
princip**. Čísla níže jsou to, co ty snímky nesou.

## 7.1 Rejstříky a orientační soubory

| Údaj | Hodnota |
|---|---|
| ADR celkem | 54 |
| z toho aktivních / navržených / override | 28 / 25 / 1 |
| kategorie `process` / `api` / `hw` / `db` / `integration` | 20 / 16 / 10 / 4 / 3 |
| souborů `INDEX.md` v `docs/adr/` | 7 (souhrn + 6 kategorií) |
| zápisů v `docs/meetings/` | 66 |

Pravidlo, které tu hranici drží: `.claude/rules/shared/RULE-DOC-001_orientacni-soubory.md`.
Rozděluje tři soubory podle **adresáta a okamžiku načtení** — README čte člověk na vyžádání,
INDEX je registr s ID a stavem (**práh zhruba >10 položek**), `CLAUDE.md` se načítá automaticky,
a proto se za jeho obsah platí kontextem v každé session. Pravidlo výslovně zakazuje psát
do `CLAUDE.md` adresářové stromy a výčty souborů: *„to si čtenář zjistí levněji `ls`em
a stárne to při každé změně struktury."*

## 7.2 Funkční požadavky a testovací scénáře

| Údaj | Hodnota |
|---|---|
| souborů `FR-*.md` | 52 |
| souborů `*.feature` v `docs/fr/**/tc/` | 109 |
| scénářů v `docs/fr/tc-list.csv` | 946 |
| z toho unikátních testovacích případů | 108 |
| klasifikace positive / negative / edge-case | 529 / 409 / 8 |
| typ behavior / contract / boundary | 336 / 326 / 281 |
| stav done / draft | 862 / 84 |

Tvary ID podle `docs/fr/README.md`: `FR-COMP-WES-{oblast}-{seq}` (1.1.x), `FR-COMP-API-…` (1.2.x),
`FR-COMP-UI-…` (1.3.x), `FR-BP-{oblast}-{seq}` (2.x). Kanonické ID scénáře je `{TC-ID}.S{NN}`.

Konvenci scénářů drží `RULE-TC-001_tc-konvence.md`. Dvě věty, které stojí za citování doslova:
`@S{NN}` se **NIKDY** nepřečíslovává ani nerecykluje (smazaný scénář nechá mezeru a poznámku
`# Retired: …`), a kroky popisují **doménovou akci**, ne názvy služeb — aby scénáře přežily
přejmenování v kódu. Důvod uvedený v pravidle: stabilní `@S` drží dohledatelnost
FR → TC → C# test napříč refaktoringy.

## 7.3 Registr dotazů na dodavatele

| Údaj | Hodnota |
|---|---|
| otázek celkem | 152 |
| bullseye / bluesword | 126 / 26 |
| Answered / Partially / No answer / Declined | 58 / 52 / 32 / 10 |
| s vyplněným `landed_in` | 61 |

`landed_in` je `soubor:řádek`, kde je odpověď zapsaná ve specifikaci. **Bez něj je registr
jen hezčí mailbox** — tohle je to nejpřenositelnější z celého bloku.

Zdroj pravdy je `questions.yaml`; `OTEVRENE.md`, `QUESTIONS.tsv` i `questions-view.html`
jsou generované a needitují se. Identifikátory `PRE-*` / `MEZ-*` / `PORT-*` a číselník stavů
jsou převzaté z komunikačního registru dodavatele a **záměrně se nepřejmenovávají** — odkazuje
na ně dodavatel ve svých odpovědích (`docs/suppliers/README.md`).

## 7.4 Skilly, příkazy, agenti, pluginy

| Údaj | alzask | fhb |
|---|---|---|
| skillů v `.claude/skills/` | 2 | 1 |
| příkazů v `.claude/commands/` | 9 | — |
| agentů v `.claude/agents/` | 5 | 7 (`spec-*`) |

Skill `ontologie-prvku-alzask` je **generovaný** z `ontology.yaml` — hlavička souboru to říká
(`GENEROVANO — needituj`, `generated_from: ontology.yaml@…`). Sedmice agentů v fhb je tatáž,
kterou balí plugin `spec-factory` 1.9.0 z marketplace `kvados-plugins`
(`~/.claude/plugins/installed_plugins.json`).

**Doklad z oficiální dokumentace** ([code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills),
ověřeno 11. 9. 2026), doslovně: *„In a regular session, skill descriptions are loaded into context
so Claude knows what's available, but full skill content only loads when invoked."* a *„The
`description` helps Claude decide when to load the skill automatically."* Z toho plyne věta
pro publikum: **popis je jediné, co model vidí předem** — špatný popis znamená skill,
který se nikdy nespustí.

## 7.5 Drobná korekce části 6.5

`RELATIONS.tsv` má 32 504 B, tedy **33 kB**, ne 32 kB. Zaokrouhlení, ne změna souboru.
Ostatní velikosti registru sedí: `INDEX.md` 32 kB, `TERMS.tsv` 183 kB, `conflicts.md` 349 kB,
`ontology.yaml` 1,7 MB. Počítá se **kB = 1000 B**; kdo použije 1024, dostane 179 a 341
a bude se zbytečně divit.
