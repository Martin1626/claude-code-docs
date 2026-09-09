import os, glob, json

# Kolik stoji "nulovy" kontext: CLAUDE.md soubory, pravidla, skilly, pameti.
# Hrube: 1 token ~ 3,5 znaku pro EN; cestina je hustsi na tokeny, takze pouzijeme
# konzervativni 3,0 znaku/token pro cesky text a oznacime to jako ODHAD.

CZ_RATIO = 3.0
targets = [
    ('CLAUDE.md projektu alzask', ['C:/Git/alzask/CLAUDE.md']),
    ('CLAUDE.md podadresaru alzask', glob.glob('C:/Git/alzask/**/CLAUDE.md', recursive=True)),
    ('pravidla shared alzask', glob.glob('C:/Git/alzask/.claude/rules/shared/*.md')),
    ('pravidla shared fhb', glob.glob('C:/Git/fhb/.claude/rules/shared/*.md')),
    ('pamet alzask (MEMORY.md)', ['C:/Users/ai_martint/.claude/projects/C--Git-alzask/memory/MEMORY.md']),
    ('pamet alzask (vsechny soubory)', glob.glob('C:/Users/ai_martint/.claude/projects/C--Git-alzask/memory/*.md')),
    ('knowledge-inbox alzask martint', glob.glob('C:/Git/alzask/.claude/knowledge-inbox/martint/*.md')),
    ('skilly projektove alzask', glob.glob('C:/Git/alzask/.claude/skills/**/SKILL.md', recursive=True)),
    ('output style Feynman CZ', glob.glob('C:/Users/ai_martint/.claude/output-styles/*')),
]

rows = []
for label, paths in targets:
    paths = [p for p in paths if os.path.isfile(p)]
    ch = 0
    for p in paths:
        try:
            with open(p, encoding='utf-8', errors='replace') as f:
                ch += len(f.read())
        except Exception:
            pass
    rows.append((label, len(paths), ch, int(ch / CZ_RATIO)))

out = []
W = out.append
W('# Co zabira misto v kontextu, nez vubec zacnu psat')
W('')
W('Merene znaky jsou presne (velikost textu souboru). Prepocet na tokeny je **ODHAD**')
W('pri konzervativnim poměru 3,0 znaku na token pro cesky text — presny tokenizer')
W('Anthropic pro cestinu nezverejnuje, takze cislo ber jako radovou orientaci, ne fakturu.')
W('')
W('| Co | Souboru | Znaku | Tokenu (odhad) |')
W('|---|---|---|---|')
for label, n, ch, tk in rows:
    W('| ' + label + ' | ' + str(n) + ' | ' + '{:,}'.format(ch).replace(',', ' ') + ' | ~' + '{:,}'.format(tk).replace(',', ' ') + ' |')
W('')

# co se realne nacita do session pri startu v alzask:
# root CLAUDE.md (vzdy) + MEMORY.md (vzdy) + inbox za 14 dni (hook) + output style
auto = 0
auto_detail = []
for label, n, ch, tk in rows:
    if label in ('CLAUDE.md projektu alzask', 'pamet alzask (MEMORY.md)', 'output style Feynman CZ'):
        auto += ch
        auto_detail.append((label, ch))
W('## Co se nacita automaticky pri kazdem startu session v alzask')
W('')
W('| Zdroj | Znaku | Tokenu (odhad) |')
W('|---|---|---|')
for label, ch in auto_detail:
    W('| ' + label + ' | ' + '{:,}'.format(ch).replace(',', ' ') + ' | ~' + '{:,}'.format(int(ch / CZ_RATIO)).replace(',', ' ') + ' |')
W('| **Soucet** | **' + '{:,}'.format(auto).replace(',', ' ') + '** | **~' + '{:,}'.format(int(auto / CZ_RATIO)).replace(',', ' ') + '** |')
W('')
W('K tomu se pridava systemovy prompt harness, definice vsech nastroju, metadata vsech')
W('dostupnych skillu a obsah znalostniho inboxu za 14 dni (dodava SessionStart hook).')
W('Ty tri cisla nejsou v souborech, ktere umim precist — jsou uvnitr harness.')
W('')
W('## Proc na tom zalezi')
W('')
W('Kazdy z tehle tokenu je v kontextu **pred prvnim mym slovem** a posila se znovu')
W('s kazdym dalsim promptem v session. Neni to jednorazova investice — je to konstantni')
W('rezie kazdeho tahu. Prompt cache ji zlevni, ale misto v okne zabira porad.')

with open('C:/tmp/workshop-namety/_raw/doklady-cena-kontextu.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out) + '\n')

for r in rows:
    print(r)
print()
print('auto pri startu:', auto, 'znaku ~', int(auto / CZ_RATIO), 'tokenu')
