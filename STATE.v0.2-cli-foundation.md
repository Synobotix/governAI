# STATE.v0.2-cli-foundation.md

> Feature contract for building the `governAI` CLI tool.

---

## Mission

Build the `governAI` CLI tool — a pip-installable Python entry point that wraps the existing compilation pipeline with a context-aware interface. Default behavior: if `catalog/index.yaml` exists in target path, run install; otherwise, launch a creation wizard. Provide explicit subcommands `list`, `create`, `install <id|--all>`, and `help`.

Success = a user can `pip install governai` then run `governAI .` and get a working OpenCode config.

## Feature Type

`new feature`

## Change Level

**L3** — structural change (new public CLI contract, module boundary, external dependency)

## Acceptance Criteria

1. `governAI` in dir with `catalog/index.yaml` → runs `install --all` flow (compiles and writes `dist/opencode.json`)
2. `governAI` without `catalog/index.yaml` → prints message explaining no catalog found, suggests `governAI create -p <path>`
3. `governAI list -p <path>` reads `catalog/index.yaml` and prints all config IDs with their enabled status
4. `governAI list -p <path>` without catalog → prints clear error message
5. `governAI install -p <path> <config_id>` compiles and writes config for that specific ID
6. `governAI install --all -p <path>` compiles all enabled configs
7. `governAI create -p <path>` launches interactive wizard (baseline: prompts for persona selection, overlay selection, writes `catalog/index.yaml`)
8. `governAI --help` prints usage text
9. Path defaults to current directory (`.`) if `-p` omitted
10. All commands produce non-zero exit code on error, zero on success
11. Existing `scripts/compile.py` still works unchanged

## Allowed Areas

- `pyproject.toml` — add `[project.scripts]` entry point, dependencies
- `src/governai/` — new package
  - `cli/` — CLI command handlers
  - `__init__.py`
  - `__main__.py`
- `docs/` — CLI docs
- `README.md` — update with CLI usage

## Forbidden Areas

- `catalog/index.yaml` format — must not change
- `sources/personas/*` — no edits
- `sources/overlays/*` — no edits
- `.opencode/skills/*` — no edits
- `scripts/compilers/opencode_compiler.py` — import as library, no refactoring
- `scripts/validate_catalog.py` — import as library, no refactoring
- `scripts/sync_overlays_to_skills.py` — no edits
- `scripts/compile.py` — no edits (but may be restructured in later phase if needed)
- `.opencode/` — no edits
- `docs/governance/` — no edits (ADR is separate)
- `dist/` — generated output

## Public Contract Impact

- **Contract impact**: **yes**
- **Surfaces affected**:
  - CLI: new `governAI` command is a public contract
  - CLI usage and flags become stable once v0.2 ships
- **Migration needed**: no (additive)
- **ADR required**: yes (CLI contract design decisions)

## Required Gates

- `$architect`: yes — design CLI tree, module structure, command dispatch
- `$adr`: yes — record CLI contract decisions (entry point, subcommands, flag conventions)
- `$doc`: yes — CLI usage in README, maybe man page or --help
- `$qa`: yes — behavioral change, commands must work
- `$review`: yes
- `$release`: yes

Governance: no | Architect-security: no | Security: no

## Blast Radius

- **Classification**: multi-module
- **Reason**: new `src/governai/` package + `pyproject.toml` changes + docs. Compilation backend untouched. CLI is additive and doesn't modify existing behavior.

## Parallel / Collision Risk

- **Parallel risk**: none
- **Shared surfaces**: `catalog/index.yaml` read-only (no write conflict)
- **Escalation needed**: no

## Architectural Constraints

- CLI must use the existing compilation pipeline as a library, not modify it
- `scripts/compile.py` must remain runnable as-is
- CLI must be installable via `pip install .`
- Python packaging via `pyproject.toml` (setuptools or hatchling)
- Dependency choice: `click` recommended (battle-tested, composable subcommands, autocomplete support); `argparse` acceptable fallback

## Security Surface Check

- No auth, secrets, network, untrusted input parsing beyond file paths
- No new dependencies with meaningful security risk
- Safe to proceed without $security gate

## Execution Plan

1. `$architect`: design CLI module structure and command tree → produce decision in ADR
2. `$adr`: write `docs/governance/adr/0002-governai-cli-contract.md`
3. Update `pyproject.toml` with entry point and dependencies
4. Create `src/governai/__init__.py`, `__main__.py`, `cli/__init__.py`
5. Implement `help` command (default output)
6. Implement `list` command (read catalog, display configs)
7. Implement `install` command (compile single or all configs)
8. Implement context-aware default (no subcommand → detect catalog → install or suggest create)
9. Implement `create` command (baseline wizard: prompt persona + overlays, write catalog)
10. Add path argument handling to all commands (default `.`)
11. Update `README.md` with installation and CLI usage
12. Validate: `pip install -e .` then run all acceptance criteria manually

## Drift Conditions

- Adding new commands beyond list/create/install/help
- Modifying catalog format or schema
- Refactoring compiler internals
- Adding network access or auth
- Expanding wizard beyond baseline (rich TUI, templates, etc.)
- Changing scripts/compile.py signature or behavior

## TODO.md Template

```
T-001: architect design + ADR writing for CLI contract
T-002: pyproject.toml entry point setup
T-003: src/governai package skeleton
T-004: help command
T-005: list command
T-006: install command (single + --all)
T-007: context-aware default behavior
T-008: create command baseline
T-009: README + docs update
T-010: manual validation
```
