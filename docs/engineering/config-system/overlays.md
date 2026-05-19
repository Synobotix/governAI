# Spécification overlay

## Emplacement

`sources/overlays/<nom>.md`

## Rôle

Un overlay est un **modificateur comportemental modulaire** qui ajoute des règles, contraintes ou structure de sortie par-dessus une persona.

Plusieurs overlays peuvent être empilés (appliqués dans l'ordre du catalogue).

## Structure

| Section | Requise | Utilisée par le compilateur | Description |
|---|---|---|---|
| `# Overlay: <nom>` | oui | — | Titre |
| `## Identity` | oui | — | Ce que fait l'overlay |
| `## Intent` | oui | — | Pourquoi il existe |
| `## Rules` | oui | ✅ Extraites comme règles | Comportements que le modèle DOIT suivre |
| `## Constraints` | oui | ✅ Extraites comme contraintes | Comportements que le modèle NE DOIT PAS faire |
| `## Output Behavior` | oui | ✅ Extrait comme format de sortie | Structure de réponse attendue |
| `## Priority` | oui | ❌ Non utilisée | Prévue pour futur système de conflit |
| `## Behavioral Impact` | non | — | Ce que l'overlay modifie |
| `## Compatibility` | non | — | Overlays compatibles |
| `## Observable Effects` | non | — | Comment vérifier l'activation |
| `## Summary` | non | — | Référence rapide |

## Fonctionnement de la compilation

Le compilateur lit chaque overlay avec `compile_overlay()` :

- Trouve les sections `## Rules`, `## Constraints`, `## Output Behavior`
- **Rules / Constraints** : extrait les lignes commençant par `- ` (listes markdown)
- **Output Behavior** : capture le corps complet (titres `####` + prose)
- Ignore les séparateurs `---`
- Fusionne les résultats dans les sections du prompt `=== RULES ===`, `=== CONSTRAINTS ===`, `=== OUTPUT FORMAT ===`

Les overlays ne sont **pas déconflictés** : ils s'empilent séquentiellement.

## Overlays as Skills

Les overlays sont automatiquement synchronisés vers `.opencode/skills/overlays/<name>/SKILL.md`
via `scripts/sync_overlays_to_skills.py`.

Le compilateur ajoute une section `=== AVAILABLE SKILLS ===` dans le prompt listant
les overlays disponibles comme skills, et ajoute un champ `skills` dans la config
JSON de l'agent.

```bash
python3 scripts/sync_overlays_to_skills.py   # sync overlays → skills
python3 scripts/compile.py                   # compile avec skills dans le prompt
```

## Overlays existants

| Fichier | Rôle |
|---|---|
| `diagnostics.md` | Diagnostic systématique, analyse de causes racines |
| `structured-analysis.md` | Décomposition structurée de problèmes |
| `hypothesis-driven.md` | Raisonnement hypothético-déductif |
| `strict-mode.md` | Rigueur élevée, séparation faits/hypothèses |
