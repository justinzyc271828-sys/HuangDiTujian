#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit ONLY frontmatter status: dossier-complete 史料卡."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "content" / "sources"
REF = ROOT / "HuangDiTujian-Ref" / "01-史书全文与扫描" / "二十四史-简体"

BOOKS = {
    "史记": "01-史记.md",
    "汉书": "02-汉书.md",
    "后汉书": "03-后汉书.md",
    "三国志": "04-三国志.md",
    "晋书": "05-晋书.md",
    "宋书": "06-宋书.md",
    "南齐书": "07-南齐书.md",
    "梁书": "08-梁书.md",
    "陈书": "09-陈书.md",
    "魏书": "10-魏书.md",
    "北齐书": "11-北齐书.md",
    "周书": "12-周书.md",
    "隋书": "13-隋书.md",
    "南史": "14-南史.md",
    "北史": "15-北史.md",
    "旧唐书": "16-旧唐书.md",
    "新唐书": "17-新唐书.md",
    "旧五代史": "18-旧五代史.md",
    "宋史": "20-宋史.md",
    "元史": "23-元史.md",
}

_cache: dict[str, str] = {}


def load_book(name: str) -> str:
    if name not in _cache:
        fn = BOOKS.get(name)
        p = REF / fn if fn else None
        _cache[name] = p.read_text(encoding="utf-8") if p and p.exists() else ""
    return _cache[name]


def get_status(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines()[:25]:
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return ""


def parse_card(path: Path) -> dict:
    t = path.read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    if t.startswith("---"):
        for line in t.split("---", 2)[1].splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
    sm = ""
    if "## 史实摘要" in t:
        sm = t.split("## 史实摘要", 1)[1].split("##", 1)[0].strip().replace("\n", " ")
    sources = []
    for a, b, c in re.findall(r"\| ([^|]+) \| ([^|]+) \| ([^|]*) \|", t):
        if a.strip() != "文献":
            sources.append((a.strip(), b.strip(), c.strip()))
    return {
        "path": path,
        "eid": meta.get("eid", ""),
        "year": meta.get("year", ""),
        "title": meta.get("title", path.stem),
        "summary": sm,
        "sources": sources,
        "confidence": meta.get("confidence", ""),
    }


def year_int(y: str) -> int | None:
    if not y or y == "undated":
        return None
    try:
        return int(y)
    except ValueError:
        m = re.match(r"^-?\d+", y)
        return int(m.group(0)) if m else None


# Manual high-value keyword checks: (pid, title_substr, must_find_in_book, book)
FACT_CHECKS = [
    ("han-wen-di", "除肉刑", ["肉刑", "缇萦"], "汉书"),
    ("han-jing-di", "七国", ["七国", "吴楚", "晁错"], "汉书"),
    ("han-zhao-di", "盐铁", ["盐铁", "贤良"], "汉书"),
    ("han-xuan-di", "呼韩邪", ["呼韩邪"], "汉书"),
    ("han-yuan-di", "郅支", ["郅支"], "汉书"),
    ("e-han-guangwu", "昆阳", ["昆阳"], "后汉书"),
    ("e-han-ming", "云台", ["云台"], "后汉书"),
    ("e-han-zhang", "白虎", ["白虎"], "后汉书"),
    ("e-han-he", "燕然", ["燕然"], "后汉书"),
    ("e-han-ling", "黄巾", ["黄巾"], "后汉书"),
    ("e-han-xian", "都许", ["许"], "后汉书"),
    ("wei-wen", "受禅", ["禅", "黄初"], "三国志"),
    ("wei-qi", "高平陵", ["高平陵", "曹爽"], "三国志"),
    ("shu-zhaolie", "夷陵", ["猇亭", "夷陵", "陆逊"], "三国志"),
    ("shu-houzhu", "降", ["降", "邓艾"], "三国志"),
    ("wu-da", "赤壁", ["赤壁", "乌林"], "三国志"),
    ("wu-wucheng", "降", ["降", "王濬"], "三国志"),
    ("w-jin-wu", "平吴", ["孙皓", "吴"], "晋书"),
    ("w-jin-hui", "肉糜", ["肉糜"], "晋书"),
    ("w-jin-huai", "洛阳", ["洛阳"], "晋书"),
    ("e-jin-xiaowu", "淝水", ["淝水", "苻坚"], "晋书"),
    ("qin-shi-huang", "称始皇帝", ["始皇帝", "二十六年"], "史记"),
    ("tang-tai-zong", "玄武", ["玄武"], "旧唐书"),
    ("sui-yang", "江都", ["江都"], "隋书"),
    # 十六国 / 刘宋（本批升格）
    ("q-zhao-liu-cong", "陷洛阳", ["洛阳", "怀帝"], "晋书"),
    ("q-zhao-liu-yao", "洛阳大战", ["石勒", "洛阳"], "晋书"),
    ("h-qin-yao-chang", "杀苻坚", ["苻坚", "新平"], "晋书"),
    ("h-yan-murong-chui", "参合", ["参合"], "晋书"),
    ("xia-helian", "统万", ["统万"], "晋书"),
    ("liu-song-wu", "受禅", ["禅", "永初"], "宋书"),
    ("liu-song-wen", "元嘉", ["元嘉"], "宋书"),
    ("liu-song-wen", "瓜步", ["瓜步", "玄谟"], "宋书"),
    # 南北朝（本批）
    ("qi-gao", "受禅", ["禅", "建元"], "南齐书"),
    ("qi-wu", "永明", ["永明"], "南齐书"),
    ("chen-houzhu", "隋灭陈", ["隋", "祯明"], "陈书"),
    ("n-wei-daowu", "参合", ["参合"], "魏书"),
    ("n-wei-xiaozhuang", "河阴", ["河阴", "尔朱"], "魏书"),
    ("n-zhou-wu", "灭北齐", ["齐", "邺"], "周书"),
    ("n-zhou-wu", "诛宇文护", ["护"], "周书"),
    ("n-qi-houzhu", "齐亡", ["周", "亡"], "北齐书"),
    # 隋唐（交叉比对批）
    ("sui-gong", "禅位唐", ["禅", "李渊"], "隋书"),
    ("tang-gao-zu", "太原起兵", ["太原", "义兵"], "旧唐书"),
    ("tang-gao-zu", "受禅称帝", ["武德", "禅"], "旧唐书"),
    ("tang-gao-zong", "废王立武", ["武后", "皇后"], "旧唐书"),
    ("tang-zhong-zong-b", "复位", ["神龙"], "旧唐书"),
    ("tang-xuan-zong", "安史", ["安禄山", "天宝"], "旧唐书"),
    ("tang-xuan-zong", "马嵬", ["马嵬"], "旧唐书"),
    ("tang-su-zong", "灵武", ["灵武"], "旧唐书"),
    ("tang-de-zong", "奉天", ["奉天"], "旧唐书"),
    ("tang-shun-zong", "永贞", ["永贞", "叔文"], "旧唐书"),
    ("tang-wen-zong", "甘露", ["甘露"], "旧唐书"),
    ("tang-wu-zong", "会昌灭佛", ["废寺", "僧尼"], "旧唐书"),
    ("tang-xi-zong", "黄巢", ["黄巢"], "旧唐书"),
    ("tang-ai-di", "禅位后梁", ["禅", "朱全忠"], "旧唐书"),
]


def main():
    complete: list[tuple[str, list[dict]]] = []
    for d in sorted(SRC.iterdir()):
        if not d.is_dir() or not (d / "00-史源卡.md").exists():
            continue
        if get_status(d / "00-史源卡.md") != "dossier-complete":
            continue
        cards = [
            parse_card(f)
            for f in sorted((d / "证据").glob("E*.md"))
            if f.name != "_template.md"
        ]
        complete.append((d.name, cards))

    issues: list[str] = []
    for pid, cards in complete:
        prev: int | None = None
        for c in cards:
            y = year_int(c["year"])
            if y is not None and prev is not None:
                if (y > 0 and prev > 0 and y < prev - 3) or (
                    y < 0 and prev < 0 and y > prev + 3
                ):
                    # BCE years: -180 then -167 is OK (increasing); reverse would be -167 then -180
                    if y < 0 and prev < 0 and y < prev:  # more negative = earlier, OK
                        pass
                    elif y > 0 and prev > 0 and y < prev:
                        issues.append(
                            f"CHRONO {pid} {c['eid']}: {prev} -> {y} ({c['title']})"
                        )
            if y is not None:
                # for BCE, more negative is earlier; "progress" means y increases toward 0 then positive
                prev = y
            if len(c["summary"]) < 25:
                issues.append(f"THIN {pid} {c['eid']} {c['title']} len={len(c['summary'])}")
            for bad in ("骨架卡", "待本纪条列", "称公元", "中期政务高峰", "初政措置"):
                if bad in c["summary"] or bad in c["title"]:
                    issues.append(f"BADLANG {pid} {c['eid']}: {bad}")

    # fact checks
    fact_lines = []
    for pid, title_key, kws, book in FACT_CHECKS:
        text = load_book(book)
        cards = dict(complete).get(pid)
        if not cards:
            fact_lines.append(f"SKIP {pid}: not complete")
            continue
        hit_card = None
        for c in cards:
            if title_key in c["title"] or title_key in c["summary"]:
                hit_card = c
                break
        if not hit_card:
            fact_lines.append(f"FAIL {pid}: no card for key「{title_key}」")
            issues.append(f"FACT_NOCARD {pid} {title_key}")
            continue
        ok = any(k in text for k in kws)
        if ok:
            fact_lines.append(f"OK {pid}「{title_key}」↔ {book} ({hit_card['eid']})")
        else:
            fact_lines.append(f"FAIL {pid}「{title_key}」not found in {book}")
            issues.append(f"FACT_MISS {pid} {title_key} {book}")

    report = ROOT / "docs" / "references" / "notes" / "史料卡全量复核-complete.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    types = Counter(i.split()[0] for i in issues)
    n_cards = sum(len(c) for _, c in complete)
    body = [
        "# 史料卡全量复核报告（dossier-complete）",
        "",
        f"- **日期：** 2026-08-07",
        f"- **范围：** frontmatter `status: dossier-complete` 仅（不含 scaffold）",
        f"- **人数 / 卡数：** **{len(complete)}** 人 · **{n_cards}** 条",
        f"- **自动问题：** {dict(types) if types else '无'} 合计 **{len(issues)}**",
        f"- **工具：** `tools/audit_complete_dossiers.py` · `fix_complete_dossiers_qa.py` · `patch_chrono_facts.py`",
        "",
        "## 1. 结论",
        "",
        "| 项 | 结果 |",
        "|----|------|",
        f"| 编年倒挂 CHRONO | **{types.get('CHRONO', 0)}** |",
        f"| 摘要过短 THIN | **{types.get('THIN', 0)}** |",
        f"| 弱表述 BADLANG | **{types.get('BADLANG', 0)}** |",
        f"| 名场面对读失败 | **{types.get('FACT_NOCARD', 0) + types.get('FACT_MISS', 0)}** |",
        f"| 名场面通过 | **{sum(1 for x in fact_lines if x.startswith('OK'))}/{len(fact_lines)}** |",
        "",
        "> 196 人 scaffold **不在本报告范围内**，升格时再核。",
        "",
        "## 2. 名场面正史对读",
        "",
    ]
    body += [f"- {x}" for x in fact_lines]
    body += [
        "",
        "## 3. 本轮修复要点（人工）",
        "",
        "- 公历年升序 + 同年事件优先级（生→即位→要事→崩→总评）并重编号 E###",
        "- 光武封禅：中元元年（56），非中元二年",
        "- 明帝封东海公 year=39（建武十五年）；同年内刘备/惠帝/始皇事件序校正",
        "- 弱摘要加长；骨架/垃圾题清理",
        "",
        "## 4. 自动问题（前 80）",
        "",
    ]
    if issues:
        body += [f"- {x}" for x in issues[:80]]
    else:
        body.append("- （无）")
    body += ["", "## 5. 人物卡目", ""]
    for pid, cards in complete:
        body.append(f"### `{pid}`（{len(cards)}）")
        for c in cards:
            body.append(f"- {c['eid']} · `{c['year']}` · **{c['title']}**")
        body.append("")
    report.write_text("\n".join(body), encoding="utf-8")
    print("complete", len(complete), "cards", sum(len(c) for _, c in complete))
    print("issues", dict(types), "total", len(issues))
    for x in fact_lines:
        print(x)
    for x in issues[:25]:
        print("!", x)
    print("report", report)


if __name__ == "__main__":
    main()
