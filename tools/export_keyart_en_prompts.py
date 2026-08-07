#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export 20 English key-art prompts to fixed workspace folders."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from keyart_appearance_data import NEGATIVE, SCENES  # noqa: E402
from build_video20_keyart_prompts import full_prompt, personal_name  # noqa: E402

OUT_PKG = ROOT / "content" / "video" / "video-01" / "key-art" / "en-prompts"
OUT_ROOT = ROOT / "key-art-en-prompts-video01"
VIDEO20 = ROOT / "data" / "catalog" / "video20.json"


def write_set(out: Path, profiles: dict) -> None:
    out.mkdir(parents=True, exist_ok=True)
    index_rows = [
        "| # | id | name | file |",
        "|---|-----|------|------|",
    ]
    all_md_parts = ["# ALL 20 English prompts (video-01)\n"]
    all_txt_parts: list[str] = []

    for pid, sc in sorted(SCENES.items(), key=lambda x: x[1]["order"]):
        p = profiles[pid]
        name = personal_name(p)
        order = sc["order"]
        pos = full_prompt(sc["prompt"])
        fname = f"{order:02d}-{pid}.txt"
        body = "\n".join(
            [
                f"ID: {pid}",
                f"ORDER: {order}",
                f"PERSONAL_NAME_ZH: {name}",
                f"DISPLAY_ZH: {p['display']}",
                f"EPITHET_ZH: {p['epithet']}",
                f"EVENT_ZH: {' / '.join(sc['event_zh'])}",
                f"APPEARANCE_LEVEL: {sc['appearance_level']}",
                f"COSTUME_LEVEL: {sc.get('costume_level', '')}",
                f"STYLE_ZH: {sc['style_faction_zh']}",
                "",
                "=== POSITIVE PROMPT (English — copy to Image) ===",
                "",
                pos,
                "",
                "=== NEGATIVE PROMPT (English) ===",
                "",
                NEGATIVE,
                "",
                "=== SETTINGS ===",
                "aspect_ratio: 16:9",
                "language: English prompt only for generation",
                "overlay_later: Chinese personal name first, then title; no book-title marks on events",
                "",
            ]
        )
        (out / fname).write_text(body, encoding="utf-8")
        index_rows.append(f"| {order} | `{pid}` | {name} | `{fname}` |")
        all_md_parts.append(
            f"## {order:02d} {name} / {p['display']} (`{pid}`)\n\n"
            f"### Positive\n\n```\n{pos}\n```\n\n"
            f"### Negative\n\n```\n{NEGATIVE}\n```\n\n---\n"
        )
        all_txt_parts += [
            f"########## {order:02d} {pid} {name} ##########",
            "POSITIVE:",
            pos,
            "NEGATIVE:",
            NEGATIVE,
            "",
        ]

    readme = "\n".join(
        [
            "# English Image Prompts — video-01 (20 emperors)",
            "",
            "Prompts are **English-only** for your image model.",
            "Chinese fields in each `.txt` are metadata for later overlay only.",
            "",
            "## Fixed paths in this repo",
            "",
            f"- `{OUT_PKG.relative_to(ROOT).as_posix()}/`",
            f"- `{OUT_ROOT.relative_to(ROOT).as_posix()}/`  ← workspace-root shortcut",
            "",
            "## How to use",
            "",
            "1. Open `01-….txt` … `20-….txt`",
            "2. Copy the **POSITIVE** block into Image",
            "3. Paste **NEGATIVE** if supported",
            "4. Aspect **16:9**",
            "5. After generation, overlay Chinese name (personal first) + radar from `overlay-zh.json`",
            "",
            "## Combined files",
            "",
            "- `ALL-20-PROMPTS.md`",
            "- `ALL-20-PROMPTS.txt`",
            "",
            "## Index",
            "",
            *index_rows,
            "",
            "Rebuild export: `python tools/export_keyart_en_prompts.py`",
            "",
        ]
    )
    (out / "README.md").write_text(readme, encoding="utf-8")
    (out / "ALL-20-PROMPTS.md").write_text("\n".join(all_md_parts), encoding="utf-8")
    (out / "ALL-20-PROMPTS.txt").write_text("\n".join(all_txt_parts), encoding="utf-8")


def main() -> None:
    profiles = {
        p["id"]: p
        for p in json.loads(VIDEO20.read_text(encoding="utf-8"))["profiles"]
    }
    write_set(OUT_PKG, profiles)
    write_set(OUT_ROOT, profiles)
    print("OK", OUT_PKG)
    print("OK", OUT_ROOT)
    print("txt count root:", len(list(OUT_ROOT.glob("0*.txt"))))


if __name__ == "__main__":
    main()
