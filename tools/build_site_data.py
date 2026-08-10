#!/usr/bin/env python3
"""Build apps/web/public/data/site.json from YAML + master catalog + bios."""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("需要: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "apps" / "web" / "public" / "data" / "site.json"
MASTER = ROOT / "data" / "catalog" / "emperors_master.json"
ILLU_DIR = ROOT / "assets" / "video-01" / "emperor-illustrations" / "outputs"
LINK_RE = re.compile(r"\[\[([a-z0-9-]+)(?:\|([^\]]+))?\]\]")


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_bio(md: str) -> list[dict]:
    # 奏折页自绘「主要事迹」标题，bio 里的 ATX 标题行不再透出
    md = "\n".join(line for line in md.splitlines() if not line.lstrip().startswith("#"))
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


def stub_from_catalog(c: dict) -> dict:
    return {
        "id": c["id"],
        "tier": c.get("tier") or "emperor",
        "sort_key": f"{c.get('dynasty','')}-{c.get('sequence',0):03d}",
        "names": {
            "display": c.get("display") or c["id"],
            "personal": c.get("personal") or "",
            "temple": None,
            "posthumous": None,
            "aliases": [],
        },
        "dynasty": {
            "id": c.get("dynasty_id") or "",
            "label": c.get("dynasty") or "",
            "sequence": c.get("sequence"),
        },
        "reign": {
            "start": str(c.get("reign_start") or ""),
            "end": str(c.get("reign_end") or ""),
            "eras": [],
        },
        "summary": c.get("note")
        or "索引占位：尚无人物专页，史料卡与正文待补。",
        "tags": [],
        "timeline": [],
        "relations": [],
        "routes": [],
        "sources": [],
        "bio_md": "",
        "bio_parts": [
            {
                "type": "text",
                "value": "本页为索引灰卡（stub）。已收录身份与在位年，完整事迹、年表与地图路线待撰写。",
            }
        ],
        "meta": {
            "status": "stub",
            "confidence": "low",
            "page_status": "stub",
            "note": c.get("note") or "",
        },
        "page_status": "stub",
        "portrait": {"disclaimer": "画像暂缓"},
    }


def main() -> int:
    places = {}
    for p in sorted((ROOT / "data" / "places").glob("*.yaml")):
        d = load_yaml(p)
        places[d["id"]] = d

    dynasties = load_yaml(ROOT / "data" / "dynasties.yaml") or []

    full: dict[str, dict] = {}
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
        # 英文 bio（可选）：content/bios/en/{id}.md 存在则解析；不存在不设该字段
        en_bio = ROOT / "content" / "bios" / "en" / f"{d['id']}.md"
        if en_bio.is_file():
            d["bio_parts_en"] = parse_bio(en_bio.read_text(encoding="utf-8"))
        d["page_status"] = "draft"
        meta = d.get("meta") or {}
        meta["page_status"] = "draft"
        d["meta"] = meta
        full[d["id"]] = d

    # video-01 已批准插画：拷贝到 public/illustrations/ 并写入 illustration 字段
    illu_copied: dict[str, str] = {}
    if ILLU_DIR.is_dir():
        illu_out = OUT.parent.parent / "illustrations"
        illu_out.mkdir(parents=True, exist_ok=True)
        for png in sorted(ILLU_DIR.glob("*.png")):
            m = re.fullmatch(r"\d+-(.+)\.png", png.name)
            if not m:
                continue
            eid = m.group(1)
            shutil.copy2(png, illu_out / f"{eid}.png")
            illu_copied[eid] = f"illustrations/{eid}.png"
    for eid, rel in illu_copied.items():
        if eid in full:
            full[eid]["illustration"] = rel
    if illu_copied:
        print(f"OK -> illustrations copied: {len(illu_copied)}")

    master_list: list[dict] = []
    if MASTER.is_file():
        master = json.loads(MASTER.read_text(encoding="utf-8"))
        master_list = master.get("emperors") or []

    emperors: list[dict] = []
    seen = set()
    for c in master_list:
        eid = c["id"]
        seen.add(eid)
        if eid in full:
            emperors.append(full[eid])
        else:
            emperors.append(stub_from_catalog(c))

    # YAML not in master still appear (safety)
    for eid, d in full.items():
        if eid not in seen:
            emperors.append(d)

    catalog_stats = {
        "total": len(emperors),
        "stub": sum(1 for e in emperors if e.get("page_status") == "stub"),
        "draft": sum(1 for e in emperors if e.get("page_status") == "draft"),
        "quasi": sum(1 for e in emperors if e.get("tier") == "quasi"),
        "emperor": sum(1 for e in emperors if e.get("tier") == "emperor"),
    }

    video20_path = ROOT / "data" / "catalog" / "video20.json"
    featured_ids: list[str] = []
    if video20_path.is_file():
        v20 = json.loads(video20_path.read_text(encoding="utf-8"))
        featured_ids = [p["id"] for p in (v20.get("profiles") or [])]

    site = {
        "generated_note": "由 tools/build_site_data.py 生成，勿手改",
        "dynasties": dynasties,
        "places": places,
        "emperors": emperors,
        "featured_ids": featured_ids,
        "catalog_stats": catalog_stats,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(site, ensure_ascii=False, indent=2), encoding="utf-8")

    # 替身档 Lab 数据
    stand_src = ROOT / "data" / "catalog" / "stand_stats.json"
    if stand_src.is_file():
        stand_out = OUT.parent / "stand_stats.json"
        stand_out.write_text(stand_src.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"OK -> {stand_out.relative_to(ROOT)}")

    print(
        f"OK -> {OUT.relative_to(ROOT)}  total={catalog_stats['total']} "
        f"draft={catalog_stats['draft']} stub={catalog_stats['stub']} "
        f"quasi={catalog_stats['quasi']} places={len(places)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
