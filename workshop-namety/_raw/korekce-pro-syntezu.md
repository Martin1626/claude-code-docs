# Korekce a výhrady, které musí projít do finálních výstupů

Sesbírané v hlavní session z ověřování. Každá položka mění nebo omezuje nějaké tvrzení,
které by se jinak do katalogu dostalo v silnější podobě, než snese.

## 1. Dvě sady čísel — nezaměňovat

Statistiky z `history.jsonl` se liší podle toho, jestli měřím celou historii, nebo jen
projekty v rozsahu workshopu. Rozdíl není kosmetický.

| Metrika | Celá historie (2670+) | Pracovní projekty (1507+) |
|---|---|---|
| `/compact` | 67× | 51× |
| `/model` | 63× | 53× |
| `/context` | 42× | 37× |
| `/resume` | 58× | 33× |
| `/clear` | 6× | **1×** |
| medián délky promptu | 75 znaků | 65 znaků |
| max délka promptu | 22 386 | 7 213 |
| promptů nad 1000 znaků | 44 | 31 |

Zadání workshopu uvádělo první sadu. **Ve výstupu vždy napsat, o kterou jde.**

## 2. Existující deck má chybu, kterou je třeba opravit

`C:\Git\shared\docs\claude-code\claude-code-jak-funguje.html`, řádek 311, tvrdí
**≈ 3,5 znaku na token** pro angličtinu a odkazuje se na „dokumentaci Anthropic".

Dokumentovaná hodnota je **≈ 4 znaky na token** — doslovná citace z FAQ na
`platform.claude.com/docs/en/about-claude/pricing`: *„As a rough estimate, 1 token is
approximately 4 characters or 0.75 words in English."* Ověřeno 2026-08-26.

Deck je jinak dobrý a použitelný; tohle je jednořádková oprava, ne důvod ho zahodit.

## 3. Poměr pro češtinu Anthropic nezveřejňuje — a to se musí říct

Nikde není oficiální číslo znaků na token pro češtinu ani pro žádný jiný jazyk než
angličtinu. Dokumentace říká jen „přesný počet se liší podle jazyka".

Co se dá tvrdit poctivě: obecný princip byte-level BPE tokenizace („byte premium effect")
vysvětluje, **proč** text s diakritikou stojí víc tokenů — ASCII znak je jeden bajt,
znak s diakritikou vícebajtová UTF-8 sekvence, a slovník je natrénovaný převážně na
angličtině, takže časté anglické sekvence se slučují do velkých tokenů, zatímco
diakritika ne. Zdroj je nezávislý (arxiv), ne Anthropic.

**Formulace pro workshop:** „Tohle Anthropic píše černé na bílém (4 znaky/token pro
angličtinu). Tohle je obecně platný technický princip, který vysvětluje, proč čeština
stojí víc — ale číslo pro češtinu Anthropic nepublikuje."

Můj vlastní odhad 3,0 znaku/token pro český text (použitý v `doklady-cena-kontextu.md`)
je konzervativní odhad, ne měření. Označit jako odhad.

## 4. Výhrada k dokladu o kompaktaci

Čísla v `doklady-kompaktace.md` (19 kompaktací, medián 97,3 % zahozeno, medián 180,7 s)
jsem získal přímým parsováním `.jsonl` transkriptů. Dvě výhrady:

- **Dokumentace to výslovně nedoporučuje.** Formát záznamů je interní a mění se mezi
  verzemi; skript, který ho parsuje, se může rozbít s každým vydáním. Doporučená cesta
  jsou `/export`, `claude -p --output-format json` nebo pole `transcript_path`, které
  dostávají hooky. Čísla jsou platná pro tuto verzi, ne navždy.
- **21 je podvýběr, ne úplný počet.** Historie zná 175 sessions jen pro alzask, ale na
  disku je 84 souborů transkriptů. Skutečný počet kompaktací je vyšší (`/compact` 51×
  v pracovních projektech).

## 5. Systémový prompt a CLAUDE.md — ilustrativní vs. moje skutečnost

Dokumentace uvádí v simulaci kontextového okna **ilustrativní** hodnoty: systémový prompt
≈ 4 200 tokenů, projektové `CLAUDE.md` ≈ 1 800, metadata skillů ≈ 450, auto memory ≈ 680.
Explicitně označené jako ilustrativní, ne měřené konstanty.

Moje skutečnost je jiná: `C:\Git\alzask\CLAUDE.md` má 23 427 znaků, tedy odhadem
**~7 800 tokenů — přes čtyřnásobek ilustrativního příkladu**. K tomu `MEMORY.md` 13 426
znaků (~4 500 tokenů). To je použitelný doklad: „ilustrativní příklad v dokumentaci je
1 800 tokenů, můj reálný soubor má čtyřikrát víc."

Přesné číslo dá jen `/context` v živé session.

## 6. Netriviální fakt, který vysvětluje reálný problém

**Metadata skillů se po `/compact` nenačtou znovu.** Dokumentace: *„Unlike the rest of the
startup content, this listing is not re-injected after `/compact`. Only skills you actually
invoked get preserved."* Tedy po kompaktaci Claude nezná skilly, které do té doby nepoužil,
dokud nezačne nová session.

To je konkrétní, měřitelný důsledek kompaktace, který se dá předvést, a vysvětluje jeden
druh „po compactu je hloupější".

## 7. `/clear` je zdarma, `/compact` není

`/clear` neposílá žádný request — jen přestane odkazovat na starou historii; stará cache
vyprší sama po TTL. `/compact` naopak posílá sumarizační request, který musí přečíst celou
dosavadní konverzaci (proto medián 180,7 s).

Poměr v mých datech: `/compact` 51× proti `/clear` 1×. Používal jsem drahou operaci tam,
kde na přepnutí mezi nesouvisejícími úkoly stačila zdarma.

## 8. Fáze 1 nahlásila 0 hooků — ve skutečnosti 4

Viz `faze1-korekce-hooky.md`. Hooky nejsou jen v `settings.json`, ale i v pluginech
(`<plugin>/hooks/hooks.json`). Použité eventy: 2 z cca 8 (`SessionStart`, `PreToolUse`).

## 9. Fáze 2 běžela na 5 agentech, ne na 4

Zadání předpokládalo rozdělení alzask na dvě poloviny, ale `prompty-alzask-H2.md` měl
249,5 KB proti limitu 150 KB. Rozdělil jsem ho po měsících (06 = 40 KB, 07 = 77 KB,
08 = 132 KB), takže fáze 2 měla pět agentů: H1+06, 07, 08, fhb+myfaber, shared.
Původní `prompty-alzask-H2.md` zůstal na disku jako nepoužitý.

## 10. Existuje vestavěný `/insights`

Analyzuje posledních až 200 sessions na stroji a udělá HTML report o tom, na čem pracuju
a kde vázne komunikace. Tedy přesně ta inventura, kterou tady dělám ručně skripty
a dvanácti agenty. Do katalogu to patří i s tou ironií — a jako první věc, kterou si
kolega může spustit sám na svých datech, bez jakékoli infrastruktury.

## 11. Brána č. 6 (nic nezapsáno do repozitářů) — drží, ale vyžaduje vysvětlení

Na začátku běhu (08:42) byly `alzask`, `fhb`, `shared` i `myfaber` čisté. Na konci má
`alzask` 15 necommitnutých změn (ontologie kotev, `RULE-ONT-003`, `ADR-ASK-PROC-020`,
`/ontologie:kotvy`, `cite.py`, `reanchor.py`, `anchors.py`).

**Autorem není tato session ani žádný z jejích agentů.** Doklad je čtyřnásobný:

1. **Časová a tematická koherence s cizí session.** V `history.jsonl` je v 08:44 prompt
   ze session `d651a725`: „V pravidlu je napsáno, že zmizelé kotvy má opravovat člověk.
   To mi přijde neudržitelně náročné…" Změněné soubory jsou přesně ty, které tahle úloha
   mění — smazané `RULE-ONT-003_zmizela-resi-clovek.md`, nové
   `RULE-ONT-003_kotvy-tri-tridy.md`, nový příkaz. Časy modifikace 08:58–09:14.
2. **Zadání agentů.** Žádný ze třinácti agentů nedostal v zadání ontologii kotev,
   `ADR-ASK-PROC-020` ani cokoli z `.ontology-tools/`.
3. **Explicitní zákaz.** Všech třináct mělo v zadání větu „NIC nezapisuj do žádného
   repozitáře, jediná povolená zápisová zóna je `C:\tmp\workshop-namety\`" a všichni
   to v souhrnu potvrdili. `fhb`, `shared` i `myfaber` zůstaly čisté.
4. **Harness sám ohlásil přírůstek.** Během běhu přišla notifikace o novém dostupném
   skillu `ontologie:kotvy` a o změně `CLAUDE.md` — tedy o změně, která vznikla vně
   této session.

**A je to zároveň námět.** V jednom repozitáři běžely současně **čtyři session** téhož
člověka: tato (workshop), kotvy ontologie, příprava e-mailu dodavateli a ladění output
stylu. Každá psala jinam, takže se nesrazily — ale nikdo to nekoordinoval, drželo to
jen shodou náhod v rozdělení témat. Otázka pro workshop: **jak poznáš, že si dvě tvoje
session sahají na týž soubor?** Odpověď „podle git statusu, až bude pozdě" není dobrá.
