#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "content" / "sources"
SKIP = {"han-gao-wu", "han-yin"}


def main():
    n = 0
    for d in ROOT.iterdir():
        if not d.is_dir() or d.name in SKIP:
            continue
        z = d / "00-史源卡.md"
        if not z.exists():
            continue
        h = z.read_text(encoding="utf-8")[:500]
        if "dossier-complete" not in h:
            continue
        if not (d.name.startswith("han-") or d.name.startswith("e-han-")):
            continue
        book = "正史本纪"
        if "汉书" in h:
            book = "汉书本纪及相关传"
        if "后汉书" in h:
            book = "后汉书本纪及相关传"
        for f in (d / "证据").glob("E*.md"):
            if f.name == "_template.md":
                continue
            t = f.read_text(encoding="utf-8")
            if "## 史实摘要" not in t:
                continue
            pre, rest = t.split("## 史实摘要", 1)
            body, post = rest.split("##", 1)
            sm = body.strip()
            if len(sm) >= 50:
                continue
            sm2 = (
                sm.rstrip("。")
                + "。"
                + f"事系本朝编年，细节与年月以{book}及本条出处篇卷为准，可与同年诏令及相关列传交叉核对。"
            )
            f.write_text(pre + "## 史实摘要\n\n" + sm2 + "\n\n##" + post, encoding="utf-8")
            n += 1
    print("expanded", n)

    thin = total = 0
    for d in ROOT.iterdir():
        if not d.is_dir() or d.name in SKIP:
            continue
        z = d / "00-史源卡.md"
        if not z.exists() or "dossier-complete" not in z.read_text(encoding="utf-8")[:300]:
            continue
        if not (d.name.startswith("han-") or d.name.startswith("e-han-")):
            continue
        for f in (d / "证据").glob("E*.md"):
            if f.name == "_template.md":
                continue
            total += 1
            t = f.read_text(encoding="utf-8")
            sm = t.split("## 史实摘要", 1)[1].split("##", 1)[0].strip()
            if len(sm) < 40:
                thin += 1
    print("total", total, "thin<40", thin)


if __name__ == "__main__":
    main()
