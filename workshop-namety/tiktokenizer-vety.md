# Věty pro ukázku tokenizace — blok 2 (F-02), 10 min

**Nástroj:** [tiktokenizer.vercel.app](https://tiktokenizer.vercel.app/), výchozí model **gpt-4o** (tokenizér `o200k_base`).

> ⚠ **Říct nahlas, dřív než se cokoli vloží:** tiktokenizer používá tokenizéry **OpenAI**, ne Claude. Anthropic svůj tokenizér nezveřejňuje (ověřeno — negativní nález). Ukázka předvádí **princip** — jak se text seká a že čeština se seká víc — **ne počty pro Claude**. Žádné „česká věta má v Claude N tokenů". Princip je stejný u všech byte-level BPE tokenizérů; čísla se liší.

Čísla níže jsou **předpočítaná lokálně stejným tokenizérem** (`tiktoken`, `o200k_base`, 2026-09-09), takže víš, co se na plátně objeví, a nemusíš improvizovat. Znaky a bajty jsou měřené přesně.

## Doporučené pořadí na plátně (5 vložení, ~6 min)

| # | Vlož | Znaků | Bajtů | Tokenů (gpt-4o) | Znaků/token | Co ukazuje |
|---|---|---:|---:|---:|---:|---|
| 1 | `Create a functional requirement for container putaway` | 53 | 53 | **8** | 6,6 | angličtina: jedno slovo ≈ jeden token |
| 2 | `Vytvoř funkční požadavek pro naskladnění nosiče` | 47 | 54 | **18** | 2,6 | **tatáž věta česky: o 6 znaků kratší, 2,25× víc tokenů** — titul karty F-02 |
| 3 | `Vytvor funkcni pozadavek pro naskladneni nosice` | 47 | 47 | 17 | 2,8 | bez diakritiky jen o 1 token míň → **diakritika není hlavní příčina**, flexe a vzácnost slov jsou |
| 4 | `nosič, nosiče, nosiči, nosičem, nosičů, nosičům` vs. `container, containers` | 47 / 21 | 55 / 21 | **23 / 3** | 2,0 / 7,0 | skloňování rozpráší frekvenci: šest forem = šest zaplacení, `container` je jeden token |
| 5 | `PICK_STATION_A2_LOAD` | 20 | 20 | **7** | 2,9 | identifikátor: skoro tolik tokenů jako celá anglická věta — a analytik jich píše stovky |

**Volitelně, když je čas (1 min):** cesta `C:\Git\alzask\docs\fr\comp\wes\` → **15 tokenů** na 32 znaků; každý backslash je hranice. Tohle je to, čím se plní `CLAUDE.md` a pravidla.

## Účastníci si zkusí vlastní větu (3 min)

Zadání: *„Vezměte jednu větu, kterou jste dnes napsali do e-mailu nebo specifikace. Vložte ji česky. Pak ji přeložte do angličtiny (klidně kostrbatě) a vložte znovu. Porovnejte počet tokenů, ne znaků."*

Očekávaný výsledek u běžné české věty: **2,5–3 znaky na token**; u anglické **6–7**. Kdo dostane něco výrazně jiného, má v textu identifikátory, čísla nebo cesty — což je přesně pointa řádku 5.

## Rozpad na tokeny — pro případ, že se někdo zeptá „a jak to seká?"

```
Create a functional requirement for container putaway
 Create | a | functional | requirement | for | container | put | away            (8)

Vytvoř funkční požadavek pro naskladnění nosiče
 V | yt | vo | ř | funk | ční | pož | ad | ave | k | pro | n | ask | lad | nění | nos | ič | e   (18)

PICK_STATION_A2_LOAD
 P | ICK | _ST | ATION | _A | 2 | _LOAD                                          (7)
```

`požadavek` = 4 tokeny (`pož`,`ad`,`ave`,`k`), `requirement` = 1. To je celý příběh v jednom slově.

## Co z toho plyne — jedna věta na závěr bloku

**Šetři v tom, co se posílá pokaždé** (`CLAUDE.md`, pravidla, popisky skillů — česky psané a plné identifikátorů), **ne v promptu, který napíšeš jednou.** Vazba na blok 4 (`/context`).

## Co NEříkat

- konkrétní počet tokenů „v Claude" pro cokoli výše — nemáme ho
- „tiktoken podhodnocuje o X %" — zdroj nedohledán
- „čeština stojí 2× víc" jako fakt o Claude — je to fakt o tomto tokenizéru; o Claude víme jen, že Anthropic pro češtinu číslo nezveřejňuje a že tokenizér od Opus 4.7 dává ≈ 30 % víc tokenů než starší ([Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting))

## Záloha, kdyby nešla síť

Tabulka výše je celá ukázka. Stačí ji promítnout a říct, že čísla jsou z téhož tokenizéru, který by běžel v prohlížeči. Rozpady výše jsou z něj taky.

---
*Předpočítáno: `python -c "import tiktoken; tiktoken.get_encoding('o200k_base').encode(...)"`, tiktoken instalován 2026-09-09. tiktokenizer.vercel.app může mít v nabídce i jiné modely; držet **gpt-4o**, aby čísla seděla s touto tabulkou.*
