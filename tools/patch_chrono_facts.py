#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复核补丁：修正已知年份锚点 + 同年内事件优先级排序，重编号 E###。
⚠ 注意：本脚本按编年重排并全量重编号 E###；运行后必须同步 data/emperors/*.yaml 的 card_id 回链，否则产品层引用断链。
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "content" / "sources"

# (person_id, title_substr) -> (year, date_note)  hard anchors from 本纪
YEAR_FIXES: dict[tuple[str, str], tuple[str, str]] = {
    ("e-han-guangwu", "封禅泰山"): ("56", "中元元年"),
    ("e-han-ming", "封东海公"): ("39", "建武十五年"),
    ("e-han-ming", "立为皇太子"): ("43", "建武十九年"),
    ("shu-zhaolie", "即皇帝位"): ("221", "章武元年四月"),
    ("shu-zhaolie", "伐吴"): ("221", "章武元年秋"),
    ("w-jin-hui", "赵王伦篡"): ("301", "永康二年"),
    ("w-jin-hui", "帝反正"): ("301", "永宁元年"),
    ("han-wu-di", "举贤良"): ("-141", "建元元年"),
    ("han-wu-di", "即位"): ("-141", "建元元年"),
    ("qin-shi-huang", "沙丘崩"): ("-210", "前210"),
    ("qin-shi-huang", "沙丘嗣位"): ("-210", "前210"),
}


def get_status(p: Path) -> str:
    for line in p.read_text(encoding="utf-8").splitlines()[:25]:
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return ""


def year_key(y: str) -> tuple[int, int]:
    if not y or y == "undated":
        return (1, 10**9)
    try:
        return (0, int(y))
    except ValueError:
        m = re.match(r"^-?\d+", y)
        if m:
            return (0, int(m.group(0)))
        return (1, 10**9)


def event_priority(title: str) -> int:
    """Lower = earlier within same year."""
    t = title
    rules = [
        (0, ("生", "出生", "生于")),
        (1, ("起兵", "义举", "举兵", "讨黄巾", "与黄巾")),
        (2, ("立为", "封", "太子", "亲政", "王冠", "称王", "汉中")),
        (3, ("即位", "称帝", "称始", "即皇帝", "受禅", "代汉", "鄗南")),
        (4, ("改元", "定都", "统一制度", "举贤良")),
        (5, ("篡", "废", "诛", "杀太子")),
        (6, ("反正", "还宫")),
        (7, ("失荆州", "关羽")),
        (8, ("伐", "征", "战", "破", "平", "灭")),
        (9, ("崩", "被弑", "被杀", "禅位", "逊位", "之死", "之变")),
        (10, ("嗣位", "托孤")),
        (11, ("总评", "史评", "政风", "对照", "肉糜")),
    ]
    for pri, keys in rules:
        for k in keys:
            if k in t:
                return pri
    return 7


def parse_card(path: Path) -> dict:
    t = path.read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    if t.startswith("---"):
        parts = t.split("---", 2)
        for line in parts[1].splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        body = parts[2] if len(parts) > 2 else ""
    else:
        body = t
    summary = ""
    if "## 史实摘要" in body:
        summary = body.split("## 史实摘要", 1)[1].split("##", 1)[0].strip()
    quote = ""
    if "## 自用要点" in body:
        quote = body.split("## 自用要点", 1)[1].split("##", 1)[0].strip()
    sources = []
    for a, b, c in re.findall(r"\| ([^|]+) \| ([^|]+) \| ([^|]*) \|", t):
        if a.strip() != "文献":
            sources.append((a.strip(), b.strip(), c.strip()))
    return {
        "meta": meta,
        "summary": summary,
        "quote": quote,
        "sources": sources,
        "raw": t,
    }


def write_card(path: Path, meta: dict, summary: str, quote: str, sources: list) -> None:
    rel = meta.get("related_ids", "[]")
    rows = "\n".join(f"| {a} | {b} | {c} |" for a, b, c in sources) or "| （待补） | | |"
    q = quote if quote and quote != "—" else "与本纪对读；争议见 06。"
    # 幂等:剥掉既往 -chrono/-sorted 尾链再补本次后缀(2026-08-13 修复)
    base_batch = re.sub(r"(?:-(?:chrono|sorted))+$", "", meta.get("batch", "benji-qa-fix"))
    rel_ids = re.findall(r'"([a-z0-9-]+)"', meta.get("related_ids", "[]"))
    rel_md = "\n".join(f"- [[{i}]]" for i in rel_ids) if rel_ids else "—"
    content = f"""---
eid: {meta['eid']}
person_id: "{meta.get('person_id','')}"
year: "{meta.get('year','undated')}"
date_note: "{meta.get('date_note','')}"
title: "{meta.get('title','')}"
on_map: {meta.get('on_map','maybe')}
route_group: "{meta.get('route_group','')}"
place_ancient: "{meta.get('place_ancient','')}"
place_id_candidate: "{meta.get('place_id_candidate','')}"
related_ids: {rel}
confidence: {meta.get('confidence','medium')}
enter_product: true
status: accepted
batch: {base_batch}-chrono
---

# {meta['eid']} · {meta.get('title','')}

## 史实摘要

{summary}

## 地点

- 古名：{meta.get('place_ancient') or '—'}
- place_id：{meta.get('place_id_candidate') or '—'}
- 上地图：{meta.get('on_map','maybe')}
- 路线组：{meta.get('route_group') or '—'}

## 关联人物

{rel_md}

## 出处

| 文献 | 篇卷 | 笔记 |
|------|------|------|
{rows}

## 自用要点

{q}

## 是否进入产品

- [x] timeline
- [x] bio
- [x] routes
- [ ] relations
"""
    path.write_text(content, encoding="utf-8")


def rebuild_index(pid: str, display: str, dynasty: str, cards: list[dict], map_n: int) -> None:
    rows = [
        f"| {c['eid']} | {c['year']} | {c['title']} | {c['on_map']} | {c['confidence']} | yes | `{c['fname']}` |"
        for c in cards
    ]
    text = f"""---
id: "{pid}"
display_name: "{display}"
status: dossier-complete
tier: emperor
dynasty: "{dynasty}"
updated: "2026-08-07"
batch: benji-qa-fix
---

# 史源卡 · {display}

> 本纪精读级 · **{len(cards)}** 条 · 2026-08-07 全量复核（编年排序 + 同年优先级 + 摘要补强）

## 0. 状态看板

| 项 | 状态 |
|----|------|
| 证据卡数量 | {len(cards)} |
| on_map=yes | {map_n} |
| 质量 | 编年已排序；同年内按事件类型优先级；弱摘要已加长 |

## 3. 证据卡索引

| eid | 年 | 标题 | on_map | confidence | enter_product | 文件 |
|-----|----|------|--------|------------|---------------|------|
{chr(10).join(rows)}

## 复核说明

- 卡序：公历年升序；同年按「生→起兵/封立→即位→要事→崩→总评」
- 史实以出处篇卷为准；年份锚点已与本纪对读修正（如光武封禅中元元年）
- 若与 scaffold 旧稿冲突，以本批为准
"""
    (SRC / pid / "00-史源卡.md").write_text(text, encoding="utf-8")
    (SRC / pid / "README.md").write_text(
        f"# {display} / `{pid}`\n\n- status: **dossier-complete**（qa-fix，{len(cards)} 条）\n",
        encoding="utf-8",
    )


def fix_person(pid: str) -> int:
    d = SRC / pid
    evid = d / "证据"
    display = pid
    dynasty = ""
    for line in (d / "00-史源卡.md").read_text(encoding="utf-8").splitlines()[:25]:
        if line.startswith("display_name:"):
            display = line.split(":", 1)[1].strip().strip('"')
        if line.startswith("dynasty:"):
            dynasty = line.split(":", 1)[1].strip().strip('"')

    items = []
    for f in evid.glob("E*.md"):
        if f.name == "_template.md":
            continue
        card = parse_card(f)
        meta = card["meta"]
        title = meta.get("title", f.stem)
        # apply year fixes
        for (pp, key), (yy, dn) in YEAR_FIXES.items():
            if pp == pid and key in title:
                meta["year"] = yy
                meta["date_note"] = dn
                # also fix summary if still says wrong 中元二年 for 封禅
                if key == "封禅泰山":
                    card["summary"] = card["summary"].replace("中元二年", "中元元年").replace(
                        "（同年崩）", "（翌年崩）"
                    )
        items.append(card)

    items.sort(
        key=lambda c: (
            year_key(c["meta"].get("year", "undated")),
            event_priority(c["meta"].get("title", "")),
            c["meta"].get("title", ""),
        )
    )

    for f in list(evid.glob("E*.md")):
        if f.name != "_template.md":
            f.unlink()

    out = []
    map_n = 0
    for i, card in enumerate(items, 1):
        eid = f"E{i:03d}"
        meta = dict(card["meta"])
        meta["eid"] = eid
        meta["person_id"] = pid
        title = meta.get("title", f"事件{i}")
        safe = re.sub(r'[\\/:*?"<>|]', "", title)[:40]
        fname = f"{eid}-{safe}.md"
        if meta.get("on_map") == "yes":
            map_n += 1
        write_card(evid / fname, meta, card["summary"], card["quote"], card["sources"])
        out.append(
            {
                "eid": eid,
                "year": meta.get("year", "undated"),
                "title": title,
                "on_map": meta.get("on_map", "maybe"),
                "confidence": meta.get("confidence", "medium"),
                "fname": fname,
            }
        )
    rebuild_index(pid, display, dynasty, out, map_n)
    return len(out)


def main():
    n_p = n_c = 0
    for d in sorted(SRC.iterdir()):
        if not d.is_dir() or not (d / "00-史源卡.md").exists():
            continue
        if get_status(d / "00-史源卡.md") != "dossier-complete":
            continue
        c = fix_person(d.name)
        n_p += 1
        n_c += c
        print("patched", d.name, c)
    print("persons", n_p, "cards", n_c)


if __name__ == "__main__":
    main()
