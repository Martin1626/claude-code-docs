# -*- coding: utf-8 -*-
"""Red-team: presne pocty slash prikazu a klicovych slov v cele history.jsonl."""
import json, io, re, collections, os

p = os.path.expanduser("~/.claude/history.jsonl")
rows = []
with io.open(p, encoding="utf-8", errors="replace") as fh:
    for line in fh:
        line = line.strip()
        if not line: continue
        try: rows.append(json.loads(line))
        except Exception: pass
print("radku:", len(rows))
k = collections.Counter()
for r in rows: k.update(r.keys())
print("klice:", k.most_common(12))

def proj(r):
    v = (r.get("project") or r.get("cwd") or r.get("projectPath") or "")
    return v.replace("\\","/").lower()

WORK = ("c:/git/alzask","c:/git/fhb","c:/git/myfaber","c:/git/shared")
def is_work(r):
    pr = proj(r)
    return any(pr.startswith(w) for w in WORK)

def txt(r):
    return (r.get("display") or r.get("prompt") or r.get("text") or r.get("content") or "")

work = [r for r in rows if is_work(r)]
print("pracovnich promptu:", len(work), " celkem:", len(rows))

pats = {
 "/review-docs": r"^/review-docs",
 "/learn": r"^/learn", "/lookup": r"^/lookup", "/overview": r"^/overview", "/glossary": r"^/glossary",
 "/project:": r"^/project:",
 "/insights": r"^/insights", "/rewind": r"^/rewind", "/clear": r"^/clear", "/compact": r"^/compact",
 "/usage": r"^/usage", "/cost": r"^/cost", "/plan": r"^/plan", "/loop": r"^/loop",
 "/memory": r"^/memory", "/therapy": r"^/therapy", "/pruzkum": r"^/pruzkum",
 "/body-z-jednani": r"^/body-z-jednani", "/spec": r"^/spec", "/dodavatele": r"^/dodavatele",
 "/knowledge-loop": r"^/knowledge-loop", "/rule-new": r"rule-new", "rules-consolidate": r"rules-consolidate",
 "/ontologie": r"^/ontologie", "/ontology-registry": r"^/ontology-registry",
 "/model": r"^/model", "/effort": r"^/effort", "/context": r"^/context", "/resume": r"^/resume",
 "/agents": r"^/agents", "/hooks": r"^/hooks", "/output-style": r"^/output-style",
}
print("\n| vzor | cela historie | pracovni |")
print("|---|---|---|")
for name, pat in pats.items():
    a = sum(1 for r in rows if re.match(pat, txt(r).strip(), re.I))
    b = sum(1 for r in work if re.match(pat, txt(r).strip(), re.I))
    print("| %s | %d | %d |" % (name, a, b))

# review agenti zminovani v textu
print("\nzminky review-* agentu v textu promptu (pracovni):",
      sum(1 for r in work if re.search(r"review-(semantic|structural|design|fixer|reporter)", txt(r), re.I)))
print("zminky 'compact' s instrukci (/compact <text>):",
      sum(1 for r in rows if re.match(r"^/compact\s+\S", txt(r).strip(), re.I)))
