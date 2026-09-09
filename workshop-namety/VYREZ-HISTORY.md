# Výřezy z `history.jsonl` pro 1. sezení

**Zdroj:** `~/.claude/history.jsonl` (3 078 řádků, 1,04 MB k 2026-09-09), filtr `project == C:\Git\alzask` (1 513 řádků).
**Účel:** ukázat na plátně jen prompty z projektu Alza — celý soubor obsahuje i jiné klienty a nepatří před publikum.

---

## 1. `vyrez-history-2026-08-19.jsonl` → blok 1 (F-01), navazuje na bloky 6–7

Jedna session (`740e5808…`), **14 řádků**, 16:33–23:03, přesně tak, jak leží v `history.jsonl` — nic přepsáno, nic zkráceno (`pastedContents` byl u všech 14 řádků prázdný už v originále).

| Čas | Znaků | Prompt (začátek) |
|---|---|---|
| 16:33 | 59 | `Proveď prompt C:\Temp\PROMPT_kontrola_volani_na_portech.md` |
| 19:41 | 1216 | `1. Spusť docs/plc/.plc-tools/validate.cmd …` |
| 19:41 | 8 | `/compact` |
| 19:45 | 1216 | *(totéž zadání znovu — po kompaktaci)* |
| 20:24 | 23 | `ještě jedno kolo revize` |
| 20:35 | 208 | `/btw Jak došlo k tomu, že u PICK_SHIPPING_NORTH …` |
| 21:03 | 8 | `/compact` |
| 21:10 | 113 | `Proveď prompt C:\Temp\PROMPT_readyToClose_sever_expedice.md …` |
| 21:30 | 77 | `V ADR nepotřebuji zmiňovat, že jeden den platilo něco jiného.` |
| 22:24 | 24 | `Verzi API posuň na 1.2.2` |
| 22:29 | 8 | `/compact` |
| 22:33 | 70 | `/spec-factory:review-spec Změny v @docs/api/…` |
| 22:40 | 8 | `/compact` |
| 23:03 | 82 | `Jsou informace z C:\Temp\WMS_volani_na_portech_k_odsouhlaseni.md podchycené v ADR?` |

**Proč právě tahle session — tři věci na jedné obrazovce:**

1. **F-01:** každý prompt = jeden řádek JSON s časem, textem a ID session. „Tohle je vaše konverzace. Na vašem disku, ne v hlavě modelu."
2. **K-01 předehra:** 10 ze 14 promptů má pod 120 znaků a **tři z nich jen ukazují na soubor** (`Proveď prompt C:\Temp\…md`). Krátký prompt, protože zadání leží v souboru.
3. **F-03/F-04 doklad:** **4× `/compact` v jedné session** (19:41, 21:03, 22:29, 22:40) — to jsou **řádky 11–14 tabulky kompaktací** na slidu (session `740e5808`, 4 kompaktace, 1 425 143 zahozených tokenů). Publikum uvidí tu samou událost ze dvou stran: příkaz v historii a její cenu v transkriptu.

**Jak ukázat:** otevřít soubor v editoru (VS Code, zalamování vypnuté), neupravovat. Účastníci si zatím otevřou svůj `~/.claude/history.jsonl`.

## 2. `vyrez-history-2026-07-09-K01.txt` → blok 8 (K-01)

Prompt z **2026-07-09 21:54**, session `413b4605…`, **2 106 znaků, 34 řádků** — nejdelší prompt měsíce. Text promptu doslova, bez JSON obalu.

Struktura: první řádek `Zapracuj odpovědi požadované v @docs/plc/BACKLOG.md`, pak očíslované otázky z backlogu a pod každou odsazená odpověď. **15 odpovědí, žádná otázka** — otázky žijí v `BACKLOG.md`, prompt je jen doručení rozhodnutí. Přesně teze karty K-01.

**Jak ukázat:** vedle sebe tento soubor a `docs/plc/BACKLOG.md` v projektu Alza (stav z 2026-07-09, pokud ho git má — ověřit `git log -1 --before=2026-07-10 -- docs/plc/BACKLOG.md`).

---

## Kontrola citlivého obsahu (provedena 2026-09-09)

Nad všemi 1 513 řádky projektu alzask:

- **Přístupové klíče / tokeny:** hledány vzory `sk-ant-`, `ghp_`, `glpat-`, `xox[bp]-`, `Bearer …`, JWT (`eyJ…`), řetězce 32+ znaků — **žádný skutečný klíč.** 75 zásahů dlouhých řetězců jsou názvy souborů, čísla objednávek (`940-SO-…`), UUID a ID požadavků. Slovo „token" 8× — vždy ve smyslu LLM tokenů nebo návrhu API (bez hodnot).
- **E-maily:** 0.
- Čtyři tokeny zmiňované v kartě N-04 tedy **nejsou v projektu alzask** — jsou v jiném projektu; do výřezu se nedostanou.

Oba výřezy obsahují interní názvy z projektu Alza (`PICK_SHIPPING_NORTH`, `readyToClose`, `API-myFABER-WES-AlzaSk.yml`, TMT, PAC, Sick 1050). Před publikem z Alzy je to jejich vlastní projekt; před jiným publikem by se výřez musel anonymizovat.

## Poznámka k časům — nesoulad, který je třeba znát

Časy v `history.jsonl` jsou **lokální (CEST)**; časy v tabulce kompaktací (`DOKLADY.md`, slide) pocházejí z transkriptů a jsou **UTC**. Řádky 11–14 slidu (17:45, 19:06, 20:32, 20:43) odpovídají příkazům `/compact` v historii (19:41, 21:03, 22:29, 22:40) — rozdíl 2 h + doba běhu kompaktace (3 min). Sedí to, ale kdyby se někdo zeptal, proč se časy liší, tohle je odpověď. Volitelně lze slide přepočítat na lokální čas.
