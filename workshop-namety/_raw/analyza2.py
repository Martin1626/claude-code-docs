# -*- coding: utf-8 -*-
import re, io, os, collections
BASE = r"C:\tmp\workshop-namety\_raw"
def parse(path):
    txt = io.open(path, encoding="utf-8").read()
    parts = re.split(r"^## (\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*$", txt, flags=re.M)
    out=[]
    for i in range(1,len(parts),2):
        b=re.sub(r"\n---\nPocet promptu v souboru: \d+\s*$","",parts[i+1]).strip()
        out.append((parts[i],b))
    return out
allp=[]
for f in ["prompty-alzask-H1.md","prompty-alzask-06.md"]:
    allp += [(f,)+x for x in parse(os.path.join(BASE,f))]

def cnt(pred): return [ (ts,b) for f,ts,b in allp if pred(b) ]

ref = cnt(lambda b: "@" in b or re.search(r"[A-Za-z]:\\\\|C:\\\\", b) or "C:\\" in b)
print("s odkazem na soubor/cestu:", len(ref))
q = cnt(lambda b: "?" in b)
print("obsahuje otazku:", len(q))
ano = cnt(lambda b: re.match(r"^\s*(ano|ok|souhlas|schvaluji|hotovo|zkop)", b, re.I))
print("potvrzeni/schvaleni:", len(ano), [t for t,_ in ano])
pokr = cnt(lambda b: re.match(r"^\s*pokra", b, re.I))
print("pokracuj:", len(pokr))
wt = cnt(lambda b: "worktree" in b.lower())
print("worktree:", len(wt), [t for t,_ in wt])
otaz = cnt(lambda b: re.search(r"Ot[aá]zky\?|zeptej se|Polo[zž] mi|dopta", b, re.I))
print("vyzva k doptani:", len(otaz), [t for t,_ in otaz])
prev = cnt(lambda b: re.search(r"Prom[ií]tni|zapracuj|Dopl[nň] (kontrolu|to) tak|tak[eé] do|Zapamatuj", b, re.I))
print("propsani do souvisejicich/zafixovani:", len(prev), [t for t,_ in prev])
zafix = cnt(lambda b: re.search(r"Zapamatuj|zalo[zž] rule|na shared|user level|vytvo[rř] validate|napi[sš] plc-lint|slash|command|skill", b, re.I))
print("zafixovani do nastroje:", len(zafix), [t for t,_ in zafix])
meta = cnt(lambda b: re.search(r"analyzuj (posledn[ií]|pro[cč])|Prozkoumej thinking|journal|session", b, re.I))
print("meta-analyza vlastnich behu:", len(meta), [t for t,_ in meta])
# duplicity
seen=collections.Counter([b[:120] for f,ts,b in allp if len(b)>60])
print("duplikaty(prefix120):", [(k[:60],v) for k,v in seen.items() if v>1])
