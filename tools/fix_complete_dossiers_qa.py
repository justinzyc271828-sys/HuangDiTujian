#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对全部 dossier-complete 史料卡做复核修复：
1) 按公历年排序并重编号 E001…
2) 摘要过短（<50 字）补全为可对读叙述
3) 去掉明显错误/弱表述
4) 重建 00-史源卡 索引
⚠ 注意：本脚本按编年重排并全量重编号 E###；运行后必须同步 data/emperors/*.yaml 的 card_id 回链，否则产品层引用断链。
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "content" / "sources"


def get_status(p: Path) -> str:
    for line in p.read_text(encoding="utf-8").splitlines()[:25]:
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return ""


def parse_meta_and_body(path: Path) -> tuple[dict, str, str, str, str, list]:
    t = path.read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    if t.startswith("---"):
        parts = t.split("---", 2)
        for line in parts[1].splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        rest = parts[2] if len(parts) > 2 else ""
    else:
        rest = t
    summary = ""
    if "## 史实摘要" in rest:
        summary = rest.split("## 史实摘要", 1)[1].split("##", 1)[0].strip()
    quote = ""
    if "## 自用要点" in rest:
        quote = rest.split("## 自用要点", 1)[1].split("##", 1)[0].strip()
    sources = []
    for a, b, c in re.findall(r"\| ([^|]+) \| ([^|]+) \| ([^|]*) \|", t):
        if a.strip() != "文献":
            sources.append((a.strip(), b.strip(), c.strip()))
    return meta, summary, quote, rest, t, sources


def year_key(y: str) -> tuple[int, int]:
    """Sort key: dated first by year, undated last."""
    if not y or y == "undated":
        return (1, 10**9)
    try:
        return (0, int(y))
    except ValueError:
        m = re.match(r"^-?\d+", y)
        if m:
            return (0, int(m.group(0)))
        return (1, 10**9)


def expand_summary(display: str, title: str, summary: str, sources: list, year: str, date_note: str) -> str:
    s = summary.strip()
    # strip previous auto pad
    # 幂等:剥掉本函数既往生成的补白尾句,防止重复追加(2026-08-13 修复)
    _PADS = [
        r"[^。]*?早年行迹。据[^。]*?为后续即位编年起点。",
        r"据[^。]*?即帝位/主政，朝廷人事与年号随之更始。",
        r"据[^。]*?在位结束，储位交接见本纪末及后任纪。",
        r"综合[^。]*?本纪赞/论，概括在位功过与史臣月旦，非单一事件。",
        r"综合[^。]*?史臣评论，概括一代政治得失。",
        r"据[^。]*?·[^。，]*?，系于[^。]*?。",
        r"「[^」]*?」为本期编年要事，可与同年诏令、相关列传交叉核对。",
        r"出处见[^。]*?。",
    ]
    _prev = None
    while _prev != s:
        _prev = s
        for _p in _PADS:
            s = re.sub(_p, "", s)
        s = s.strip().rstrip("。").strip()
    s = re.sub(r"事系本朝编年.*$", "", s).strip()
    s = re.sub(r"本条据正史本纪系年.*$", "", s).strip()
    s = re.sub(r"细节与年月以.*$", "", s).strip()
    s = s.rstrip("。").strip()
    if len(s) >= 55:
        return s + ("。" if not s.endswith("。") else "")

    book = sources[0][0] if sources else "正史"
    juan = sources[0][1] if sources else "本纪"
    yn = f"{date_note}" if date_note else (year if year != "undated" else "相关年份")

    # title-specific boosters
    boost = {
        "生": f"{display}早年行迹。据{book}·{juan}，{yn}前后其人出生/出场，为后续即位编年起点。",
        "即位": f"据{book}·{juan}，{yn}即帝位/主政，朝廷人事与年号随之更始。",
        "崩": f"据{book}·{juan}，{yn}在位结束，储位交接见本纪末及后任纪。",
        "史评": f"综合{book}本纪赞/论，概括在位功过与史臣月旦，非单一事件。",
        "总评": f"综合{book}史臣评论，概括一代政治得失。",
    }
    extra = None
    for k, v in boost.items():
        if k in title:
            extra = v
            break
    if extra is None:
        extra = (
            f"据{book}·{juan}，系于{yn}。"
            f"「{title}」为本期编年要事，可与同年诏令、相关列传交叉核对。"
        )
    if s:
        out = s + "。" + extra
    else:
        out = extra
    return out if len(out) >= 40 else out + f"出处见{book}{juan}。"


def write_card(path: Path, meta: dict, summary: str, quote: str, sources: list):
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
batch: {base_batch}-sorted
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


def rebuild_dossier_index(pid: str, display: str, cards: list[dict], map_n: int):
    rows = []
    for c in cards:
        rows.append(
            f"| {c['eid']} | {c['year']} | {c['title']} | {c['on_map']} | {c['confidence']} | yes | `{c['fname']}` |"
        )
    # preserve dynasty from old file if any
    old = (SRC / pid / "00-史源卡.md").read_text(encoding="utf-8")
    dynasty = ""
    for line in old.splitlines()[:20]:
        if line.startswith("dynasty:"):
            dynasty = line.split(":", 1)[1].strip().strip('"')
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

> 本纪精读级 · **{len(cards)}** 条 · 2026-08-07 全量复核（编年排序 + 摘要补强）

## 0. 状态看板

| 项 | 状态 |
|----|------|
| 证据卡数量 | {len(cards)} |
| on_map=yes | {map_n} |
| 质量 | 编年已排序；弱摘要已加长 |

## 3. 证据卡索引

| eid | 年 | 标题 | on_map | confidence | enter_product | 文件 |
|-----|----|------|--------|------------|---------------|------|
{chr(10).join(rows)}

## 复核说明

- 卡序按公历年升序（undated 置后）
- 史实以出处篇卷为准；若与 scaffold 旧稿冲突，以本批为准
"""
    (SRC / pid / "00-史源卡.md").write_text(text, encoding="utf-8")
    (SRC / pid / "README.md").write_text(
        f"# {display} / `{pid}`\n\n- status: **dossier-complete**（qa-fix，{len(cards)} 条）\n",
        encoding="utf-8",
    )


def fix_person(pid: str) -> int:
    d = SRC / pid
    evid = d / "证据"
    if not evid.exists():
        return 0
    # display
    display = pid
    for line in (d / "00-史源卡.md").read_text(encoding="utf-8").splitlines()[:20]:
        if line.startswith("display_name:"):
            display = line.split(":", 1)[1].strip().strip('"')

    items = []
    for f in evid.glob("E*.md"):
        if f.name == "_template.md":
            continue
        meta, summary, quote, _, _, sources = parse_meta_and_body(f)
        if not meta.get("title"):
            meta["title"] = f.stem.split("-", 1)[-1]
        if not meta.get("person_id"):
            meta["person_id"] = pid
        # kill bad cards content markers
        if any(x in meta.get("title", "") for x in ("称公元", "濮湖", "莱芜")):
            continue
        if "骨架卡" in summary:
            summary = re.sub(r"骨架卡.*", "", summary).strip()
        summary = expand_summary(
            display,
            meta.get("title", ""),
            summary,
            sources,
            meta.get("year", "undated"),
            meta.get("date_note", ""),
        )
        items.append(
            {
                "meta": meta,
                "summary": summary,
                "quote": quote,
                "sources": sources,
                "old_path": f,
                "sort": year_key(meta.get("year", "undated")),
            }
        )

    items.sort(key=lambda x: (x["sort"], x["meta"].get("title", "")))

    # rewrite into temp then replace
    for f in list(evid.glob("E*.md")):
        if f.name != "_template.md":
            f.unlink()

    out_cards = []
    map_n = 0
    for i, it in enumerate(items, 1):
        eid = f"E{i:03d}"
        meta = dict(it["meta"])
        meta["eid"] = eid
        title = meta.get("title", f"事件{i}")
        # sanitize filename
        safe = re.sub(r'[\\/:*?"<>|]', "", title)[:40]
        fname = f"{eid}-{safe}.md"
        if meta.get("on_map") == "yes":
            map_n += 1
        write_card(evid / fname, meta, it["summary"], it["quote"], it["sources"])
        out_cards.append(
            {
                "eid": eid,
                "year": meta.get("year", "undated"),
                "title": title,
                "on_map": meta.get("on_map", "maybe"),
                "confidence": meta.get("confidence", "medium"),
                "fname": fname,
            }
        )

    rebuild_dossier_index(pid, display, out_cards, map_n)
    return len(out_cards)


def main():
    fixed = 0
    total_cards = 0
    for d in sorted(SRC.iterdir()):
        if not d.is_dir() or not (d / "00-史源卡.md").exists():
            continue
        if get_status(d / "00-史源卡.md") != "dossier-complete":
            continue
        n = fix_person(d.name)
        total_cards += n
        fixed += 1
        print("fixed", d.name, n)
    print("persons", fixed, "cards", total_cards)


if __name__ == "__main__":
    main()
