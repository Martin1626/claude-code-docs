# Statistiky z history.jsonl — ověřený podklad

Zdroj: `C:/Users/ai_martint/.claude/history.jsonl`, odečteno 2026-08-26 08:55.
Jeden řádek = jeden prompt zadaný člověkem. Normalizace cesty: lowercase + zpětná lomítka na dopředná (cesty v souboru mají nekonzistentní velikost písmen).

## Základní rozsah

| Celek | Promptů | Období |
|---|---|---|
| Celá historie (všechny projekty) | 2671 | 2026-01-19 → 2026-08-26 |
| Jen pracovní projekty (v rozsahu) | 1508 | 2026-01-29 → 2026-08-26 |

> **Pozor na dvě sady čísel.** Většina statistik níže je uvedena dvakrát — pro celou historii a jen pro pracovní projekty. Rozdíl je podstatný (např. `/compact` 67× vs. 51×) a záměna vede k nesprávně atribuovanému tvrzení.

## Prompty per projekt (pracovní projekty)

| Projekt | Promptů | % z pracovních |
|---|---|---|
| `c:/git/alzask` | 1139 | 75.5 % |
| `c:/git/fhb` | 212 | 14.1 % |
| `c:/git/shared/plugins/spec-factory` | 137 | 9.1 % |
| `c:/git/shared` | 14 | 0.9 % |
| `c:/git/myfaber` | 6 | 0.4 % |
| **Celkem** | **1508** | **100 %** |

## Prompty per měsíc

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

## Slash commandy

### Vestavěné — vypovídají o praxi řízení kontextu a modelu

| Příkaz | Celá historie | Pracovní projekty | Co to říká |
|---|---|---|---|
| `/compact` | 67× | 51× | tolikrát mi kontext došel a musel se destruktivně shrnout |
| `/model` | 63× | 53× | tolikrát jsem přepínal model — volba modelu je vědomá operace, ne nastavení jednou navždy |
| `/resume` | 58× | 33× | tolikrát jsem se vracel do staré session místo psaní nové |
| `/context` | 42× | 37× | tolikrát jsem si šel ručně zkontrolovat zaplnění okna |
| `/effort` | 9× | 4× | reasoning effort přepínám řádově méně často než model |
| `/clear` | 6× | 1× | čistý reset s předáním — proti 51 kompaktacím prakticky nepoužívaný |

**Klíčový poměr:** `/compact` 51× proti `/clear` 1× v pracovních projektech. Kontext jsem nechával dojet do kompaktace místo řízeného resetu s předáním.

### Vlastní commandy a skilly

| Příkaz | Celá historie | Pracovní projekty |
|---|---|---|
| `/body-z-jednani` | 34× | 33× |
| `/spec` | 22× | 21× |
| `/spec-factory:spec` | 6× | 4× |
| `/btw` | 8× | 7× |
| `/dodavatele:mail` | 4× | 4× |
| `/dodavatele:stav` | 3× | 3× |
| `/pruzkum` | 5× | 4× |

### Kompletní pořadí (pracovní projekty, vše nad 2×)

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

## Délka promptu

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

### Histogram (pracovní projekty)

| Pásmo (znaků) | Promptů | % | Co to typicky je |
|---|---|---|---|
| 0–50 | 652 | 43.2 % | jednoslovné dodatky, potvrzení, slash commandy |
| 50–100 | 269 | 17.8 % | krátký dodatek v rozjeté konverzaci |
| 100–250 | 346 | 22.9 % | jedna konkrétní otázka nebo úkol |
| 250–500 | 139 | 9.2 % | úkol s kontextem |
| 500–1000 | 71 | 4.7 % | úkol s kontextem a omezeními |
| 1000+ | 31 | 2.1 % | strukturované zadání — kontext, úkol, omezení, formát výstupu |

**Napětí, které stojí za pozornost:** medián 66 znaků, ale 31 promptů nad 1000 znaků (celá historie: medián 75, 44 nad 1000). Zadávání má dva režimy: velké strukturované zadání na začátku úlohy a pak desítky krátkých dodatků. Ty krátké dodatky jsou levné na napsání, ale každý z nich přeposílá celou historii znovu.

## Nejdelší prompty (pracovní projekty, nad 1000 znaků)

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

## Sessions a vložený obsah

| Projekt | Sessions | Promptů | Promptů na session |
|---|---|---|---|
| alzask | 176 | 1139 | 6.5 |
| fhb | 39 | 212 | 5.4 |
| spec-factory | 19 | 137 | 7.2 |
| shared | 6 | 14 | 2.3 |
| myfaber | 2 | 6 | 3.0 |

Promptů s vloženým obsahem (`pastedContents`): **29** z 1508.
Velikost vloženého obsahu ve znacích: medián 67, maximum 1876.

## Poznámka k reprodukovatelnosti

Když jsem tato čísla měřil, historie mezi dvěma běhy povyrostla o 4 prompty — o moje vlastní prompty z toho měření. `history.jsonl` je soubor, který roste s každým zadáním. Je to drobnost, ale dobře ilustruje, že „paměť" Claude Code je soubor na disku, ne vlastnost modelu.

