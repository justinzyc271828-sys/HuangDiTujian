#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path

items = json.loads(
    Path("data/catalog/emperors_master.json").read_text(encoding="utf-8")
)["emperors"]
src = Path("content/sources")
G16 = {
    "前赵",
    "后赵",
    "前燕",
    "后燕",
    "南燕",
    "北燕",
    "前秦",
    "后秦",
    "西秦",
    "前凉",
    "后凉",
    "南凉",
    "北凉",
    "西凉",
    "成汉",
    "胡夏",
    "代",
    "冉魏",
    "西燕",
}
GNB = {"刘宋", "南齐", "梁", "陈", "北魏", "东魏", "西魏", "北齐", "北周"}
for gname, gset in [("十六国", G16), ("南北朝", GNB)]:
    print("====", gname)
    for it in items:
        if it["dynasty"] not in gset:
            continue
        p = src / it["id"] / "00-史源卡.md"
        st = "?"
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines()[:20]:
                if line.startswith("status:"):
                    st = line.split(":", 1)[1].strip()
        mark = "OK" if st == "dossier-complete" else "sc"
        print(
            f"  {mark} {it['id']:28s} {it['dynasty']:6s} {it['display']} "
            f"{it.get('reign_start')}-{it.get('reign_end')}"
        )
