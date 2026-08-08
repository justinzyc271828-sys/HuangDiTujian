#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from pathlib import Path

items = json.loads(
    Path("data/catalog/emperors_master.json").read_text(encoding="utf-8")
)["emperors"]
src = Path("content/sources")
for dy in ("隋", "唐"):
    print("===", dy)
    for it in items:
        if it["dynasty"] != dy:
            continue
        p = src / it["id"] / "00-史源卡.md"
        st = "?"
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines()[:20]:
                if line.startswith("status:"):
                    st = line.split(":", 1)[1].strip()
        mark = "OK" if st == "dossier-complete" else "sc"
        print(
            f"  {mark} {it['id']:28s} {it['display']} "
            f"{it.get('reign_start')}-{it.get('reign_end')}"
        )
