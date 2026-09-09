# PROMPTY-SHARED

## 2026-07-05 01:10
/exit

## 2026-07-05 01:12
/model

## 2026-07-05 01:13
Reviduj agenty, zda jejich použití ve smyčce i jejich počet dává dobrý smysl při vytváření spec. Zároveň chci, aby při prvním použití na novém projektu nemusel mít uživatel v lokálním adresáři projekt FHB ani Alza.

## 2026-07-05 01:34
zapracuj nálezy 1, 2, 3

## 2026-07-05 01:39
/model

## 2026-07-05 01:41
V Spec Factory nepotřebuji nikde zmínku o projektech FHB ani Alza. Ani o změnách, které byly postupně do pluginu prováděné.

## 2026-07-05 07:53
/model

## 2026-07-05 07:54
V pravidlech mám "Stopa použití". Jak se toto v pluginu bude využívat?

## 2026-07-05 12:13
/context

## 2026-07-05 12:13
/compact

## 2026-07-05 12:14
V předchozích turnech jsem chtěl, abys přesně tyto a podobné věci odhalil a navrhnul způsoby opravy. Proč jsi to neudělal a jak bych musel zadat příště prompt, abys to správně udělal?

## 2026-07-05 12:14
/compact

## 2026-07-05 12:16
V předchozích turnech jsem chtěl, abys přesně tyto a podobné věci odhalil a navrhnul způsoby opravy.
  Proč jsi to neudělal a jak bych musel zadat příště prompt, abys to správně udělal?

## 2026-07-05 12:22
/model fable

## 2026-07-05 12:23
NApiš kompletní lepší prompt včetně smyčky "co dalšího je takhle".

## 2026-07-05 12:24
Nyní to podle tohoto promptu proveď.

## 2026-07-05 12:35
Postupně vyřeš 1 až 7

## 2026-07-05 13:16
Proveď kompletní audit pluginu spec-factory.

ROZSAH: celý plugin — agenti, orchestrátor (commands/spec.md), hooky, tools,
rules, templates, konfigurace (.claude-plugin, spec-schema.yaml, spec-dod.yaml).
Všechno v repu, ne jen to, co jsem vyjmenoval.

CO HLEDAT:
- mrtvé/osiřelé konstrukty: nic je nečte, nezapisuje, nevolá, nikam se nekopírují;
- rozpor mezi deklarací a realitou: dokument slibuje X, kód dělá Y; cesta míří
  na soubor nebo mechanismus, který neexistuje;
- neúplné řetězy: krok A předpokládá výstup kroku B, který nikde nevzniká;
- pozůstatky původního projektu, které v generickém pluginu nedávají smysl;
- cokoli dalšího, co „nedává smysl", i mimo tyhle kategorie.

SMYČKA „CO DALŠÍHO JE TAKHLE": u každého nálezu se před jeho uzavřením zeptej,
jestli stejný vzor není i jinde — a aktivně to prohledej (grep, křížové odkazy,
opačný směr závislosti). Opakuj kola, dokud kolo nepřinese žádný nový nález.
Nikdy se nezastavuj u prvního výskytu vzoru.

VÝSTUP: očíslovaný seznam nálezů, seřazený od nejzávažnějšího. U každého:
co to je (soubor:řádek), proč je to problém, návrh opravy — u nejednoznačných
2–3 varianty s doporučením a důvodem.

NEAPLIKUJ ŽÁDNOU OPRAVU. Jen nahlas a navrhni. Pokud jsi na problém narazil,
ale nevešel se do rozsahu nebo si nejsi jistý, jestli to problém je — stejně
ho uveď, označený jako „mimo rozsah / nejistý". O opravách rozhodnu já.

## 2026-07-05 21:35
/context

## 2026-07-05 21:38
Proveď postupně všechny opravy. Pokud je na výběr více variant, vyber to kvalitnější, dlouhodobější a spolehlivější řešení. Cílem je, aby skutečně byla respektována specifika každého projektu a dodržování pravidel bylo kontrolováno a vynucováno.

## 2026-07-06 18:45
/model

## 2026-07-06 18:48
Vytvoř prompt k prověření efektivity Spec Factory. Například zda rozdělení workflow do subagentů je vhodné, zda činnosti subagentů jsou vhodně definované, zda systém neobsahuje pozůstatky jiných funkcí. Zeptej se mě na další 10 věcí, které by bylo vhodné prověřit a já si vyberu, co chci do promptu zahrnout. Nic nemodifikuj.

## 2026-07-06 18:48
/model

## 2026-07-06 18:49
Vytvoř prompt k prověření efektivity Spec Factory. Například zda rozdělení workflow do subagentů je vhodné, zda činnosti subagentů jsou vhodně definované, zda systém neobsahuje pozůstatky jiných funkcí. Zeptej se mě na další 10 věcí, které by bylo vhodné prověřit a já si vyberu, co chci do promptu zahrnout. Nic nemodifikuj.

## 2026-07-06 18:56
/rename Prompt-prověření-3

## 2026-07-06 18:59
Prověření 3

## 2026-07-06 18:59
/model

## 2026-07-06 19:00
[Pasted text #1 +112 lines]

## 2026-07-06 19:06
Průzkum promptu prověření 4

## 2026-07-06 19:07
/model

## 2026-07-06 19:12
Napiš prompt, který následně spustím na https://www.alphaxiv.org/. Chci tam vyhledat studie, které pomohou vylepšit, zdokonalit, zefektivnit mou Spec Factory. Chci najít nejrelevantnější zdroje pro mé potřeby vytváření specifikací software. Nic neměň, prompt do chatu.

## 2026-07-06 19:28
/rename Prompt pro alphaxiv

## 2026-07-06 19:33
/compact

## 2026-07-06 19:34
/model

## 2026-07-06 19:38
Připrav plán všech smysluplných oprav a vylepšení. Zohledni při tom studie: C:\Temp\Studie-spec-factory

[Pasted text #1 +47 lines]

## 2026-07-06 19:39
/model

## 2026-07-06 19:39
Připrav plán všech smysluplných oprav a vylepšení. Zohledni při tom studie: C:\Temp\Studie-spec-factory

[Pasted text #1 +47 lines]

## 2026-07-06 20:28
[Image #1] Potřebuji, aby popis pluginu byl napsán více srozumitelněji pro lidi, kteří nejsou tak hluboko ponořeni do problematiky.

## 2026-07-06 20:54
/context

## 2026-07-06 20:54
/compact

## 2026-07-06 21:50
/model

## 2026-07-06 21:54
Spustil jsem plugin v C:\GitHub\HA-security\docs\spec\2026-07-06_faktorial. Chci zkontrolovat, zda plugin zafungoval správně, respektuje pravidla, funguje vynucování pravidel, jsou používány validační funkce ze správných zdrojů (cest) apod. Chci prozkoumat journal dané session. Připrav prompt pro takovouto kontrolu. Nedělej žádné změny, jen prompt.

## 2026-07-06 23:00
/model

## 2026-07-06 23:00
/context

## 2026-07-06 23:00
/compact

## 2026-07-07 07:14
Ověř session podle připraveného promptu.

## 2026-07-07 11:11
/context

## 2026-07-07 11:18
odchylka 1: rozšiř regex i na tabulku
odchylka 2: Je možné efektivně ošetřit pro Windows i MacOS?

## 2026-07-07 12:02
Potřebuji připravit plán adopce Spec Factory v projektu Alza.

## 2026-07-07 12:03
Potřebuji připravit plán adopce Spec Factory v projektu Alza.
@..\docs\ADOPTION-ALZA.md 
C:\Git\alzask

## 2026-07-07 12:22
/rename Adopce-SpecFactory-Alza

## 2026-07-07 17:40
Návrh obecných pravidel

## 2026-07-07 17:43
Návrh obecných pravidel
Která pravidla zachycená zde:
C:\Git\alzask\.claude\knowledge-inbox
C:\Git\alzask\.claude\rules\shared
C:\Git\fhb\.claude\rules\_personal
C:\Git\fhb\.claude\rules\shared

je vhodné zapracovat do C:\Git\shared\plugins\spec-factory\rules\shared?

## 2026-07-07 17:48
/model

## 2026-07-07 17:48
pokračuj

## 2026-07-07 19:02
/plugins

## 2026-07-07 19:03
/plan

## 2026-07-07 19:03
/plugins

## 2026-07-07 19:07
/model

## 2026-07-07 19:08
Nyní můžeš vymazat nahrazená pravidla v projektech Alza a FHB, přestože to není v tomto repu

## 2026-07-08 20:22
Proveď audit, že pravidla uložená v plugins\spec-factory\rules\shared jsou správně zohledňovaná

## 2026-07-08 20:22
Proveď audit, že pravidla uložená v plugins\spec-factory\rules\shared jsou správně zohledňovaná
Například v projektu C:\Git\alzask se v nové session zobrazuj:


## 2026-07-08 20:24
Proveď audit, že pravidla uložená v plugins\spec-factory\rules\shared jsou správně zohledňovaná
  Například v projektu C:\Git\alzask se v nové session zobrazuje:

[Image #1]

## 2026-07-08 21:15
Vysvětli srozumitelně, co by obnášela varianta A.

## 2026-07-08 21:28
OK, proveď variantu A. Zároveň zruš ze Spec Factory tato pravidla a jejich přenášení v rámci pluginu. Je to mimo doménovou oblast Spec Factory a nepatří to sem. Možná později uděláme jiný plugin. Stávající pravidla přenes do C:\Git\alzask a C:\Git\fhb

## 2026-07-08 22:34
Potřebuji znalosntí smyčku z projeků

## 2026-07-08 22:34
/model

## 2026-07-08 22:38
Potřebuji znalosntí smyčku z projeků
C:\Git\alzask
C:\Git\fhb
přepracovat tak, abych ji mohl sdílet napříč projekty, podobně jako SpecFactory.
Nová osobní pravidla chci ukládat rovnou do projektu do složky pojmenované daným uživatelem a ukládat je do Gitu. Díky tomu uvidím v Gitu nejen již odsouhlasená sdílená pravidla (shared), ale i nová osobní pravidla členů týmu. Pak se mohu rozhodnout, která pravidla povýším na shared.

## 2026-07-08 22:40
/plugins

## 2026-07-08 22:52
Pohlídej, aby se v nových sessions správně načítala nejen sdílená pravidla, ale i osobní pravidla a pravidla z osobního inboxu.

## 2026-07-09 08:24
Cizí pravidla se sice ukládají do Gitu, ale nesmí se nikdy načítat ostatním uživatelům.

## 2026-07-09 09:14
Provedl jsem instalaci.

A proč v marketplace vidím stále kvados-spec-factory?
[Image #1]

## 2026-07-09 09:21
/plugins

## 2026-07-09 09:42
/model

## 2026-07-09 09:43
Commity jsi provedl pod špatným uživatelem. Správně má být tomis@kvados.cz
Oprav, co ještě jde.

## 2026-07-09 09:56
Co mám nyní udělat před merge do main?
[Image #2]

## 2026-07-09 10:04
Asi jsem provedl špatně. Potřebuji asi ještě jednou.
[Image #3]

## 2026-07-09 10:36
push hotov

## 2026-07-09 13:28
Vytvoř prompt pro opravu FHB, který pak spustím v nové session v FHB repu.

## 2026-07-09 16:34
/model

## 2026-07-09 16:34
/compact

## 2026-07-09 16:37
/model

## 2026-07-09 16:39
Spustil jsem prompt v Session ID:       49d99d0b-ef92-48b3-aac1-cf6483cbccc6
Zkontroluj, zda implementace byla provedena správně.
Potom zkontroluj repo C:\Git\alzask a případně také připrav prompt, který v něm mám spustit.

## 2026-07-09 16:50
Kde je ten prompt uložený?

## 2026-07-09 16:51
Proč v Alzask není taky docs\spec-grounding?

## 2026-07-09 16:54
Rád bych to přesto sjednotil na spec-grounding. Doplň to do promptu.

## 2026-07-10 13:22
Otestuj, že pluginy jsou přístupní nově již i přes project token glpat-o-EKU93o1s1XLfHukxWfqG86MQp1OjRjCA.01.0y0lmdqo5

## 2026-07-10 13:41
Vyzkoušej tento token:
glpat-YKzzlZxsOQx1FIakOw_d6m86MQp1OjRkCA.01.0y0fyl0af

## 2026-07-10 13:52
Prověř ještě tento:
glpat-2LcGxFvePhidYs2eF8Y2CW86MQp1OjRlCA.01.0y0dsbbby

## 2026-07-10 14:03
Fungují tedy nyní všechny tři tokeny?

## 2026-07-10 14:06
Původní tokeny byly smazány. Vyzkoušej proto tento nový:
glpat-6pVHhXNMdoQrZnPf3DItTm86MQp1OjRmCA.01.0y1kzrnsv

## 2026-07-10 14:09
OK, oprav, ale necommituj. Potřebuji pak vyzkoušet reinstalaci pluginů z marketplace, který bude přístupný přes ten token.

## 2026-07-10 14:23
Marketplace chci nainstalovat z gitu nově. Napiš přesný postup.

## 2026-07-10 14:29
Provedl jsem commit té změny.

## 2026-07-10 14:33
/plugin marketplace remove kvados-plugins

## 2026-07-10 14:33
/plugins

## 2026-07-10 14:33
/plugin marketplace add https://gitlab01.st.kvados.cz/kvados/customers/shared.git

## 2026-07-10 14:34
/plugins

## 2026-07-10 14:35
/reload-plugins

## 2026-07-10 14:36
Ověř, že je všechno OK a mohu na repu C:\Git\alzask používat.

## 2026-07-10 14:38
Zkontroluj, zda jsou správné instrukce v plugins\README.md

## 2026-07-10 14:40
Oprav README i homepage, ale necommituj

## 2026-07-10 14:46
ADR může obsahovat TODO, pokud je ve stavu draft. Když je schváleno, tak nesmí. Oprav validace.

## 2026-07-10 14:47
ADR může obsahovat TODO, pokud je ve stavu draft. Když je schváleno, tak nesmí. Oprav validace.
viz projekt Alza:
[Pasted text #1 +13 lines]

## 2026-07-10 15:28
Napiš do backlogu, Přepsat prompty do angličtiny, protože šetří tokeny.

## 2026-07-10 20:11
Uprav dokumentaci, aby byla srozumitelná i pro méně zasvěcené lidi.

## 2026-07-10 20:15
Uprav dokumentaci, aby byla srozumitelná i pro méně zasvěcené lidi. Například nepoužívej:
Paměť je cross-session 
Rules jsou path-scoped
precedence vč. cizí-personal-informativní
Preflight
scaffoldne
skalár přepíše jádro
operacionalizuje
protichůdný enforcement
atd

## 2026-07-10 20:15
pokračuj

## 2026-07-10 20:37
Připrav atraktivní html prezentaci (dark mode), pomocí které tyto dva pluginy budu moci představit ostatním kolegům. Chci logické pořadí: v čem mi to pomůže, jak to funguje, jak to mám používat... Ulož do C:\Git\shared\plugins\docs

## 2026-07-10 20:50
Instalaci pluginů nechci v readme doporučovat alternativně z lokálního repa.

## 2026-07-10 20:51
PLuginy se netýkají jen FHB a Alza. Vůbec je nezmiňuj. V budoucnu to budou další projekty.

## 2026-07-10 20:56
Uprav styl podle nějakého oblíbeného popularizátora AI. Chci to mít méně formální a umělé, více přirozené a zajímavé. Nepřeháněj to se žargónem.

## 2026-07-10 22:05
Nebylo by v rámci spec-factory efektivnější, aby se nejprve provedl research a teprve po něm planner? A je vhodné používat workflow?

## 2026-07-10 22:06
/model

## 2026-07-10 22:06
Nebylo by v rámci spec-factory efektivnější, aby se nejprve provedl research a teprve po něm planner? A je vhodné používat workflow?

## 2026-07-10 22:12
Ano, navrhni znění outline-revision kroku

## 2026-07-10 22:14
Ano, zapiš to

## 2026-07-11 08:04
Vysvětlím jí princip instalace pluginů přes project  token . Zajímá mě například kde ten token je uložený . A když jsi parkin bude instalovat někdo jiný než já, tak zda si jej musí někde předem uložit nebo jak ten princip celý funguje.

## 2026-07-11 08:04
Vysvětli mi princip instalace pluginů přes project  token . Zajímá mě například kde ten token je uložený . A když jsi parkin bude instalovat někdo jiný než já, tak zda si jej musí někde předem uložit nebo jak ten princip celý funguje.

## 2026-07-11 08:12
Ještě tomu nerozumím. Stačí pro kolegu, když má přístup pro čtení do https://gitlab01.st.kvados.cz/kvados/customers/shared? Pak už může jen spustit instalaci?

## 2026-07-11 08:16
MY se přihlašujeme všichni přes kerberos. Jak to s tím souvisí?

## 2026-07-11 08:17
Když jsem totiž zprovozňoval instalaci pluginů přes project token, tak kolega, který spravuje gitlab mi vygeneroval nějaký token a ten jsem ti zadal, abys jej ověřil. Přitom přes kerberos jsem už přístup měl. Takže mě zajímá, zda bude muset správce takový token generovat i ostatním koelgům.

## 2026-07-11 08:22
Jak si mají kolegové vložit ten klíč do GITLAB_TOKEN?

## 2026-07-12 15:12
Prezentace

## 2026-07-12 15:17
Prezentace
Mým cílem je vytvořit přehlednou intuitivní prezentaci, jack funguje Claude Code. Nyní chce vytvořit jenom osnovu až si ji schválíme tak teprve budeš pokračovat dále. Chtěl bych začít nejdříve jako vysvětlit jak funguje samotný jazykový model to znamená že to je bez stavový automat který vlastně dostane na vstupu nějaký jako základní blok textu ve formě tokenů a vyplivne jako výstupní blok textu to znamená že kdybych podruhé mu dal na vstup stejný blok textu tak vlastně mi ji vyplivne podobný výsledek nebude to úplně stejné z těch důvodů které tam uveď jo vyhledej si v dokumentaci nebo ve známých zdrojích nebo v ověřených zdrojích to jak tyto jazykové modely fungují . Teď ti popisuji vlastně jenom takovou svou vizi jak by to mohlo jako vypadat ale chci aby si to doplnil podloženými a ověřenými znalostmi. Pokud mé doporučení s tím nesouvisí nebo jsou v rozporu tak mě na to upozorní . To znamená že když dostanu nebo když ten harness toho cloth kódu dostane ten výstupní text tak v něm třeba najde hmm nějaký script který má spustit a ten harness se o to postará spustí script no a vlastně na vstup toho jazykového modelu vloží tu samotnou odpověď kterou z jazykového modelu dostal+ ten script a výsledky toho skriptu no a jazykový model ví že tyto data nyní může zpracovat a poskytne zase nový výsledek jo ve kterém budou zase nové dokumenty nebo nové informace které už tvoří ten finální výstup nebo znova ten harnes rozpozná že je třeba je ještě dále nezpracovávat a způsob vlastně opakovat tuto smyčku. Doplň do tohoto popisu samozřejmě všechny nezbytné detaily jak to funguje které jsem nezmínil. Takže teďka udělají osnovu a pak se domluvíme co dále .

## 2026-07-12 15:31
S osnovou souhlasím. Ještě bys tam mohl doplnit princip a ukázky tokenizace textu.
A doplň vysvětlení, co se dělá při druhém a dalším turnu. Jak se kešují již dříve poslané tokeny, aby se za ně znovu neplatilo. A také to, co se děje při přetečení kontextového okna. Co by se stalo, kdyby nedošlo ke kompaktaci.

Technický šum nechci vysvětlovat podrobně, ale uvést jako zajímavost, jak můj dotaz ovlivňují současné cizí požadavky.
Publikum: smíšené.
Formát: HTML, dark mode, vyhledej atraktivní vizualizace, které jsou v tomto kontextu velice oceňované uživateli.

Nyní spusť researcher pro ověření chování přímo ve zdrojích Claude Code.

## 2026-07-12 16:02
Na slidu 2 bych rád měl nějaké jednoduché grafické schéma té funkce. Ten text v rámečku už je zahlcující. To grafické schéma by mohlo být animované, jak tokeny protékají modelem nebo něco podobného.
Když vstoupím na slide 10, tak chci mít všechny rámečky "rozsvícené", jako po přehrání, ať jsou hned lépe čitelné.
Jinak je to OK a můžeš vytvořit HTML do C:\Git\shared\docs\claude-code

## 2026-07-12 16:10
Na poslední slide doplň ještě také vhodný diagram vztahu modelu, harnessu a jak to pracuje.

## 2026-07-12 16:14
Třetí odrážka je špatně formátovaná.
[Image #1]

## 2026-07-13 13:24
/spec-factory:spec asdjkf lkdasj gljaslůkgj lkasjd gflksjdalfj lsdaj

## 2026-07-13 21:44
Simulace Fable

## 2026-07-13 21:44
/model

## 2026-07-13 21:47
Nosiče přijíždějí z pravé strany jsou odebírané z levé strany.
   Simulace musí umožnit z levé strany odebrat paletu , například kliknutím. Zároveň z pravé strany zase přidává novou paletu . To znamená v té vizualizaci z té poslední volné lokace vpravo se tam objeví paleta která je převzata na tu 10 lokaci dopravníku. Jo takle uživatel si bude moci zkoušet různé kombinace jak dopravníky a jednotlivé segmenty těch dopravníků se budou pohybovat když budem průběžně odebírat z levé strany palety a na pravé straně je zase vkládat ta simulace .
  Ta simulace musí fungovat v reálném čase, to znamená jak existuje nějaká doba po posunutí nosiče z jednoduchou segmentu dopravníku na 2, nějaká přiměřená doba , ale dopravníky se musí to určit průběžně, musí na sebe hodně navazovat. Cílem posunu tě nosičů je maximální zaplněnost toho dopravníku, aby tam nevznikaly žádné volné lokace . V přiloženém obrázku je ukázka, jak se budou nosiče zastavovat na segmentech dopravníků, kdy jíl je dopravník zaplněný do určité části jenom tečka obdobným způsobem to pak musí fungovat když jsou nosiče odebírány, tak zase se odeberou nosiče do té míry aby nevznikaly na dopravníku mezery . Promyslí dobře algoritmus kdy se který dopravník musí roztočit pokud jim něco nejasnýho tak jsem je na to zeptej předem. Cílem je možnost si vyzkoušet jak situace bude vypadat když vlastně budu vkládat palety na dopravník AA zase je odebírat . Takle asi potřebuju tam mít možnost nějakým kliknutím paletu volit znamená by přijela z pravé strany, jiným kliknutím zase paletu odebrat le jste posleprvní dní lokace planeta odjede .
[Image #2]

Ten algoritmus není vůbec jednoduchý. Je potřeba to pořádně promyslet a inspirovat se na
  internetu, jak se obvykle takové úlohy na dopravnících řeší.

## 2026-07-13 21:48
Nepracuj vůbec s adresářem C:\tmp a nenačítej z něj žádná data.

## 2026-07-13 22:13
A

## 2026-07-13 22:21
OK

## 2026-07-13 23:07
test

## 2026-07-13 23:08
/plugins

## 2026-08-19 21:28
Uprav

## 2026-08-19 21:29
a

## 2026-08-19 21:39
Přečti C:\tmp\review-spec-zadani.md a proveď ho celý

## 2026-08-19 21:49
/plugins

## 2026-08-19 22:00
Rozšiř description.
Dále připrav název a popis pro commit

## 2026-08-19 22:14
review-spec se mi v nové session nenabízí. Proč? Přitom mám verzi 1.8.0
[Image #1]

## 2026-08-20 14:48
Zjisti zpětnou vazbu k review-spec na základě Session ID:       dd923fb6-6ee5-4cda-82d9-63fc000d6ae7. Mají poslední úpravy v pluginu pozitivní dopad?

## 2026-08-20 15:03
aplikovat pravidlo :159 i na už přijaté nálezy před eskalací

## 2026-08-21 19:04
Mám dojem, že AI má tendenci produkovat více, než úlohy skutečně potřebují. Proveď proto posouzení, zda přístup YAGNI (You Aren't Gonna Need It) je vhodné více aplikovat do review-spec a spec. Můžeš přitom analyzovat nedávné sessions, kde se review-spec používalo.

## 2026-08-24 11:32
Přečti si celý a proveď C:\Git\alzask\docs\onboarding\PROMPT-plugin-ontology-registry.md

## 2026-08-24 12:14
napiš do chatu prompt, který mám spustit v repu Alzask.

## 2026-08-24 23:01
V souborech pro ontology-registry se objevuje datum 2026-08-24 nebo informace o aktuální kontrole registru. To se ale týká konkrétního projektu Alzask, ale tento plugin má být obecný pro jakýkoliv projekt.

## 2026-08-25 08:40
Co by znamenalo dorovnat Alzask ze šablony?

---
**Celkem promptů v souboru: 151**
