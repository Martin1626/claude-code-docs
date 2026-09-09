---

## Okruh K — Kontext a grounding

### K-01 — Dokument nese kontext, prompt nese rozhodnutí

**O čem to je.** Tohle je nejdůležitější námět celé série a jde proti intuici.
Můj medián promptu je 65 znaků, promptů nad 1000 znaků jsou 2 %. Vypadá to jako „piš
krátce" — ale ono to znamená, že **kontext leží v souborech, ne v promptu.**

Nejdelší prompt jednoho měsíce (2106 znaků) nese **patnáct odpovědí a ani jednu otázku.**
Otázky žijí v `BACKLOG.md`. Prompt je tedy jen doručení rozhodnutí do rozjeté úlohy.

Kdo si odnese jen půlku („piš krátké prompty"), dostane špatný výsledek. Musí si odnést
**„nejdřív postav místo, kam otázky patří."**

**Doklad:** `_raw/faze2b-prompty-alzask-07.md` (prompt z 2026-07-09 21:54, 2106 znaků,
15 odpovědí bez otázek) · `DOKLADY.md` část 1 (histogram délek: 47 % promptů pod 100 znaků)

**Role:** `[výklad]` + `[demo]` · **Náročnost:** střední · **Odhad:** 20 min ·
**Závislosti:** F-05 · **Priorita:** must

**Co ukážu na obrazovce:** vedle sebe ten 2106znakový prompt a `BACKLOG.md`, na který
odpovídá. Publikum vidí, že „krátký prompt" je vrchol ledovce. Pak histogram délek promptů
z `DOKLADY.md` — a otázku: proč je těch krátkých tolik?

**Výhrada:** funguje to jen tam, kde ten dokument někdo vede. Pro kolegu bez zavedeného
backlogu je první krok „založ si soubor", ne „piš krátce". Bez toho je rada škodlivá.

### K-02 — Bezcílný rozkaz: jedenáctkrát tentýž prompt

**O čem to je.** Nejčastější vada mého zadávání za sedm měsíců: prompt odejde jako holý
rozkaz bez uvedení, čeho se týká, a musí se poslat znovu s doplněnou cestou. Čistá režie,
nula výsledku.

**Doklad — jedenáct doložených dvojic**, například:

| Odeslané | O pár minut později |
|---|---|
| „V dokumentu" (07-10 07:14) | „V dokumentu @docs/analysis/Seznam_prvku…xml na listu Prvky je seznam HW zařízení…" (07:20) |
| „Oprav barevné signalizace podle nových změn v" (14:52) | „…v `docs/adr/hw/ADR-ASK-HW-001.md`" (14:54) |
| „Doplňuji info" (16:26) | „Doplňuji info do @docs/plc/BACKLOG.md: Reset tlačítko…" (16:28) |
| „Navrhni nejvhodnější pojmenování" (07-09 21:04) | + sloupce, list, soubor, zdroje — **tři kola** (21:06, 21:08) |

A varianty bez opravy, které prostě dopadly špatně: `Proveď opravy`, `Reviduj`,
`backlog aktualizuj`, `proveď revizi`.

**Role:** `[příběh]` + `[cvičení]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** ty dvojice vedle sebe. Pak cvičení: dám publiku pět holých
rozkazů a nechám je doplnit, co v nich chybí. Je to nejlevnější zlepšení v celé sérii —
naučí se to za pět minut.

**Výhrada:** žádná. Tohle je čistý zisk pro každého bez ohledu na infrastrukturu.

### K-03 — Co NEčíst — a proč u každé položky

**O čem to je.** Do zadání nepatří jen „co si přečti", ale i **„co ignoruj, a proč".**
Bez toho model sáhne po souboru, který vypadá relevantně, a postaví na něm celou odpověď.

Klíčové je to „proč" u každé položky. Ne „neřeš baseline", ale **„rozdíl proti zmraženému
baseline NENÍ nález, je to vývoj"** — to je informace, kterou si model nedomyslí.

**Doklad:** `_raw/faze2c-prompty-alzask-08.md` (P07) — sekce `CO NEČÍST` s důvody
v obou instancích vrstvového auditu (2026-08-14) · `_raw/faze2a-prompty-alzask-H1-06.md`
(P3, P4) — explicitní výčet toho, co se nemá řešit, a vyloučení konkrétního souboru

**Role:** `[výklad]` + `[cvičení]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** K-01 · **Priorita:** must

**Co ukážu na obrazovce:** tentýž úkol dvakrát — bez sekce `CO NEČÍST` a s ní. Bez ní
model najde „rozpory", které jsou jen zastaralý baseline. Vidět v jednom kole.

**Výhrada:** dá se to přehnat. Zadání, které vylučuje třicet souborů, je špatně strukturované
zadání — problém je jinde.

### K-04 — Ticho je nález, ne absence nálezu

**O čem to je.** Když se ptáš, jestli tři dokumenty souhlasí, a jeden z nich o věci
**mlčí**, není to „v pořádku". Je to zjištění. Model bez explicitní instrukce mlčení
přeskočí, protože nemá co citovat — a ty se dozvíš „rozpor nenalezen".

Proto se ve výstupu vyžaduje u každé vrstvy **buď `soubor:řádek`, nebo doslovně „mlčí"**.

**Doklad:** `_raw/faze2c-prompty-alzask-08.md` (P15) — formulace „ticho jedné vrstvy je
nález, ne absence nálezu" ve zadání vrstvového auditu 2026-08-14

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 10 min ·
**Závislosti:** K-03 · **Priorita:** must

**Co ukážu na obrazovce:** dva výstupy téhož auditu — jeden bez té věty, druhý s ní.
Nálezy typu „vrstva mlčí" jsou přesně ta místa, kde se implementace rozhodne sama za sebe.

**Výhrada:** je to zásada pro audit dokumentace, ne univerzální pravidlo. U běžného dotazu
by vyžadování „mlčí" jen nafouklo odpověď.

### K-05 — Citace se ověřuje, nevěří

**O čem to je.** `soubor:řádek` vypadá jako důkaz, ale je to **pozice, ne obsah.** Jak
dokument roste, řádek 412 ukazuje na něco jiného než včera — a citace přitom vypadá pořád
stejně důvěryhodně. Odtud dvě odlišné situace: **posun** (obsah existuje, jen se přesunul)
se dá opravit mechanicky, **zmizení** (obsah tam není) je rozhodnutí pro člověka.

Kdo opraví zmizelou citaci přepsáním čísla řádku, vyrobí horší stav než zastaralý:
**tvar sedí, obsah lže.**

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (2.3) — nástroj vrací `OK` / `POSUN` /
`ZMIZELA`, jednoznačnost kotvy 86 % → 95 % → 99 % podle šířky okna

**Role:** `[demo]` · **Náročnost:** vysoká · **Odhad:** 15 min ·
**Závislosti:** K-01 · **Priorita:** should

**Co ukážu na obrazovce:** vezmu citaci, do souboru nad ní přidám tři řádky, spustím
kontrolu → `POSUN` a automatická oprava. Pak citovaný text smažu → `ZMIZELA` a nástroj
odmítne opravit sám.

**Výhrada:** `[infra]` — ten nástroj je součást mého registru. Přenositelná je **zásada**
(cituj obsah, ne pozici; rozliš posun od zmizení), ne implementace. Kolega bez nástroje
si odnese jen ostražitost vůči starým citacím, a to je málo. Zvážit, jestli to nepatří
do dílu pro budovatele nástrojů.

### K-06 — Hierarchie autority rozhoduje spor, ne datum

**O čem to je.** Když si dva dokumenty odporují, potřebuješ pravidlo, které rozhodne
**předem** — jinak rozhodne to, co model přečte první, nebo co je napsané přesvědčivěji.
Novější dokument nemusí vyhrát: specifikace prohrála s daty ze skutečného nasazení.

A nejhorší případ je **rozpor uvnitř téže vrstvy autority** — tam hierarchie nepomůže
a implementátor si vybere tu verzi, kterou přečte první.

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (2.6b/h) — sedm vrstev autority zdrojů,
doložený případ, kdy novější PLC specifikace prohrála s daty nasazení

**Role:** `[výklad]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** should

**Co ukážu na obrazovce:** tabulku vrstev a jeden reálný spor s verdiktem. Pak otázku
publiku: který z vašich dokumentů je nejvyšší autorita? (většinou to nikdo neví)

**Výhrada:** hierarchii musí někdo napsat a ta práce je doménová. Bez ní je to jen
myšlenkový rámec.

### K-07 — `CLAUDE.md` driftuje od skutečnosti

**O čem to je.** Soubor s instrukcemi pro Claude je taky dokumentace — a stárne jako každá
jiná. Rozdíl je v tom, že **tuhle dokumentaci Claude bere jako platnou.** Když v ní stojí
postup, který už neplatí, model ho poslušně provede.

**Doklad:** tři doložené nesoulady v `fhb/CLAUDE.md` — popsaný formát souborů, který se
už nepoužívá; lokální nástroj nahrazený pluginem; a **vrstva pravidel, která vůbec
neexistuje** (viz X-08). Zdroj: `_raw/faze2d-prompty-fhb-myfaber.md`.

**Role:** `[příběh]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** must

**Co ukážu na obrazovce:** otevřu `CLAUDE.md` a vedle toho skutečnost. Pak `grep` na
adresář, který `CLAUDE.md` uvádí a který na disku není.

**Výhrada:** je to nepříjemné přiznání, ne technika. Ale právě proto to funguje —
publikum má to samé a nevědí o tom.

---

## Okruh R — Rozšíření

### R-01 — Zadání do souboru, session ho jen provede

**O čem to je.** Nejsilnější přenositelná praxe z celé inventury a stojí to jeden soubor.
Dlouhé zadání se napíše jako verzovaný Markdown **mimo chat** a prompt je jen ukazatel:
„Přečti X a proveď ho celý." Vypadá to jako lakonický prompt o 52 znacích — a je za ním
12,8 kB zadání.

Řeší to tři věci naráz: zadání se dá **revidovat před spuštěním**, dá se **spustit znovu**
v jiné session nebo jiném repozitáři, a je **v Gitu**, takže se z něj postupně stane
dokumentace postupu.

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

**Doklad:** 2026-08-19 21:39 — „Přečti `…\review-spec-zadani.md` a proveď ho celý"
(52 znaků → 12,8 kB) · 2026-08-24 11:32 — 88 znaků → 7,3 kB. Zdroj:
`_raw/faze2e-prompty-shared.md` (P10). Vzor navíc **v čase silní** — oba nejčistší
výskyty jsou nejnovější.

**Role:** `[demo]` + `[cvičení]` · **Náročnost:** nízká · **Odhad:** 15 min ·
**Závislosti:** K-01 · **Priorita:** must

**Co ukážu na obrazovce:** vedle sebe jednořádkový prompt a 12,8 kB soubor za ním.
Nejnázornější slide celé série. **A pak meta-ukázka: tenhle katalog vznikl přesně tak** —
zadání mělo 12 kB v souboru a prompt zněl „Přečti si celý a proveď".

**Výhrada:** žádná. Nepotřebuje plugin ani nástroj, jen soubor.

### R-02 — Metodika bez spouštěče je jen text

**O čem to je.** Napsat postup do `README.md` nestačí — nikdo ho nespustí, protože
v README není „jak na to", ale „co platí". Postup potřebuje **spouštěč**: skill, který
se sám najde podle popisu, nebo slash command jako tenkou obálku nad ním.

Poznávací znamení, že ti spouštěč chybí: v návodu píšeš odstavec **„co řekneš Claude Code"**.
Tím jsi právě přiznal, že tam patří příkaz. Věta k opsání je command bez implementace.

**Doklad:** vlastní zkušenost z 2026-08-25 — postavil jsem evidenci se třemi vrstvami
dokumentace a dostal otázku „Proč jsi na to nevytvořil skills? Rád bych to používal
opakovaně jednoduchým způsobem." Za tři hodiny z toho byly tři slash commandy.
Zdroj: `_raw/faze2c-prompty-alzask-08.md` (V01).

**Role:** `[příběh]` + `[demo]` · **Náročnost:** střední · **Odhad:** 12 min ·
**Závislosti:** R-01 · **Priorita:** should

**Co ukážu na obrazovce:** `POSTUP-pro-analytiky.md` s odstavcem „co řekneš Claude Code"
a vedle toho command, který ten odstavec nahradil. Pak ho spustím.

**Výhrada:** commandů má být tři až čtyři. Víc znamená, že si člověk nevybere. Vodítko:
kolik akcí opakuje **týdně**.

### R-03 — Uložený postup místo opakovaného promptu

**O čem to je.** Když tentýž prompt píšeš třikrát, patří do souboru s příkazem. Zvlášť
u kroků, které se **snadno opomenou** — u nich není „rada v návodu" dost, musí být
součástí postupu.

Reálný případ: „vždycky otevři přílohy" bylo devět dní radou. Pak se ukázalo, že dodavatel
napsal „parametry máme v nastavení" a v přiloženém screenshotu byly konkrétní hodnoty.
Devět dní se to vedlo jako „chybí hodnoty". Dnes je čtení příloh **součást příkazu**.

**Doklad:** `docs/suppliers/POSTUP-pro-analytiky.md` — tři příkazy pokrývající osm situací ·
`_raw/faze3a-alzask-metodiky.md` (sekce 8, 9) — 8 commandů, 2 skilly

**Role:** `[demo]` · **Náročnost:** nízká · **Odhad:** 12 min ·
**Závislosti:** R-02 · **Priorita:** should

**Co ukážu na obrazovce:** `/dodavatele:stav` bez argumentu — vypíše, na co se čeká.
Pak otevřu ten command a ukážu, že je to obyčejný Markdown soubor. Publikum uvidí,
že si to postaví taky.

**Výhrada:** argument má být nepovinný. `/dodavatele:mail` bez cesty najde nezpracované
sám — člověk nemusí vědět, kde soubory leží.

### R-04 — Dvě vrstvy dokumentace podle čtenáře

**O čem to je.** Jedna metodika pro člověka na vyžádání (dlouhá, vysvětlující) a jeden
krátký checklist toho, co se nesmí zvorat, ve vždy načteném kontextu. **Z krátkého ukazuj
na dlouhé, neduplikuj** — dvě kopie téhož se rozejdou.

Rozdíl adresátů: `README.md` je metodika pro člověka · `CLAUDE.md` jsou pravidla, která
model nesmí zvorat · **skill je postup, který se má provést.** Postup napsaný do README
nikdo nespustí.

**Doklad:** `_raw/faze3a-alzask-metodiky.md` (1.1) — 1201řádková metodika + 69řádkový
quick-reference v automaticky načítaném kontextu

**Role:** `[výklad]` · **Náročnost:** nízká · **Odhad:** 10 min ·
**Závislosti:** — · **Priorita:** should

**Co ukážu na obrazovce:** oba soubory vedle sebe a v krátkém ukážu odkaz do dlouhého.
Pak počet řádků obou — 69 proti 1201.

**Výhrada:** platí, jen když se ten krátký skutečně načítá automaticky. `CLAUDE.md`
v podadresáři se spolehlivě uplatní jen při práci v tom adresáři — na to se dá naletět.

### R-05 — Hook: kontrola, kterou nemusíš spouštět

**O čem to je.** Hook je příkaz, který harness spustí sám v určitém okamžiku — na začátku
session, před zápisem do souboru, před kompaktací. Rozdíl proti validátoru: **nemusíš si
na něj vzpomenout.**

Používám dva eventy z asi osmi (`SessionStart`, `PreToolUse`). Nejnápadnější mezera:
při 51 kompaktacích nemám na kompaktaci pověšenou žádnou automatiku, i když dokumentovaný
vzor existuje (`SessionStart` s `matcher: "compact"`).

**Doklad:** `_raw/faze1-korekce-hooky.md` — čtyři aktivní hooky, dva eventy z osmi ·
`_raw/faze4b-verifikace-a-mezery.md` sekce B — přehled nepoužitých eventů

**Role:** `[demo]` · **Náročnost:** vysoká · **Odhad:** 12 min ·
**Závislosti:** — · **Priorita:** could

**Co ukážu na obrazovce:** `/clear` a hned potom hlášku, kterou vypsal `SessionStart`
hook — publikum vidí, že to nikdo nespustil ručně. Pak obsah `hooks.json`, aby bylo vidět,
že je to pár řádků.

**Výhrada:** `[infra]` a **netestováno** u toho, co nepoužívám. `PreCompact` existuje,
ale dokumentace k němu nemá propracovaný příklad — nesmím to publiku doporučit jako
vyzkoušené.
