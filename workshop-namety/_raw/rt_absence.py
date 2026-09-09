# -*- coding: utf-8 -*-
"""Red-team: hledani ABSENCE temat v surovych promptech (doklad pro nalezy typu 'chybi')."""
import re, glob, os, io, json, collections

files = ["prompty-alzask-H1.md","prompty-alzask-06.md","prompty-alzask-07.md",
         "prompty-alzask-08.md","prompty-fhb-myfaber.md","prompty-shared.md"]
base = os.path.dirname(os.path.abspath(__file__))
txt = {}
for f in files:
    p = os.path.join(base,f)
    if os.path.exists(p):
        txt[f] = io.open(p, encoding="utf-8", errors="replace").read()
all_txt = "\n".join(txt.values())
print("celkem znaku surovych promptu:", len(all_txt))

groups = {
 "zakaznik/jednani": [r"z[aá]kazn[ií]k", r"jedn[aá]n[ií]", r"sch[uů]zk", r"BullsEye", r"Blue[Ss]word"],
 "prezentace publiku": [r"prezentac", r"slide", r"deck", r"workshop"],
 "odhady/pracnost": [r"odhad", r"pracnost", r"man-?day", r"\bMD\b", r"story point", r"kapacit"],
 "cena/rozpocet": [r"rozpo[cč]et", r"kolik.{0,20}stoj", r"\$", r"MTok", r"n[aá]klad na token", r"cena tokenu"],
 "bezpecnost/GDPR": [r"GDPR", r"osobn[ií] [uú]daj", r"citliv", r"anonymiz", r"de-?identif", r"NDA", r"tajemstv"],
 "licence": [r"licen[cs]", r"copyright", r"autorsk"],
 "code review ciziho kodu": [r"code ?review", r"review k[oó]du", r"merge request", r"\bMR\b", r"pull request"],
 "prace ve dvojici/tym": [r"ve dvojici", r"pair", r"kolega", r"koleg", r"t[yý]m\b", r"t[yý]mov"],
 "onboarding cloveka": [r"onboarding", r"nov[yý] [cč]len", r"za[sš]kol"],
 "testovani/testy": [r"\btest", r"\bTC-"],
 "kdy NEpouzit": [r"ne[pP]ou[zž]", r"rad[eě]ji ru[cč]n", r"ud[eě]l[aá]m to s[aá]m", r"bez claude"],
 "psani kodu": [r"implementuj", r"naprogramuj", r"refaktor", r"unit test", r"debug"],
 "obrazky/screenshoty": [r"screenshot", r"obr[aá]zek", r"sn[ií]mek", r"\.png", r"\.jpg"],
 "hlasovy vstup/diktovani": [r"diktov", r"nahr[aá]vk", r"\.vtt", r"transkript"],
 "MCP/Notion": [r"\bMCP\b", r"Notion", r"Jira", r"Freelo"],
 "excel/xlsx": [r"xlsx", r"excel", r"\.csv"],
 "email": [r"e-?mail", r"\.msg", r"outlook"],
 "worktree": [r"worktree"],
 "git": [r"\bgit\b", r"commit", r"branch", r"v[eě]tv"],
}
print()
print("| tema | vyskytu | v kolika souborech |")
print("|---|---|---|")
for name, pats in groups.items():
    tot = 0
    nf = 0
    for f,t in txt.items():
        c = sum(len(re.findall(p, t, re.I)) for p in pats)
        tot += c
        if c: nf += 1
    print("| %s | %d | %d/%d |" % (name, tot, nf, len(txt)))
