#!/usr/bin/env python3
"""轻量校验：id 唯一、引用存在、画像路径声明（不强制文件存在于 draft）。"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("需要 PyYAML：pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
EMP_DIR = ROOT / "data" / "emperors"
PLACE_DIR = ROOT / "data" / "places"
BIO_DIR = ROOT / "content" / "bios"
MASTER = ROOT / "data" / "catalog" / "emperors_master.json"
LINK_RE = re.compile(r"\[\[([a-z0-9-]+)(?:\|[^\]]+)?\]\]")


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    emperors: dict[str, dict] = {}
    for path in sorted(EMP_DIR.glob("*.yaml")):
        data = load_yaml(path)
        if not data or "id" not in data:
            errors.append(f"{path.name}: 缺少 id")
            continue
        eid = data["id"]
        if eid != path.stem:
            errors.append(f"{path.name}: id={eid} 与文件名不一致")
        if eid in emperors:
            errors.append(f"重复 id: {eid}")
        emperors[eid] = data

    places: set[str] = set()
    for path in sorted(PLACE_DIR.glob("*.yaml")):
        data = load_yaml(path)
        if not data or "id" not in data:
            errors.append(f"place {path.name}: 缺少 id")
            continue
        if data["id"] != path.stem:
            errors.append(f"place {path.name}: id 与文件名不一致")
        places.add(data["id"])

    # 全库目录 id（含未升格 stub）：关联/链接允许指向灰卡页，
    # 图鉴 269 张卡都是合法路由，升格推进期间关联图不对称是常态
    catalog_ids: set[str] = set()
    if MASTER.is_file():
        master = json.loads(MASTER.read_text(encoding="utf-8"))
        catalog_ids = {e["id"] for e in master.get("emperors", []) if "id" in e}

    def known_person(target: str) -> bool:
        return target in emperors or target in catalog_ids

    for eid, data in emperors.items():
        tier = data.get("tier")
        if tier in ("quasi", "honorary") and not (data.get("meta") or {}).get(
            "inclusion_reason"
        ):
            errors.append(f"{eid}: {tier} 必须填写 meta.inclusion_reason")

        for rel in data.get("relations") or []:
            tid = rel.get("target_id")
            if tid and not known_person(tid):
                errors.append(f"{eid}: relation 目标不存在: {tid}")

        for ev in data.get("timeline") or []:
            pid = ev.get("place_id")
            if pid and pid not in places:
                errors.append(f"{eid}: timeline place 不存在: {pid}")
            for rid in ev.get("related_person_ids") or []:
                if not known_person(rid):
                    errors.append(f"{eid}: timeline 关联人物不存在: {rid}")

        for rt in data.get("routes") or []:
            pid = rt.get("place_id")
            if pid and pid not in places:
                errors.append(f"{eid}: route place 不存在: {pid}")

        bio = data.get("bio") or {}
        bio_path = None
        if bio.get("file"):
            bio_path = ROOT / bio["file"]
            if not bio_path.is_file():
                errors.append(f"{eid}: bio 文件不存在: {bio['file']}")
        text = ""
        if bio_path and bio_path.is_file():
            text = bio_path.read_text(encoding="utf-8")
        if bio.get("inline"):
            text += "\n" + bio["inline"]
        for link in LINK_RE.findall(text):
            if not known_person(link):
                errors.append(f"{eid}: bio 坏链 [[{link}]]")

        status = (data.get("meta") or {}).get("status", "draft")
        portrait = (data.get("portrait") or {}).get("primary")
        if portrait:
            p = ROOT / portrait
            if not p.is_file():
                msg = f"{eid}: 画像文件缺失: {portrait}"
                if status == "published":
                    errors.append(msg)
                else:
                    warnings.append(msg)

    print(f"帝王 {len(emperors)} · 地点 {len(places)}")
    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERROR {e}")
    if errors:
        print(f"失败：{len(errors)} 个错误")
        return 1
    print("通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
