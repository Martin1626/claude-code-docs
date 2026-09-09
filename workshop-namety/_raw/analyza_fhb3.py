#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, io, sys
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'C:/tmp/workshop-namety/_raw/prompty-fhb-myfaber.md'
txt = open(P, encoding='utf-8').read()
parts = re.split(r'^## (\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*$', txt, flags=re.M)
items = []
for i in range(1, len(parts), 2):
    b = re.sub(r'\n---\n\*\*Celkem.*$', '', parts[i+1].strip(), flags=re.S).strip()
    items.append((parts[i], b))

c = Counter(ts[:10] for ts, _ in items)
print("PER DAY (%d dnu):" % len(c))
for d in sorted(c):
    print("  %s  %3d" % (d, c[d]))

# clusters of interest
def show(d0, d1=None):
    d1 = d1 or d0
    sel = [(ts,b) for ts,b in items if d0 <= ts[:10] <= d1]
    print("\n##### %s..%s : %d promptu" % (d0, d1, len(sel)))
    for ts,b in sel:
        print("  %s | %s" % (ts[11:], b[:110].replace('\n',' ')))

show('2026-06-26','2026-06-27')
show('2026-07-04','2026-07-05')
show('2026-07-07')
show('2026-08-20','2026-08-25')
