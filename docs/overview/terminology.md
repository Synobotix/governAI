# Terminologie

## Concepts

| Term | Definition |
|---|---|
| **Persona** | Stable cognitive baseline. Defines identity, reasoning style, communication preferences, strengths, and weaknesses. Stored in `sources/personas/<name>.md`. |
| **Overlay** | Modular behavioral modifier. Adds rules, constraints, or output structure on top of a persona. Stored in `sources/overlays/<name>.md`. |
| **Catalog** | Registry of all executable agent configurations. YAML file at `catalog/index.yaml`. The single entry point for the build pipeline. |
| **Config** | A single catalog entry: persona + overlays + model + tools + targets. Produces one agent. |
| **Agent** | The compiled output: a fully defined AI assistant with system prompt, model, tools, and permissions. |

## Build Pipeline

| Term | Definition |
|---|---|
| **IR (Intermediate Representation)** | Dict with `persona`, `rules`, `constraints`, `output_format`. Produced by `build_ir()`. |
| **Compilation** | The process of transforming catalog + sources into runtime-ready JSON. |
| **Flatten** | Converting IR into a formatted string prompt with labeled sections. |
| **Runtime Export** | Transforming opencode.json into other formats (Claude, generic JSON). |

## OpenCode Concepts

| Term | Definition |
|---|---|
| **Primary agent** | Main assistant in a session. Switch via Tab. |
| **Subagent** | Specialized agent invoked via `@mention` or spawned via Task tool. |
| **Task tool** | Mechanism for an agent to spawn a child subagent session. |
| **Skill** | Runtime-loadable behavior packaged as `.opencode/skills/<name>/SKILL.md`. Overlays are synced to skills; the compiler lists available skills in the prompt and config. |
| **task_budget** | Maximum number of Task tool calls an agent can make (prevents infinite recursion). |
| **permission.task** | Glob patterns controlling which subagents can be spawned via Task. |

## Directory Structure

| Path | Purpose |
|---|---|
| `sources/personas/` | Persona definitions (markdown) |
| `sources/overlays/` | Overlay definitions (markdown) |
| `catalog/` | Configuration registry |
| `scripts/` | Python build/export tooling (`compile.py`, `sync_overlays_to_skills.py`) |
| `dist/` | Build output artifacts |
| `.opencode/` | OpenCode runtime config + skills + commands |
