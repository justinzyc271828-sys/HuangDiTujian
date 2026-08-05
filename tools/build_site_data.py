#!/usr/bin/env python3
"""Build apps/web/public/data/site.json from YAML + bios."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("需要: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "apps" / "web" / "public" / "data" / "site.json"
LINK_RE = re.compile(r"\[\[([a-z0-9-]+)(?:\|([^\]]+))?\]\]")


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_bio(md: str) -> list[dict]:
    """Split markdown into segments of text / emperor links."""
    parts: list[dict] = []
    last = 0
    for m in LINK_RE.finditer(md):
        if m.start() > last:
            parts.append({"type": "text", "value": md[last : m.start()]})
        parts.append(
            {
                "type": "link",
                "id": m.group(1),
                "label": m.group(2) or m.group(1),
            }
        )
        last = m.end()
    if last < len(md):
        parts.append({"type": "text", "value": md[last:]})
    return parts


def main() -> int:
    places = {}
    for p in sorted((ROOT / "data" / "places").glob("*.yaml")):
        d = load_yaml(p)
        places[d["id"]] = d

    dynasties = load_yaml(ROOT / "data" / "dynasties.yaml") or []

    emperors = []
    for p in sorted((ROOT / "data" / "emperors").glob("*.yaml")):
        d = load_yaml(p)
        bio_file = (d.get("bio") or {}).get("file")
        bio_md = ""
        if bio_file:
            bp = ROOT / bio_file
            if bp.is_file():
                bio_md = bp.read_text(encoding="utf-8")
        d["bio_md"] = bio_md
        d["bio_parts"] = parse_bio(bio_md)
        # drop heavy unused fields for client if needed — keep full for MVP
        emperors.append(d)

    emperors.sort(key=lambda e: e.get("sort_key") or e["id"])

    site = {
        "generated_note": "由 tools/build_site_data.py 生成，勿手改",
        "dynasties": dynasties,
        "places": places,
        "emperors": emperors,
        "featured_ids": ["qin-shi-huang", "han-wu-di", "tang-tai-zong"],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(site, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK -> {OUT.relative_to(ROOT)}  emperors={len(emperors)} places={len(places)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
