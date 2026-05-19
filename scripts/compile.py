import yaml
import json
from pathlib import Path

from compilers.opencode_compiler import (
    build_ir,
    normalize_ir,
    flatten_to_opencode_prompt,
    compile_overlay
)


ROOT = Path(__file__).resolve().parents[1]

CATALOG_PATH = ROOT / "catalog" / "index.yaml"
PERSONAS_PATH = ROOT / "sources" / "personas"
OVERLAYS_PATH = ROOT / "sources" / "overlays"
DIST_PATH = ROOT / "dist" / "opencode.json"


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build():
    catalog = load_yaml(CATALOG_PATH)

    configs = catalog.get("configs", [])

    if not configs:
        raise ValueError("No configs found in catalog (expected 'configs')")

    output = {
        "$schema": "https://opencode.ai/config.json",
        "agent": {}
    }

    for config in configs:

        agent_id = config.get("id")
        enabled = config.get("enabled", True)

        if not enabled:
            continue

        source = config.get("source", {})
        persona_name = source.get("persona")

        if not persona_name:
            raise ValueError(f"Missing persona for agent {agent_id}")

        overlays = source.get("overlays", [])

        # load persona
        persona_path = PERSONAS_PATH / f"{persona_name}.md"
        persona = load_text(persona_path)

        # compile overlays
        overlay_data = []
        for o in overlays:
            path = OVERLAYS_PATH / f"{o}.md"
            overlay_data.append(
                compile_overlay(load_text(path))
            )

        # build IR
        ir = build_ir(persona, overlay_data)
        ir = normalize_ir(ir)
        task_rules = config.get("tasks", [])
        prompt = flatten_to_opencode_prompt(
            ir, task_rules=task_rules, overlay_names=overlays
        )

        # targets (multi-runtime ready but OpenCode only for now)
        targets = config.get("targets", [])
        model = config.get("model", "anthropic/claude-sonnet-4-20250514")
        tools = config.get("tools", {"write": True, "edit": True, "bash": True})
        mode = config.get("mode", "primary")
        permission = config.get("permission")
        task_budget = config.get("task_budget")

        overlay_skills = [
            f"overlays/{name}" for name in overlays
        ]

        agent_cfg = {
            "description": f"Generated agent: {agent_id}",
            "mode": mode,
            "model": model,
            "prompt": prompt,
            "skills": overlay_skills,
            "meta": {
                "targets": targets
            },
            "tools": tools
        }

        if permission:
            agent_cfg["permission"] = permission
        if task_budget is not None:
            agent_cfg["steps"] = task_budget

        output["agent"][agent_id] = agent_cfg

    DIST_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(DIST_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✔ Generated: {DIST_PATH}")


if __name__ == "__main__":
    build()