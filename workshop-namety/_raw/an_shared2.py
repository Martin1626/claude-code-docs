import re, collections
p = r"C:\tmp\workshop-namety\_raw\prompty-shared.md"
txt = open(p, encoding="utf-8").read()
blocks = []
for m in re.finditer(r"^## (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})\s*\n(.*?)(?=^## \d{4}-\d{2}-\d{2} |\Z)",
                     txt, re.S | re.M):
    body = re.sub(r"\n---\s*\n\*\*Celkem.*$", "", m.group(3), flags=re.S).strip()
    blocks.append((m.group(1), m.group(2), body))

real = [b for b in blocks if not b[2].startswith("/") and len(b[2]) > 12]
out = []
for i, (d, t, s) in enumerate(real, 1):
    out.append("%03d| %s %s |%5d| %s" % (i, d, t, len(s), re.sub(r"\s+", " ", s)[:150]))
open(r"C:\tmp\workshop-namety\_raw\an_shared2_out.txt", "w", encoding="utf-8").write("\n".join(out))
print(len(real), "radku zapsano")

# tema pluginu vs. jine tema
temata = {
 "spec-factory": r"(spec.factory|spec-factory|review-spec|agent|orchestr|rubrik|planner|research|YAGNI|nález|DoD|osnov)",
 "knowledge-loop": r"(znalost|pravidl|inbox|osobní pravid|rules)",
 "ontology": r"(ontolog)",
 "marketplace/instalace": r"(marketplace|token|instal|plugin|reload|README|homepage|commit|merge|push)",
 "prezentace/docs": r"(prezentac|dokumentac|srozumiteln|HTML|slide|osnov|populariz)",
 "mimo (simulace)": r"(dopravník|nosič|palet|simulac)",
}
for name, rx in temata.items():
    hits = [b for b in real if re.search(rx, b[2], re.I)]
    print("%-24s %d" % (name, len(hits)))
