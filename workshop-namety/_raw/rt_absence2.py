# -*- coding: utf-8 -*-
"""Red-team: kontexty vzacnych temat + presnejsi odhady."""
import re, os, io

files = ["prompty-alzask-H1.md","prompty-alzask-06.md","prompty-alzask-07.md",
         "prompty-alzask-08.md","prompty-fhb-myfaber.md","prompty-shared.md"]
base = os.path.dirname(os.path.abspath(__file__))
txt = {}
for f in files:
    p = os.path.join(base,f)
    if os.path.exists(p):
        txt[f] = io.open(p, encoding="utf-8", errors="replace").read()

def show(label, pat, limit=12, w=90):
    print("\n### %s   pattern=%s" % (label, pat))
    n = 0
    for f,t in txt.items():
        for m in re.finditer(pat, t, re.I):
            n += 1
            if n > limit:
                print("   ... (dalsi vynechany)")
                return
            s = max(0, m.start()-w); e = min(len(t), m.end()+w)
            frag = t[s:e].replace("\n"," ")
            print("  [%s] ...%s..." % (f, frag))
    if n == 0:
        print("  ZADNY VYSKYT")

show("cena/rozpocet", r"rozpo[cč]et|kolik.{0,20}stoj|MTok|cena tokenu")
show("GDPR/citlive", r"GDPR|osobn[ií] [uú]daj|citliv|anonymiz|de-?identif|NDA")
show("code review", r"code ?review|review k[oó]du|merge request|pull request")
show("kdy NEpouzit claude", r"rad[eě]ji ru[cč]n|ud[eě]l[aá]m to s[aá]m|bez claude|nepou[zž]ij")
show("odhad pracnosti (presne)", r"odhad(ni|nout|em|u)?\s+(pracnost|nabídk|ceny|času|casu|MD)|pracnost|man-?day|story point")
show("prace ve dvojici", r"ve dvojici|pair progr|spole[cč]n[eě] s koleg")
show("prezentace pro publikum", r"prezentac|slide|deck")
show("licence", r"licen[cs]|copyright|autorsk")
