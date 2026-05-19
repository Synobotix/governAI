# STATE.v0.3-overlay-priority-and-output.md

> Feature contract for overlay priority-based conflict resolution and output destination change.

---

## Mission

Add priority-based conflict resolution to overlay compilation and change `governAI install` output destination to `.opencode/opencode.json`.

Priority resolution: when multiple overlays define identical rules/constraints, the overlay with the highest priority wins. Overlay priority is read from the `## Priority` section (HIGH > MEDIUM-HIGH > MEDIUM > LOW). Sort overlays by priority descending before building IR so the existing dedup in `normalize_ir()` naturally keeps the highest-priority version.

Output destination: `governAI install` writes `.opencode/opencode.json` instead of `dist/opencode.json`. The legacy `scripts/compile.py` continues writing to `dist/` unchanged.

## Feature Type

`new feature`

## Change Level

**L3** — structural change (pipeline semantics, output contract, core compiler modification)

## Acceptance Criteria

1. Overlays with PRIORITY=HIGH are processed before MEDIUM-HIGH, before MEDIUM, before LOW
2. When two overlays define the same rule text, the higher-priority overlay's version appears in the output
3. Lower-priority identical rules are silently deduplicated (not duplicated)
4. `governAI install --all -p <path>` writes to `<path>/.opencode/opencode.json`
5. `governAI install <id> -p <path>` writes to `<path>/.opencode/opencode.json`
6. `governAI` (context-aware default) writes to `.opencode/opencode.json`
7. Legacy `python3 scripts/compile.py` still writes to `dist/opencode.json`
8. If `.opencode/` doesn't exist, it is created automatically
9. Existing output file is overwritten (no merge)
10. Priority parsing handles: HIGH, MEDIUM-HIGH, MEDIUM, MEDIUM-LOW, LOW (case-insensitive)
11. Missing priority defaults to MEDIUM

## Allowed Areas

- `scripts/compilers/opencode_compiler.py` — add priority extraction, overlay sorting
- `src/governai/cli.py` — change install output path to `.opencode/`
- `docs/` — document priority behavior and new output path

## Forbidden Areas

- `catalog/index.yaml` format — no changes
- `sources/personas/*` — no edits
- `sources/overlays/*` — no edits
- `scripts/compile.py` — no edits
- `scripts/validate_catalog.py` — no edits
- `scripts/sync_overlays_to_skills.py` — no edits
- `.opencode/` — no edits (output destination, not source)
- `src/governai/` — only cli.py may change

## Public Contract Impact

- **Contract impact**: **yes**
- **Surfaces affected**:
  - Pipeline semantics: overlays are now priority-sorted before compilation
  - Output destination: `.opencode/opencode.json` is the new default output for CLI
  - `dist/` remains as legacy output via `scripts/compile.py`
- **Migration needed**: no (additive change, no existing users)
- **ADR required**: yes (overlay conflict resolution strategy + output contract)

## Required Gates

- `$architect`: yes — overlay sorting strategy, output contract change
- `$adr`: yes — conflict resolution rule and output destination
- `$doc`: yes — document priority behavior and new output path
- `$qa`: yes — behavioral change
- `$review`: yes
- `$release`: yes

Governance: no | Architect-security: no | Security: no

## Blast Radius

- **Classification**: multi-module
- **Reason**: compiler module + CLI + docs. Core compilation logic changes but scope is bounded.

## Parallel / Collision Risk

- **Parallel risk**: none
- **Shared surfaces**: `opencode_compiler.py` (compilation pipeline)

## Architectural Constraints

- Priority sorting happens in `build_ir()` or as a preprocessing step before it
- Existing `compile_overlay()` must extract priority from `## Priority` section
- Priority values map to integers: HIGH=3, MEDIUM-HIGH=2, MEDIUM=1, MEDIUM-LOW=0, LOW=-1
- Unknown or missing priority → MEDIUM (1)
- Dedup logic stays in `normalize_ir()` — no changes needed there
- `scripts/compile.py` stays unchanged (continues writing to `dist/`)
- CLI determines root path, writes to `<root>/.opencode/opencode.json`

## Security Surface Check

- No security concerns. Safe to proceed.

## Execution Plan

1. `$architect`: validate overlay priority sorting approach and output contract change
2. `$adr`: write `docs/governance/adr/0003-overlay-priority-and-output-contract.md`
3. Add priority extraction to `compile_overlay()` in `opencode_compiler.py`
4. Add overlay sorting by priority in `build_ir()` or in a preprocessing step
5. Update CLI `install` command to write to `.opencode/opencode.json`
6. Update docs (README, overlays spec, build pipeline)
7. Validate: compile with multiple overlays, verify priority-based dedup, verify output path

## Drift Conditions

- Adding new priority levels beyond HIGH/MEDIUM-HIGH/MEDIUM/MEDIUM-LOW/LOW
- Changing `scripts/compile.py` output path
- Removing `dist/` output from legacy scripts
- Adding interactive conflict resolution (manual merge) — that's v0.3+ scope

## TODO.md Template

```
T-001: architect + ADR for overlay priority and output contract
T-002: priority extraction in compile_overlay()
T-003: priority-based overlay sorting in build_ir()
T-004: output path change to .opencode/ in CLI
T-005: docs update
T-006: validation
```
