---
plaud_id: 5840853786e5da3f95dd85f4087bd708
title: 09-02 Alza: Úvod do využívání LLM a nástrojů „Cloud Code“ pro analytiky
created_at: 2026-09-02T15:32:14+00:00
language: auto
speakers: 1
project: Alza
classification_source: name
---

## Summary

> Datum a čas: 2026-09-02 17:32:14
> Místo: [Vložit místo]
> Lektor: Martin Tomis
## Shrnutí
Záznam popisuje přípravu dvouhodinového úvodního školení pro analytiky o využívání AI a nástrojů typu „Cloud Code“/„code“. Cílem je od základů vysvětlit fungování jazykových modelů (bezstavovost, kontextové okno, tokeny, tokenizace), nástrojový „harness“ pro interakci s okolním světem (čtení/zápis souborů, internetové vyhledávání, CLI, skenování obrazovky), pojmy jako sessions a turns, a principy účtování tokenů včetně cache. Další tematický blok se zaměří na poskytování dat modelu, strukturu projektového adresáře (instrukce, settings, code soubory), práci s velkými soubory a výběr relevantního kontextu, zavedení ontologie prvků systému (fyzické/logické prvky, popisy, vazby, citace, pravidla priority zdrojů), a prostor pro dotazy a sdílení zkušeností. Následné části školení budou prakticky orientované na strukturování informací pro tvorbu softwarových specifikací a analýz, včetně doporučených formátů (např. Markdown) a přizpůsobení projektové struktury. Datum konání shrnutí je stanoveno k 2026-09-02.
## Vědomostní body
### 1. Základy fungování jazykových modelů
- Bezstavovost jazykového modelu
  - Model si neukládá trvalý stav mezi nezávislými sezeními; každý nový dotaz/sezení začíná prakticky znovu bez vnitřní paměti předchozí konverzace.
  - Historie konverzace je udržována externě jako text (či tokeny) připojované na konec; uživatel přidává své dotazy/příkazy, model přidává odpovědi, čímž se postupně plní kontextové okno.
- Kontextové okno
  - Kontextové okno je sekvence tokenů reprezentující aktuální konverzační historii a vstupy; model při generování vždy znovu čte tuto sekvenci.
  - Postupné doplňování dotazů a odpovědí kontextové okno zaplňuje; práce s velkými kontexty má vliv na náklady i konzistenci výstupů.
- Tokeny a tokenizace
  - Model nezpracovává slova nebo písmena, ale tokeny (číselné reprezentace segmentů textu).
  - Vstup do modelu je řada čísel (tokenů) a stejné platí pro výstup; po generování se numerické výstupy převádějí zpět na text.
  - Plánovaná ukázka tokenizace ilustruje rozpad textu na tokeny a dopad na délku vstupu a cenu.
- Postprocessing výstupu a „harness“
  - Nad výstupem modelu existuje „harness“ – sada nástrojů, které dávají modelu „ruce“ pro interakci s okolním světem.
  - Příklady nástrojů: čtení souborů z lokálních či cloudových úložišť, vyhledávání na internetu, zapisování a vytváření souborů, spouštění příkazů z příkazové řádky, skenování obrazovky.
  - Harness zajišťuje provádění úkolů, které model textově navrhuje, takže práce s agentem není jen chat, ale i tvorba artefaktů (dokumentů, souborů), jež mohou sloužit jako vstup do dalších sezení.
- Pojmy „sessions“ a „turns“
  - „Session“ označuje celé sezení (konverzační relaci) s agentem; „turn“ je jednotlivý výměnný krok (uživatelův vstup a modelova odpověď).
  - Pochopení těchto pojmů pomáhá správně strukturovat interakci, historii a řídit kontext.
### 2. Náklady, účtování tokenů a cache
- Účtování za příchozí a odchozí tokeny
  - Náklady jsou odděleně účtovány za vstupní (příchozí) tokeny a výstupní (odchozí) tokeny; ceny se mohou lišit pro každý směr.
  - Plná cena se hradí za nově přidané tokeny ve vstupu a za tokeny, které model vygeneruje na výstupu.
- Cache kontextu
  - Tokeny, které jsou již v kontextovém okně a jsou uložené v cache, lze v dalším navazujícím dotazu znovu využít s nižší cenou (uváděna přibližně desetinová cena).
  - Využití cache vyžaduje zaplatit vyšší cenu při zápisu tokenů do cache, ale následně snižuje náklady za opakované předávání stejného kontextu.
  - Praktické dopady: optimalizace nákladů pro dlouhé a postupně doplňované konverzace; důležitá je strategie, co ukládat do cache.
### 3. Poskytování dat modelu a struktura projektu
- Jaká data poskytovat modelu
  - Model by neměl „vymýšlet“ chybějící kontext; je vhodné dodat co nejlepší podpůrné informace k úkolu.
  - Předání relevantních dat zvyšuje kvalitu výsledků a snižuje halucinace; kontext má být přesný, přiměřený a dobře strukturovaný.
- Struktura projektového adresáře
  - Jasná organizace souborů: kde jsou instrukce, co je v „code“ souborech, co v „settings“ souborech; cílem je poskytnout agentovi srozumitelnou orientaci.
  - Hlavní orientace „kde co je“ pomáhá nástrojům typu „Cloud Code“ efektivně najít správné části projektu.
- Práce s velkými soubory
  - Agent nečte vždy celé soubory, aby nezaplnil kontextové okno; místo toho čte začátky nebo relevantní části nalezené fulltextovým vyhledáváním.
  - Pokud je potřeba, načítá zbytek postupně; to může vést k tomu, že se při různých bězích načtou jiné části kontextu a výsledky se liší.
  - Je vhodné vysvětlit, jak „code“ primárně vybírá soubory do kontextu a jak tomuto procesu napomoci lepší strukturou a metadaty.
### 4. Ontologie prvků systému a řízení zdrojů pravdy
- Zavedení ontologie
  - Ontologie je rejstřík všech prvků v projektu (fyzické i logické), jejich popisů, vazeb a vztahů; slouží k systematickému zarámování domény.
  - Uvádí se odkazy na citace a zdroje, ze kterých informace pocházejí; pomáhá dohledatelnosti a auditovatelnosti.
- Priority a rozpory ve zdrojích
  - Při rozporech je nutné definovat, kterým dokumentům se dává přednost (pravidla precedence).
  - Jasná pravidla pro „zdroj pravdy“ zvyšují konzistenci výstupů modelu i týmu.
- Praktické příklady
  - Doporučeno uvést konkrétní příklady vhodné k vysvětlení ontologie a jejího využití v projektu.
  - Téma je natolik rozsáhlé, že může vyplnit celé první sezení při doplnění o ukázky.
### 5. Interakce, sdílení a navazující části školení
- Prostor pro dotazy a sdílení
  - Účastníci mají mít prostor k dotazům a sdílení vlastních zkušeností; to podpoří pochopení a propojení teorie s praxí.
- Navazující části školení
  - Budou zaměřeny na strukturování informací pro tvorbu softwarových specifikací a analýz.
  - Vhodné formáty (např. Markdown) je dobré používat od začátku; celá struktura projektu má být těmto formátům přizpůsobena, včetně pracovních postupů s nimi.
## Otázky
- [Vložit otázku/nejasnost]
## Úkoly
- [ ] 1. Připravit podrobný program dvouhodinového úvodního školení pro analytiky, včetně časového rozvrhu bloků (LM základy, tokenizace, harness, účtování a cache, struktura projektu, práce s velkými soubory, ontologie, Q&A).
- [ ] 2. Připravit ukázky tokenizace na reálných textech a vizualizace průběhu plnění kontextového okna.
- [ ] 3. Sestavit seznam a demonstrace nástrojů v „harnessu“ (čtení/zápis souborů, internetové vyhledávání, CLI, skenování obrazovky) a doplnit další relevantní příklady.
- [ ] 4. Vytvořit doporučenou strukturu projektového adresáře s příklady „instructions“, „code“ a „settings“ souborů a pokyny k orientaci.
- [ ] 5. Připravit vysvětlení strategie práce s velkými soubory (fulltext, výběr úryvků, postupné načítání) a ukázat, jak minimalizovat variabilitu kontextu.
- [ ] 6. Navrhnout základ ontologie prvků systému (seznam fyzických/logických prvků, popisy, vztahy, citace zdrojů) a pravidla precedence při rozporech.
- [ ] 7. Připravit praktické příklady a případové studie k ontologii a ke strukturování kontextu pro „Cloud Code“.
- [ ] 8. Zahrnout Q&A segment a facilitované sdílení zkušeností účastníků do závěru sezení.
- [ ] 9. Pro navazující školení připravit materiály o strukturování informací pro softwarové specifikace a analýzy, s důrazem na Markdown a přizpůsobení projektové struktury.

## Outline

- **00:01** Příprava školení AI
- **00:23** Cílová skupina analytici
- **00:31** Základy fungování LLM
- **00:55** Plán první části
- **01:30** Bezstavovost a kontext
- **02:09** Kontextové okno a tokeny
- **02:45** Tokeny a výstupní vrstvy
- **03:25** Nástroje kolem modelu
- **03:37** Příklady nástrojů a harness
- **04:10** Agent jako tvůrce artefaktů
- **04:53** Sessions, turns a účtování
- **05:51** Cache a náklady tokenů
- **06:19** Shrnutí: stroj, čísla, nástroje
- **06:50** Provádění úkolů nástroji
- **07:12** Jaká data poskytnout LLM
- **07:49** Struktura projektu a soubory
- **09:13** Práce s velkými soubory
- **09:51** Proměnlivý kontext a výsledky
- **10:21** Pomoc modelu a ontologie
- **10:58** Typy prvků a priority zdrojů
- **11:30** Rozsah prvního sezení
- **11:57** Prostor pro dotazy
- **12:36** Další části: formáty a struktura

## Transcript

**Martin Tomis** [00:01]
Předtím si vidím, že mám takovou přípravu pro školení, které mám vést a na kterém mám školit využívání AI, cloud pod, píše se to česky cloud, code. To školení je určeno pro analytiky. A vlastně chtěl bych začít od samotných základů toho, co je skutečně důležité pochopit, jak jazykové modely fungují, aby je potom byl schopen člověk správně používat při jakékoliv práci. Takže přemýšlím, co všechno bych měl zařadit. Nadto první části, to znamená ta, která bude trvat zhruba dvě hodiny a chtěl bych tam mluvit o tom, že jazykový model je bezstavový, že si vlastně neukládá žádné informace a každý nové sezení. Nebo respektive nový dotaz začíná téměř znovu. Co znamená, že se mu předávají, nebo že jazykový model si čte znovu a znovu stejná data A tím vzniká, nebo zapisuje ty odpovědi na konec svoje. Já tam připisuju zase své dotazy nebo příkazy a takhle se to opakuje a tím se postupně plní kontextové okno toho modelu. Takže to je jeden z témat, vysvětlení jak funguje kontextové okno. No a chtěl bych k tomu přidat... Možná je dobré vědět, že v tom kontextovém okně se nezpracovávají slova nebo písmena, Ale zpracovávají se tokeny, takže chtěl bych udělat ukázku poté, jak probíhá tokenizace, Jak takové tokeny vypadají, ať si člověk potom dokáže představit, Co vlastně je na vstupu toho jazykového modelu, že to je řada čísel. A stejně tak je to jen na tom výstupu. A asi by bylo potom dobré říct, co se děje s tím výstupem. To znamená, že je tam nějaký harness, který dává tomu jazykovému modelu v úvozovkách ruce. To znamená, jsou to nástroje, které mu pomáhají interagovat s tím okolním světem, Jako je například čtení souborů z nějakých úložišť lokálního nebo cloudového, Vyhledávání na internetu, zapisování, vytváření souborů. Nebo třeba spouštění příkazů z příkazové řádky, nebo skenování obrazovky a tak dále. Bylo by dobré tam uvést další příklady, nebo aby si mi tam potom doplnil další příklady, co všechno ten harness tvoří. Takže díky tomu by měli lidé pochopit, že... Komunikace s agentem není jenom o tom si jako chatovat, ale v podstatě vytvářet nové artefakty, nové dokumenty a ty potom můžou sloužit opět jako vstup pro další sezení nebo další dotazy. Asi bylo dobré vysvětlit pojmy, jako jsou sessions a turns a podobné další často používané pojmy. A ještě mám na mysli pořád to, jak se počítá cena těch tokenů, to znamená, jak je to účtováno, Že se za nějakou cenu účtují příchozí, za nějakou odchozí tokeny. A že vlastně to kontextové okno, které je tam uloženo na serveru a on si ho pamatuje, tak že je možné ty tokeny uložit do nějaké mezipaměti, do nějaké cache a v dalším navazujícím dotazu vlastně nemusím platit plnou cenu za všechny. Za celé to kontextové okno, které tam předávám, ale plnou cenu platím jenom za ty nově přidané tokeny a za ty tokeny, které tam jazykový model přidal, ale ty, které tam už byly dříve, tak pokud jsou uložené v cache, tak za ní se platí cirka desetinová cena, pokud vím, ale musím zase zaplatit vyšší cenu při zápisu do té cache. Takže to bych chtěl trošičku jako vysvětlit, rozvést, aby lidé pochopili, že je to nějaký stroj, nebo automat, který na jedné straně, do kterého vstupují čísla, na druhé straně ta čísla zase vystupují, jsou převáděny na text a nástroje, které jsou potom kolem toho jazykového modelu, jako je třeba ten Cloud Code. Zajišťují spouštění těch příkazů, respektive provádění úkolů, které ten jazykový model generuje, že by bylo dobré provést. Další téma potom bude o tom, jaká data poskytovat tomu jazykovému modelu. Aby si ji nemusel vymýšlet, ale měl co nejlepší kontext o tom, co má udělat, nebo k tomu, co má udělat. A k tomu bych chtěl zmínit strukturu projektového adresáře, to znamená, jak je rozložit. Kde mít a jak rozložené instrukce, to znamená, co může člověk hledat v code souboru, co je v nějakých settings, souborech, takovou tu hlavní orientaci, kde co je. Hm. Jo, co je dobré zmínit určitě, tak to je to, jak on pracuje s velkými soubory. To znamená, že on si nečte všechny soubory celé, tím by si zaplnil to kontextové okno. Takže on si přečte třeba jenom začátek toho souboru nebo nějaké části toho souboru podle toho, co nějakým fulltextovým vyhledáváním najde uvnitř. Toho souboru a to si načte do kontextového okna a pokud potřebuje, tak si potom načíta zbytek. Ale tím se může stát, že si pokaždé načte trošičku jiný kontext, načte si jiné soubory, A tím pádem dávají z tohoto důvodu jiné výsledky. Takže to bych chtěl tam trošičku jako rozvést, jak si code, code hlavně teda, Protože o něm to hlavně bude. Jak si ty soubory primárně vybírá a načítá do kontextového okna? No, protože budu to směřovat k tomu, jak mu v tom pomoct, Aby si ten kontext vlastně plnil co nejlépe. Jednou z těch věcí je zavedení ontologie prvků systému, To znamená ten rejstřík toho, co všechno, s čím se... V tom projektu třeba pracuje a jaké ty prvky mají mezi sebou vazby, vztahy a uvést tam nějaké konkrétní příklady, které se k tomu dobře hodí. To znamená, že jsou nějaké fyzické prvky, logické prvky, že existuje k ním nějaký popis a vazby a odkazy na citace, kde se... Vlastně ty hlavní informace o těchto prvcích tvrdí, Ze kterých zdrojů to vzniklo. A pokud tam jsou nějaké rozpory, Tak čemu se bude dávat přednost k informacím ze kterých dokumentů. To si myslím, že je hodně důležité a chtělo by to rozvést. Trošku mám pocit, že toto už je téma na celé první sezení, Pokud se to doplní vhodnými příklady a ukázkami možná. A pak bych chtěl, aby lidé měli prostor pro dotazy a sdílení vlastních zkušeností. Takže toto jsou myšlenky, s kterými do toho zatím... Vstupuju a potřeboval bych, abys je rozvedl a na základě nich mi připravil program tohoto zhruba dvouhodinového úvodního školení s tím, že další části toho školení budou už konkrétně o tom, jak... Strukturovat informace k tomu, abychom je dokázali využívat při tvorbě softwarových specifikací a analýz. Možná je třeba říct právě ty vhodné formáty, markdown a podobně, které jsou nejvhodnější od začátku používat a celé. Celou strukturu toho projektu tomu přizpůsobit, jak s tím pracovat.
