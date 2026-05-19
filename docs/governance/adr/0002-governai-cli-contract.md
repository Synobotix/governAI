---
title: Define governAI CLI Contract
date: 2026-05-19
status: Accepted
supersedes: null
superseded-by: null
---

# ADR 0002: Define governAI CLI Contract

## Context

SynthKit v0.1 exists as a Python compilation pipeline invoked via `python3 scripts/compile.py`. To make the tool usable as a standalone product, it needs a CLI entry point installable via pip.

Requirements:

- CLI must be context-aware: if `catalog/index.yaml` exists, compile and install; otherwise, guide the user toward creating one
- Subcommands: `list`, `create`, `install <id|--all>`, `help`
- Optional path argument (default `.`)
- Must reuse the existing compilation pipeline as a library, not fork or rewrite it
- Must be installable via `pip install .`

## Decision

### 1. CLI library: click

Use `click` for command parsing, subcommand dispatch, and help generation. It is the de facto standard for Python CLIs, supports composable subcommands, autocomplete, and auto-generated `--help`.

Alternatives considered:

- **argparse**: stdlib, but more boilerplate for nested subcommands, no auto help groups, no autocomplete
- **typer**: built on click, but adds an extra abstraction layer and dependency chain (typer → click → rich → ...) — not justified for 4 commands

### 2. Module structure: single-file CLI

```
src/governai/
├── __init__.py
├── __main__.py
├── _version.py
└── cli.py
```

All commands in one file. 4 subcommands don't warrant module splitting. If the file exceeds ~300 lines in a future version, split at that point.

### 3. Command tree

```
governAI [OPTIONS] COMMAND [ARGS]...
  no subcommand → context-aware:
    catalog/index.yaml exists → install --all
    no catalog                → print message, suggest "governAI create -p <path>"

governAI list -p <path>
governAI create -p <path>
governAI install [--all] [-p <path>] [CONFIG_ID]
governAI --help
```

### 4. Path behavior

- Path is an option (`-p` / `--path`) on every subcommand, not a positional argument
- Path defaults to current directory (`.`)
- Accepted: relative path, absolute path
- All commands resolve paths via `pathlib.Path.resolve()`
- Rationale: positional path conflicts with command dispatch — click interprets the first token as a subcommand name, making `governAI list .` ambiguous

### 5. Compiler integration

Import directly as Python modules:

```python
from scripts.compilers.opencode_compiler import build_ir, normalize_ir, flatten_to_opencode_prompt
from scripts.validate_catalog import validate_catalog
```

No changes to the existing compilation pipeline.

### 6. Wizard (create command)

Minimal interactive mode using `input()` prompts:

1. List available personas from `sources/personas/`
2. Prompt user to select one
3. List available overlays from `sources/overlays/`
4. Prompt user to select (comma-separated)
5. Prompt for config ID
6. Write `catalog/index.yaml`

No TUI libraries. No template system. Upgradable in a later version.

## Consequences

### Positive

- Users can install and use the tool without knowing the internal script structure
- Context-aware default reduces friction for the common case
- Existing compilation pipeline remains untouched and independently usable
- Low maintenance burden (single file, well-known library)

### Negative

- `click` is an additional dependency (though already standard for Python CLI tools)
- Single-file CLI will need splitting if commands grow significantly
- Wizard UX is basic — power users may prefer editing YAML directly

### Neutral

- CLI contract becomes stable from v0.2 onward — future changes must be additive or versioned
- Path argument defaults to `.` — users must specify a path explicitly when operating outside current directory

## Migration

None — purely additive. Existing `scripts/compile.py` usage unchanged.

## Rollback

Uninstall the package: `pip uninstall governai`. Existing catalog and compiler scripts remain intact.

## Related ADRs

- ADR 0001: `(deleted — covered dead field removal)`
