# Spécification persona

## Emplacement

`sources/personas/<nom>.md`

## Rôle

Une persona définit le **socle cognitif stable** d'un agent IA : style de raisonnement, communication, forces et faiblesses.

Ce n'est PAS une instruction de tâche. C'est la couche de base que les overlays viennent modifier.

## Structure

| Section | Requise | Description |
|---|---|---|
| `# Persona: <nom>` | oui | Ligne de titre |
| `## Identity` | oui | Ce qu'est la persona |
| `## Cognitive Profile` | oui | Comment elle pense |
| `## Communication Style` | oui | Comment elle s'exprime |
| `## Default Reasoning Behavior` | oui | Stratégie de raisonnement par défaut |
| `## Strengths` | non | Ce qu'elle fait bien |
| `## Weaknesses / Tradeoffs` | non | Limitations connues |
| `## Operating Principles` | non | Valeurs fondamentales |
| `## Decision Heuristics` | non | Démarche pas à pas |
| `## Default Output Tendencies` | non | Forme de réponse typique |
| `## Summary` | non | Référence rapide |

## Règles

- Une persona par fichier
- La persona définit l'identité, pas la tâche
- Stable dans le temps (change rarement)
- Indépendante des overlays et des runtimes

## Personas existantes

| Fichier | Domaine |
|---|---|
| `system-engineer.md` | Systèmes, architecture, diagnostic, fiabilité |
