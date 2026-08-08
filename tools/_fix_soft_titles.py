#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "content" / "sources"

RENAMES = {
    ("jin-zhang-zong", "开禧对应"): "泰和对宋之战",
    ("liao-mu-zong", "周宋易代"): "应历边事",
    ("liao-mu-zong", "睡王"): "嗜酒酣饮",
    ("liao-tai-zu", "汉契分治"): "南北面官",
}

for (pid, old), new in RENAMES.items():
    evid = SRC / pid / "证据"
    for f in list(evid.glob("E*.md")):
        t = f.read_text(encoding="utf-8")
        if f'title: "{old}"' not in t and old not in f.name:
            continue
        t2 = t.replace(f'title: "{old}"', f'title: "{new}"')
        t2 = t2.replace(f"· {old}", f"· {new}")
        # also expand summary if needed with historical term
        if old == "睡王" and "酣饮" not in t2:
            t2 = t2.replace(
                "## 史实摘要\n\n",
                "## 史实摘要\n\n史称嗜酒，昼夜酣饮（俗号睡王）。",
            )
        if old == "汉契分治" and "北面" not in t2:
            t2 = t2.replace(
                "## 史实摘要\n\n",
                "## 史实摘要\n\n设南北面官分治契丹与汉人事务。",
            )
        if old == "开禧对应" and "泰和" not in t2.split("## 史实摘要", 1)[-1][:80]:
            t2 = t2.replace(
                "## 史实摘要\n\n",
                "## 史实摘要\n\n泰和六年宋韩侂胄北伐，金军拒之。",
            )
        f.write_text(t2, encoding="utf-8")
        print("content", pid, old, "->", new, f.name)

print("run patch_chrono next")
