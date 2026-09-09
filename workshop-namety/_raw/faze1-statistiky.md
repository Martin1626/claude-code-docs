# PART B — Statistiky z history.jsonl

**Soubor:** C:/Users/ai_martint/.claude/history.jsonl
**Zpracováno:** 1507 promptů (z 2670 řádků)
**Období:** 2026-01 až 2026-08

## Per projekt

| Projekt | Počet | % |
|---------|-------|----|
| alzask | 1138 | 75.5% |
| fhb | 212 | 14.1% |
| myfaber | 6 | 0.4% |
| shared | 14 | 0.9% |
| spec-factory | 137 | 9.1% |
| **CELKEM** | **1507** | **100%** |

**KONTROLA:** Očekáváno (alzask 1134, fhb 212, myfaber 6, shared 14, spec-factory 137) = 1503; aktuálně = 1507 (diff: 4).

## Per měsíc

| Měsíc | Celkem | alzask | fhb | myfaber | shared | spec-factory |
|-------|--------|--------|-----|---------|--------|---------------|
| 2026-01 | 7 | 7 | 0 | 0 | 0 | 0 |
| 2026-02 | 8 | 7 | 0 | 1 | 0 | 0 |
| 2026-03 | 3 | 0 | 3 | 0 | 0 | 0 |
| 2026-04 | 7 | 0 | 7 | 0 | 0 | 0 |
| 2026-06 | 357 | 235 | 117 | 5 | 0 | 0 |
| 2026-07 | 628 | 432 | 58 | 0 | 1 | 137 |
| 2026-08 | 497 | 457 | 27 | 0 | 13 | 0 |

## Slash commands (top 15)

| Příkaz | Počet |
|--------|-------|
| /model | 53 |
| /compact | 51 |
| /context | 37 |
| /resume | 33 |
| /body-z-jednani | 33 |
| /rename | 29 |
| /plugins | 27 |
| /spec | 20 |
| /reload-plugins | 12 |
| /status | 10 |
| /config | 8 |
| /plugin | 8 |
| /btw | 7 |
| /new | 5 |
| /exit | 5 |

## Distribuce délek promptů

| Metrika | Hodnota |
|---------|----------|
| Minimum | 1 znaků |
| P25 | 15 znaků |
| Medián | 65 znaků |
| P75 | 166 znaků |
| P90 | 365 znaků |
| P99 | 1775 znaků |
| Maximum | 7213 znaků |

### Histogram

| Rozpětí | Počet | % |
|---------|-------|----|
| 0-50 | 652 | 43.3% |
| 50-100 | 269 | 17.9% |
| 100-250 | 345 | 22.9% |
| 250-500 | 139 | 9.2% |
| 500-1000 | 71 | 4.7% |
| 1000+ | 31 | 2.1% |

## Prompty nad 1000 znaků

**Celkem:** 31

| Datum | Délka | Text (prvních 100 znaků) |
|-------|-------|-------------------------|
| 2026-06-19 21:57 | 1775 | /spec Kolegyně, kterou nemám příliš v oblibě, mi poslala připomínky k diagramu   @docs/api/Diagrams- |
| 2026-06-19 22:04 | 1821 | /spec Kolegyně, kterou nemám příliš v oblibě, mi poslala připomínky k diagramu     @docs/api/Diagram |
| 2026-06-19 23:48 | 1821 | /spec Kolegyně, kterou nemám příliš v oblibě, mi poslala připomínky k diagramu     @docs/api/Diagram |
| 2026-06-19 23:51 | 1879 | /spec Kolegyně, kterou nemám příliš v oblibě, mi poslala připomínky k diagramu       @docs/api/Diagr |
| 2026-06-22 09:11 | 1004 | Myslím, že tuto situaci mu budeme muset řešit jako výjimku. Pokud se nepletu tak můžou nastat 2 situ |
| 2026-06-26 21:24 | 6240 | Na základě závěrů schůzky @docs/meetings/2026-06-26_06-26_FHB_Sjednocení_terminologie_a_procesy_dopr |
| 2026-06-29 20:38 | 1535 |   Architektura zastavení a PLC                                                                       |
| 2026-07-05 13:16 | 1384 | Proveď kompletní audit pluginu spec-factory.  ROZSAH: celý plugin — agenti, orchestrátor (commands/s |
| 2026-07-09 21:54 | 2106 | Zapracuj odpovědi požadované v @docs/plc/BACKLOG.md  1. Kdo dodává bezpečnostní a řídicí prvky portů |
| 2026-07-11 12:53 | 1598 | Signalizace majáku, které jsou u portů, jsou pro operátora. Musí tedy odpovídat této konvenci.    9. |
| 2026-07-12 15:17 | 1679 | Prezentace Mým cílem je vytvořit přehlednou intuitivní prezentaci, jack funguje Claude Code. Nyní ch |
| 2026-07-12 16:47 | 1611 | Dokuemnty @docs/plc/AlzaSk-PLC-specifikace.md a @docs/plc/AlzaSk-PLC-specifikace-mezanin.md jsou obs |
| 2026-07-13 20:47 | 1875 | Připrav html stránku, která bude demonstrovat pohyb palet po dopravníku. jedná se o dopravník s 10 p |
| 2026-07-13 20:48 | 1886 | Připrav html stránku, která bude demonstrovat pohyb palet po dopravníku. jedná se o dopravník s 10 p |
| 2026-07-13 21:47 | 1767 | Nosiče přijíždějí z pravé strany jsou odebírané z levé strany.    Simulace musí umožnit z levé stran |
| 2026-07-30 09:21 | 1049 | Proveď následující úpravy v @docs/api/API-myFABER-WES-AlzaSk.yml a v @docs/api/Diagrams-API-AlzaSk-v |
| 2026-08-04 19:48 | 2445 | Co se týká těch majáků tak tam došlo k nějakému nedorozumění. Ty věci se týkají 2 různých portů. V o |
| 2026-08-07 18:13 | 1012 | Při ochranném zaststavení by se muselo také sjednotit.  PAC na tom ještě nezačala pracovat. Je proto |
| 2026-08-10 19:43 | 1607 | Upozorňuji, že ERROR_PRE_RECEIPT_0_1_P01 je dopravníkový port na dopravníkové stanici ERROR_PRE_RECE |
| 2026-08-11 08:20 | 1211 | Proveď změnu ADR-ASK-API-011. Pořadí volání je nyní již platné. Rozšiř ADR-ASK-HW-005 , aŤ je to jas |
| 2026-08-12 13:48 | 1905 | Pomoz mi formulovat krátký, cílený dotaz na upřesnění konkrétního chování. Zatím BullsEye odpovídá p |
| 2026-08-14 19:36 | 3052 | Přečti tyto tři dokumenty ve složce C:\Git\fhb\docs\api\asrs-v2\ jako tři vrstvy popisu jedné a téže |
| 2026-08-14 20:13 | 3344 | Přečti tyto tři dokumenty ve složce C:\Git\fhb\docs\api\asrs-v2\ jako tři vrstvy popisu jedné a téže |
| 2026-08-14 20:29 | 5280 | Porovnej dvě vrstvy popisu jednoho API v repozitáři C:\Git\alzask:    TOK       docs\api\Diagrams-AP |
| 2026-08-18 15:13 | 1086 | Vytvoř pracovní markdown dokument který bude sloužit pro jako podklad k jednání s bullseye . Nejprve |
| 2026-08-19 11:21 | 2175 | Přelož do angličtiny tento text:  Zápis ze společného jednání KVADOS – BullsEye  Datum: 19. 8. 2026  |
| 2026-08-19 19:41 | 1216 | 1. Spusť docs/plc/.plc-tools/validate.cmd (nebo fr-tools/validate.py). Chyby lintru oprav hned, bez  |
| 2026-08-19 19:45 | 1216 | 1. Spusť docs/plc/.plc-tools/validate.cmd (nebo fr-tools/validate.py). Chyby lintru oprav hned, bez  |
| 2026-08-24 12:18 | 7213 | # PROMPT — Zpětné dorovnání nástrojů registru ze šablony pluginu (AlzaSk)  > **Jak to použít:** vlož |
| 2026-08-24 20:47 | 1371 | Formuluj v češtině následující otázky tak, aby jim dodavatel správně rozuměl.  Dotaz na BullsEye, ja |
| 2026-08-25 19:38 | 4502 | Naléhavě potřebuju propsat doložené odpovědi dodavatele BullsEye do PLC specifikací. Kontext: v před |

## PastedContents

| Metrika | Hodnota |
|---------|----------|
| Prompty s pastedContents | 29 |

## Unikátní sessions per projekt

| Projekt | Sessions |
|---------|----------|
| alzask | 176 |
| fhb | 39 |
| myfaber | 2 |
| shared | 6 |
| spec-factory | 19 |
