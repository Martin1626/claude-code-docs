import re, io, sys, json, collections

p = r"C:\tmp\workshop-namety\_raw\prompty-shared.md"
txt = open(p, encoding="utf-8").read()

blocks = []
for m in re.finditer(r"^## (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})\s*\n(.*?)(?=^## \d{4}-\d{2}-\d{2} |\Z)",
                     txt, re.S | re.M):
    d, t, body = m.group(1), m.group(2), m.group(3)
    body = body.strip()
    body = re.sub(r"\n---\s*\n\*\*Celkem.*$", "", body, flags=re.S).strip()
    blocks.append({"date": d, "time": t, "text": body, "len": len(body)})

print("BLOKU:", len(blocks))

# slash-only / trivial
slash = [b for b in blocks if b["text"].startswith("/")]
print("zacina slash:", len(slash))
sc = collections.Counter(b["text"].split()[0] for b in slash)
print("slash rozpad:", sc.most_common())

trivial = [b for b in blocks if b["len"] <= 12 and not b["text"].startswith("/")]
print("trivialni (<=12 znaku, ne slash):", len(trivial), [b["text"] for b in trivial])

real = [b for b in blocks if not b["text"].startswith("/") and b["len"] > 12]
print("vecne prompty:", len(real))

# distribuce delek vecnych
buckets = collections.Counter()
for b in real:
    L = b["len"]
    k = "<100" if L < 100 else "100-300" if L < 300 else "300-1000" if L < 1000 else "1000+"
    buckets[k] += 1
print("delky vecnych:", buckets.most_common())
print("nad 1000:", [(b["date"], b["time"], b["len"]) for b in real if b["len"] >= 1000])
print("300-1000:", [(b["date"], b["time"], b["len"]) for b in real if 300 <= b["len"] < 1000])

# duplicity (prepsany prompt po /model apod.)
norm = lambda s: re.sub(r"\s+", " ", s).strip().lower()
seen = collections.defaultdict(list)
for b in blocks:
    if b["len"] > 25:
        seen[norm(b["text"])[:120]].append(b["date"] + " " + b["time"])
dups = {k: v for k, v in seen.items() if len(v) > 1}
print("\nDUPLIKATNI PROMPTY:", len(dups))
for k, v in dups.items():
    print("  ", v, "|", k[:80])

# dny
days = collections.Counter(b["date"] for b in blocks)
print("\nDNY:", sorted(days.items()))

# mesice
mo = collections.Counter(b["date"][:7] for b in blocks)
print("MESICE:", sorted(mo.items()))

# klicova slova
kw = {
 "korekce": r"\b(ne|nesouhlas|špatn|proč jsi|znovu|nechtěl|radši|přesto|omyl|nefunguje|nenabízí|stále)\b",
 "prompt_o_promptu": r"(napiš|vytvoř|připrav|napíš)\s+.{0,20}prompt",
 "nemodifikuj": r"(nic nemodifikuj|nedělej žádné změny|neaplikuj|necommituj|jen prompt|nic neměň|nezapisuj)",
 "audit": r"(audit|prověř|zkontroluj|ověř|reviduj|zjisti zpětnou vazbu)",
 "generictnost": r"(obecn|generick|jakýkoliv projekt|nezmiňuj|napříč projekt)",
 "srozumitelnost": r"(srozumiteln|méně zasvěcen|žargón|žargon|neformáln)",
 "session_ref": r"(Session ID|session)",
 "varianty": r"(varian|2–3|více variant)",
}
for name, rx in kw.items():
    hits = [b for b in blocks if re.search(rx, b["text"], re.I)]
    print("\n== %s : %d" % (name, len(hits)))
    for b in hits:
        print("   %s %s | %s" % (b["date"], b["time"], re.sub(r"\s+", " ", b["text"])[:110]))
