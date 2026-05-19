# AGENTS.override.md

> Project-specific overrides for SynthKit / governAI.

## Identity

- **Project**: SynthKit (product name: governAI)
- **Description**: Python compilation system transforming modular AI behaviors (personas + overlays) into executable OpenCode agent configurations
- **Stack**: Python 3.11+, PyYAML, click
- **Package name**: `governai`
- **Entry point**: `governAI` CLI command

## Architecture Triggers

- Adding new CLI commands beyond list/create/install/help
- Changing the compilation pipeline signature or behavior
- Modifying the catalog schema or file format
- Adding new runtime export formats beyond OpenCode

## Security Triggers

- Adding network access or remote config fetching
- Adding auth tokens or credential handling
- Adding plugin/connector execution boundaries
- Adding dependency on untrusted third-party packages

## System Invariants

- I-04: Catalog format (catalog/index.yaml) is the authoritative source for agent configs
- I-05: Compilation pipeline produces deterministic output given the same inputs
- I-06: CLI path argument defaults to current directory

## Forbidden Areas

- `.opencode/_constitution.md` — immutable source of truth
- `.opencode/skills/*` — skill definitions, immutable during feature work
- `sources/personas/*`, `sources/overlays/*` — source content, not to be edited during CLI work
- `scripts/compilers/opencode_compiler.py` — import only, no refactoring
- `catalog/index.yaml` format — stable contract
- `docs/governance/constitution.md` — auto-generated mirror

## Runtime Contract

- CLI runs on Python 3.11+
- No network access required
- Single-user, local-only execution
- Output written to `dist/` relative to target path

## Public Contracts

- `governAI [path]` CLI command (v0.2+)
- `catalog/index.yaml` format (stable from v0.1)
- `scripts/compile.py` standalone invocation (stable from v0.1)
