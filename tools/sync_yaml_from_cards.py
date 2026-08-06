#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按 content/sources/*/证据 史料卡重写三人 YAML 的 timeline/routes。"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EMP = ROOT / "data" / "emperors"
SRC = ROOT / "content" / "sources"

PERSONS = ["qin-shi-huang", "han-wu-di", "tang-tai-zong"]


def parse_card(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fm = re.match(r"^---\n(.*?)\n---", text, re.S)
    meta: dict = {}
    if fm:
        for line in fm.group(1).splitlines():
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    # related_ids
    rel = meta.get("related_ids", "[]")
    ids = re.findall(r'"([^"]+)"', rel)
    summary_m = re.search(r"## 史实摘要\n\n(.+?)(?:\n\n## |\Z)", text, re.S)
    summary = (summary_m.group(1).strip() if summary_m else "")[:200]
    return {
        "eid": meta.get("eid"),
        "year": meta.get("year", ""),
        "date_note": meta.get("date_note", ""),
        "title": meta.get("title", ""),
        "summary": summary,
        "on_map": meta.get("on_map", "no"),
        "route_group": meta.get("route_group", ""),
        "place_id": meta.get("place_id_candidate", "") or None,
        "related": ids,
        "enter": meta.get("enter_product", "true") == "true",
        "sources_note": meta.get("eid", ""),
    }


def sources_from_card(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    rows = re.findall(
        r"^\| ([^|]+) \| ([^|]+) \| ([^|]+) \|$", text, re.M
    )
    out = []
    for a, b, c in rows:
        if a.strip() in ("文献", "------"):
            continue
        out.append(f"{a.strip()}·{b.strip()}")
    return out or ["史料卡"]


def sync_one(pid: str) -> None:
    ypath = EMP / f"{pid}.yaml"
    data = yaml.safe_load(ypath.read_text(encoding="utf-8"))
    cards_dir = SRC / pid / "证据"
    cards = []
    for p in sorted(cards_dir.glob("E*.md")):
        c = parse_card(p)
        c["path"] = p
        c["src_list"] = sources_from_card(p)
        if c["enter"]:
            cards.append(c)

    timeline = []
    routes = []
    order = 0
    for c in cards:
        # skip pure bio-only if needed — include all enter
        pid_place = c["place_id"] if c["place_id"] not in (None, "", "—", '""') else None
        timeline.append(
            {
                "year": c["year"],
                "date_note": c["date_note"],
                "title": c["title"],
                "summary": c["summary"],
                "place_id": pid_place,
                "related_person_ids": c["related"],
                "sources": c["src_list"],
                "card_id": c["eid"],
            }
        )
        if c["on_map"] == "yes" and pid_place:
            order += 1
            routes.append(
                {
                    "group": c["route_group"] or "其他",
                    "order": order,
                    "year": c["year"],
                    "place_id": pid_place,
                    "event": c["title"],
                }
            )

    data["timeline"] = timeline
    data["routes"] = routes
    meta = data.get("meta") or {}
    meta["status"] = "draft"
    meta["confidence"] = "medium"
    meta["last_reviewed"] = "2026-08-06"
    meta["synced_from_cards"] = True
    data["meta"] = meta

    # enrich sources list
    base_sources = data.get("sources") or []
    titles = {s.get("title") for s in base_sources if isinstance(s, dict)}
    for c in cards:
        for s in c["src_list"]:
            if s not in titles:
                base_sources.append({"title": s, "note": "史料卡同步"})
                titles.add(s)
    data["sources"] = base_sources

    ypath.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8",
    )
    print(f"{pid}: timeline={len(timeline)} routes={len(routes)}")


def main() -> None:
    for pid in PERSONS:
        sync_one(pid)


if __name__ == "__main__":
    main()
