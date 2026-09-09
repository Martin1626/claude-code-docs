# -*- coding: utf-8 -*-
import re, io, json, collections

path = r"C:\tmp\workshop-namety\_raw\prompty-alzask-07.md"
src = io.open(path, encoding="utf-8").read()

# split into prompts
parts = re.split(r"^## (\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*$", src, flags=re.M)
# parts[0] = header, then pairs
prompts = []
for i in range(1, len(parts), 2):
    ts = parts[i]
    body = parts[i+1].strip()
    body = re.sub(r"\n---\nPocet promptu.*$", "", body, flags=re.S).strip()
    prompts.append((ts, body))

print("POCET PROMPTU:", len(prompts))

# slash commands
slash = collections.Counter()
for ts, b in prompts:
    m = re.match(r"^(/[a-zA-Z0-9_:\-]+)", b)
    if m:
        slash[m.group(1)] += 1
print("\n=== SLASH PRIKAZY (pocet) ===")
for k, v in slash.most_common(40):
    print("%4d  %s" % (v, k))
print("celkem slash promptu:", sum(slash.values()))

# lengths
lens = [(len(b), ts, b) for ts, b in prompts]
long = [x for x in lens if x[0] >= 1000]
mid = [x for x in lens if 400 <= x[0] < 1000]
short = [x for x in lens if x[0] < 100]
print("\n=== DELKY ===")
print("nad 1000 znaku:", len(long))
print("400-999:", len(mid))
print("pod 100 znaku:", len(short))
print("median:", sorted(x[0] for x in lens)[len(lens)//2])
print("\n--- DLOUHE (>=1000) ---")
for L, ts, b in sorted(long, reverse=True):
    print("%5d  %s  | %s" % (L, ts, b[:110].replace("\n", " / ")))

# context management: what surrounds /compact
print("\n=== OKOLI /compact ===")
for i, (ts, b) in enumerate(prompts):
    if b.strip().startswith("/compact"):
        prev = prompts[i-1] if i > 0 else ("-", "-")
        nxt = prompts[i+1] if i+1 < len(prompts) else ("-", "-")
        print("--- compact %s" % ts)
        print("   PRED: %s | %s" % (prev[0], prev[1][:100].replace("\n", " / ")))
        print("   PO  : %s | %s" % (nxt[0], nxt[1][:100].replace("\n", " / ")))

# corrections heuristics
markers = ["ne ", "nefunguj", "špatn", "chyb", "proč jsi", "znovu", "nesouhlas", "to není",
           "nechtěl", "mýlíš", "radši", "raději", "koriguj", "oprav", "vlastně", "nerozumím",
           "nejsem si jistý", "změnil jsem názor", "je tam logická chyba", "opět", "pořád",
           "stále", "nepotřebuj", "neuváděj", "nedělá", "vrať"]
print("\n=== KANDIDATI KOREKCE ===")
cnt = 0
for ts, b in prompts:
    low = b.lower()
    hits = [m for m in markers if m in low]
    if hits and not b.startswith("/"):
        cnt += 1
        print("[%s] {%s} %s" % (ts, ",".join(hits[:4]), b[:160].replace("\n", " / ")))
print("kandidatu korekce:", cnt)

# @-references and absolute paths
at = sum(1 for ts, b in prompts if "@docs/" in b or "@..\\" in b or "@temp/" in b)
abspath = sum(1 for ts, b in prompts if re.search(r"[Cc]:\\", b))
img = sum(1 for ts, b in prompts if "[Image #" in b)
print("\npromptu s @-referenci:", at)
print("promptu s absolutni cestou:", abspath)
print("promptu s obrazkem:", img)

# two-step pattern: same prompt sent twice / prefix repeated
print("\n=== DVOUFAZOVE ZADANI (kratky pak dlouhy se stejnym zacatkem) ===")
for i in range(len(prompts)-1):
    a = prompts[i][1]
    bb = prompts[i+1][1]
    if a.startswith("/") or len(a) > 200:
        continue
    head = a.strip()[:25]
    if len(head) > 8 and bb.startswith(head[:15]) and len(bb) > len(a) + 40:
        print("[%s] %r  ->  [%s] %s" % (prompts[i][0], a[:60], prompts[i+1][0], bb[:90].replace("\n", " / ")))

# repeated identical prompts (re-send)
print("\n=== OPAKOVANE IDENTICKE PROMPTY ===")
norm = collections.Counter()
for ts, b in prompts:
    key = re.sub(r"\s+", " ", b).strip().lower()[:120]
    norm[key] += 1
for k, v in norm.most_common(25):
    if v > 1:
        print("%2dx  %s" % (v, k[:110]))
