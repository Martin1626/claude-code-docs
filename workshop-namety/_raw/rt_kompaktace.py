# -*- coding: utf-8 -*-
"""Red-team: prepocet tabulky kompaktaci z doklady-kompaktace.md — hledani duplikatu a chyb souctu."""
rows = [
 (1,"2026-08-09 18:17","8671e215",579010,8244,570766),
 (2,"2026-08-10 15:26","8671e215",440617,9506,431111),
 (3,"2026-08-11 05:32","8671e215",544395,7100,537295),
 (4,"2026-08-11 13:55","8671e215",586517,11668,574849),
 (5,"2026-08-12 19:24","84d16ec6",602574,14075,2702520),
 (6,"2026-08-12 19:24","8671e215",602574,14075,588499),
 (7,"2026-08-13 06:26","84d16ec6",408542,11757,396785),
 (8,"2026-08-13 06:26","8671e215",408542,11757,396785),
 (9,"2026-08-13 10:27","84d16ec6",419004,11950,407054),
 (10,"2026-08-13 20:58","fe6ed3f5",356334,9488,346846),
 (11,"2026-08-18 20:16","c72f51b9",583578,12127,571451),
 (12,"2026-08-19 13:26","e8e214bb",572770,13344,559426),
 (13,"2026-08-19 17:45","740e5808",422833,18885,403948),
 (14,"2026-08-19 19:06","740e5808",416445,16927,399518),
 (15,"2026-08-19 20:32","740e5808",521073,15372,505701),
 (16,"2026-08-19 20:43","740e5808",136471,20495,115976),
 (17,"2026-08-20 10:01","dd923fb6",214931,13372,201559),
 (18,"2026-08-21 14:17","aa5edff8",618390,15342,603048),
 (19,"2026-08-22 21:21","90d8b6e7",575151,15666,559485),
 (20,"2026-08-24 06:06","70e84664",464352,10248,454104),
 (21,"2026-08-25 10:09","d02c3695",392015,18245,373770),
]
print("radku:", len(rows))
# duplikaty podle (datum, pre, post)
seen = {}
dups = []
for r in rows:
    k = (r[1], r[3], r[4])
    if k in seen: dups.append((seen[k], r[0], k))
    else: seen[k] = r[0]
print("duplikatni udalosti (stejny cas + pre + post, jina session):", dups)

# konzistence: pre - post == zahozeno v kroku?
print("\nnekonzistentni radky (pre-post != zahozeno):")
for r in rows:
    if r[3]-r[4] != r[5]:
        print("  #%d %s  pre-post=%d  tabulka=%d  rozdil=%d" % (r[0], r[1], r[3]-r[4], r[5], r[5]-(r[3]-r[4])))

tot = sum(r[5] for r in rows)
print("\nsoucet sloupce 'zahozeno' jak je v dokladu:", tot)
fixed = [(r[3]-r[4]) for r in rows]
print("soucet po opraveni radku 5 na pre-post:", sum(fixed))
dedup_ids = {5,8}   # odstranit jeden z kazde duplikatni dvojice
dd = sum(r[3]-r[4] for r in rows if r[0] not in dedup_ids)
print("soucet po opraveni A deduplikaci (bez #5 a #8):", dd)
print("nadhodnoceni dokladu vuci opravenemu:", tot-dd, "=", round(100.0*(tot-dd)/dd,1), "%")
print("pocet skutecnych kompaktaci po deduplikaci:", len(rows)-len(dedup_ids))

# median procent
import statistics
pcts = sorted(round(100.0*(r[3]-r[4])/r[3],1) for r in rows if r[0] not in dedup_ids)
print("\nmedian procent zahozeno (dedup):", statistics.median(pcts))
pre = sorted(r[3] for r in rows if r[0] not in dedup_ids)
post = sorted(r[4] for r in rows if r[0] not in dedup_ids)
print("median pre:", statistics.median(pre), " median post:", statistics.median(post))
print("procenta z paru medianu (583578 -> 12127):", round(100.0*(583578-12127)/583578,1))
dur = sorted([196.4,186.2,171.5,224.1,159.7,159.7,159.9,159.9,201.7,191.4,180.7,119.3,200.7,193.9,184.9,183.5,177.5,173.8,162.2,172.8,168.6])
print("median trvani (vsech 21):", statistics.median(dur))
