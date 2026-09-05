#!/usr/bin/env python3
"""Create a new static site folder and registry entry by slug."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "sites.json"
TEMPLATE = Path(__file__).resolve().parent / "templates" / "index.html"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_registry() -> dict:
    if REGISTRY.exists():
        return json.loads(REGISTRY.read_text())
    return {"version": 1, "sites": []}


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a slug-based static site")
    parser.add_argument("slug", help="URL slug, e.g. my-new-site")
    parser.add_argument("title", help="Site title shown on the portal")
    parser.add_argument(
        "--description",
        default="New static site.",
        help="Short description for the portal",
    )
    parser.add_argument(
        "--tags",
        default="",
        help="Comma-separated tags, e.g. docs,tools",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing index.html if present",
    )
    args = parser.parse_args()

    slug = args.slug.strip().lower()
    if not SLUG_RE.fullmatch(slug):
        fail("slug must use lowercase letters, numbers, and hyphens only")

    site_dir = ROOT / slug
    index_file = site_dir / "index.html"
    if index_file.exists() and not args.force:
        fail(f"{index_file} already exists (use --force to overwrite)")

    data = load_registry()
    sites = data.setdefault("sites", [])
    if any(site.get("slug") == slug for site in sites):
        fail(f"slug '{slug}' already exists in sites.json")

    if not TEMPLATE.exists():
        fail(f"missing template: {TEMPLATE}")

    site_dir.mkdir(parents=True, exist_ok=True)
    html = TEMPLATE.read_text()
    html = html.replace("{{TITLE}}", args.title).replace(
        "{{DESCRIPTION}}", args.description
    )
    index_file.write_text(html)

    entry = {
        "slug": slug,
        "title": args.title,
        "description": args.description,
    }
    tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
    if tags:
        entry["tags"] = tags

    sites.append(entry)
    sites.sort(key=lambda item: item["slug"])
    REGISTRY.write_text(json.dumps(data, indent=2) + "\n")

    print(f"created: {index_file}")
    print(f"updated: {REGISTRY}")
    print(f"local url: http://localhost:8080/{slug}/")
    print(f"pages url: https://singhalshubham89.github.io/website/{slug}/")


if __name__ == "__main__":
    main()
