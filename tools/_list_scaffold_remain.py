#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from collections import Counter
from pathlib import Path

items = json.loads(
    Path("data/catalog/emperors_master.json").read_text(encoding="utf-8")
)["emperors"]
src = Path("content/sources")
sc = []
for it in items:
    p = src / it["id"] / "00-史源卡.md"
    st = "?"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines()[:20]:
            if line.startswith("status:"):
                st = line.split(":", 1)[1].strip()
    if st != "dossier-complete":
        sc.append(it)

print("scaffold", len(sc))
print("--- by dynasty ---")
for dy, n in Counter(x["dynasty"] for x in sc).most_common():
    print(f"  {n:3d}  {dy}")
print("--- list ---")
for it in sc:
    print(
        f"  {it['id']:28s} {it['dynasty']:8s} {it['display']} "
        f"{it.get('reign_start')}-{it.get('reign_end')}"
    )
