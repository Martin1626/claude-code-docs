# -*- coding: utf-8 -*-
import io, re, collections, sys
sys.stdout.reconfigure(encoding='utf-8')

SRC = r"C:\tmp\workshop-namety\_raw\prompty-alzask-08.md"
txt = io.open(SRC, encoding="utf-8").read()
parts = re.split(r"(?m)^## (\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*$", txt)
prompts = [(parts[i], parts[i+1].strip()) for i in range(1, len(parts), 2)]
core = [p for p in prompts if not (p[0].startswith("2026-08-26") and p[0] >= "2026-08-26 08:16")]

def norm(s):
    return " ".join(s.split()).lower()

# near-duplicates (resend)
seen = collections.defaultdict(list)
for t, b in core:
    if len(b) < 25: continue
    seen[norm(b)[:120]].append(t)
dups = {k: v for k, v in seen.items() if len(v) > 1}
print("=== NEAR-DUPLICATE RESENDS: %d groups, %d prompts ===" % (len(dups), sum(len(v) for v in dups.values())))
for k, v in sorted(dups.items(), key=lambda x: -len(x[1])):
    print(len(v), v, "|", k[:90])

# short prompts (< 60 chars) not slash
short = [(t,b) for t,b in core if len(b) < 60 and not b.startswith("/")]
print("\n=== SHORT (<60ch, non-slash): %d ===" % len(short))
for t,b in short: print("  ", t, "|", " ".join(b.split()))
