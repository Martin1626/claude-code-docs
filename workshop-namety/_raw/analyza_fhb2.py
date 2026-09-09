#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'C:/tmp/workshop-namety/_raw/prompty-fhb-myfaber.md'
txt = open(P, encoding='utf-8').read()
parts = re.split(r'^## (\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*$', txt, flags=re.M)
items = []
for i in range(1, len(parts), 2):
    b = re.sub(r'\n---\n\*\*Celkem.*$', '', parts[i+1].strip(), flags=re.S).strip()
    items.append((parts[i], b))

PATS = {
 'A_otazky_zaver': r'(?i)\botázky\?|jsou nějaké otázky|pokud jsou nějaké otázky|zeptej se',
 'B_obdobne_jako': r'(?i)obdobn[ěé]|stejně jako|jako minule|jako v alza|jako v C:',
 'C_nejprve_cesky': r'(?i)nejprve v češtině|po odsouhlasení|přelož|čínšt|číňan|angličtin',
 'D_jen_navrh': r'(?i)připrav jen návrh|vyberu co|nechej|nesahej|neupravuj|jen návrh|do chatu|zde do chatu|Nedávej tam',
 'E_picklist': r'(?i)^(\s*)(otázky |proveď|zapracuj|oprav |pokračuj)?\s*\d+\s*(,|\s+až\s+|a\s+\d)',
 'F_at_file': r'@[\w\."/\\-]+\.(md|yaml|yml|docx|feature)',
 'G_abs_path': r'[Cc]:\\+(Git|GitHub|Temp|Users)',
 'H_image': r'\[Image #\d+\]',
 'I_pasted': r'\[Pasted text #\d+',
 'J_session_ref': r'(?i)session\s+[\w-]{4,}|Session ID',
 'K_proc_why': r'(?i)^\s*(a\s+)?proč\b|\bproč (jsi|došlo|v |u |nepovažovat)',
 'L_vysvetli': r'(?i)^\s*(vysvětli|vysvětlí|popiš|co (je|to je|znamená)|k čemu|jak (funguje|se|mám|to|nastav|probíhá)|jaký|jaké|jakým|je možné|kde )',
 'M_meta_ccode': r'(?i)claude code|plugin|marketplace|worktree|outputStyle|settings|session|/model|/context|token|instalac',
 'N_domena': r'(?i)nosič|dopravník|port|WMS|WES|WCS|AGV|T40|container|alarm|inbound|picking|zaskladň',
 'O_kontrola_prace': r'(?i)zkontroluj, zda|reviduj|prověř, zda|ověř|zda jsem|zda byly|adversi',
 'P_pamet_clovek': r'(?i)co si pamatuji|myslím, že|myslím že|domlouvali|pokud se nepletu|aspoň takto',
}
print("N =", len(items))
for k, pat in sorted(PATS.items()):
    hits = [(ts, b) for ts, b in items if re.search(pat, b, flags=re.M)]
    print("\n===== %s : %d" % (k, len(hits)))
    for ts, b in hits:
        print("  ", ts, "|", b[:150].replace('\n', ' '))
