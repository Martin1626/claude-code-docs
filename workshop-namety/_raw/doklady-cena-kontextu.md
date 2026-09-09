# Co zabira misto v kontextu, nez vubec zacnu psat

Merene znaky jsou presne (velikost textu souboru). Prepocet na tokeny je **ODHAD**
pri konzervativnim poměru 3,0 znaku na token pro cesky text — presny tokenizer
Anthropic pro cestinu nezverejnuje, takze cislo ber jako radovou orientaci, ne fakturu.

| Co | Souboru | Znaku | Tokenu (odhad) |
|---|---|---|---|
| CLAUDE.md projektu alzask | 1 | 23 818 | ~7 939 |
| CLAUDE.md podadresaru alzask | 5 | 36 604 | ~12 201 |
| pravidla shared alzask | 15 | 34 840 | ~11 613 |
| pravidla shared fhb | 13 | 25 581 | ~8 527 |
| pamet alzask (MEMORY.md) | 1 | 13 426 | ~4 475 |
| pamet alzask (vsechny soubory) | 27 | 60 836 | ~20 278 |
| knowledge-inbox alzask martint | 18 | 127 067 | ~42 355 |
| skilly projektove alzask | 2 | 12 391 | ~4 130 |
| output style Feynman CZ | 1 | 3 998 | ~1 332 |

## Co se nacita automaticky pri kazdem startu session v alzask

| Zdroj | Znaku | Tokenu (odhad) |
|---|---|---|
| CLAUDE.md projektu alzask | 23 818 | ~7 939 |
| pamet alzask (MEMORY.md) | 13 426 | ~4 475 |
| output style Feynman CZ | 3 998 | ~1 332 |
| **Soucet** | **41 242** | **~13 747** |

K tomu se pridava systemovy prompt harness, definice vsech nastroju, metadata vsech
dostupnych skillu a obsah znalostniho inboxu za 14 dni (dodava SessionStart hook).
Ty tri cisla nejsou v souborech, ktere umim precist — jsou uvnitr harness.

## Proc na tom zalezi

Kazdy z tehle tokenu je v kontextu **pred prvnim mym slovem** a posila se znovu
s kazdym dalsim promptem v session. Neni to jednorazova investice — je to konstantni
rezie kazdeho tahu. Prompt cache ji zlevni, ale misto v okne zabira porad.
