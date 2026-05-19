# Pipeline de build

## Pipeline

```
scripts/validate_catalog.py               # validation du catalogue (optionnel)
scripts/sync_overlays_to_skills.py        # synchro overlays → .opencode/skills/overlays/
  ↓
catalog/index.yaml
  → résoudre persona depuis sources/personas/<nom>.md
  → résoudre overlays depuis sources/overlays/<nom>.md
  → construire l'IR (persona + règles + contraintes + sortie)
  → aplatir en chaîne de prompt (inclut sections OUTPUT FORMAT + AVAILABLE SKILLS)
  → ajouter skills à la config agent
  → écrire dist/opencode.json
```

Implémenté dans `scripts/compile.py`, `scripts/validate_catalog.py` et `scripts/sync_overlays_to_skills.py`.

## Étapes

### 1. Chargement du catalogue

Lecture de `catalog/index.yaml`, itération sur les configs activées.

### 2. Résolution des sources

- Persona : chargée depuis `sources/personas/<persona>.md`
- Overlays : chargés depuis `sources/overlays/<overlay>.md` (liste ordonnée)
- Échec du build si un fichier source est manquant

### 3. Compilation de l'IR

`build_ir()` agrège le texte de la persona + les règles/contraintes des overlays (listes) + le corps des sections Output Behavior (titres + prose) en un dictionnaire intermédiaire.

### 4. Aplatissement

`flatten_to_opencode_prompt()` produit une chaîne unique avec sections :

```
SYSTEM PERSONA:
...
=== RULES ===
...
=== CONSTRAINTS ===
...
=== TASK BEHAVIOR ===
...
=== OUTPUT FORMAT ===
...
=== AVAILABLE SKILLS ===
...
```

### 5. Ajout des skills

La config agent reçoit un champ `skills` listant les overlays disponibles comme skills OpenCode.

### 6. Écriture du JSON

Sortie dans `dist/opencode.json` avec id, mode, model, prompt, skills, tools, permissions.

## Pre-build validation

```bash
python3 scripts/validate_catalog.py
```

Vérifie le schéma du catalogue et l'existence des fichiers source.

## Pre-build skill sync

```bash
python3 scripts/sync_overlays_to_skills.py
```

Synchronise les overlays de `sources/overlays/` vers `.opencode/skills/overlays/<name>/SKILL.md`.

## Artefacts de sortie

```
dist/
  opencode.json       # Configuration agent OpenCode

.opencode/skills/overlays/
  <name>/SKILL.md     # Overlays disponibles comme skills
```

## Runtime supporté

Un seul runtime pour l'instant : **OpenCode** (`targets: [{runtime: opencode}]`).
