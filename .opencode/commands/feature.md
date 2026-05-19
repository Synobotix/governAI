Tu reçois une demande de feature. Tu dois exécuter le flux complet, skill par skill, dans l'ordre strict.

## Requête

$ARGUMENTS

## Contexte Projet
- Lis `AGENTS.md` et `AGENTS.override.md` pour les configurations du dépôt et les informations spécifiques au projet. Les informations de `AGENTS.override.md` complètent et surchargent si besoin les configurations de `AGENTS.md`.
- **Mempalace Global** (`~/.mempalace/`) : Consulte les patterns historiques, erreurs passées, leçons d'autres projets via MCP `mempalace-global`.
- **Mempalace Local** (`.mempalace/` dans le repo) : Consulte l'historique du projet, les décisions passées, le contexte architecturel via MCP `mempalace-local`.
- **Sentrux** : Qualité architecturale, métriques de code, détection de dette via MCP `sentrux`.

## Flux à suivre

Exécute chaque étape séquentiellement. À chaque étape, lis le SKILL.md correspondant, exécute-le, puis passe à l'étape suivante uniquement si le résultat le permet.

### Étape 0 — Mémoire de session
Lis `MEMORY.md` avant toute autre action.
- Reprends uniquement les informations inter-sessions encore vraies.
- Si le contenu est obsolète ou contradictoire avec l'état réel du dépôt, nettoie `MEMORY.md` avant de continuer.

### Étape 1 — Triage
Lis `.opencode/skills/triage/SKILL.md` puis exécute le skill triage sur la requête ci-dessus.
- Si le statut est `ESCALATE_GOVERNANCE` → lis `.opencode/skills/governance/SKILL.md` et exécute governance d'abord, puis reprends triage.
- Si le triage identifie un flux structurel → ajoute les étapes architect + adr avant preflight.
- Si le triage identifie un flux sécurité → ajoute les étapes architect-security + adr avant preflight.
- Note le niveau (L1/L2/L3) et les portes requises pour la suite.
- Puis lis `.opencode/skills/skeptic/SKILL.md` et exécute skeptic sur le résultat du triage. Suggere des corrections si nécessaire.

### Étape 2 — Spécification (NLSpec)
Lis `.opencode/skills/nlspec/SKILL.md` puis exécute le skill nlspec.
- **Si L1 (fonctionnalité mineure)** : Identifie le fichier de spécification (NLSpec) existant le plus cohérent avec la demande (dans `specs/`) et édite-le pour couvrir la nouvelle fonctionnalité.
- **Si L2 ou L3 (fonctionnalité complexe)** : Crée une nouvelle spécification dédiée dans `specs/`.
- **Mempalace Global** : Consulte les patterns NLSpec existants et les leçons passées d'autres projets.
- **Mempalace Local** : Vérifie l'historique des spécifications du projet.
- Cette étape doit être complétée avant la génération de tests et le planning.
- Puis lis `.opencode/skills/skeptic/SKILL.md` et exécute skeptic sur le résultat du nlspec. Suggere des corrections si nécessaire.

### Étape 3 — Génération de Tests (TDD)
Lis `.opencode/skills/test-gen/SKILL.md` puis exécute le skill test-gen.
- Génère les tests unitaires, d'intégration, E2E et de mutation basés sur les NLSpec dans `specs/`.
- **Mempalace Global** : Récupère les patterns de tests historiques et les erreurs courantes d'autres projets.
- **Mempalace Local** : Consulte l'historique des tests du projet.
- Soumet la proposition de tests à `.opencode/skills/skeptic/SKILL.md` pour validation.
- Itère avec skeptic jusqu'à obtention du statut `SATISFIED`.
- Écrit les fichiers de tests finaux et committe (phase rouge TDD).
- Les tests doivent couvrir :
  - Modèles de domaine (Company, Lead, ICP, etc.)
  - Règles métier (ICP, routing, deliverabilité, compliance)
  - Composants runtime (agents, workflow, event bus)
  - Flux de bout en bout (prospection complète)
  - Modes d'échec et taxonomie d'erreurs
  - Frontières de sécurité et de confiance.
- Cette étape est obligatoire et doit précéder le planning et le codage (approche TDD).

### Étape 4 — Planner
Lis `.opencode/skills/planner/SKILL.md` puis exécute le skill planner.
- **Mempalace Global** : Consulte les patterns de planification et les décisions architecturales passées d'autres projets.
- **Mempalace Local** : Stocke les nouvelles décisions et le plan dans le contexte projet.
- Produits `STATE.<slug>.md`, `TODO.<slug>.md`, `DECISIONS.<slug>.md`.
- Si le worktree n'existe pas encore, lis `.opencode/skills/worktree/SKILL.md` et crée-le d'abord.
- Puis lis `.opencode/skills/skeptic/SKILL.md` et exécute skeptic sur le résultat du planner. Suggere des corrections si nécessaire.

### Étape 5 — Portes amont (si requises par triage)
Si le triage a identifié des portes architect, architect-security, security, ou adr comme requises :
- Lis et exécute chaque skill requis dans l'ordre : architect → architect-security → security → adr.
- Après chaque skill : lis `.opencode/skills/skeptic/SKILL.md` et exécute skeptic sur le résultat. Suggere des corrections si nécessaire.
- Ne passe à l'étape suivante que si toutes les portes requises sont satisfaites.

### Étape 6 — Preflight
Lis `.opencode/skills/preflight/SKILL.md` puis exécute le skill preflight.
- La vérification de `AGENTS.override.md` et du dossier `specs/` s'effectue ici.
- **Sentrux** : Vérifie la qualité architecturale avant de commencer (scan initial, baseline).
- Si `BLOCKED` → corrige les blockers identifiés et relance preflight.
- Ne passe à coder que sur `PASS`.
- Puis lis `.opencode/skills/skeptic/SKILL.md` et exécute skeptic sur le résultat du preflight. Suggere des corrections si nécessaire.

### Étape 7 — Coder (boucle)
Lis `.opencode/skills/coder/SKILL.md` puis exécute le skill coder.
- **Mempalace Local** : Stocke les décisions d'implémentation et les choix locaux.
- **Mempalace Global** : Consulte les patterns d'implémentation d'autres projets.
- **Sentrux** : Utilise `session_start()` avant et `session_end()` après pour détecter la dégradation.
- Exécute une tâche à la fois depuis `TODO.<slug>.md`.
- Valide localement, commit immédiatement (1 tâche = 1 commit).
- Répète jusqu'à ce que toutes les tâches du TODO soient terminées.
- Si dérive détectée → STOP → retour à l'étape 3 (planner).
- Puis lis `.opencode/skills/skeptic/SKILL.md` et exécute skeptic sur le résultat du coder. Suggere des corrections si nécessaire.

### Étape 8 — Synchronisation NLSpec
Lis `.opencode/skills/nlspec/SKILL.md` puis exécute le skill nlspec.
- Compare l'implémentation de code actuelle avec les fichiers NLSpec dans `specs/` :
  - Vérifie si de nouvelles fonctions, classes ou modules ont été ajoutés.
  - Vérifie si les interfaces publiques (API, CLI, config) ont changé.
  - Vérifie si les comportements décrits dans les NLSpec sont toujours exacts.
  - Vérifie si les modèles de données ou schémas ont évolué.
- **Mempalace Local** : Met à jour l'historique des spécifications.
- Si le code a évolué par rapport aux spécifications :
  - **Si L1** : Met à jour le fichier NLSpec existant le plus cohérent.
  - **Si L2 ou L3** : Crée ou met à jour la spécification dédiée dans `specs/`.
- Si la synchronisation échoue ou révèle une divergence majeure :
  - `BLOCKED` → retour à l'étape 3 (planner) pour corriger le planning ou les spécifications.
- Cette étape garantit que les NLSpec restent la source de vérité synchronisée avec le code.
- Puis lis `.opencode/skills/skeptic/SKILL.md` et exécute skeptic sur le résultat de la synchronisation. Suggere des corrections si nécessaire.

### Étape 9 — QA
Lis `.opencode/skills/qa/SKILL.md` puis exécute le skill qa.
- **Sentrux** : Vérifie la qualité architecturale (scan, health, check_rules, session_end).
- **Mempalace Global** : Compare avec les patterns de validation d'autres projets.
- **Mempalace Local** : Consulte l'historique des validations du projet.
- Si `FAIL` → retour à l'étape 6 (coder) pour corriger, puis relance QA.
- Puis lis `.opencode/skills/skeptic/SKILL.md` et exécute skeptic sur le résultat du qa. Suggere des corrections si nécessaire.

### Étape 10 — Review
Lis `.opencode/skills/review/SKILL.md` puis exécute le skill review.
- **Mempalace Global** : Consulte les patterns de review d'autres projets.
- Si `CHANGES_REQUESTED` → retour à l'étape 6 (coder) pour corriger, puis relance QA + review.
- Puis lis `.opencode/skills/skeptic/SKILL.md` et exécute skeptic sur le résultat du review. Suggere des corrections si nécessaire.

### Étape 11 — Doc (si requis)
Si le triage ou le STATE indique que la documentation est requise :
- Lis `.opencode/skills/doc/SKILL.md` puis exécute le skill doc.
- Puis lis `.opencode/skills/skeptic/SKILL.md` et exécute skeptic sur le résultat du doc. Suggere des corrections si nécessaire.

### Étape 12 — Release
Lis `.opencode/skills/release/SKILL.md` puis exécute le skill release.
- Déclare `MERGE_READY` ou `RELEASE_READY` uniquement si toutes les portes sont satisfaites.
- Puis lis `.opencode/skills/skeptic/SKILL.md` et exécute skeptic sur le résultat du release. Suggere des corrections si nécessaire.

## Règles d'orchestration

- Maintiens `MEMORY.md` à jour pendant le flux, pas seulement en lecture.
- Après planner, renseigne ou corrige au minimum : feature active, branche/worktree, tâche courante et statut des portes connues.
- À chaque changement d'état significatif, mets à jour `MEMORY.md` : transition de porte, nouveau blocker, blocker résolu, tâche courante, contexte de reprise.
- En fin de flux ou avant toute interruption, écris le contexte de reprise dans `MEMORY.md`, puis supprime les entrées devenues fausses.
- À chaque transition de skill, affiche un résumé court du résultat et de l'étape suivante.
- Si un skill retourne BLOCKED ou FAIL, ne saute jamais l'étape — résous ou escalade.
- Si le flux doit s'interrompre (besoin d'input utilisateur, décision ambiguë), demande explicitement avant de continuer.
- Si le flux est terminé, nettoie `MEMORY.md` pour ne laisser aucun état actif faux ou périmé.
- **Mempalace** : Utilise systématiquement le dual (Global pour cross-projet, Local pour le contexte précis).
- **Sentrux** : Utilise comme garde-fou architecturale à chaque étape critique (preflight, coder, qa).
