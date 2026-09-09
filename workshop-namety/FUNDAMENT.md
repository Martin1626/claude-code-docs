> **Součást katalogu námětů na workshop.**
> Hlavní katalog: [NAMETY.md](NAMETY.md) · doklady a statistiky: [DOKLADY.md](DOKLADY.md) ·
> vyřazené náměty: [VYRAZENO.md](VYRAZENO.md).
> Pracovní podklady dvanácti agentů zůstaly v `_raw/`.

> **Jak tento dokument vznikl.** Výklad tří mechanik (bezstavovost, tokenizace, kontextové
> okno) napsal agent na modelu opus, který u každého tvrzení musel označit, jestli je
> ověřené, odhadnuté, nebo nevěděl. Bodů „nevím a nehádám" bylo v první verzi **jedenáct**.
> Druhý agent je ověřil proti dokumentaci a **deset padlo**. Zbylých pět (dva z nich nové)
> je poctivě uvedeno na konci jako úkoly na přípravu — u dvou z nich brání API klíč, který
> na tomto stroji není.
>
> Ta jedenáctka je sama o sobě námět: **výklad, který si dovolí říct „tady nevím",
> se dá ověřit. Výklad, který to zamlčí, se ověřit nedá.**

# FÁZE 4a — Fundament: tři mechaniky LLM pro analytika

> **Publikum:** analytici softwaru, kteří Claude Code používají denně. Vědí, co je terminál,
> co je Git, co je YAML. Netuší, co se děje mezi stiskem Enter a odpovědí.
> **Cíl výkladu:** aby po něm chápali, PROČ jejich zvyky fungují nebo nefungují.
>
> **Stav dokumentu:** 3. verze. Zapracována ověření z `_raw/faze4b-verifikace-a-mezery.md`
> (web, 2026-08-26), měření z `_raw/doklady-kompaktace.md` a `_raw/doklady-cena-kontextu.md`.
> Dvě ověření změnila výklad podstatně — viz „Co se proti 1. verzi opravilo" níže.

---

## Co se proti 1. verzi opravilo (nepřehlédni)

| Původně jsem napsal | Ověřeno, a je to jinak |
|---|---|
| „Tokenizér na slidu 02 decku je zadrátovaný, ale čísla, která zobrazí, jsou ověřená" | **Ten tokenizér vůbec nepočítá tokeny.** Poměr „znaků/token" je jen `text.length / arr.length` nad ručně předrozděleným polem. Je to **ilustrace**, ne měření. Nesmím ji citovat jako doklad. |
| „Angličtina ≈ 3,5 znaku na token (dle decku)" | **≈ 4 znaky na token.** Doslovná citace z oficiálního FAQ: *„1 token is approximately 4 characters or 0.75 words in English."* Deck má na ř. 311 věcnou chybu. |
| „`/compact` není nástroj, je to nehoda — vyhýbej se mu" | **`/compact` přijímá instrukci**: `/compact focus on the auth bug fix`. Dokumentace doslova: *„The summary keeps what you choose instead of what the automatic pass guesses is important."* Doporučení se tím překlápí — viz F-03. |
| „`/compact` mi 51× narazil na strop" | **Ani jednou.** Ve 19 zaznamenaných kompaktacích je trigger **19× `manual`, 0× `auto`**. Vždycky jsem `/compact` napsal sám, při mediánu 464 352 tokenů — tedy na ~58 % okna, dávno před stropem. Problém není že kompaktuju, ale **kdy** a **bez instrukce**. |
| „1M okno beru jako danost" | 1M je **výchozí**, ne beta za příplatek, a **za tokeny nad 200K není cenový příplatek**. Starý mentální model „1M = drahá beta" je potřeba publiku aktivně vyvrátit. |

---

## Vztah k existujícímu decku

V `C:\Git\shared\docs\claude-code\claude-code-jak-funguje.html` **už existuje** laický deck
o tomtéž: 12 slidů (label 00–11), česky. Přečteno včetně JavaScriptu.

**Co deck pokrývá dobře a co tedy nepíšu znovu:** model jako bezstavová funkce (01), tokeny
jako jednotka (02), autoregrese (03), teplota a losování (04), kontextové okno a jeho skladba
(05), prompt caching s cenami (06), kompaktace (07), model vs. harness (08), tool_use jako
dohodnutý JSON (09), agentní smyčka (10), shrnutí (11).

**Čísla u cache na slidu 06 souhlasí** s dokumentací: čtení 10 %, zápis 5 min +25 %, zápis 1 h
+100 % ↔ ověřeno 0,1× / 1,25× / 2×. Na tom lze stavět bez opravování.

**Dvě věcné chyby, které jsem v decku našel** (a jsou to opravy, ne důvod ho zahodit):
1. **Slide 02, ř. 311: „≈ 3,5 znaku na token" — správně je ≈ 4** (doslovná citace z FAQ,
   viz níže). Deck se navíc odvolává na „dokumentaci Anthropic", aniž by uvedl kterou.
2. **„Interaktivní" tokenizér na slidu 02 nepočítá tokeny.** Jsou to dvě ručně předrozdělená
   pole (`TOK_EN`, `TOK_CZ`, JS ř. 596–597) a zobrazený poměr je jen podíl délky a počtu prvků
   toho pole. Je to ilustrace principu, ne měření — a deck to sám v poznámce přiznává
   („rozpad tokenů níže je ilustrativní").

To druhé je mimochodem **samo o sobě dobrá lekce pro workshop:** hezké interaktivní demo
nemusí měřit to, co tvrdí. Řekni to publiku nahlas — jinak si někdo zkusí napsat vlastní větu,
zjistí, že to nejde, a přijdeš o kredit.

**Kde je moje přidaná hodnota.** Deck vysvětluje **mechaniku**. Nemá ani jedno moje číslo
a nikde neříká, co s tou mechanikou má analytik v pondělí ráno dělat.

| Mezera v decku | Co dodávám |
|---|---|
| Bezstavovost je popsaná jako **vlastnost technologie**. Chybí, že z ní plyne **kvadratický náklad session** a že cena tahu nesouvisí s délkou promptu. | Téma 1 + doklad z 2 670 promptů |
| U tokenů má deck chybné číslo a falešné demo. Chybí příčiny (byte premium), identifikátory a cesty, a hlavně praktický důsledek. | Téma 2 + měření + ověřená citace |
| Kompaktace je na slidu 07 popsaná **neutrálně jako feature**. Chybí druhá polovina pravdy — a hlavně chybí, že se dá **řídit instrukcí**. | Téma 3 + 21 měřených kompaktací |
| Slide 05 nemá **výstupy nástrojů ani metadata skillů** a nemá poměry — nevidíš, kdo vyhrává. | Téma 3 + měření startovní režie |

---

## Poznámka k číslům, než začneme

Čtveřičné značení. Publikum si zaslouží vědět, čemu smí věřit — a **rozdíl mezi řádky 1 a 3
je potřeba na workshopu vyslovit nahlas**, protože je to jediná obrana proti tomu, aby si někdo
odnesl odhad jako fakturu.

| Značka | Význam |
|--------|--------|
| **dokumentováno** | Anthropic to píše černé na bílém (URL v `faze4b-verifikace-a-mezery.md`) |
| **změřeno** | Změřeno na stroji autora — přesná hodnota (počet bajtů, znaků, záznam z transkriptu) |
| **odhad** | Výpočet z ověřených veličin. Řádově správné, není to faktura. |
| `[K OVĚŘENÍ: …]` | Nevím a nehádám. |

### Tři sady dat, které se nesmí míchat

**(A) Historie zadaných příkazů** — co jsem kdy napsal:

| Metrika | Celá historie (2 670 promptů, 7 měsíců) | Jen pracovní projekty (1 507 promptů) |
|---|---:|---:|
| `/compact` | 67× | **51×** |
| `/model` | 63× | 53× |
| `/context` | 42× | 37× |
| `/resume` | 58× | 33× |
| `/effort` | 9× | 4× |
| `/clear` | 6× | **1×** |
| medián délky promptu | 75 znaků | 65 znaků |
| max délka promptu | 22 386 znaků | 7 213 znaků |
| promptů nad 1000 znaků | 44 | 31 |

Období 2026-01-19 → 2026-08-26 ≈ **31 týdnů**. Model `opus[1m]`, `effortLevel: high`.

**(B) `compactMetadata` z transkriptů** (`_raw/doklady-kompaktace.md`, skript
`_raw/compact_stats.py`) — nejtvrdší sada, protože **harness si u každé kompaktace sám zapisuje
přesná čísla**: `trigger`, `preTokens`, `postTokens`, `cumulativeDroppedTokens`, `durationMs`
a `preservedSegment`. **19 zaznamenaných kompaktací** (alzask + fhb).

> **Dvě poctivé výhrady, obě řekni nahlas.**
> **(1) Těch 21 je podvýběr, ne úplný počet.** Transkripty na disku pokrývají jen část
> sessions — 84 souborů pro alzask, ale historie zná 175 sessions jen pro tenhle projekt.
> Proto se 19 kompaktací nerovná 51× `/compact` z historie příkazů.
> **(2) Formát `.jsonl` je interní.** Dokumentace výslovně varuje, že *„the entry format is
> internal to Claude Code and changes between versions, so scripts that parse these files
> directly can break on any release"* (dokumentováno) a doporučuje `/export` nebo
> `claude -p --output-format json`. Můj skript funguje **dnes**, na téhle verzi. Není to API.

**(C) Startovní režie kontextu** (`_raw/doklady-cena-kontextu.md`) — kolik je v okně, **než
napíšu první slovo**. Znaky přesné, tokeny odhadem při konzervativních 3,0 znaku/token pro
češtinu (**ten poměr je předpoklad, nikoli dokumentovaná hodnota** — viz téma 2).

---

## 1. LLM je bezstavový

### Co k tomu má deck (slide 01 „Model je bezstavová funkce")

Analogii automatu na text, věty *„mezi dvěma voláními si model nepamatuje vůbec nic"* a
*„‚paměť‘ konverzace je iluze, kterou vytváří okolí"*. To je správné a stačí to — **nepřepisuj
to.** Chybí tam ale úplně **ekonomika**: že přeposílání celé historie má kvadratický charakter
a že cena jednoho tahu nesouvisí s tím, co jsi napsal. To je celý obsah tohoto tématu.

### Podstata

Deck říká „automat na text". Pro analytika je nosnější jiná analogie, protože nese i ten
ekonomický důsledek: **externí konzultant s naprostou amnézií.** Každé ráno přijde a nepamatuje
si nic — ani tebe, ani projekt, ani co včera řekl. Ty mu proto při každé otázce položíš na stůl
**celou složku**: kompletní zápis všeho, co jste si dosud řekli, od první věty. On složku
přečte, odpoví na tvoji poslední otázku, ty jeho odpověď připíšeš do složky — a on odchází
a zapomíná. Zítra to celé zopakujete, jen se složka rozroste.

Rozdíl proti „automatu na text" je ten, že u konzultanta okamžitě vidíš, kdo platí za čtení
té složky. Platíš ty. Při každé otázce. Za celou složku.

A tu složku si můžeš najít. Na stroji autora leží transkripty session projektu AlzaSk
v `C:\Users\<user>\.claude\projects\C--Git-alzask\` — **84 souborů `.jsonl`, dohromady
120,4 MB** (změřeno). Největší jediná session má **18,8 MB a 8 937 záznamů** (změřeno). Když
si takový soubor otevřeš, koukáš se na tu složku. Není to metafora paměti — je to ta paměť.

Nejlepší doklad se ale objevil sám, mimochodem, při přípravě téhle prezentace: **když jsem
data měřil, historie mi během měření povyrostla o 4 prompty — o moje vlastní prompty z toho
měření** (změřeno). Soubor `history.jsonl` roste každým zadáním. Měřicí přístroj se zapsal
do měřeného vzorku, protože „paměť" není stav v modelu — je to append-only soubor na disku,
do kterého se připisuje všechno, včetně toho, když se ptáš na obsah toho souboru.

Z toho plyne rozlišení, které zní jako slovíčkaření, ale je to nejužitečnější věta v celém
výkladu: **model nezapomíná, model přestává vážit.** Když po dvou stech zprávách poruší
instrukci z prvního promptu, ta instrukce tam pořád fyzicky je (pokud mezitím neproběhl
`/compact` — viz téma 3). Model ji vidí. Jen soutěží o pozornost s dvěma sty dalšími zprávami,
z nichž ty poslední se týkají něčeho jiného. Není to výpadek paměti. Je to rozpuštění signálu
v šumu. A léčí se to jinak než zapomínání: ne připomínáním („už jsem ti to říkal"), ale
**přesunutím instrukce na místo, kde má váhu** — na konec promptu, nebo do `CLAUDE.md`, které
se vkládá znovu do každého jednotlivého požadavku.

### Proč to analytika zajímá

**(a) „Už jsem ti to říkal" není argument, je to diagnóza.** Když to řekneš, popsal jsi symptom
a neudělal nic. Nefunguje to ze dvou různých důvodů a je užitečné je odlišit: buď je ta věta
pořád v kontextu a jen se utopila (pak ji zopakuj **teď**, na konci, kde má váhu — nebo ji
povyš do `CLAUDE.md`), nebo v kontextu už není, protože ji sežral `/compact` (pak je opakování
jediná možnost). Praktické pravidlo: **instrukce, kterou potřebuješ dodržet napořád, nepatří
do promptu — patří do `CLAUDE.md`, do pravidla, nebo do hooku** (viz téma 3, páka 5).

**(b) Délka session zdražuje každý další prompt — a to kvadraticky.** Deck tuhle mechaniku
nezmiňuje, přitom je to ta nejméně intuitivní část. Pokud každý tah přidá do složky přibližně
stejně velký kus, pak 1. tah zpracuje 1 kus, 2. tah 2 kusy, 10. tah 10 kusů. Součet za celou
session je řádově **N²/2** — kvadratický v počtu tahů, nikoli lineární.

Konkrétní číslo, a teď už s **měřenými** vstupy: medián kontextu, ve kterém jsem sahal
po `/compact`, byl **464 352 tokenů** (změřeno, 19 kompaktací). Vstup Opus 5 stojí
**$5 / 1M tokenů** (dokumentováno) → **každý** tah v tom stavu nesl přibližně **$2,90**
za vstup, bez cache (odhad z měřené velikosti a dokumentované ceny). Ať jsem napsal „ano",
nebo třístránkové zadání.

Prompt cache (slide 06 decku) tuhle kvadratiku **zlevní, ale nezruší** — a přesně tohle deck
neříká. Čtení z cache stojí 0,1× (dokumentováno) → tentýž tah spadne na ~$0,29. **Objem
zůstává kvadratický, jen se platí desetinovou sazbou.** Cache je **prefixová shoda**: jakákoli
změna bajtu v prefixu zneplatní všechno za sebou, hierarchie `tools → system → messages`
(dokumentováno). Minimální cachovatelný prefix ~1024 tokenů; kratší se tiše necachuje.
A přepnutí modelu vynutí kompletní přestavbu — cache jsou model-scoped a **úniková cesta
neexistuje** (dokumentováno, doslova: „Model switch has no escape hatch").

**(c) Cena promptu nemá nic společného s jeho délkou.** Krátká věta „ne, jinak" v rozjeté
session je dražší než třístránkové zadání na začátku. Tohle je nejkontraintuitivnější věta
celého tématu a je to přesně to, co v decku chybí: **neplatíš za prompt, platíš za session.**

**(d) Bonus, který vyvrací zafixovanou představu:** 1M kontext **není** drahá beta funkce.
Je to **výchozí** kontext aktuální generace (Opus 5, Sonnet 5) a **za tokeny nad 200K není
žádný cenový příplatek** — dokumentace doslova: *„900k-token request je účtován stejnou sazbou
za token jako 9k-token request"* (dokumentováno). Na Max/Team/Enterprise je 1M součástí
předplatného automaticky; na Pro vyžaduje usage credits. Kdo se bojí velkého okna kvůli ceně,
bojí se něčeho, co už dva roky neplatí. **Bát se má objemu, ne sazby.**

### Doklad z mých dat

**Medián délky promptu 65 znaků (pracovní projekty) vs. 31 promptů nad 1000 znaků z 1 507.**
Nejzajímavější číslo z celé sady, protože popisuje **tvar** práce. 98 % promptů je krátkých —
typicky „jo", „ne, jinak", „a ještě to druhé", „proč?". Dvě procenta jsou velká zadání. Tvar je
jasný: **jedno dlouhé zadání na začátku a pak dlouhá řada krátkých korekcí.** A právě tenhle
tvar je motor kvadratického nákladu: dlouhé zadání nastaví velký kontext, každá z těch stovek
krátkých korekcí ho pak celý znovu protlačí modelem. Medián 65 znaků neznamená „používám model
úsporně". Znamená **„platím 1 500× za historii, kterou jsem napsal 31×".**

Doplňkově: v celé historii je maximum promptu 22 386 znaků, v pracovních projektech jen 7 213.
Ta nejdelší zadání tedy nejsou z práce — v práci zadávám kratší a **doptávám se víc**, což ten
kvadratický náklad ještě zvýrazňuje.

**`/resume` 33× v pracovních projektech (58× celkem).** Teď už vím přesně, co se při tom děje
a co ne (dokumentováno, `code.claude.com/docs/en/sessions`):

| Obnoví se | Neobnoví se |
|---|---|
| Celá historie konverzace včetně tool calls a výsledků | **Prompt cache** — po pauze vypršela; první request ji staví od nuly |
| Model (nebyl-li vyřazen nebo vynucen flagem) | **Background Bash a Monitor úlohy — nikdy** |
| Agent (`--agent`) se systémovým promptem, nástroji, modelem | `--mcp-config`, `--settings`, `--plugin-dir`, `--fallback-model`, `--add-dir` |
| Permission mode (s výjimkami) | `plan` a `bypassPermissions` mode — nikdy |
| Naplánované úlohy (`/loop`), nevypršely-li (7 dní) | Adresáře přidané za běhu (`/add-dir`) |

Takže: **první prompt po `/resume` je nejdražší request v celé session** — cache se staví
od nuly nad celou historií. Třiatřicetkrát jsem to zaplatil, než jsem věděl proč. Navíc:
na Pro/Max plánu nabídne Claude Code u session neaktivní >1 h a >100 000 tokenů dialog
**„Resume from summary"** (což spustí `/compact` **hned**) vs. **„Resume full session as-is"**
(plná historie, ale drahá přestavba cache). Kdo tam klikne „from summary", právě si vybral
ztrátu 97 % — viz téma 3.

**`/model` 53× v pracovních projektech.** Padesát tři přepnutí = padesát tři zahození celého
cache prefixu (dokumentováno).

### Co ukázat na obrazovce

**Nejdřív slide 01 decku** (automat na text) — 60 sekund, zavede slovník. Pak už jde vlastní
demo, protože to, co následuje, deck nemá.

**Demo 1a — „paměť je soubor" (60 s, nepotřebuje nic než terminál).**

```bash
ls -laS ~/.claude/projects/C--Git-alzask/*.jsonl | head -5
du -sh ~/.claude/projects/C--Git-alzask/
tail -c 2000 ~/.claude/projects/C--Git-alzask/<aktualni-session>.jsonl | head -40
```

Ukaž: 84 souborů, 120,4 MB, největší 18,8 MB, a strukturu JSON záznamů. Věta: *„To, co si
Claude ‚pamatuje‘, je tenhle soubor. Až tady skončí, skončí paměť. A tenhle soubor se při každém
mém promptu celý znovu posílá na vstup."*

**Demo 1b — pointa o měřicím přístroji (20 s, přílepek k 1a, velmi levný a velmi silný).**
Ukaž počet řádků `history.jsonl`, napiš jeden prompt, ukaž počet znovu. *„Když jsem si tuhle
statistiku měřil, narostla mi o čtyři prompty — o ty, kterými jsem se ptal na tu statistiku."*

**Demo 1c — kvadratika naživo, na jednom slovu (90 s).**
1. `/context` → ukaž aktuální zaplnění.
2. Napiš jednoslovný prompt: `ok`.
3. Znovu `/context`.

Pointa: dvouznakový prompt právě protlačil modelem celý kontext. Publikum vidí na ukazateli,
že cena tahu nemá nic společného s délkou toho, co napsali. Nechej po tom dvě sekundy ticha.

**Příprava:** nic navíc, obojí běží bez API klíče. Mít předem otevřenou **velkou** session
(na malé je efekt nepřesvědčivý) a jednu čerstvou pro srovnání.

### Časté nedorozumění

| Co si lidé myslí | Jak to je |
|---|---|
| „Claude si mě pamatuje, když jsem s ním mluvil včera." | Nepamatuje. Harness mu podal soubor z disku. |
| „Zapomněl, co jsem mu řekl na začátku." | Nezapomněl — buď to má a nevěnuje tomu váhu, nebo to `/compact` fyzicky odstranil. Léčba je v každém případě jiná než výčitka. |
| „Krátký prompt = levný prompt." | Cena tahu = velikost celého kontextu. Dvouznakové „ok" při 583 tisících tokenů je jeden z nejdražších tahů, co uděláš. |
| „Prompt cache znamená, že se za historii neplatí." | Platí se 0,1×. Zápis navíc stojí **1,25×** (5 min) resp. **2×** (1 h) — vrátí se až při druhém resp. třetím použití téhož prefixu (dokumentováno; deck to má na slidu 06 správně). |
| „`/resume` mě vrátí přesně tam, kde jsem byl." | Vrátí historii, model, agenta. **Nevrátí cache** (první request je nejdražší v session) ani background úlohy — ty nikdy (dokumentováno). |
| „1M kontext je drahá beta, radši ho nepoužívám." | Je **výchozí** a za tokeny nad 200K **není příplatek** (dokumentováno). Bát se má objemu, ne sazby. |

---

## 2. Tokenizace

### Co k tomu má deck (slide 02) — a co je na něm špatně

Deck má správnou definici („model nevidí písmena ani slova, ale kousky slov"), správný důraz
(„jednotka, za kterou se platí a která plní kontext") a poctivé přiznání *„přesný poměr pro
češtinu Anthropic nezveřejňuje"*.

**Dvě chyby, obě je nutné na workshopu opravit:**
1. **„≈ 3,5 znaku na token" je věcně špatně.** Dokumentovaná hodnota, doslovná citace
   z oficiálního FAQ: *„As a rough estimate, 1 token is approximately 4 characters
   or 0.75 words in English."* (dokumentováno, `platform.claude.com/docs/en/about-claude/pricing`).
   **Správně ≈ 4 znaky na token.**
2. **Ten „interaktivní tokenizér" tokeny nepočítá.** Jsou to dvě ručně předrozdělená pole
   a zobrazený poměr je jen `text.length / arr.length` nad nimi (změřeno čtením JS, ř. 595–619).
   Je to ilustrace principu, ne měření.

**Co v decku chybí úplně:** příčiny (proč čeština stojí víc), identifikátory a cesty,
a praktický důsledek — který je pravý opak toho, co si publikum ze slidu 02 odnese.

### Podstata

Model nevidí písmena a nevidí slova. Vidí **tokeny** — kousky textu, které dostaly v tréninku
vlastní číslo ve slovníku. Pro angličtinu platí dokumentovaný odhad **≈ 4 znaky na token,
resp. 0,75 slova** (dokumentováno, doslovná citace výše). Běžné anglické slovo bývá tedy
jeden token, delší dva.

Pro češtinu **žádné takové číslo neexistuje.** Dokumentace říká jen *„přesný počet se liší
podle jazyka a typu obsahu"* — a per-jazyk tabulku Anthropic nezveřejňuje (ověřeno jako
**negativní nález** na pricing i token-counting stránce). Tohle je potřeba publiku říct
otevřeně, protože **ta asymetrie je sama o sobě lekce**: pro angličtinu si počet tokenů umíš
odhadnout z hlavy, pro češtinu ne. A my píšeme česky.

Co tedy víme? Dvě věci, každá jiné jistoty.

**Změřit umím znaky a bajty (přesně):**

| Věta | Znaků | UTF-8 bajtů | Slov |
|------|------:|------------:|-----:|
| `Vytvoř funkční požadavek pro naskladnění nosiče` | **47** | 54 | 6 |
| `Create a functional requirement for container putaway` | **53** | 53 | 7 |

(změřeno lokálně, `_raw/_tok.py`)

Ta česká věta je **o 6 znaků kratší.** U anglické umím dopočítat: 53 znaků ÷ 4 ≈ **13 tokenů**
(odhad z dokumentované hodnoty). U české to dopočítat **nedokážu** — a přesně to je ten bod:
kdyby platil stejný poměr, vyšlo by ~12 tokenů, tedy méně. Nevyjde. Ale o kolik víc, nevím
bez `count_tokens`.

**Proč to vůbec vyjde jinak — a tady je nutné rozlišit dvě úrovně jistoty:**

*Obecný princip, doložený literaturou o BPE tokenizaci, nikoli tvrzení specifické pro Claude:*
tokenizéry typu **byte-level BPE** kódují text jako UTF-8 bajty. ASCII znaky = 1 bajt/znak;
znaky s diakritikou (á, č, ř, š, ž) jsou vícebajtové sekvence. Trénovací data slovníků jsou
dominantně anglická, takže frekventované anglické bajtové sekvence se sloučí do velkých,
efektivních tokenů, zatímco vzácnější vícebajtové se slučují méně. V literatuře se tomu říká
**„byte premium effect"** (arxiv 2505.24689 a obecné výklady byte-level BPE). **Toto je obecný
princip, ne dokumentovaný fakt o Claude.**

Tři konkrétní projevy, které umím ukázat na měřených datech:

**(1) Diakritika je vícebajtová.** `příjmu` = 6 znaků / **8 bajtů**; `prijmu` = 6 znaků /
**6 bajtů** (změřeno). Stejné slovo, o třetinu víc surového materiálu, který musí tokenizér
nějak pokrýt.

**(2) Čeština rozprašuje frekvenci flexí.** Nejsilnější příčina, a lidé ji nikdy nevidí:

| Pojem | Povrchové formy | Znaků |
|---|---|---:|
| `nosič, nosiče, nosiči, nosičem, nosičů, nosičům` | 6 forem (a to není všechny) | 47 |
| `container, containers` | 2 formy | 21 |

(změřeno)

Jeden anglický pojem = dvě formy, obě dost frekventované na vlastní token. Tentýž český pojem =
šest a víc forem, každá se šestinou frekvence, žádná dost silná na vlastní záznam ve slovníku.
Skloňování tedy neplatíš jednou, ale u **každého výskytu každého pádu.**

**(3) Identifikátory a cesty jsou horší než čeština.** To, co v decku není vůbec, přitom je to
to, čím analytik plní text nejvíc:

| Řetězec | Znaků | Proč je drahý |
|---|---:|---|
| `PICK_STATION_A2_LOAD` | 20 | Podtržítka a číslice jsou hranice. Rozpad pravděpodobně `PICK`,`_`,`STATION`,`_`,`A`,`2`,`_`,`LOAD` — **odhad 8–10 tokenů**. Tolik jako celá anglická věta. |
| `C:\Git\alzask\docs\fr\comp\wes\` | 31 | Sedm backslashů = sedm hranic, mezi nimi krátké segmenty (`fr`, `comp`, `wes`), na které slovník nemá důvod mít záznam. **Odhad 12–16 tokenů.** |

(znaky změřeny; počty tokenů jsou **odhad**, a to i podle dokumentované hodnoty pro angličtinu —
4 znaky/token by u těch 20 znaků dalo 5 tokenů, což je u identifikátoru s hranicemi nereálně nízko)

### Proč to analytika zajímá

Ze slidu 02 se dá odnést špatný závěr — a většina lidí ho odnese. Špatný závěr zní: „budu psát
promptů méně a úsporněji, ideálně anglicky".

**To je špatně, a to ze dvou důvodů.** Za prvé, prompt jde do modelu **jednou**; nejasný prompt
zaplatíš třemi dalšími tahy na vysvětlování, což je řádově dražší než ušetřené tokeny. Za druhé,
my specifikujeme česky, terminologie je česká a překlad domény do angličtiny je nová chyba,
ne úspora.

**Správný závěr:** šetři tam, co se **opakuje**, ne tam, co jde jednou.

| Text | Kolikrát ho model dostane | Vyplatí se ho krátit? |
|---|---|---|
| Tvůj prompt | 1× (pak už jen jako historie, z cache za 0,1×) | **Ne.** Jasnost je vždycky levnější než úspora. |
| `CLAUDE.md` | **v každém requestu** (v cachovaném prefixu, ale místo v okně zabírá pořád) | **Ano, a hodně.** |
| Popisky skillů | **v každém requestu** (dtto) | **Ano.** |
| Definice nástrojů | **v každém requestu** | Ano, ale to neřídíš ty (MCP servery ano — `/mcp`). |
| Výstupy toolů | 1× při vzniku, pak navždy v historii | Ano — cíleným čtením, viz téma 3. |

Konkrétní číslo, které mi převrátilo prioritu (změřeno, `_raw/doklady-cena-kontextu.md`):
`CLAUDE.md` projektu AlzaSk má **23 427 znaků** (= 25 696 bajtů; ten rozdíl 2 269 je právě
diakritika, mimochodem hezká mini-ilustrace k bodu (1) výše). Při konzervativním předpokladu
3,0 znaku/token pro češtinu je to **odhadem ~7 800 tokenů** v každém requestu každé session.

Srovnání, které to zasadí do kontextu: dokumentace uvádí jako **ilustrativní** velikost
projektového `CLAUDE.md` **1 800 tokenů** (dokumentováno jako ilustrace, ne konstanta).
**Můj je přes čtyřnásobek.** Když z něj vyhodíš tisíc tokenů balastu, ušetříš tisíc tokenů
**krát počet všech tahů ve všech session projektu.** Když zkrátíš prompt o tisíc tokenů,
ušetříš je jednou — a pravděpodobně si koupíš nedorozumění.

Druhý praktický důsledek: **odhadovat počet tokenů z délky textu u češtiny nefunguje** (dokázáno
výše) a **cizí tokenizér je horší než nehádat** — `tiktoken` podhodnocuje o 15–20 % na běžném
textu a víc na kódu a neanglickém vstupu (dokumentováno). Pro nás, kdo píšeme česky a plníme
text cestami, to znamená, že populární „počítadla tokenů" na webu lžou v nejhorším možném směru:
říkají nám, že jsme úspornější, než jsme.

### Doklad z mých dat

**`/context` 37× v pracovních projektech (42× celkem).** Tolikrát jsem se šel ručně podívat,
kolik místa zbývá. To je přesně chování člověka, kterému chybí spolehlivý odhad tokenů „z hlavy" —
a chybí mu právem, protože u češtiny se z délky odhadnout nedá a dokumentace pro ni číslo nemá.
37 kontrol není nedůvěra v nástroj; je to **jediná dostupná metoda měření.**

**Medián promptu 65 znaků (pracovní projekty).** Můj typický prompt je **odhadem ~20 tokenů**.
Zanedbatelný. Ale startovní režie, která k němu jde přiložená, je odhadem **~12 950 tokenů**
(změřené znaky, odhadnutý přepočet — rozpis v tématu 3) — tedy **přibližně 600× víc než můj
průměrný prompt.** Kdybych optimalizoval to, co píšu, řešil bych zlomek procenta problému.

### Co ukázat na obrazovce

**Demo 2a — slide 02 decku jako ilustrace, s dvojím přiznáním (2 min).**
Otevři slide 02, klikni **Angličtina** (zobrazí 39 znaků / 9 tokenů / 4,3), pak **Čeština**
(32 znaků / 11 tokenů / 2,9). Ukaž prstem na barevné kousky: `" agent"`, `" runs"`, `" loop"` =
celá slova; `" ob"`, `"íh"`, `"á"`, `"čku"` = drť. **To je ten princip a je vidět okamžitě.**

Pak **dvě věci přiznej nahlas**, obě do jedné minuty:
> *„Dvě poznámky k tomuhle slidu. První: čísla na něm nejsou naměřená — je to ručně
> předrozdělená ukázka, tokenizér to není. Nezkoušejte tam psát vlastní větu, nejde to.
> Druhá: to ‚3,5 znaku na token‘ je špatně, dokumentace říká čtyři. A teď to nejzajímavější —
> pro češtinu Anthropic žádné takové číslo nezveřejňuje vůbec. Pro angličtinu si to spočítáte
> z hlavy. Pro naši dokumentaci nikdy."*

Tohle vypadá jako obírání sebe o pointu. Není. **Ta asymetrie JE pointa** — a přiznaná chyba
v cizím slidu dá výkladu víc kredibility než cokoli jiného.

**Demo 2b — naše vlastní věty, přesná čísla (2 min). VYŽADUJE PŘÍPRAVU, na živo to nejde.**
Tady je ta část, kterou deck nemá — naše doména. Skript:

```python
from anthropic import Anthropic
client = Anthropic()
for s in ["Vytvoř funkční požadavek pro naskladnění nosiče",
          "Create a functional requirement for container putaway",
          "PICK_STATION_A2_LOAD",
          "C:" + chr(92) + "Git" + chr(92) + "alzask" + chr(92) + "docs" + chr(92) + "fr",
          "příjmu", "prijmu",
          "nosič, nosiče, nosiči, nosičem, nosičů, nosičům",
          "container, containers",
          open(r"C:\Git\alzask\CLAUDE.md", encoding="utf-8").read()]:
    n = client.messages.count_tokens(model="claude-opus-5",
                                     messages=[{"role":"user","content":s}]).input_tokens
    print(n, repr(s[:60]))
```

**Co potřebuješ:** `pip install anthropic` + API klíč (`ANTHROPIC_API_KEY`, nebo `ant auth login`
— na stroji autora **není ani jedno**, změřeno; je to úkol na přípravu). Model musí být **stejný**,
jaký reálně používáš — počty jsou model-specific. Endpoint je zdarma, limit dle usage tier
(Start 2000 req/min). Výstup dej na jeden slide jako tabulku a **hlavní číslo ať je počet tokenů
`CLAUDE.md`** — to je ten, který mění chování publika.

**Není jiná cesta:** veřejný tokenizér pro Claude bez autentizace **neexistuje** — žádný widget
v Console, žádný stažitelný vocab soubor (ověřeno jako negativní nález). `count_tokens` je jediná
dokumentovaná cesta a vyžaduje přihlášení.

**Fallback, když klíč do workshopu nebude:** neříkej žádná čísla tokenů. Řekni jen měřené znaky
(47 vs. 53), dokumentované 4 znaky/token pro angličtinu, a **že pro češtinu to číslo nikdo
nezveřejnil.** Je to slabší demo, ale je poctivé — a poctivost je tady důležitější, protože
celý zbytek prezentace stojí na tom, že moje čísla drží.

**Demo 2c — cena identifikátoru (30 s, přílepek k 2b).**
*„Jeden identifikátor našeho systému stojí přibližně tolik, kolik celá anglická věta. Když
v jedné odpovědi zmíníme dvacet cest, je to samostatný odstavec textu, který nikdo nenapsal."*

**Demo 2d — skloňování (30 s, volitelné, ale je to ten ‚aha‘ moment).**
`nosič, nosiče, nosiči, nosičem, nosičů, nosičům` (47 znaků) proti `container, containers`
(21 znaků; změřeno). *„Angličtina má na tenhle pojem dvě slova. My šest. A platíme za skloňování
při každém jednotlivém výskytu."*

### Časté nedorozumění

| Co si lidé myslí | Jak to je |
|---|---|
| „Token = slovo." | Token = kousek. V angličtině ≈ 4 znaky / 0,75 slova (dokumentováno). Identifikátor `PICK_STATION_A2_LOAD` odhadem 8–10 tokenů. |
| „Ten tokenizér v prezentaci si můžu vyzkoušet na své větě." | Nemůžeš — nepočítá tokeny, je to ručně předrozdělená ukázka (změřeno v JS). |
| „Angličtina má 3,5 znaku na token." | **4** (dokumentováno, doslovná citace z FAQ). Deck má chybu. |
| „Pro češtinu je poměr asi 2,5–3." | To je **můj předpoklad pro přepočty, nikoli dokumentovaná hodnota.** Anthropic per-jazyk čísla nezveřejňuje (negativní nález). Tuhle nejistotu neschovávej. |
| „Čeština stojí víc, protože je delší." | **Ne.** Změřeno: naše česká věta je o 6 znaků **kratší**. Příčina je pokrytí slovníku (byte premium effect), ne délka. |
| „Spočítám si to tokenizérem z webu." | Pro Claude to nefunguje. `tiktoken` podhodnocuje o 15–20 %, na neanglickém vstupu víc (dokumentováno). |
| „Budu tedy psát prompty kratší / anglicky." | Špatný závěr. Prompt jde do modelu jednou. Šetři v `CLAUDE.md` a v popiskách skillů. |
| „Diakritiku vynechám, ať šetřím." | Ušetříš málo a rozbiješ dohledatelnost, terminologii i grepovatelnost. Bod je o `CLAUDE.md`, ne o mrzačení češtiny. |

---

## 3. Kontextové okno

### Co k tomu má deck (slidy 05, 06, 07)

Slide 05 („Kontext — jediné, co model vidí") má správnou skladbu okna a milionový strop.
Slide 06 má prompt caching s korektními cenami. Slide 07 („Když dojde místo: kompaktace")
popisuje kompaktaci a staví ji do kontrastu „s kompaktací / bez kompaktace".

**Co v decku chybí:**
1. Slide 05 **nezmiňuje výstupy nástrojů ani popisky skillů** — přitom výstupy nástrojů jsou
   obvykle ten největší žrout a popisky skillů ta nejvíc překvapivá položka.
2. Slide 05 nemá **poměry** — nevidíš, kdo z těch vrstev vyhrává.
3. Slide 07 popisuje kompaktaci **neutrálně jako feature**, a hlavně **neřekne, že se dá řídit
   instrukcí.** To je nejcennější jednotlivá informace v celém tomto tématu.
4. Chybí celá **hierarchie protiopatření** (subagenti, `/clear`, workspace soubory, cílené
   čtení, hook po kompaktaci).

### To napětí u kompaktace — vytáhni ho explicitně

Slide 07 říká: *„starší část konverzace shrne a nahradí souhrnem. Zůstane záměr úkolu, klíčová
rozhodnutí a stav souborů; zahodí se doslovné výstupy nástrojů a mezikroky"* a *„Okno se uvolní,
session pokračuje dál."*

Tenhle popis je **věcně správný a nechci ho opravovat.** Dokumentace ho potvrzuje do detailu:
shrnutí obsahuje záměr a požadavky uživatele, klíčové technické koncepty, soubory s důležitými
úryvky, chyby a jejich opravy, nedokončené úkoly a aktuální stav práce (dokumentováno). A část
konverzace se zachová **doslovně** — v metadatech je na ni ukazatel `preservedSegment` (změřeno).
Není to tedy „celá historie na kaši".

Co k tomu ale patří a na slidu není:

> **Kompaktace ti session zachrání — a ty nevíš, co z ní vypadlo. Obojí je pravda a to napětí
> je pro tvou práci důležitější než kterákoli z těch dvou verzí samostatně.**

Formulace „zahodí se doslovné výstupy nástrojů a mezikroky" zní jako popis kontrolovaného úklidu —
jako by někdo věděl, co je odpad. **A tady je ta zásadní novinka: můžeš mu to říct.** Dokumentace,
doslova: *„run `/compact` with instructions, like `/compact focus on the auth bug fix`, before
starting a long new task. The summary keeps what you choose instead of what the automatic pass
guesses is important."* (dokumentováno)

Bez instrukce hádá. **Ve všech 21 zaznamenaných případech jsem `/compact` napsal bez instrukce**
(změřeno). To není abstraktní riziko — to je konkrétní, doložená chyba, kterou udělá i publikum.
A oprava je **jedno slovo za příkazem.**

Zip je bijekce: co vložíš, to rozbalíš. Shrnutí je **projekce** — něco jde dovnitř a nevyjde to
zpátky. Lepší přirovnání než „úklid": `/compact` je zápis z osmihodinové porady, který napsal
někdo jiný, **a nahrávka porady se smazala.** Zápis je užitečný. Ale nikdy nezjistíš, co v něm
není — nemáš proti čemu srovnat. Rozdíl s instrukcí je ten, že zapisovateli aspoň řekneš,
na co si má dát pozor.

Co typicky nepřežije:
- **doslovné výstupy nástrojů** — čísla řádků, přesná znění, konkrétní hodnoty (deck to přiznává);
- **odmítnuté varianty a proč** — „zkusili jsme X, nešlo to, protože Y" se srazí na „použij Z",
  a tím se ztratí obrana proti tomu, aby model X zkusil znovu;
- **tvoje explicitní zákazy z rané fáze** — přesně ta kategorie, u které si nejvíc myslíš,
  že ji model „dostal";
- **popisky skillů!** Dokumentace doslova: *„this listing is not re-injected after `/compact`.
  Only skills you actually invoked get preserved"* (dokumentováno). **Po kompaktaci Claude
  dočasně neví, jaké skilly má k dispozici** — kromě těch, které už použil. To je konkrétní,
  mechanické vysvětlení pocitu „po compactu je hloupější". Není to dojem. Je to dokumentovaná
  ztráta schopností.

Typický symptom, který každý v publiku zažil: po `/compact` se agent vrátí k chybě, kterou jsi
mu už dvakrát zakázal — nebo přestane používat skill, který předtím používal. Neignoruje tě.
Ta informace v jeho vstupu **fyzicky není.** Tohle je jediný případ, kde je „zapomněl" popisně
správné slovo: bez kompaktace model nezapomíná, jen nevěnuje váhu; **s kompaktací zapomíná
doopravdy.**

### Podstata — co okno plní

Kontextové okno je jediná deska stolu, na kterou se musí naráz vejít **všechno**, co model
při jednom tahu vidí. U `opus[1m]` je to **1 000 000 vstupních tokenů** (dokumentováno; `opus[1m]`
je platný alias v `/model`, na Max/Team/Enterprise součást předplatného, na Pro za usage credits,
vypnout jde přes `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`). Zní to jako nekonečno. Není.

**Startovní režie — změřeno, co je v okně, než napíšu první slovo** (`_raw/doklady-cena-kontextu.md`):

| Zdroj | Znaků (změřeno) | Tokenů (odhad @3,0) |
|---|---:|---:|
| `CLAUDE.md` projektu alzask | 23 427 | ~7 809 |
| Paměť alzask (`MEMORY.md`) | 13 426 | ~4 475 |
| Output style „Feynman CZ" | 1 985 | ~661 |
| **Součet z souborů, které umím přečíst** | **38 838** | **~12 946** |

A k tomu se přidávají tři věci, které v žádném souboru nejsou — jsou uvnitř harness:

| Vrstva | Ilustrativní hodnota z dokumentace | Poznámka |
|---|---:|---|
| Systémový prompt Claude Code | ~4 200 tokenů | dokumentováno **jako ilustrace**, ne konstanta |
| Popisky skillů | ~450 tokenů | dtto; u mě ~50 skillů v listingu, tedy pravděpodobně víc |
| Environment info + auto memory + MCP názvy | ~1 080 tokenů | dtto |

Dokumentace u těch čísel výslovně píše: *„Token counts are illustrative. Actual values vary with
your CLAUDE.md size, MCP servers, and file lengths."* Přesné číslo pro tvůj stroj dá **jedině
`/context`**. Ale i ta ilustrativní čísla ukazují poměr: **režie je řádově 15–20 tisíc tokenů,
což je 600× můj medián promptu** (65 znaků ≈ 20 tokenů).

**Dvě položky, které slide 05 nemá vůbec:**

**Popisky skillů.** Skill má dvě části: obsah (načte se, až ho vyvoláš) a **popisek — jméno
a jednořádkový popis, který je v kontextu od začátku session, aby model věděl, že skill
existuje.** Přesná mechanika (dokumentováno): popisky jsou součástí **systémového promptu**,
tedy spadají do **cachovaného prefixu** — při dalších requestech v téže konverzaci se čtou
za 0,1×. **Ale místo v okně zabírají pořád.** Cache snižuje cenu za token, ne počet tokenů
v okně. V této session je v listingu ~50 skillů (změřeno spočítáním), většinu z nich dnes
nevyvolám. Konkrétní příklad: popisek skillu `claude-api` není jednořádková věta — je to celý
odstavec s pravidly TRIGGER a SKIP, odhadem 150–250 tokenů, které zabírají místo nezávisle
na tom, jestli ho použiju. (A skilly s `disable-model-invocation: true` jsou z kontextu
úplně mimo, dokud je nezavoláš — dokumentováno.)

Že je to reálný problém, přiznává sám harness: nástroje v této session jsou částečně
**deferred** — v promptu je jen jejich jméno, schéma se dotáhne až na vyžádání přes
`ToolSearch`. Někdo v Anthropicu narazil na přesně tenhle strop a musel ho obejít. Dobrá
zpráva pro publikum: nejste hloupí, že vám kontext teče; teče i lidem, kdo ten nástroj staví.

**Výstupy nástrojů obvykle vyhrají.** Jeden `Read` na velký YAML. Jeden `grep` bez `head_limit`
přes celý repozitář. Jeden `npm test` s dvěma tisíci řádky logu. Kterákoli z těch tří věcí je
jednorázově větší než tvoje celá dosavadní konverzace — a **zůstane v historii navždy**, protože
historie je append-only. Nezaplňuje ti okno to, co píšeš. Zaplňuje ti ho to, co si necháš přečíst.

**A kdy přijde auto-kompaktace?** Není to jedno procento (dokumentováno):
u **Sonnet 5 kolem 967 000 tokenů** (výchozí), u Sonnet 4.6 / Opus 4.6 bez extended context
na 200K. Nastavitelné třemi způsoby: `/autocompact 500k`, flag `--autocompact`, nebo env
`CLAUDE_CODE_AUTO_COMPACT_WINDOW` (rozsah 100K–1M, env má nejvyšší prioritu).
**Já se do auto-kompaktace nikdy nedostal** — 21 z 19 kompaktací bylo ručních (změřeno).

### Pět pák, jak si kontext udržet — od nejsilnější

**(1) Subagenti.** Zdaleka největší pákový efekt. Subagent má **vlastní kontextové okno**.
Přečte si čtyřicet souborů, prohrabe se repozitářem, udělá deset grepů — a do tvého okna se
z toho vrátí jen jeho **závěr**. Ten hluk zůstane v jeho okně a s ním zmizí. Řádový poměr:
agent spotřebuje odhadem 50 000–80 000 tokenů na průzkum a vrátí 300–500 tokenů. **Redukce
o dva řády** za cenu toho, že ztratíš doslovnost (u průzkumu obvykle nevadí).

Kritérium: **„odpověď je krátká, ale cesta k ní je dlouhá."** Hledání „kde v repozitáři je
definované X" je učebnicový případ. Editace, u které potřebuješ vidět přesné znění, subagentovi
nepatří.

**(2) `/clear` při přepnutí tématu — a je to ZDARMA.** Nejdůležitější věc, kterou jsem se naučil
až při přípravě téhle prezentace: **`/clear` neposílá žádný request**, prostě začne novou prázdnou
konverzaci (systémový prompt + projektový kontext, bez historie). Proto je zdarma — dokumentace
doslova: *„When you want a fresh start instead of continuity, `/clear` costs nothing."*
`/compact` naproti tomu **posílá sumarizační request nad celou historií** — a odtud ten medián
180,7 s (viz níže). Na starou cache `/clear` nesahá, ta prostě vyprší po TTL.

Kdy je to správná volba: **když jdeš na nesouvisející úkol.** Tam kompaktace pracuje na
zachování návaznosti, kterou už nepotřebuješ — a platíš za to časem i ztrátou.

**(3) `/clear` s předáním přes soubor** — pro případ, kdy návaznost potřebuješ: napiš stav
do souboru (`spec/<task>/handoff.md`, workspace poznámka) → `/clear` → v čerstvé session ten
soubor načti. Zásadní rozdíl proti `/compact`: **rozhoduješ TY, co přežije — a můžeš si to
před smazáním přečíst.** `/compact` je shrnutí, které za tebe napsal někdo jiný a nedal ti ho
zkontrolovat; `/clear` s handoffem je shrnutí, které jsi podepsal.

**(4) Cílené čtení a workspace soubory místo kontextu.** `sed -n '100,160p'` místo `cat`,
`grep -n` s `head_limit` místo `grep -r` naslepo, `head -50` na výstup buildu. A dlouhodobý stav
(rozhodnutí, otevřené otázky, TODO) nemá žít v historii konverzace — má žít **na disku**. Disk
je persistentní a nekonečný; kontext ani jedno. Přesně to dělá `spec-factory` se svým per-úloha
workspace. Root `CLAUDE.md` tohohle projektu tuhle disciplínu už **kodifikuje** — u ontologie
stojí doslova *„Zdroj pravdy je `docs/ontology/ontology.yaml` (nikdy nenačítat celý)"* a *„ve
velkých souborech (`TERMS.tsv`, `RELATIONS.tsv`) grepuj"*. To není estetická preference. To je
řízení kontextu zapsané do pravidla, protože jednou bolelo.

**(5) `/compact <instrukce>`, a hook, který doplní zbytek.** Když už do kompaktace jdeš, **řekni
jí, co zachovat.** A dokumentovaný vzor, jak si po ní automaticky vrátit to podstatné, je
**`SessionStart` hook s `matcher: "compact"`** (nikoli `PreCompact` — ten sice existuje, ale
dokumentace k němu nemá příklad). `SessionStart` dostává pole `source` s hodnotami `startup` /
`resume` / `clear` / `compact` / `fork`, takže matcher `"compact"` odchytí přesně ten moment
po kompaktaci a stdout příkazu se přidá do kontextu. Dokumentovaný příklad:

```json
{"hooks":{"SessionStart":[{"matcher":"compact","hooks":[
  {"type":"command","command":"echo 'Připomínka: konvence FR viz docs/fr/CLAUDE.md'"}]}]}}
```

Řeší přesně tu situaci „51× `/compact`, co se ztratilo" — po každé kompaktaci automaticky
připomene projektové konvence, aktuální úkol, poslední commity (`git log --oneline -5`).
**Netestováno — vlastní zkušenost s tím nemám.**

### Doklad z mých dat

Tady jsou ta nejtvrdší čísla celé prezentace, protože si je **harness zapsal sám**
(`compactMetadata`, 19 kompaktací, `_raw/doklady-kompaktace.md`):

| Metrika | Hodnota (změřeno) |
|---|---:|
| Zaznamenaných kompaktací | 21 |
| **Ručních (`/compact`) / automatických** | **19 / 0** |
| Z toho s instrukcí (`/compact <co zachovat>`) | **0 / 21** |
| Medián kontextu **před** kompaktací | **464 352 tokenů** |
| Maximum před kompaktací | 618 390 tokenů |
| Medián kontextu **po** kompaktaci | **13 344 tokenů** |
| **Medián zahozeného podílu** | **97,3 %** |
| Rozsah zahozeného | 85,0 % – 98,7 % |
| **Medián doby kompaktace** | **180,7 s** |
| Nejdelší kompaktace | 224,1 s |
| **Celkem zahozeno** | **8 601 191 tokenů** |

**Čtyři interpretace, a jedna z nich mě vyvedla z omylu.**

**(1) Nula automatických. To je vlastně obhajitelná praxe — a mění diagnózu.** Původně jsem
tohle chtěl vyprávět jako „narazil jsem na strop 51×". Data říkají něco jiného: **vždycky jsem
`/compact` napsal sám**, ve chvíli, kdy jsem věděl, že úsek je uzavřený. To je řízený zásah,
ne nehoda. Diagnóza tedy není „kompaktuješ", ale **„kompaktuješ pozdě a bez instrukce"**.

**(2) Čekal jsem do 583 tisíc tokenů a pak zahodil 97,3 %.** To je ~58 % milionového okna —
dávno před stropem (auto by přišlo kolem 967K). Zbytečně pozdě: kdybych stav průběžně přenášel
do souboru, zahodil bych mnohem méně informace, protože bych ji měl na disku. **Tohle je jádro
celého tématu:** neztratil jsem informaci proto, že se okno zaplnilo. Ztratil jsem ji proto, že
jsem s ní nic neudělal, dokud okno nebylo z 58 % plné.

**(3) Kompaktace trvá skoro tři minuty.** Medián **180,7 s**, nejdelší 224,1 s (změřeno).
Teď už vím proč: `/compact` posílá **další request přes celou dosavadní konverzaci**
(dokumentováno) — model musí přečíst 583 tisíc tokenů, aby napsal shrnutí. Ta operace není
zdarma ani rychlá. Pro srovnání: `/clear` neposílá nic, je okamžitý a zdarma.
**Dvacetkrát × tři minuty ≈ hodina čekání**, kterou jsem věnoval operaci, jež mi zahodila 97 %
kontextu — a kterou bych ve většině případů mohl nahradit `/clear`.

**(4) 8 601 191 zahozených tokenů.** Číslo, které funguje samo. Jedenáct a sedm desetin milionu
tokenů, které jsem nechal projít modelem a pak zahodit — a u žádného z nich nemám seznam toho,
co v nich bylo.

**`/clear` 1× proti `/compact` 51× v pracovních projektech.** Poměr **1 : 51** — a teď, když vím,
že `/clear` je zdarma a okamžitý, je to nejostřejší číslo z celé sady. Padesátkrát jsem zaplatil
tři minuty čekání a ztrátu 97 % za operaci, kterou by ve velké části případů (přepnutí
na nesouvisející úkol) nahradila operace za nula sekund a nula dolarů.

A je to učená bezmoc, ne lenost: **`/compact` je ten příkaz, který si člověk pamatuje, protože
mu ho nástroj nabízí jako řešení plného kontextu.** `/clear` musíš znát. Pointa pro publikum:
*„Padesát jedna ku jedné. Ne proto, že bych byl nepořádný — proto, že jsem znal jen jednu
z těch dvou možností. Vy dnes odcházíte s oběma."*

**`/context` 37× proti `/compact` 51×.** Poměr 0,73. Na každé tři kompaktace dva preventivní
pohledy na ukazatel. Čte se to jako záznam někoho, kdo **reagoval častěji, než předcházel** —
a to je poctivá diagnóza, ne sebemrskačství. Řízení kontextu se nikde neučí. Není to feature
v release notes, není to v žádném tutoriálu. Je to **samostatná disciplína**, kterou se každý
učí naostro. Jedenáct milionů zahozených tokenů je má učební cena.

**Největší session `8671e215` — 18,8 MB, 8 937 záznamů, 6 kompaktací, 3 099 305 zahozených
tokenů** (změřeno). Přes tři miliony tokenů prošlo jednou session, jejíž okno má milion.
Nevešla se a nemohla vejít. Poučení: i s milionovým oknem je limit reálná věc, kterou překročíš
za jeden pracovní den.

### Co ukázat na obrazovce

**Demo 3a — slide 05 decku, pak `/context` proti němu (2 min).**
Nejdřív slide 05 — hezký obrázek, správná skladba. Pak přepni do terminálu a spusť `/context`.
Věta: *„Tohle je ten samý obrázek, jen naměřený. A jsou v něm dvě položky, které na slidu nejsou."*
Projdi řádky prstem a nech publikum **uhodnout, kdo vyhrává**, než jim to ukážeš. Pak ukaž řádek
s popisky skillů a zeptej se: *„Kolik z těch padesáti jsem dnes použil?"*

**Demo 3b — `compactMetadata`: harness si to zapsal sám (2 min). NEJPŘESVĚDČIVĚJŠÍ DOKLAD.**
Nemusíš nic vymýšlet — čísla jsou v transkriptu. Spusť hotový skript:

```bash
python C:/tmp/workshop-namety/_raw/compact_stats.py
```

Nebo ukaž jeden konkrétní záznam a **přečti `preTokens` → `postTokens` naživo**:
464 352 → 13 344. Věta: *„To ‚97 % zahozeno‘ není moje interpretace. To je číslo, které si
Claude Code sám zapsal do transkriptu, včetně toho, jak dlouho to trvalo."*

**Výhrady, obě řekni:** (a) 19 kompaktací je **podvýběr** — transkripty pokrývají jen část
sessions; (b) formát `.jsonl` je **interní a mezi verzemi se mění** (dokumentace před parsováním
výslovně varuje a doporučuje `/export`), takže tenhle skript funguje dnes, na téhle verzi.

**Demo 3c — slide 07 a to, co na něm chybí (3 min).**
Ukaž slide 07 a **přečti nahlas** jeho vlastní věty o kompaktaci. Pak: *„Všechno na tomhle
slidu je pravda. A chybí tam dvě věty."* První: analogie o zápisu z porady, u které smazali
nahrávku, a číslo **97,3 %**. Druhá — a tu pověz jako pointu: *„A hlavně: tomu shrnutí můžete
říct, co má zachovat. `/compact focus on the auth bug fix`. Já jsem to jednadvacetkrát z
jednadvaceti neudělal."* Pak ukaž na **51 : 1** a na **180,7 s**.

**Demo 3d — dva způsoby, jak zjistit totéž (3 min). NEJSILNĚJŠÍ DEMO CELÉHO WORKSHOPU.**
Čerstvá session a otázka s krátkou odpovědí a dlouhou cestou — třeba *„kolik FR souborů má
ve frontmatteru status `draft`?"*
1. `/context` → zapiš na tabuli výchozí číslo.
2. **Cesta A (naivně):** nech Claude přečíst velké soubory rovnou — `Read` na
   `docs/pbs/pozadavky.md`, `Read` na velký YAML, `grep -r` bez limitu.
3. `/context` → zapiš. **Ukaž skok.**
4. `/clear` (a poznamenej: *„tohle bylo zdarma a okamžité"*).
5. **Cesta B (subagentem):** stejná otázka zadaná subagentovi (`Agent` / `Explore`).
6. `/context` → zapiš. **Ukaž, že se skoro nepohnul.**

Tři čísla vedle sebe na tabuli jsou celý argument pro subagenty, bez jediného slidu.
**Příprava:** vyzkoušej předem — cesta A musí dát **viditelný** skok a subagent v cestě B musí
uspět. Měj čísla z předběžného běhu jako záložní plán.

**Volitelně místo 3a, pokud bude čas na meta-demo:** `/insights` analyzuje až 200 posledních
sessions na stroji a vygeneruje HTML report o tom, jak s nástrojem pracuješ. **Netestováno**,
ale jako otvírák workshopu o vlastních zvycích je to nabíledni.

### Časté nedorozumění

| Co si lidé myslí | Jak to je |
|---|---|
| „Mám milionové okno, kontext neřeším." | Moje největší session protlačila přes 3 miliony tokenů a šestkrát kompaktovala (změřeno). Milion je jeden pracovní den, ne nekonečno. |
| „`/compact` kontext zmenší." | **Shrne.** Medián: 464 352 → 13 344 tokenů, tedy **97,3 % zahozeno** (změřeno). Session ti zachrání (deck má pravdu) a zároveň nevíš, co vypadlo. |
| „Kompaktace ví, co je odpad." | Bez instrukce **hádá** — dokumentace to říká doslova („what the automatic pass guesses"). S instrukcí `/compact focus on X` zachová, co určíš ty. |
| „`/compact` je rychlý příkaz." | Medián **180,7 s**, nejdelší 224,1 s (změřeno). Posílá další request přes celou historii (dokumentováno). `/clear` neposílá nic — je okamžitý a zdarma. |
| „`/clear` je hrubší varianta `/compact`." | Opačně. `/clear` je **zdarma a okamžitý** a ty rozhoduješ, co si přeneseš. `/compact` rozhoduje za tebe, trvá tři minuty a zahodí 97 %. Můj poměr 1 : 51 ukazuje, že jsem to měl přesně obráceně. |
| „Po compactu je Claude hloupější — to je jen dojem." | **Není.** Popisky skillů se po `/compact` **znovu nenačtou**; zachovají se jen skilly, které už použil (dokumentováno). Fyzicky neví, co má k dispozici. |
| „Zaplňuje mi to hlavně dlouhá konverzace." | Obvykle výstupy nástrojů. Jeden `Read` velkého souboru přebije desítky tahů — a zůstane v historii navždy. Slide 05 tuhle položku vůbec nemá. |
| „Skilly, které nepoužívám, mě nic nestojí." | Za tokeny platíš 0,1× (jsou v cachovaném prefixu), **ale místo v okně zabírají plnou cenu.** Cache snižuje sazbu, ne objem. |
| „Subagent je na složité úkoly." | Subagent je na úkoly, kde je **odpověď krátká a cesta dlouhá**. Není to o složitosti, je to o poměru hluku k výsledku. |

---

## Návrh námětů do katalogu

### F-01 — Claude si tě nepamatuje. Vede si o tobě složku.
**O čem to je:** Nadstavba nad slidem 01 decku. Deck říká, že model je bezstavový; tenhle blok
říká, **co to stojí**. Cena tahu nesouvisí s délkou tvého promptu, náklad session je kvadratický,
první request po `/resume` je nejdražší v celé session, a „už jsem ti to říkal" není argument,
ale diagnóza. Vyvrací i zafixovanou představu „1M kontext je drahá beta".
**Doklad:** 84 transkriptů / 120,4 MB na disku; největší session 18,8 MB / 8 937 záznamů;
při mediánu 464 352 tokenů nesl **každý** tah ~$2,90 vstupu bez cache (odhad z měřené velikosti
a dokumentované ceny $5/MTok); `/resume` 33× v pracovních projektech, přičemž `/resume`
prokazatelně **neobnovuje prompt cache** (dokumentováno). A nejlepší doklad: při měření statistik
mi historie narostla o 4 prompty — o ty, kterými jsem se ptal na tu statistiku.
**Role:** [výklad] + [demo]
**Náročnost pro publikum:** nízká
**Odhad:** 12 min (2 slide 01 + 10 vlastní)
**Závislosti:** slide 01 decku jako 2minutový úvod (nepřepisovat)
**Co ukážu na obrazovce:** `ls -laS ~/.claude/projects/C--Git-alzask/*.jsonl` + `du -sh`
(84 souborů, 120,4 MB) → `tail` transkriptu, ať vidí strukturu záznamů → počet řádků
`history.jsonl`, jeden prompt, počet znovu („měřicí přístroj se zapsal do vzorku") → `/context`,
pak jednoslovný prompt `ok`, pak `/context` znovu: dvouznakový prompt právě protlačil modelem
celý kontext.
**Priorita:** must
**Výhrada:** Bezstavovost i cena jsou dvě různé pointy a při 12 minutách hrozí, že splynou.
Pokud musím škrtat, škrtám bezstavovost — tu deck už má. Cena za session je ta část, kterou
publikum nedostane nikde jinde.

### F-02 — Čeština není dražší, protože je delší (a ten slide má chybu)
**O čem to je:** Tokenizace poctivě. Měřené znaky ukazují, že česká věta je **kratší** než
anglická a přesto stojí víc — takže to není o délce, ale o pokrytí slovníku (byte premium effect).
Součástí je oprava dvou chyb v existujícím decku: „3,5 znaku na token" je špatně (správně **4**,
doslovná citace z FAQ) a jeho „interaktivní tokenizér" tokeny vůbec nepočítá. A pointa, která
z toho vypadne: **pro angličtinu si počet tokenů spočítáš z hlavy, pro češtinu ho Anthropic
nezveřejnil vůbec.** Praktický důsledek: šetři tam, co se opakuje (`CLAUDE.md`, popisky skillů),
ne tam, co jde jednou (prompt).
**Doklad:** Změřeno — `Vytvoř funkční požadavek pro naskladnění nosiče` = 47 znaků proti
`Create a functional requirement for container putaway` = 53 znaků; `příjmu` = 8 bajtů proti
`prijmu` = 6; šest českých forem „nosiče" = 47 znaků proti `container, containers` = 21.
Dokumentováno — 1 token ≈ 4 znaky / 0,75 slova v angličtině; pro jiné jazyky **žádné číslo**
(negativní nález). A hlavní číslo: `CLAUDE.md` AlzaSk = **23 427 znaků, odhadem ~7 800 tokenů**
v každém requestu, proti dokumentované **ilustrativní** hodnotě 1 800 tokenů = **přes
čtyřnásobek**; medián mého promptu je proti tomu ~20 tokenů.
**Role:** [demo] + [výklad]
**Náročnost pro publikum:** střední
**Odhad:** 10 min
**Závislosti:** slide 02 decku (jako ilustrace principu, s přiznáním)
**Co ukážu na obrazovce:** Slide 02, klik Angličtina → 39/9/4,3; klik Čeština → 32/11/2,9,
a prstem na kousky: `" agent"`, `" runs"` = celá slova; `" ob"`, `"íh"`, `"čku"` = drť. **Pak dvě
přiznání nahlas:** čísla nejsou naměřená (ručně předrozdělené pole, nejde tam psát) a „3,5" je
špatně, správně 4 — *„a pro češtinu žádné číslo neexistuje."* Pak vlastní slide s výstupem
`count_tokens` pro naše věty, `PICK_STATION_A2_LOAD`, cestu a `CLAUDE.md`.
**Priorita:** must
**Výhrada:** Pro naše věty **nemám přesná čísla** — na stroji není API klíč (změřeno) a veřejný
tokenizér bez autentizace **neexistuje** (ověřeno jako negativní nález). Bez klíče musí demo
skončit u měřených znaků a dokumentované hodnoty pro angličtinu, **bez vyslovení čísel tokenů
pro češtinu.** Je to slabší, ale poctivé — a celý zbytek prezentace stojí na tom, že moje čísla
drží. Druhá výhrada: hrozí, že si publikum odnese „psát anglicky / bez diakritiky" — musí být
explicitně vyvráceno, ne jen neřečeno.

### F-03 — Tomu shrnutí můžeš říct, co má zachovat
**O čem to je:** Nejsilnější akční námět celé prezentace, a překlopil se ověřením.
`/compact` **přijímá instrukci** (`/compact focus on X`) — dokumentace doslova: *„The summary
keeps what you choose instead of what the automatic pass guesses is important."* Bez instrukce
hádá. Já jsem ji ve **21 z 21** zaznamenaných kompaktací nedal. Doporučení pro publikum tedy
není „vyhýbej se kompaktaci", ale trojice: **(1)** nedostat se do ní (průběžně přenášej
do souboru), **(2)** když už, tak s instrukcí, **(3)** na nesouvisející úkol `/clear` — je zdarma.
Součástí je vědomé napětí proti slidu 07 decku: kompaktace session zachrání **a** ty nevíš,
co z ní vypadlo. Obojí je pravda.
**Doklad:** 19 kompaktací, **21× manual / 0× auto, 0× s instrukcí** (změřeno). Medián
**464 352 → 13 344 tokenů = 97,3 % zahozeno**. Celkem **8 601 191 zahozených tokenů**.
A mechanické vysvětlení pocitu „po compactu je hloupější": popisky skillů se po `/compact`
**znovu nenačtou**, zachovají se jen ty už použité (dokumentováno).
**Role:** [výklad] + [demo] + [příběh]
**Náročnost pro publikum:** nízká
**Odhad:** 10 min
**Závislosti:** F-01 (bez bezstavovosti není jasné, proč vůbec něco „vypadává"); slide 07 decku
**Co ukážu na obrazovce:** Slide 07 a **přečtu nahlas jeho vlastní věty**. Pak: *„Všechno na tomhle
slidu je pravda. A chybí tam dvě věty."* → analogie o smazané nahrávce + **97,3 %** → a pointa:
*„tomu shrnutí můžete říct, co má zachovat; já to jednadvacetkrát z jednadvaceti neudělal."*
Pak `python compact_stats.py`, případně jeden konkrétní `compactMetadata` záznam a přečtení
`preTokens` → `postTokens` naživo (464 352 → 13 344) — *„to není moje interpretace, to si zapsal
Claude Code sám."*
**Priorita:** must
**Výhrada:** Nesmí to vyznít jako oprava decku — deck je věcně správný a publikum ho možná už
vidělo. Formulace musí být „a chybí tam dvě věty", ne „je to tam špatně". Druhá výhrada: formát
`.jsonl` je **interní a mezi verzemi se mění** (dokumentace před parsováním varuje), takže skript
funguje dnes; a 19 kompaktací je **podvýběr** z transkriptů na disku, ne úplný počet — obojí říct.

### F-04 — Padesát jedna ku jedné, tři minuty a 97 procent
**O čem to je:** Blok postavený na jednom poměru: `/compact` 51× proti `/clear` 1×. Teprve
ověřením se ukázalo, jak ostré to je: **`/clear` neposílá žádný request, je zdarma a okamžitý**;
`/compact` posílá sumarizační request přes celou historii — odtud medián **180,7 s**. Padesátkrát
jsem tedy zaplatil tři minuty čekání a ztrátu 97 % za operaci, kterou by při přepnutí na
nesouvisející úkol nahradilo něco za nula sekund. Není to nepořádnost — je to tím, že `/compact`
si člověk pamatuje (nástroj ho nabízí jako řešení plného kontextu), zatímco `/clear` musí znát.
A důležitá korekce vlastní diagnózy: **0 z 19 kompaktací bylo automatických** — vždycky jsem
sáhl sám, při mediánu 583 tisíc tokenů, tedy na ~58 % okna. Problém není že kompaktuju, ale
**kdy** a **bez instrukce**.
**Doklad:** `/clear` **1×** proti `/compact` **51×** (pracovní projekty). `/clear` zdarma,
neposílá request (dokumentováno) vs. medián `/compact` 180,7 s, nejdelší 224,1 s (změřeno).
21/21 manual, medián 464 352 tokenů před zásahem, auto-kompaktace by přišla až kolem 967K
(dokumentováno pro Sonnet 5). Doplňkově `/effort` 4× proti `/model` 53× (1 : 13) — třináctkrát
častěji jsem přepínal, **kdo** myslí, než **jak hluboko**, a přitom přepnutí modelu zahazuje
cache, zatímco effort ne.
**Role:** [příběh] + [výklad]
**Náročnost pro publikum:** nízká
**Odhad:** 7 min
**Závislosti:** F-03 (bez „shrnutí bez instrukce hádá" je poměr 1 : 51 jen kuriozita)
**Co ukážu na obrazovce:** Tři čísla na prázdném slidu, nic jiného: **51 : 1** — **180,7 s** —
**97,3 %**. Pak: *„Ne proto, že bych byl nepořádný — proto, že jsem znal jen jednu z těch dvou
možností. Vy dnes odcházíte s oběma."* Pak pět pák jako seznam a u čtvrté citace z našeho
vlastního `CLAUDE.md`: *„nikdy nenačítat celý"*, *„ve velkých souborech grepuj"* — doklad, že
tuhle disciplínu už máme v pravidlech, protože bolela. U páté páky ukázat dokumentovaný
`SessionStart` hook s `matcher: "compact"`.
**Priorita:** must
**Výhrada:** Nejosobnější blok prezentace — přiznání chyby. Funguje jen podán bez sebemrskačství,
jako diagnóza systému („nástroj mi nabízel jen jednu z těch dvou možností"), ne jako zpověď.
Pokud si na ten tón netroufám, patří to jako dvouminutový přílepek do F-03. A hook z páky 5
je **netestováno** — nesmí být prezentován jako vyzkoušená praxe.

### F-05 — Co tě stojí místo, o kterém nevíš
**O čem to je:** Anatomie kontextového okna položka po položce, se třemi překvapeními, která
slide 05 decku nemá: **(a)** startovní režie ~13–20 tisíc tokenů, **než napíšu první slovo**;
**(b)** popisky skillů — v cachovaném prefixu (0,1× cena), **ale místo v okně zabírají plnou
cenu**, i u skillů, které dnes nevyvolám; **(c)** výstupy nástrojů obvykle vyhrají nad
konverzací. Uzavírá to živé srovnání dvou cest ke stejné odpovědi: přečtu si to sám vs. nechám
subagenta. Kritérium: **odpověď krátká, cesta dlouhá.**
**Doklad:** Změřená startovní režie alzask: `CLAUDE.md` 23 427 + `MEMORY.md` 13 426 + output
style 1 985 = **38 838 znaků, odhadem ~12 946 tokenů** — plus systémový prompt (~4 200
ilustrativně) a popisky skillů (~450 ilustrativně, u mě ~50 skillů v listingu). Proti tomu můj
medián promptu ~20 tokenů = režie je **řádově 600–1000× větší než to, co píšu**. Subagent:
odhadem 50–80 tis. tokenů průzkumu → 300–500 tokenů závěru = redukce o dva řády. A přiznání
od harness: nástroje jsou **deferred**, schéma se dotahuje na vyžádání — na tenhle strop narazili
i ti, kdo nástroj staví.
**Role:** [demo] + [cvičení]
**Náročnost pro publikum:** střední
**Odhad:** 12 min (8 demo + 4 cvičení)
**Závislosti:** F-04 (subagent je první z těch pěti pák); slide 05 decku
**Co ukážu na obrazovce:** Slide 05, pak `/context` proti němu (*„ten samý obrázek, jen naměřený —
a jsou v něm dvě položky, které na slidu nejsou"*), publikum hádá, kdo vyhrává; pak řádek
s popisky skillů a otázka *„kolik z těch padesáti jsem dnes použil?"*. Pak hlavní demo: čerstvá
session, otázka s krátkou odpovědí a dlouhou cestou. `/context` → číslo na tabuli. Cesta A
(velké soubory rovnou) → `/context` → **skok**. `/clear` (*„zdarma a okamžité"*). Cesta B
(subagentem) → `/context` → **skoro se nepohnul**. Tři čísla vedle sebe.
Cvičení: každý si na vlastním projektu pustí `/context`, najde největší položku a nahlas řekne,
čím ji nahradí.
**Priorita:** must
**Výhrada:** Jediné demo, které může na živo selhat (subagent nemusí uspět, skok nemusí být
vidět) — **vyzkoušet předem a mít čísla z předběžného běhu jako záložní plán.** Druhá výhrada:
přepočet znaků na tokeny u startovní režie je **odhad při 3,0 znaku/token pro češtinu, což není
dokumentovaná hodnota** — musí být na slidu označeno jako odhad, jinak jeden dotaz z publika
podkope celý blok. Přesná čísla dá jedině `/context` na daném stroji.

---

## Stav bodů `[K OVĚŘENÍ]`

### Padly (uzavřeno ověřením 2026-08-26)

| # | Bod | Výsledek |
|---|---|---|
| 1 | Jak `/compact` vybírá, co zachová; lze to ovlivnit? | **Ano — `/compact <instrukce>`.** Bez ní hádá. Překlopilo F-03. |
| 2 | Práh auto-kompaktace | Není jedno %. Sonnet 5 ~967K, konfigurovatelné (`/autocompact`, `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, 100K–1M). Moje data: 0 z 21 auto. |
| 3 | Existuje veřejný tokenizér pro Claude bez klíče? | **Ne** (negativní nález). `count_tokens` API je jediná cesta a vyžaduje auth. |
| 4 | Poměr znaků/token pro angličtinu — 3,5 nebo 4? | **4** (doslovná citace z FAQ). Deck má na ř. 311 chybu. |
| 5 | Co `/resume` obnovuje a co ne | Detailně dokumentováno. Neobnovuje **cache** ani **background/monitor úlohy**. |
| 6 | Resetuje `/clear` cache na serveru? | Nic neresetuje — začne novou konverzaci, stará cache vyprší po TTL. **Klíčové: `/clear` neposílá žádný request → je zdarma.** |
| 7 | Velikost systémového promptu Claude Code | ~4 200 tokenů **ilustrativně** (ne garantovaná konstanta). Přesně jen `/context`. |
| 8 | Popisky skillů — každý request, nebo cachovaný prefix? | **Cachovaný prefix (0,1×), ale místo v okně zabírají pořád.** Bonus: po `/compact` se **nenačtou znovu**. |
| 9 | Je `opus[1m]` v Claude Code skutečně 1M? | **Ano, 1 000 000 vstupních tokenů**, výchozí, **bez cenového příplatku** nad 200K. |
| 10 | Jak je hranice kompaktace značená v `.jsonl`? | Nedohledáno v dokumentaci, ale **ověřeno vlastním měřením**: `isCompactSummary: true` + `compactMetadata` + `system/compact_boundary`. Formát je interní a mezi verzemi se mění. |

### Zůstávají otevřené

| # | Bod | Dopad |
|---|---|---|
| A | **Přesné počty tokenů** pro naše CZ/EN věty, `PICK_STATION_A2_LOAD`, cestu, `příjmu`/`prijmu`, paradigma „nosiče" a `C:\Git\alzask\CLAUDE.md` — přes `count_tokens` s `claude-opus-5`. | **Blokuje demo 2b** (F-02). Na stroji není API klíč ani `ant` CLI (změřeno). Úkol na přípravu, ne na živo. Bez toho musí F-02 skončit u měřených znaků. |
| B | **Poměr znaků/token pro češtinu** — jakákoli dokumentovaná hodnota. | Ověřeno, že Anthropic **nezveřejňuje** (negativní nález). Můj přepočet 3,0 znaku/token je **předpoklad** — musí být takto označen ve F-02 i F-05. Uzavře se jedině měřením přes bod A. |
| C | Zda **Sonnet 5** sdílí „nový" tokenizér s Opus 5. | Nízký dopad na výklad — dokumentace jmenuje jen „4.7 a novější + Mythos Preview", Sonnet 5 nepotvrzen ani vyvrácen. Zmínit jen kdyby se někdo ptal. |
| D | Chování **`SessionStart` hooku s `matcher: "compact"`** v praxi. | Dokumentováno včetně příkladu, ale **netestováno**. Ve F-04 musí být uvedeno jako „netestováno", ne jako vyzkoušená praxe. |
| E | Přesná velikost **popisků skillů v mé session** (~50 skillů). | Ilustrativní hodnota z dokumentace je ~450 tokenů; můj listing je zjevně větší. Přesně dá jedině `/context` — a to je zároveň demo 3a, takže se to uzavře na místě. |
