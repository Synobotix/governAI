#!/usr/bin/env python3
"""
Validate catalog/index.yaml schema and source references.

Checks:
- Required fields: id, source.persona, targets
- Source files exist (persona, overlays)
- mode is valid (primary / subagent)
- Runtime targets are supported

Usage:
    python3 scripts/validate_catalog.py
"""

import yaml
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog" / "index.yaml"
PERSONAS_PATH = ROOT / "sources" / "personas"
OVERLAYS_PATH = ROOT / "sources" / "overlays"


class CatalogError(Exception):
    pass


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate():
    catalog = load_yaml(CATALOG_PATH)

    if "configs" not in catalog:
        raise CatalogError("Missing top-level 'configs'")
    if not isinstance(catalog["configs"], list):
        raise CatalogError("'configs' must be a list")

    for entry in catalog["configs"]:
        cid = entry.get("id", "<unnamed>")

        if not entry.get("enabled", True):
            print(f"  ⏭  {cid}: disabled, skipping")
            continue

        if "id" not in entry:
            raise CatalogError("Config missing 'id'")

        persona = entry.get("source", {}).get("persona")
        if not persona:
            raise CatalogError(f"Config '{cid}' missing source.persona")

        persona_file = PERSONAS_PATH / f"{persona}.md"
        if not persona_file.exists():
            raise CatalogError(
                f"Config '{cid}' persona '{persona}' not found at {persona_file}"
            )

        for overlay in entry.get("source", {}).get("overlays", []):
            overlay_file = OVERLAYS_PATH / f"{overlay}.md"
            if not overlay_file.exists():
                raise CatalogError(
                    f"Config '{cid}' overlay '{overlay}' not found at {overlay_file}"
                )

        mode = entry.get("mode", "primary")
        if mode not in ("primary", "subagent"):
            raise CatalogError(
                f"Config '{cid}' mode must be 'primary' or 'subagent', got '{mode}'"
            )

        targets = entry.get("targets", [])
        if not targets:
            raise CatalogError(f"Config '{cid}' has no targets")

        for t in targets:
            if t.get("runtime") != "opencode":
                raise CatalogError(
                    f"Config '{cid}' unsupported runtime '{t.get('runtime')}'"
                )

        print(f"  ✔ {cid}: valid")

    print("✔ Catalog is valid")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(validate())
    except CatalogError as e:
        print(f"✖ {e}")
        sys.exit(1)
