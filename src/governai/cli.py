import sys
import json
from pathlib import Path

import click


_scripts_added = False


def _ensure_scripts():
    global _scripts_added
    if not _scripts_added:
        root = Path(__file__).resolve().parents[2]
        scripts = str(root)
        if scripts not in sys.path:
            sys.path.insert(0, scripts)
        _scripts_added = True


def _resolve_path(ctx, param, value):
    return Path(value).resolve()


def _load_yaml(path):
    import yaml
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _build_config(config, personas_path, overlays_path):
    source = config.get("source", {})
    persona_name = source.get("persona")
    if not persona_name:
        raise click.ClickException(f"Missing persona for config '{config.get('id')}'")

    from scripts.compilers.opencode_compiler import (
        build_ir,
        normalize_ir,
        flatten_to_opencode_prompt,
        compile_overlay,
    )

    persona = _load_text(personas_path / f"{persona_name}.md")
    overlays = source.get("overlays", [])

    overlay_data = []
    for o in overlays:
        path = overlays_path / f"{o}.md"
        overlay_data.append(compile_overlay(_load_text(path)))

    ir = build_ir(persona, overlay_data)
    ir = normalize_ir(ir)
    task_rules = config.get("tasks", [])
    prompt = flatten_to_opencode_prompt(ir, task_rules=task_rules, overlay_names=overlays)

    overlay_skills = [f"overlays/{name}" for name in overlays]

    agent_cfg = {
        "description": f"Generated agent: {config.get('id')}",
        "mode": config.get("mode", "primary"),
        "model": config.get("model", "opencode/deepseek-v4-flash-free"),
        "prompt": prompt,
        "skills": overlay_skills,
        "meta": {"targets": config.get("targets", [])},
        "tools": config.get("tools", {"write": True, "edit": True, "bash": True}),
    }

    permission = config.get("permission")
    if permission:
        agent_cfg["permission"] = permission
    task_budget = config.get("task_budget")
    if task_budget is not None:
        agent_cfg["steps"] = task_budget

    return agent_cfg


@click.group(invoke_without_command=True)
@click.option("-p", "--path", default=".", callback=_resolve_path, help="Target directory")
@click.pass_context
def main(ctx, path):
    _ensure_scripts()
    ctx.ensure_object(dict)
    ctx.obj["path"] = path

    if ctx.invoked_subcommand is None:
        catalog = path / "catalog" / "index.yaml"
        if catalog.exists():
            ctx.invoke(install, config_id=None, all_flag=True, path=path)
        else:
            click.echo("No catalog found in " + str(path))
            click.echo("Run: governAI create -p " + str(path))
            sys.exit(1)


@main.command()
@click.option("-p", "--path", default=".", callback=_resolve_path, help="Target directory")
def list(path):
    catalog = path / "catalog" / "index.yaml"
    if not catalog.exists():
        click.echo("No catalog found at " + str(path), err=True)
        sys.exit(1)
    data = _load_yaml(catalog)
    configs = data.get("configs", [])
    if not configs:
        click.echo("No configs defined in catalog")
        return
    for c in configs:
        mark = "✔" if c.get("enabled", True) else "⏭"
        click.echo(f"  {mark} {c['id']}")
    click.echo(f"\n{len(configs)} config(s)")


@main.command()
@click.option("-p", "--path", default=".", callback=_resolve_path, help="Target directory")
def create(path):
    personas_dir = path / "sources" / "personas"
    overlays_dir = path / "sources" / "overlays"

    if not personas_dir.exists():
        click.echo("No personas directory found at " + str(personas_dir), err=True)
        click.echo("This wizard must be run from a governAI project root with sources/")
        sys.exit(1)

    personas = sorted(p.stem for p in personas_dir.glob("*.md"))
    overlays = sorted(p.stem for p in overlays_dir.glob("*.md")) if overlays_dir.exists() else []

    click.echo("governAI — create agent config")
    click.echo("─" * 50)

    click.echo("\nAvailable personas:")
    for i, p in enumerate(personas, 1):
        click.echo(f"  {i}. {p}")
    sel = click.prompt("\nSelect persona", type=int, default=1)
    persona = personas[sel - 1]

    selected_overlays = []
    if overlays:
        click.echo("\nAvailable overlays (comma-separated numbers, or 0 for none):")
        for i, o in enumerate(overlays, 1):
            click.echo(f"  {i}. {o}")
        sel_overlays = click.prompt("Select overlays", default="0")
        if sel_overlays.strip() != "0":
            for s in sel_overlays.split(","):
                s = s.strip()
                if s.isdigit():
                    idx = int(s) - 1
                    if 0 <= idx < len(overlays):
                        selected_overlays.append(overlays[idx])

    config_id = click.prompt("Config ID", default=persona)
    enabled = click.confirm("Enable this config?", default=True)

    catalog_dir = path / "catalog"
    catalog_dir.mkdir(parents=True, exist_ok=True)

    entry = {
        "id": config_id,
        "enabled": enabled,
        "source": {
            "persona": persona,
            "overlays": selected_overlays,
        },
        "targets": [{"runtime": "opencode"}],
    }

    dst = catalog_dir / "index.yaml"
    if dst.exists():
        import yaml
        data = _load_yaml(dst)
        data.setdefault("configs", []).append(entry)
    else:
        data = {"configs": [entry]}

    with open(dst, "w", encoding="utf-8") as f:
        import yaml
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    click.echo(f"\n✔ Config added: {dst}")


@main.command()
@click.option("-p", "--path", default=".", callback=_resolve_path, help="Target directory")
@click.argument("config_id", required=False, default=None)
@click.option("--all", "all_flag", is_flag=True, help="Install all enabled configs")
def install(config_id, all_flag, path):
    catalog = path / "catalog" / "index.yaml"
    if not catalog.exists():
        click.echo("No catalog found at " + str(path), err=True)
        sys.exit(1)

    data = _load_yaml(catalog)
    all_configs = data.get("configs", [])

    selected = []
    for c in all_configs:
        if not c.get("enabled", True):
            continue
        if config_id and c.get("id") != config_id:
            continue
        if not config_id and not all_flag:
            continue
        selected.append(c)

    if not selected:
        click.echo("No matching enabled configs", err=True)
        sys.exit(1)

    personas_path = path / "sources" / "personas"
    overlays_path = path / "sources" / "overlays"

    output = {
        "$schema": "https://opencode.ai/config.json",
        "agent": {},
    }

    for c in selected:
        cid = c["id"]
        try:
            agent_cfg = _build_config(c, personas_path, overlays_path)
            output["agent"][cid] = agent_cfg
            click.echo(f"  ✔ {cid}")
        except Exception as e:
            click.echo(f"  ✖ {cid}: {e}", err=True)
            sys.exit(1)

    dist_dir = path / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)
    dst = dist_dir / "opencode.json"
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    click.echo(f"✔ Generated: {dst}")
