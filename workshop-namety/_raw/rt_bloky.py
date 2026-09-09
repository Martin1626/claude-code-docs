# -*- coding: utf-8 -*-
"""Red-team: kontrola aritmetiky bloku a rozlozeni draftu."""
import re, io, collections
t = io.open("katalog-draft.md", encoding="utf-8").read()
items = {}
for m in re.finditer(r"^\| ([FNKRMOAUX]-\d\d) \| ([FNKRMOAUX]) \| (.+?) \| (.+?) \| (\d+) \| (must|should|could) \| (\d) \| (.*?) \|$", t, re.M):
    iid, okruh, nazev, role, mins, prio, blok, dep = m.groups()
    items[iid] = dict(okruh=okruh, nazev=nazev, role=role, min=int(mins), prio=prio, blok=int(blok), dep=dep.strip())
print("polozek nalezeno:", len(items))

by_blok = collections.defaultdict(list)
for iid,d in items.items(): by_blok[d["blok"]].append(iid)
print("\n| blok | polozek | soucet min | must | should | could |")
print("|---|---|---|---|---|---|")
tot=0
for b in sorted(by_blok):
    ids = by_blok[b]
    s = sum(items[i]["min"] for i in ids); tot+=s
    pr = collections.Counter(items[i]["prio"] for i in ids)
    print("| %d | %d | %d | %d | %d | %d |" % (b, len(ids), s, pr["must"], pr["should"], pr["could"]))
print("CELKEM minut:", tot, " = ", round(tot/60.0,1), "hodin cisteho obsahu (bez diskuse/prestávek)")

# role distribuce
print("\nrole:")
for r,c in collections.Counter(items[i]["role"] for i in items).most_common():
    print("  %-18s %d" % (r,c))
demo = [i for i in items if "demo" in items[i]["role"]]
print("polozek s demo:", len(demo), "=", round(100.0*len(demo)/len(items)), "%")
prib = [i for i in items if "příběh" in items[i]["role"]]
print("polozek s pribehem:", len(prib))
cvic = [i for i in items if "cvičení" in items[i]["role"]]
print("polozek s cvicenim:", len(cvic), cvic)

# okruhy
print("\nokruhy:", dict(collections.Counter(items[i]["okruh"] for i in items)))
print("\nprio celkem:", dict(collections.Counter(items[i]["prio"] for i in items)))
print("must minut:", sum(items[i]["min"] for i in items if items[i]["prio"]=="must"))

# kontrola: dep ukazuje na existujici ID?
print("\nrozbite/krizove zavislosti:")
for iid,d in sorted(items.items()):
    for dep in [x.strip() for x in d["dep"].split(",")]:
        if dep in ("","—"): continue
        if dep not in items: print("  %s -> NEEXISTUJICI %s" % (iid,dep))
        elif items[dep]["blok"] > d["blok"]:
            print("  %s (blok %d) zavisi na %s (blok %d) -- ZAVISLOST DOPREDU" % (iid,d["blok"],dep,items[dep]["blok"]))

# porovnani se souhrnem v draftu
print("\ndeklarovane v draftu: bloky 1=88 2=137 3=175 4=125 5=156 6=72")
