---
name: init-context
description: Initialiser ou mettre a jour PROJECT.md, docs/architecture/* (assumptions, system-boundaries, interfaces, data-flow, deployment, security-architecture, modularity-principles), docs/architecture/c4/*.md (C4 context/container/component/code), et AGENTS.override.md avant implementation. Utiliser quand le depot manque de contexte fiable ou quand un changement impose de re-aligner ces documents.
---

# Role

Tu es le skill `init-context`.

Produire un contexte projet fiable et exploitable pour les autres skills.
Ne pas ecrire de code de production.

# Scope

Couvrir tous les documents de contexte du projet:

## context/
- `context/product_context.md` (identité, utilisateurs, problème, valeur, scope)
- `context/technical_context.md` (langage, stack, tests, storage)
- `context/constraints.md` (contraintes fonctionnelles, sécurité, compliance)
- `context/ai/model_context.md` (provider, modèle, capabilities)
- `context/ai/prompt_context.md` (architecture prompts, conventions)
- `context/ai/agent_context.md` (agents, outils, memory)
- `context/ai/safety_context.md` (sécurité IA, trust boundaries)

## PROJECT.md
- `PROJECT.md` (source de vérité courte, identité, objectifs, architecture, stack)

## docs/architecture/
- `docs/architecture/overview.md` (architecture système)
- `docs/architecture/assumptions.md` (hypothèses)
- `docs/architecture/system-boundaries.md` (périmètre, trust boundaries)
- `docs/architecture/interfaces.md` (API, NLSpec, MCP, external APIs)
- `docs/architecture/data-flow.md` (flux de données)
- `docs/architecture/deployment.md` (modèle de déploiement)
- `docs/architecture/security-architecture.md` (sécurité, PII, GDPR)
- `docs/architecture/modularity-principles.md` (couplage, invariants, Sentrux)
- `docs/architecture/c4/*.md` (C4 models: context, containers, components with Mermaid)

## Configuration
- `AGENTS.md`
- `AGENTS.override.md`

# MemPalace Integration

Ce skill utilise **Mempalace** (MCP servers `mempalace-global` et `mempalace-local`) pour:

- **Mempalace Global** : Récupérer les patterns historiques, erreurs passées, leçons apprises d'autres projets
- **Mempalace Local** : Consulter l'historique du projet, les décisions passées, le contexte architecturel

### Usage
- Avant de créer `AGENTS.override.md` : interroger Mempalace Global pour les bonnes pratiques
- Lors de la création : stocke les nouvelles décisions dans Mempalace Local
- Utilise `mempalace-global` pour cross-référencement des patterns de documentation

# Workflow

1. Inspecter le depot et les fichiers cibles existants (`context/*`, `PROJECT.md`, `docs/architecture/*`, `docs/architecture/c4/*.md`).
2. **Interroger Mempalace** (Global + Local) pour récupérer le contexte historique.
3. Identifier les trous de contexte et les incoherences.
4. Interviewer l'utilisateur par blocs courts:
   - Identite produit (pour context/product_context.md, PROJECT.md sections 1-6)
   - Stack technique (pour context/technical_context.md, PROJECT.md section 14, docs/architecture/*)
   - Architecture (pour context/ai/*, PROJECT.md sections 13, docs/architecture/overview.md)
   - Contraintes (pour context/constraints.md, PROJECT.md section 9, docs/architecture/security-architecture.md)
   - IA (si applicable) (pour context/ai/*, PROJECT.md section 20)
   - Informations pour AGENTS.override.md (identite projet, stack, architecture, contraintes specifiques)
5. Marquer explicitement `not defined` pour toute information inconnue.
6. Resumer les informations collectees et demander approbation explicite.
7. Apres approbation:
   - Remplir `context/*` (tous placeholders `<...>` et `<!-- FILL -->`)
   - Remplir `PROJECT.md` (tous placeholders `<...>` et `<!-- FILL -->`)
   - Ecrire ou mettre a jour `docs/architecture/*.md` (overview, assumptions, system-boundaries, interfaces, data-flow, deployment, security-architecture, modularity-principles)
   - Creer ou mettre a jour `docs/architecture/c4/*.md` (C4 models: context.mmd, containers.md, components.md with Mermaid diagrams)
   - Creer ou mettre a jour `AGENTS.override.md` avec les informations fournies par l'utilisateur.
   - Stocker les nouvelles décisions dans **Mempalace Local**.
8. Verifier coherence croisee entre context/*, PROJECT.md, docs/architecture/* et docs/architecture/c4/*.
9. Rapporter les fichiers modifies et les points restant `not defined`.

# Interview Rules

- Poser 3 a 5 questions maximum par bloc.
- Adapter les questions selon les reponses.
- Ne jamais inventer d'information.
- Si le projet n'utilise pas l'IA, remplir `context/ai/*` et les sections IA de `PROJECT.md` avec `Not applicable - project does not use AI.`
- Rester concis et specifique.

# Writing Rules

- Decrire l'etat reel du projet, pas une intention future.
- Conserver la structure de `context/*`, `PROJECT.md` et `docs/architecture/*.md`.
- **Creer les dossiers s'ils n'existent pas** avant d'ecrire les fichiers (ex: `mkdir -p docs/architecture/c4/`).
- Remplacer seulement les placeholders (`<...>`, `<!-- FILL -->`) ou sections attendues.
- Utiliser des tableaux pour contrats, interfaces, assumptions, risques.
- Utiliser ASCII pour les vues d'architecture (ex: data-flow.md).
- Utiliser Mermaid pour les diagrammes C4 (`docs/architecture/c4/*.md`).
- Garder des noms coherence (modules, traits, APIs) dans context/*, PROJECT.md et docs/architecture/*.
- Creer ou mettre a jour `AGENTS.override.md` avec les informations fournies par l'utilisateur.

# Quality Gate

Verifier obligatoirement:
- coherence des noms entre `context/*`, `PROJECT.md` et `docs/architecture/interfaces.md`, `system-boundaries.md`, `modularity-principles.md`
- alignement `PROJECT.md` (section 9: Contraintes) -> `context/constraints.md` + `docs/architecture/data-flow.md`/`security-architecture.md`
- alignement `PROJECT.md` (section 14: Stack) -> `context/technical_context.md` + `docs/architecture/deployment.md`
- alignement `context/product_context.md` -> `PROJECT.md` (sections 1-8, 12-13)
- absence de texte generique non actionnable dans `context/*`, `PROJECT.md`, `docs/architecture/*.md` et `docs/architecture/c4/*.md`
- contenu Mermaid propre dans `docs/architecture/c4/*.md` (context, containers, components)
- contenu ASCII propre dans `docs/architecture/data-flow.md`

Rapporter en sortie:
```text
INIT_CONTEXT_REPORT:
  approval_received: yes/no
  files_updated: <list>
  cross_reference_consistent: yes/no
  alignment_consistent: yes/no
  unresolved_not_defined: <list or none>
```

# Hard Prohibitions

- Ne pas coder en production.
- Ne pas toucher `.opencode/_*.md`.
- Ne pas modifier le perimetre hors documentation de contexte.
- Ne pas remplir sans approbation utilisateur explicite.
- Ne pas contredire les informations deja confirmees.