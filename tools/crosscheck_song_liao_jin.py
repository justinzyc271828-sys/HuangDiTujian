#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
南宋/辽/金 本批卡片交叉核验：
1) 卡标题关键词是否在对应正史 md 出现
2) 卡内出处「文献」列是否与朝别匹配
3) 编年是否升序
写出 notes 报告。
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "content" / "sources"
REF = ROOT / "HuangDiTujian-Ref" / "01-史书全文与扫描" / "二十四史-简体"
OUT = ROOT / "docs" / "references" / "notes" / "交叉核验-南宋辽金.md"

BOOK_FILES = {
    "宋史": "20-宋史.md",
    "辽史": "21-辽史.md",
    "金史": "22-金史.md",
    "元史": "23-元史.md",
}

# pid -> expected primary book
COHORT = {
    # 南宋
    "s-song-gao": "宋史",
    "s-song-xiao": "宋史",
    "s-song-guang": "宋史",
    "s-song-ning": "宋史",
    "s-song-li": "宋史",
    "s-song-du": "宋史",
    "s-song-gong": "宋史",
    "s-song-duan": "宋史",
    "s-song-di-bing": "宋史",
    # 辽
    "liao-tai-zu": "辽史",
    "liao-tai-zong": "辽史",
    "liao-shi-zong": "辽史",
    "liao-mu-zong": "辽史",
    "liao-jing-zong": "辽史",
    "liao-sheng-zong": "辽史",
    "liao-xing-zong": "辽史",
    "liao-dao-zong": "辽史",
    "liao-tianzuo": "辽史",
    # 金
    "jin-tai-zu": "金史",
    "jin-tai-zong": "金史",
    "jin-xi-zong": "金史",
    "jin-hailiing": "金史",
    "jin-shi-zong": "金史",
    "jin-zhang-zong": "金史",
    "jin-wei-shao": "金史",
    "jin-xuan-zong": "金史",
    "jin-ai-zong": "金史",
}

# high-value title substrings that MUST appear in the primary book
MUST = [
    ("s-song-gao", "岳飞", "宋史"),
    ("s-song-gao", "绍兴", "宋史"),
    ("s-song-gao", "建炎", "宋史"),
    ("s-song-xiao", "隆兴", "宋史"),
    ("s-song-ning", "开禧", "宋史"),
    ("s-song-li", "蔡州", "宋史"),
    ("s-song-di-bing", "崖山", "宋史"),
    ("s-song-gong", "德祐", "宋史"),
    ("liao-tai-zu", "神册", "辽史"),
    ("liao-tai-zu", "渤海", "辽史"),
    ("liao-tai-zong", "十六", "辽史"),  # 十六州 narrative
    ("liao-sheng-zong", "澶渊", "辽史"),
    ("liao-tianzuo", "天祚", "辽史"),
    ("jin-tai-zu", "收国", "金史"),
    ("jin-tai-zong", "天会", "金史"),
    ("jin-hailiing", "中都", "金史"),
    ("jin-shi-zong", "大定", "金史"),
    ("jin-ai-zong", "蔡州", "金史"),
    ("jin-ai-zong", "天兴", "金史"),
]

_cache: dict[str, str] = {}


def load(book: str) -> str:
    if book not in _cache:
        fn = BOOK_FILES.get(book)
        p = REF / fn if fn else None
        _cache[book] = p.read_text(encoding="utf-8") if p and p.exists() else ""
    return _cache[book]


def parse_cards(pid: str) -> list[dict]:
    evid = SRC / pid / "证据"
    out = []
    if not evid.exists():
        return out
    for f in sorted(evid.glob("E*.md")):
        if f.name == "_template.md":
            continue
        t = f.read_text(encoding="utf-8")
        meta = {}
        if t.startswith("---"):
            for line in t.split("---", 2)[1].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"')
        sm = ""
        if "## 史实摘要" in t:
            sm = t.split("## 史实摘要", 1)[1].split("##", 1)[0].strip()
        books = []
        for a, b, c in re.findall(r"\| ([^|]+) \| ([^|]+) \| ([^|]*) \|", t):
            if a.strip() != "文献":
                books.append(a.strip())
        out.append(
            {
                "eid": meta.get("eid", ""),
                "year": meta.get("year", ""),
                "title": meta.get("title", ""),
                "summary": sm,
                "books": books,
                "file": f.name,
            }
        )
    return out


def year_int(y: str) -> int | None:
    if not y or y == "undated":
        return None
    try:
        return int(y)
    except ValueError:
        m = re.match(r"^-?\d+", y)
        return int(m.group(0)) if m else None


def main():
    lines = [
        "# 交叉核验 · 南宋 / 辽 / 金",
        "",
        "- 日期：2026-08-07",
        f"- 人数：{len(COHORT)}",
        "- 方法：卡标题/摘要关键词 ∈ 正史全文；出处书名匹配；编年升序",
        "",
    ]
    ok_n = fail_n = 0
    issues = []

    # MUST checks
    lines.append("## 1. 名场面关键词")
    lines.append("")
    for pid, key, book in MUST:
        text = load(book)
        cards = parse_cards(pid)
        if not cards:
            issues.append(f"NO_CARDS {pid}")
            fail_n += 1
            lines.append(f"- FAIL {pid} 无卡")
            continue
        hit_card = next(
            (c for c in cards if key in c["title"] or key in c["summary"]),
            None,
        )
        in_book = key in text if text else False
        if hit_card and in_book:
            ok_n += 1
            lines.append(f"- OK {pid}「{key}」↔ {book} ({hit_card['eid']})")
        else:
            fail_n += 1
            why = []
            if not hit_card:
                why.append("卡无此题")
            if not in_book:
                why.append(f"{book}正文未命中")
            issues.append(f"MUST {pid} {key}: {','.join(why)}")
            lines.append(f"- FAIL {pid}「{key}」— {', '.join(why)}")

    # per-person source + chrono
    lines.append("")
    lines.append("## 2. 出处匹配与编年")
    lines.append("")
    for pid, exp_book in sorted(COHORT.items()):
        cards = parse_cards(pid)
        if not cards:
            issues.append(f"EMPTY {pid}")
            lines.append(f"- FAIL `{pid}` 无证据卡")
            continue
        # primary source present?
        has_src = any(exp_book in b for c in cards for b in c["books"])
        # chrono
        prev = None
        chrono_ok = True
        for c in cards:
            y = year_int(c["year"])
            if y is not None and prev is not None and y > 0 and prev > 0 and y < prev:
                chrono_ok = False
                issues.append(f"CHRONO {pid} {c['eid']} {prev}->{y}")
            if y is not None:
                prev = y
        # title keyword soft check: first 2 chars of title in book?
        text = load(exp_book)
        soft_miss = []
        for c in cards:
            title = c["title"]
            # skip undated 史评/总评
            if any(
                x in title
                for x in (
                    "总评",
                    "史评",
                    "政风",
                    "文化",
                    "艺术",
                    "制度",
                    "名分",
                    "余绪",
                    "文学",
                )
            ):
                continue
            # sliding bigrams from Chinese title (full-string match is too strict)
            chars = re.findall(r"[\u4e00-\u9fff]", title)
            bigrams = ["".join(chars[i : i + 2]) for i in range(len(chars) - 1)]
            # drop weak bigrams
            bigrams = [
                b
                for b in bigrams
                if b
                not in (
                    "即位",
                    "被弑",
                    "遇害",
                    "同年",
                    "前后",
                    "之战",
                    "之变",
                    "之治",
                    "对应",
                    "预政",
                    "易代",
                    "分治",
                    "汉化",
                    "和好",
                )
            ]
            if not bigrams or not text:
                continue
            if not any(b in text for b in bigrams):
                soft_miss.append(f"{c['eid']}:{title}")
        status = []
        if has_src:
            status.append(f"出处含{exp_book}")
        else:
            status.append(f"缺{exp_book}出处")
            issues.append(f"SRC {pid} missing {exp_book}")
        status.append("编年OK" if chrono_ok else "编年FAIL")
        if soft_miss:
            status.append(f"弱未命中{len(soft_miss)}")
            for s in soft_miss[:3]:
                issues.append(f"SOFT {pid} {s}")
        mark = "OK" if has_src and chrono_ok and not soft_miss else (
            "WARN" if has_src and chrono_ok else "FAIL"
        )
        if mark == "OK":
            ok_n += 1
        elif mark == "FAIL":
            fail_n += 1
        lines.append(f"- {mark} `{pid}`（{len(cards)}）{' · '.join(status)}")
        if soft_miss and mark != "FAIL":
            lines.append(f"  - soft: {', '.join(soft_miss[:5])}")

    lines.append("")
    lines.append("## 3. 问题汇总")
    lines.append("")
    lines.append(f"- MUST/结构 OK 计数（含逐人）：约通过项见上")
    lines.append(f"- issues 条数：**{len(issues)}**")
    if issues:
        for i in issues:
            lines.append(f"- {i}")
    else:
        lines.append("- （无）")

    lines.append("")
    lines.append("## 4. 说明")
    lines.append("")
    lines.append("- SOFT：标题用词与正文用字不完全一致时可能误报（如异名、省称）")
    lines.append("- 非纸书页码精校")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", OUT)
    print("issues", len(issues))
    for i in issues[:30]:
        print("!", i)


if __name__ == "__main__":
    main()
