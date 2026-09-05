#!/usr/bin/env python3
"""Validate slug registry and on-disk site folders."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "sites.json"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESERVED = {"scripts", ".git"}


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not REGISTRY.exists():
        fail(f"missing registry file: {REGISTRY}")

    data = json.loads(REGISTRY.read_text())
    sites = data.get("sites")
    if not isinstance(sites, list):
        fail("sites.json must contain a 'sites' array")

    seen: set[str] = set()
    registered: set[str] = set()

    for index, site in enumerate(sites):
        if not isinstance(site, dict):
            fail(f"sites[{index}] must be an object")

        slug = site.get("slug")
        if not slug or not isinstance(slug, str):
            fail(f"sites[{index}] missing string 'slug'")
        if slug in RESERVED:
            fail(f"slug '{slug}' is reserved")
        if not SLUG_RE.fullmatch(slug):
            fail(f"invalid slug '{slug}' (use lowercase letters, numbers, hyphens)")
        if slug in seen:
            fail(f"duplicate slug '{slug}'")
        seen.add(slug)
        registered.add(slug)

        site_dir = ROOT / slug
        index_file = site_dir / "index.html"
        if not index_file.exists():
            fail(f"missing entry file for slug '{slug}': {index_file}")

        if not site.get("title"):
            fail(f"sites[{index}] missing 'title'")

    for child in ROOT.iterdir():
        if not child.is_dir() or child.name.startswith("."):
            continue
        if child.name in RESERVED:
            continue
        if (child / "index.html").exists() and child.name not in registered:
            fail(
                f"folder '{child.name}' has index.html but is not listed in sites.json"
            )

    print(f"ok: validated {len(registered)} site(s)")


if __name__ == "__main__":
    main()
