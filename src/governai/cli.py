import sys
from pathlib import Path

import click


def _resolve_path(ctx, param, value):
    return Path(value).resolve()


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    ctx.ensure_object(dict)
    ctx.obj["path"] = Path.cwd()

    if ctx.invoked_subcommand is None:
        catalog = ctx.obj["path"] / "catalog" / "index.yaml"
        if catalog.exists():
            ctx.invoke(install, config_id=None, all_flag=True)
        else:
            click.echo("No catalog found in " + str(ctx.obj["path"]))
            click.echo("Run: governAI create -p " + str(ctx.obj["path"]))
            sys.exit(1)


@main.command()
@click.option("-p", "--path", default=".", callback=_resolve_path, help="Target directory")
def list(path):
    catalog = path / "catalog" / "index.yaml"
    if not catalog.exists():
        click.echo("No catalog found at " + str(path), err=True)
        sys.exit(1)
    click.echo("governAI — available configs")
    click.echo("─" * 50)


@main.command()
@click.option("-p", "--path", default=".", callback=_resolve_path, help="Target directory")
def create(path):
    click.echo("Interactive wizard not yet implemented")
    click.echo("For now, create catalog/index.yaml manually")
    sys.exit(1)


@main.command()
@click.option("-p", "--path", default=".", callback=_resolve_path, help="Target directory")
@click.argument("config_id", required=False, default=None)
@click.option("--all", "all_flag", is_flag=True, help="Install all enabled configs")
@click.pass_context
def install(ctx, config_id, all_flag, path):
    catalog = path / "catalog" / "index.yaml"
    if not catalog.exists():
        click.echo("No catalog found at " + str(path), err=True)
        sys.exit(1)
    click.echo("Install" + (" all" if all_flag else " " + (config_id or "?")))
