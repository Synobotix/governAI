# Système de configuration

Trois primitives :

- **Personas** → `sources/personas/<nom>.md` — socle cognitif stable
- **Overlays** → `sources/overlays/<nom>.md` — modificateurs comportementaux modulaires
- **Configs** → `catalog/index.yaml` — compositions exécutables

## Flux de données

```
Persona (comportement de base)
  + Overlays (règles, contraintes, sortie)
  → Section "SYSTEM PERSONA" du prompt
  → Section "=== RULES ===" du prompt
  → Section "=== CONSTRAINTS ===" du prompt
  → Section "=== TASK BEHAVIOR ===" du prompt
  → Section "=== OUTPUT FORMAT ===" du prompt
  → dist/opencode.json
```

Le compilateur concatène persona + overlays + règles task en un seul prompt système. Pas de résolution de conflit — les overlays sont empilés dans l'ordre du catalogue.

## Runtime

Un seul runtime supporté : **OpenCode**.
