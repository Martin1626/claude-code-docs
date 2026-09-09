---

## Okruh K — Kontext a grounding

### K-01 — Dokument nese kontext, prompt nese rozhodnutí

**O čem to je.** Nejdůležitější námět celé série a jde proti intuici. Můj medián promptu
je 65 znaků, promptů nad 1000 znaků jsou 2 %. Vypadá to jako „piš krátce" — ale znamená
to, že **kontext leží v souborech, ne v promptu.**

Nejdelší prompt jednoho měsíce (2106 znaků) nese **patnáct odpovědí a ani jednu otázku.**
Otázky žijí v `BACKLOG.md`. Prompt je jen doručení rozhodnutí do rozjeté úlohy.

**Doklad:** `_raw/faze2b-prompty-alzask-07.md` (prompt z 2026-07-09 21:54) ·
`DOKLADY.md` část 1 (histogram: 47 % promptů pod 100 znaků)

**Role:** `[výklad]` + `[demo]` · **Náročnost:** střední · **Odhad:** 20 min ·
**Závislosti:** F-05 · **Priorita:** must

**Co ukážu na obrazovce:** vedle sebe ten 2106znakový prompt a `BACKLOG.md`, na který
odpovídá. Publikum vidí, že „krátký prompt" je vrchol ledovce.

**Výhrada:** funguje to jen tam, kde ten dokument někdo vede. Pro kolegu bez zavedeného
backlogu je první krok „založ si soubor", ne „piš krátce". Bez toho je rada škodlivá.

### K-02 — Bezcílný rozkaz ⚠

**O čem to je.** Nejčastější vada mého zadávání: prompt odejde jako holý rozkaz bez
uvedení, čeho se týká, a musí se poslat znovu s doplněnou cestou. Čistá režie.

**Doklad — pět doložených dvojic** (jedna z nich ve třech kolech) **a dalších pět
bezcílných rozkazů bez opravy:**

| Odeslané | O pár minut později |
|---|---|
| „V dokumentu" (07-10 07:14) | „V dokumentu @docs/analysis/Seznam_prvku…xml na listu Prvky…" (07:20) |
| „Oprav barevné signalizace podle nových změn v" (14:52) | „…v `docs/adr/hw/ADR-ASK-HW-001.md`" (14:54) |
| „Doplňuji info" (16:26) | „Doplňuji info do @docs/plc/BACKLOG.md: Reset tlačítko…" (16:28) |
| „Navrhni nejvhodnější pojmenování" (07-09 21:04) | + sloupce, list, soubor, zdroje — **tři kola** |

Bez opravy: `Proveď opravy`, `Reviduj`, `backlog aktualizuj`, `proveď revizi`, `Proveď revizi`.

**Role:** `[příběh]` + `[cvičení]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** ty dvojice vedle sebe. Pak cvičení: publikum dostane pět holých
rozkazů a doplní, co v nich chybí. Nejlevnější zlepšení v celé sérii.

**Výhrada:** draft původně tvrdil „jedenáct dvojic" — red-team ukázal, že doložených
párů je pět a zbytek jsou bezcílné rozkazy bez opravy. Obojí je vada, ale je to jiná
vada a číslo muselo být opravené.

### K-03 — Co NEčíst — a proč u každé položky

**O čem to je.** Do zadání nepatří jen „co si přečti", ale i **„co ignoruj, a proč".**
Bez toho model sáhne po souboru, který vypadá relevantně, a postaví na něm odpověď.

Klíčové je to „proč" u každé položky. Ne „neřeš baseline", ale **„rozdíl proti zmraženému
baseline NENÍ nález, je to vývoj"** — to si model nedomyslí.

**Doklad:** `_raw/faze2c-prompty-alzask-08.md` (P07) — sekce `CO NEČÍST` s důvody v obou
instancích vrstvového auditu · `_raw/faze2a-prompty-alzask-H1-06.md` (P3, P4)

**Role:** `[výklad]` + `[cvičení]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** K-01 · **Priorita:** must

**Co ukážu na obrazovce:** tentýž úkol dvakrát — bez sekce `CO NEČÍST` a s ní. Bez ní
model najde „rozpory", které jsou jen zastaralý baseline.

**Výhrada:** dá se to přehnat. Zadání, které vylučuje třicet souborů, má problém jinde.

### K-04 — Ticho je nález, ne absence nálezu

**O čem to je.** Když se ptáš, jestli tři dokumenty souhlasí, a jeden z nich o věci
**mlčí**, není to „v pořádku". Je to zjištění. Model bez explicitní instrukce mlčení
přeskočí, protože nemá co citovat — a ty se dozvíš „rozpor nenalezen".

Proto se u každé vrstvy vyžaduje **buď `soubor:řádek`, nebo doslovně „mlčí"**.

**Doklad:** `_raw/faze2c-prompty-alzask-08.md` (P15) — ta formulace je doslova v zadání
vrstvového auditu z 2026-08-14

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 10 min ·
**Závislosti:** K-03 · **Priorita:** must

**Co ukážu na obrazovce:** dva výstupy téhož auditu — bez té věty a s ní. Nálezy typu
„vrstva mlčí" jsou přesně ta místa, kde se implementace rozhodne sama za sebe.

**Výhrada:** je to zásada pro audit dokumentace, ne univerzální pravidlo.

### K-05 — Citace se ověřuje, nevěří `[příloha]`

**O čem to je.** `soubor:řádek` vypadá jako důkaz, ale je to **pozice, ne obsah.** Jak
dokument roste, řádek 412 ukazuje na něco jiného než včera — a citace vypadá pořád stejně
důvěryhodně. Odtud dvě odlišné situace: **posun** (obsah existuje, přesunul se) se opraví
mechanicky, **zmizení** (obsah tam není) je rozhodnutí pro člověka.

Kdo opraví zmizelou citaci přepsáním čísla řádku, vyrobí horší stav než zastaralý:
**tvar sedí, obsah lže.**

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (2.3) — verdikty `OK` / `POSUN` / `ZMIZELA`,
jednoznačnost kotvy 86 % → 95 % → 99 % podle šířky okna

**Role:** `[demo]` + `[infra]` · **Náročnost:** vysoká · **Odhad:** 15 min ·
**Závislosti:** K-01 · **Priorita:** should, **blok `P`** (příloha pro budovatele)

**Co ukážu na obrazovce:** přidám tři řádky nad citaci → `POSUN` a automatická oprava.
Pak citovaný text smažu → `ZMIZELA` a nástroj odmítne opravit sám.

**Výhrada:** patří do přílohy, ne do hlavního programu. Kolega bez toho nástroje si odnese
jen ostražitost vůči starým citacím — a to je málo na patnáct minut.

### K-06 — Hierarchie autority rozhoduje spor, ne datum

**O čem to je.** Když si dva dokumenty odporují, potřebuješ pravidlo, které rozhodne
**předem** — jinak rozhodne to, co model přečte první. Novější dokument nemusí vyhrát:
u mě specifikace prohrála s daty ze skutečného nasazení.

Nejhorší případ je **rozpor uvnitř téže vrstvy** — tam hierarchie nepomůže a implementátor
si vybere verzi, kterou přečte první.

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (2.6b/h) — sedm vrstev autority, doložený
případ, kdy novější specifikace prohrála

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** should

**Co ukážu na obrazovce:** tabulku vrstev a jeden reálný spor s verdiktem. Pak otázku
publiku: který z vašich dokumentů je nejvyšší autorita? (většinou to nikdo neví)

**Výhrada:** hierarchii musí někdo napsat a je to doménová práce.

### K-07 — Čtvrtina mého `CLAUDE.md`, kterou nikdo nikdy nespustil ⚑

**O čem to je.** `CLAUDE.md` je taky dokumentace — a stárne jako každá jiná. Rozdíl je
v tom, že **tuhle dokumentaci model bere jako platnou** a **platíš ji každý tah.**

**Čtyři exponáty z jednoho souboru:**

| Exponát | Doklad |
|---|---|
| Sekce „Projektový asistent" — 3 031 znaků, 12,7 % souboru, ~1000 tokenů každý tah | **za 2 678 promptů nespuštěna ani jednou** (`/learn`, `/lookup`, `/overview`, `/glossary` = 0×) |
| Popsaný formát souborů, který se už nepoužívá | soubor je na disku v jiném formátu, než `CLAUDE.md` tvrdí |
| Lokální nástroj, nahrazený pluginem | `CLAUDE.md` ho pořád popisuje jako aktuální |
| Vrstva „cross-project shared" pravidel | **ten adresář na disku vůbec není** (viz X-04 v `VYRAZENO.md`) |

**Role:** `[příběh]` + `[demo]` · **Náročnost:** nízká · **Odhad:** 15 min ·
**Závislosti:** — · **Priorita:** must ⚑

**Co ukážu na obrazovce:** otevřu vlastní `CLAUDE.md`, označím tu čtvrtinu a řeknu, kolik
mě stála. Pak `grep` na příkazy, které v ní jsou popsané — nula výskytů v celé historii.
A `ls` na adresář, který v ní je uvedený a neexistuje.

**Výhrada:** je to nepříjemné přiznání, ne technika. A právě proto to funguje — publikum
má to samé a nevědí o tom. Zásada, kterou si odnesou: **co je v `CLAUDE.md`, platíš
každý tah, tak to jednou za čtvrt roku projdi.**

---

## Okruh R — Rozšíření

### R-01 — Zadání do souboru, session ho jen provede

**O čem to je.** Nejsilnější přenositelná praxe z celé inventury a stojí to jeden soubor.
Dlouhé zadání se napíše jako verzovaný Markdown **mimo chat** a prompt je jen ukazatel:
„Přečti X a proveď ho celý." Vypadá to jako prompt o 52 znacích — a je za ním 12,8 kB
zadání.

Řeší to tři věci naráz: zadání se dá **revidovat před spuštěním**, dá se **spustit znovu**
v jiné session, a je **v Gitu**, takže se z něj stane dokumentace postupu.

**Ověřená anatomie** (z obou reálných souborů, ne domněnka):

```
Proč (podklad — neměň závěry, můžeš je doplnit)
Dekompozice na části (Část A1 / A2 / B), každá:
    Problém / Vstup / Návrhové rozhodnutí, které dodrž / Fáze
Mantinely (platí pro celý úkol)
Definition of done
```

Druhý soubor navíc: `Krok 0 — ověření předpokladů (brána běhu, bez ní nepokračuj)`,
`Antipatterny`, `Historie revizí`.

**Doklad:** 2026-08-19 21:39 — 52 znaků → 12,8 kB · 2026-08-24 11:32 — 88 znaků → 7,3 kB.
Zdroj: `_raw/faze2e-prompty-shared.md` (P10). Vzor **v čase silní** — oba nejčistší
výskyty jsou nejnovější.

**Role:** `[demo]` + `[cvičení]` · **Náročnost:** nízká · **Odhad:** 15 min ·
**Závislosti:** K-01 · **Priorita:** must

**Co ukážu na obrazovce:** vedle sebe jednořádkový prompt a 12,8 kB soubor za ním.
**A pak meta-ukázka: tenhle katalog vznikl přesně tak** — zadání mělo 12 kB v souboru
a prompt zněl „Přečti si celý a proveď".

**Výhrada:** žádná. Nepotřebuje plugin ani nástroj, jen soubor.

### R-02 — Metodika bez spouštěče je jen text ⚑

**O čem to je.** Napsat postup do `README.md` nestačí — nikdo ho nespustí, protože
v README není „jak na to", ale „co platí". Postup potřebuje **spouštěč**: skill, který
se sám najde podle popisu, nebo slash command jako tenkou obálku nad ním.

Poznávací znamení, že ti spouštěč chybí: v návodu píšeš odstavec **„co řekneš Claude
Code"**. Tím jsi právě přiznal, že tam patří příkaz.

**Doklad:** vlastní zkušenost z 2026-08-25 — postavil jsem evidenci se třemi vrstvami
dokumentace a dostal otázku „Proč jsi na to nevytvořil skills? Rád bych to používal
opakovaně jednoduchým způsobem." Za tři hodiny z toho byly tři slash commandy.

**A tady je to sebe-ilustrující:** tenhle poznatek jsem si tehdy zapsal jako kandidáta
na pravidlo — a **do pravidla se nikdy nepovýšil.** Sám o něm mluvím na workshopu a sám
jsem ho nedotáhl. To je přesně ta propast mezi „vím to" a „mám to zařízené".

**Role:** `[příběh]` + `[demo]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** R-01 · **Priorita:** must ⚑

**Co ukážu na obrazovce:** návod s odstavcem „co řekneš Claude Code" a vedle toho command,
který ten odstavec nahradil. Pak ho spustím. A nakonec ten záznam v inboxu, který nikdy
nedošel do pravidel.

**Výhrada:** commandů má být tři až čtyři. Víc znamená, že si člověk nevybere.

### R-03 — Uložený postup místo opakovaného promptu

**O čem to je.** Když tentýž prompt píšeš třikrát, patří do souboru s příkazem. Zvlášť
u kroků, které se **snadno opomenou** — u nich rada v návodu nestačí, musí být součástí
postupu.

Reálný případ: „vždycky otevři přílohy" bylo devět dní radou. Pak se ukázalo, že
v přiloženém obrázku byly konkrétní hodnoty, které se devět dní vedly jako „chybí".
Dnes je čtení příloh **součást příkazu**.

**Doklad:** `docs/suppliers/POSTUP-pro-analytiky.md` — tři příkazy na osm situací ·
`_raw/faze3a-alzask-metodiky.md` (8, 9)

**Role:** `[demo]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** R-02 · **Priorita:** should

**Co ukážu na obrazovce:** spustím příkaz **nad anonymizovanou kopií dvou záznamů
v cvičném repozitáři** — ne nad produkční evidencí. Pak otevřu ten command a ukážu,
že je to obyčejný Markdown soubor.

**Výhrada:** původní plán byl pustit to nad skutečnou evidencí. To nejde — promítlo by to
jména zákazníka i dodavatelů a otevřené závazky na projektor. Anonymizovaná kopie je
podmínka, ne detail.

### R-04 — Dvě vrstvy se rozjedou, když jednu z nich nikdo nečte ⚑

**O čem to je.** Doporučení zní: dlouhá metodika pro člověka na vyžádání a krátký checklist
v automaticky načítaném kontextu; z krátkého ukazuj na dlouhé, neduplikuj.

**A teď co se stane, když se to nedodrží.** Mám 1201řádkovou metodiku a 69řádkový
quick-reference. Ale ten dlouhý dokument nikdo nečte, protože se načítá jen na vyžádání —
takže se rozešel se skutečností a nikdo si toho nevšiml. Rozdíl adresátů (`README` pro
člověka · `CLAUDE.md` pravidla · **skill = postup k provedení**) je správný princip,
ale **bez čtenáře je i dobrá struktura jen archiv.**

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (1.1) — poměr 1201 : 69 řádků ·
a doložené nesoulady v tom dlouhém dokumentu (K-07)

**Role:** `[výklad]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** should ⚑

**Co ukážu na obrazovce:** oba soubory vedle sebe, počet řádků, a pak jedno místo,
kde se ten dlouhý rozešel se skutečností.

**Výhrada:** `CLAUDE.md` v podadresáři se spolehlivě uplatní jen při práci v tom adresáři.
Na to se dá naletět — a já jsem naletěl.

### R-05 — Dva hooky, které mi běží, a šest, které neznám

**O čem to je.** Hook je příkaz, který harness spustí sám v určitém okamžiku. Rozdíl proti
validátoru: **nemusíš si na něj vzpomenout.**

**Doklad:** mám **čtyři aktivní hooky, ale jen dva různé eventy** z asi osmi.
Nejnápadnější mezera: při 51 kompaktacích nemám na kompaktaci pověšenou žádnou automatiku,
i když dokumentovaný vzor existuje. Zdroj: `_raw/faze1-korekce-hooky.md`.

**Role:** `[demo]` · **Náročnost:** vysoká · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** could

**Co ukážu na obrazovce:** **jen ty dva, které mi skutečně běží.** `/clear` a hned potom
hláška, kterou vypsal startovací hook — publikum vidí, že to nikdo nespustil ručně.
Pak `hooks.json`, aby bylo vidět, že je to pár řádků.

**Výhrada:** o hookech, které nepoužívám, mluvit jen jako o možnosti — **ne je předvádět.**
Draft původně chtěl doporučit hook na kompaktaci; ten sice existuje, ale nikdy jsem ho
nespustil, takže to nesmím podávat jako vyzkoušené.

---

## Okruh M — Mechanika kvality

### M-01 — Brána, kterou nikdo nespouští, je taky jen prompt ⚑

**O čem to je.** Zásada „kontrolu, kterou umí skript, nepiš jako věty do promptu" je
nejsilnější konvergence celé inventury — našlo ji pět nezávislých analýz. Důvod: věta
v promptu je **prosba** (model ji splní většinou), skript je **fakt** (vrátí chybu vždy,
i za půl roku, i po kompaktaci).

**A teď druhá polovina, kterou by draft zamlčel.** V tom samém projektu, který má na tuhle
zásadu vlastní pravidlo, **žádná brána neběží automaticky:**

- `core.hooksPath` míří do `.git/hooks`, kde není **jediný aktivní hook**
- `.githooks/` je v repozitáři nedotčené **7,2 měsíce** a i tak by kontrolovalo jen
  typy souborů, které tam nejsou
- CI spouští jen jednu denní úlohu, která kontroluje changelog

Takže validátory existují, jsou dobré, a **spouští je jedině člověk, když si vzpomene.**
To je přesně to, co ta zásada zakazuje.

**Doklad:** `_raw/faze5-redteam.md` (RT-35) — ověřeno na konfiguraci repozitáře ·
a protipól: pravidlo o pořadí záznamů v changelogu existuje 2,5 měsíce a **dodnes se
mechanicky porušuje**, protože ho nic nevynucuje

**Role:** `[výklad]` + `[demo]` · **Náročnost:** střední · **Odhad:** 18 min ·
**Závislosti:** — · **Priorita:** must ⚑

**Co ukážu na obrazovce:** dvě věci vedle sebe. Nejdřív **validátor naživo** — udělám
v souboru chybu, spustím, vrátí nenulový kód s pojmenovaným polem za necelou sekundu.
Nejrychlejší demo v katalogu. A hned potom `git config core.hooksPath` a `ls` na ten
adresář — je prázdný. Publikum vidí obojí: **že to funguje, a že to nikdo nespouští.**

**Výhrada a poučení, které si publikum odnese:** brána má tři části a lidé postaví jen
první. Kontrola (skript) · **spouštěč** (hook nebo CI) · a **reakce na výsledek**. Bez
druhé části je to nástroj, na který si musíš vzpomenout — tedy zase jen prosba, akorát
v jiném souboru.

### M-02 — „Napiš to do chatu, nic neměň"

**O čem to je.** Nejlepší poměr hodnoty a nákladu z celé inventury. Jedna věta, nulová
infrastruktura, funguje první den. Před zápisem do souborů si vyžádáš návrh **do chatu**
a zakážeš úpravu.

Je to zároveň nejlepší odpověď na strach z autonomie: nemusíš zakazovat práci se soubory
natrvalo, jen si oddělíš **návrh** od **provedení**.

**Doklad:** *„Navrhni ještě vhodnější pojmenování akce než je assignContainer. Napiš
varianty zde do chatu, nic neměň."* (2026-07-09 08:44) → o 25 minut později *„OK, rozhodl
jsem se pro containerPlaced. Oprav všude."* (09:09). Celkem **14 výskytů**, z toho 5×
s explicitním zákazem zápisu.

**Role:** `[demo]` + `[cvičení]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** tentýž úkol dvakrát. Bez té věty model začne editovat soubory.
S ní vypíše varianty s odůvodněním a čeká.

**Výhrada:** žádná — ale stojí za to zmínit, že vestavěný **režim plánování** (N-03) dělá
totéž systémověji. Tahle věta je to, co člověk použije, když si na režim nevzpomene.

### M-03 — Triáž dělá člověk. Dva ze tří nálezů jsou falešné.

**O čem to je.** Když necháš model najít chyby a hned je opravit, dostaneš dvě věci
zároveň: opravené skutečné chyby a **zanesené nové**, protože část nálezů byla falešná.
Triáž — rozhodnutí, který nález je skutečný — **nesmí být delegovaná.**

Číslo, které to dělá konkrétní: **počítej, že dva ze tří nálezů jsou falešné.**
Nezávislé měření precision revizorů dává 21–31 %.

**Doklad:** vlastní diagnóza z 2026-08-19 16:20: *„při opravách často dochází k zanášení
nových chyb a zároveň spotřebovává mnoho tokenů"* → o tři hodiny později náhrada:
linter bez modelu → **slepí** recenzenti, každý s jednou optikou → **triáž člověkem** →
opravy po jedné větě, ne přepisem sekce.

**A ještě jeden doklad z této práce:** red-team proti tomuto katalogu vznesl 42 nálezů.
Zapracoval jsem je **selektivně** — část jako opravu, část jako přeformulování, část
jako odmítnutí. Kdybych je nechal zapracovat automaticky, katalog by se scvrkl na tři díly
a přišel bych o zásobu, která byla cílem.

**Role:** `[výklad]` + `[příběh]` · **Náročnost:** střední · **Odhad:** 15 min ·
**Závislosti:** M-02 · **Priorita:** must

**Co ukážu na obrazovce:** report z revize a projdu s publikem tři nálezy — u jednoho
se ukáže, že je falešný. Pak ten protokol: co dělá stroj, co člověk.

**Výhrada:** vyžaduje to disciplínu, ne nástroj. A je to nepohodlné, protože „nechat to
opravit samo" je pohodlnější.

### M-04 — Slepý recenzent ⚠

**O čem to je.** Recenzentovi **neříkej, co a proč jsi změnil.** Když to ví, hledá
potvrzení tvého záměru. Když to neví, čte artefakt jako cizí text.

Praktická formulace: *„artefakt jako cizí text, bez věty, co a proč jsme měnili"*.
A u verifikace opravy: *„ANI SLOVO o tom, že jde o opravenou verzi"*.

**Doklad:** `_raw/faze3b-pluginy.md` (2) — v definici revizního agenta je klauzule
o slepotě napsaná explicitně · `_raw/faze2c-prompty-alzask-08.md` (P18)

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 10 min ·
**Závislosti:** M-03 · **Priorita:** should

**Co ukážu na obrazovce:** **statický exponát** — tu klauzuli v definici agenta,
a vedle ní zadání, které slepotu ruší.

**Výhrada:** draft to chtěl jako demo („spustím dva recenzenty a uvidíte rozdíl").
To nejde: model není deterministický, takže demo je **tvrzení o tom, jak se model
zachová** — a když se zachová jinak, tvrzení se před publikem samo vyvrátí.
Statický exponát tuhle slabinu nemá.

### M-05 — Vykazuj, kolik jsi toho NEzkontroloval

**O čem to je.** „Nic jsem nenašel" a „nic jsem neměřil" vypadají v reportu stejně.
Rozdíl udělá **součtová pojistka**: kontrola vykáže nejen nálezy, ale i kolik položek
vůbec nekontrolovala a proč.

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (2.3) — brána vykazuje součet
`2558 = 1278 kontrolováno + 0 bez kotvy + 661 mimo kontrolu + 619 opakovaných`.
Bez toho čísla by „1278 zkontrolováno" znělo jako úplnost.

**A meta-doklad:** tenhle katalog má tu pojistku taky — `VYRAZENO.md` sekce C přiznává,
co v datech není. **Report bez sekce „co chybí" je nedokončený report.**

**Role:** `[demo]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** M-01 · **Priorita:** must

**Co ukážu na obrazovce:** ten součet naživo. A pak stejnou úlohu bez pojistky — report
řekne „vše v pořádku", i když se polovina položek nekontrolovala.

**Výhrada:** je to nepohodlné. Pojistka vždycky ukáže, že jsi zkontroloval méně,
než sis myslel.

### M-06 — Deterministická kontrola vs. sémantická

**O čem to je.** Rozděl kontroly na **ověřitelné bez porozumění** (čísla, odkazy, formát,
součty → skript) a **vyžadující porozumění** (souhlasí popis s diagramem? → model nebo
člověk). A pak to hlavní: **nikdy nenech druhou hromádku předstírat, že dělá práci první.**

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (4.2) — linter má pravidla deterministicky,
sémantickou konzistenci **explicitně nechává** na kontrole modelem, a je to napsané
v jeho dokumentaci jako známé omezení

**A doklad, proč to platí:** tučně značená tabulka místo nadpisu tiše vypnula celou třídu
kontrol — a přesně tak unikla chyba ve velikosti datového pole. Nástroj kontroluje jen to,
co pozná.

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** M-01 · **Priorita:** must

**Co ukážu na obrazovce:** změním hodnotu tak, aby porušila pravidlo → linter to chytí
okamžitě s kódem chyby. Pak změním **význam** popisu, aby nesouhlasil s diagramem →
linter mlčí. To je ta hranice.

**Výhrada:** hranice není vždy ostrá. Ale mít ji napsanou je lepší než ji nemít.

### M-07 — Práh, který realita překračuje — a prázdné pole, ze kterého se počítá ⚑

**O čem to je.** Brána, která hlásí 56 varování, přestala být bránou — mezi nimi se ztratí
dvě skutečné chyby a lidé si zvyknou přehlížet i je.

**A druhá vrstva téhož problému:** ten práh se počítá z pole, které **32 z 35 dokumentů
vůbec nemá vyplněné.** Takže brána měří stárnutí na datech, která z většiny neexistují.
A devět nejstarších architektonických rozhodnutí je pořád ve stavu „draft".

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (1.3) — práh 30 dní, 23 dokumentů v draftu
55–201 dní, výsledek 56 varování a 2 skutečné chyby · `_raw/faze5-redteam.md` (RT-40) —
prázdné pole u 32 z 35, devět rozhodnutí ve stavu draft

**Role:** `[příběh]` + `[demo]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** M-01 · **Priorita:** should ⚑

**Co ukážu na obrazovce:** spustím validátor a nechám publikum **najít ty dvě chyby
v 56 varováních.** Nikdo je nenajde. Pak ukážu, že pole, ze kterého se práh počítá,
je většinou prázdné.

**Výhrada:** žádná — je to obecná vlastnost varovných systémů. Tři možnosti, co s tím:
zvednout práh, snížit závažnost, nebo ho zrušit. Nechat ho křičet do prázdna je nejhorší.

### M-08 — Dva exit kódy = dva různé signály `[příloha]`

**O čem to je.** Brána musí rozlišit „evidence je poškozená" (blokuj) od „je tu otevřená
práce" (jen upozorni). Bez toho buď zablokuješ proces kvůli běžnému čekání, nebo si zvykneš
ignorovat i skutečné chyby. Zvláštní případ: **„čekáme na externí vstup" není chyba,
je to stav.**

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (3.5, 4.4b)

**Role:** `[demo]` + `[infra]` · **Náročnost:** střední · **Odhad:** 10 min ·
**Závislosti:** M-01 · **Priorita:** could, **blok `P`**

**Co ukážu na obrazovce:** dvě různé chyby, dvě různé návratové hodnoty, dvě různé reakce.

**Výhrada:** patří do přílohy pro budovatele. Zásada je přenositelná, kódy jsou moje.
