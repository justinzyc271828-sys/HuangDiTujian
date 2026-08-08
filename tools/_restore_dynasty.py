#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Restore empty dynasty fields on 00-史源卡 from master catalog."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "content" / "sources"
master = {
    e["id"]: e
    for e in json.loads(
        (ROOT / "data" / "catalog" / "emperors_master.json").read_text(encoding="utf-8")
    )["emperors"]
}

n = 0
for d in sorted(SRC.iterdir()):
    if not d.is_dir():
        continue
    p = d / "00-史源卡.md"
    if not p.exists():
        continue
    t = p.read_text(encoding="utf-8")
    m = re.search(r'^dynasty:\s*"?(.*?)"?\s*$', t, re.M)
    if not m:
        continue
    cur = m.group(1).strip().strip('"')
    if cur:
        continue
    info = master.get(d.name)
    if not info:
        continue
    dy = info.get("dynasty", "")
    if not dy:
        continue
    t2 = re.sub(r'^dynasty:\s*"?.*?"?\s*$', f'dynasty: "{dy}"', t, count=1, flags=re.M)
    if t2 != t:
        p.write_text(t2, encoding="utf-8")
        n += 1
        print("restored", d.name, dy)
print("restored", n)
