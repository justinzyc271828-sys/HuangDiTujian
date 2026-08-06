#!/usr/bin/env python3
"""在参考库简体史书中快速检索（写史料卡用）。"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "HuangDiTujian-Ref" / "01-史书全文与扫描"

BOOK_MAP = {
    "史记": REF / "二十四史-简体" / "01-史记.md",
    "汉书": REF / "二十四史-简体" / "02-汉书.md",
    "旧唐书": REF / "二十四史-简体" / "16-旧唐书.md",
    "新唐书": REF / "二十四史-简体" / "17-新唐书.md",
    "通鉴": REF / "资治通鉴-简体" / "01-资治通鉴.md",
    "资治通鉴": REF / "资治通鉴-简体" / "01-资治通鉴.md",
}


def nearest_heading(text: str, pos: int) -> str:
    head = text[:pos]
    h2 = list(re.finditer(r"^## (.+)$", head, re.M))
    h3 = list(re.finditer(r"^### (.+)$", head, re.M))
    parts = []
    if h2:
        parts.append("## " + h2[-1].group(1).strip())
    if h3:
        parts.append("### " + h3[-1].group(1).strip())
    return " / ".join(parts) if parts else "(文件开头)"


def search_file(path: Path, query: str, limit: int) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    print(f"\n=== {path.name} ===")
    count = 0
    for m in re.finditer(re.escape(query), text):
        count += 1
        if count > limit:
            continue
        pos = m.start()
        line = text.count("\n", 0, pos) + 1
        ctx = text[max(0, pos - 40) : pos + 80].replace("\n", " ↵ ")
        print(f"#{count} line≈{line}  {nearest_heading(text, pos)}")
        print(f"   …{ctx}…")
    total = len(re.findall(re.escape(query), text))
    if total > limit:
        print(f"   …另有 {total - limit} 处未显示（共 {total}）")
    if total == 0:
        print("   (无命中)")


def main() -> int:
    ap = argparse.ArgumentParser(description="检索参考库简体史书")
    ap.add_argument("query", help="精确子串")
    ap.add_argument("--book", help="史记|汉书|旧唐书|新唐书|通鉴，默认全关键书")
    ap.add_argument("--limit", type=int, default=8, help="每书最多显示条数")
    args = ap.parse_args()

    if args.book:
        key = args.book.strip()
        if key not in BOOK_MAP:
            print("未知 --book，可选:", ", ".join(BOOK_MAP))
            return 2
        paths = [BOOK_MAP[key]]
    else:
        paths = list(BOOK_MAP.values())
        # unique preserve order
        seen = set()
        paths = [p for p in paths if not (p in seen or seen.add(p))]

    for p in paths:
        if not p.is_file():
            print("缺文件", p)
            continue
        search_file(p, args.query, args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
