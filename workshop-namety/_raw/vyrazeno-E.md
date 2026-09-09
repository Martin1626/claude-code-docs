---

## E. Doložení brány „nic nezapsáno do repozitářů"

Zadání této inventury mělo jedinou povolenou zápisovou zónu — `C:\tmp\workshop-namety\`.
Na konci běhu ale **`shared` má pět necommitnutých změn** a `alzask` je měl v průběhu
patnáct. Protože je to přesně ta situace, ve které se nemá věřit tvrzení bez dokladu,
je tady rozbor.

**Výsledek:** ani jednu z těch změn nezpůsobila tato session ani žádný z jejích třinácti
agentů.

**Doklad je časový a tematický.** Během tohoto běhu pracoval tentýž člověk v **pěti
paralelních session**:

| Session | Repozitář | Co v ní dělal |
|---|---|---|
| `87fe6ffd` | alzask | **tato inventura** |
| `d651a725` | alzask | automatizace opravy zmizelých kotev ontologie |
| `2ead8bd4` | alzask | příprava e-mailu dodavateli |
| `be023ba3` | alzask | ladění stylu odpovědí |
| `5edcb929` | **shared** | propsání té automatizace kotev do šablony pluginu |

Změny v `alzask` (kotvy, `RULE-ONT-003`, `ADR-ASK-PROC-020`, nový příkaz) odpovídají
promptu ze session `d651a725` z 8:44 a byly změněné mezi 8:58 a 9:14. Do konce běhu je
ta session commitla, takže `alzask` je teď čistý.

Změny v `shared` mají doslovnou předehru: v **9:31** padlo v session `d651a725`
*„Napiš prompt, který provede i v pluginu ontology-registry. Já jej pak spustím sám."*
a v **9:48** se v session `5edcb929` objevilo *„Přečti
`C:/tmp/prompt-ontology-registry-kotvy.md` a proveď to."* Soubory jsou změněné 9:51–9:56.

**Proč to nemohla být tato session:**

1. Žádný ze třinácti agentů nedostal v zadání ontologii kotev, `ADR-ASK-PROC-020`
   ani cokoli z `ontology-registry`.
2. Všech třináct mělo v zadání explicitní zákaz zápisu do repozitářů a všichni ho
   v souhrnu potvrdili. `fhb` a `myfaber` zůstaly čisté po celou dobu.
3. Poslední agent (adversariální průchod) dokončil dřív, než ty soubory vznikly.
4. Harness sám během běhu ohlásil přírůstek dostupného příkazu a změnu `CLAUDE.md` —
   tedy změny vzniklé **vně** této session.

**A je z toho námět.** Pět paralelních session v jednom pracovním prostoru se nesrazilo —
ale jen proto, že každá psala jinam. Nikdo to nekoordinoval. Otázka **„jak poznáš, že si
dvě tvoje session sahají na týž soubor?"** nemá v mých datech odpověď; vidím to teprve
v `git status`, tedy pozdě. Je to přiznaná mezera (sekce C3) a zároveň nejlepší doklad,
jak se to dá zaměnit: kdybych se spolehl jen na `git status` na konci, vyvodil bych
z něj, že jsem porušil zadání.
