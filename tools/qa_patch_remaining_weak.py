#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from upgrade_benji_dossiers import card

ROOT = Path(__file__).resolve().parents[1] / "content" / "sources"


def rewrite_file(
    pid,
    eid,
    title,
    year,
    date_note,
    summary,
    sources,
    quote,
    on_map="yes",
    place="洛阳",
    place_id="luoyang",
    conf="high",
    route="都城",
):
    evid = ROOT / pid / "证据"
    for f in evid.glob(f"{eid}-*.md"):
        f.unlink()
    md = card(
        eid,
        pid,
        year,
        date_note,
        title,
        summary,
        on_map,
        route,
        place,
        place_id,
        [],
        conf,
        sources,
        quote,
    )
    (evid / f"{eid}-{title}.md").write_text(md, encoding="utf-8")
    print("wrote", pid, eid, title)


def refresh_index(pid: str, display: str, src_a: str, juan: str):
    evid = ROOT / pid / "证据"
    rows = []
    map_n = 0
    files = sorted(
        [p for p in evid.glob("E*.md") if p.name != "_template.md"],
        key=lambda p: p.name,
    )
    for p in files:
        t = p.read_text(encoding="utf-8")
        meta = {}
        if t.startswith("---"):
            body = t.split("---", 2)[1]
            for line in body.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"')
        eid = meta.get("eid", p.stem[:4])
        year = meta.get("year", "")
        title = meta.get("title", p.stem.split("-", 1)[-1])
        om = meta.get("on_map", "maybe")
        conf = meta.get("confidence", "medium")
        if om == "yes":
            map_n += 1
        rows.append(
            f"| {eid} | {year} | {title} | {om} | {conf} | yes | `{p.name}` |"
        )
    n = len(rows)
    dossier = f"""---
id: "{pid}"
display_name: "{display}"
status: dossier-complete
tier: emperor
updated: "2026-08-07"
batch: benji-upgrade-qa
---

# 史源卡 · {display}

> 本纪精读级（QA 复核 {n} 条）。主据 {src_a} {juan}。

## 0. 状态看板

| 项 | 状态 |
|----|------|
| 证据卡 | {n} |
| on_map=yes | {map_n} |
| 质量 | 2026-08-07 复核 |

## 3. 证据卡索引

| eid | 年 | 标题 | on_map | confidence | enter_product | 文件 |
|-----|----|------|--------|------------|---------------|------|
{chr(10).join(rows)}
"""
    (ROOT / pid / "00-史源卡.md").write_text(dossier, encoding="utf-8")
    print("index", pid, n)


def main():
    rewrite_file(
        "e-han-he",
        "E008",
        "永元九年蝗灾求言",
        "97",
        "永元九年",
        "永元九年京师及郡国蝗，诏举有道；窦太后崩前后，和帝亲政后仍以灾异求言恤民。",
        [("后汉书", "卷004·孝和帝纪", "永元九年")],
        "以民生诏令取代纯太后崩弱卡。",
    )
    rewrite_file(
        "e-han-an",
        "E012",
        "安帝朝羌乱边费",
        "108",
        "永初二年",
        "先零羌等大叛，边郡残破，汉连年发兵，国用空竭，为安帝朝最重边患。",
        [("后汉书", "卷005·孝安帝纪", "羌"), ("后汉书", "西羌传", "对照")],
        "边费与羌乱。",
    )
    rewrite_file(
        "han-ai-di",
        "E007",
        "策免三公求直言",
        "-2",
        "元寿元年",
        "日食等灾异后，哀帝策免丞相孔光等，下诏求直言。时董贤贵宠，朝政乖剌。",
        [("汉书", "卷011·哀帝纪", "元寿元年")],
        "灾异绑定人事。",
        place="长安",
        place_id="chang-an",
    )
    rewrite_file(
        "han-cheng-di",
        "E007",
        "罢昌陵",
        "-20",
        "鸿嘉永始间",
        "成帝营昌陵，功费甚巨，后罢昌陵还复延陵，吏民称便。",
        [("汉书", "卷010·成帝纪", "罢昌陵")],
        "陵制与财政。",
        place="长安",
        place_id="chang-an",
        conf="medium",
    )
    rewrite_file(
        "e-han-chong",
        "E006",
        "梁冀立质帝",
        "145",
        "永嘉元年",
        "冲帝崩，梁太后与梁冀定策，迎立渤海孝王鸿子刘缵，是为质帝。",
        [("后汉书", "卷006", "立质帝"), ("后汉书", "梁冀传", "对照")],
        "继统。",
    )
    rewrite_file(
        "e-han-shang",
        "E006",
        "邓后定策立安帝",
        "106",
        "延平元年",
        "殇帝崩，邓太后与兄邓骘定策禁中，迎清河王子祜，是为安帝。",
        [("后汉书", "卷005", "迎立"), ("后汉书", "皇后纪", "邓")],
        "继统。",
    )
    rewrite_file(
        "e-han-shao-bei",
        "E006",
        "十九侯迎立顺帝",
        "125",
        "延光四年",
        "北乡侯薨，中黄门孙程等十九人斩江京，迎济阴王保，是为顺帝。",
        [("后汉书", "卷006", "迎立"), ("后汉书", "宦者传", "孙程")],
        "宦官定策。",
    )

    for pid, disp, sa, j in [
        ("e-han-he", "汉和帝", "后汉书", "卷004"),
        ("e-han-an", "汉安帝", "后汉书", "卷005"),
        ("han-ai-di", "汉哀帝", "汉书", "卷011"),
        ("han-cheng-di", "汉成帝", "汉书", "卷010"),
        ("e-han-chong", "汉冲帝", "后汉书", "卷006"),
        ("e-han-shang", "汉殇帝", "后汉书", "卷004"),
        ("e-han-shao-bei", "北乡侯", "后汉书", "卷006"),
        ("han-wen-di", "汉文帝", "汉书", "卷004"),
        ("han-jing-di", "汉景帝", "汉书", "卷005"),
        ("han-zhao-di", "汉昭帝", "汉书", "卷007"),
        ("han-ping-di", "汉平帝", "汉书", "卷012"),
        ("e-han-ming", "汉明帝", "后汉书", "卷002"),
    ]:
        refresh_index(pid, disp, sa, j)

    bad = []
    for d in ROOT.iterdir():
        if not d.is_dir():
            continue
        z = d / "00-史源卡.md"
        if not z.exists():
            continue
        h = z.read_text(encoding="utf-8")[:400]
        if "dossier-complete" not in h:
            continue
        if not (d.name.startswith("han-") or d.name.startswith("e-han-")):
            continue
        if d.name in ("han-gao-wu", "han-yin"):
            continue
        for f in (d / "证据").glob("E*.md"):
            t = f.read_text(encoding="utf-8")
            if any(x in t for x in ("称公元", "骨架卡", "濮湖", "莱芜", "optional")):
                bad.append(str(f.relative_to(ROOT)))
    print("REMAINING_BAD", bad)
    print("e-han-an", len(list((ROOT / "e-han-an" / "证据").glob("E*.md"))))


if __name__ == "__main__":
    main()
