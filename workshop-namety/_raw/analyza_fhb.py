#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, io, sys, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'C:/tmp/workshop-namety/_raw/prompty-fhb-myfaber.md'
txt = open(P, encoding='utf-8').read()

# split on headers
parts = re.split(r'^## (\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*$', txt, flags=re.M)
# parts[0] = header
items = []
for i in range(1, len(parts), 2):
    ts = parts[i]
    body = parts[i+1].strip()
    body = re.sub(r'\n---\n\*\*Celkem.*$', '', body, flags=re.S).strip()
    items.append((ts, body))
print("POCET PROMPTU:", len(items))

lens = sorted(len(b) for _, b in items)
def pct(p):
    return lens[int(len(lens)*p/100)]
print("len min/p25/med/p75/p90/max:", lens[0], pct(25), pct(50), pct(75), pct(90), lens[-1])

# monthly
from collections import Counter, defaultdict
m = Counter(ts[:7] for ts, _ in items)
print("PER MONTH:", sorted(m.items()))

slash = [ (ts,b) for ts,b in items if b.startswith('/') ]
print("SLASH COUNT:", len(slash))
print("SLASH CMDS:", Counter(re.match(r'/[\w:-]+', b).group(0) for ts,b in slash).most_common())

short = [ (ts,b) for ts,b in items if len(b) <= 20 and not b.startswith('/') ]
print("\n--- KRATKE (<=20 znaku, ne slash):", len(short))
for ts,b in short: print("  ", ts, "|", b.replace('\n',' '))

print("\n=== DLOUHE >500 znaku ===")
longs = [ (ts,b) for ts,b in items if len(b) > 500 ]
print("pocet:", len(longs))
for ts,b in longs:
    print("-"*70)
    print(ts, "| LEN", len(b))
    print(b[:400].replace('\n',' | '))

# keyword scans
kws = {
 'alzask-ref': r'(?i)\balza(sk|\.sk|)\b|C:\\\\Git\\\\alzask|obdobn|stejn(ě|e) jako|jako v ',
 'korekce': r'(?i)^(ne|ne,|nesouhlas|špatn|proč jsi|znovu|to není|to jsem nechtěl|radši|vrať)',
 'vrat-zpet': r'(?i)vrať|zpět|zruš|proč (došlo|jsi|v )|nekoncep',
 'over': r'(?i)ověř|prověř|zkontroluj|kontrol|revid|reviz',
 'citace': r'(?i)citac|soubor:řádek|`soubor',
 'zeptej': r'(?i)zeptej se|pokud jsou nějaké otázky|nedomýšlej|nejsi si jistý',
 'nesahej': r'(?i)nesahej|nic nezapisuj|jen návrh|připrav jen návrh|neupravuj|bez commitu',
 'styl': r'(?i)styl|feynman|laicky|populární|srozumiteln|jednodu(še|chému)',
 'plugin': r'(?i)plugin|marketplace|spec factory|specfactory|spec-factory',
 'meta': r'(?i)worktree|settings|instalac|git|commit|merge|token|kerberos|krb',
}
print("\n=== KEYWORD HITS ===")
for k, pat in kws.items():
    hits = [(ts,b) for ts,b in items if re.search(pat, b, flags=re.M)]
    print("\n## %s : %d" % (k, len(hits)))
    for ts,b in hits[:60]:
        print("   ", ts, "|", b[:130].replace('\n',' '))
