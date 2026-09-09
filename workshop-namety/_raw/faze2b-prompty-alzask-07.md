# FÁZE 2b — Destilace praxe zadávání z promptů AlzaSk, 2026-07

**Vstup:** `C:\tmp\workshop-namety\_raw\prompty-alzask-07.md` — 432 promptů, 2026-07-01 až 2026-07-30
**Skripty:** `analyza07.py`, `analyza07b.py` (tamtéž)
**Zpracováno:** 2026-08-26

---

## 0. Metodická poznámka a limity vstupu

Co vstup **umí** doložit: znění promptu, čas, pořadí, počet iterací nad jedním tématem, slash příkazy.
Co **neumí**: odpovědi Claude. Proto u korekcí rekonstruuju „co Claude udělal špatně" z toho, co
uživatel v korekci vytýká — je to nepřímý, ale u konkrétních korekcí („místo Error port chci…")
spolehlivý doklad. Kde je rekonstrukce spekulativní, je to označeno **(dedukce)**.

Dva technické artefakty logu, které je třeba odfiltrovat, aby nezkreslily statistiku:

- **Dvojité odeslání téhož promptu** (24 párů). Vzniká tak, že uživatel prompt odešle, pak přepne
  model (`/model`) nebo doplní cestu a odešle znovu. Není to iterace ani korekce — je to režie.
- **Šum:** `test` (3×), `alza`, `V xccc`, `/resu` — vyřazeno.

Statistika po odfiltrování: **432 promptů celkem, 110 slash příkazů, 322 věcných promptů.**

---

## 1. Číselný obraz měsíce (kontext pro všechny kandidáty)

| Metrika | Hodnota | Poznámka |
|---|---|---|
| Promptů celkem | 432 | nejintenzivnější měsíc |
| Slash příkazů | 110 (25 %) | čtvrtina vstupů je řízení nástroje, ne práce |
| Medián délky promptu | **66 znaků** | drtivá většina je jedna věta |
| Promptů pod 100 znaků | 263 (61 %) | |
| Promptů nad 1000 znaků | **6 (1,4 %)** | dlouhá zadání jsou vzácná — viz sekce 4 |
| Promptů s `@`-referencí | 33 | |
| Promptů s absolutní cestou | 26 | |
| Promptů s obrázkem | **35** | schémata, screenshoty, výřezy tabulek |
| `/model` | 19 | |
| `/compact` | 16 | |
| `/context` | 8 | |
| `/body-z-jednani` | 16 | z toho 8× `/body-z-jednani 30` v jednom dni |
| `/reload-plugins` | 8 | režie zavádění pluginů |
| Kandidátů korekce | ~113 | po ruční filtraci ~40 skutečných korekcí |

**Klíčové čtení těch čísel:** praxe **není** „napsat dobrý dlouhý prompt". Je to **krátký prompt
v dobře postaveném kontextu** — medián 66 znaků funguje jen proto, že v repozitáři existuje
`CLAUDE.md`, glosář, ADR, validátory a otevřený backlog. To je pro workshop nejdůležitější
jediná věta: **kolega, který si odnese jen „piš krátce", dostane špatný výsledek.**

---

## 2. Struktura zadávání — je v tom systém?

**Odpověď: ano, ale nikoli ve tvaru „kontext → úkol → omezení → formát".** Zadání se skládá
**přes několik promptů**, nikoli v jednom. Doložený tvar (vzor „inkrementální zadání"):

```
prompt 1:  úkol + cíl                      (krátký, 1–2 věty)
prompt 2:  doplnění zdroje/cesty            (často po ESC a znovuodeslání)
prompt 3:  omezení („nic neměň", „jen vypiš")
prompt 4:  formát výstupu („do chatu", „středníkem oddělené", „max 60 slov")
```

To se nedá zaměnit s nahodilostí: prvky se opakují ve stejném pořadí a stejným slovníkem
(10× „do chatu", 5× „nic neměň / neopravuj", 12× terminologické sjednocení, 13× číslované
odpovědi). Ale ve **prvním** promptu skoro nikdy nejsou všechny čtyři.

To je zároveň největší doložený prostor ke zlepšení → viz **X1**.

---

## 3. Kandidáti — okruh K (kontext a grounding)

### K1 — Uzavřený zdroj pravdy jmenovaný v promptu („čerpej jen ze…")

**Co to je:** V zadání je explicitně jmenován jediný přípustný zdroj hodnot a zákaz doplňovat
z modelu.

**Doklad:** *„Doplň/zkontroluj Kód stanice, Kód portu, Kód procesní lokace, pokud je to možné.
Nevymýšlej si je, ale čerpej jen ze zdroje C:\…\DEV\initData.json."* (2026-07-10 07:20)

**Opakování:** Explicitní zákaz 1×, ale `initData.json` jmenován jako **závazná** autorita pro
pojmenování 4× (07-02 12:15 „Pravděpodobně nejvíce relevantní údaj je … initData.json, kde je
závazné pojmenování stanic a portů", 07-09 21:08, 07-10 07:20, 07-11 12:53 „Není to dotaz na PAC.
Máme v initData.json"). Vzor.

**Přenositelná praxe.** Kolega nepotřebuje nic postavit — potřebuje jen vědět, který soubor v jeho
oblasti je kanonický, a napsat to do promptu. Formulace „nevymýšlej si je, ale čerpej jen ze
zdroje X" je přenositelná doslova.

**Okruh:** K
**Předvedatelnost:** Silná. Naživo: stejný úkol dvakrát — bez věty o zdroji (Claude doplní
plausibilní kódy) a s ní (Claude vypíše, co ve zdroji chybí). Rozdíl je vidět okamžitě.

---

### K2 — Provenience tvrzení jako samostatný fakt („kdo to řekl")

**Co to je:** Uživatel opravuje ne obsah rozhodnutí, ale jeho **autorství** — protože v dokumentu
je rozdíl mezi „potvrzeno dodavatelem" a „rozhodli jsme si sami".

**Doklad:** *„Ta rozhodnutí nedodal PAC ale udělal jsem je sám podle svých znalostí."*
(2026-07-11 22:01) — reakce na to, že Claude předchozí dávku odpovědí zapsal jako odpovědi PAC
(dedukce z předchozího promptu 07-11 21:54 „Odpovědi PAC: P2… P3… P4…").
Protipól: *„Na jedné z poslední schůzek bylo panem Krčmářem potvrzeno, že …Vytvoř na to ADR
(pokus se dohledat záznam z jednání, asi 9.7.2026)"* (2026-07-11 21:31).

**Opakování:** 2 přímé výskyty, ale celý měsíc je na tom postavený (registr dotazů dodavatelům,
`[PAC/DWG]` značky v backlogu).

**Přenositelná praxe** — princip. `[infra]` jen tam, kde chceš mít registr dotazů s ID.
Kolega si odnese: **v analytickém dokumentu je „potvrzeno kým" stejně důležité jako „co".**

**Okruh:** K (přesah A)
**Předvedatelnost:** Střední. Nejlépe na jednom odstavci specifikace: přepsat tvrzení na
„potvrdil X dne Y" vs. „pracovní předpoklad KVADOS" a ukázat, jak to změní další rozhodování.

---

### K3 — Journal session jako paměť, která přežije `/compact`

**Co to je:** Když detail zmizí z kontextu, uživatel ho nezadává znovu — pošle Claude do
záznamu konverzace, aby si ho vytáhl.

**Doklad:** *„Podívej se ještě do journalu session, zda tam zjistíš nějaké nové klíčové informace
pro tento případ. Mezitím jsem už ale spustil compact podruhé."* (2026-07-10 18:38)
Silnější varianta: *„Projdi konverzaci (journal) a vypiš do chatu, co jsem při specifikaci
mezaninu chtěl udělat záměrně jinak a důkladněji, než je v primární specifikaci… Vyberu si, co
budu chtít provést."* (2026-07-11 14:34, znovu 14:41)

**Opakování:** 8 promptů pracuje s journalem / cizí session ID (07-09 18:46, 07-10 12:21,
07-10 18:22, 07-10 18:38, 07-11 14:34/14:41, 07-30 11:43). Vzor.

**Přenositelná praxe** s malou závislostí: kolega musí vědět, **že** journal existuje a kde je.
Není to jeho vlastní infrastruktura, je to vlastnost nástroje → patří do workshopu jako
„kde je uložená vaše historie".

**Okruh:** K (přesah U)
**Předvedatelnost:** Velmi silná a efektní. Naživo: `/compact`, pak „co jsme se rozhodli o X"
→ Claude neví → „najdi to v journalu této session" → najde. Publikum si to zapamatuje.

---

### K4 — `/context` **před** `/compact` (měř, než komprimuješ)

**Co to je:** Kompakce není reflex na „je toho moc", ale reakce na změřený stav.

**Doklad:** Trojice bezprostředních sekvencí `/context` → `/compact`: 07-01 11:09, 07-02 09:52→09:53,
07-02 11:39→11:48. Celkem 8× `/context` proti 16× `/compact`.

**Opakování:** Vzor (3 přímé sekvence + 8 měření).

**Přenositelná praxe.** Nulová infrastruktura.

**Okruh:** K
**Předvedatelnost:** Velmi silná — `/context` je vizuální, publikum vidí rozpad kontextu na
systémový prompt / nástroje / konverzaci.

---

### K5 — Co je před a co po `/compact` (diagnóza, ne jen technika)

**Co to je:** Analýza 16 kompakcí ukazuje **dva různé důvody** a to je pro workshop podstatnější
než samotný příkaz.

**Doklad — typ „hranice úkolu" (zdravé):** před = dokončený krok, po = nová dávka.
07-12 08:29 *„ad 3) proveď sjednocení dle …"* → `/compact` 13:20 → *„napiš seznam zbývajících
nálezů, které je potřeba ještě opravit."* (13:23). Stejně 07-11 19:03→19:54→20:00, 07-11 21:31→21:51→21:54.

**Doklad — typ „utopený v ladění" (nezdravé):** před i po je tentýž nevyřešený bug.
07-14 07:53 *„Je tam ještě chyba že když rychle přijedou 1 2 palety tak se zaseknou…"* → `/compact`
08:18 → *„Pojďme to řešit po částech, po dílčích problémech."* (08:23).
A 07-14 13:44 → `/compact` 14:11 → 14:12 *„Ještě zde v této situaci když odeberu paletu číslo 13…"*.

**Opakování:** 16 kompakcí, z toho ~9 typ „hranice", ~5 typ „utopený", 2 režijní.

**Přenositelná praxe.** Přesná lekce: *pokud po compactu pokračuješ ve stejném ladicím kole,
compact ti nepomohl — problém není kontext, ale zadání.* U 07-14 08:18 to sám uživatel v následujícím
promptu potvrzuje (přeformuloval úlohu, ne kontext).

**Okruh:** K (přesah X)
**Předvedatelnost:** Střední — jde o vyprávěný příběh s citacemi, ne o živou ukázku.

---

### K6 — Sjednocení terminologie napříč dokumenty → zavedení do glosáře

**Co to je:** Terminologický spor se neřeší v hlavě, ale (a) rekapitulací napříč všemi dokumenty,
(b) zápisem do jednoho glosáře, (c) následnou kontrolou, kdo ještě používá starý termín.

**Doklad — celá smyčka v jednom dni (2026-07-08):**
*„Jaká terminologie se používá pro porty? … Používá se pojem 'zabezpečený port'?"* (16:58) →
*„Zaveď toto do @docs/onboarding/glossary.md"* (17:02) →
*„Místo Error port chci v glossary používat Dopravníkový error port."* (17:15) →
*„Proveď revizi"* (17:21).
Dva dny nato kontrola staré konvence: *„zkontroluj i FR-COMP-WES-STATION-002 a PTL a @temp/… ,
jestli neodkazují na starou konvenci"* (07-10 15:39).

**Opakování:** 12 promptů na terminologii/sjednocení. Vzor.

**Přenositelná praxe.** `[infra]` je jen sám glosář — a ten je jeden soubor, ne nástroj.
Kolega si odnese celou smyčku: *zjisti stav → zapiš do jednoho místa → dohledej, kdo používá staré*.

**Okruh:** K
**Předvedatelnost:** Silná. Naživo grep na starý termín po zápisu nového do glosáře.

---

### K7 — Adresát dokumentu jako parametr zadání

**Co to je:** Uživatel opakovaně nekoriguje obsah, ale **registr jazyka** podle toho, kdo
dokument bude číst.

**Doklad:** *„backlog je pro mě příliš zhuštěný a nerozumím pojmům. nepoužívej žargón, více
vysvětluj."* (2026-07-10 20:42)
*„Připrav zde do chatu srozumitelný seznam otázek (nebude obsahovat tolik odkazů) dle sekce 03"*
(07-08 22:25) — tj. varianta téhož obsahu pro externího adresáta (PAC), bez interních odkazů.
*„Připrav podklad 9 bodů pro PAC."* (07-11 21:03)

**Opakování:** 3 jasné výskyty + celý režim PLC specifikace („self-contained pro externího
dodavatele"). Vzor.

**Přenositelná praxe.** Nulová infrastruktura.

**Okruh:** K
**Předvedatelnost:** Silná. Naživo: tentýž seznam otevřených bodů vygenerovat 2× — „pro mě"
a „pro dodavatele". Rozdíl je markantní a publikum ho okamžitě pochopí.

---

### K8 — Trvanlivost odkazů: neukotvuj trvalý dokument do pracovní zóny

**Co to je:** Pravidlo o tom, kam smí a nesmí odkazovat promovaný dokument, formulované
**s důvodem**.

**Doklad:** *„V promovaných dokumentech se neodkazuj na spec/ a jeho D12 apod. spec mohou být
časem odstraněny a ADR by ztratil odkaz."* (2026-07-10 18:19)

**Opakování:** Jednorázovka (ale s trvalým následkem — stalo se z toho pravidlo).

**Přenositelná praxe** jako princip; konkrétní cesty `spec/` jsou `[infra]`.
Kolega si odnese: *odkaz z trvalého artefaktu do dočasného pracoviště je budoucí mrtvý odkaz.*

**Okruh:** K
**Předvedatelnost:** Slabá naživo, silná jako pravidlo na slidu.

---

### K9 — Obrázek jako zdroj, ne jako ilustrace

**Co to je:** 35 promptů obsahuje obrázek. Ve třech různých rolích, a jen jedna z nich je dobrá
praxe.

**Doklad — dobrá role „obrázek jako zadání/schéma":**
*„/spec Rozšíření docs\plc\… o ovládání prvků v Automatické dekantaci, Manuální dekantaci,
Předpříjmu a Severní error stanici. … Schéma automatické dekantace: [Image] Schéma manuální
dekantace: [Image] Schéma předpříjmu: [Image] Severní error stanice: [Image]"* (2026-07-11 15:28)
— čtyři výkresy jako primární vstup k pěti stránkám specifikace.
**Dobrá role „obrázek jako oprava dat":** *„Zjistil jsem chybné pojmenování SHIPING_WEST portů.
Oprav to na listech Prvky i Prvky - instance. Takto je to správně: [Image]"* (07-10 09:51).
**Slabá role „screenshot místo popisu chyby":** viz **X4**.

**Opakování:** 35 promptů. Silný vzor.

**Přenositelná praxe.** Analytik má výkresy, tabulky, snímky z XLS — a tohle je nejrychlejší
cesta, jak je dostat do zadání.

**Okruh:** K
**Předvedatelnost:** Velmi silná. Vložit výkres a nechat z něj vygenerovat tabulku prvků.

---

## 4. Anatomie dlouhých zadání (nad 1000 znaků) — jen 6 kusů

Zásadní nález: **dlouhá zadání jsou 1,4 % promptů a ve dvou různých žánrech.** Kostry:

### Žánr A — „dávka odpovědí na číslované otázky" (3 z 6)

```
[1 řádek] Zapracuj odpovědi požadované v @docs/plc/BACKLOG.md
[blank]
1. <doslovná otázka z backlogu>   [PAC/TMT]
       <odpověď uživatele>
2. <doslovná otázka>              [PAC/DWG]
       <odpověď>
…15.
[podsekce] Dohledávky u projektanta (DWG):
12. … 15. …
```
**Doklad:** 2026-07-09 21:54 (2106 znaků, 15 bodů) — nejdelší prompt měsíce. Stejná kostra
07-11 12:53 (1598 zn., body „9.1 … 9.22") a 07-30 09:21 (1049 zn., body „1, 2, 5, 6, 9, 30 …").

**Co je tam vždycky:** odkaz na dokument s otázkami; číslo bodu; odpověď; značka zdroje
(`[PAC]`, `[DWG]`).
**Co jen někdy:** přiznání „to zatím nevíme" (07-09 body 10, 13, 14 — velmi cenné, viz M4);
přiložený e-mail dodavatele; nová myšlenka na konci („Ještě přemýšlím nad tím, že…", 07-11 12:53).

**Pozorování:** Uživatel **nepřepisuje** kontext otázky. Otázka žije v dokumentu, prompt nese jen
číslo + odpověď. To je klíč k medánu 66 znaků.

### Žánr B — „zadání nové věci od nuly" (3 z 6)

```
[cíl 1 věta]        Připrav html stránku, která bude demonstrovat pohyb palet po dopravníku.
[fyzika/domain]     dopravník s 10 lokacemi, první dva segmenty jednopaletové, ostatní dvojpaletové…
[chování/interakce] simulace musí umožnit odebrat paletu kliknutím…
[nefunkční nárok]   musí fungovat v reálném čase…
[cíl znovu, jinak]  Cílem posunu … je maximální zaplněnost dopravníku, aby nevznikaly volné lokace
[příloha]           V přiloženém obrázku je ukázka…
[klauzule dotazu]   pokud [je] něco nejasnýho tak se … na to zeptej předem
```
**Doklad:** 2026-07-13 20:47 (1875 zn.) a 20:48 (1886 zn., týž text + obrázek).
Stejná kostra 07-12 16:47 (1611 zn., HTML prezentace) — tam navíc *„nejprve navrhni principy,
přístupy a možná i nějaký výzkum, který je třeba provést předtím než takovou aplikaci začneme
tvořit abychom nevymýšleli něco, co už je někde vymyšleno"* a *„Připrav tedy koncept a pak se
mě zeptej na klíčové informace, které by měl dále rozhodnout."*

**Co je tam vždycky:** cíl; doménová omezení; klauzule „zeptej se předem".
**Co chybí a chybět nemá:** **měřitelný invariant.** V obou dlouhých zadáních žánru B je cíl
popsaný slovně („maximální zaplněnost, aby nevznikaly volné lokace"), ale ne jako testovatelné
pravidlo. Následek: 30 iterací → viz **X2/A1**.

**Přenositelná praxe:** obě kostry ano — a je to nejlepší jednotlivý materiál na handout.
**Okruh:** K (žánr A), A (žánr B)
**Předvedatelnost:** Velmi silná — kostra na slidu, vedle ní reálný prompt.

---

## 5. Kandidáti — okruh M (mechanika kvality)

### M1 — Návrhová brána: „do chatu, nic neměň" ★ TOP

**Co to je:** Před zápisem do souborů si uživatel vyžádá návrh do chatu a zakáže úpravu.

**Doklad:** *„Navrhni ještě vhodnější pojmenování akce než je assignContainer. Napiš varianty
zde do chatu, nic neměň."* (2026-07-09 08:44) → o 25 minut později
*„OK, rozhodl jsem se pro containerPlaced. Oprav všude."* (09:09).
Dále: *„Připrav stručný přehled do chatu. Jedná se mi o správnou terminologii."* (07-02 12:05),
*„Vypiš do chatu … Vyberu si, co budu chtít provést."* (07-11 14:34).

**Opakování:** 10× „do chatu", z toho 5× s explicitním zákazem zápisu. **Vzor.**

**Přenositelná praxe.** Nulová infrastruktura, funguje první den. Nejlepší poměr
hodnota/náklady z celého měsíce.

**Okruh:** M
**Předvedatelnost:** Velmi silná. Naživo: tentýž úkol bez věty (Claude začne editovat soubory)
a s větou (vypíše 4 varianty s odůvodněním). Publikum vidí rozdíl v jednom kole.

---

### M2 — Rozdělený rozsah zápisu a hlášení ★ TOP

**Co to je:** V jednom promptu jsou dvě různá oprávnění: *tady oprav*, *tam jen nahlas*.

**Doklad:** *„Na list Prvky byly doplněny ESTOP tlačítka. Doplň příslušné řádky pro jednotlivé
porty také na list Prvky - instance. … Pokud najdeš ještě i jiné rozdíly, tak ty jen vypiš do
chatu ale neopravuj je."* (2026-07-10 15:54)
Stejný tvar: *„Doplň ID zařízení na list Prvky - instance … Pokud něco chybí nebo nadbývá, tak mi
to napiš do chatu, ale sám nepřidávej."* (07-11 09:47).
A na kontrolním úkolu úplně: *„Zkontroluj a vypiš rozdíly … Nic neměň."* (07-10 07:52).

**Opakování:** 4 výskyty ve třech různých dnech. Vzor.

**Přenositelná praxe.** Nulová infrastruktura. Řeší nejčastější strach analytika
(„nechci, aby mi to přepsalo dokument") lépe než zákaz práce se soubory.

**Okruh:** M
**Předvedatelnost:** Velmi silná, a je to zároveň nejlepší odpověď na obavu z autonomie.

---

### M3 — Schvalovací brána u strukturální změny

**Co to je:** Když si uživatel není jistý, že si s Claude rozumí, zastaví práci a vyžádá si
výčet k odsouhlasení.

**Doklad:** *„Nejsem si jistý, že si rozumíme. Napiš, které prvky budou součástí UDT
dopravníkových portů a které zůstanou samostatně. Potřebuji to nejprve schválit."*
(2026-07-11 11:35) — kontext: dvě předchozí kola o rozdělení UDT (10:54, 11:32) šla mimo.

**Opakování:** 4 (07-03 11:38, 07-11 11:35, 07-11 14:34, 07-11 14:41).

**Přenositelná praxe.** Formulace „nejsem si jistý, že si rozumíme — napiš mi X, potřebuji to
nejprve schválit" je přenositelná doslova.

**Okruh:** M
**Předvedatelnost:** Střední (potřebuje předchozí nedorozumění, aby vynikla).

---

### M4 — Číslované otevřené body ↔ dávková odpověď po číslech ★ TOP (vzor měsíce)

**Co to je:** Claude vede seznam otevřených otázek s čísly; uživatel odpovídá dávkou
„ad N) …", často s odpovědí **„zatím nevíme"**, což je legitimní stav, ne mezera.

**Doklad:** *„ad 1) Všechny PLC499, PLC699, PLC199, PLC299, PLC399 mají stejné UDT a využívají
RESET i START. Neplatí, že ResetPressed/StartPressed jsou instance jen PLC699. ad 2) Na ně jsem
zapomněl…"* (2026-07-12 08:28)
*„bod 3) OK / bod 6) ano poznámku. Musí odpovídat analýze rizik. / bod 5) chci koordinovanou změnu
/ 4) upravit tabulku."* (07-02 10:07)
Odpověď „nevíme": *„10. Jaká je doba přechodu vrat…? Testovací vrata jsou na cestě. PAC bude
testovat. … Zatím tedy nevíme."* (07-09 21:54)
Uzavírací příkaz: *„V seznamu otevřených bodů nech jen ty nedořešené."* (07-11 22:11).

**Opakování:** **13 promptů** ve tvaru číslované dávky. Nejsilnější vzor měsíce.

**Přenositelná praxe** v mechanismu; `[infra]` je jen persistence (`BACKLOG.md` — jeden soubor,
který si kolega založí za minutu, ne nástroj). Podstata: **Claude očísluje, člověk odpovídá číslem.**

**Okruh:** M (přesah A, O)
**Předvedatelnost:** Velmi silná. Naživo: „vypiš otevřené otázky jako číslovaný seznam" →
odpovědět na tři z nich číslem → „v seznamu nech jen nedořešené".

---

### M5 — Revize jako samostatný krok s vymezeným typem nálezu

**Co to je:** Kontrola se nezadává jako „zkontroluj to", ale s cílem a s typem hledané chyby.

**Doklad — silná varianta:** *„Reviduj @docs/plc/AlzaSk-PLC-specifikace.md a
@docs/plc/AlzaSk-PLC-specifikace-mezanin.md . Hledej vnitřní nekonzistence, rozpory, logické
chyby apod."* (2026-07-11 22:40), navazuje *„postupně také zkontroluj logiku všech diagramů."*
(22:54) a *„napiš seznam zbývajících nálezů, které je potřeba ještě opravit."* (07-12 13:23).
**Slabá varianta téhož dne:** `Reviduj` (22:39, bez cíle — okamžitě znovu odesláno s cestami).

**Opakování:** 22 promptů typu reviduj/audit/zkontroluj. Vzor.

**Přenositelná praxe** v jádru („řekni, jaký typ chyby hledáš, a nech si nálezy vypsat jako
seznam"). `[infra]`: paralelní review subagenti (`review-semantic`, `review-structural`) a
validátory — to kolega nemá.

**Okruh:** M
**Předvedatelnost:** Silná pro slabou/silnou variantu vedle sebe. Subagenti až v pokročilém dílu.

---

### M6 — Ověřovací sonda před stavbou (spike → rozhodnutí → uklizení → plán) ★ TOP

**Co to je:** Před stavbou většího celku se otestuje jediná riziková věc.

**Doklad — celá čtyřkroková smyčka v 23 minutách (2026-07-12):**
*„pojďme nejprve vyzkoušet testem, zda zobrazování mermaid diagramu ze specifikace bude v HTML
fungovat. Připrav jednoduchý test."* (17:12) →
*„Diagramy se zobrazují OK. Je ale nezbytné mít spuštěný server? Nejde to napsat do jedné html
stránky?"* (17:16) →
*„Ano, chci variantu A. Otestujme."* (17:20) →
*„Testovací soubory smaž, spusť implementační plán"* (17:35).

**Opakování:** 1 úplný výskyt, ale nejčistší v celém měsíci.

**Přenositelná praxe.** Nulová infrastruktura. Jednorázovka, ale vzorová — pro workshop je
hodnotnější než průměrný vzor.

**Okruh:** M (přesah A)
**Předvedatelnost:** Velmi silná — dá se celá odehrát naživo za 5 minut.

---

### M7 — Opakovaná korekce se povyšuje na pravidlo (a co když se to neudělá)

**Co to je:** Kontrast dvou osudů téže situace ve stejném týdnu.

**Doklad — správně (doménové pravidlo skončí v ADR):**
*„#6) Pokud je pole typu string a má pojmout n znaků, tak v datovém bloku potřebuje zabírat
velikost n+2. Sjednoť to."* (2026-07-12 14:50) → *„To pravidlo pro string n+2 zapiš do ADR."*
(14:56).
**Doklad — špatně (stylové pravidlo se opakuje 3×):**
*„Uvnitř specifikace neuváděj, co bylo přepracováno oproti předchozí verzi. Teprve tvoříme první
verzi. Důležitý je finální stav."* (07-11 11:43) →
*„Obecně nepotřebuji uvádět informace o změnách oproti předchozí verzi v textu (ponechej jen
changelog)."* (07-11 20:21) →
*„Obecně ve specifikacích neuváděj změny oproti poslední verzi (beze změny, rozšířena)."*
(07-12 08:28).

**Opakování:** 3× tatáž korekce (doloženo) vs. 1× povýšení na pravidlo.

**Přenositelná praxe.** Zásada („třetí opakování téže korekce je chyba v konfiguraci, ne
v modelu") je přenositelná. `[infra]`: kam pravidlo zapsat — `CLAUDE.md`, ADR, rules —
to už tým musí mít.

**Okruh:** M (přesah X, U)
**Předvedatelnost:** Silná jako příběh se třemi citacemi a datem. Publikum si v tom pozná sebe.

---

### M8 — Měřitelné omezení formátu výstupu

**Co to je:** Omezení výstupu číslem, ne adjektivem.

**Doklad:** *„V changelogu @docs/plc/AlzaSk-PLC-specifikace.md ponech jen jeden řádek s popisem
nejdůležitějších změn (max. 60 slov)."* (2026-07-11 13:48); *„V changelogu nech jen poslední řádek
(maximálně 80 slov)."* (07-11 22:11); *„aby dejme tomu na 3 kliknutí se člověk mohl dostat
k zařízení které ho zajímá"* (07-12 16:47).

**Opakování:** 3 výskyty. Slabší vzor, ale jednoznačný.

**Přenositelná praxe.** Nulová infrastruktura.

**Okruh:** M
**Předvedatelnost:** Silná (výsledek je měřitelný přímo na obrazovce).

---

### M9 — Formát výstupu přizpůsobený dalšímu nástroji, s odůvodněním ★ TOP

**Co to je:** Výstup se nežádá „přehledně", ale ve tvaru, který spolkne navazující nástroj —
a v promptu je řečeno **proč**.

**Doklad:** *„Napiš středníkem oddělené hodnoty: původní hodnota, nová hodnota. Pro každý sloupec
samostatně. Použiju pro funkci SVYHLEDAT při nahrazení."* (2026-07-09 22:19)

**Opakování:** Jednorázovka, ale prototypová pro analytika (Excel je jeho hlavní nástroj).

**Přenositelná praxe.** Nulová infrastruktura. Pro cílovou skupinu (analytici v Excelu) to je
nejrychlejší „aha" moment z celého materiálu.

**Okruh:** M
**Předvedatelnost:** Velmi silná — výstup se rovnou vloží do Excelu a SVYHLEDAT funguje.

---

### M10 — Zobecnění nalezené chyby („platí to i jinde?") ★ TOP

**Co to je:** Po nalezení jednoho případu se nikdy neopravuje jen ten případ; hned se ptá,
kde ještě.

**Doklad:** *„Zkontroluj, zda k obdobné situaci nemůže dojít i na jiných segmentech dopravníku,
když je tam méně nosičů."* (2026-07-14 07:29)
*„Chci 1. Zkontroluj, zda obdobně se není potřeba zachovat ještě i k dalším souborům."*
(07-07 16:08)
*„Zkontroluj, zda není potřeba doplnit ještě do jiných FR nebo TC"* (07-10 19:03)
*„zkontroluj i FR-COMP-WES-STATION-002 a PTL a @temp/… , jestli neodkazují na starou konvenci"*
(07-10 15:39)
*„Bude to platit i pro ostatní dvousegmenty."* (07-13 22:02)

**Opakování:** **5 výskytů** ve čtyřech různých kontextech (kód, konfigurace, dokumentace,
terminologie). Silný vzor.

**Přenositelná praxe.** Nulová infrastruktura. Jedna věta, obrovský efekt.

**Okruh:** M (přesah A)
**Předvedatelnost:** Velmi silná — po jakékoli opravě přidat tu větu a ukázat, co se najde.

---

### M11 — Ověření odpovědi proti druhému zdroji

**Co to je:** Uživatel nepřijme první odpověď a nechá si ji potvrdit z jiného dokumentu.

**Doklad:** *„Zjisti, zda nouzové zastavení v přízemí zastavuje všechny zóny. A zda ochranné
zastavení v AGV zóně zastaví jen AGV zónu…"* (2026-07-10 10:46) → o 9 minut později
*„Je to takto dokumentované i v analýze rizik, že e-stop u Vychystávání zastavuje jen jednu zónu?
Skutečně e-stop nezastavuje celé přízemí?"* (10:55).
Obdobně u zákaznického dotazu: *„Dává smysl tato odpověď? Má zásadní mezery?"* (07-03 12:15).

**Opakování:** 3 výskyty. Vzor.

**Přenositelná praxe.** Nulová infrastruktura. U bezpečnostně relevantních tvrzení je to
povinnost, ne zvyk.

**Okruh:** M (přesah K)
**Předvedatelnost:** Silná.

---

## 6. Kandidáti — okruh A (analytické postupy)

### A1 — Redukce na minimální případ po sérii selhání ★ TOP (nejsilnější příběh měsíce)

**Co to je:** Po šesti kolech neúspěšného ladění na plné úloze se úloha zmenší na nejmenší
konfiguraci, ve které se problém ještě projeví.

**Doklad — bod obratu:** *„Pojďme to řešit po částech, po dílčích problémech. Pokud by měl
dopravník jen segmenty Z1, Z2, Z3 a vlezou se na něj maximálně 4 palety, tak jak musí algoritmus
fungovat. To je potřeba doladit."* (2026-07-14 08:23)
**Co mu předcházelo (6 kol na plné úloze, vždy se screenshotem):** 07-13 21:16 („Je tam logická
chyba…"), 22:02, 23:00 („Opět vznikají chyby…"), 23:05, 23:16, 07-14 06:39, 07:29, 07:53
(„Je tam ještě chyba…" + 2 obrázky).
**Co následovalo:** 08:29 „ano", 08:50 jedna přesná chyba, 09:01 *„Nyní to už vypadá, že algoritmus
funguje správně."*

**Opakování:** 1 výskyt — ale jde o oblouk přes 30 promptů a ~14 hodin. Pro workshop
nejcennější jediná položka.

**Přenositelná praxe.** Nulová infrastruktura, univerzálně platné.

**Okruh:** A (přesah X)
**Předvedatelnost:** Velmi silná jako vyprávěný příběh s časovou osou 20:38 → 09:01. Naživo se
dá odehrát zkrácená verze na jednoduchém algoritmu.

---

### A2 — Specifikace invariantem místo symptomu ★ TOP (rub A1)

**Co to je:** Diagnóza, **proč** A1 bylo potřeba. Zadání popisovalo cíl slovně („aby nevznikaly
volné lokace") a chyby se pak hlásily jako symptomy ze screenshotů. Průlom přišel, až když
uživatel vyslovil **pravidlo** systému.

**Doklad — vyslovení invariantu:** *„Myslím, že tam musí být vazba mezi lokací 9 a 8. Pokud je
aktuálně paleta na lokaci 10 a zóna s lokacemi 7 a 8 se má právě posunout, tak nejprve se musí
posunout nosič z lokace 10 na lokaci 9 a pak se teprve mohou posunout lokace 7 a 8…"*
(2026-07-13 22:25)
**Doklad frustrace ze symptomového ladění:** *„Zadal jsem ti cíl, tak s…"* (07-13 22:20).
**Doklad původního slovního cíle:** *„Cílem posunu tě nosičů je maximální zaplněnost toho
dopravníku, aby tam nevznikaly žádné volné lokace."* (07-13 20:47).

**Opakování:** 1 oblouk, ale invariant se v různých formulacích objevuje 5× (21:16, 22:25,
07-14 08:23, 08:50, 09:34).

**Přenositelná praxe.** Přesně to, co analytik umí a čeho nevyužívá: **umí napsat pravidlo, ale
posílá screenshot.**

**Okruh:** A (přesah X)
**Předvedatelnost:** Silná — vedle sebe „tady je chyba [screenshot]" a „platí pravidlo: nikdy
nesmí…".

---

### A3 — „Podívej se, jak se to obvykle řeší" před vlastním návrhem

**Co to je:** Než se navrhne řešení netriviální úlohy, nechá se dohledat, jak se řeší v praxi.

**Doklad:** *„Ten algoritmus není vůbec jednoduchý. Je potřeba to pořádně promyslet a inspirovat
se na internetu, jak se obvykle takové úlohy na dopravnících řeší."* (2026-07-13 20:55)
*„…nejprve navrhni principy, přístupy a možná i nějaký výzkum, který je třeba provést předtím než
takovou aplikaci začneme tvořit abychom nevymýšleli něco, co už je někde vymyšleno."* (07-12 16:47)
*„Existují nějaké konkrétní informace, jak se budou ovládat měřící brány na dopravnících
v mezaninech? Existuje odkaz na technickou dokumentaci? Vyhledej relevantní zdroje. Ale jde jen
o dopravníky v mezaninech, ostatní mě nezajímá."* (07-10 21:28)

**Opakování:** 3 výskyty. Vzor. Třetí citace je navíc ukázka **hranice rozsahu hledání** —
samostatně cenná.

**Přenositelná praxe.** Nulová infrastruktura (u kolegy `[infra]` jen pokud nemá web přístup).

**Okruh:** A
**Předvedatelnost:** Silná.

---

### A4 — Zpětné promítnutí do starších dokumentů (harvest z konverzace)

**Co to je:** Když se při práci na novém dokumentu udělá věc lépe než v tom starém, nechá se to
najít a přenést zpět.

**Doklad:** *„Projdi konverzaci (journal) a vypiš do chatu, co jsem při specifikaci mezaninu chtěl
udělat záměrně jinak a důkladněji, než je v primární specifikaci a proto by bylo dobré to takto
sjednotit i v primární specifikaci. Vypiš jako přehledný seznam. Vyberu si, co budu chtít
provést."* (2026-07-11 14:34, znovu 14:41)
Následek: *„#8) Sjednoť mezaniny podle hlavní specifikace…"* (07-12 14:50), *„ad 3) proveď
sjednocení dle …"* (07-12 08:29).

**Opakování:** 1 zadání, ale spustilo 4 dny sjednocovací práce.

**Přenositelná praxe** — a je to unikátní move, který jsem nikde jinde v materiálu neviděl.
Kombinuje K3 (journal), M1 (do chatu) a M3 (picklist).

**Okruh:** A (přesah K, U)
**Předvedatelnost:** Střední-silná (vyžaduje delší session, ale dá se udělat na 30minutové).

---

### A5 — Křížová kontrola dokument × dokument × výkres ★ TOP

**Co to je:** Nejčastější analytická operace měsíce: dva nezávislé podklady se položí proti sobě
a hlásí se rozdíly.

**Doklad:** *„V dokumentu C:\Temp\Alza.drawio je na více listech přehled HW prvků v jednotlivých
patrech. Každý prvek má svůj piktogram. Zkontroluj a vypiš rozdíly, kdy to neodpovídá nebo to
není možné ověřit, že tyto prvky nejsou zaznamenané v tabulce @docs/analysis/Seznam_prvku_…xml na
listu 'Prvky - instance'. Nic neměň."* (2026-07-10 07:52)
Další: XLSX × `initData.json` (07-09 21:08), XML × PLC spec × SVG (07-10 11:54), PLC spec ×
spec mezaninu (07-11 22:40), ADR × FR × PTL × temp (07-10 15:39).

**Opakování:** 6+ výskytů. Silný vzor. Všimni si, že je vždy kombinovaný s **M2** („nic neměň").

**Přenositelná praxe.** Nulová infrastruktura. Nejlepší „první úloha" pro nováčka —
je bezpečná (nic nezapisuje) a výsledek je okamžitě užitečný.

**Okruh:** A
**Předvedatelnost:** Velmi silná. Doporučuju jako hlavní živou ukázku workshopu.

---

### A6 — Varianty pojmenování před rozhodnutím, pak hromadné přejmenování

**Co to je:** Pojmenování se nerozhoduje intuitivně — nechá si vypsat varianty s odůvodněním,
rozhodne, a přejmenování pak proběhne jedním příkazem napříč repozitářem.

**Doklad:** *„Navrhni ještě vhodnější pojmenování akce než je assignContainer. Napiš varianty zde
do chatu, nic neměň."* (2026-07-09 08:44) → *„OK, rozhodl jsem se pro containerPlaced. Oprav
všude."* (09:09).
Argumentované odmítnutí návrhu: *„Pro pojemnování UDT_ShippingLane bych raději místo Shipping
volil Conveyor nebo něco podobného, aby UDT se případně dalo použít i na jiné segmenty dopravníku
s podobnou funcí (zatím takové ale nemáme)."* (07-11 12:18)
Terminologická rešerše: *„pojem hoist není v tomto kontextu úplně přesný… Lift – nejběžnější a
nejvhodnější označení… Jak to máme v jiných částech dokumentace? Je lift vhodné?"* (07-11 13:11)

**Opakování:** 4 výskyty. Vzor.

**Přenositelná praxe.** Nulová infrastruktura. Pozor: „Oprav všude" je bezpečné jen s verzováním
→ patří k tomu poznámka o gitu.

**Okruh:** A
**Předvedatelnost:** Silná.

---

### A7 — „Co mám nyní rozhodnout?" — frontu rozhodnutí drží asistent

**Co to je:** Uživatel se ptá na svůj vlastní seznam úkolů.

**Doklad:** *„Co mám nyní rozhodnout?"* (2026-07-02 09:35)
*„/btw Kde najdu zapsané otázky, které je potřeba rozhodnout?"* (07-11 20:49)
*„Čím dálle nejlépe mám pokračovat?"* (07-11 20:52)
*„Proveď zmapování, které oblasti PLC specifikace jsou již zpracované, které jsou rozpracované
nebo dočasně uložené. Potřebuji přehled, abych věděl, kde je nyní potřeba pokračovat."*
(07-08 20:40)

**Opakování:** 4 výskyty. Vzor.

**Přenositelná praxe.** Nulová infrastruktura pro variantu „zmapuj stav dokumentu"; `[infra]`
pro variantu „kde jsou zapsané otázky" (potřebuje backlog/registr).

**Okruh:** A (přesah O)
**Předvedatelnost:** Silná — a je to velmi „lidský" moment, který publikum ocení.

---

### A8 — Cizí dotaz/odpověď jako vstup k posouzení ★ TOP

**Co to je:** E-mail zákazníka nebo dodavatele se vloží celý a úkol je *posoudit*, ne jen
odpovědět.

**Doklad — varianty řešení:** *„Zákazník Alza poslal níže uvedený dotaz. Jaké jsou varianty
řešení? Dokáže WMS rozpoznat přiřazený nosič například podle portu, kde bude nosič přistavený?
Je skutečně nutné rozšiřovat API?"* + doslovný text dotazu (2026-07-03 11:38)
**Kontrola vlastní odpovědi před odesláním:** *„Dává smysl tato odpověď? Má zásadní mezery?"*
+ doslovný text (07-03 12:15)
**Vysvětlení cizího technického vstupu:** *„Od pana Černého jsem e-mailem dostal následující
informace: … Vysvětli mi, co by to mohlo znamenat?"* (07-01 09:40)
**Formulace dotazu zpět:** *„Napiš dotazy na dodavatele: pochopil jsem správně, že operátor bude
mít k dispozici tlačítko override i RESET? … Sepiš příklad sekvenčního diagramu, jak by proces
v případě zaseknutí nosiče … měl fungovat."* (07-01 10:13)

**Opakování:** 5+ výskytů, různé role (vysvětli / posuď / navrhni varianty / formuluj dotaz).
Silný vzor.

**Přenositelná praxe.** Nulová infrastruktura. Přesně sedí na denní práci analytika.
`[infra]` jen pro evidenci (registr dotazů dodavatelům).

**Okruh:** A
**Předvedatelnost:** Velmi silná. Doporučuju jako druhou hlavní živou ukázku — s anonymizovaným
e-mailem.

---

### A9 — Diagram jako artefakt k revizi, ne jako obrázek

**Co to je:** Sekvenční diagramy se revidují stejně jako text — hledá se v nich logická chyba,
chybějící blok, nekonzistence napříč sadou.

**Doklad — připomínka kolegyně jako vstup:** *„U diagramu D2, D3 a D4 stále není to HW tlačítko,
i když v D1 už je - Je to stejná situace. U odvozu nosiče z portu už nedáváme to ten context
portDispatch? V D6, D7 a D8 máš u odvozu periodicSupply/order"* (2026-07-01 11:11)
*„Kolegyně namítá: V tom diagramu D4 … tam není to HW tlačítko. Ale podle mě ten proces bude
stejný, taky bych tam dala ten blok SAFETY-OPEN-PRE-RECEIPT"* (07-07 19:25)
*„Jaký je důvod té výjimky 'D9 je dokumentovaná výjimka, kde orderCompleted přichází před
otevřením portu.'?"* (07-03 10:10)
*„postupně také zkontroluj logiku všech diagramů."* (07-11 22:54)

**Opakování:** 8+ promptů o diagramech. Silný vzor.

**Přenositelná praxe.** Nulová infrastruktura (Mermaid v md). Podstatné: diagram je **text**,
proto se dá revidovat a diffovat. To je pro analytiky nová informace.

**Okruh:** A (přesah M)
**Předvedatelnost:** Velmi silná — Mermaid v markdownu, změna jednoho řádku, diff.

---

### A10 — Zdroj pravdy jednou, generování odjinud (argumentované rozhodnutí)

**Co to je:** Rozhodnutí o formátu artefaktu se dělá podle **budoucích změn**, ne podle
pohodlí teď — a v promptu je uveden důvod.

**Doklad:** *„Diagramy neukládej do SVG, ale ponech v mermaid formátu. Budou se zobrazovat online
nástrojem (nepotřebuji mermaid runtime). Čeká nás v budoucnu hodně změn a nechci složité
generování svg při každé změně. … Ideální by bylo, kdyby se diagramy v HTML rovnou načítaly ze
specifikací, aby se změny ve specifikacích hned promítly i do HTML."* (2026-07-12 17:01)
Důsledek nedodržení téhož principu jinde: *„Změny v kódování ID zařízení nejsou promítnuté do
svg"* (07-11 20:40).

**Opakování:** 1 rozhodnutí + 1 doklad ceny za jeho nedodržení. Silný pár.

**Přenositelná praxe.** Nulová infrastruktura. A ta druhá citace je nejlepší možný argument.

**Okruh:** A (přesah M)
**Předvedatelnost:** Střední-silná.

---

## 7. Kandidáti — okruh O (orchestrace)

### O1 — Runbook jako předávka mezi sessions / repozitáři

**Co to je:** Práce se rozdělí: v jedné session se naplánuje a ověří, výstupem je *runbook*,
který se v druhé session (jiný repozitář) provede.

**Doklad:** *„Adopce pluginu Spec Factory. Plán adopce Spec Factory pro Alzu hotový a schválený;
Část A (sjednocení pluginu) provedena a otestována (76 testů zelených, necommitnuto na
dev/martint), Část B předána jako ověřený runbook ADOPTION-ALZA-RUNBOOK.md k provedení z Alza CC
session přes bránu E2."* (2026-07-07 14:22) → tentýž text znovu s cestou:
*„…viz C:\git\shared\plugins\docs\ADOPTION-ALZA-RUNBOOK.md."* (14:23)
Obdobně, ale menší: uživatel si nechal napsat migrační postup a pak ho krok za krokem odklikal
jako 6 samostatných promptů — *„1. /plugin uninstall … 2. /plugin marketplace remove … 3. /plugin
marketplace add C:\Git\shared … 4. /plugin install …"* (07-09 09:25 a pak 09:26–09:28).

**Opakování:** 2 výskyty (velký + malý). Vzor.

**Přenositelná praxe** v principu (*„výstupem plánovací session je soubor, ne odpověď v chatu"*).
`[infra]` je konkrétní obsah runbooku a existence druhého repozitáře.

**Okruh:** O
**Předvedatelnost:** Silná pro malou variantu (nech si napsat postup → vykonej krok za krokem);
slabá pro velkou (příliš specifické).

---

### O2 — Jedna session = jedno téma, pojmenované

**Co to je:** Práce se dělí na tematické sessions; první prompt je často jen název tématu
a session se přejmenovává.

**Doklad — tematické hlavičky jako první prompt:** „Adopce pluginu Spec Factory" (07-07 14:22),
„Instalace pluginu knowladge-loop" (07-09 09:11), „Alza sjednocení znalostní smyčky" (07-09 18:31),
„Alza PLC dekantace a předpříjem" (07-11 15:25), „Prezentace zařízení" (07-12 16:43),
„Body z jednání" (07-13 18:34), „Upravení diagramů" (07-07 19:23), „Úpravy API" (07-30 08:58).
Plus `/rename` 3× a `/resume` 6×.

**Opakování:** 8 tematických hlaviček. Silný vzor.

**Přenositelná praxe.** Nulová infrastruktura. Přímý důsledek: journal se dá dohledat (K3),
`/resume` má smysl.

**Okruh:** O
**Předvedatelnost:** Velmi silná — `/resume` se seznamem pojmenovaných sessions vs. seznamem
„Untitled".

---

### O3 — Volba modelu a úsilí per úkol + gotcha se subagenty

**Co to je:** Model a effort nejsou nastavení, ale volba k úkolu. A jeden konkrétní gotcha:
volba se nepropaguje do subagentů.

**Doklad — volba k úkolu:** *„Proveď revizi diagramů modelem Fable 5."* (2026-07-03 10:30)
**Gotcha:** *„Subagent nemá nastaven model Fable!"* (07-03 11:52)
**Meta-dotaz na správný výběr:** *„Na internetu zjisti hlavní výhody a schopnosti modelu Claude
Fable 5. Potom projdi mé předchozí sessions a zjisti, které úkoly jsem řešil a Fable 5 by byl pro
ně ideálním řešením. Pak navrhni, na které úloze bych mohl Fable 5 vyzkoušet, abych mohl porovnat
rozdíl."* (07-04 21:05)
**Rozpočtové omezení jako součást zadání:** *„Potřebuji používat jen modely Haiku, Sonnet a Opus
v těchto agentech."* (07-04 21:25)

**Opakování:** 19× `/model`, 3× `/effort`, 25 promptů zmiňujících model/effort. Silný vzor.

**Přenositelná praxe** pro princip a pro gotcha. `[infra]`: definice agentů s modelem
ve frontmatteru.

**Okruh:** O (přesah N)
**Předvedatelnost:** Silná pro gotcha (spustit subagenta a ukázat, jaký model mu vlastně běží).

---

### O4 — Druhý pár očí jiným modelem

**Co to je:** Revizi vlastního výstupu dělá jiný model / jiný agent než ten, který ho napsal.

**Doklad:** *„Proveď revizi návrhů modelem Fable. Důležité je, že WMS posílá i objednávky dle SKU,
tím pádem WMS nezná konkrétní containerId těchto zdrojových nosičů."* (2026-07-03 11:48)
*„@'spec-critic (agent)' Reviduj toto řešení (diagramy, FR, TC)"* (07-02 12:00)
*„Chci modelem Fable 5 revidovat mé agenty tvořící Spec Factory. Zjisti, zda stávající systém je
funkční, plní dobře svou funkci, je efektivní a ekonomický."* (07-04 21:25)

**Opakování:** 4 výskyty. Vzor.

**Přenositelná praxe** v jádru (jiný model / čistá session na revizi). `[infra]`: pojmenovaní
agenti (`spec-critic`).

**Okruh:** O
**Předvedatelnost:** Silná.

---

### O5 — Migrace nástroje není hotová, dokud nezmizel starý vstupní bod

**Co to je:** Po adopci pluginu uživatel dvakrát narazí na to, že v repozitáři zůstal starý
lokální příkaz, a pak nález zobecní.

**Doklad:** *„Proč stále zůstává C:\Git\alzask\.claude\commands\spec.md? Myslel jsem, že bude
nahrazený tím pluginem."* (2026-07-07 16:02) — **a znovu tentýž prompt v 19:29** (tj. ani po
prvním kole nebylo hotovo) → *„Chci 1. Zkontroluj, zda obdobně se není potřeba zachovat ještě
i k dalším souborům."* (16:08)
Souvisí: 5× `/spec` (staré) proti 2× `/spec-factory:spec` (nové) — v jednom promptu i **oba
zaráz**: *„/spec-factory:spec /spec Rozšíření docs\plc\…"* (07-11 15:30). Doklad, že přechod
na nový vstupní bod trvá i uživateli, ne jen repozitáři.

**Opakování:** 2 identické dotazy + 1 hybridní volání. Vzor.

**Přenositelná praxe.** Princip („migrace = nový vstupní bod funguje **a** starý neexistuje")
je univerzální; konkrétní cesty `[infra]`.

**Okruh:** O (přesah N, X)
**Předvedatelnost:** Silná — `ls .claude/commands` po adopci pluginu.

---

### O6 — Kompletní příběh adopce pluginu (07-04 → 07-11)

**Co to je:** Oblouk problém → improvizace → zafixování do nástroje, doložený den po dni.
**Nejlepší narativní materiál celého měsíce pro workshop.**

**Časová osa s doklady:**

| Datum | Prompt (zkráceně) | Fáze |
|---|---|---|
| 07-02 12:00 | *„@'spec-critic (agent)' Reviduj toto řešení"* | lokální agenti fungují |
| 07-04 21:25 | *„Chci modelem Fable 5 revidovat mé agenty tvořící Spec Factory. Zjisti, zda stávající systém je funkční…"* | audit vlastního nástroje |
| 07-04 21:46 | *„Proveď: P1, P2, P3, P4, P5, P6. Spec Factory jsem začal zpracovávat jako samostatný plugin"* | rozhodnutí |
| 07-05 01:02 | `/plugins`, `/reload-plugins` | první pokus |
| 07-07 14:22 | *„Adopce pluginu Spec Factory … Část B předána jako ověřený runbook"* | řízená adopce (O1) |
| 07-07 15:02–16:08 | *„je možné pokračovat?"*, *„Jak přesně mám restart provést?"*, `/resume` ×4, *„spustil jsem"*, *„hotovo"* | **režie a friction** |
| 07-07 15:58 | *„V Git jsi vytvořil samostatnou větev. já obvykle commituju do dev/martint. Přesuneš mi tam ty změny nebo to není vhodné?"* | nečekaný git stav |
| 07-07 16:02 + 19:29 | *„Proč stále zůstává … spec.md?"* (2×) | nedoklizený starý vstup (O5) |
| 07-09 09:25–09:28 | 6 promptů odinstalace/instalace marketplace | přejmenování marketplace |
| 07-10 21:04 | *„/spec-factory:spec O4 — Přepracování specifikace mezaninu, viz backlog"* | **nový nástroj v produktivním provozu** |

**Poučení, které z toho pro workshop plyne (a je doložené):** samotná adopce zabrala ~4 dny
a v tom asi **14 promptů čisté režie** (restart, `/resume`, `/reload-plugins`, dohledávání
zbytků). To je realistický obraz, který kolegům řekne pravdu: nástroj se nezavede „mezi řečí".

**Přenositelná praxe** jako varování a jako checklist adopce. Konkrétní plugin je `[infra]`.
**Okruh:** O (přesah N)
**Předvedatelnost:** Silná jako příběh s časovou osou; ta tabulka je hotový slide.

---

## 8. Kandidáti — okruh U (učení)

### U1 — „Díky čemu se to podařilo? Bude to fungovat i příště?" ★ TOP

**Co to je:** Když něco neočekávaně vyjde, uživatel se neposune dál — zjistí příčinu a uloží ji.

**Doklad:** *„Exportuj ještě diagram do svg"* (2026-07-01 10:26) → *„Díky čemu se to podařilo?
Bude možnost exportu i příště?"* (10:45) → *„ulož do paměti"* (10:48).

**Opakování:** 1 úplná trojice (ale je to nejkompaktnější příběh v celém materiálu — tři prompty,
22 minut, trvalý výsledek).

**Přenositelná praxe.** Nulová infrastruktura (`ulož do paměti` je vestavěná funkce).

**Okruh:** U
**Předvedatelnost:** Velmi silná. Tři prompty se dají odehrát za 2 minuty a jsou dokonalý
mikro-příběh na otevření okruhu.

---

### U2 — „Co je z toho poučení a jak to zafixovat?" ★ TOP

**Co to je:** Po sérii nalezených mezer se neptá „oprav to", ale „jakou znalost z toho vytěžit,
aby to příště nevzniklo".

**Doklad:** *„Co je poučením z těch gaps, které jsem zjistil a zadal jsem k opravě? Jakou znalost
z toho můžeme pro příště vytěžit, aby SpecFactory dokázal vyřešit lépe?"* (2026-07-10 19:36)
Kontext: bezprostředně předtím čtyři korekce téhož výstupu (18:30, 18:36, 19:03, 19:14) a
metodická korekce *„Proč v sekvenčním diagramu je uvedeno ADR (containerId, ADR-ASK-API-013).
To obvykle neděláme, ne?"* (19:36).

**Opakování:** 1 výskyt, ale je to explicitní jméno celého principu znalostní smyčky.

**Přenositelná praxe.** Nulová infrastruktura pro *otázku*; `[infra]` pro *zafixování*
(kam poučení uložit).

**Okruh:** U
**Předvedatelnost:** Silná — a je to nejlepší uzavření celého workshopu.

---

### U3 — Ptát se nástroje na jeho vlastní konfiguraci ★ TOP

**Co to je:** Když se Claude chová nějak, uživatel se nehádá — zjistí, odkud to chování pochází.

**Doklad:** *„Jakým stylem máš odpovídat?"* (2026-07-08 17:12) → o 4 minuty později
*„Kde je tato instrukce uložena?"* (17:16).

**Opakování:** 1 dvojice. Jednorázovka, ale nejlepší poměr délka/hodnota v celém souboru.

**Přenositelná praxe.** Nulová infrastruktura. Přímo řeší nejčastější problém nováčka
(„nevím, proč to dělá, co dělá").

**Okruh:** U (přesah N)
**Předvedatelnost:** Velmi silná. Dvě otázky, okamžitá odpověď, publikum pochopí, že `CLAUDE.md`
je kniha pravidel a dá se na ni ukázat prstem.

---

### U4 — Doménové učení analytika přes Claude

**Co to je:** Analytik používá Claude, aby se doučil doménu, ve které specifikuje.

**Doklad:** *„Vysvětli mi, co by to mohlo znamenat?"* (2026-07-01 09:40, k mutingu závory)
*„Přepokládal jsem, že u dopravníku bude jen RESET tlačítko. Znamená to, že někde musí být ještě
zcela jiné tlačítko?"* (07-01 10:01) — hypotéza + žádost o vyvrácení
*„Co je to LOTO?"* uprostřed jinak technického promptu (07-11 09:47)
*„Nastuduj architekturu @docs/plc/sources/BullsEye-PLC-architecture-2026-07-10.xlsx a vysvětli
nejdůležitější body."* (07-10 13:47)
*„Vysvětli základní koncept disaster recovery plan."* + cesta ke spec (07-30 13:35)

**Opakování:** 6+ výskytů. Silný vzor.

**Přenositelná praxe.** Nulová infrastruktura. Pro cílovou skupinu (analytici bez HW/PLC pozadí)
zásadní.

**Okruh:** U
**Předvedatelnost:** Silná. A stojí za to zmínit vzor „hypotéza + žádost o vyvrácení" (07-01 10:01)
zvlášť — je lepší než holé „vysvětli mi".

---

### U5 — Forenzní analýza vlastní session

**Co to je:** Když výsledek neodpovídá očekávání, uživatel nechá Claude analyzovat, co se v jeho
předchozí session stalo.

**Doklad:** *„Analyzuj, proč v Session ID: 18816e0c… byl do changelogu přidána verze 0.7, když
poslední verze byla 0.8. Je to chyba? Je to problém slabšího modelu nebo nastaveného nízkého
úsilí?"* (2026-07-10 12:21)
*„V Session ID: bb69d26c… jsem provedl compact na modelu haiku. Pak se mi ale znovu zaplnil
context na cca 60 %. Co a proč se stalo?"* (07-10 18:22) → *„ano prověř podrobněji"* (18:30)
*„Líbil se mi výsledek, který jsem dostal v Session ID: a26dff63… Jak bych měl nyní zadat prompt,
abych dostal obdobný výsledek?"* (07-30 11:43)

**Opakování:** 3 výskyty. Vzor.

**Přenositelná praxe.** Nulová infrastruktura. Ta třetí citace je samostatně nejcennější:
**reverzní inženýrství promptu z výsledku, který se povedl.**

**Okruh:** U (přesah K, N)
**Předvedatelnost:** Velmi silná pro třetí variantu.

**Pozor — poloviční antipattern:** v první citaci uživatel hledá vysvětlení v modelu/effortu,
zatímco skutečná příčina je „pravidlo o changelogu nebylo vynucené bránou". Viz **X6**.

---

## 9. Antipatterny (okruh X) — plnohodnotný výstup

### X1 — Bezcílný imperativ: 11 promptů odesláno bez cíle a hned znovu s cestou ★ TOP

**Co to je:** Prompt odejde jako holý rozkaz bez uvedení souboru a musí být znovu odeslán
s doplněnou cestou. Čistá režie.

**Doklad (11 doložených párů):**
| Neúplný | Doplněný |
|---|---|
| *„V dokumentu"* (07-10 07:14) | *„V dokumentu @docs/analysis/Seznam_prvku_ALZA_2026-07-10.xml na listu Prvky je seznam HW zařízení…"* (07:20) |
| *„Oprav barevné signalizace podle nových změn v"* (07-10 14:52) | *„…v C:\Git\alzask\docs\adr\hw\ADR-ASK-HW-001.md"* (14:54) |
| *„Nastuduj architekturu a vysvětli nejdůležitější body."* (07-10 13:46) | *„Nastuduj architekturu @docs/plc/sources/BullsEye-PLC-architecture-2026-07-10.xlsx a…"* (13:47) |
| *„Doplňuji info"* (07-10 16:26) | *„Doplňuji info do @docs/plc/BACKLOG.md : Reset tlačítko: ER12-SB3C4…"* (16:28) |
| *„Navrhni nejvhodnější pojmenování"* (07-09 21:04) | +sloupce, list, XLSX, zdroje (21:06, 21:08 — **tři** kola) |

Stejná vada bez opravy: `Proveď opravy` (07-08 21:55), `Reviduj` (07-11 22:39),
`backlog aktualizuj` (07-11 14:00), `proveď revizi` (07-01 13:32), `Proveď revizi` (07-08 17:21).

**Opakování:** **11 doložených dvojic + 5 samostatných.** Nejčastější vada měsíce.

**Přenositelná lekce.** Jedna věta na slide: *„Rozkaz bez cíle není zadání."* Kolega si odnese
kontrolní seznam: **co, kde (cesta), z čeho (zdroj), kam (výstup).**

**Okruh:** X (přesah K)
**Předvedatelnost:** Velmi silná — pár promptů vedle sebe je sám sobě argumentem.

---

### X2 — Ladění screenshoty místo invariantu: 30 promptů na jeden algoritmus ★ TOP

**Co to je:** Chyba se hlásí jako snímek stavu („v této situaci když odeberu paletu 13…"),
ne jako porušené pravidlo. Vede k dlouhé sérii lokálních záplat.

**Doklad — 8 kol s obrázkem během 14 hodin:** 07-13 21:16, 22:02 (2 obr.), 23:00 (1 obr.),
23:05 (2 obr.), 23:16 (1 obr.), 07-14 06:39 (1 obr.), 07:29 (2 obr.), 07:53 (2 obr.).
Reprezentativní citace: *„Když v této situaci odeberu paletu 8, tak se pousune i paleta 16 a není
již možné vložit další paletu, přestože na dopravníku jsou dvě volné lokace."* (07-13 22:02)
**Cena:** ~30 promptů, 07-13 20:38 → 07-14 14:38. Průlom až u **A1** (redukce na 4 palety).

**Opakování:** 1 velká epizoda, ale je z ní vidět všechno.

**Přenositelná lekce.** *Screenshot říká, co se stalo. Invariant říká, co se stát nesmí. Model
umí opravit jen to druhé.*

**Okruh:** X (rub: A1, A2)
**Předvedatelnost:** Velmi silná jako příběh.

---

### X3 — Mikro-iterace UI po jednom promptu: ~25 kol na jednom HTML

**Co to je:** Vizuální ladění se zadává po jedné drobnosti, každá jako samostatný prompt.

**Doklad (07-12, 21:18 → 22:19, ~60 minut):** *„Vlastně Tam nepotřebuji zobrazovat vůbec číslo
a řádku."* (22:07, **odesláno 2×**) → *„Byl to záměr, že bubliny těch jednotlivých komentářů jsou
vertikálně nalepené tak těsně za sebou?"* (22:09) → *„Chybí možnost upravit a smazat pod
komentář."* (22:11) → *„Tak tlačítko a 3 teček mají kolem sebe to ještě 2 rámeček. Ten vnější
rámeček tam nechci, není to moc hezké."* (22:18) → *„A U pod komentářů to tlačítko překáží…"* (22:19)

**Opakování:** ~25 promptů v jedné epizodě + druhá obdobná (07-12 18:38–20:20).

**Přenositelná lekce — dvojí.** (1) Když jde o vzhled, dávkuj — sepiš 5 nedostatků do jednoho
promptu. (2) Když jde o vzhled **a nevíš, co chceš**, tak je iterace legitimní a levná — ale
patří do jiné session než analytická práce. Uživatel to sám nakonec udělal správně:
*„/frontend-design:frontend-design Předělej simulátor na profesionální vzhled."* (07-14 09:21) —
jeden prompt místo dvaceti.

**Okruh:** X
**Předvedatelnost:** Silná — kontrast „25 promptů" vs. „jeden prompt s designovým skillem".

---

### X4 — Ladění modelu a úsilí bez srovnávací základny ★ TOP

**Co to je:** Osm změn modelu/effortu v příkazu během 2 hodin, každá otestovaná jedním spuštěním,
bez zafixovaného vstupu a bez uložené referenční odpovědi. Konec: revert.

**Doklad — časová osa 2026-07-30:**
09:03 *„Uprav /body-z-jednani tak, aby používal Haiku a low effort"* → 09:04 *„Zároveň není potřeba
na extrakci spouštět subagenta"* → 09:23 *„Nechtěl jsem vytvářet nového agenta, ale upravit toho
stávajícího."* → 09:30 *„Proveď změnu: střední effort"* → 09:39 *„Proveď ještě změnu na Sonnet,
medium. Přidej agentovi parametr effort."* → 09:54 *„Změň ještě na Haiku a effort high"* →
10:02 parametrizace modelu i effortu → 10:06 *„Změnil jsem názor. Chci jen jednoho agenta."* →
mezitím 8× `/body-z-jednani 30` jako test → 10:49 **„Jaký model a effort byl používaný předtím,
než jsme začali provádět dnešní změny?"** → 11:57 **„Pořád dostávám jiný výsledek, než tomu bylo
dříve. Vrať proto zpět dnešní změny a chci pak vyzkoušet znovu."**

**Opakování:** 1 epizoda, ~20 promptů. Ale úplně čitelná.

**Přenositelná lekce.** *Než začneš ladit model a effort: zafixuj vstup, ulož referenční výstup,
poznač si výchozí nastavení.* Otázka v 10:49 je doklad, že se ztratila výchozí hodnota — tedy
i cesta zpět.

**Okruh:** X (přesah N, O)
**Předvedatelnost:** Velmi silná — časová osa se dvěma závěrečnými citacemi je hotový slide.

---

### X5 — Dvojité odeslání téhož promptu po přepnutí modelu

**Co to je:** 24 párů identických promptů. Většina vzniká tak, že uživatel prompt odešle, pak
zjistí, že chce jiný model, přepne (`/model`) a odešle znovu.

**Doklad:** *„Proveď zmapování, které oblasti PLC specifikace jsou již zpracované…"* (07-08 20:40)
→ `/model` (20:40) → tentýž prompt znovu (20:40). Stejně 07-08 20:53, 07-10 14:54–14:55
(tam navíc `/model sonnet`, `/model sonnet --help`, `/model` — tři pokusy o přepnutí).

**Opakování:** 24 párů (po odečtení skutečných iterací zůstává ~10 čistě režijních).

**Přenositelná lekce.** *Model si vyber, než napíšeš prompt* — a naučte se, že `--help`
u `/model` nefunguje tak, jak se zdá.

**Okruh:** X (přesah N)
**Předvedatelnost:** Silná, drobná.

---

### X6 — Vysvětlování chyby modelem místo chybějící brány

**Co to je:** Když výstup neodpovídá pravidlu, první hypotéza je „slabší model / nízké úsilí",
ne „pravidlo není nikde vynucené".

**Doklad:** *„Analyzuj, proč … byl do changelogu přidána verze 0.7, když poslední verze byla 0.8.
Je to chyba? Je to problém slabšího modelu nebo nastaveného nízkého úsilí?"* (2026-07-10 12:21)
Protipól ve stejném týdnu, kde to uživatel udělal správně: *„To pravidlo pro string n+2 zapiš do
ADR."* (07-12 14:56).

**Opakování:** 1 jasný výskyt (+ celá epizoda X4 je téhož druhu).

**Přenositelná lekce.** *Pravidlo, které má platit vždy, nepatří do promptu ani do modelu —
patří do brány (validátor, `CLAUDE.md`, ADR).* Tohle je zároveň nejlepší most k okruhu N.

**Okruh:** X (přesah N, M)
**Předvedatelnost:** Střední.

---

### X7 — Diktovaný prompt s přepisovými chybami

**Co to je:** Dlouhá zadání jsou zřejmě diktovaná a obsahují chyby, které mění význam.

**Doklad:** *„Prostuduji si tedy tyto dokumenty a nejprve navrhni principy…"* (07-12 16:47 —
má být „Prostuduj si"; v tomto tvaru je to výrok o uživateli, ne pokyn).
*„Promyslí dobře algoritmus kdy se který do Prahy vník musí roztočit pokud jim něco nejasnýho tak
jsem je na to zeptej předem."* (07-13 20:47 — „dopravník" → „do Prahy vník").
*„paletu odebrat le jste posleprvní dní lokace planeta odjede"* (tamtéž).

**Opakování:** 3 ze 6 dlouhých promptů. U žánru B pravidlo.

**Přenositelná lekce — vyváženě.** Diktování je pro dlouhá zadání **správná** volba (jinak by
nevznikla). Ale: přečti si to před odesláním, hlavně imperativy a doménové termíny. Claude si
„do Prahy vník" domyslí, ale „Prostuduji" vs. „Prostuduj" mění zadání.

**Okruh:** X
**Předvedatelnost:** Silná a odlehčující (publikum se zasměje a zapamatuje si to).

---

### X8 — `pokračuj` jako plnohodnotný prompt

**Co to je:** 9 promptů je jen „pokračuj" / „POKRAČUJ" / „ok pokračuj". Funguje, ale nese nulovou
informaci — a při přerušení kontextu (compact) je to nejhorší možný vstup.

**Doklad:** „POKRAČUJ" (07-03 16:09), „pokračuj" (07-07 15:11, 15:50, 20:26, 07-09 09:22,
07-30 09:04, 09:28), „ok pokračuj" (07-03 12:31), „Pokračuj. Prohoď modré a zelené tlačítko…"
(07-13 21:30 — tady správně, s doplněním).

**Opakování:** 9 výskytů.

**Přenositelná lekce.** Po compactu nebo po delší pauze místo „pokračuj" napiš „pokračuj X —
zbývá Y". Poslední citace je vzor toho lepšího tvaru.

**Okruh:** X
**Předvedatelnost:** Střední.

---

## 10. Kandidáti — okruh N (nastavení)

### N1 — Zafixování opakované instrukce (a zjištění, kde vlastně žije)

**Doklad:** *„Zaveď toto do @docs/onboarding/glossary.md"* (07-08 17:02); *„Kde je tato instrukce
uložena?"* (17:16); *„To pravidlo pro string n+2 zapiš do ADR."* (07-12 14:56);
*„ulož do paměti"* (07-01 10:48); *„Ano, aktualizuj verzní razítko i příště"* (07-14 14:38).
**Opakování:** 5 výskytů. Vzor.
**Přenositelná praxe** — a je to jádro okruhu N. `[infra]` je jen struktura (`CLAUDE.md`, ADR,
rules); to je ale právě to, co má workshop naučit postavit.
**Okruh:** N | **Předvedatelnost:** Velmi silná.

### N2 — Subagent nedědí volbu modelu

**Doklad:** *„Subagent nemá nastaven model Fable!"* (07-03 11:52).
**Opakování:** 1× — ale je to reálný gotcha, který kolegu zaskočí.
**Přenositelná praxe** (vlastnost nástroje). **Okruh:** N | **Předvedatelnost:** Silná.

### N3 — Režie pluginů a skillů je viditelná

**Doklad:** 8× `/reload-plugins`, 6× `/plugins`, 1× `/reload-skills`, `/reload-plugin` (překlep),
6 promptů přeinstalace marketplace (07-09 09:25–09:28), *„Jak přesně mám restart provést?"*
(07-07 15:06).
**Opakování:** ~20 promptů čisté nástrojové režie.
**Přenositelná praxe** jako **očekávání** („počítej s tím, tady je postup"), nikoli jako technika.
**Okruh:** N | **Předvedatelnost:** Střední — spíš čestná poznámka v úvodu.

### N4 — Nastavení nasazená na diagnózu, ne na dojem

**Doklad:** *„Proveď analýzu mého lokálního počítače a zjisti, co jej aktuálně nejvíce zatěžuje
a zpomaluje. Zda je problém s pamětí, sítí, diskem nebo něčím jiným."* (07-30 11:02) →
*„Ano, proveď úpravu settings"* (11:48) → *„Provedl jsem restart. Je to nyní už OK?"* (11:58).
**Opakování:** 1 epizoda (~10 promptů).
**Osobní zvyk / `[infra]`** — obsah je specifický pro stroj uživatele. Přenositelný je jen tvar
otázky („zjisti a rozhodni mezi hypotézami A/B/C"), který už pokrývá A8.
**Okruh:** N | **Předvedatelnost:** Slabá pro workshop analytiků. **Nedoporučuju.**

---

## 11. Momenty vzniku (nejlepší příběhy s oblouk problém → improvizace → nástroj)

| # | Oblouk | Datum | Klíčový prompt | Okruh |
|---|---|---|---|---|
| 1 | Nečekaně funkční SVG export → dotaz na příčinu → uložení do paměti | 07-01 10:26–10:48 | *„Díky čemu se to podařilo? Bude možnost exportu i příště?"* | U |
| 2 | Terminologický spor → glosář → kontrola staré konvence | 07-08 16:58 → 07-10 15:39 | *„Zaveď toto do @docs/onboarding/glossary.md"* | K |
| 3 | Audit 3 dokumentů → **vznik `BACKLOG.md`** → 4 dny řízené práce (O1, sekce 03, O4) | 07-08 21:03 → 07-11 | *„Jako výsledek potřebuji backlog… Preferuji seskupení do oblastí, které je logické analyzovat společně… Pokud je něco nejasné, předem se zeptej."* | M/O |
| 4 | Lokální agenti → audit vlastního nástroje → plugin → produktivní provoz | 07-04 → 07-10 21:04 | *„Chci modelem Fable 5 revidovat mé agenty tvořící Spec Factory…"* | O |
| 5 | Mezerná specifikace → 4 korekce → dotaz na poučení pro nástroj | 07-10 18:30–19:36 | *„Jakou znalost z toho můžeme pro příště vytěžit, aby SpecFactory dokázal vyřešit lépe?"* | U |
| 6 | Pravidlo n+2 zjištěné při revizi → ADR | 07-12 14:50 → 14:56 | *„To pravidlo pro string n+2 zapiš do ADR."* | M/N |
| 7 | 30 kol ladění → redukce na minimální případ → funkční algoritmus | 07-13 20:38 → 07-14 09:01 | *„Pojďme to řešit po částech… Pokud by měl dopravník jen segmenty Z1, Z2, Z3…"* | A/X |
| 8 | Verzní razítko HTML → povýšení na trvalé pravidlo | 07-14 14:30 → 14:38 | *„Ano, aktualizuj verzní razítko i příště"* | N |
| 9 | Ladění modelu bez baseline → revert → ponaučení | 07-30 09:03 → 11:57 | *„Pořád dostávám jiný výsledek… Vrať proto zpět dnešní změny."* | X |

**Doporučení pro dramaturgii:** příběh #7 jako hlavní (nejdelší oblouk, univerzálně
pochopitelný), #1 jako otvírák (nejkratší), #9 jako varovný, #3 jako most k okruhu O,
#5 jako závěr.

---

## 12. Co jsem zvážil a **nedoporučuju** brát na workshop

| Kandidát | Doklad | Proč ne |
|---|---|---|
| Git konflikty a `gdevup.bat` | 07-08 11:19, 11:24 | Firemní skripty, `[infra]`, nesouvisí s praxí zadávání |
| Analýza výkonu lokálního PC | 07-30 11:02–13:09 (~12 promptů) | Zajímavé, ale je to jiné povolání; tvar otázky pokrývá A8 |
| `/rate-limit-options`, `/usage`, `/status` | 07-03 13:17, 07-08 11:09, 3× | Provozní, bez metodické hodnoty |
| Frontend design HTML prezentace jako celek | 07-12, ~35 promptů | Jako praxe je to X3; jako výstup je to mimo rozsah analytické práce |
| „test" / „alza" / „V xccc" / `/resu` | 5 promptů | Šum |
| Konkrétní obsah PLC rozhodnutí (majáky, UDT, závory) | desítky promptů | Doména, ne metodika. Použít **jen** jako materiál k ukázkám |
| `/body-z-jednani` jako nástroj | 16× | Vlastní příkaz uživatele — `[infra]`. Ale **jeho ladění** je X4, to ano |

---

## 13. Souhrnná tabulka kandidátů

| ID | Název | Okruh | Výskyty | Přenositelnost | Předvedatelnost |
|---|---|---|---|---|---|
| K1 | Uzavřený zdroj pravdy („čerpej jen ze…") | K | 4 | přenositelná | ★★★ |
| K2 | Provenience tvrzení | K | 2 | přenositelná (princip) | ★★ |
| K3 | Journal přežije compact | K | 8 | přenositelná | ★★★ |
| K4 | `/context` před `/compact` | K | 3+8 | přenositelná | ★★★ |
| K5 | Diagnóza kompakce (hranice vs. utopený) | K/X | 16 | přenositelná | ★★ |
| K6 | Terminologie → glosář → kontrola | K | 12 | přenositelná (+1 soubor) | ★★★ |
| K7 | Adresát dokumentu jako parametr | K | 3 | přenositelná | ★★★ |
| K8 | Trvanlivost odkazů | K | 1 | přenositelná (princip) | ★ |
| K9 | Obrázek jako zdroj | K | 35 | přenositelná | ★★★ |
| M1 | „do chatu, nic neměň" ★ | M | 10 | přenositelná | ★★★ |
| M2 | Rozdělený rozsah zápisu/hlášení ★ | M | 4 | přenositelná | ★★★ |
| M3 | Schvalovací brána | M | 4 | přenositelná | ★★ |
| M4 | Číslované body ↔ dávková odpověď ★ | M | 13 | přenositelná (+1 soubor) | ★★★ |
| M5 | Revize s typem nálezu | M | 22 | přenositelná / `[infra]` subagenti | ★★ |
| M6 | Sonda před stavbou ★ | M | 1 | přenositelná | ★★★ |
| M7 | Opakovaná korekce → pravidlo | M/X/U | 3 vs. 1 | přenositelná / `[infra]` úložiště | ★★★ |
| M8 | Měřitelné omezení formátu | M | 3 | přenositelná | ★★★ |
| M9 | Formát pro navazující nástroj ★ | M | 1 | přenositelná | ★★★ |
| M10 | Zobecnění nálezu („i jinde?") ★ | M/A | 5 | přenositelná | ★★★ |
| M11 | Ověření proti druhému zdroji | M/K | 3 | přenositelná | ★★★ |
| A1 | Redukce na minimální případ ★ | A/X | 1 (oblouk 30) | přenositelná | ★★★ |
| A2 | Invariant místo symptomu ★ | A/X | 5 | přenositelná | ★★★ |
| A3 | „jak se to obvykle řeší" | A | 3 | přenositelná | ★★★ |
| A4 | Zpětné promítnutí z konverzace | A/K | 1 | přenositelná | ★★ |
| A5 | Křížová kontrola podkladů ★ | A | 6 | přenositelná | ★★★ |
| A6 | Varianty pojmenování → rozhodnutí | A | 4 | přenositelná | ★★★ |
| A7 | „Co mám nyní rozhodnout?" | A/O | 4 | přenositelná / `[infra]` registr | ★★★ |
| A8 | Cizí dotaz jako vstup k posouzení ★ | A | 5 | přenositelná | ★★★ |
| A9 | Diagram jako revidovatelný text | A/M | 8 | přenositelná | ★★★ |
| A10 | Zdroj pravdy jednou (argumentovaně) | A/M | 2 | přenositelná | ★★ |
| O1 | Runbook jako předávka | O | 2 | přenositelná (princip) / `[infra]` | ★★ |
| O2 | Jedna session = jedno téma | O | 8 | přenositelná | ★★★ |
| O3 | Model/effort per úkol + gotcha | O/N | 25 | přenositelná | ★★ |
| O4 | Druhý pár očí jiným modelem | O | 4 | přenositelná / `[infra]` agenti | ★★ |
| O5 | Migrace = zmizel starý vstup | O/N/X | 3 | přenositelná (princip) | ★★★ |
| O6 | Příběh adopce pluginu | O/N | oblouk 4 dny | přenositelná (poučení) / `[infra]` | ★★★ |
| U1 | „Díky čemu se to podařilo?" ★ | U | 1 | přenositelná | ★★★ |
| U2 | „Jakou znalost vytěžit?" ★ | U | 1 | přenositelná / `[infra]` úložiště | ★★★ |
| U3 | Ptát se na vlastní konfiguraci ★ | U/N | 1 | přenositelná | ★★★ |
| U4 | Doménové učení analytika | U | 6 | přenositelná | ★★★ |
| U5 | Forenzní analýza vlastní session | U/K/N | 3 | přenositelná | ★★★ |
| X1 | Bezcílný imperativ ★ | X/K | 11+5 | přenositelná (lekce) | ★★★ |
| X2 | Ladění screenshoty ★ | X | oblouk 30 | přenositelná (lekce) | ★★★ |
| X3 | Mikro-iterace UI | X | ~25 | přenositelná (lekce) | ★★ |
| X4 | Ladění modelu bez baseline ★ | X/N/O | ~20 | přenositelná (lekce) | ★★★ |
| X5 | Dvojité odeslání po `/model` | X/N | 24 | přenositelná (lekce) | ★★ |
| X6 | Chyba modelu vs. chybějící brána | X/N/M | 1+ | přenositelná (lekce) | ★★ |
| X7 | Diktovaný prompt s chybami | X | 3/6 | přenositelná (lekce) | ★★★ |
| X8 | „pokračuj" jako prompt | X | 9 | přenositelná (lekce) | ★★ |
| N1 | Zafixování instrukce | N | 5 | přenositelná / `[infra]` struktura | ★★★ |
| N2 | Subagent nedědí model | N | 1 | přenositelná | ★★★ |
| N3 | Režie pluginů | N | ~20 | přenositelná (očekávání) | ★★ |
| N4 | Diagnostika stroje | N | 1 | **osobní zvyk — nedoporučuju** | ★ |

**Bilance:** 53 kandidátů celkem.
**Plně přenositelných bez jakékoli infrastruktury: 41.**
**Přenositelných, ale s lehkou závislostí (jeden soubor — glosář, backlog, `CLAUDE.md`): 8**
(K6, M4, M7, A7, U2, N1, K3 částečně, O1 částečně).
**Vyžadujících postavenou infrastrukturu `[infra]`: 3** (M5 subagenti, O4 pojmenovaní agenti,
O6 plugin).
**Osobní zvyk / nedoporučuji: 1** (N4).

---

## 14. Tři nejsilnější nálezy měsíce

**1. Medián promptu 66 znaků není praxe zadávání — je to důsledek postaveného kontextu.**
Nejdelší prompt měsíce (2106 znaků, 07-09 21:54) nese 15 odpovědí a **žádnou z otázek** — ty
žijí v `BACKLOG.md`. To je celý mechanismus: dokument nese kontext, prompt nese jen rozhodnutí.
Bez toho dokumentu by tentýž prompt musel mít 8000 znaků. Kolega, který si odnese jen „piš
krátce", dostane špatný výsledek; musí si odnést „napřed postav místo, kam otázky patří".

**2. Nejúčinnější věta z celého měsíce se dá naučit za 30 sekund: „do chatu, nic neměň" — a její
sourozenec „ostatní rozdíly jen vypiš, neopravuj je".** 14 doložených výskytů (M1+M2), nulová
infrastruktura, okamžitý efekt, a zároveň to je nejlepší odpověď na strach analytika, že mu
Claude přepíše dokument. Proti tomu stojí nejčastější vada (X1): 11× odeslaný rozkaz bez cíle.
Tyto dvě položky spolu tvoří hotový úvodní blok workshopu.

**3. Dva nejdelší oblouky měsíce mají stejnou příčinu a stejný lék — a lék je analytická
disciplína, ne nástroj.** 30 promptů na algoritmus dopravníku (07-13→14) a ~20 promptů na ladění
modelu příkazu (07-30) selhaly z téhož důvodu: **chyběl testovatelný invariant a zafixovaná
základna.** Průlom v obou případech přišel od člověka, ne od nástroje —
*„Pojďme to řešit po částech… Pokud by měl dopravník jen segmenty Z1, Z2, Z3…"* (07-14 08:23)
a *„Jaký model a effort byl používaný předtím, než jsme začali provádět dnešní změny?"*
(07-30 10:49). Pro workshop to znamená, že okruh **A** (analytické postupy) je důležitější
než okruh **N** (nastavení), i když druhý vypadá atraktivněji.
