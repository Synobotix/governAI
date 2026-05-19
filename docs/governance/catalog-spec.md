# Spécification du catalogue

## Emplacement

`catalog/index.yaml` — source unique de vérité pour toutes les configurations d'agents.

## Schéma

```yaml
configs:
  - id: string            # unique, kebab-case
    enabled: boolean
    source:
      persona: string     # référence sources/personas/<nom>.md
      overlays:           # ordonné, référence sources/overlays/<nom>.md
        - string
    model: string         # ID du modèle OpenCode
    mode: string          # "primary" | "subagent"
    tools:
      write: boolean
      edit: boolean
      bash: boolean
      task: boolean
    permission:
      task:
        "*": "allow" | "deny"
    task_budget: int
    tasks:                # compilé dans la section === TASK BEHAVIOR ===
      - string
    targets:
      - runtime: string   # actuellement seulement "opencode"
```

## Champs supportés

| Champ | Requis | Défaut | Description |
|---|---|---|---|
| `id` | oui | — | Identifiant unique |
| `enabled` | oui | — | `true` pour inclure dans le build |
| `source.persona` | oui | — | Référence fichier persona |
| `source.overlays` | non | `[]` | Références fichiers overlay |
| `model` | non | `anthropic/claude-sonnet-4-20250514` | ID du modèle LLM |
| `mode` | non | `primary` | Mode de l'agent |
| `tools` | non | `{write, edit, bash}` | Permissions d'outils |
| `permission.task` | non | — | Permission de délégation |
| `task_budget` | non | — | Nombre max d'appels task |
| `tasks` | non | `[]` | Règles de comportement task |
| `targets` | oui | — | Cibles d'exécution |

## Validation

- `id` doit être présent
- `source.persona` doit référencer un fichier existant
- `source.overlays` doivent référencer des fichiers existants
- `mode` doit être `primary` ou `subagent`
- `targets` doit contenir au moins une entrée
- Runtime supporté : `opencode` uniquement
- Les champs `behavior`, `constraints`, `output` ne sont pas supportés (supprimés en v0.2)

Un validateur automatique est disponible :

```bash
python3 scripts/validate_catalog.py
```
