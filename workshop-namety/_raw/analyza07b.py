# -*- coding: utf-8 -*-
import re, io, collections

path = r"C:\tmp\workshop-namety\_raw\prompty-alzask-07.md"
src = io.open(path, encoding="utf-8").read()
parts = re.split(r"^## (\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*$", src, flags=re.M)
prompts = []
for i in range(1, len(parts), 2):
    body = re.sub(r"\n---\nPocet promptu.*$", "", parts[i+1], flags=re.S).strip()
    prompts.append((parts[i], body))

fams = {
    "do chatu (nezapisuj)": ["do chatu", "zde do chatu", "sem do chatu"],
    "nic nemen / neopravuj": ["nic nemen", "neopravuj", "nic nezapisuj", "jen vypis"],
    "doptej se / zeptej se predem": ["doptej se", "zeptej se", "predem se zeptej", "nejasn"],
    "nevymyslej / cerpej jen ze zdroje": ["nevymyslej", "cerpej jen", "nehadej"],
    "zavedena terminologie / sjednot": ["zavedenou terminologii", "sjednot", "jednotne", "terminologi"],
    "schvaleni pred zapisem": ["schvalit", "potrebuji to nejprve", "vyberu si", "vyberu"],
    "reviduj / proved revizi / audit": ["reviduj", "proved revizi", "audit", "zkontroluj"],
    "changelog / verze": ["changelog", "verzi", "verze"],
    "journal / session": ["journal", "session id", "konverzaci"],
    "pokracuj": ["pokracuj"],
    "ulozeni do pameti/pravidla": ["uloz do pameti", "zaved to do", "zapis do adr", "kde je tato instrukce"],
    "model/effort meta": ["effort", "haiku", "sonnet", "opus", "fable"],
}

def strip(s):
    tr = str.maketrans("áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ", "acdeeinorstuuyzACDEEINORSTUUYZ")
    return s.translate(tr).lower()

print("=== FREKVENCE FRAZOVYCH RODIN ===")
for name, keys in fams.items():
    hits = []
    for ts, b in prompts:
        s = strip(b)
        if any(k in s for k in keys):
            hits.append(ts)
    print("%-38s %3d  (napr. %s)" % (name, len(hits), ", ".join(hits[:4])))

print("\n=== PROMPTY S 'do chatu' ===")
for ts, b in prompts:
    if "do chatu" in strip(b):
        print("[%s] %s" % (ts, b[:170].replace("\n", " / ")))

print("\n=== PROMPTY S 'neopravuj / nic nemen / jen vypis' ===")
for ts, b in prompts:
    s = strip(b)
    if any(k in s for k in ["neopravuj", "nic nemen", "jen vypis", "sam nepridavej", "nic nezapisuj"]):
        print("[%s] %s" % (ts, b[:200].replace("\n", " / ")))

print("\n=== PROMPTY S 'doptej/zeptej se predem' ===")
for ts, b in prompts:
    s = strip(b)
    if "doptej se" in s or "zeptej se" in s or "predem se zeptej" in s:
        print("[%s] %s" % (ts, b[:200].replace("\n", " / ")))

print("\n=== PROMPTY S 'nevymyslej/cerpej jen' ===")
for ts, b in prompts:
    s = strip(b)
    if "nevymyslej" in s or "cerpej jen" in s:
        print("[%s] %s" % (ts, b[:220].replace("\n", " / ")))

print("\n=== NUMEROVANE ODPOVEDI (ad N / #N / bod N / PN / 9.N) ===")
for ts, b in prompts:
    if re.search(r"^\s*(ad\s*\d|#\d|bod \d|P\d[:)]|\d+[.)]\s)", b, re.M | re.I):
        print("[%s] %s" % (ts, b[:120].replace("\n", " / ")))
