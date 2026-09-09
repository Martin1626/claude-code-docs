#!/usr/bin/env python3
import os
import re
import json
from pathlib import Path

def get_frontmatter(file_path):
    """Extract first line after --- markers (YAML/TOML)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if content.startswith('---'):
                lines = content.split('\n')
                in_fm = False
                fm_lines = []
                for line in lines[1:]:
                    if line.startswith('---'):
                        break
                    fm_lines.append(line)
                fm = '\n'.join(fm_lines)
                # Parse YAML
                if 'description:' in fm:
                    m = re.search(r'description:\s*(.+?)(?:\n|$)', fm)
                    if m:
                        return m.group(1).strip().strip('"\'')
    except:
        pass
    return ""

# Create output directory
os.makedirs('C:/tmp/workshop-namety/_raw', exist_ok=True)

out = []

# === SKILLS ===
out.append("# PART A — Inventář výbavy\n")
out.append("## 1. SKILLS\n")
out.append("| Jméno | Zdroj | Popis |\n|-------|-------|-------|\n")

skill_file = Path("C:/Users/ai_martint/.claude/skills/notion-osobni-evidence.md")
if skill_file.exists():
    desc = get_frontmatter(str(skill_file))
    out.append(f"| notion-osobni-evidence | ~/.claude/skills/ | {desc or 'N/A'} |\n")

# === COMMANDS ===
out.append("\n## 2. COMMANDS\n")
out.append("| Jméno | Zdroj | Popis |\n|-------|-------|-------|\n")

commands = {
    'glossary': 'C:/Git/alzask/.claude/commands/glossary.md',
    'learn': 'C:/Git/alzask/.claude/commands/learn.md',
    'lookup': 'C:/Git/alzask/.claude/commands/lookup.md',
    'overview': 'C:/Git/alzask/.claude/commands/overview.md',
    'review-docs': 'C:/Git/alzask/.claude/commands/review-docs.md',
    'mail': 'C:/Git/alzask/.claude/commands/dodavatele/mail.md',
    'stav': 'C:/Git/alzask/.claude/commands/dodavatele/stav.md',
    'hotovo': 'C:/Git/alzask/.claude/commands/dodavatele/hotovo.md',
}

for name, fpath in sorted(commands.items()):
    if os.path.exists(fpath):
        desc = get_frontmatter(fpath)
        out.append(f"| {name} | .claude/commands/ | {desc or 'N/A'} |\n")

# === AGENTS ===
out.append("\n## 3. AGENTS\n")
out.append("| Jméno | Soubor | Description |\n|-------|--------|-------------|\n")

agents = {
    'review-design': 'C:/Git/alzask/.claude/agents/review-design.md',
    'review-fixer': 'C:/Git/alzask/.claude/agents/review-fixer.md',
    'review-reporter': 'C:/Git/alzask/.claude/agents/review-reporter.md',
    'review-semantic': 'C:/Git/alzask/.claude/agents/review-semantic.md',
    'review-structural': 'C:/Git/alzask/.claude/agents/review-structural.md',
}

for name, fpath in sorted(agents.items()):
    if os.path.exists(fpath):
        desc = get_frontmatter(fpath)
        out.append(f"| {name} | .claude/agents/ | {desc or 'N/A'} |\n")

# === HOOKS ===
out.append("\n## 4. HOOKS (ze settings.json)\n")
out.append("| Event | File | Popis |\n|-------|------|-------|\n")
out.append("| (žádné hooks nalezeny v settings.json) |\n")

# === RULES ===
out.append("\n## 5. RULES\n")
out.append("\n### Shared rules\n")
out.append("| ID | Název | Paths glob |\n|----|----|----------|\n")

rules_path = Path("C:/Git/alzask/.claude/rules/shared")
if rules_path.exists():
    for md_file in sorted(rules_path.glob("*.md")):
        name = md_file.stem
        # Extract ID from filename
        out.append(f"| {name} | {name} | (viz soubor) |\n")

out.append("\n### Personal rules (martint)\n")
out.append("| Soubor |\n|--------|\n")
personal_path = Path("C:/Git/alzask/.claude/rules-personal/martint")
if personal_path.exists():
    for md_file in sorted(personal_path.glob("*.md")):
        out.append(f"| {md_file.stem} |\n")

# === KNOWLEDGE-INBOX ===
out.append("\n## 6. KNOWLEDGE-INBOX\n")
out.append("| Autor | Soubor | Datum | Počet kandidátů |\n|------|--------|-------|----------------|\n")

kb_path = Path("C:/Git/alzask/docs")
for author_dir in ['martint', 'tomasw']:
    kb_author = kb_path / 'knowledge-inbox' / author_dir
    if kb_author.exists():
        for md_file in sorted(kb_author.glob("*.md")):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    count = len(re.findall(r'^\s*##\s+', content, re.MULTILINE))
                out.append(f"| {author_dir} | {md_file.name} | {md_file.stem} | {count} |\n")
            except:
                pass

# === OUTPUT STYLES ===
out.append("\n## 7. OUTPUT STYLES\n")
out.append("| Jméno | Popis |\n|-------|-------|\n")
out.append("| Feynman CZ | Český, intuitivní výklad |\n")

# === PLUGINY ===
out.append("\n## 8. PLUGINY (installed_plugins.json)\n")
out.append("| Jméno | Verze | InstallPath (zkráceno) |\n|-------|--------|----------------------|\n")

plugins_info = {
    "superpowers@claude-plugins-official": "6.3.0",
    "knowledge-loop@kvados-plugins": "2.0.0",
    "spec-factory@kvados-plugins": "1.9.0",
    "frontend-design@claude-plugins-official": "b819188d2eea",
    "ontology-registry@kvados-plugins": "1.0.0",
}

for name, version in sorted(plugins_info.items()):
    out.append(f"| {name} | {version} | ~/.claude/plugins/cache/... |\n")

# === SETTINGS ===
out.append("\n## 9. SETTINGS.JSON (klíčové položky)\n")
out.append("| Položka | Hodnota |\n|---------|--------|\n")
out.append("| model | opus[1m] |\n")
out.append("| effort | high |\n")
out.append("| language | Čeština |\n")
out.append("| outputStyle | Feynman CZ |\n")
out.append("| worktree.bgIsolation | none |\n")
out.append("| statusLine | command (ccstatusline) |\n")
out.append("| enabledPlugins | superpowers, knowledge-loop, spec-factory, frontend-design, ontology-registry |\n")
out.append("| permissions.allow | 157 pravidel (read, bash, webfetch, websearch, design) |\n")
out.append("| permissions.deny | 18 pravidel (git force, rm destructive, format) |\n")
out.append("| permissions.additionalDirectories | 7 lokací (tmp, documents, projects, choco) |\n")

# === VALIDÁTORY ===
out.append("\n## 10. VALIDÁTORY A NÁSTROJE\n")
out.append("| Lokace | Nástroje |\n|--------|----------|\n")

validators = {
    ".claude/rules/shared": ["README.md"],
    ".fr-tools": ["validate.py", "config.yaml", "schema.yaml", "validate.cmd"],
    ".plc-tools": ["validate.cmd", "plc-lint.py", "README.md"],
    ".adr-tools": ["config.yaml", "validate.cmd"],
    ".ontology-tools": ["audit.py", "build.cmd", "cite.py", "reanchor.py", "README.md"],
    "docs/suppliers/.tools": ["questions.py", "msg_extract.py"],
}

for loc, tools in sorted(validators.items()):
    out.append(f"| {loc} | {', '.join(tools)} |\n")

out.append("\n## 11. PLUGINS V C:/Git/shared/plugins/\n")
out.append("| Plugin | Verze |\n|--------|-------|\n")

shared_plugins = {
    'knowledge-loop': '2.0.0',
    'ontology-registry': '1.0.0',
    'spec-factory': '1.9.0',
}

for plugin, version in sorted(shared_plugins.items()):
    out.append(f"| {plugin} | {version} |\n")

# Uložení
output_path = Path("C:/tmp/workshop-namety/_raw/faze1-inventar.md")
with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(out)

print(f"Inventář uložen: {output_path}")
print(f"Velikost: {output_path.stat().st_size} B")
