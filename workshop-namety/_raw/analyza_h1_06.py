# -*- coding: utf-8 -*-
import re, io, sys, os, collections

BASE = r"C:\tmp\workshop-namety\_raw"
files = ["prompty-alzask-H1.md", "prompty-alzask-06.md"]

def parse(path):
    txt = io.open(path, encoding="utf-8").read()
    parts = re.split(r"^## (\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*$", txt, flags=re.M)
    out = []
    for i in range(1, len(parts), 2):
        ts = parts[i]
        body = parts[i+1]
        body = re.sub(r"\n---\nPocet promptu v souboru: \d+\s*$", "", body)
        out.append((ts, body.strip()))
    return out

allp = []
for f in files:
    p = parse(os.path.join(BASE, f))
    print(f, len(p))
    allp += [(f,) + x for x in p]

# length distribution
lens = [len(b) for _,_,b in allp]
print("total", len(allp))
buckets = collections.Counter()
for L in lens:
    if L < 20: buckets["<20"] += 1
    elif L < 100: buckets["20-99"] += 1
    elif L < 300: buckets["100-299"] += 1
    elif L < 1000: buckets["300-999"] += 1
    else: buckets[">=1000"] += 1
print(sorted(buckets.items(), key=lambda x: x[1], reverse=True))

# slash commands
slash = collections.Counter()
for _,_,b in allp:
    m = re.match(r"^\s*/([\w:-]+)", b)
    if m: slash[m.group(1)] += 1
print("slash total", sum(slash.values()))
print(slash.most_common(40))

# one-liners that are continuations
cont = collections.Counter()
for _,_,b in allp:
    bl = b.lower().strip()
    if len(bl) < 40:
        cont[bl] += 1
print("short prompts:", [x for x in cont.most_common(60)])

print("\n=== LONG >=1000 ===")
for f,ts,b in allp:
    if len(b) >= 1000:
        print("---", ts, len(b))
        print(b[:260].replace("\n"," | "))

print("\n=== CORRECTION CANDIDATES ===")
pat = re.compile(r"\b(ne|nesouhlas|špatně|nespráv|proč jsi|znovu|to není|nechtěl|mýlíš|radši|raději|ale |nerozum|nevidím|chybí|opra|vrať|obnov|nefunguje|neuloží|zůstal|nemá|nesmí|neměl|místo toho|naopak|nechci|neuváděj|nezmiňuj|nevšímej|nezahrnuj|jak je to možné|už mnohokrát)", re.I)
n=0
for f,ts,b in allp:
    if pat.search(b) and len(b) > 25:
        n+=1
        print("---", ts, "|", b[:230].replace("\n"," | "))
print("correction candidates:", n)
