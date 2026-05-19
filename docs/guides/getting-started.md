# Guide de démarrage

## Prérequis

- Python 3.10+
- `pip install pyyaml`

## Structure du projet

```
sources/
  personas/       # profils cognitifs (markdown)
  overlays/       # modificateurs comportementaux (markdown)
catalog/
  index.yaml      # registre de configurations
scripts/
  compile.py                  # build : catalogue → dist/opencode.json
  validate_catalog.py         # validation du schéma catalogue
  sync_overlays_to_skills.py  # synchro overlays → skills
dist/
  opencode.json   # configuration OpenCode générée
```

## Utilisation

### 1. Définir une persona

`sources/personas/<nom>.md` — profil cognitif stable (identité, style de raisonnement, communication).

### 2. Définir des overlays (optionnel)

`sources/overlays/<nom>.md` — comportements modulaires avec sections `## Identity`, `## Intent`, `## Rules`, `## Constraints`, `## Output Behavior`, `## Priority`, et sections optionnelles.

### 3. Enregistrer dans le catalogue

`catalog/index.yaml` :

```yaml
configs:
  - id: mon-agent
    enabled: true
    source:
      persona: system-engineer
      overlays:
        - diagnostics
    model: opencode/deepseek-v4-flash-free
    mode: primary          # primary | subagent
    tools:
      write: true
      edit: true
      bash: true
    targets:
      - runtime: opencode
```

### 4. Valider le catalogue (optionnel)

```bash
python3 scripts/validate_catalog.py
# → ✔ system-engineer-diagnostics: valid
```

### 5. Synchroniser les overlays vers les skills

```bash
python3 scripts/sync_overlays_to_skills.py
# → .opencode/skills/overlays/<nom>/SKILL.md
```

### 6. Compiler

```bash
python3 scripts/compile.py
# → dist/opencode.json (avec sections RULES, CONSTRAINTS, OUTPUT FORMAT,
#                        TASK BEHAVIOR, AVAILABLE SKILLS dans le prompt)
```

### 7. Utiliser dans OpenCode

```bash
opencode --agent mon-agent
```

Ou copier `dist/opencode.json` vers `.opencode/opencode.json`.

## Champs disponibles (catalogue)

| Champ | Requis | Défaut | Description |
|---|---|---|---|
| `id` | oui | — | Identifiant unique en kebab-case |
| `enabled` | oui | — | `true` pour inclure dans le build |
| `source.persona` | oui | — | Référence `sources/personas/<nom>.md` |
| `source.overlays` | non | `[]` | Liste ordonnée, réf. `sources/overlays/<nom>.md` |
| `model` | non | `anthropic/claude-sonnet-4-20250514` | ID du modèle OpenCode |
| `mode` | non | `primary` | `primary` ou `subagent` |
| `tools` | non | `{write, edit, bash}` | Permissions d'outils |
| `permission.task` | non | — | Règles de délégation par glob |
| `task_budget` | non | — | Nombre max d'appels Task |
| `tasks` | non | `[]` | Règles de comportement Task (compilées dans le prompt) |
| `targets` | oui | — | Cibles d'exécution (`opencode`) |

## Ce que l'outil fait

- Compile persona + overlays + règles task en un seul prompt
- Génère un `opencode.json` valide
- Supporte les modes primary et subagent
- Supporte la délégation de tâches avec permissions et budget

## Ce que l'outil ne fait pas (encore)

- Résolution de conflits entre overlays
- Évaluation / benchmarking comportemental
- Exports multi-runtime (Claude, générique)
- Builds incrémentaux

## Runtime supporté

Un seul runtime pour l'instant : **OpenCode**. Le catalogue ne compile que pour `targets: [{runtime: opencode}].
