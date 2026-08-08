#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉比对：在二十四史简体 md 中检索关键词，输出命中/未命中。
用于升格前/后核验事件是否能在正史正文中对上。
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "HuangDiTujian-Ref" / "01-史书全文与扫描" / "二十四史-简体"

BOOKS = {
    "旧唐书": "16-旧唐书.md",
    "新唐书": "17-新唐书.md",
    "隋书": "13-隋书.md",
    "晋书": "05-晋书.md",
    "宋书": "06-宋书.md",
    "魏书": "10-魏书.md",
    "北齐书": "11-北齐书.md",
    "周书": "12-周书.md",
    "南齐书": "07-南齐书.md",
    "梁书": "08-梁书.md",
    "陈书": "09-陈书.md",
    "史记": "01-史记.md",
    "汉书": "02-汉书.md",
    "后汉书": "03-后汉书.md",
    "三国志": "04-三国志.md",
}

_cache: dict[str, str] = {}


def load(book: str) -> str:
    if book not in _cache:
        fn = BOOKS.get(book)
        p = REF / fn if fn else None
        _cache[book] = p.read_text(encoding="utf-8") if p and p.exists() else ""
    return _cache[book]


def hit(book: str, keywords: list[str], any_mode: bool = True) -> tuple[bool, list[str]]:
    text = load(book)
    if not text:
        return False, ["BOOK_MISSING"]
    found, miss = [], []
    for k in keywords:
        if k in text:
            found.append(k)
        else:
            miss.append(k)
    ok = bool(found) if any_mode else not miss
    return ok, found if ok else miss


# (label, book, keywords any-of)
CHECKS: list[tuple[str, str, list[str]]] = [
    # 隋
    ("隋文帝·开皇", "隋书", ["开皇", "杨坚"]),
    ("隋文帝·平陈", "隋书", ["平陈", "陈国亡", "叔宝"]),
    ("隋恭帝·禅唐", "隋书", ["恭帝", "禅", "李渊"]),
    # 唐关键
    ("高祖·太原", "旧唐书", ["太原", "义兵", "高祖"]),
    ("高祖·武德", "旧唐书", ["武德", "李渊"]),
    ("太宗·玄武门", "旧唐书", ["玄武门"]),
    ("太宗·贞观", "旧唐书", ["贞观"]),
    ("太宗·突厥", "旧唐书", ["突厥", "颉利"]),
    ("高宗·废王立武", "旧唐书", ["武后", "皇后", "王皇后"]),
    ("武后·称帝", "旧唐书", ["则天皇后", "圣神皇帝", "革唐"]),
    ("武后·神都", "旧唐书", ["神都", "洛阳"]),
    ("中宗·复位", "旧唐书", ["神龙", "中宗"]),
    ("玄宗·开元", "旧唐书", ["开元"]),
    ("玄宗·安史", "旧唐书", ["安禄山", "天宝"]),
    ("玄宗·马嵬", "旧唐书", ["马嵬"]),
    ("肃宗·灵武", "旧唐书", ["灵武"]),
    ("代宗·吐蕃入京", "旧唐书", ["吐蕃", "长安"]),
    ("德宗·奉天", "旧唐书", ["奉天"]),
    ("顺宗·永贞", "旧唐书", ["永贞"]),
    ("宪宗·元和中兴", "旧唐书", ["元和"]),
    ("宪宗·平淮西", "旧唐书", ["淮西", "吴元济"]),
    ("穆宗·长庆", "旧唐书", ["长庆"]),
    ("敬宗·遇弑", "旧唐书", ["敬宗", "苏佐明"]),
    ("文宗·甘露", "旧唐书", ["甘露"]),
    ("武宗·会昌", "旧唐书", ["会昌"]),
    ("武宗·灭佛", "旧唐书", ["废寺", "僧尼", "会昌"]),
    ("宣宗·大中", "旧唐书", ["大中"]),
    ("懿宗·庞勋", "旧唐书", ["庞勋"]),
    ("僖宗·黄巢", "旧唐书", ["黄巢"]),
    ("昭宗·迁洛", "旧唐书", ["洛阳", "朱全忠"]),
    ("哀帝·禅梁", "旧唐书", ["哀帝", "禅", "朱全忠"]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="substring filter on label")
    args = ap.parse_args()
    ok_n = fail_n = 0
    lines = ["# 正史交叉比对（关键词）", ""]
    for label, book, kws in CHECKS:
        if args.only and args.only not in label:
            continue
        ok, detail = hit(book, kws, any_mode=True)
        if ok:
            ok_n += 1
            lines.append(f"- OK {label} ↔ {book} hit={detail}")
            print(f"OK  {label} ↔ {book} {detail}")
        else:
            fail_n += 1
            lines.append(f"- FAIL {label} ↔ {book} miss={detail}")
            print(f"FAIL {label} ↔ {book} {detail}")
    lines += ["", f"合计 OK {ok_n} / FAIL {fail_n}"]
    out = ROOT / "docs" / "references" / "notes" / "交叉比对-隋唐关键词.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", out, "OK", ok_n, "FAIL", fail_n)


if __name__ == "__main__":
    main()
