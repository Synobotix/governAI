# Configuration Composition System

## Overview

The Configuration Composition System defines how **Personas and Overlays are combined into executable AI agents**.

It acts as the **core assembly layer** of the entire configuration pipeline.

Its role is to transform abstract definitions into a **deterministic, runtime-ready agent specification**.

---

## Core Idea

A configuration is not a prompt.

It is the result of a **composition process**:

```text id="composition-core"
Persona + Overlays → Composed Agent → Runtime Export
```

---

## Composition Model

The system follows a strict layered evaluation order:

### 1. Persona Layer (Base)

Defines the default cognitive behavior.

- reasoning style
- communication style
- structural tendencies

### 2. Overlay Layer (Modifiers)

Applies behavioral transformations on top of the persona.

- add constraints
- modify reasoning flow
- enforce output structure
- adjust cognitive patterns

Overlays are stacked sequentially in catalog order.

### 3. Output Layer (Runtime Form)

Final composed configuration ready for export.

Targets:

OpenCode-compatible format

---

## Composition Rules
### 1. Determinism

Same input MUST always produce the same output.

No stochastic behavior allowed in composition.

### 2. Sequential Stacking

Overlays are applied in the order they appear in the catalog entry.

No conflict resolution is performed — overlays are concatenated.

### 3. Atomic Composition

Each overlay contributes a single behavioral transformation.

No overlapping responsibilities.

---

## Composition Pipeline

1. Load Config (catalog entry)
2. Resolve Persona
3. Load Overlays
4. Compile overlays via `compile_overlay()` (extracts Rules, Constraints, Output behavior)
5. Build IR via `build_ir()` (concatenates persona text + overlay lists)
6. Normalize IR via `normalize_ir()` (deduplicates lists)
7. Flatten to prompt string via `flatten_to_opencode_prompt()`
8. Write `dist/opencode.json`

## Validation Requirements

Before a configuration is considered valid:

- Persona file must exist (implicit: `FileNotFoundError` on load)
- All overlay files must exist (implicit: `FileNotFoundError` on load)
- Catalog entry must have `id`, `source.persona`, and `targets`
- Output must match OpenCode runtime schema

---

## Failure Modes

A composition fails if:

- A persona file is missing or invalid
- An overlay file is missing
- A required catalog field is absent

---

## Design Principles

### 1. Deterministic Assembly

Composition is a pure function:

```
input → compile.py → output
```

### 2. No Hidden Logic

All behavior must be explicitly defined in:

- persona
- overlays

No implicit transformations allowed.

### 3. OpenCode-Only Output

The compiler produces OpenCode-specific JSON (`dist/opencode.json`).

Other runtime formats (Claude, generic) are not currently supported.

---

### Example Flow

```
Persona: system-engineer
Overlays: diagnostics + strict-mode

↓

Step 1: load persona file
Step 2: load overlay files
Step 3: compile_overlay() for each overlay
Step 4: build_ir() → concatenate all rules/constraints
Step 5: normalize_ir() → deduplicate
Step 6: flatten_to_opencode_prompt() → string
Step 7: write dist/opencode.json
Output: valid OpenCode agent config
```

The output of composition is a fully resolved OpenCode agent specification (`dist/opencode.json`).

---

## Future (v0.3+)

Conflict resolution is planned but not yet implemented:

- Priority-based overlay resolution
- Constraint conflict detection
- Strictness rules for ambiguous cases

When available, overlays will define priority levels and conflict resolution rules.

---

## Related Sections

- [Personas](./personas.md)
- [Overlays](./overlays.md)
- [Catalog Specification](../../governance/catalog-spec.md)
- [Build Pipeline](../build-system/build-pipeline.md)

## Summary

The Composition System is the core deterministic engine that transforms modular behavioral definitions into executable OpenCode agents.

It ensures:

- reproducibility
- consistency