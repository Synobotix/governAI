---
title: Overlay Priority-Based Conflict Resolution and Output Contract
date: 2026-05-19
status: Accepted
supersedes: null
superseded-by: null
---

# ADR 0003: Overlay Priority-Based Conflict Resolution and Output Contract

## Context

Overlays define behavioral modifiers (Rules, Constraints, Output Behavior) that are stacked together during compilation. When multiple overlays define identical rules or constraints, the current implementation simply deduplicates silently, keeping the first occurrence — which depends on catalog listing order.

Two problems:

1. **Non-deterministic conflict resolution**: The winning overlay depends on catalog entry order, not semantic importance. If overlays are reordered in the catalog, the output changes silently.

2. **Output destination**: `governAI install` writes to `dist/opencode.json`, but OpenCode reads from `.opencode/opencode.json`. After install, the user must manually copy or symlink the file.

## Decision

### 1. Priority-based overlay sorting

Each overlay has a `## Priority` section with a text value. Before building the IR, overlays are sorted by priority descending (highest first). The existing dedup in `normalize_ir()` then naturally keeps the highest-priority version of any duplicate rule/constraint.

Priority scale:

| Text | Value | Meaning |
|------|-------|---------|
| HIGH | 3 | Highest authority — overrides all |
| MEDIUM-HIGH | 2 | Higher than default |
| MEDIUM | 1 | Default — normal priority |
| MEDIUM-LOW | 0 | Lower than default |
| LOW | -1 | Lowest — overridden by all |

Missing priority defaults to MEDIUM (1). Case-insensitive parsing.

### 2. Output destination: `.opencode/opencode.json`

`governAI install` writes to `<target>/.opencode/opencode.json`. This is the path OpenCode reads by default, enabling immediate use after install.

- Legacy `python3 scripts/compile.py` remains unchanged (writes to `dist/`)
- `.opencode/` is created automatically if it doesn't exist
- Existing file is overwritten (no merge logic)

### Alternatives considered

- **No sorting** (keep catalog order): Non-deterministic, order-dependent. Rejected.
- **Explicit conflict markers** (like `OVERRIDE` suffix in rules): More complex, harder to maintain. Rejected for v0.3.
- **Write to both `dist/` and `.opencode/`**: Unnecessary — `dist/` was a build artifact, not a runtime path.

## Consequences

### Positive

- Deterministic conflict resolution independent of catalog entry order
- `governAI install` produces immediately usable output
- Simple implementation — sorting + existing dedup
- Backward compatible (all existing overlays default to MEDIUM)

### Negative

- Priority is a coarse mechanism — cannot express "override rule X but keep rule Y from same overlay"
- Output file overwrite means manual changes to `.opencode/opencode.json` are lost on next install

### Neutral

- Priority granularity (5 levels) may need expansion as the overlay ecosystem grows
- `dist/` remains for legacy pipeline users

## Migration

None — purely additive. Existing overlays without priority default to MEDIUM, behavior unchanged.

## Rollback

Pin compiler to previous version. Output path: use `scripts/compile.py` instead of CLI.

## Related ADRs

- ADR 0002: governAI CLI contract (established `-p` path option, reused here)
