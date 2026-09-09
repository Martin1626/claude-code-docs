# FÁZE 2c — Destilace přenositelné praxe zadávání

**Zdroj:** `C:\tmp\workshop-namety\_raw\prompty-alzask-08.md` — 457 promptů, 2026-08-03 → 2026-08-26.
**Do analýzy vzato:** 451 promptů (vynecháno 6 promptů z 26. 8. dopoledne o přípravě workshopu).
**Pomocné skripty:** `an08.py`, `an08b.py` (tamtéž), výstupy `an08.out.txt`, `an08b.out.txt`.

**Legenda okruhů:** `K` kontext a grounding · `R` rozšíření · `M` mechanika kvality · `O` orchestrace ·
`A` analytické postupy · `U` učení · `X` antipatterny · `N` nastavení

**Legenda přenositelnosti:** `[P]` přenositelná praxe (kolega si odnese bez tvé infrastruktury) ·
`[I]` infra (funguje, ale někdo to musí pro tým postavit) · `[Z]` osobní zvyk / náhoda (neučit)

---

## 0. Kvantitativní kostra (kontext pro celý dokument)

| Metrika | Hodnota |
|---|---|
| Promptů celkem / v analýze | 457 / 451 |
| Slash příkazů | 77 (17 %) — `/compact` 19×, `/plugins` 11×, `/body-z-jednani` 8×, `/model` 6×, `/dodavatele:*` 7×, `/pruzkum` 2×, `/spec-factory:review-spec` 2× |
| **Mediánová délka promptu** | **106 znaků** |
| Promptů pod 100 znaků | 211 (47 %) |
| Promptů nad 1000 znaků | **14 (3 %)** |
| Zmínek subagenta | 37 |
| Explicitní read-only brána („zatím nic neměň") | 12 |
| Grounding výzva („odkud to pochází / kde to má oporu") | 13 |
| Prompt jako artefakt („připrav prompt, který…") | 10 |
| Reverzy vlastního rozhodnutí | 9 |
| Přeposlání téhož promptu podruhé/potřetí | 14 skupin / 29 promptů |

### Headline nález, který určuje tón celého workshopu

**Není tu jeden „správný dlouhý prompt". Jsou tu dva zcela odlišné režimy zadávání a rozdíl mezi
nimi je ta nejcennější věc, kterou si kolega může odnést:**

1. **Krátký dialogický režim (97 % promptů, medián 106 znaků).** Kontext nese repozitář a předchozí
   turn, ne prompt. Prompt je jedna věta: rozhodnutí, korekce, dotaz na doklad. Struktura
   „kontext → úkol → omezení → formát" v jednotlivém promptu **není** — je rozprostřená přes
   10–30 turnů. Funguje to, protože je pod tím ukotvená dokumentace a `CLAUDE.md`.
2. **Dlouhý strukturovaný režim (14 promptů, 1000–7200 znaků).** Používá se **jen ve třech
   situacích**: (a) předání práce do jiné session nebo jiného repozitáře, (b) vrstvový audit
   konzistence dokumentace, (c) dávkové promítnutí závěrů jednání. Tady struktura je, je pevná
   a dá se z ní udělat šablona (viz kandidát P06).

Pro workshop to znamená: neučit kolegy „psát dlouhé prompty". Učit je **poznat, kdy krátký nestačí**.

---

# ČÁST A — PŘENOSITELNÁ PRAXE

## P01 · Read-only brána v prvním promptu („zatím nic neměň") `[P]` — okruh `M`

**Co to je.** Zadání, které explicitně zakazuje zápis, dokud si člověk nepřečte návrh. Odděluje
fázi „zjisti a navrhni" od fáze „proveď".

**Doklad.**
- „Připrav mi podklady k tomu, abych mohl rozhodnout, co se má zobrazovat na HMI panelech. ZAtím
  nic neukládej, jen zjisti související informace a zeptej se mě na to, co potřebuješ vědět"
  — 2026-08-04 12:13
- „Načti si API a relevantní ADR, FR a TC. Připrav návrh, co je potřeba doplnit… **Zatím nic
  neměň, vyberu, co implementovat.** Pokud je něco nejasné, předem se mě zeptej." — 2026-08-17 15:10
- „Proveď `alzask-prompt-porty-aktivace-stanice.md`. **Nic needituj ani nevytvářej. Zatím piš jen
  do chatu.**" — 2026-08-19 21:38
- „Předpokládám, že kvůli NSwag tam tělo být musí, je to tak?… **Nic zatím neměň.**" — 2026-08-15 13:23

**Opakování.** 12× — jasný vzor, ne jednorázovka.

**Přenositelnost.** `[P]`. Nula infrastruktury. Je to jedna větička na konec promptu a je to
nejlevnější ochrana proti tomu, aby model „opravil" 40 souborů podle špatného pochopení.

**Předvedatelnost.** Vysoká. Naživo dvakrát totéž zadání — bez brány a s bránou — a porovnat
`git status`.

---

## P02 · Číslovaný picklist a odpověď čísly (s výjimkami inline) `[P]` (nástroj `[I]`) — okruh `A`

**Co to je.** Model vyrobí číslovaný seznam bodů/nálezů/změn; člověk odpoví **výčtem čísel**
a u jednotlivých čísel doplní odchylku jednou větou. Rozhodovací šířka pásma bez psaní prózy.

**Doklad.**
- „Implementuj a zkontroluj, že aktuální stav odpovídá závěrům bodů: 3, 4, 7, 8, 10, … 22,
  **23: nejedná se o BMW, ale WMS volá readyToClose**, **24: jedná se o výstupní port**, 28, 29…"
  — 2026-08-04 11:33
- „Zapracuj do dokumentací… tyto body: 1, 2, 3, 6, 7, **8: i u portu, kde se neřeší bezpečnost,
  bude zdroj pravdy v PLC**, … **18: tady byl zápis asi nepřesný. Platí to, co je aktuálně
  popsáno v PLC specifikaci**, 19, 22, 24, 26, 27, 28" — 2026-08-19 11:44
- „Má zahrnovat jen tyto body: 3, 4, 5, 6, 8, 12, 13, 14, 15, 16, 17, 20, 21, 22, 24, 25…"
  — 2026-08-19 10:01
- „Zapiš pouze A1, A2, A3, A4" — 2026-08-21 11:10 · „N1, N2, N4 přijmout před přenosem. N3
  zamítnout" — 2026-08-24 10:44 · „Q2, Q4, Q5, Q7, Q8, Q9, Q10, Q11, Q14, Q15, Q17, Q18
  nepotřebuji. Q19 — ponech jen otázku 1" — 2026-08-18 22:35

**Opakování.** Vzor. 8× přes `/body-z-jednani` + minimálně 10× ručně nad jinými seznamy
(ADR návrhy, nálezy revize, otázky na dodavatele).

**Přenositelnost.** **Rozdělit:** samotný **vzor je `[P]`** — stačí do promptu napsat „vypiš to
jako číslovaný seznam, ze kterého si vyberu". Skill `/body-z-jednani` je `[I]`, ale nutný není.

**Předvedatelnost.** Velmi vysoká, a je to nejvýživnější věc pro netechnického analytika. Naživo:
vzít přepis jednání, nechat vyrobit picklist, odpovědět „3, 7, 9: ale jen pro mezaniny".

---

## P03 · Uzavřené otázky s variantami a odpověď písmenem `[P]` — okruh `A`

**Co to je.** Model musí otevřené body předložit jako uzavřené otázky s variantami (a)/(b)/(c),
u každé varianty jednou větou důsledek, a označit doporučenou. Člověk odpovídá jedním znakem.

**Doklad.**
- Zadání: „Každá otázka: uzavřená, s variantami (a) / (b) / (c) — u každé varianty jednou větou,
  co se změní ve které vrstvě — označ doporučenou variantu a proč — **chci umět odpovědět
  písmenem**" — 2026-08-14 20:29
- Užití: „Varianta A, nakresli D8.2 a D8.4" — 2026-08-15 09:31 · „Varianta 2, uprav subagentem
  ADR i diagramy" — 2026-08-15 11:27 · „Udělej A." — 2026-08-17 21:07 · „Proveď A + C"
  — 2026-08-24 11:30 · „A) založ navrhovaná ADR. další změny zatím nedělej." — 2026-08-14 21:11

**Opakování.** Vzor — v zadání 2×, v odpovědích min. 8×.

**Přenositelnost.** `[P]`. Nezávisí na ničem. Přímý zásah proti nejčastější ztrátě času:
model se ptá otevřeně („jak to chcete?"), analytik odpovídá dlouze a nepřesně.

**Předvedatelnost.** Vysoká. Ukázat rozdíl mezi odpovědí na otevřenou a uzavřenou otázku
na stopkách.

---

## P04 · Rozpočet na otázky + nerovnoměrné rozdělení `[P]` — okruh `A`

**Co to je.** Zadání limituje počet otázek a zakazuje jejich rovnoměrné rozdělení mezi nálezy.

**Doklad.**
- „Otázek může být maximálně 5." — 2026-08-14 20:24 (holá verze)
- „OTÁZKY PRO MĚ — nejvýš 5 CELKEM za všechny tři nálezy. **Nerozděluj je rovnoměrně. Rozpočet
  utrať podle páky**: nález, který drží nejvíc navazujícího, si zaslouží dvě otázky, slabší jednu.
  Nález, u kterého je odpověď zřejmá z citací, otázku nepotřebuje vůbec." — 2026-08-14 20:29

**Opakování.** 2× (evoluce holého limitu na sofistikovanou verzi za 5 minut).

**Přenositelnost.** `[P]`. Bez limitu dostane analytik 20 otázek a neodpoví na žádnou.

**Předvedatelnost.** Vysoká — dvě spuštění téhož auditu, jednou bez limitu, jednou s limitem 5.

---

## P05 · „Páka" jako řadicí kritérium místo „co je nejasné" `[P]` — okruh `A`

**Co to je.** Nálezy se neřadí podle pořadí v dokumentu ani podle nejasnosti, ale podle toho,
kolik navazujících věcí jedna odpověď srovná.

**Doklad.** „Vytipuj 3 body s nejvyšší **pákou** — místa, kde jedno rozhodnutí ode mě srovná řadu
důsledků. Páka = kolik konkrétních věcí se změní podle toho, jak odpovím (schémata, endpointy,
enum hodnoty, povinná pole, stavové přechody, chybové kódy, kroky v diagramech, testovací
scénáře). **Ne „co je nejasné", ale „co drží nejvíc navazujícího".**" — 2026-08-14 20:29
(shodně 2026-08-14 19:36 a v zárodku 2026-08-14 13:38: „vytipuj 3 rozpory nebo informace, po
jejichž správném vyjasnění bys dokázal opravit řadu důležitých důsledků")

**Opakování.** 4× (13:38 → 15:53 → 17:04 „Vylepši tento prompt" → 19:36 → 20:29). Je to
nejlépe zdokumentovaná evoluce jednoho promptu v celém měsíci.

**Přenositelnost.** `[P]`. Přeložitelné na jakoukoli analytickou domény: „co drží nejvíc
navazujícího" je univerzální.

**Předvedatelnost.** Velmi vysoká — a rovnou jako ukázka **iterace promptu**: pustit verzi
z 13:38 a verzi z 20:29 nad stejnými soubory a porovnat výstup.

---

## P06 · Vrstvový audit dokumentace (KONCEPT / KONTRAKT / NÁVOD, resp. TOK / KONTRAKT) `[P]` — okruh `A` + `K`

**Co to je.** Nejsilnější jednotlivý artefakt měsíce. Prompt zadá modelu, aby **tytéž skutečnosti**
přečetl ve dvou nebo třech dokumentech, které je popisují na různých úrovních, a hledal rozpory
**na hranici mezi vrstvami**, ne uvnitř jedné.

**Doklad — kostra (zkráceno; plná verze 2026-08-14 19:36 = 3052 zn., 2026-08-14 20:29 = 5280 zn.):**

```
1  ROLE SOUBORŮ      KONCEPT  ...-koncept.md  — záměr: co a proč to má dělat
                     KONTRAKT ...-v2.yaml     — tvar dat: co skutečně projde
                     NÁVOD    ...-README.md   — jak to má druhá strana použít
2  JAK ČÍST          „Čti je celé, včetně poznámek pod sekcemi, otevřených otázek, TODO a
                     odstavců typu 'k dořešení s implementací' — právě tam bývá věta,
                     která ruší platnost mechanismu popsaného nad ní."
3  CO NEČÍST         + důvod u každé položky (viz P07)
4  ROZHODČÍ          ADR / INDEX + heuristika zralosti (viz P08)
5  CO HLEDAT         taxonomie nálezů A–E (resp. A–H) — pojmenované kategorie rozporu
6  ÚKOL              3 body s nejvyšší pákou (viz P05)
7  VÝSTUP / NÁLEZ    kategorie · stav ve VŠECH vrstvách (citace `soubor:řádek` NEBO „mlčí")
                     · verdikt rozhodčího · jmenovitý výčet dotčených míst
8  OTÁZKY            rozpočet 5, uzavřené, (a)/(b)/(c), doporučená varianta (viz P03, P04)
9  PRAVIDLA          nic z paměti · pravidlo ≠ instance · nesahej na soubory ·
                     řaď podle páky · přebytek nad 3 vypiš jednořádkově, ať nezmizí
```

**Opakování.** 2 plné instance + 3 předchůdci. V rámci měsíce vznikl jako **produkt iterace**,
ne jednorázově.

**Přenositelnost.** `[P]`, a to je klíčové: prompt sám nepotřebuje žádný plugin ani validátor.
Potřebuje jen to, že v projektu **existují dva dokumenty popisující totéž na jiné úrovni** —
což je v analytickém projektu vždycky (procesní analýza vs. API spec, FR vs. TC, ADR vs. diagram).

**Předvedatelnost.** Nejvyšší v celém dokumentu. Doporučuji jako **centrální ukázku workshopu**:
předhodit kolegům jejich vlastní dvojici dokumentů a nechat prompt běžet naživo.

---

## P07 · Negativní kontext: „CO NEČÍST" s důvodem u každé položky `[P]` — okruh `K`

**Co to je.** Vyjmenování souborů, které model **nemá** čtít, a u každého věcný důvod. Bez toho
model najde „rozpory" proti zmraženému baseline nebo staré verzi a analytik triážuje šum.

**Doklad.**
```
CO NEČÍST
  docs\api\temp\**                    — zakázaná složka (viz CLAUDE.md)
  docs\api\ARCHITECTURE_DECISIONS.md  — mimo rozsah
  docs\api\Diagrams-API-AlzaSk.md     — starší verze, ne platný stav
  docs\api\podepsaná-verze\**         — zmražený baseline z 2026-01-30; rozdíl proti
                                        němu NENÍ nález, je to vývoj.
Platný stav je výhradně v3 + aktuální YAML.
```
— 2026-08-14 20:29. Obdobně „Složku snapshots/ ignoruj — jsou to starší verze, ne platný stav;
sáhni tam jen když potřebuješ doložit, kdy se něco změnilo." — 2026-08-14 19:36.

Motivace je doložená i mimo tyto prompty: „Máme v claude.md podchyceno pravidlo, že se nemají
běžně využívat informace ze složek temp, tmp nebo spec, pokud to není explicitně vyžádáno?
Jak to lépe specifikovat?" — 2026-08-19 09:00.

**Opakování.** 2× v plné podobě + systémový projev v `CLAUDE.md`.

**Přenositelnost.** `[P]`. „Rozdíl proti zmraženému baseline není nález" je věta, kterou si
kolega odnese a použije na svůj repozitář hned.

**Předvedatelnost.** Střední-vysoká: ukázat audit bez negativního seznamu (šum ze starých verzí)
a s ním.

---

## P08 · Vrstva „ROZHODČÍ" — než se zeptáš, zjisti, jestli to není rozhodnuté `[P]` — okruh `K`

**Co to je.** Prompt dá modelu **hierarchii autority** a heuristiku zralosti. Nález proti
rozhodnutí není otázka, ale porušení — a to se hlásí jinak.

**Doklad.**
- „**ROZHODČÍ** — než položíš otázku, ověř, zda věc už není rozhodnutá: `docs\adr\INDEX.md` →
  `docs\adr\**` … `docs\fr\comp\api\**\tc\*.feature` — testovací scénáře; **existence TC je
  signál, že chování je dotažené, jeho absence u bohatě rozepsané pasáže signál opačný**"
  — 2026-08-14 20:29
- „Verdikt rozhodčího: je to už rozhodnuté v některém ADR? Pokud ano, **není to otázka pro mě,
  ale nesoulad s rozhodnutím** — označ, která vrstva ho porušuje, a rovnou to napiš." — tamtéž
- „Jako rozhodčí měj po ruce `ADR-ASRS-API-001-design-decisions.md`." — 2026-08-14 19:36

**Opakování.** 2×, ale koncepčně to prostupuje celý měsíc (13 grounding výzev, viz P09).

**Přenositelnost.** `[P]` s výhradou: aby to fungovalo, musí existovat **nějaká** evidence
rozhodnutí. Kdo nemá ADR, nasadí místo toho zápisy z jednání nebo changelog. Podstata („dej
modelu zdroj autority a rozliš otázku od porušení") je přenositelná bez čehokoli.

**Předvedatelnost.** Střední. Nejlépe jako slide, ne live demo.

---

## P09 · Grounding výzva: „Odkud to pochází? Kde to má oporu? Kdo a kdy to změnil?" `[P]` — okruh `K` + `X`

**Co to je.** Když model něco tvrdí, analytik místo přijetí nebo hádky **žádá provenienci**.
Řetězec dotazů zužuje: co přesně tvrdíš → máme to podložené dřív než v této session → kdo to změnil.

**Doklad — nejlepší uzavřený příběh měsíce (5 promptů, 27 minut):**
1. „Odkud pochází tvrzení, že Alza nebude posílat readyToClose u vstupního dopravníku
   předpříjmu?" — 2026-08-07 16:48
2. „Mi se jedná ale o tvrzení „svítí" nebo „bliká". Co je správně?" — 16:55
3. „Jedná se mi o to, **zda máme někde dříve než v této session podloženou informaci**, zda HW
   tlačítko RESET má svítit nebo blikat?" — 16:57
4. „**Zjisti, kdo a kdy to měnil z bliká na svítí.**" — 17:01
5. „Chci proto ponechat tvrzení, že tlačítko bliká. **Zruš provedené změny na „svítí".**" — 17:15

**Další doklady.** „Skutečně platí, že na západních portech AGV zóny… WMS volá readyToClose?
**Kde to má oporu? Je tato kontrola nezbytná? Tvrdilo se to na nějakém jednání?** Nech toto
prověřit subagenta." — 2026-08-09 20:44 · „Proč na Expedici sever se neposílá readyToClose?
**Jak jsi na to přišel?**" — 2026-08-05 17:50 · „**Odkud máš informaci**, že událost se posílá
už po vyložení na vstupní pozici dopravníku?" — 2026-08-14 08:56 · „Kde vzniklo tvrzení, že na
vstupních portech v mezaninu má Alza volat readyToClose? **Dává to v celkovém kontextu smysl?**"
— 2026-08-09 20:28

**Opakování.** 13× — silný vzor.

**Přenositelnost.** `[P]`, nejsilnější kandidát celého okruhu `K`. Nepotřebuje nic než Git
a dokumentaci. Je to zároveň **jádro analytické práce s LLM**: model dokáže vyrobit plausibilní
tvrzení a udržet ho napříč deseti soubory; jediná obrana je dotaz na provenienci.

**Předvedatelnost.** Nejvyšší. Nechat model tvrdit něco o vlastní dokumentaci a naživo mu
položit „odkud to pochází" — a ukázat, jak často odpovědí je „z předchozí odpovědi v této session".

---

## P10 · Zdrojová izolace: „jen z těchto dokumentů a nic ze specifikace" `[P]` — okruh `K`

**Co to je.** Zadání zakáže mísit dodavatelské tvrzení s vlastní specifikací. Vzniká dokument,
o kterém se dá říct „to tvrdí dodavatel", ne „to si myslíme my".

**Doklad.** „Potřebuji, aby ve výsledném dokumentu byly uvedené **pouze informace obsažené v těch
dvou uvedených dokumentech a nic ze specifikace**. Chci mít čisté informace, které nám tvrdí náš
dodavatel. **U důležitých informací uváděj citace nebo odkazy na zdroje**, kde je možné si
informaci ověřit." — 2026-08-03 15:05

Doplňkově: „Přečti si celý dokument … Jakým způsobem WCS žádá WMS (WES) o inbound task? Jsou
popsané nějaké možnosti? **Nevymýšlej si.**" — 2026-08-18 10:54 · „Zajímá mě především vyjádření
BullsEye" — 2026-08-18 14:14

**Opakování.** Vzor napříč celou dodavatelskou linkou (55 promptů se dodavatelů týká).

**Přenositelnost.** `[P]`. Nula infrastruktury a okamžitá hodnota pro kohokoli, kdo pracuje
s dodavatelskou dokumentací.

**Předvedatelnost.** Vysoká: zpracovat týž PDF dvakrát — jednou bez izolace (model doplní, co
„obvykle bývá"), jednou s izolací.

---

## P11 · Hypotéza k vyvrácení místo otevřené otázky `[P]` — okruh `A`

**Co to je.** Analytik napíše **svůj model** a požádá o jeho zbourání, ne o vysvětlení. Modelu
tím dá co falzifikovat a sobě zpětnou vazbu na vlastní pochopení.

**Doklad.**
- „Možná by to mohlo fungovat i bez toho, aby WCS žádalo o povolení. WES totiž odešle vždy jen
  jeden nosič… **Uvažuji správně? Bude to fungovat i v hraničních situacích?**" — 2026-08-07 11:29
- „Je dobrý nápad rozlišit to blikáním RESET tlačítka? Tzn. … **Kde jsou slabá místa?**"
  — 2026-08-07 17:55
- „Jak by to vypadalo v tomto případě? **Kde může být kolize?**" — 2026-08-10 15:57
- „Sedí to s tvým poznáním?" — 2026-08-10 19:19 · „Chápeš to stejně?" — 2026-08-21 18:15
- „Potřebuji uvažovat a formulovat myšlenky jednoduše. Myslím, že potřebuji: … **Zapomněl jsem
  na něco stejně důležitého?**" — 2026-08-07 11:23
- „**Co je tedy nyní špatně a je potřeba upravit?**" — 2026-08-25 19:54
- „Na první pohled to vypadá logicky. Potřebuji ale aby ses nad tím **pořádně zamyslel, zda to
  nebude kolidovat v žádných situacích**. Potřebuji, aby to bylo spolehlivé a blbuvzdorné i pro
  obsluhu." — 2026-08-25 19:25 (vstupem je návrh kolegyně, ne vlastní)

**Opakování.** 12× — silný vzor a zdaleka nejlepší „analytický" pattern v materiálu.

**Přenositelnost.** `[P]`. Přenositelné beze zbytku a přeneseně použitelné i na návrh kolegy
(„předhoď to modelu jako cizí text s pokynem hledat kolize" — 2026-08-21 11:12, 2026-08-25 19:25).

**Předvedatelnost.** Velmi vysoká. Naživo: totéž téma jako otevřená otázka („jak má fungovat X?")
vs. jako hypotéza („myslím, že X funguje takto — kde jsou slabá místa?").

---

## P12 · Vyjednání terminologie **před** psaním `[P]` — okruh `A` + `K`

**Co to je.** Než se cokoli zapíše, sjednotí se slovník — a to explicitně, se zdůvodněním, a s
kontrolní otázkou zpět. Nejnákladnější chyby měsíce byly terminologické, ne obsahové.

**Doklad — tři samostatné epizody:**
- **error stanice vs. error větev** (3 prompty): „Pevný fakt je ten, že `ERROR_PRE_RECEIPT_0_1_P01`
  je dopravníkový port na dopravníkové stanici **bez ohledu na to, jak se jmenuje**. Není to error
  port na který by jezdil robot. To nelze. Je to dopravník. … **Platí Error stanice ≠ error větev
  dopravníku.** Oprav to všude, kde je potřeba." — 2026-08-10 19:31
- **odběrové místo → port** (2 prompty): „Pokud tedy odběrovým místem myslíme port, tak **jej
  pojmenovávej jako port**. Věta by pak měla znít, že nosiče čekají **před** odběrovým místem…
  Ne **za** odběrovým místem." — 2026-08-14 13:43 → „ano, sjednoť to na 'pozice portu' všude"
  — 2026-08-14 18:35
- **patro skladu vs. patro mezaninu** (3 prompty): „Nevím, zda si přesně rozumíme. Používej
  'patro skladu' a 'patro mezaninu'. Přitom například 3. patro skladu výškově odpovídá 1. patru
  mezaninu. … **Chápeš to stejně?**" — 2026-08-21 18:15

**Opakování.** 3 epizody × 2–3 prompty. Vzor.

**Přenositelnost.** `[P]`. Absolutně.

**Předvedatelnost.** Vysoká, a je to skvělý „aha" moment: ukázat, jak model bez sjednoceného
slovníku vyrobí správnou větu o špatném prvku.

---

## P13 · Neaváděj nový pojem — zjisti, který se už používá častěji `[P]` — okruh `A`

**Co to je.** Podmnožina P12, ale zaslouží si vlastní slot, protože je to praxe, kterou LLM
sám nikdy nenavrhne: model raději zavede čistý nový termín, než by měřil zvyk v repozitáři.

**Doklad.** „Co se používalo dosud častěji který pojem patro nebo podlaží. **Neměl jsem v úmyslu
zavádět nový pojem, raději bych použil ten, který se již nyní používal častěji.**"
— 2026-08-21 18:34

Tamtéž ve stejném promptu i tvrdá korekce faktu: „**Není pravda:** 'Nad automatizovaným paletovým
skladem (PS, 4D shuttle) stojí mezaninová nástavba se třemi patry.' Mezaniny stojí **vedle**
automatizovaného paletového skladu."

**Opakování.** 1× explicitně, ale je to pointa celé epizody P12/c.

**Přenositelnost.** `[P]`. „Změř zvyk, než zavedeš termín" je jednořádkové pravidlo do promptu.

**Předvedatelnost.** Vysoká a rychlá: `grep -c` obou variant a rozhodnutí podle čísel.

---

## P14 · Rozliš pravidlo od jeho instance `[P]` — okruh `K` + `X`

**Co to je.** Explicitní pravidlo v promptu proti nejtypičtější chybě modelu ve specifikaci:
z věty o jednom konkrétním zařízení udělá obecný rozpor.

**Doklad.** „**Rozlišuj pravidlo od jeho instance v konkrétním nasazení.** Věta o konkrétní
stanici, zařízení nebo identifikátoru platí jen tam, kde ten prvek existuje." — 2026-08-14 20:29
(v 19:36 v mírně jiné formulaci: „Věta o konkrétním zařízení, lokaci nebo identifikátoru… ověř to,
než z ní uděláš obecný rozpor.")

Reálný projev toho, co se stane bez tohoto pravidla — samostatná debata o typologii:
„A nebylo by tedy správnější zavést typy prvků například 'měřící brána řízená BullsEye' a 'měřící
brána řízená PAC'? **Nebo rozlišovat tím, zda údaje z tohoto zařízení jsou do WES přenášeny přes
REST nebo načítány z PLC?**" — 2026-08-21 15:25 (reakce na „dělba je určena místem, ne typem prvku")

**Opakování.** 2× v zadání, 1 samostatná odborná epizoda.

**Přenositelnost.** `[P]`. Jedna věta do promptu, obrovská úspora triáže.

**Předvedatelnost.** Střední. Lepší jako slide s konkrétním falešným nálezem.

---

## P15 · „Ticho jedné vrstvy je nález, ne absence nálezu" `[P]` — okruh `A`

**Co to je.** Kategorie nálezu, kterou model sám nikdy nevyprodukuje: dva dokumenty věc řeší,
třetí o ní neví. Bez pojmenování se to ve výstupu neobjeví.

**Doklad.** „**G) MLČENÍ JEDNÉ VRSTVY** — jedna vrstva věc řeší, druhá o ní neví. **Ticho je
nález, ne absence nálezu**; ověř, zda není záměrné." — 2026-08-14 20:29. A vynucení ve formátu
výstupu: „Stav v OBOU vrstvách — u každé buď citace `soubor:řádek` s doslovným úryvkem, **nebo
explicitně „mlčí". Vrstvu nikdy nevynech proto, že o věci nemluví.**"

Doplňkově kategorie „**H) NEDOURČENÍ** — chování je otevřené (TODO, otevřená otázka), ale druhá
vrstva na něm už staví jako na rozhodnutém."

**Opakování.** 2×.

**Přenositelnost.** `[P]`. Nejelegantnější jednotlivá myšlenka v celém materiálu a přenese se
na cokoli.

**Předvedatelnost.** Vysoká — dá se ukázat na jediném nálezu.

---

## P16 · Prompt jako artefakt (soubor), ne jako zpráva v chatu `[P]` — okruh `O` + `R`

**Co to je.** Zadání se nechá vyrobit, uloží se do souboru a session ho pak jen **provede**.
Řeší tři věci současně: přenos mezi session/repozitáři, opakovatelnost a ztrátu textu při vkládání.

**Doklad — výroba:**
- „**Připrav prompt, který mi pomůže s tímto:** Promysli, jak má WES správně řídit porty ovládané
  PLC… V čem stávající specifikace nevyhovuje? Jaké jsou příčiny současného nevyhovujícího stavu
  a zodpovězení kterých otázek by tyto příčiny dokázalo vyřešit?" — 2026-08-19 14:35
- „Zjistil jsem, že volání událostí v diagramech neodpovídá tomu, co je v … `.md`. **Připrav
  prompt, který provede komplexní kontrolu a připraví plán opravy.** Pokud bude potřeba ještě něco
  rozhodnout, tak se mě na to předem zeptá." — 2026-08-19 15:18
- „**Vylepši tento prompt a napiš do chatu:** …" — 2026-08-14 17:04
- „**Vytvoř nyní obdobný prompt pro:** `docs\api\Diagrams-API-AlzaSk-v3.md`, `…yml`" — 2026-08-14 20:15
- „**Připrav ale prompt, který spustím v jiném repu.**" — 2026-08-19 21:26 · „Pro změny v pluginech
  vytvoř pak samostatný prompt, abych jej mohl spustit ve správném repu." — 2026-08-24 10:44
- „**Napiš prompt pro novou session**, co je potřeba nejnaléhavěji dodělat" — 2026-08-25 19:29

**Doklad — provedení:** „Proveď prompt `C:\Temp\PROMPT_kontrola_volani_na_portech.md`"
— 2026-08-19 16:33 · „Proveď `PROMPT_readyToClose_sever_expedice.md`. **Pořadí containerRemoved →
readyToClose je závazné.**" — 2026-08-19 21:10 · „Přečti celý a proveď
`docs/onboarding/PROMPT-ukotveni-ontologie.md`" — 2026-08-24 09:02

**Opakování.** 10× výroba + min. 6× provedení. Silný vzor, a v průběhu měsíce **rostoucí** —
druhá polovina srpna už bez toho nefunguje.

**Přenositelnost.** `[P]`. Nepotřebuje nic než složku. **A je to zároveň lék na antipattern X02.**

**Předvedatelnost.** Vysoká. Ukázat trojici: nechat vyrobit prompt → uložit → v čisté session
provést. Zvlášť efektivní je ukázat, že prompt je pak **kritizovatelný artefakt** („Vylepši tento
prompt", „Doplň zadání ještě o tyto body" — 2026-08-14 14:24).

---

## P17 · Handoff prompt: priority + doklady + varování o tom, co ještě neplatí `[P]` (obsah `[I]`) — okruh `O`

**Co to je.** Nejvyzrálejší dlouhý prompt měsíce (4502 zn.). Předává práci do nové session tak,
že nová session **nemůže** dojít ke špatnému závěru: každá priorita má zdroje s `soubor:řádek`,
u každé je napsáno **co je otevřené a nesmí se domýšlet**, a na konci je odstavec „proč právě takhle".

**Doklad — kostra:**
```
NALÉHAVOST + KONTEXT   „v předchozí session jsem ukotvil… Registr prvků je hotový;
                        teď chybí ta samá fakta ve specifikacích. Zapisuj v tomto pořadí:"
PRIORITA 1..3          každá: cílový soubor + co dnes chybně tvrdí + seznam zdrojů
                        s `soubor:řádek`
NEGATIVNÍ VAROVÁNÍ     „Pozor: matici … dodavatel přislíbil na 27. 8. a **ještě nedorazila**
                        — specifikace ji nesmí předpokládat."
                        „Otevřené zůstává mapování safety výstupů… to dodavatel neuvedl,
                        **nedomýšlej to.**"
PO KAŽDÉM KROKU        doplň evidenci (`landed_in`) / spusť validátor
PRAVIDLA, KTERÁ NESMÍŠ ZVORAT   self-contained dokument · cituj původní zdroj ·
                        necommituj a nepushuj
STAV REPOZITÁŘE        „V repozitáři jsou z předchozí session necommitnuté změny…"
ODŮVODNĚNÍ POŘADÍ      „Prioritu 1 dělá naléhavou to, že **specifikace aktivně tvrdí
                        neznalost** — PAC si to domyslí sám. To je horší než chybějící
                        kapitola. Prioritu 3 jsem dal na konec záměrně: …"
```
— 2026-08-25 19:38

**Opakování.** 2 plné instance (druhá 2026-08-24 12:18, 7213 zn. — nejdelší prompt měsíce,
s vlastní sekcí **„## 7. Antipatterny"** a s branou „Krok 0 — brána běhu, bez ní nepokračuj").

**Přenositelnost.** **Rozdělit.** Struktura je `[P]`: priority · doklad u každé · **negativní
varování** · pravidla · stav repozitáře · odůvodnění pořadí. Konkrétní obsah (validátory,
`landed_in`, RULE-ONT-002) je `[I]`.

**Předvedatelnost.** Střední — je to na čtení, ne na live demo. Ale **kostru** lze předvést jako
šablonu k vyplnění, a to je jedna z nejlepších „odnesu si to" věcí.

**Nejcennější detail pro workshop:** *negativní varování*. „Toto ještě nedorazilo, nesmíš to
předpokládat" je jediná ochrana proti tomu, aby model doplnil chybějící kapitolu logickou dedukcí.

---

## P18 · Slepá revize — recenzentovi neříkej, co a proč se změnilo `[P]` — okruh `M`

**Co to je.** Recenzní subagent dostane artefakt jako **cizí text**, bez informace, že jde
o opravenou verzi a bez příběhu změny. Odstraňuje potvrzovací zkreslení.

**Doklad.** „Spusť 2–3 subagenty PARALELNĚ, každému dej JEN: — artefakt nebo diff **jako cizí
text (bez věty, co a proč jsme měnili)**, — cesty na normy, — **jednu optiku**." A o krok dál:
„jednoho haiku subagenta na mechanickou verifikaci… **Nový soud jen na změněná místa, v zadání
ANI SLOVO o tom, že jde o opravenou verzi.**" — 2026-08-19 19:41

**Opakování.** 1 zadání, poslané 2× (19:41 a 19:45) — jednorázovka co do výskytu, ale je to
**závěr z předchozích 30 dnů** (viz X01), takže má váhu vzoru.

**Přenositelnost.** `[P]`. Nepotřebuje nic. Je to čistě způsob, jak formulovat zadání subagenta.

**Předvedatelnost.** Velmi vysoká a velmi působivá: dát tentýž text dvěma subagentům, jednomu
s větou „tohle jsme právě opravili podle nálezů" a druhému bez ní, a porovnat počet nálezů.

---

## P19 · Triáž nálezů dělá člověk, ne model. „Počítej, že dva ze tří nálezů jsou falešné." `[P]` — okruh `M`

**Co to je.** Nálezy revize se **nezapracovávají automaticky**. Hlavní session (člověk) je
triážuje, nedoložený nález zavře, u zbytku ověří oporu, a při rozporu zapíše **REBUTTAL s citací**.
Opravy se dělají po jedné, cílenou editací zasažené věty, nikdy přepisem sekce.

**Doklad.**
```
3. TRIÁŽ (děláš ty, v hlavní session): nedoložený nález zavři. U každého zbylého ověř oporu sám
   — počítej, že dva ze tří nálezů jsou falešné. Odporuje-li nález zdroji, zapiš REBUTTAL s citací.
4. Oprav potvrzené nálezy SÁM, po jednom, cílenou editací zasažené věty. Ne přepis sekce.
5. … Konec: 0 otevřených critical, ≤ 2 major, nebo 3. iterace → eskalace na tebe.
```
— 2026-08-19 19:41 (celý protokol 1216 zn.)

**Opakování.** 1 protokol (2×). **Ale je to explicitní náhrada vzoru, který se opakoval 8× —
viz X01.** Tím pádem to je nejcennější jednotlivá věc v okruhu `M`.

**Přenositelnost.** Protokol je `[P]` až na krok 1 (`validate.cmd`), který je `[I]`. Věta
„dva ze tří nálezů jsou falešné, triáž je práce člověka" se přenese beze zbytku.

**Předvedatelnost.** Vysoká: pustit revizi, spočítat nálezy, projít je s kolegy a spočítat,
kolik z nich obstojí.

---

## P20 · Deterministická brána před LLM: „Chyby lintru oprav hned, bez LLM." `[P]` (nástroje `[I]`) — okruh `M`

**Co to je.** Co dokáže rozhodnout skript, se modelu vůbec nedává. Vzor „brána, ne věta v promptu".

**Doklad.** „1. Spusť `docs/plc/.plc-tools/validate.cmd` (nebo `fr-tools/validate.py`). **Chyby
lintru oprav hned, bez LLM.**" — 2026-08-19 19:41. A opačně, když brána chybí: „V UDT
`ZoneSafety_PlcToWes` je potřeba `buttonsPressed` změnit na `byte[8]`… **Oprav kontrolu, která
to měla zachytit a nezachytila.**" — 2026-08-14 14:28.

**Opakování.** 2× v protokolu + 1 reakce na selhání brány + systémový projev (validátory FR,
PLC, ontologie, dodavatelů).

**Přenositelnost.** Princip `[P]`, konkrétní validátory `[I]`. Pro kolegu bez validátorů má
hodnotu i tak: „než pošleš model kontrolovat čísla a adresy, zkontroluj je skriptem" a druhá
polovina věty **„když nález prošel, oprav kontrolu, ne jen ten nález"**.

**Předvedatelnost.** Vysoká (spustit validátor), ale vyžaduje připravené demo.

---

## P21 · Modely podle povahy podúlohy `[P]` — okruh `O`

**Co to je.** Explicitní volba modelu per role: silný na adversariální revizi, prostřední na
opravy, nejmenší na mechanickou verifikaci.

**Doklad.**
- „2. Potom **subagentem s modelem Fable** proveď revizi všech provedených změn. 3. Pokud existují
  závažné nálezy, tak je **subagentem s Sonnet** oprav a pokračuj krokem 2." — 2026-08-17 21:07
- „**jednoho haiku subagenta** na mechanickou verifikaci: 'pro každý nález {id, místo, rezoluce}
  vrať fixed/partial/not-fixed s citací z aktuálního textu'" — 2026-08-19 19:41
- „**Subagentem (Fable)** učeš zkrácený dokument, aby byl srozumitelný, přehledný, správný
  a přeložený celý do angličtiny." — 2026-08-18 22:50

**Opakování.** 4× + 6× `/model`.

**Přenositelnost.** `[P]`. Nepotřebuje nic, jen vědomí, že se to dá napsat do promptu.

**Předvedatelnost.** Nízká-střední (rozdíl není vidět naživo), ale patří to do slidu o nákladech.

---

## P22 · Před revizí znovu načti zdroje, které se změnily `[P]` — okruh `M`

**Co to je.** Levná ochrana proti tomu, aby recenzent soudil proti zastaralé kopii normy
ve svém kontextu.

**Doklad.** „**ADR se mírně změnila, tak před revizí si je načti znovu.**" — 2026-08-15 09:35 ·
„Až bude vhodný čas, proveď si compact kontextového okna, ať máš přesnější výsledky."
— 2026-08-22 22:57

**Opakování.** 2×.

**Přenositelnost.** `[P]`. Jedna věta, velký efekt, nikdo na to sám nepřijde.

**Předvedatelnost.** Nízká. Patří do checklistu, ne do dema.

---

## P23 · Straw-man otázka na dodavatele: napiš navrhovanou odpověď, ať ji jen potvrdí `[P]` — okruh `A`

**Co to je.** Otázka na třetí stranu se nepokládá otevřeně. Přiloží se navržená odpověď (nebo
příklad odpovědi), aby protistrana mohla jen potvrdit — a aby bylo poznat, co přesně se ptáme.

**Doklad.** „Formuluj otázky ještě stručněji. **Pokud je to možné, tak u otázek napiš navrhovanou
odpověď, aby ji mohl dodavatel jednoduše potvrdit.** Jedná se mi o to, jaké konkrétní rozhraní
a s jakými hodnotami se volá v dané chvíli. **Pokud je to již zřejmé, tak u otázky napiš příklad
takové odpovědi.** Ale potřebuji to mít stručné, aby se to dalo prezentovat při telefonickém
hovoru." — 2026-08-18 15:46

Doplňkově: „Přečti si `…komunikace-dopravniku-bullseye-tmt`, zda tam jsou odpovědi na otázky
komunikace s PLC. Pokud ano, **tak do otázky napiš navrhovaný způsob komunikace, aby to dodavatel
mohl případně jen potvrdit.**" — 2026-08-18 15:58

**Opakování.** 2× explicitně, ale je to řídící princip celého BullsEye bloku (55 promptů).

**Přenositelnost.** `[P]`. Naprosto univerzální — funguje na dodavatele, zákazníka i kolegu.

**Předvedatelnost.** Vysoká. Ukázat dvě verze téže otázky a nechat publikum odhadnout, na kterou
přijde odpověď.

---

## P24 · Argumentovat příkladem, když protistrana odmítá `[P]` — okruh `A`

**Co to je.** Když dodavatel odmítá požadavek, nezvyšuje se hlas — vyrobí se konkrétní scénář,
ve kterém požadavek zjevně chybí.

**Doklad.** „Napiš v češtině **konkrétní příklad, proč potřebujeme vydávat povolení, aby to
dodavatel správně pochopil, když to zatím odmítá.**" — 2026-08-07 11:43

Navazuje: „Pomoz mi formulovat krátký, cílený dotaz na upřesnění konkrétního chování. **Zatím
BullsEye odpovídá příliš v obecné rovině.** … Potřebuji, aby z toho bylo cítit důraz, že již
kriticky potřebujeme konkrétní a přesné odpovědi." — 2026-08-12 13:48 → „**Potřebuji ke každému
jejich bodu jednu maximálně dvě věty.**" — 2026-08-12 13:51

**Opakování.** 2 epizody.

**Přenositelnost.** `[P]`.

**Předvedatelnost.** Střední. Dobrý příběh na slide.

---

## P25 · Jazyková vrstva pro cizí publikum — a kontrola, že to opravdu chápou `[P]` — okruh `A`

**Co to je.** Překlad se nezadává jako „přelož", ale s cílovým publikem. A pak se **ověřuje
srozumitelnost jednotlivých slov**.

**Doklad.**
- „Ano, udělej anglickou verzi… **Překládej jednoduchou angličtinou, aby číňané snadno
  pochopili.**" — 2026-08-07 11:53
- „**Skutečně budou rozumět tomu, že 'remove the pallet' znamená odvezení palety?**"
  — 2026-08-10 15:23 → „Tady se nejedná o sundání palety operátorem, ale o posunutí palety na
  dopravníku dále…" — 15:24 → „**co znamená onward?**" — 15:25
- „**Místo 'naše PLC' používej všude WES-PLC. Místo 'vaše PLC' používej WCS-PLC.**" — 2026-08-18 19:23
  → „**Místo 'na naší straně' používej 'na straně WES'.** Obdobně pro stranu WCS." — 19:26

**Opakování.** 8 promptů, 3 epizody.

**Přenositelnost.** `[P]`, a ta druhá a třetí odrážka jsou nečekaně cenné: **v dokumentu pro
třetí stranu je „my/vy" chyba** — musí tam být jmenované systémy.

**Předvedatelnost.** Vysoká, rychlá a vtipná (viz „co znamená onward?").

---

## P26 · Dvě verze dokumentu: plná pracovní + krátká k odsouhlasení `[P]` — okruh `A`

**Co to je.** Z jednoho zdroje se generují dva výstupy pro dvě publika a explicitně se říká,
co se ve zkrácené verzi vypustí.

**Doklad.**
- „Připrav ještě druhou kratší verzi dokumentu … **pro zákazníka s těmi nejdůležitějšími
  informacemi. Potřebuji jej k odsouhlasení toho, co a na kterých stanicích bude WMS volat.**"
  — 2026-08-10 07:14
- „vytvoř druhou zkrácenou verzi dokumentu, která bude obsahovat jen ty nejdůležitější informace.
  **Sekvenční diagramy budou stejné. U otázek bude u každé kapitoly jen první odstavec 'Otázka: …',
  nebudou tam již návrhy variant řešení.**" — 2026-08-18 19:57
- „Zápis je příliš dlouhý. **Udělej stručnější, cca na třetinu současné velikosti.**" — 2026-08-19 11:10

**Opakování.** 3× — vzor.

**Přenositelnost.** `[P]`. Druhá odrážka je vzorová v tom, že říká **pravidlo krácení**, ne jen
„zkrať to".

**Předvedatelnost.** Vysoká.

**Pozor — návazný antipattern:** „Zkontroluj otázky, po zkrácení u některých zůstaly zbytky,
které nyní nedávají smysl — viz Q14, Q16 …" — 2026-08-18 21:16. Krácení nechává ohryzky;
po krácení patří kontrola.

---

## P27 · Formát výstupu jako součást zadání `[P]` — okruh `A`

**Co to je.** Nejen „co", ale i „v jaké podobě a kam". Včetně negativních formátových pravidel.

**Doklad.**
- „**Vypiš všechny názvy do jednoduchého seznamu zde, abych ti řekl, jak chci pojmenovat.**"
  — 2026-08-10 18:31
- „**Nepiš pořadová čísla na začátek řádků. Jen D01, D02 …**" — 2026-08-10 18:57
- „Připrav **tabulku Excel** se srovnáním pořadí volání webhooků v jednotlivých sekvenčních
  grafech, aby bylo zřetelné, kdy pořadí wh je totožné a kdy se liší." — 2026-08-11 15:11
- „**Otázky formuluj jako podkapitoly: 2.1.1 Q1 — How does WES-PLC talk to WCS-PLC**, atd.
  V rámci kapitol nedávej vše na jeden řádek." — 2026-08-18 16:09
- „**Otázky umísti vždy pod diagram, kterého se týkají.**" — 2026-08-18 15:46
- „Napiš 5 až 10 hlavních změn… **Pro každou 1 odstavec.**" — 2026-08-11 14:30

**Opakování.** Vzor, desítky výskytů.

**Přenositelnost.** `[P]`.

**Předvedatelnost.** Vysoká, ale nudná. Spíš krátký blok „formát je součást zadání" s baterií
příkladů.

---

## P28 · Sebekritika návrhu: útok na náklad na údržbu, ne na správnost `[P]` — okruh `A` + `M`

**Co to je.** Když model navrhne mechanismus, analytik ho nezkoumá „je to správné?", ale
**„vydrží to půl roku provozu a kolik mě to bude stát?"**. Tohle je nejzralejší praxe měsíce
a v materiálu se opakuje důsledně.

**Doklad.**
- „Je vhodné používat odkazy jen pomocí čísel řádků do zdrojových dokumentů? **Mám obavy, že
  velice rychle se tyto odkazy rozjedou**, když budeme zasahovat do zdrojových dokumentů."
  — 2026-08-22 22:41
- „**Bude tvůj návrh vhodný i pro Claude Code**, aby uměl dohledat zdroje podle těchto kotev
  **a nezabral si kontextové okno?**" — 2026-08-22 22:50
- „**Neměla by Citace obsahovat ale nějaký minimální počet slov?** Pokud je to jen jedno slovo,
  tak hrozí, že úpravou dokumentu může také rychle nastat duplicita." — 2026-08-22 23:08
- „V `SKILL.md` jsou zapsaná čísla, která se po aktualizacích ontologie mění. **Připadá mi to
  neefektivní, chybné a zbytečné. Je to tak?**" — 2026-08-24 21:42 → „**Je to u některých dalších
  souborů podobně zbytečně?**" — 21:44
- „**K čemu jsou v ontology uváděné dávky? Je to efektivní a nutné? Čím a jak by se to dalo
  nahradit? Nějak mi to tam nesedí…**" — 2026-08-24 23:24
- „V pravidlu je napsáno, že zmizelé kotvy má opravovat člověk. **To mi přijde neudržitelně
  náročné a zdlouhavé. Brání něco tomu, aby to dělal Claude Code sám a automaticky?**"
  — 2026-08-26 08:44 (revize **vlastního** pravidla)
- „Provedl jsem commit, ale po regeneraci ontology vzniklo **350 změn v entitách, protože se
  změnil jen hash**… bude to velice nepřehledné. **Navrhni varianty**, jak to elegantně vyřešit."
  — 2026-08-24 11:17

**Opakování.** 7× — silný vzor, koncentrovaný do posledních 5 dnů měsíce (= zralost).

**Přenositelnost.** `[P]`. Nejlepší přenositelná **návyk** v celém dokumentu, protože LLM
tenhle dotaz sám nikdy nepoloží: model optimalizuje na správnost prvního běhu, ne na náklad
desátého.

**Předvedatelnost.** Velmi vysoká. Nechat model navrhnout mechanismus a pak mu položit tyhle
čtyři otázky: *Kdo to bude udržovat? Co se rozjede? Kolik to sežere kontextu? Co se v tom mění
zbytečně?*

---

## P29 · Před rozhodnutím si nech vysvětlit laicky a pojmenuj, co nevíš `[P]` — okruh `U`

**Co to je.** Analytik nerozhoduje o věci, kterou nechápe. Explicitně žádá laické vysvětlení
a **jmenuje slovo, které mu nic neříká**.

**Doklad.**
- „**Laicky vysvětli V3. Nevím, co jsou seamy.** Nebylo by vhodnějším řešením, kdyby ontologie
  byla vždy řešena jen na úrovni konkrétního projektu…?" — 2026-08-24 09:40
- „**laicky vysvětli ten latentní rozpor**" — 2026-08-24 09:53
- „**Vysvětli nejprve rozdíl, co by znamenal merge a co rebase.**" — 2026-08-11 18:52
  → „udělej merge" — 18:59 (rozhodnutí až po vysvětlení)
- „Vysvětli jednoduše problematiku containerPrepared u příjmu." — 2026-08-13 10:03
- „Laicky mi vysvětli princip a postup, který tedy navrhuješ. **Jak bude vypadat index, kdo
  a kdy jej vytváří apod?**" — 2026-08-22 19:52
- „K čemu je vlastně dobré používat `AcceptedResponse` a jak to vzniklo? Není lepší místo toho
  prázdný payload?" — 2026-08-15 13:17

**Opakování.** 10× — vzor.

**Přenositelnost.** `[P]`, a pro workshop netechnických analytiků je to **vstupní brána**:
„nemusíš rozumět, musíš umět říct, čemu nerozumíš."

**Předvedatelnost.** Velmi vysoká a okamžitě uklidňující pro publikum.

---

## P30 · Model jako připravovač agendy jednání `[P]` — okruh `A`

**Co to je.** Před schůzkou se nechá vyrobit seznam otázek, které se mají probrat, nebo
„kickoff" seznam k rozpoutání diskuse.

**Doklad.**
- „Dnes budu mít schůzku 'chci vykopnout diskusi o tom, jak by měl probíhat proces zapínání
  systémů a obnovování po nouzovém zastavení.' **Připrav mi seznam nejdůležitějších otázek,
  které by bylo vhodné nejprve projednat.**" — 2026-08-24 13:07
- „Z toho vytvoř **stručný seznam otázek na dodavatele**." — 2026-08-03 19:02
- „Napiš stručný seznam otázek, které je na základě závěrů schůzky potřeba poslat na BullsEye.
  **Týká se to komunikace směrem z WES do WCS a řízení PLC.**" — 2026-08-10 15:06
- „Připrav stručný přehled závěrů z jednání, na čem jsme se dohodli, co BullsEye potvrdil, který
  pak budeme schopni odeslat všem účastníkům. **Slučuj body, které řeší společné téma**, aby
  zápis byl přehlednější." — 2026-08-19 10:01

**Opakování.** 5× — vzor.

**Přenositelnost.** `[P]`.

**Předvedatelnost.** Vysoká a extrémně relatable.

---

## P31 · Definuj publikum dokumentu a vyřež z něj všechny vnitřní odkazy `[P]` — okruh `A`

**Co to je.** Dokument, který jde třetí straně, nesmí odkazovat do vnitřní evidence. Pravidlo
je v promptu explicitní, protože model přirozeně odkazuje na všechno, co viděl.

**Doklad.** „PLC specifikace je **self-contained** — žádné odkazy na ADR, FR, ontologii ani na
registr dotazů, žádná historická veteš, changelog jeden řádek." — 2026-08-25 19:38 · „Cílem je
dostat všechny podklady, aby programátoři WES mohli řídit dopravník." — 2026-08-18 16:11 ·
„Doplň ještě do dokumentu, že to je dokument od BullsEye a je to ten dokument, který má uzavřít
mezeru v komunikaci mezi dopravníky od BullsEye a TMT." — 2026-08-06 16:19

**Opakování.** 3×.

**Přenositelnost.** `[P]`.

**Předvedatelnost.** Střední.

---

## P32 · Commit píše člověk; agent připraví text a seznam, co ještě není commitnuté `[P]` — okruh `N` + `M`

**Co to je.** Agent do Gitu nezasahuje. Připraví ale (a) název a popis commitu, (b) inventuru
nezacommitovaných změn, aby člověk věděl, co drží v ruce.

**Doklad.**
- „**Napiš 5 až 10 hlavních změn, které jsem provedl a chybí jejich commit. Pro každou 1
  odstavec.**" — 2026-08-11 14:30
- „Na konci **Připrav název a popis pro commit**" — 2026-08-13 13:30 (a 2026-08-13 07:58)
- „**Před tím než budu dělat commit** proveď subagentem závěrečnou revizi a dej mi stručnou
  zprávu." — 2026-08-13 15:13
- „**Necommituj a nepushuj** — změny nech necommitnuté ve working tree." — 2026-08-25 19:38
  (a 2026-08-24 12:18)

**Opakování.** 5× — vzor.

**Přenositelnost.** `[P]`. Konkrétní důvod (agent nemá GitLab credentials) je osobní, ale
pravidlo „commit je lidský podpis" je přenositelné a dobré.

**Předvedatelnost.** Vysoká, rychlá.

---

## P33 · Nechat model kontrolovat sám sebe metaanalýzou vlastních session `[P]` — okruh `M` + `U`

**Co to je.** Než se nový mechanismus zafixuje, ověří se na **historii vlastní práce**, jestli
by vůbec pomohl.

**Doklad.** „**Založ subagenta, který prozkoumá transkripty několika sessions v tomto repu
z posledních 7 dní a na nich zjistí, jak tato ontologie bude prospěšná** a zda je potřeba nějaké
další vylepšení." — 2026-08-22 20:27

Obdobně na úrovni nástrojů: „Udělej průzkum, jak v Claude Code nejefektivněji provádět revize při
tvorbě specifikací tohoto mého projektu. **Zatím používám tento prompt, ale při opravách často
dochází k zanášení nových chyb a zároveň spotřebovává mnoho tokenů:** …" — 2026-08-19 16:20

**Opakování.** 3× (+ workshopové prompty z 26. 8., mimo rozsah).

**Přenositelnost.** `[P]`. Je to obecný postup „než to zafixuješ, ověř to na vlastní historii",
a to je pro workshop metodicky nejcennější rám vůbec.

**Předvedatelnost.** Střední (běh je dlouhý), ale výsledek se dá připravit dopředu.

---

## P34 · Vysvětlení pro kolegy jako artefakt, ne jako řeč `[P]` — okruh `U`

**Co to je.** Když má věc pochopit tým, nevyrábí se odstavec v chatu, ale schematická stránka.

**Doklad.** „**Vytvoř grafickou schématickou stránku (claude artefakt), pomocí které budu schopen
kolegům analytikům vysvětlit smysl a princip používání ontologie na projektu. Vysvětluj spíše
laicky, používej vhodná schémata.**" — 2026-08-24 13:00 · „**Na konci mi pak laicky napiš postup,
jak máme jako analytici v jednotlivých situacích postupovat, co máme dělat, jaké pokyny máme dát
Claude Code apod.**" — 2026-08-25 11:33

**Opakování.** 2×.

**Přenositelnost.** `[P]`.

**Předvedatelnost.** Nejvyšší možná — je to sám workshop.

---

# ČÁST B — MOMENTY VZNIKU (příběhy s obloukem)

## V01 · Evidence dodavatelů: od chaosu k slash commandu za jeden den `[I]` (příběh `[P]`) — okruh `R`

**Nejlepší workshopový příběh v celém materiálu.** Kompletní oblouk problém → improvizace →
zafixování, uzavřený během ~3 hodin, a s explicitní korekcí analytika uprostřed.

| Čas | Prompt (zkráceně) | Fáze |
|---|---|---|
| 2026-08-25 10:01 | „Kde jsou uložené odpovědi od BlueSword a BullsEye na naše otázky?" | Symptom |
| 10:19 | „**Začínáme se v těch konverzacích s dodavateli ztrácet.** Posíláme si otázky a odpovědi e-maily a **nevíme, k čemu již máme dostatek informací a co ještě chybí.** Snažili jsme se to rekapitulovat i v Excel dokumentu, ale také to není ideální. Zároveň potřebujeme, aby aktuální informace mohl efektivně čerpat Claude Code. … **navrhni varianty.**" | Pojmenování problému + „navrhni varianty" |
| 11:06 | „Kolega už zpracoval seznam otázek a přiřadil jim identifikátory: `…xlsx`. **Při vytváření příkladů prvních 3 e-mailů převezmi identifikátory z tohoto souboru.**" | Napojení na existující lidskou evidenci — nezakládá se nové ID schéma |
| 11:33 | „**Na konci mi pak laicky napiš postup, jak máme jako analytici v jednotlivých situacích postupovat**, co máme dělat, jaké pokyny máme dát Claude Code apod." | Návod pro tým jako součást zadání |
| 12:09 | „**Proč jsi na to nevytvořil vhodné projektové skills? Rád bych to používal opakovaně jednoduchým způsobem.** e-maily z inboxu se po zpracování někam automaticky přesouvají?" | **KOREKCE — bod zafixování** |
| 12:16 | „Z důvodu přehlednosti by se mi líbilo, abych nové e-maily nahrával do složek `inbox`. Po zpracování je dávka nebo Claude přejmenuje a přesune na místo, kde budou primárně uložené. **Jsou e-maily ukládané také do md formátu, aby byly dobře dohledatelné z Claude Code?**" | Návrh operačního rozhraní pro člověka |
| 13:04 | `/dodavatele:stav` | **Hotovo a v provozu** |
| 14:10, 14:18, 14:52, 15:51 | `/dodavatele:mail` (4×), „V e-mailu z 18.8. nám BullsEye poslal excel tabulku s aktualizovanými odpověďmi. Aktualizuj toto do naší evidence." | Rutinní užití |
| 14:45 | „**Jak to, že v inboxu zůstal** `…msg`?" → 14:46 „ano, smaž ho" | Ladění mechaniky |
| 14:11 | „**Když posílám nové otázky dodavateli, kdo a kdy jim přidělí čísla?** Co v okamžiku, když už jsem poslal své otázky a nepřidělil jim čísla nebo je očísloval jen 1 až 20?" | Hraniční případ procesu |
| 22:17 | „Otázka PRE-016 ještě nebyla odeslána. **Je to nějak rozlišeno statusem? Jak se změní status po odeslání?**" | Kontrola stavového modelu |

**Přenositelnost.** Registr samotný je `[I]`. **Příběh a jeho pointa jsou `[P]`** a pointa je
jednořádková: *„Když to samé zadáváš třikrát, přestaň zadávat a nech si z toho udělat skill."*
Druhá pointa je stejně cenná: **nezakládej nové ID schéma, převezmi to lidské, které už tým používá.**

**Předvedatelnost.** Nejvyšší v celém dokumentu. Doporučuji jako **hlavní demo okruhu `R`**:
promítnout tuhle tabulku, pak naživo `/dodavatele:stav`.

---

## V02 · Ontologie prvků: od diktovaného promptu s překlepy k pluginu za 4 dny `[I]` (poučení `[P]`) — okruh `R` + `M`

| Čas | Prompt (zkráceně) | Fáze |
|---|---|---|
| 2026-08-22 11:21 | „připrav projekt který smapuje všechny prvky systému a připraví jejich ontologií chci projít postupně všechny důležité dokumen ty ve k nezapomnělo **zatím nic nespouštějí pouze přípravkem**" | Diktovaný, silně zkomolený start — a přesto s read-only bránou |
| 11:22 | „připrav **prompt** který zmapuje…" (jediná změna: *projekt* → *prompt*) | Přesměrování na artefakt (P16) |
| 11:39 | „nyní **postupně spouštěj jednotlivé dávky jako samostatné sessions na pozadí**" | Dávková orchestrace |
| 14:49 | „navrhni způsob nebo nástroj **jak přehledně a efektivně prohlížet** `ontology.yaml`" | Použitelnost pro člověka |
| 19:37 | `/pruzkum` „Dále potřebuji, aby tuto ontologii **mohl efektivně využívat jazykový model**… jak mít data uložená a formátována, aby to **nespotřebovávalo zbytečně mnoho tokenů**. Pokud je potřeba konverze, **preferuji deterministický způsob.**" | Použitelnost pro LLM + požadavek determinismu |
| 22:41 → 23:08 | „**Mám obavy, že velice rychle se tyto odkazy rozjedou**" → „Neměla by Citace obsahovat nějaký minimální počet slov?" | Útok na náklad na údržbu (P28) — **před** implementací |
| 2026-08-24 08:38 | „potřebuji ji **ukotvit do projektu**, aby při dalších změnách se specifikace o ni vhodně opíraly… Zároveň bych tuto zkušenost rád **sdílel mezi dalšími projekty**… Napiš nyní prompt, který má udělat průzkum a návrh" | Přechod z artefaktu na mechanismus |
| 09:19, 09:51, 10:00, 10:44 | „Pokračuj dávkou B / C / D", „N1, N2, N4 přijmout před přenosem. N3 zamítnout" | Řízení po dávkách + picklist (P02) |
| 09:40 | „**Laicky vysvětli V3. Nevím, co jsou seamy.** Nebylo by vhodnějším řešením, kdyby ontologie byla vždy řešena jen na úrovni konkrétního projektu, aby byla spolehlivě udržovaná? A plugin by třeba obsahoval **jen nástroj pro zavedení ontologie na novém projektu**?" | **Klíčové rozhodnutí, vyhrané laickou otázkou** |
| 11:17 | „po regeneraci ontology vzniklo **350 změn v entitách**, protože se změnil jen hash… **Navrhni varianty**" | Praktický náraz |
| 12:18 | 7213znakový handoff prompt s **„Krok 0 — brána běhu (bez ní nepokračuj)"** a sekcí **„## 7. Antipatterny"** | Zafixování do přenositelného promptu |
| 2026-08-25 22:42 → 22:43 | „Proveď úklid podle RULE-ONT-003." → „**Ty zmizelé kotvy se pokus opravit sám.**" | Rutinní provoz — a hned ohýbání vlastního pravidla |
| 2026-08-26 08:44 | „V pravidlu je napsáno, že zmizelé kotvy má opravovat člověk. **To mi přijde neudržitelně náročné.** Brání něco tomu, aby to dělal Claude Code sám?" | Revize vlastního pravidla po 2 dnech provozu |

**Přenositelná poučení (`[P]`) z jinak `[I]` příběhu:**
1. Rozhodnutí „ontologie ať zůstane na projektu, plugin ať jen zavádí kostru" **vzniklo z laické
   otázky**, ne z technické analýzy. (P29 má reálnou návratnost.)
2. Náklad na údržbu se testoval **před** implementací (P28) a přesto se dvakrát nabořil
   (350 hashových změn, čísla v `SKILL.md`) — poučení: *nedávej do generovaných souborů nic,
   co se mění častěji než jejich obsah.*
3. Pravidlo, které si sám napíšeš, budeš do dvou dnů chtít změnit. To je normální; podstatné je,
   že se to ptá, ne že se to obchází.

**Předvedatelnost.** Střední na živé demo, vysoká jako narativní slide s touto tabulkou.

---

## V03 · Vznik triážního protokolu: uživatel si vlastní vzor sám diagnostikoval `[P]` — okruh `M` + `X`

Nejcennější oblouk v okruhu mechaniky kvality, protože je to **opuštění zaběhnutého vzoru**.

| Čas | Prompt (zkráceně) |
|---|---|
| celý srpen, 8× | „1. Subagentem (Fable) proveď adversariální revizi provedených změn. 2. Pokud existují závažné nálezy, oprav je subagentem a **pokračuj bodem 1**." |
| 2026-08-19 16:20 | „Udělej průzkum, jak v Claude Code nejefektivněji provádět revize při tvorbě specifikací tohoto mého projektu. **Zatím používám tento prompt, ale při opravách často dochází k zanášení nových chyb a zároveň spotřebovává mnoho tokenů**" |
| 16:20 | `/pruzkum <totéž>` — přesun do strukturovaného průzkumu |
| 16:25 | „**Další kolo oprav již neprováděj.**" — brzda smyčce ještě před výsledkem |
| 19:31 | „**Jak s tvým zjištěním koresponduje** `C:\Git\shared\plugins\spec-factory`?" — konfrontace zjištění s existující infrastrukturou |
| 19:41 / 19:45 | Nový 5krokový protokol (P18–P20): linter → paralelní slepí recenzenti s jednou optikou → **triáž člověkem s REBUTTAL** → cílené opravy po jedné větě → mechanická verifikace haiku → stop podmínka |
| 20:24 | „ještě jedno kolo revize" — ale už řízené, ne automatické |

**Přenositelnost.** `[P]`. Celý oblouk lze převyprávět bez jediné zmínky o projektu. A pointa
je univerzální: **„revize → oprava → revize" jako smyčka bez lidské triáže vyrábí nové chyby
a spaluje tokeny.**

**Předvedatelnost.** Vysoká. Ukázat obě zadání proti sobě a nechat publikum uhádnout, které
z nich je starší.

---

# ČÁST C — ANTIPATTERNY

## X01 · Autonomní smyčka „revize → oprava → revize" bez lidské triáže `[X]` — okruh `X` → `M`

**Co to je.** Nejrozšířenější vzor měsíce (8×) a **sám uživatel ho označil za vadný**.
Subagent najde nálezy, jiný subagent je opraví, další subagent zreviduje — a nikdo neověří,
že nález byl pravdivý.

**Doklad — vzor:**
- „1. Subagenty projdi všechny relevantní FR a TC a zkontroluj… 2. Potom oprav závažné nálezy
  (použij subagenty, pokud je to vhodné). 3. Subagentem zkontroluj provedené změny. 4. **Pokud
  existují závažné nálezy, pokračuj bodem 2.**" — 2026-08-13 08:27
- „Diagramy vytvoř subagentem dle precizního zadání. Pak je druhým subagentem reviduj. Pak oprav
  chyby. Pak znovu subagentem zreviduj. Pak oprav závažné chyby." — 2026-08-10 19:43
- „…pak jej druhým subagentem nech revidovat a dalším opravit chyby, **dokud nebude OK
  (maximálně 3 kola)**." — 2026-08-07 18:56

**Doklad — vlastní diagnóza:** „**při opravách často dochází k zanášení nových chyb a zároveň
spotřebovává mnoho tokenů**" — 2026-08-19 16:20

**Opakování.** 8× jako zadání, přes celý měsíc, do 19. 8.

**Přenositelnost.** Jako **antipattern `[P]`** — a je to nejužitečnější varování, které kolegům
můžeš dát, protože je to přesně to, co si každý vymyslí sám jako první.

**Předvedatelnost.** Vysoká, pokud se ukáže vedle P19. Nechat smyčku běžet 3 kola a spočítat
nálezy, které vznikly opravou předchozích.

**Náhrada:** P18 + P19 + P20.

---

## X02 · Přeposílání téhož promptu (a dlouhé prompty vkládané do chatu) `[X]` — okruh `X` → `O`

**Co to je.** 14 skupin / 29 promptů je přeposlání téhož zadání. Příčiny: (a) dlouhý vložený
text se při vkládání ořízne, (b) `/compact` nebo `/resume` uprostřed, (c) nejistota, jestli to
prošlo.

**Doklad — přeposílání:**
- 3× identicky „Přečti celý a proveď `docs/onboarding/PROMPT-ukotveni-ontologie.md`"
  — 2026-08-24 09:02, 09:07, 09:10
- 2× identicky celý 1216znakový triážní protokol — 2026-08-19 19:41 a 19:45
- 2× identicky 1216/916/905znaková zadání (14. 8. 14:24 → 19:39, 13. 8. 22:52 → 22:55…)

**Doklad — přímé přiznání příčiny:** „**Ještě jednou dávám prompt, kdyby při kopírování náhodou
něco vypadlo:** [Pasted text #1 +53 lines]" — 2026-08-25 19:41

**Doklad — skutečná ztráta textu.** Prompt z 2026-08-14 19:36 (3052 zn.) je ve zdroji viditelně
poškozený: „1. Kategorii (A–E) a jednovětné **shr**", „nebo **explicrstvu** proto, že o věci
nemluví", „**Nic z paměti ani z obecné znalost**zení citací." — tj. zadání s pravidly odešlo
s dírami. Stejný typ poškození v handoff promptu 2026-08-25 19:38: „**3. Měřicí trakt na
předpříjmu — j**", „tři podklady z 16. 8. v `docs/ časový diagram`".

**Opakování.** 14 skupin — systémový problém, ne nehoda.

**Přenositelnost.** `[P]` jako varování s hotovým lékem: **dlouhé zadání patří do souboru**
(P16) a session ho jen provede. Ušetří to přeposílání i tiché díry v pravidlech.

**Předvedatelnost.** Velmi vysoká a nezapomenutelná: promítnout ten poškozený prompt a ukázat,
že v něm chybí půlka pravidla „nic z paměti".

---

## X03 · Regenerace přepíše ruční editaci člověka `[X]` — okruh `X` → `M`

**Co to je.** Člověk ručně upraví vygenerovaný artefakt; další běh agenta to přepíše, protože
o té úpravě neví.

**Doklad.** „**Pořadí participantů chci ponechat jak jsem upravil**" — 2026-08-18 22:58,
následováno hned dalším promptem „Operátor má být první" — 22:58. Obdobně „Pozor! Ve změnách TC
vidím **stále** toto! **Proč jsi to nevrátil zpět?**" — 2026-08-07 17:28.

**Opakování.** 2 doložené epizody, ale je to strukturální riziko celého generovaného světa
(viz i 350 hashových změn, 2026-08-24 11:17).

**Přenositelnost.** `[P]`. Pravidlo: *co jsi ručně upravil v generovaném souboru, řekni agentovi
předem — nebo to nedělej ručně a oprav generátor.* Doložený správný reflex: „**Neopravuj
`RELATIONS.tsv` ruční editací. Je to derivát; oprava patří do generátoru.**" — 2026-08-24 12:18.

**Předvedatelnost.** Vysoká.

---

## X04 · Diktované zadání s překlepy — funguje v próze, ne v identifikátorech `[X]` s nuancí — okruh `X`

**Co to je.** Řada dlouhých promptů je diktovaná a silně zkomolená. Překvapivě to většinou
funguje — ale právě v těchto promptech vznikly nejdražší terminologické chyby.

**Doklad — komolení:** „Jakmile tam dorazí další paleta tak PLC automaticky port otevře potom
po odebrání palety operátorem **je čidlo detekuje le paleta tam míč není cool rozbliká**…"
— 2026-08-04 19:48 (2445 zn.) · „chci projít postupně všechny důležité **dokumen ty ve k
nezapomnělo** zatím nic **nespouštějí pouze přípravkem**" — 2026-08-22 11:21

**Doklad — cena:** ta samá vlna diktovaných promptů vede k epizodám P12 (error stanice vs. error
větev, 3 prompty) a k „**'příjem outbound' je blbost.** Mám příjmový dopravník a expediční
dopravník (označovaný jako error větev)" — 2026-08-10 18:59.

**Opakování.** Vzor v dlouhých promptech.

**Přenositelnost.** `[P]` jako **kalibrace očekávání**, ne jako doporučení. Poselství pro
kolegy: *model tvoje překlepy v próze snese; nesnese je v názvech prvků, číslech a
identifikátorech* — a tam, kde ti záleží na slovníku, si ho nech přečíst zpět (P12).

**Předvedatelnost.** Vysoká a odlehčující. Promítnout diktovaný prompt a jeho korektní výsledek.

---

## X05 · Úklid historie rozhodnutí, který si vzápětí vypálí oči `[X]` — diskusní bod — okruh `X` + `M`

**Co to je.** Analytik důsledně požaduje, aby dokumentace nesla jen **aktuální stav**, bez
historie oscilací. Je to obhajitelné (dokumentace není changelog) — ale ve stejném měsíci ho
právě chybějící historie donutila pátrat po proveniencii.

**Doklad — požadavek na úklid:** „**Nepotřebuji v komentáři zapisovat, že se to měnilo tam a zase
zpět. Stačí mi aktuální stav.**" — 2026-08-11 17:18 · „**V ADR nepotřebuji zmiňovat, že jeden
den platilo něco jiného. Je to zbytečné.**" — 2026-08-19 21:30 · „Zruš seznam změn v úvodu
dokumentu. Nepotřebuji ho." — 2026-08-14 18:17

**Doklad — cena:** „**Zjisti, kdo a kdy to měnil z bliká na svítí.**" — 2026-08-07 17:01 ·
„Jedná se mi o to, **zda máme někde dříve než v této session podloženou informaci**…" — 16:57 ·
„**Jak to bylo dosud před touto mou změnou?**" — 2026-08-13 13:57 · „**Kde vzniklo tvrzení**, že
na vstupních portech v mezaninu má Alza volat readyToClose?" — 2026-08-09 20:28

**Opakování.** 3 požadavky na úklid vs. 4 pátrání po historii. Vzor na obou stranách.

**Přenositelnost.** `[P]` jako **diskusní bod**, ne jako doporučení. Otázka pro workshop:
*kam patří historie rozhodnutí, když ji nechceme v dokumentu?* (Odpověď v tomto projektu:
do changelogu ADR a do Gitu — ale to musí být rozhodnuté vědomě.)

**Předvedatelnost.** Střední. Skvělý materiál na 5minutovou diskusi.

---

## X06 · 9 reverzů vlastního rozhodnutí — a proč to *není* chyba zadávání `[P]` s výhradou — okruh `A` + `X`

**Co to je.** Devět promptů explicitně ruší předchozí rozhodnutí. Kritická otázka je, jestli je
to špatné zadání, nebo vyjasňující se úloha. **V tomto materiálu jednoznačně to druhé** — a to je
pro workshop klíčové rozlišení.

**Doklad — reverzy z vyjasnění (legitimní):**
- „**Tak nakonec jsem to přehodnotil** a chci to srovnat podle toho, jak to je v AGV zóně… **Jak
  by to vypadalo v tomto případě? Kde může být kolize?**" — 2026-08-10 15:57 (reverz + rovnou
  žádost o kolize)
- „**Beru zpět rozhodnutí**, že na AGV portech se nevolá readyToClose. **Platí to jen pro režim
  OUT.** … Vrať změnu a narovnej tuto situaci." — 2026-08-11 16:15 (reverz zpřesněním scope)
- „**Omlouvám se**, HMI panel na předpříjmu i nouzovém předpříjmu má tlačítko pro odebrání…
  **Dává to takto lepší smysl? Co musím dále rozhodnout nebo potvrdit?**" — 2026-08-13 14:52
- „**Tak to jsem špatně pochopil.** Potvrzuji, že měřící brána má jen čidla, která měří
  volno/obsazeno…" — 2026-08-25 20:19 (reverz po tom, co si nechal vysvětlit fyziku zařízení)

**Doklad — reverz ze změny scope (taky legitimní, ale jinak):**
- „**Měním rozhodnutí. Budu chtít změnit jen diagramy. FR a TC nechám na kolegyni.**"
  — 2026-08-25 20:26
- „Promítni zatím jen do D9/D10. Do FR a TC dorovnáme dodatečně." — 2026-08-10 16:27

**Doklad — jediný skutečně nákladný reverz:** epizoda „bliká vs. svítí" (2026-08-07 16:48–17:15).
Tam se model **nechal přesvědčit vlastní dřívější odpovědí**, změnil tvrzení v dokumentaci
a analytik musel 5 promptů pátrat, kdo to změnil, než to vrátil zpět.

**Opakování.** 9×.

**Přenositelnost.** `[P]` jako **rám**: reverz není selhání zadání; selhání je reverz, u kterého
nedokážeš dohledat, odkud vzniklo původní tvrzení. Praktický lék je P01 (read-only brána) —
reverz před zápisem je zdarma.

**Předvedatelnost.** Vysoká jako slide s tabulkou „legitimní reverz / drahý reverz".

---

## X07 · Pracovní artefakty pro zákazníka bydlící v `C:\Temp` `[X]` — okruh `X` → `N`

**Co to je.** Dokument, který se týden vyvíjel a šel na odsouhlasení zákazníkovi, ležel mimo
repozitář, bez verzování, vedle promptů a scratchů.

**Doklad.** „Aktualizuj podle toho tabulku v `C:\Temp\Prehled_stanic_readyToClose.md`"
— 2026-08-05 15:17 → ještě 2026-08-10 08:05 a 2026-08-19 23:03 („Jsou informace
z `C:\Temp\WMS_volani_na_portech_k_odsouhlaseni.md` podchycené v ADR?"). Zároveň si toho je
uživatel vědom: „**Máme v claude.md podchyceno pravidlo, že se nemají běžně využívat informace
ze složek temp, tmp nebo spec**, pokud to není explicitně vyžádáno? **Jak to lépe specifikovat?**"
— 2026-08-19 09:00.

**Opakování.** Min. 6 promptů se odkazuje na `C:\Temp\*`.

**Přenositelnost.** `[P]` jako varování + hotová hranice: **rozliš scratch (agent tam nesmí
čítat) od pracovního artefaktu (patří do repozitáře)**, a napiš to do `CLAUDE.md`.

**Předvedatelnost.** Střední.

---

## X08 · „pokračuj" jako řídicí nástroj `[Z]` / mírný `[X]` — okruh `X`

**Co to je.** 8× samostatné „pokračuj" jako celý prompt. Levné, ale rozsah dalšího kroku
si vybírá model.

**Doklad.** „pokračuj" — 2026-08-05 15:33, 08-07 18:42, 08-12 21:12, 08-13 07:08, 08-13 21:43,
08-19 15:26, 08-24 09:16, 08-24 12:25.

**Opakování.** 8×.

**Přenositelnost.** Nehodí se učit. Zmínit jako kontrast k P02: **„pokračuj bodem 3" je řízení,
„pokračuj" je odevzdání volantu.** Uživatel sám tu lepší verzi má: „Pokračuj dávkou B."
— 2026-08-24 09:19.

**Předvedatelnost.** Nízká.

---

# ČÁST D — OSOBNÍ ZVYKY, KTERÉ NEUČIT

## Z01 · Koordinace dvou session přes Session ID a „práce v noci" `[Z]` — okruh `O`

**Doklad.** „Zatím ještě **Session ID: 70e84664-… dokončuje `onthology.yaml`. Jakmile úspěšně
dokončí svoji práci, můžeš pracovat na svých úkolech.** Zatím si můžeš připravit podklady…
**abys práci mohl provést samostatně v noci.**" — 2026-08-22 21:37 · „Podívej se na výsledek
vedlejší session, zda můžeš pokračovat" — 2026-08-23 06:34

**Proč nezobecňovat.** Session nemá jak spolehlivě zjistit stav jiné session; funguje to jen
proto, že mezi nimi leží soubory v repozitáři a člověk u toho sedí. Pro workshop je z toho
použitelné jen tolik, že **rozhraním mezi session je soubor, ne instrukce** — a to už pokrývá P16.

---

## Z02 · Dávková organizace práce (D1…D13, „Pokračuj dávkou B") `[Z]`/`[I]` — okruh `O`

**Doklad.** „nyní postupně spouštěj jednotlivé dávky jako samostatné sessions na pozadí"
— 2026-08-22 11:39 · „Pokračuj dávkou B / C / D" — 2026-08-24 09:19, 09:51, 10:00 ·
„**K čemu jsou v ontology uváděné dávky? Je to efektivní a nutné?**" — 2026-08-24 23:24
(sám to zpochybnil) · „Potom mi vysvětli význam těch dávek D1, D2… **K čemu jsou, když ontologie
už je hotová? Proč má smysl ty dávky stále ještě uvádět?**" — 2026-08-24 10:48

**Proč nezobecňovat.** Uživatel sám dvakrát došel k tomu, že dávky přežily svůj účel. Pro
workshop je z toho použitelný jen princip **„rozděl velkou úlohu na dávky s jasným koncem"** —
to je P02/P16 — a varování, že **artefakty procesu nemají zůstávat v produktu**.

---

## Z03 · Verzování API v každém druhém promptu `[Z]`/`[I]` — okruh `N`

**Doklad.** „V API popiš změnu do verze 1.1.1" — 2026-08-04 20:28 · „Verzi API posuň na 1.2.2"
— 2026-08-19 22:24 · „V API dej do verze 1.2.3" — 2026-08-24 12:53 · „API verze 1.2.3 → 1.2.4"
— 2026-08-25 21:38

**Proč nezobecňovat jako praxi zadávání.** Je to projektová konvence, nikoli technika promptování.
Pro workshop maximálně jedna větička v okruhu `M`: *bump verze kontraktu je jednotka změny —
řekni to agentovi, ať to nezapomene.*

---

## Z04 · `/compact` 19× a mikromanagement kontextu `[Z]` s jedním přenositelným zbytkem — okruh `N`

**Doklad.** 19× `/compact`, včetně `/compact` slepeného se zadáním (2026-08-12 21:20)
a „Až bude vhodný čas, **proveď si compact** kontextového okna, ať máš přesnější výsledky."
— 2026-08-22 22:57

**Proč většinou nezobecňovat.** Je to reakce na dlouhé session, ne technika. **Přenositelný
zbytek je P22:** po compactu (a po změně normy) se musí zdroje **znovu načíst**, jinak recenzent
soudí proti paměti.

---

# ČÁST E — DOPORUČENÁ SKLADBA WORKSHOPU (z tohoto úseku)

| Okruh | Nosné kandidáty | Poznámka |
|---|---|---|
| **K** kontext a grounding | P09 (výzva na provenienci) · P10 (zdrojová izolace) · P07 (CO NEČÍST) · P08 (rozhodčí) · P14 (pravidlo ≠ instance) | P09 je nejsilnější kandidát celého dokumentu |
| **A** analytické postupy | **P06 (vrstvový audit)** · P05 (páka) · P03+P04 (uzavřené otázky, rozpočet) · P11 (hypotéza k vyvrácení) · P12+P13 (terminologie) · P15 (ticho je nález) · P23 (straw-man otázka) · P25 (jazyk publika) · P26 · P27 · P30 | P06 jako centrální live demo |
| **M** mechanika kvality | **P19 (triáž člověkem)** · P18 (slepá revize) · P20 (deterministická brána) · P22 · P28 (náklad na údržbu) · P32 | Uvést vždy vedle X01 |
| **O** orchestrace | **P16 (prompt jako soubor)** · P17 (handoff prompt) · P21 (modely per role) | P16 je zároveň lék na X02 |
| **R** rozšíření | **V01 (evidence dodavatelů)** · V02 (ontologie) | V01 je nejlepší demo v celém materiálu |
| **U** učení | P29 (laicky + pojmenuj neznámé) · P34 (artefakt pro kolegy) · P33 (metaanalýza vlastních session) | Vstupní brána pro netechnické publikum |
| **X** antipatterny | **X01 (autonomní smyčka)** · X02 (přeposílání / ořezané prompty) · X03 (regenerace přepsala člověka) · X06 (reverzy — s rámem) · X05 (úklid historie — jako diskuse) · X04 · X07 · X08 | X01 + V03 = nejlepší oblouk workshopu |
| **N** nastavení | P32 (commit dělá člověk) · X07 (hranice scratch/repo) · Z04 zbytek (P22) | Krátký blok, ne přednáška |

**Tři nejsilnější položky pro program:**
1. **P06 + P05 + P15** — vrstvový audit dokumentace jako jeden hotový, přenositelný prompt
   (kostra + „páka" + „ticho je nález"). Nepotřebuje žádnou infrastrukturu a nese největší
   analytickou hodnotu.
2. **X01 → V03 → P19/P18** — příběh „automatická smyčka revizí vyrábí chyby" a jeho náhrada
   triážním protokolem se slepými recenzenty. Doložená vlastní diagnóza dělá z toho příběh,
   ne poučování.
3. **V01** — evidence dodavatelů: chaos v e-mailech → varianty → převzetí lidských ID →
   „Proč jsi na to nevytvořil skill?" → `/dodavatele:stav` v provozu za 3 hodiny. Oblouk
   problém → improvizace → nástroj, kompletně doložený a předvedatelný naživo.

**Co z tohoto úseku do workshopu NEDÁVAT:** Z01 (koordinace přes Session ID), Z02 (dávky D1…D13
jako organizační princip), Z03 (verzování API), většinu Z04 (`/compact` jako technika), X08
(„pokračuj").
