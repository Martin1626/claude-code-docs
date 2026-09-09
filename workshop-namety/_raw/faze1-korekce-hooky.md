# Korekce inventáře — hooky a nastavení (ověřeno hlavní session)

Fáze 1 nahlásila **0 hooků**. To je nesprávné: hooky nejsou jen v `settings.json`, ale hlavně
v pluginech (`<plugin>/hooks/hooks.json`), a ty se do session načtou taky. Doklad, že aspoň
jeden fakticky běží: knowledge-loop SessionStart hook dodal na startu této session handle
`martint` a obsah znalostního inboxu.

## Reálně aktivní hooky (4)

| Event | Matcher | Co spouští | Zdroj | Co to dělá |
|---|---|---|---|---|
| `SessionStart` | `startup\|clear` | `hooks/session-context.py` | `C:/Git/shared/plugins/knowledge-loop/hooks/hooks.json` | Dodá do session handle autora + obsah jeho knowledge-inboxu za 14 dní; generuje gitignored zrcadlo `.claude/rules/personal/` |
| `PreToolUse` | `Write\|Edit\|NotebookEdit` | `hooks/spec-guard.py` | `C:/Git/shared/plugins/spec-factory/hooks/hooks.json` | Blokuje zápis spec-agentů mimo workspace; governance zóny jsou PROTECT pro automatické agenty |
| `SessionStart` | `startup\|clear` | `docs/ontology/.ontology-tools/session-check.py` | `C:/Git/alzask/.claude/settings.json` | Warning-only kontrola, jestli jsou deriváty ontologie a kotvy citací aktuální |
| `PreToolUse` | `Write\|Edit\|NotebookEdit` | `.claude/hooks/spec-guard.py` | `C:/Git/fhb/.claude/settings.json` | Totéž jako spec-factory guard, ale projektová kopie (starší způsob — v alzask už je nahrazený pluginem) |

**Pozorování pro katalog:** ve fhb je guard nasazený jako projektový hook, v alzask jako
pluginový. Tentýž mechanismus ve dvou vrstvách — doklad, že cesta „nejdřív si to postav
v projektu, pak to povyš do pluginu" je reálná, ne teoretická.

**Použité eventy: 2 ze cca 8** (`SessionStart`, `PreToolUse`). Nepoužívám `PostToolUse`,
`UserPromptSubmit`, `Stop`, `SubagentStop`, `PreCompact`, `Notification` — zejména
`PreCompact` je nápadná mezera při 51 kompaktacích v pracovních projektech.

## Klíčové nastavení (`~/.claude/settings.json`)

| Klíč | Hodnota | Poznámka pro workshop |
|---|---|---|
| `model` | `opus[1m]` | Nejsilnější model s 1M kontextovým oknem jako výchozí |
| `effortLevel` | `high` | Reasoning effort natrvalo vysoký; `/effort` jen 4× v pracovních projektech |
| `outputStyle` | `Feynman CZ` | Vlastní output style — čeština, tykání, vysvětlování od podstaty |
| `language` | `Čeština` | |
| `permissions` | 154 allow / 28 deny / 0 ask, `defaultMode: auto` | 154 ručně odklikaných povolení je doklad, že allowlist se buduje postupně |
| `worktree` | `bgIsolation: none` | Background joby pracují v working tree, ne v izolovaném worktree |
| `statusLine` | `node <dist>/ccstatusline.js`, `refreshInterval` | Volá se node přímo, ne přes `npx` — viz paměť o statusline leaku |
| `enabledPlugins` | superpowers, knowledge-loop, spec-factory, frontend-design + další | Mix oficiálních a vlastních |
| `extraKnownMarketplaces` | `kvados-plugins` → GitLab | Vlastní marketplace jako git repozitář |
| `skipDangerousModePermissionPrompt`, `skipAutoPermissionPrompt` | `true` | |

## Projektová nastavení (alzask i fhb, identická)

`permissions.deny`: `Bash(rm *)`, `Bash(git push*)`, `Bash(git reset --hard*)`

Tři zákazy na úrovni projektu jsou mechanická pojistka proti tomu, aby agent smazal soubory,
pushnul nebo zahodil rozpracovanou práci. To je přenositelná zásada v čisté podobě: nebezpečná
operace se nezakazuje větou v `CLAUDE.md`, ale položkou v `deny`.
