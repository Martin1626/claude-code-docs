# -*- coding: utf-8 -*-
import io, re, json, collections

SRC = r"C:\tmp\workshop-namety\_raw\prompty-alzask-08.md"
txt = io.open(SRC, encoding="utf-8").read()

# split into prompts
parts = re.split(r"(?m)^## (\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*$", txt)
# parts[0] = header, then pairs
prompts = []
for i in range(1, len(parts), 2):
    ts = parts[i]
    body = parts[i+1].strip()
    prompts.append((ts, body))

# drop last 4 (workshop prep) -> but only those on 2026-08-26 about workshop
print("total prompts parsed:", len(prompts))
print("last 6:", [p[0] for p in prompts[-6:]])

# filter out the workshop-prep ones (2026-08-26 08:16 onward per instruction: last 4)
core = [p for p in prompts if not (p[0].startswith("2026-08-26") and p[0] >= "2026-08-26 08:16")]
print("core prompts:", len(core))

slash = [p for p in core if p[1].startswith("/")]
print("slash commands:", len(slash))
cnt = collections.Counter(re.match(r"/[\w:-]+", p[1]).group(0) for p in slash)
print(cnt.most_common(40))

lens = sorted(((len(b), t) for t, b in core), reverse=True)
print("\n=== longest 25 ===")
for l, t in lens[:25]:
    print(l, t)

print("\nover 1000 chars:", sum(1 for l, t in lens if l > 1000))
print("over 500:", sum(1 for l, t in lens if l > 500))
print("under 100:", sum(1 for l, t in lens if l < 100))
print("median len:", lens[len(lens)//2][0])

def find(pat, label, flags=re.I):
    rx = re.compile(pat, flags)
    hits = [(t, b) for t, b in core if rx.search(b)]
    print("\n### %s : %d" % (label, len(hits)))
    for t, b in hits:
        first = " ".join(b.split())[:150]
        print("  -", t, "|", first)
    return hits

find(r"subagent|sub-agent|subagenty|subagentem", "SUBAGENT")
find(r"\bzatím nic ne|nic zatím ne|Nesahej na žádný soubor|zatím neupravuj|Nic needituj", "NO-WRITE GATE")
find(r"připrav prompt|napiš prompt|Vylepši tento prompt|Vytvoř .{0,20}prompt|napiš zadání|Připrav zadání", "PROMPT-AS-ARTIFACT")
find(r"zeptej se m|polož mi|předem se m|Pokud je něco nejasn|Pokud budeš mít dotazy", "ASK-FIRST")
find(r"Odkud pochází|kde to má oporu|Kde vzniklo|Jak jsi na to přišel|kdo a kdy|Kde je uvedeno|odkud máš informaci|Nevymýšlej si|Tvrdí někdo opak|Je to tak\?", "GROUNDING CHALLENGE")
find(r"revizi|reviduj|adversari", "REVIEW")
find(r"měním (své )?rozhodnutí|beru zpět|Rozhodl jsem se|přehodnotil|Vrať změnu|Zruš provedené změny|Omlouvám se|špatně jsem|Tak to jsem špatně", "DECISION REVERSAL / SELF-CORRECTION")
find(r"laicky|Vysvětli jednoduše|jednoduše vysvětli|vysvětli mi|Vysvětli, |Vysvětli co|Vysvětli jak|Vysvětli i", "EXPLAIN / LEARNING")
find(r"není pravda|to je chyba|Chyba v|Proč jsi|nesouhlas|To je blbost|blbost|mýlíš|Pozor!|není přesné|Toto je mlná|mlná", "CORRECTION HARD")
find(r"Necommituj|nepushuj|commit", "GIT")
find(r"číselník|citac|soubor:řádek|kotv|reanchor|RULE-ONT", "ONTOLOGY/CITATION")
find(r"dodavatel|BullsEye|BlueSword|PAC\b|TMT", "SUPPLIER")
find(r"Sedí to s tvým poznáním|Uvažuji|Chápeš to stejně|Dává to.{0,20}smysl|Je to tak\?|Co je tedy nyní špatně|Kde jsou slabá místa|Kde může být kolize|Zapomněl jsem na něco", "HYPOTHESIS-CHECK")
find(r"Přelož|angličtin|anglick", "TRANSLATION")
find(r"pokračuj$|^pokračuj", "CONTINUE")
