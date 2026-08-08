#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import Counter
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "content" / "sources"

rows = []
for d in sorted(SRC.iterdir()):
    if not d.is_dir():
        continue
    p = d / "00-史源卡.md"
    if not p.exists():
        continue
    st = dy = dn = ""
    for line in p.read_text(encoding="utf-8").splitlines()[:30]:
        if line.startswith("status:"):
            st = line.split(":", 1)[1].strip()
        if line.startswith("dynasty:"):
            dy = line.split(":", 1)[1].strip().strip('"')
        if line.startswith("display_name:"):
            dn = line.split(":", 1)[1].strip().strip('"')
    n = len(list((d / "证据").glob("E*.md"))) if (d / "证据").exists() else 0
    rows.append((st, dy, d.name, dn, n))

print("STATUS", Counter(r[0] for r in rows))
print("\n--- complete by dynasty ---")
for dy, c in Counter(r[1] for r in rows if r[0] == "dossier-complete").most_common():
    print(f"  {c:3d}  {dy}")
print("\n--- scaffold by dynasty ---")
for dy, c in Counter(r[1] for r in rows if r[0] == "dossier-scaffold").most_common():
    print(f"  {c:3d}  {dy}")
print("\n--- scaffold list (first 80) ---")
for r in [x for x in rows if x[0] == "dossier-scaffold"][:80]:
    print(f"  {r[2]:28s} {r[1]:12s} {r[3]}  ({r[4]} cards)")
print("total scaffold", sum(1 for r in rows if r[0] == "dossier-scaffold"))
