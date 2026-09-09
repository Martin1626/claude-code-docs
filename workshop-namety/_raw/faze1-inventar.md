# PART A — Inventář výbavy
## 1. SKILLS
| Jméno | Zdroj | Popis |
|-------|-------|-------|

## 2. COMMANDS
| Jméno | Zdroj | Popis |
|-------|-------|-------|
| glossary | .claude/commands/ | N/A |
| hotovo | .claude/commands/ | Zapíše, že odpověď dodavatele je propsaná do specifikace |
| learn | .claude/commands/ | N/A |
| lookup | .claude/commands/ | N/A |
| mail | .claude/commands/ | Zpracuje e-mail od/pro dodavatele do registru dotazů |
| overview | .claude/commands/ | N/A |
| review-docs | .claude/commands/ | N/A |
| stav | .claude/commands/ | Vypíše, na co se u dodavatele čeká a co už víme |

## 3. AGENTS
| Jméno | Soubor | Description |
|-------|--------|-------------|
| review-design | .claude/agents/ | Designová kontrola — soulad ADR, API spec, procesní analýzy a FR |
| review-fixer | .claude/agents/ | Automatická oprava auto-fixable nálezů z review reportu (kromě ARCH-DECISION) |
| review-reporter | .claude/agents/ | Agregace nálezů a generování centrálního review reportu |
| review-semantic | .claude/agents/ | Sémantická kontrola FR/TC — konzistence s API schématem, ADR, procesní analýzou |
| review-structural | .claude/agents/ | Strukturální kontrola FR/TC — cross-reference, metodika, init data |

## 4. HOOKS (ze settings.json)
| Event | File | Popis |
|-------|------|-------|
| (žádné hooks nalezeny v settings.json) |

## 5. RULES

### Shared rules
| ID | Název | Paths glob |
|----|----|----------|
| RULE-AP-001_antipatterns | RULE-AP-001_antipatterns | (viz soubor) |
| RULE-AP-002_pokryti-ze-zdroje | RULE-AP-002_pokryti-ze-zdroje | (viz soubor) |
| RULE-CL-001_changelog | RULE-CL-001_changelog | (viz soubor) |
| RULE-DIAG-001_diagramy | RULE-DIAG-001_diagramy | (viz soubor) |
| RULE-GOV-001_boundary-promoce | RULE-GOV-001_boundary-promoce | (viz soubor) |
| RULE-GOV-002_brana-ne-prompt | RULE-GOV-002_brana-ne-prompt | (viz soubor) |
| RULE-META-001_metadata-styl | RULE-META-001_metadata-styl | (viz soubor) |
| RULE-ONT-001_novy-prvek-do-registru | RULE-ONT-001_novy-prvek-do-registru | (viz soubor) |
| RULE-ONT-002_cituj-zdroj-ne-registr | RULE-ONT-002_cituj-zdroj-ne-registr | (viz soubor) |
| RULE-ONT-003_zmizela-resi-clovek | RULE-ONT-003_zmizela-resi-clovek | (viz soubor) |
| RULE-SPEC-001_trace-akceptace | RULE-SPEC-001_trace-akceptace | (viz soubor) |
| RULE-SPEC-002_kritik-cizi-vystup | RULE-SPEC-002_kritik-cizi-vystup | (viz soubor) |
| RULE-SPEC-004_model-pred-hromadnou-aplikaci | RULE-SPEC-004_model-pred-hromadnou-aplikaci | (viz soubor) |
| RULE-TC-001_tc-konvence | RULE-TC-001_tc-konvence | (viz soubor) |
| RULE-TERM-001_terminologie | RULE-TERM-001_terminologie | (viz soubor) |

### Personal rules (martint)
| Soubor |
|--------|

## 6. KNOWLEDGE-INBOX
| Autor | Soubor | Datum | Počet kandidátů |
|------|--------|-------|----------------|

## 7. OUTPUT STYLES
| Jméno | Popis |
|-------|-------|
| Feynman CZ | Český, intuitivní výklad |

## 8. PLUGINY (installed_plugins.json)
| Jméno | Verze | InstallPath (zkráceno) |
|-------|--------|----------------------|
| frontend-design@claude-plugins-official | b819188d2eea | ~/.claude/plugins/cache/... |
| knowledge-loop@kvados-plugins | 2.0.0 | ~/.claude/plugins/cache/... |
| ontology-registry@kvados-plugins | 1.0.0 | ~/.claude/plugins/cache/... |
| spec-factory@kvados-plugins | 1.9.0 | ~/.claude/plugins/cache/... |
| superpowers@claude-plugins-official | 6.3.0 | ~/.claude/plugins/cache/... |

## 9. SETTINGS.JSON (klíčové položky)
| Položka | Hodnota |
|---------|--------|
| model | opus[1m] |
| effort | high |
| language | Čeština |
| outputStyle | Feynman CZ |
| worktree.bgIsolation | none |
| statusLine | command (ccstatusline) |
| enabledPlugins | superpowers, knowledge-loop, spec-factory, frontend-design, ontology-registry |
| permissions.allow | 157 pravidel (read, bash, webfetch, websearch, design) |
| permissions.deny | 18 pravidel (git force, rm destructive, format) |
| permissions.additionalDirectories | 7 lokací (tmp, documents, projects, choco) |

## 10. VALIDÁTORY A NÁSTROJE
| Lokace | Nástroje |
|--------|----------|
| .adr-tools | config.yaml, validate.cmd |
| .claude/rules/shared | README.md |
| .fr-tools | validate.py, config.yaml, schema.yaml, validate.cmd |
| .ontology-tools | audit.py, build.cmd, cite.py, reanchor.py, README.md |
| .plc-tools | validate.cmd, plc-lint.py, README.md |
| docs/suppliers/.tools | questions.py, msg_extract.py |

## 11. PLUGINS V C:/Git/shared/plugins/
| Plugin | Verze |
|--------|-------|
| knowledge-loop | 2.0.0 |
| ontology-registry | 1.0.0 |
| spec-factory | 1.9.0 |
