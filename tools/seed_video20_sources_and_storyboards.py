#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 video-01 先导二十人：
1) 补建 content/sources/{id}/ 史源卡 + 核心史料卡（已有 dossier-complete 的三人跳过证据写入）
2) 写入 content/video/video-01/ 系列规范 + 二十人分镜文稿

安全保险（2026-08-09 事故后加装）：默认 dry-run 只打印不写盘；
--apply 才写入，且跳过任何已存在的文件（种子脚本绝不允许覆盖已策展内容）；
--force 才允许覆盖。曾一次性把 17 人本纪级 dossier 盖成 6 条薄模板。
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "content" / "sources"
VID = ROOT / "content" / "video" / "video-01"
REF_WB = ROOT / "HuangDiTujian-Ref" / "11-史料卡工作台"

# 已有完整 12 条证据的三人
ALREADY_COMPLETE = {"qin-shi-huang", "han-wu-di", "tang-tai-zong"}


def _install_write_guard(apply: bool, force: bool) -> dict:
    """给本脚本所有 Path.write_text 加保险。

    - 默认（无参数）:dry-run,只打印计划写入的路径，一个字节都不落盘;
    - --apply:真正写入，但目标文件已存在则跳过（种子只补缺失，绝不覆盖已策展内容）;
    - --force:允许覆盖已存在文件（仅在确知后果时使用）。

    通过包装 Path.write_text 实现，覆盖脚本内现有及未来新增的全部写入点。
    返回统计 dict,运行结束可打印汇总。
    """
    original_write_text = Path.write_text
    stats = {"written": 0, "skipped": 0, "planned": 0}

    def guarded_write_text(self: Path, data, *args, **kwargs):
        if not apply:
            stats["planned"] += 1
            print(f"[dry-run] would write {self}")
            return len(data)
        if not force and self.exists():
            stats["skipped"] += 1
            print(f"[skip] already exists (use --force to overwrite): {self}")
            return len(data)
        stats["written"] += 1
        return original_write_text(self, data, *args, **kwargs)

    Path.write_text = guarded_write_text
    return stats


def card_md(
    eid,
    person_id,
    year,
    date_note,
    title,
    summary,
    on_map,
    route_group,
    place,
    place_id,
    related,
    confidence,
    sources,
    quote,
    enter=True,
):
    related_s = "[" + ", ".join(f'"{x}"' for x in related) + "]"
    lines = [
        "---",
        f"eid: {eid}",
        f'person_id: "{person_id}"',
        f'year: "{year}"',
        f'date_note: "{date_note}"',
        f'title: "{title}"',
        f"on_map: {on_map}",
        f'route_group: "{route_group}"',
        f'place_ancient: "{place}"',
        f'place_id_candidate: "{place_id}"',
        f"related_ids: {related_s}",
        f"confidence: {confidence}",
        f"enter_product: {'true' if enter else 'false'}",
        "status: accepted",
        "batch: video-01",
        "---",
        "",
        f"# {eid} · {title}",
        "",
        "## 史实摘要",
        "",
        summary,
        "",
        "## 地点",
        "",
        f"- 古名：{place or '—'}",
        f"- place_id：{place_id or '—'}",
        f"- 上地图：{on_map}",
        f"- 路线组：{route_group or '—'}",
        "",
        "## 关联人物",
        "",
        (", ".join(related) if related else "—"),
        "",
        "## 出处",
        "",
        "| 文献 | 篇卷 | 笔记 |",
        "|------|------|------|",
    ]
    for a, b, c in sources:
        lines.append(f"| {a} | {b} | {c} |")
    lines += [
        "",
        "## 自用要点",
        "",
        quote,
        "",
        "## 是否进入产品",
        "",
        "- [x] timeline" if enter else "- [ ] timeline",
        "- [x] bio" if enter else "- [ ] bio",
        "- [x] routes" if on_map == "yes" and enter else "- [ ] routes",
        "- [ ] relations",
        "",
        "> video-01 先导包：先服务分镜与六维，正式 dossier-complete 可再扩至 12 条。",
        "",
    ]
    return "\n".join(lines)


def write_scaffold(pid: str, meta: dict, events: list):
    d = SRC / pid
    evid = d / "证据"
    excerpt = d / "摘录"
    evid.mkdir(parents=True, exist_ok=True)
    excerpt.mkdir(parents=True, exist_ok=True)
    (excerpt / ".gitkeep").write_text("", encoding="utf-8")
    (evid / "_template.md").write_text(
        (SRC / "_templates" / "史料卡.template.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    index_rows = []
    map_n = 0
    for i, e in enumerate(events, 1):
        eid = f"E{i:03d}"
        title = e["title"]
        fname = f"{eid}-{title}.md"
        on_map = e.get("on_map", "maybe")
        if on_map == "yes":
            map_n += 1
        md = card_md(
            eid=eid,
            person_id=pid,
            year=e["year"],
            date_note=e["date_note"],
            title=title,
            summary=e["summary"],
            on_map=on_map,
            route_group=e.get("route_group", ""),
            place=e.get("place", ""),
            place_id=e.get("place_id", ""),
            related=e.get("related", []),
            confidence=e.get("confidence", "high"),
            sources=e["sources"],
            quote=e.get("quote", ""),
            enter=e.get("enter", True),
        )
        (evid / fname).write_text(md, encoding="utf-8")
        index_rows.append(
            f"| {eid} | {e['year']} | {title} | {on_map} | {e.get('confidence','high')} | yes | `{fname}` |"
        )

    dossier = f"""---
id: "{pid}"
display_name: "{meta['display']}"
status: in-progress
tier: {meta.get('tier', 'emperor')}
dynasty: "{meta.get('dynasty', '')}"
updated: "2026-08-06"
batch: video-01
---

# 史源卡 · {meta['display']}

> video-01 先导包：核心史料卡 {len(events)} 条，服务分镜与六维；后续可扩至 12 条达 dossier-complete。

## 0. 状态看板

| 项 | 状态 |
|----|------|
| 材料包 | ☑ in-progress（video-01） |
| 证据卡数量 | {len(events)} |
| 可上地图条数 | {map_n} |
| 产品 YAML | ☐ 未建 / draft |
| 画像 | 暂缓 |
| 分镜文稿 | `content/video/video-01/分镜/{pid}.md` |

## 1. 身份速查

| 字段 | 内容 |
|------|------|
| id | `{pid}` |
| 显示名 | {meta['display']} |
| 姓名 | {meta.get('personal', '')} |
| 四字号 | {meta.get('epithet', '')} |
| 王朝 | {meta.get('dynasty', '')} |
| 记忆点 | {meta.get('memory', '')} |
| 在位/称制 | {meta.get('reign', '')} |
| 都城 | {meta.get('capital', '')} |

## 2. 主文献地图

| 优先级 | 文献 | 篇卷 | 用途 |
|--------|------|------|------|
| A | {meta.get('src_a', '')} | {meta.get('src_a_juan', '')} | 主叙事 |
| B | {meta.get('src_b', '资治通鉴')} | {meta.get('src_b_juan', '待标卷')} | 编年 |
| E | 谭图 / CHGIS | — | 地点 |

本地全文：`HuangDiTujian-Ref/01-史书全文与扫描/二十四史-简体/` · 通鉴-简体

## 3. 证据卡索引

| eid | 年 | 标题 | on_map | confidence | enter_product | 文件 |
|-----|----|------|--------|------------|---------------|------|
{chr(10).join(index_rows)}

## 4. 争议与待考（摘要）

{meta.get('disputes', '- 见 06-争议与待考.md')}

## 5. 下一步

1. 分镜定稿后按镜头补原文短摘  
2. 扩证据至 ≥12 条 → dossier-complete  
3. 同步 `data/emperors/{pid}.yaml` + bio  
"""
    (d / "00-史源卡.md").write_text(dossier, encoding="utf-8")

    (d / "01-阅读顺序.md").write_text(
        f"""# 阅读顺序 · {meta['display']}

1. {meta.get('src_a', '正史本纪')}（A 级）
2. 通鉴对应年段（B 级）
3. 本夹 `证据/` 已有条目核对
4. 争议条见 `06-争议与待考.md`
""",
        encoding="utf-8",
    )
    (d / "02-书目清单.md").write_text(
        f"""# 书目 · {meta['display']}

| 级别 | 书 | 状态 |
|------|-----|------|
| A | {meta.get('src_a', '')} {meta.get('src_a_juan', '')} | 库内 md 可检索 |
| B | {meta.get('src_b', '资治通鉴')} | 库内 md |
| F | 通行通史对照 | 可选 |
""",
        encoding="utf-8",
    )
    places = meta.get("places", [])
    place_lines = ["| 古名 | 今地猜想 | place_id 候选 | 备注 |", "|------|----------|---------------|------|"]
    for p in places:
        place_lines.append(f"| {p[0]} | {p[1]} | {p[2]} | {p[3]} |")
    (d / "03-地点候选表.md").write_text(
        f"# 地点候选 · {meta['display']}\n\n" + "\n".join(place_lines) + "\n",
        encoding="utf-8",
    )
    rels = meta.get("relations", [])
    rel_lines = ["| 关系 | 人物 | 备注 |", "|------|------|------|"]
    for r in rels:
        rel_lines.append(f"| {r[0]} | {r[1]} | {r[2]} |")
    (d / "04-关联人物候选表.md").write_text(
        f"# 关联人物 · {meta['display']}\n\n" + "\n".join(rel_lines) + "\n",
        encoding="utf-8",
    )
    (d / "05-路线草稿.md").write_text(
        f"""# 路线草稿 · {meta['display']}

适合上地图的节点（video-01）：

{meta.get('routes_note', '- 见证据卡 on_map=yes 条目')}
""",
        encoding="utf-8",
    )
    (d / "06-争议与待考.md").write_text(
        f"""# 争议与待考 · {meta['display']}

{meta.get('disputes', '暂无单列重大争议；月旦与后效分离见 video20.json score_note。')}
""",
        encoding="utf-8",
    )
    (d / "README.md").write_text(
        f"""# {meta['display']} / `{pid}`

- status: **in-progress**（video-01 核心 {len(events)} 条）
- 史源卡：`00-史源卡.md`
- 分镜：`../../video/video-01/分镜/{pid}.md`
""",
        encoding="utf-8",
    )

    # 工作台锚点
    REF_WB.mkdir(parents=True, exist_ok=True)
    (REF_WB / f"{pid}.md").write_text(
        f"""# 史料卡工作台 · {meta['display']}

- 正式证据：`content/sources/{pid}/证据/`
- 史源总台：`content/sources/{pid}/00-史源卡.md`
- 分镜：`content/video/video-01/分镜/{pid}.md`
- A 级：{meta.get('src_a', '')} {meta.get('src_a_juan', '')}
""",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# 17 人事件数据（三人已有完整包则不写入）
# ---------------------------------------------------------------------------

PEOPLE = {
    "han-xuan-di": {
        "meta": {
            "display": "汉宣帝",
            "personal": "刘询（病已）",
            "epithet": "综核名实",
            "dynasty": "西汉",
            "tier": "emperor",
            "memory": "地节亲政 / 昭宣气象",
            "reign": "前74–前49",
            "capital": "长安",
            "src_a": "汉书",
            "src_a_juan": "卷008·宣帝纪",
            "src_b": "资治通鉴",
            "src_b_juan": "汉纪·昭宣段",
            "places": [
                ("长安", "西安", "chang-an", "都城"),
                ("民间/掖庭", "西安一带", "chang-an", "早年"),
            ],
            "relations": [
                ("前朝权臣", "霍光", "迎立与霍氏之诛"),
                ("匈奴", "呼韩邪单于", "臣汉叙事"),
            ],
            "routes_note": "- 长安都城线\n- 匈奴入朝/边事线（概念图）",
            "disputes": "- 「昭宣中兴」评价口径不一，本卡取综核名实为主标签。\n- 霍光功过与宣帝权术并读。",
        },
        "events": [
            {
                "year": "-91",
                "date_note": "巫蛊后",
                "title": "民间长养",
                "summary": "巫蛊之祸后皇曾孙病已养于民间，后入掖庭，经历底层与宫廷边缘。",
                "on_map": "yes",
                "route_group": "流徙",
                "place": "长安民间/掖庭",
                "place_id": "chang-an",
                "sources": [("汉书", "卷008·宣帝纪", "早年经历")],
                "quote": "自民间来，知闾里奸邪、吏治得失。",
            },
            {
                "year": "-74",
                "date_note": "元平元年",
                "title": "霍光迎立",
                "summary": "昌邑王废后，霍光等迎立皇曾孙即位，是为宣帝。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "长安",
                "place_id": "chang-an",
                "related": [],
                "sources": [("汉书", "卷008·宣帝纪", "即位"), ("汉书", "卷068·霍光传", "废立")],
                "quote": "迎立场面是权臣政治峰值。",
            },
            {
                "year": "-68",
                "date_note": "地节二年",
                "title": "霍光薨逝",
                "summary": "霍光死，宣帝逐步收回权柄，进入亲政前夜。",
                "on_map": "no",
                "route_group": "",
                "place": "长安",
                "place_id": "chang-an",
                "sources": [("汉书", "卷068·霍光传", "地节二年")],
                "quote": "权臣时代结束的拐点。",
            },
            {
                "year": "-66",
                "date_note": "地节四年",
                "title": "诛霍氏",
                "summary": "霍禹等谋反事败，霍氏灭族，宣帝真正亲政，史称综核名实之始。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "长安",
                "place_id": "chang-an",
                "sources": [("汉书", "卷008·宣帝纪", "地节四年"), ("汉书", "卷068·霍光传", "霍禹")],
                "quote": "四字号「综核名实」的政治前提。",
            },
            {
                "year": "-60",
                "date_note": "神爵二年",
                "title": "西域都护",
                "summary": "郑吉并护南北道，号都护，汉在西域制度化驻节。",
                "on_map": "yes",
                "route_group": "拓边",
                "place": "西域",
                "place_id": "hexi",
                "sources": [("汉书", "卷070·郑吉传", "都护"), ("汉书", "卷096·西域传", "建置")],
                "quote": "武功在宣帝朝的制度落点。",
            },
            {
                "year": "-51",
                "date_note": "甘露三年",
                "title": "呼韩邪朝汉",
                "summary": "呼韩邪单于入朝称臣，匈汉关系进入新阶段，边事叙事高峰。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "长安",
                "place_id": "chang-an",
                "sources": [("汉书", "卷008·宣帝纪", "甘露三年"), ("汉书", "卷094·匈奴传", "呼韩邪")],
                "quote": "昭宣气象的视觉名场面。",
            },
            {
                "year": "-49",
                "date_note": "黄龙元年",
                "title": "宣帝崩",
                "summary": "宣帝崩，元帝即位；昭宣积累的吏治与边防格局转入下一朝。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "长安",
                "place_id": "chang-an",
                "sources": [("汉书", "卷008·宣帝纪", "黄龙元年")],
                "quote": "国祚与后效交接。",
            },
            {
                "year": "undated",
                "date_note": "施政总评",
                "title": "综核名实",
                "summary": "信赏必罚、察吏治、抑虚名，形成与武帝开边不同的「收束型」中兴路径。",
                "on_map": "no",
                "route_group": "",
                "place": "",
                "place_id": "",
                "sources": [("汉书", "卷008·宣帝纪", "赞"), ("资治通鉴", "汉纪", "史臣评")],
                "quote": "六维高分在文治·韬略，非拓边口号。",
                "confidence": "medium",
            },
        ],
    },
    "xin-wang-mang": {
        "meta": {
            "display": "新帝王莽",
            "personal": "王莽",
            "epithet": "以儒窃国",
            "dynasty": "新",
            "tier": "quasi",
            "memory": "始建国元年（9）",
            "reign": "9–23",
            "capital": "常安（长安）",
            "src_a": "汉书",
            "src_a_juan": "卷099·王莽传",
            "places": [("长安/常安", "西安", "chang-an", "都城"), ("渐台", "西安汉城遗址一带", "chang-an", "死地")],
            "relations": [("前朝", "汉元后/成哀平", "外戚路径"), ("对手", "刘秀等", "新亡汉兴")],
            "disputes": "- 「篡贼」与「理想主义改革者」两极评价；本项目月旦取负，后效保留改制讨论价值。",
        },
        "events": [
            {
                "year": "1",
                "date_note": "元始中",
                "title": "安汉公",
                "summary": "以外戚与儒学声望累迁，受封安汉公，掌控朝政。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "长安",
                "place_id": "chang-an",
                "sources": [("汉书", "卷099·王莽传", "安汉公")],
                "quote": "以儒入局。",
            },
            {
                "year": "6",
                "date_note": "居摄元年",
                "title": "居摄称制",
                "summary": "平帝死后立孺子婴，王莽居摄，行周公故事，加号假皇帝。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "长安",
                "place_id": "chang-an",
                "sources": [("汉书", "卷099·王莽传", "居摄")],
                "quote": "假周公叙事。",
            },
            {
                "year": "9",
                "date_note": "始建国元年",
                "title": "代汉称帝",
                "summary": "废孺子婴，建国号新，改元始建国，是为新朝。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "长安",
                "place_id": "chang-an",
                "sources": [("汉书", "卷099·王莽传", "始建国")],
                "quote": "记忆点：始建国元年。",
            },
            {
                "year": "9",
                "date_note": "始建国年间",
                "title": "托古改制",
                "summary": "行王田、禁奴婢、屡改货币官名，托《周礼》等经典，社会震荡剧烈。",
                "on_map": "no",
                "route_group": "",
                "place": "常安",
                "place_id": "chang-an",
                "sources": [("汉书", "卷099·王莽传", "王田奴婢货币")],
                "quote": "后效在「改制讨论」不在成功。",
            },
            {
                "year": "17",
                "date_note": "天凤中",
                "title": "绿林赤眉",
                "summary": "民变蜂起，绿林、赤眉等起兵，新朝控制力崩解。",
                "on_map": "maybe",
                "route_group": "其他",
                "place": "荆州/青徐一带",
                "place_id": "",
                "sources": [("汉书", "卷099·王莽传", "民变"), ("后汉书", "卷011", "刘玄等")],
                "quote": "国祚崩盘前兆。",
                "confidence": "medium",
            },
            {
                "year": "23",
                "date_note": "地皇四年",
                "title": "昆阳新败",
                "summary": "新军大败于昆阳，洛阳等地动摇，新朝军事崩溃。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "昆阳",
                "place_id": "",
                "related": ["e-han-guangwu"],
                "sources": [("后汉书", "卷001·光武帝纪", "昆阳"), ("汉书", "卷099·王莽传", "败讯")],
                "quote": "与光武昆阳对打的一张卡。",
            },
            {
                "year": "23",
                "date_note": "地皇四年",
                "title": "渐台之死",
                "summary": "更始军入长安，王莽死于渐台，新亡。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "长安渐台",
                "place_id": "chang-an",
                "sources": [("汉书", "卷099·王莽传", "渐台")],
                "quote": "以儒窃国终局。",
            },
        ],
    },
    "e-han-guangwu": {
        "meta": {
            "display": "汉光武帝",
            "personal": "刘秀",
            "epithet": "昆阳一旅",
            "dynasty": "东汉",
            "tier": "emperor",
            "memory": "昆阳之战",
            "reign": "25–57",
            "capital": "洛阳",
            "src_a": "后汉书",
            "src_a_juan": "卷001·光武帝纪",
            "places": [
                ("舂陵", "湖北枣阳一带", "", "起兵"),
                ("昆阳", "河南叶县", "", "名战"),
                ("洛阳", "洛阳", "luoyang", "都城"),
            ],
            "relations": [("对手", "王莽", "新汉"), ("将", "云台诸将", "中兴班底")],
            "disputes": "- 「柔道」与度田之争；总体月旦正面。",
        },
        "events": [
            {
                "year": "22",
                "date_note": "地皇三年",
                "title": "舂陵起兵",
                "summary": "与宗室宾客起兵于舂陵，卷入反新浪潮。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "舂陵",
                "place_id": "",
                "sources": [("后汉书", "卷001·光武帝纪", "起兵")],
                "quote": "中兴起点。",
            },
            {
                "year": "23",
                "date_note": "地皇四年",
                "title": "昆阳之战",
                "summary": "以少击众大破新军于昆阳，奠定刘秀军事声望。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "昆阳",
                "place_id": "",
                "related": ["xin-wang-mang"],
                "sources": [("后汉书", "卷001·光武帝纪", "昆阳")],
                "quote": "四字号记忆核。",
            },
            {
                "year": "24",
                "date_note": "更始中",
                "title": "定河北",
                "summary": "渡河经营河北，收揽人才，与更始政权渐行渐远。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "河北",
                "place_id": "handan",
                "sources": [("后汉书", "卷001·光武帝纪", "河北")],
                "quote": "韬略面：根据地。",
            },
            {
                "year": "25",
                "date_note": "建武元年",
                "title": "鄗南称帝",
                "summary": "即皇帝位，建元建武，东汉开始。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "鄗",
                "place_id": "",
                "sources": [("后汉书", "卷001·光武帝纪", "建武元年")],
                "quote": "国号汉续。",
            },
            {
                "year": "36",
                "date_note": "建武十二年",
                "title": "统一大致完成",
                "summary": "平公孙述等，全国粗定，中兴局面落定。",
                "on_map": "maybe",
                "route_group": "亲征",
                "place": "巴蜀等",
                "place_id": "",
                "sources": [("后汉书", "卷001·光武帝纪", "平蜀")],
                "quote": "武功收束。",
                "confidence": "medium",
            },
            {
                "year": "undated",
                "date_note": "建武年间",
                "title": "柔道与退功臣",
                "summary": "崇尚柔道、退功臣进文吏，云台图像功臣而不使揽政，塑造中兴政风。",
                "on_map": "no",
                "route_group": "",
                "place": "洛阳",
                "place_id": "luoyang",
                "sources": [("后汉书", "卷001·光武帝纪", "赞与政风"), ("后汉书", "卷022", "云台")],
                "quote": "文治高分来源。",
            },
            {
                "year": "57",
                "date_note": "中元二年",
                "title": "光武崩",
                "summary": "崩于洛阳，明帝继位，东汉国祚延续。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "洛阳",
                "place_id": "luoyang",
                "sources": [("后汉书", "卷001·光武帝纪", "中元二年")],
                "quote": "国祚评分支撑。",
            },
        ],
    },
    "h-zhao-shi-le": {
        "meta": {
            "display": "后赵石勒",
            "personal": "石勒",
            "epithet": "奴隶天子",
            "dynasty": "后赵",
            "tier": "quasi",
            "memory": "襄国称赵",
            "reign": "319–333（赵王/帝）",
            "capital": "襄国",
            "src_a": "晋书",
            "src_a_juan": "卷104–105·石勒载记",
            "places": [("襄国", "河北邢台", "", "都"), ("邺", "河北临漳", "", "后重心")],
            "relations": [("谋主", "张宾", "右侯"), ("后继", "石虎", "暴政对照")],
            "disputes": "- 胡汉关系与残暴记载需分「本人/石虎」；史家仍称其雄略。",
        },
        "events": [
            {
                "year": "303",
                "date_note": "约永兴前后",
                "title": "被掠为奴",
                "summary": "羯人石勒少时被掠卖为奴，后聚众起兵，是十六国最戏剧性的社会流动叙事。",
                "on_map": "maybe",
                "route_group": "流徙",
                "place": "并州一带",
                "place_id": "",
                "sources": [("晋书", "卷104·石勒载记", "早年")],
                "quote": "奴隶天子起点。",
                "confidence": "medium",
            },
            {
                "year": "308",
                "date_note": "永嘉前后",
                "title": "依附汉赵",
                "summary": "一度归刘渊、刘聪系统，在华北作战中积累实力。",
                "on_map": "maybe",
                "route_group": "亲征",
                "place": "河北/河南",
                "place_id": "",
                "sources": [("晋书", "卷104·石勒载记", "从汉")],
                "quote": "借壳壮大。",
                "confidence": "medium",
            },
            {
                "year": "319",
                "date_note": "太兴二年",
                "title": "襄国称赵",
                "summary": "称赵王，都襄国，后赵政权成立，脱离前赵阴影。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "襄国",
                "place_id": "",
                "sources": [("晋书", "卷104·石勒载记", "称赵王")],
                "quote": "记忆点。",
            },
            {
                "year": "329",
                "date_note": "咸和四年",
                "title": "灭前赵",
                "summary": "破刘曜，灭前赵，北方大部归后赵。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "洛阳/关中一线",
                "place_id": "luoyang",
                "sources": [("晋书", "卷105·石勒载记", "灭刘曜")],
                "quote": "武功峰值。",
            },
            {
                "year": "330",
                "date_note": "咸和五年",
                "title": "称帝",
                "summary": "称皇帝，后赵帝制完备。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "襄国",
                "place_id": "",
                "sources": [("晋书", "卷105·石勒载记", "称帝")],
                "quote": "奴隶到天子完成式。",
            },
            {
                "year": "undated",
                "date_note": "在位间",
                "title": "重用张宾",
                "summary": "以张宾为谋主，兴学校、定制度，胡汉分治中有秩序建设。",
                "on_map": "no",
                "route_group": "",
                "place": "襄国",
                "place_id": "",
                "sources": [("晋书", "卷105·石勒载记", "张宾")],
                "quote": "文治与韬略分。",
            },
            {
                "year": "333",
                "date_note": "咸和八年",
                "title": "石勒崩",
                "summary": "勒崩，石弘继而石虎夺位，后赵政治迅速恶化。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "襄国",
                "place_id": "",
                "sources": [("晋书", "卷105·石勒载记", "崩")],
                "quote": "国祚低：身后不稳。",
            },
        ],
    },
    "liang-wu": {
        "meta": {
            "display": "梁武帝",
            "personal": "萧衍",
            "epithet": "皇帝菩萨",
            "dynasty": "梁",
            "tier": "emperor",
            "memory": "舍身同泰 / 侯景之乱",
            "reign": "502–549",
            "capital": "建康",
            "src_a": "梁书",
            "src_a_juan": "卷001–003·武帝纪",
            "src_b": "南史",
            "places": [("建康", "南京", "", "都"), ("同泰寺", "南京", "", "舍身"), ("台城", "南京", "", "饿死")],
            "relations": [("叛将", "侯景", "乱梁"), ("文化", "昭明太子等", "文治面")],
            "disputes": "- 前半英主/后半佞佛与侯景；月旦取中。",
        },
        "events": [
            {
                "year": "501",
                "date_note": "中兴元年",
                "title": "起兵建康",
                "summary": "自襄阳东下攻入建康，掌控南齐残局。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "建康",
                "place_id": "",
                "sources": [("梁书", "卷001·武帝纪", "起兵")],
                "quote": "开国武戏。",
            },
            {
                "year": "502",
                "date_note": "天监元年",
                "title": "受禅建梁",
                "summary": "齐禅于梁，萧衍即帝位，梁朝建立。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "建康",
                "place_id": "",
                "sources": [("梁书", "卷001·武帝纪", "受禅")],
                "quote": "国祚起点。",
            },
            {
                "year": "undated",
                "date_note": "天监–大同",
                "title": "文化全盛",
                "summary": "长年安定，文学、佛学、礼乐兴盛，南朝文化高峰之一。",
                "on_map": "no",
                "route_group": "",
                "place": "建康",
                "place_id": "",
                "sources": [("梁书", "卷003·武帝纪", "史臣对文治"), ("南史", "梁本纪", "文化")],
                "quote": "文治分来源。",
                "confidence": "medium",
            },
            {
                "year": "527",
                "date_note": "大通元年等",
                "title": "舍身同泰",
                "summary": "数次舍身同泰寺，群臣以钱奉赎，佛事与财政绑定，成史著名场面。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "同泰寺",
                "place_id": "",
                "sources": [("梁书", "卷003·武帝纪", "舍身"), ("南史", "梁本纪中", "同泰")],
                "quote": "四字号「皇帝菩萨」。",
            },
            {
                "year": "548",
                "date_note": "太清二年",
                "title": "纳侯景",
                "summary": "接受侯景，旋即爆发侯景之乱，建康遭灾。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "建康",
                "place_id": "",
                "sources": [("梁书", "卷003·武帝纪", "太清"), ("梁书", "卷056·侯景传", "乱")],
                "quote": "战略误判。",
            },
            {
                "year": "549",
                "date_note": "太清三年",
                "title": "台城饿死",
                "summary": "台城陷后，武帝被制，忧愤饥病而崩。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "台城",
                "place_id": "",
                "sources": [("梁书", "卷003·武帝纪", "崩"), ("南史", "梁本纪中", "台城")],
                "quote": "月旦下坠终点。",
            },
        ],
    },
    "xixia-li-yuanhao": {
        "meta": {
            "display": "西夏景宗",
            "personal": "李元昊（嵬名曩霄）",
            "epithet": "河西称制",
            "dynasty": "西夏",
            "tier": "quasi",
            "memory": "1038称帝",
            "reign": "1038–1048",
            "capital": "兴庆府",
            "src_a": "宋史",
            "src_a_juan": "卷485–486·夏国传",
            "src_b": "辽史/续资治通鉴长编（二手入口）",
            "places": [("兴庆", "银川", "", "都"), ("好水川", "宁夏隆德一带", "", "大胜宋")],
            "relations": [("宋", "宋仁宗", "和战"), ("辽", "辽兴宗", "三角")],
            "disputes": "- 宋辽史书站位偏贬；本项目月旦取中。西夏文创制细节待补专书。",
        },
        "events": [
            {
                "year": "1032",
                "date_note": "明道元年",
                "title": "袭夏王位",
                "summary": "李德明卒，元昊嗣位，加速去宋化与民族国家建构。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "兴庆府",
                "place_id": "",
                "sources": [("宋史", "卷485·夏国传", "嗣位")],
                "quote": "称帝前夜。",
            },
            {
                "year": "1034",
                "date_note": "约景祐前后",
                "title": "创制西夏文",
                "summary": "命野利仁荣等造番书（西夏文），改服饰官制，强化主体性。",
                "on_map": "no",
                "route_group": "",
                "place": "兴庆",
                "place_id": "",
                "sources": [("宋史", "卷485·夏国传", "制番书")],
                "quote": "文治/国族符号。",
                "confidence": "medium",
            },
            {
                "year": "1038",
                "date_note": "天授礼法延祚元年",
                "title": "河西称帝",
                "summary": "即皇帝位，国号大夏，改元，与宋辽并立。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "兴庆府",
                "place_id": "",
                "sources": [("宋史", "卷485·夏国传", "称帝")],
                "quote": "记忆点 1038。",
            },
            {
                "year": "1041",
                "date_note": "康定/庆历",
                "title": "好水川大捷",
                "summary": "宋夏大战中夏军重创宋军，确立西夏军事地位。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "好水川",
                "place_id": "",
                "sources": [("宋史", "卷485·夏国传", "好水川"), ("宋史", "相关列传", "任福等")],
                "quote": "武功名场面。",
            },
            {
                "year": "1044",
                "date_note": "庆历四年",
                "title": "庆历和议",
                "summary": "宋夏达成和议，元昊对宋称臣而自帝其国，换岁赐与边境稳定。",
                "on_map": "no",
                "route_group": "",
                "place": "",
                "place_id": "",
                "sources": [("宋史", "卷485·夏国传", "和议")],
                "quote": "韬略：名实分离。",
            },
            {
                "year": "1048",
                "date_note": "延祚十一年",
                "title": "遇弑",
                "summary": "元昊在宫廷斗争中被刺死，西夏转入后续诸帝。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "兴庆",
                "place_id": "",
                "sources": [("宋史", "卷485·夏国传", "卒")],
                "quote": "国祚个人终结。",
            },
        ],
    },
    "q-qin-fu-jian": {
        "meta": {
            "display": "前秦世祖",
            "personal": "苻坚",
            "epithet": "投鞭断流",
            "dynasty": "前秦",
            "tier": "quasi",
            "memory": "383淝水",
            "reign": "357–385",
            "capital": "长安",
            "src_a": "晋书",
            "src_a_juan": "卷113–114·苻坚载记",
            "places": [("长安", "西安", "chang-an", "都"), ("淝水", "安徽淮南一带", "", "败")],
            "relations": [("谋臣", "王猛", "治世"), ("对手", "谢安/谢玄", "淝水")],
            "disputes": "- 「投鞭断流」语出记载的文学性；战略责任归坚本人仍成立。",
        },
        "events": [
            {
                "year": "357",
                "date_note": "永兴元年",
                "title": "杀苻生即位",
                "summary": "诛暴主苻生，即天王位，改元，前秦进入苻坚时代。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "长安",
                "place_id": "chang-an",
                "sources": [("晋书", "卷113·苻坚载记", "即位")],
                "quote": "开局。",
            },
            {
                "year": "undated",
                "date_note": "在位前中期",
                "title": "委任王猛",
                "summary": "以王猛整肃吏治、打击贵戚，前秦国力急升。",
                "on_map": "no",
                "route_group": "",
                "place": "长安",
                "place_id": "chang-an",
                "sources": [("晋书", "卷114·苻坚载记/王猛附", "治绩")],
                "quote": "文治高峰。",
            },
            {
                "year": "370",
                "date_note": "太和五年",
                "title": "灭前燕",
                "summary": "灭前燕，北方统一进程加速。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "邺",
                "place_id": "",
                "sources": [("晋书", "卷113·苻坚载记", "灭燕")],
                "quote": "武功上升。",
            },
            {
                "year": "376",
                "date_note": "太元元年",
                "title": "统一北方",
                "summary": "灭前凉、代等，北方大体统一于前秦。",
                "on_map": "maybe",
                "route_group": "亲征",
                "place": "河西/代北",
                "place_id": "hexi",
                "sources": [("晋书", "卷113·苻坚载记", "平凉代")],
                "quote": "巅峰版图。",
                "confidence": "medium",
            },
            {
                "year": "383",
                "date_note": "太元八年",
                "title": "投鞭决策",
                "summary": "决意南伐东晋，史载有「投鞭于江，足断其流」一类豪语，倾国出兵。",
                "on_map": "no",
                "route_group": "",
                "place": "长安议兵",
                "place_id": "chang-an",
                "sources": [("晋书", "卷114·苻坚载记", "南伐议")],
                "quote": "四字号来源。",
            },
            {
                "year": "383",
                "date_note": "太元八年",
                "title": "淝水之战",
                "summary": "淝水大败，前秦崩解，各族复起。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "淝水",
                "place_id": "",
                "sources": [("晋书", "卷114·苻坚载记", "淝水"), ("资治通鉴", "晋纪", "淝水")],
                "quote": "记忆点 383。",
            },
            {
                "year": "385",
                "date_note": "太元十年",
                "title": "苻坚败亡",
                "summary": "西奔后被姚苌所害，前秦迅速瓦解。",
                "on_map": "yes",
                "route_group": "流徙",
                "place": "五将山一带",
                "place_id": "",
                "sources": [("晋书", "卷114·苻坚载记", "卒")],
                "quote": "国祚崩。",
            },
        ],
    },
    "n-wei-xiaowen": {
        "meta": {
            "display": "北魏孝文帝",
            "personal": "元宏（拓跋宏）",
            "epithet": "胡骑解辫",
            "dynasty": "北魏",
            "tier": "emperor",
            "memory": "太和迁都",
            "reign": "471–499",
            "capital": "平城→洛阳",
            "src_a": "魏书",
            "src_a_juan": "卷007·高祖纪",
            "places": [("平城", "大同", "", "旧都"), ("洛阳", "洛阳", "luoyang", "新都")],
            "relations": [("祖母", "冯太后", "太和前政"), ("太武", "拓跋焘", "先统一后汉化")],
            "disputes": "- 汉化激进与六镇矛盾；后效极高。",
        },
        "events": [
            {
                "year": "471",
                "date_note": "延兴元年",
                "title": "即位",
                "summary": "幼年即位，冯太后临朝，太和改革铺垫。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "平城",
                "place_id": "",
                "sources": [("魏书", "卷007·高祖纪", "即位")],
                "quote": "开局。",
            },
            {
                "year": "484",
                "date_note": "太和八年",
                "title": "班禄制",
                "summary": "班禄酬廉，整顿吏治，太和新政重要一步。",
                "on_map": "no",
                "route_group": "",
                "place": "平城",
                "place_id": "",
                "sources": [("魏书", "卷007·高祖纪", "班禄")],
                "quote": "文治。",
            },
            {
                "year": "493",
                "date_note": "太和十七年",
                "title": "迁都洛阳",
                "summary": "以南伐为名迁都洛阳，北魏政治中心南移。",
                "on_map": "yes",
                "route_group": "迁都",
                "place": "洛阳",
                "place_id": "luoyang",
                "sources": [("魏书", "卷007下·高祖纪", "迁洛")],
                "quote": "记忆点。",
            },
            {
                "year": "494",
                "date_note": "太和十八年",
                "title": "禁胡服胡语",
                "summary": "禁鲜卑语、改服饰，推动朝臣汉化。",
                "on_map": "no",
                "route_group": "",
                "place": "洛阳",
                "place_id": "luoyang",
                "sources": [("魏书", "卷007下·高祖纪", "革衣服语言")],
                "quote": "胡骑解辫意象。",
            },
            {
                "year": "496",
                "date_note": "太和二十年",
                "title": "改姓元",
                "summary": "拓跋改姓元，门阀化与汉姓改革。",
                "on_map": "no",
                "route_group": "",
                "place": "洛阳",
                "place_id": "luoyang",
                "sources": [("魏书", "卷007下·高祖纪", "改姓")],
                "quote": "身份政治。",
            },
            {
                "year": "499",
                "date_note": "太和二十三年",
                "title": "南伐崩于军",
                "summary": "南征途中崩，汉化路线由宣武等延续，亦埋六镇隐患。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "南境/洛阳归葬",
                "place_id": "luoyang",
                "sources": [("魏书", "卷007下·高祖纪", "崩")],
                "quote": "后效与代价并读。",
            },
        ],
    },
    "sui-wen": {
        "meta": {
            "display": "隋文帝",
            "personal": "杨坚",
            "epithet": "混一戎夏",
            "dynasty": "隋",
            "tier": "emperor",
            "memory": "开皇九年灭陈",
            "reign": "581–604",
            "capital": "大兴（长安）",
            "src_a": "隋书",
            "src_a_juan": "卷001–002·高祖纪",
            "places": [("大兴", "西安", "chang-an", "都"), ("建康", "南京", "", "灭陈")],
            "relations": [("子", "炀帝杨广", "国祚对照"), ("前朝", "北周", "受禅")],
            "disputes": "- 废勇立广争议；二世而亡压国祚。",
        },
        "events": [
            {
                "year": "581",
                "date_note": "开皇元年",
                "title": "代周建隋",
                "summary": "受禅建隋，改元开皇，结束北周。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "长安/大兴",
                "place_id": "chang-an",
                "sources": [("隋书", "卷001·高祖纪", "受禅")],
                "quote": "开国。",
            },
            {
                "year": "undated",
                "date_note": "开皇间",
                "title": "开皇制度",
                "summary": "三省六部成型、统一货币度量、检括户口，奠定后世政制底盘。",
                "on_map": "no",
                "route_group": "",
                "place": "大兴",
                "place_id": "chang-an",
                "sources": [("隋书", "卷001–002·高祖纪", "制度"), ("隋书", "志", "官制食货")],
                "quote": "后效极高。",
                "confidence": "medium",
            },
            {
                "year": "589",
                "date_note": "开皇九年",
                "title": "灭陈混一",
                "summary": "平陈，南北再统一，史称混一戎夏。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "建康",
                "place_id": "",
                "sources": [("隋书", "卷002·高祖纪", "平陈")],
                "quote": "四字号+记忆点。",
            },
            {
                "year": "600",
                "date_note": "开皇二十年",
                "title": "废勇立广",
                "summary": "废太子勇，立晋王广为太子，种下国祚风险。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "大兴",
                "place_id": "chang-an",
                "related": ["sui-yang"],
                "sources": [("隋书", "卷002·高祖纪", "废立"), ("隋书", "卷045·房陵王勇传", "废")],
                "quote": "韬略争议点。",
            },
            {
                "year": "604",
                "date_note": "仁寿四年",
                "title": "文帝崩",
                "summary": "崩于仁寿宫，炀帝即位；统一遗产与二世风险同时交接。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "仁寿宫",
                "place_id": "",
                "related": ["sui-yang"],
                "sources": [("隋书", "卷002·高祖纪", "崩")],
                "quote": "国祚评分被身后压低。",
            },
        ],
    },
    "sui-yang": {
        "meta": {
            "display": "隋炀帝",
            "personal": "杨广",
            "epithet": "江东晋王",
            "dynasty": "隋",
            "tier": "emperor",
            "memory": "江都之变 / 大业",
            "reign": "604–618",
            "capital": "大兴/东都/江都",
            "src_a": "隋书",
            "src_a_juan": "卷003–004·炀帝纪",
            "places": [
                ("江都", "扬州", "", "终局"),
                ("东都", "洛阳", "luoyang", "营建"),
                ("辽东", "辽宁一带", "liaodong", "征高丽"),
            ],
            "relations": [("父", "隋文帝", "继位"), ("对照", "唐太宗", "后效承接")],
            "disputes": "- 暴君定评 vs 运河/科举/沟通南北的后效；月旦极低、后效高。",
        },
        "events": [
            {
                "year": "589",
                "date_note": "开皇九年",
                "title": "晋王平陈",
                "summary": "为晋王时参与灭陈，立功，伏笔「晋王」身份。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "建康",
                "place_id": "",
                "related": ["sui-wen"],
                "sources": [("隋书", "卷003·炀帝纪", "为晋王平陈")],
                "quote": "四字号上半：晋王。",
            },
            {
                "year": "604",
                "date_note": "仁寿四年",
                "title": "即位改元",
                "summary": "即位，后改元大业，展开大工程与扩张。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "大兴",
                "place_id": "chang-an",
                "sources": [("隋书", "卷003·炀帝纪", "即位")],
                "quote": "大业开场。",
            },
            {
                "year": "605",
                "date_note": "大业元年",
                "title": "营东都开运河",
                "summary": "营建东都洛阳，开凿通济渠等，贯通南北水运。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "洛阳",
                "place_id": "luoyang",
                "sources": [("隋书", "卷003·炀帝纪", "营东都"), ("隋书", "食货/地理相关", "漕渠")],
                "quote": "后效核心。",
            },
            {
                "year": "612",
                "date_note": "大业八年",
                "title": "一征高句丽",
                "summary": "大举征高句丽，丧师费财，国内矛盾激化。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "辽东",
                "place_id": "liaodong",
                "sources": [("隋书", "卷004·炀帝纪", "征辽")],
                "quote": "武功有企图、结果崩。",
            },
            {
                "year": "617",
                "date_note": "大业十三年",
                "title": "天下分崩",
                "summary": "群雄并起，炀帝滞留江都，中枢失控。",
                "on_map": "yes",
                "route_group": "流徙",
                "place": "江都",
                "place_id": "",
                "sources": [("隋书", "卷004·炀帝纪", "江都")],
                "quote": "国祚见底。",
            },
            {
                "year": "618",
                "date_note": "大业十四年",
                "title": "江都之变",
                "summary": "宇文化及等发动兵变，炀帝死于江都，隋亡。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "江都",
                "place_id": "",
                "sources": [("隋书", "卷004·炀帝纪", "崩"), ("资治通鉴", "隋纪", "江都")],
                "quote": "四字号下半：江东终局。",
            },
        ],
    },
    "zhou-wu-zetian": {
        "meta": {
            "display": "武则天",
            "personal": "武曌",
            "epithet": "金轮称制",
            "dynasty": "武周",
            "tier": "emperor",
            "memory": "天授元年（690）称帝",
            "reign": "690–705（称帝）；临朝更早",
            "capital": "神都洛阳",
            "src_a": "旧唐书",
            "src_a_juan": "卷006·则天皇后纪",
            "src_b": "新唐书·则天皇后",
            "places": [("洛阳", "洛阳", "luoyang", "神都"), ("长安", "西安", "chang-an", "西京")],
            "relations": [("夫", "高宗", "二圣"), ("政变", "五王/李唐复辟", "神龙")],
            "disputes": "- 传统「女祸」叙事与现代重估；月旦中性偏下。",
        },
        "events": [
            {
                "year": "655",
                "date_note": "永徽六年",
                "title": "立为皇后",
                "summary": "由昭仪立为皇后，进入权力中枢。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "长安",
                "place_id": "chang-an",
                "sources": [("旧唐书", "卷006·则天皇后纪", "立后")],
                "quote": "入局。",
            },
            {
                "year": "660",
                "date_note": "显庆五年后",
                "title": "二圣临朝",
                "summary": "高宗病，天后参决政务，形成二圣格局。",
                "on_map": "no",
                "route_group": "",
                "place": "长安/洛阳",
                "place_id": "luoyang",
                "sources": [("旧唐书", "卷006", "决事"), ("新唐书", "则天皇后", "二圣")],
                "quote": "韬略积累。",
                "confidence": "medium",
            },
            {
                "year": "684",
                "date_note": "光宅元年",
                "title": "废中宗",
                "summary": "废中宗为庐陵王，立睿宗，实掌朝政。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "洛阳",
                "place_id": "luoyang",
                "sources": [("旧唐书", "卷006", "废帝")],
                "quote": "称制前夜。",
            },
            {
                "year": "690",
                "date_note": "天授元年",
                "title": "金轮称帝",
                "summary": "改国号周，称帝，加尊号，女主正式称制。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "神都洛阳",
                "place_id": "luoyang",
                "sources": [("旧唐书", "卷006", "革唐为周"), ("新唐书", "则天皇后", "天授")],
                "quote": "记忆点+四字号。",
            },
            {
                "year": "undated",
                "date_note": "天授–长安",
                "title": "科举与能吏",
                "summary": "破格用人、发展科举殿试等，文治有实绩，亦酷吏政治并存。",
                "on_map": "no",
                "route_group": "",
                "place": "洛阳",
                "place_id": "luoyang",
                "sources": [("旧唐书", "卷006", "政绩概"), ("新唐书", "选举志等", "对照")],
                "quote": "文治 88 来源。",
                "confidence": "medium",
            },
            {
                "year": "705",
                "date_note": "神龙元年",
                "title": "神龙政变",
                "summary": "张柬之等拥中宗复位，武周结束，则天迁宫。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "洛阳",
                "place_id": "luoyang",
                "sources": [("旧唐书", "卷006", "逊位"), ("旧唐书", "中宗纪", "复位")],
                "quote": "国祚收束。",
            },
        ],
    },
    "tang-xian-zong": {
        "meta": {
            "display": "唐宪宗",
            "personal": "李纯",
            "epithet": "元和鞭藩",
            "dynasty": "唐",
            "tier": "emperor",
            "memory": "元和削藩",
            "reign": "805–820",
            "capital": "长安",
            "src_a": "旧唐书",
            "src_a_juan": "卷014–015·宪宗纪",
            "places": [("长安", "西安", "chang-an", "都"), ("蔡州", "河南汝南", "", "淮西")],
            "relations": [("藩镇", "吴元济等", "削藩"), ("宦官", "陈弘志等", "暴崩疑云")],
            "disputes": "- 暴崩与宦官；元和中兴是否可持续。",
        },
        "events": [
            {
                "year": "805",
                "date_note": "永贞元年",
                "title": "即位",
                "summary": "顺宗内禅，宪宗即位，改元元和。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "长安",
                "place_id": "chang-an",
                "sources": [("旧唐书", "卷014·宪宗纪", "即位")],
                "quote": "开局。",
            },
            {
                "year": "806",
                "date_note": "元和元年",
                "title": "平西川",
                "summary": "讨平刘辟，展示削藩决心。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "西川",
                "place_id": "",
                "sources": [("旧唐书", "卷014", "刘辟")],
                "quote": "鞭藩序章。",
            },
            {
                "year": "817",
                "date_note": "元和十二年",
                "title": "平淮西",
                "summary": "李愬雪夜入蔡州，擒吴元济，元和削藩高潮。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "蔡州",
                "place_id": "",
                "sources": [("旧唐书", "卷015", "平蔡"), ("旧唐书", "李愬传", "入蔡")],
                "quote": "记忆点。",
            },
            {
                "year": "818",
                "date_note": "元和十三年前后",
                "title": "成德归朝",
                "summary": "河朔藩镇一度听命，元和中兴气象。",
                "on_map": "maybe",
                "route_group": "其他",
                "place": "成德",
                "place_id": "",
                "sources": [("旧唐书", "卷015", "藩镇归附")],
                "quote": "中兴峰值。",
                "confidence": "medium",
            },
            {
                "year": "820",
                "date_note": "元和十五年",
                "title": "暴崩",
                "summary": "暴崩，史载与宦官相关疑云，穆宗即位，削藩成果回落。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "长安",
                "place_id": "chang-an",
                "sources": [("旧唐书", "卷015", "崩"), ("新唐书", "宪宗纪", "对照")],
                "quote": "国祚低分。",
            },
        ],
    },
    "zhou-shi": {
        "meta": {
            "display": "后周世宗",
            "personal": "柴荣",
            "epithet": "显德振旅",
            "dynasty": "后周",
            "tier": "emperor",
            "memory": "显德征伐",
            "reign": "954–959",
            "capital": "开封",
            "src_a": "旧五代史",
            "src_a_juan": "卷114–119·周书·世宗纪",
            "src_b": "新五代史·周本纪",
            "places": [("开封", "开封", "", "都"), ("高平", "山西高平", "", "名战"), ("淮南", "江淮", "", "征南唐")],
            "relations": [("养父", "郭威", "周太祖"), ("后续", "赵匡胤", "陈桥")],
            "disputes": "- 英年早逝；若永年或改宋史开局。",
        },
        "events": [
            {
                "year": "954",
                "date_note": "显德元年",
                "title": "即位",
                "summary": "郭威崩，柴荣即位，是为世宗。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "开封",
                "place_id": "",
                "sources": [("旧五代史", "周书·世宗纪", "即位")],
                "quote": "开局。",
            },
            {
                "year": "954",
                "date_note": "显德元年",
                "title": "高平之战",
                "summary": "亲征败北汉契丹联军于高平，整肃禁军，确立权威。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "高平",
                "place_id": "",
                "sources": [("旧五代史", "世宗纪", "高平"), ("资治通鉴", "后周纪", "高平")],
                "quote": "武功开门红。",
            },
            {
                "year": "undated",
                "date_note": "显德间",
                "title": "整军均田",
                "summary": "选练禁军、限制寺院、均定田赋，国力回升。",
                "on_map": "no",
                "route_group": "",
                "place": "开封",
                "place_id": "",
                "sources": [("旧五代史", "世宗纪", "改革"), ("五代会要等", "相关卷", "制度（二手入口）")],
                "quote": "文治高分。",
                "confidence": "medium",
            },
            {
                "year": "957",
                "date_note": "显德四–五年",
                "title": "经略淮南",
                "summary": "多次征南唐，取江北十四州，南压强敌。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "淮南",
                "place_id": "",
                "related": ["n-tang-houzhu"],
                "sources": [("旧五代史", "世宗纪", "征淮"), ("新五代史", "周本纪", "南征")],
                "quote": "显德振旅。",
            },
            {
                "year": "959",
                "date_note": "显德六年",
                "title": "北伐契丹",
                "summary": "北伐收复关南部分州县，病重回师。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "幽州南/关南",
                "place_id": "",
                "sources": [("旧五代史", "世宗纪", "北伐")],
                "quote": "未完成的混一。",
            },
            {
                "year": "959",
                "date_note": "显德六年",
                "title": "世宗崩",
                "summary": "崩于开封，子宗训幼，旋有陈桥兵变，周禅宋。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "开封",
                "place_id": "",
                "related": ["n-song-tai-zu"],
                "sources": [("旧五代史", "世宗纪", "崩")],
                "quote": "国祚极低、后效交给宋。",
            },
        ],
    },
    "n-tang-houzhu": {
        "meta": {
            "display": "南唐后主",
            "personal": "李煜",
            "epithet": "江南残梦",
            "dynasty": "南唐",
            "tier": "quasi",
            "memory": "975城破",
            "reign": "961–975",
            "capital": "金陵",
            "src_a": "宋史",
            "src_a_juan": "卷478·南唐李氏世家",
            "src_b": "新五代史·南唐世家 / 马令、陆游南唐书（二手）",
            "places": [("金陵", "南京", "", "都"), ("汴京", "开封", "", "北迁")],
            "relations": [("宋", "宋太祖/太宗", "灭国"), ("文", "词人身份", "后效")],
            "disputes": "- 君道失败与词人成就；月旦为同情分。七夕赐死有异说。",
        },
        "events": [
            {
                "year": "961",
                "date_note": "宋建隆二年",
                "title": "即位金陵",
                "summary": "李璟卒，李煜继位，对宋已处劣势。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "金陵",
                "place_id": "",
                "sources": [("宋史", "卷478·南唐世家", "即位")],
                "quote": "残梦开场。",
            },
            {
                "year": "undated",
                "date_note": "在位间",
                "title": "词章与文艺",
                "summary": "倾力于书画音律词章，文艺成就远超君道事功。",
                "on_map": "no",
                "route_group": "",
                "place": "金陵",
                "place_id": "",
                "sources": [("宋史", "卷478", "性好"), ("词籍", "二主词（文学史）", "后效入口")],
                "quote": "后效在文学。",
                "confidence": "medium",
            },
            {
                "year": "971",
                "date_note": "开宝前后",
                "title": "贬号称臣",
                "summary": "去帝号、称江南国主，对宋称臣以求苟安。",
                "on_map": "no",
                "route_group": "",
                "place": "金陵",
                "place_id": "",
                "related": ["n-song-tai-zu"],
                "sources": [("宋史", "卷478", "奉宋正朔")],
                "quote": "韬略低分。",
            },
            {
                "year": "975",
                "date_note": "开宝八年",
                "title": "金陵城破",
                "summary": "宋军破金陵，后主降，南唐亡。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "金陵",
                "place_id": "",
                "related": ["n-song-tai-zu"],
                "sources": [("宋史", "卷478", "国亡"), ("宋史", "太祖纪", "平江南")],
                "quote": "记忆点 975。",
            },
            {
                "year": "976",
                "date_note": "北迁后",
                "title": "违命侯",
                "summary": "封违命侯，软禁汴京，词多故国之思。",
                "on_map": "yes",
                "route_group": "流徙",
                "place": "汴京",
                "place_id": "",
                "sources": [("宋史", "卷478", "封侯")],
                "quote": "江南残梦。",
            },
            {
                "year": "978",
                "date_note": "太平兴国三年",
                "title": "后主卒",
                "summary": "卒于汴京；民间有七夕赐牵机药传说，正史记载简略，作待考。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "汴京",
                "place_id": "",
                "sources": [("宋史", "卷478", "卒"), ("笔记小说", "赐死说", "待考")],
                "quote": "传说慎用，分镜可标「传说层」。",
                "confidence": "low",
            },
        ],
    },
    "n-song-tai-zu": {
        "meta": {
            "display": "宋太祖",
            "personal": "赵匡胤",
            "epithet": "杯酒释兵",
            "dynasty": "北宋",
            "tier": "emperor",
            "memory": "杯酒释兵权（副钩：960陈桥）",
            "reign": "960–976",
            "capital": "开封",
            "src_a": "宋史",
            "src_a_juan": "卷001–003·太祖纪",
            "places": [("陈桥", "开封北", "", "兵变"), ("开封", "开封", "", "都")],
            "relations": [("前朝", "周世宗", "高平旧将"), ("弟", "太宗", "金匮争议")],
            "disputes": "- 杯酒细节有演绎；陈桥是否预谋；金匮之盟。",
        },
        "events": [
            {
                "year": "960",
                "date_note": "建隆元年",
                "title": "陈桥兵变",
                "summary": "兵变黄袍加身，代周建宋，定都开封。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "陈桥驿",
                "place_id": "",
                "related": ["zhou-shi"],
                "sources": [("宋史", "卷001·太祖纪", "陈桥")],
                "quote": "副记忆钩。",
            },
            {
                "year": "961",
                "date_note": "建隆二年",
                "title": "杯酒释兵权",
                "summary": "以酒宴方式解除禁军宿将兵权，强干弱枝开端。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "开封",
                "place_id": "",
                "sources": [("宋史", "相关列传/长编系统", "释兵权叙事"), ("续资治通鉴长编", "建隆二年", "二手入口")],
                "quote": "四字号+主记忆。",
                "confidence": "medium",
            },
            {
                "year": "undated",
                "date_note": "开宝前",
                "title": "先南后北",
                "summary": "平荆湖、后蜀、南汉、南唐等，统一南方战略。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "南方诸国",
                "place_id": "",
                "related": ["n-tang-houzhu"],
                "sources": [("宋史", "卷001–002·太祖纪", "平诸国")],
                "quote": "武功路线。",
                "confidence": "medium",
            },
            {
                "year": "undated",
                "date_note": "在位间",
                "title": "重文抑武",
                "summary": "抬高文官、分化兵权，奠定宋代国势路径。",
                "on_map": "no",
                "route_group": "",
                "place": "开封",
                "place_id": "",
                "sources": [("宋史", "太祖纪/职官志", "制度"), ("宋史", "选举志", "文官")],
                "quote": "后效 94。",
                "confidence": "medium",
            },
            {
                "year": "976",
                "date_note": "开宝九年",
                "title": "太祖崩",
                "summary": "崩，太宗即位；「烛影斧声」等为争议层。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "开封",
                "place_id": "",
                "sources": [("宋史", "卷003·太祖纪", "崩")],
                "quote": "分镜可轻点争议不坐实。",
                "confidence": "high",
            },
        ],
    },
    "yuan-shi-zu": {
        "meta": {
            "display": "元世祖",
            "personal": "忽必烈",
            "epithet": "混一车书",
            "dynasty": "元",
            "tier": "emperor",
            "memory": "1279灭宋",
            "reign": "1260–1294",
            "capital": "大都",
            "src_a": "元史",
            "src_a_juan": "卷004–017·世祖纪",
            "places": [("开平/上都", "内蒙古正蓝旗一带", "", "即位"), ("大都", "北京", "", "都"), ("崖山", "广东新会南", "", "灭宋")],
            "relations": [("宋", "宋末帝", "崖山"), ("蒙古", "阿里不哥", "汗位战")],
            "disputes": "- 征服王朝正统与汉地治理评价撕裂；月旦中性，后效极高。",
        },
        "events": [
            {
                "year": "1260",
                "date_note": "中统元年",
                "title": "开平即位",
                "summary": "即大汗位，建元中统，与阿里不哥争位。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "开平",
                "place_id": "",
                "sources": [("元史", "卷004·世祖纪", "即位")],
                "quote": "开局。",
            },
            {
                "year": "1271",
                "date_note": "至元八年",
                "title": "建国号元",
                "summary": "取《易》「大哉乾元」之义，建国号大元。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "大都",
                "place_id": "",
                "sources": [("元史", "卷007·世祖纪", "国号")],
                "quote": "车书混一的名号。",
            },
            {
                "year": "1272",
                "date_note": "至元九年",
                "title": "都于大都",
                "summary": "改中都为大都，政治中心落于燕地。",
                "on_map": "yes",
                "route_group": "迁都",
                "place": "大都",
                "place_id": "",
                "sources": [("元史", "卷007", "大都")],
                "quote": "地理遗产。",
            },
            {
                "year": "1276",
                "date_note": "至元十三年",
                "title": "下临安",
                "summary": "伯颜入临安，宋廷降，残部入海。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "临安",
                "place_id": "",
                "sources": [("元史", "卷009", "平宋"), ("宋史", "瀛国公纪", "降")],
                "quote": "灭宋进程。",
            },
            {
                "year": "1279",
                "date_note": "至元十六年",
                "title": "崖山灭宋",
                "summary": "崖山之战，宋亡，中国再度大一统于元。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "崖山",
                "place_id": "",
                "sources": [("元史", "卷010", "崖山"), ("宋史", "二王/本纪", "亡")],
                "quote": "记忆点 1279。",
            },
            {
                "year": "undated",
                "date_note": "至元间",
                "title": "行省与站赤",
                "summary": "行省制、驿站网络等，塑造后世行政区与交通遗产。",
                "on_map": "no",
                "route_group": "",
                "place": "大都",
                "place_id": "",
                "sources": [("元史", "百官志/兵志", "行省站赤")],
                "quote": "后效 96。",
                "confidence": "medium",
            },
        ],
    },
    "n-wei-taiwu": {
        "meta": {
            "display": "北魏太武帝",
            "personal": "拓跋焘",
            "epithet": "真君铁骑",
            "dynasty": "北魏",
            "tier": "emperor",
            "memory": "灭北凉 / 太平真君灭佛",
            "reign": "423–452",
            "capital": "平城",
            "src_a": "魏书",
            "src_a_juan": "卷004·世祖纪",
            "places": [("平城", "大同", "", "都"), ("姑臧", "武威", "", "灭北凉"), ("长江", "南征线", "", "至瓜步")],
            "relations": [("孙", "孝文帝", "汉化后续"), ("宗教", "崔浩/寇谦之", "灭佛")],
            "disputes": "- 武功极盛 vs 残暴/灭佛；月旦中性偏负。",
        },
        "events": [
            {
                "year": "423",
                "date_note": "始光元年",
                "title": "即位",
                "summary": "明元帝崩，焘即位，北魏进入扩张高峰。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "平城",
                "place_id": "",
                "sources": [("魏书", "卷004·世祖纪", "即位")],
                "quote": "开局。",
            },
            {
                "year": "431",
                "date_note": "神䴥四年",
                "title": "灭胡夏",
                "summary": "灭赫连夏，取关中。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "统万/长安",
                "place_id": "chang-an",
                "sources": [("魏书", "卷004", "灭夏")],
                "quote": "铁骑之一。",
            },
            {
                "year": "436",
                "date_note": "太延二年",
                "title": "灭北燕",
                "summary": "灭冯氏北燕，辽西归魏。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "和龙",
                "place_id": "",
                "sources": [("魏书", "卷004", "灭燕")],
                "quote": "北方拼图。",
            },
            {
                "year": "439",
                "date_note": "太延五年",
                "title": "灭北凉",
                "summary": "灭沮渠北凉，北方统一于北魏，十六国阶段落幕。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "姑臧",
                "place_id": "hexi",
                "sources": [("魏书", "卷004", "灭凉")],
                "quote": "武功 96 硬指标。",
            },
            {
                "year": "444",
                "date_note": "太平真君五年起",
                "title": "真君灭佛",
                "summary": "太平真君年间禁佛毁寺，宗教政策极端化。",
                "on_map": "no",
                "route_group": "",
                "place": "平城",
                "place_id": "",
                "sources": [("魏书", "卷004", "灭佛法"), ("魏书", "释老志", "灭佛")],
                "quote": "月旦下拉。",
            },
            {
                "year": "450",
                "date_note": "太平真君十一年",
                "title": "南征瓜步",
                "summary": "大举南征刘宋，至瓜步，威震而未能定南。",
                "on_map": "yes",
                "route_group": "亲征",
                "place": "瓜步",
                "place_id": "",
                "sources": [("魏书", "卷004", "南伐"), ("宋书", "文帝纪", "对照")],
                "quote": "铁骑南指。",
            },
            {
                "year": "452",
                "date_note": "正平二年",
                "title": "被弑",
                "summary": "为中常侍宗爱所弑，北魏政局动荡。",
                "on_map": "yes",
                "route_group": "都城",
                "place": "平城",
                "place_id": "",
                "sources": [("魏书", "卷004", "崩")],
                "quote": "国祚个人终局。",
            },
        ],
    },
}


# 分镜：二十人视觉设定（含已有三人）
STORY = {
    "qin-shi-huang": {
        "order": 1,
        "display": "秦始皇",
        "epithet": "一统六合",
        "tone": "玄黑+鎏金，冷硬纪念碑感",
        "palette": "黑、玄青、鎏金、石灰白",
        "bg_list": [
            "咸阳宫阙剪影（对称纵深，烟雾低）",
            "六国版图六色块逐一熄灭→统一玄色",
            "泰山封禅云海（俯瞰）",
            "竹简/权量特写作转场纹理",
            "沙丘平台夜色（终局）",
        ],
        "char_hooks": "冠冕如刀、目光平视镜头、手不持剑而「持天下」",
        "motif": "度量衡碰撞声当节奏器",
        "scores": "武96 文93 韬88 祚18 后99 月42",
        "beats": [
            ("0-3s", "黑场金印砸下「一统六合」", "无对白，印泥扩散", "片头统一模板"),
            ("3-10s", "六国地图灯灭", "旁白：六王毕，四海一", "E005"),
            ("10-22s", "咸阳制度蒙太奇：车同轨/书同文图标", "字幕：后效顶格", "E006"),
            ("22-32s", "泰山云海人影渺小", "封禅——天子与天对齐", "E007"),
            ("32-42s", "竹简燃烧与长城剪影并行", "功罪同框，不解说", "E008/E009"),
            ("42-55s", "六维雷达弹出：后效99↑国祚18↓", "月旦42——撕裂", "video20"),
            ("55-65s", "沙丘夜，御辇停", "记忆点：前221称帝 / 终局沙丘", "E010"),
            ("65-75s", "图鉴卡定格+扫码位", "下一位预告可黑", "片尾"),
        ],
        "idea": "不做「暴君说教」，做**制度纪念碑与短命帝国的剪刀差**。金印很满，国祚条却是血红色枯萎。",
    },
    "han-xuan-di": {
        "order": 2,
        "display": "汉宣帝",
        "epithet": "综核名实",
        "tone": "暖灰官署+秋日长安，冷静务实",
        "palette": "檀褐、竹青、宣纸白、暗金",
        "bg_list": [
            "长安街市人潮（低机位，皇帝曾在此）",
            "未央宫奏事房案牍如山",
            "霍光灵堂→空殿（权移）",
            "西域烽燧与都护印",
            "呼韩邪入朝仪仗长卷",
        ],
        "char_hooks": "不耀武，眼神像审计；手持简牍非剑",
        "motif": "算盘/朱批「可」「否」盖章音效",
        "scores": "武68 文94 韬90 祚80 后74 月84",
        "beats": [
            ("0-3s", "印「综核名实」", "沉稳鼓点", "模板"),
            ("3-12s", "民间巷口孩童→掖庭灯", "从里巷来的天子", "E001"),
            ("12-22s", "霍光影巨大→影消", "迎立，然后亲政", "E002-E004"),
            ("22-35s", "案牍蒙太奇，朱笔勾稽", "信赏必罚，不尚虚名", "E008"),
            ("35-48s", "西域都护印落下+匈奴使节跪拜长卷", "边事收成", "E005-E006"),
            ("48-60s", "六维：文治韬略双高，武功不吹牛", "昭宣气象", "video20"),
            ("60-70s", "图鉴卡", "记忆：地节亲政", "片尾"),
        ],
        "idea": "对标汉武的「开」——宣帝片全是「收」与「核」。视觉上少战场，多**办公美学**。",
    },
    "han-wu-di": {
        "order": 3,
        "display": "汉武帝",
        "epithet": "封狼居胥",
        "tone": "大漠金红+宫廷朱红，雄开",
        "palette": "朱红、沙金、苍青、血褐",
        "bg_list": [
            "狼居胥山影/漠北地平线",
            "长安未央灯火",
            "黄河河套收复航拍感",
            "泰山封禅玉牒",
            "轮台诏竹简特写（收束）",
        ],
        "char_hooks": "披风猎猎、马背与祭坛两种姿态切换",
        "motif": "马蹄与编钟交错",
        "scores": "武95 文82 韬85 祚86 后94 月68",
        "beats": [
            ("0-3s", "印「封狼居胥」", "号角", "模板"),
            ("3-15s", "漠北骑兵剪影冲山", "武功开场不废话", "E007-E008 河西/漠北线"),
            ("15-28s", "马邑之谋到河西廊道地图推进", "开边连台", "E006–E008"),
            ("28-40s", "封禅泰山", "天子与天下对齐", "E009"),
            ("40-52s", "巫蛊血色宫廷一闪", "雄主背面", "E011"),
            ("52-62s", "轮台诏：镜头从战场收回长安", "后效与月旦拉扯", "E012"),
            ("62-75s", "六维+图鉴卡", "记忆：漠北/元封二选一主打", "片尾"),
        ],
        "idea": "一片拆两截：**上半封狼，下半轮台**。月旦68用「金色裂痕」表现。",
    },
    "xin-wang-mang": {
        "order": 4,
        "display": "新帝王莽",
        "epithet": "以儒窃国",
        "tone": "伪古典——礼器闪光但色相发冷",
        "palette": "铜绿、惨白、暗紫、朱砂印过浓",
        "bg_list": [
            "明堂/辟雍建筑透视（过满）",
            "刀币、错刀货币特写混乱切换",
            "周公画像被王莽身影叠化",
            "渐台秋风",
            "绿林火光远景",
        ],
        "char_hooks": "捧圭过度端正，微笑标准像面具",
        "motif": "礼乐声逐渐跑调走音",
        "scores": "武35 文55 韬72 祚12 后70 月22",
        "beats": [
            ("0-3s", "印「以儒窃国」", "礼乐走音", "模板"),
            ("3-14s", "安汉公→假皇帝头衔字幕层叠", "周公故事", "E001-E002"),
            ("14-26s", "始建国改元大典，礼器满屏", "以儒入篡", "E003"),
            ("26-40s", "王田奴婢货币图标崩坏动画", "托古，天下碎", "E004"),
            ("40-52s", "昆阳战火反射到长安宫墙", "与光武卡互文", "E006"),
            ("52-62s", "渐台，儒服染尘", "月旦22", "E007"),
            ("62-72s", "六维：后效70（话题）月旦22", "图鉴卡", "片尾"),
        ],
        "idea": "全片礼器越精美，统治越虚。**「儒」是皮肤，「窃」是骨骼**。",
    },
    "e-han-guangwu": {
        "order": 5,
        "display": "汉光武帝",
        "epithet": "昆阳一旅",
        "tone": "雨后晴空感，中兴暖金",
        "palette": "晴蓝、麦金、汉白、赭石",
        "bg_list": [
            "昆阳城头暴雨雷光",
            "河北原野麦浪",
            "洛阳南宫晨曦",
            "云台功臣虚影壁",
            "柔光殿内议政（无剑）",
        ],
        "char_hooks": "战场狼狈与称帝后从容的硬切对比",
        "motif": "雷→晴的环境音变奏",
        "scores": "武91 文90 韬90 祚84 后86 月90",
        "beats": [
            ("0-3s", "印「昆阳一旅」", "雷", "模板"),
            ("3-18s", "昆阳：少骑冲击新军潮", "一旅定名", "E002"),
            ("18-30s", "河北招抚，篝火会议", "根据地", "E003"),
            ("30-42s", "鄗南称帝/洛阳定都", "汉旗再起", "E004"),
            ("42-55s", "云台虚影，功臣退入画像", "柔道", "E006"),
            ("55-68s", "六维近乎全能正，月旦90", "图鉴卡", "片尾"),
        ],
        "idea": "最「王道」的一张英雄卡，避免无聊：用**雨战脏镜头**对比**洛阳干净晨光**。",
    },
    "h-zhao-shi-le": {
        "order": 6,
        "display": "后赵石勒",
        "epithet": "奴隶天子",
        "tone": "铁灰尘土，阶级逆袭史诗",
        "palette": "铁锈、尘黄、骨白、暗血",
        "bg_list": [
            "枷锁/马市尘土",
            "襄国城垒夯土",
            "河北战场旗海",
            "张宾授策军帐",
            "帝座但背景仍是风沙",
        ],
        "char_hooks": "从锁链特写叠化到玺印；口音可暗示胡汉边缘（不恶搞）",
        "motif": "铁链落地→鼓点变宫廷雅乐（不协调）",
        "scores": "武93 文76 韬94 祚42 后68 月72",
        "beats": [
            ("0-3s", "印「奴隶天子」", "铁链", "模板"),
            ("3-14s", "被掠为奴蒙太奇", "社会底层", "E001"),
            ("14-28s", "聚兵→襄国称赵", "赵字旗升起", "E003"),
            ("28-42s", "灭前赵，地图吞并", "武功", "E004"),
            ("42-52s", "张宾与学校一闪", "不只是屠夫", "E006"),
            ("52-62s", "崩后石虎影压暗", "国祚42", "E007"),
            ("62-72s", "六维+卡", "记忆：襄国称赵", "片尾"),
        ],
        "idea": "十六国流量密码：**阶级跃迁**。结尾故意不美化身后。",
    },
    "liang-wu": {
        "order": 7,
        "display": "梁武帝",
        "epithet": "皇帝菩萨",
        "tone": "前半金粉建康，后半焦土台城",
        "palette": "佛金、藕荷、烟灰、死青",
        "bg_list": [
            "秦淮灯船/建康宫阙",
            "同泰寺巨佛与钱山（赎身）",
            "书卷与梵呗同框",
            "侯景甲骑入城烟尘",
            "台城空碗特写",
        ],
        "char_hooks": "帝王服下袈裟一角；晚年须发乱",
        "motif": "梵呗被甲骑踩碎",
        "scores": "武48 文78 韬62 祚55 后72 月50",
        "beats": [
            ("0-3s", "印「皇帝菩萨」", "铃", "模板"),
            ("3-14s", "受禅建梁，盛世剪影", "文治开场", "E002-E003"),
            ("14-30s", "舍身同泰：金→钱堆→皇帝被「请回」", "荒诞礼佛", "E004"),
            ("30-45s", "侯景渡江，建康火", "误判", "E005"),
            ("45-58s", "台城，空碗，梵音停", "终局", "E006"),
            ("58-70s", "六维中性，图鉴卡", "记忆双面：同泰/侯景", "片尾"),
        ],
        "idea": "一片两季。**前金后灰**，中点用舍身戏做「离谱名场面」。",
    },
    "xixia-li-yuanhao": {
        "order": 8,
        "display": "西夏景宗",
        "epithet": "河西称制",
        "tone": "河西硬光，党项民族纹样",
        "palette": "砂金、藏青、血红旗、白骨色",
        "bg_list": [
            "贺兰山剪影+兴庆城",
            "西夏文字幕墙",
            "好水川谷地伏兵",
            "宋夏边境榷场",
            "宫内刀光（遇弑）",
        ],
        "char_hooks": "秃发或党项发式考据向；目光鹰隼",
        "motif": "西夏文字笔画书写音效",
        "scores": "武88 文80 韬86 祚75 后73 月55",
        "beats": [
            ("0-3s", "印「河西称制」", "胡风鼓角", "模板"),
            ("3-12s", "袭位，去宋化服饰", "主体性", "E001-E002"),
            ("12-25s", "1038称帝大典，国号大夏", "记忆点", "E003"),
            ("25-40s", "好水川：宋旗乱", "武功", "E004"),
            ("40-52s", "和议：称臣又自帝的分屏", "韬略", "E005"),
            ("52-62s", "遇弑快剪", "终", "E006"),
            ("62-72s", "六维中位月旦，图鉴卡", "小众但硬", "片尾"),
        ],
        "idea": "系列里的**「非中原正统」代表作**，强调文字/国号/三角外交，不只打仗。",
    },
    "q-qin-fu-jian": {
        "order": 9,
        "display": "前秦世祖",
        "epithet": "投鞭断流",
        "tone": "盛世金光→淝水冷灰",
        "palette": "赭金、江练白、败青、雾",
        "bg_list": [
            "长安前秦宫阙盛时",
            "王猛身影（理智象征）",
            "北方一统地图点亮",
            "长江天堑与密密麻麻鞭影幻觉",
            "淝水风声鹤唳林",
        ],
        "char_hooks": "前期明君目，后期执拗；投鞭手势定格",
        "motif": "江水声盖过鼓声",
        "scores": "武84 文81 韬65 祚35 后66 月64",
        "beats": [
            ("0-3s", "印「投鞭断流」", "江声", "模板"),
            ("3-15s", "王猛治秦蒙太奇", "惜哉有臣", "E002"),
            ("15-28s", "灭燕统一北方地图", "巅峰", "E003-E004"),
            ("28-42s", "朝议：投鞭断流字幕炸出", "豪语", "E005"),
            ("42-55s", "淝水崩溃，风声鹤唳", "383", "E006"),
            ("55-65s", "六维：韬略被肥水拉低", "图鉴卡", "片尾"),
        ],
        "idea": "悲剧结构：**名场面是一句台词，真正的戏是统一后的冒进**。",
    },
    "n-wei-xiaowen": {
        "order": 10,
        "display": "北魏孝文帝",
        "epithet": "胡骑解辫",
        "tone": "塞外风→中原礼，渐变滤镜",
        "palette": "苍褐→绛红礼服，辫发丝特写",
        "bg_list": [
            "平城雪与乳白色穹庐感",
            "迁都车队南向官道",
            "洛阳里坊规划图动画",
            "解辫、改服、汉语课蒙太奇",
            "龙门石窟影子（时代符号，慎作个人肖像）",
        ],
        "char_hooks": "解辫动作超慢镜头；汉服加身站洛阳城楼",
        "motif": "胡笳渐隐，雅乐渐起",
        "scores": "武65 文96 韬84 祚70 后93 月86",
        "beats": [
            ("0-3s", "印「胡骑解辫」", "笳→雅乐", "模板"),
            ("3-12s", "平城幼帝/冯太后影", "铺垫", "E001"),
            ("12-28s", "太和迁洛车队", "记忆点", "E003"),
            ("28-45s", "禁胡语改姓元图标", "汉化三连", "E004-E005"),
            ("45-55s", "南伐病骨", "代价", "E006"),
            ("55-68s", "六维文治后效双爆", "图鉴卡", "片尾"),
        ],
        "idea": "系列**文治样板**。解辫是 logo 级动作，务必做美但不猎奇。",
    },
    "sui-wen": {
        "order": 11,
        "display": "隋文帝",
        "epithet": "混一戎夏",
        "tone": "清俭冷色，制度蓝图感",
        "palette": "青灰、皂衣、绢白、一点江左绿",
        "bg_list": [
            "大兴城规划网格",
            "开皇官署简朴",
            "长江上南征舰队",
            "建康城降旗",
            "仁寿宫暮色（不安）",
        ],
        "char_hooks": "衣着节俭与统一大典的反差",
        "motif": "尺子与印玺（制度）",
        "scores": "武85 文95 韬88 祚55 后91 月88",
        "beats": [
            ("0-3s", "印「混一戎夏」", "钟", "模板"),
            ("3-14s", "代周建隋，网格都城", "制度国", "E001-E002"),
            ("14-32s", "灭陈：江上→建康", "开皇九年", "E003"),
            ("32-45s", "废勇立广，太子印易手", "隐患", "E004"),
            ("45-55s", "崩，二世阴影压画面一角", "国祚55", "E005"),
            ("55-68s", "六维+卡", "后效交给唐", "片尾"),
        ],
        "idea": "和炀帝做**上下集气质对打**：父是蓝图，子是施工队失控。",
    },
    "sui-yang": {
        "order": 12,
        "display": "隋炀帝",
        "epithet": "江东晋王",
        "tone": "绮丽到刺眼，再坠入江都夜",
        "palette": "龙舟金、汴水碧、辽东雪、江都磷火青",
        "bg_list": [
            "晋王甲胄灭陈（少年功）",
            "东都洛阳巨构脚手架",
            "运河俯瞰如玉带（壮美）",
            "辽东军溃泥泞",
            "江都宫夜，刀光",
        ],
        "char_hooks": "前半英姿晋王，后半倦怠帝王；龙舟是移动王座",
        "motif": "纤夫号子变哭声",
        "scores": "武70 文42 韬52 祚15 后86 月18",
        "beats": [
            ("0-3s", "印「江东晋王」", "水声", "模板"),
            ("3-12s", "晋王平陈闪回", "出身", "E001"),
            ("12-28s", "运河+东都：壮美航拍", "后效画面先给足", "E003"),
            ("28-42s", "三征高丽泥雪", "崩坏", "E004"),
            ("42-55s", "江都之变", "记忆点", "E006"),
            ("55-68s", "六维：后效86 vs 月旦18 分屏拉扯", "图鉴卡", "片尾"),
        ],
        "idea": "核心创意就是 **后效≫月旦**。上半故意拍得像盛世旅游宣传片，再一刀切断。",
    },
    "tang-tai-zong": {
        "order": 13,
        "display": "唐太宗",
        "epithet": "天可汗令",
        "tone": "贞观明朗，金甲与谏纸同光",
        "palette": "唐金、石青、宫白、战灰",
        "bg_list": [
            "玄武门晨光（短、狠）",
            "凌烟阁功臣虚影",
            "渭水便桥/突厥归附",
            "太极殿纳谏",
            "辽东风雨（晚年）",
        ],
        "char_hooks": "弓马与手持魏徵谏纸的双手特写",
        "motif": "鼓与读书声平衡",
        "scores": "武89 文96 韬95 祚88 后97 月96",
        "beats": [
            ("0-3s", "印「天可汗令」", "鼓角", "模板"),
            ("3-14s", "玄武门快剪（不美化）", "得位", "E006"),
            ("14-30s", "破突厥，天可汗", "武+名号", "E008"),
            ("30-45s", "凌烟+纳谏", "贞观", "E009/E012"),
            ("45-55s", "辽东一笔带过", "人主之疲", "E010"),
            ("55-70s", "六维顶格，图鉴卡", "系列「标杆」", "片尾"),
        ],
        "idea": "避免个人崇拜脸：用**纳谏纸压过金甲**。玄武门只给3秒伦理重量。",
    },
    "zhou-wu-zetian": {
        "order": 14,
        "display": "武则天",
        "epithet": "金轮称制",
        "tone": "神都紫雾，女帝纪念碑",
        "palette": "帝紫、金轮、洛水青、无字碑灰",
        "bg_list": [
            "明堂/天堂建筑想象（考据向简化）",
            "金轮法器光",
            "洛阳神都晨雾",
            "铜匦与告密影（暗面）",
            "无字碑（若用需注明符号）",
        ],
        "char_hooks": "冕旒下女性轮廓；不走媚俗后宫戏",
        "motif": "钟磬与权杖同音",
        "scores": "武68 文88 韬94 祚78 后88 月58",
        "beats": [
            ("0-3s", "印「金轮称制」", "钟磬", "模板"),
            ("3-14s", "后位→二圣阴影", "入局", "E001-E002"),
            ("14-28s", "天授改周大典", "690记忆", "E004"),
            ("28-42s", "科举能吏光 vs 酷吏暗", "双轨", "E005"),
            ("42-55s", "神龙政变，周→唐", "收束", "E006"),
            ("55-68s", "六维：韬略高、月旦撕裂", "图鉴卡", "片尾"),
        ],
        "idea": "定位**政治动物+制度能吏**，拒绝宫斗流量脸。金轮是视觉 logo。",
    },
    "tang-xian-zong": {
        "order": 15,
        "display": "唐宪宗",
        "epithet": "元和鞭藩",
        "tone": "中晚唐冷硬，夜战雪",
        "palette": "玄甲、雪青、烛红、宫深褐",
        "bg_list": [
            "长安大明宫夜议",
            "蔡州城墙雪夜",
            "藩镇节度使旗一一面倒下",
            "元和年号匾",
            "大内黑暗走廊（暴崩）",
        ],
        "char_hooks": "中年锐帝，手指地图上的藩镇钉",
        "motif": "鞭影抽在地图上（抽象）",
        "scores": "武76 文87 韬90 祚48 后78 月80",
        "beats": [
            ("0-3s", "印「元和鞭藩」", "鞭/鼓", "模板"),
            ("3-12s", "即位元和", "中兴意图", "E001"),
            ("12-28s", "雪夜入蔡州", "高潮", "E003"),
            ("28-40s", "河朔归命字幕", "峰值", "E004"),
            ("40-52s", "暴崩疑云，光灭", "国祚", "E005"),
            ("52-65s", "六维+卡", "回光", "片尾"),
        ],
        "idea": "中晚唐的**「最后一记鞭」**，雪夜蔡州是必做名场面。",
    },
    "zhou-shi": {
        "order": 16,
        "display": "后周世宗",
        "epithet": "显德振旅",
        "tone": "戎装励志，短促燃烧",
        "palette": "玄甲银、战旗赤、秋草黄",
        "bg_list": [
            "高平战场坡地",
            "开封整军校场",
            "淮南水网战船",
            "关南边墙",
            "病榻与未竟地图",
        ],
        "char_hooks": "青年英主，始终甲不离身",
        "motif": "鼓点越来越快突然停",
        "scores": "武92 文89 韬88 祚28 后85 月88",
        "beats": [
            ("0-3s", "印「显德振旅」", "鼓", "模板"),
            ("3-16s", "高平亲征斩逃将", "立威", "E002"),
            ("16-30s", "整军均田图标", "文治", "E003"),
            ("30-45s", "征淮取地", "振旅", "E004"),
            ("45-55s", "北伐中病，地图未合", "崩", "E005-E006"),
            ("55-68s", "六维高、国祚28；预告陈桥影", "图鉴卡", "片尾"),
        ],
        "idea": "系列最「燃」短片之一。结尾留给宋太祖的影子一帧。",
    },
    "n-tang-houzhu": {
        "order": 17,
        "display": "南唐后主",
        "epithet": "江南残梦",
        "tone": "水墨淡彩，湿冷江南",
        "palette": "月白、黛青、胭脂淡、雨灰",
        "bg_list": [
            "金陵夜雨秦淮",
            "澄心堂纸与墨",
            "城破火光映水",
            "汴京小楼窗格",
            "词句墨迹在雨中化开",
        ],
        "char_hooks": "文士肩非帝肩；降表与词稿同框",
        "motif": "古琴断弦",
        "scores": "武15 文35 韬30 祚20 后78 月78",
        "beats": [
            ("0-3s", "印「江南残梦」", "雨", "模板"),
            ("3-14s", "即位，宫中笔墨", "词人皇帝", "E001-E002"),
            ("14-28s", "贬号称臣，宋使", "屈辱", "E003"),
            ("28-42s", "975城破，船离金陵", "记忆点", "E004"),
            ("42-55s", "汴京违命侯，窗雨", "残梦", "E005"),
            ("55-68s", "六维：君道崩、月旦同情；后效在词", "图鉴卡", "片尾"),
        ],
        "idea": "唯一主打**美学失败英雄**。武功条几乎空，但用文学后效撑住卡面尊严。",
    },
    "n-song-tai-zu": {
        "order": 18,
        "display": "宋太祖",
        "epithet": "杯酒释兵",
        "tone": "夜宴烛光，权力温柔一刀",
        "palette": "烛金、酒赤、玄甲卸下后的青衫",
        "bg_list": [
            "陈桥黎明黄袍",
            "开封宫宴长案",
            "酒盏特写（权力道具）",
            "卸甲归第的将领背影",
            "文官上朝队列",
        ],
        "char_hooks": "笑着劝酒的脸；黄袍只给陈桥2秒",
        "motif": "碰杯声=兵权落地",
        "scores": "武80 文93 韬95 祚78 后94 月90",
        "beats": [
            ("0-3s", "印「杯酒释兵」", "碰杯", "模板"),
            ("3-12s", "陈桥黄袍快闪", "副钩", "E001"),
            ("12-30s", "杯酒释兵权完整戏核", "主记忆", "E002"),
            ("30-45s", "先南后北地图推进", "统一", "E003"),
            ("45-55s", "文官潮水涌殿", "后效", "E004"),
            ("55-68s", "六维+卡", "强干弱枝", "片尾"),
        ],
        "idea": "名场面就是酒桌。**战争片一秒，政治片一分钟**。",
    },
    "yuan-shi-zu": {
        "order": 19,
        "display": "元世祖",
        "epithet": "混一车书",
        "tone": "草原风+大都中轴，帝国尺度",
        "palette": "蒙古蓝、银白、宫红、海青",
        "bg_list": [
            "开平草原即位",
            "大都中轴规划",
            "驿站快马网络动画",
            "临安降、崖山浪",
            "行省色块拼图中国",
        ],
        "char_hooks": "胡帽与汉地龙袍元素并存（勿脸谱化）",
        "motif": "马蹄变车辙变印刷车书",
        "scores": "武91 文86 韬87 祚86 后96 月52",
        "beats": [
            ("0-3s", "印「混一车书」", "马蹄转车辙", "模板"),
            ("3-14s", "开平即位争位", "汗", "E001"),
            ("14-28s", "国号元·都大都", "制度与都城", "E002-E003"),
            ("28-45s", "灭宋至崖山", "1279", "E004-E005"),
            ("45-55s", "行省站赤信息图", "后效", "E006"),
            ("55-68s", "六维：后效96月旦52 张力", "图鉴卡", "片尾"),
        ],
        "idea": "与始皇、隋文同一母题**「混一」**，但尺度是欧亚。月旦争议用冷色不说教。",
    },
    "n-wei-taiwu": {
        "order": 20,
        "display": "北魏太武帝",
        "epithet": "真君铁骑",
        "tone": "铁骑史诗，粗粝寒冷",
        "palette": "铁青、雪、佛金碎裂、血褐",
        "bg_list": [
            "平城甲骑出城",
            "统万/姑臧城破烟",
            "北方一统地图合龙",
            "佛像倒下（灭佛，克制）",
            "瓜步江岸北骑南望",
        ],
        "char_hooks": "马高于人；灭佛戏避免煽动，用影子与空殿",
        "motif": "马蹄如雷，佛铃碎",
        "scores": "武96 文62 韬86 祚74 后82 月48",
        "beats": [
            ("0-3s", "印「真君铁骑」", "蹄", "模板"),
            ("3-20s", "灭夏燕凉三连地图", "统一北方", "E002-E004"),
            ("20-35s", "真君灭佛克制镜头", "月旦下拉", "E005"),
            ("35-48s", "南征瓜步", "铁骑极限", "E006"),
            ("48-58s", "被弑宫变快剪", "终", "E007"),
            ("58-70s", "六维武功顶、月旦48", "图鉴卡；可钩孝文后效", "片尾"),
        ],
        "idea": "系列压轴武戏。与孝文「解辫」形成**祖孙对照预告**（统一 vs 汉化）。",
    },
}


def story_md(pid: str, s: dict) -> str:
    bg = "\n".join(f"- {x}" for x in s["bg_list"])
    beats_rows = [
        "| 镜段 | 画面 | 旁白/字幕 | 史料/数据 |",
        "|------|------|-----------|-----------|",
    ]
    for t, shot, vo, src in s["beats"]:
        beats_rows.append(f"| {t} | {shot} | {vo} | {src} |")
    beats = "\n".join(beats_rows)
    return f"""---
id: "{pid}"
display: "{s['display']}"
epithet: "{s['epithet']}"
batch: video-01
order: {s['order']}
duration_target: "60–75s"
updated: "2026-08-06"
---

# 分镜 · {s['order']:02d} · {s['display']}「{s['epithet']}」

> 数据：`data/catalog/video20.json`  
> 史料：`content/sources/{pid}/`  
> 系列规范：`content/video/video-01/README.md`

## 1. 一句话创意

{s['idea']}

## 2. 视觉总调

| 项 | 设定 |
|----|------|
| 气质 | {s['tone']} |
| 色板 | {s['palette']} |
| 人物钩子 | {s['char_hooks']} |
| 声音母题 | {s['motif']} |
| 六维速记 | {s['scores']} |

## 3. 背景图 / 场景库（可做静帧或 AI 底图）

{bg}

## 4. 分镜节拍（约 70s）

{beats}

## 5. 封面信息条（口播/大字）

```
【{s['epithet']}】
{s['display']}
六维 {s['scores']}
```

## 6. 制作备忘

- 史实字幕优先对齐史料卡 `E00x`；演义层必须标「演绎」
- 六维动画：后效与月旦若剪刀差大（如炀帝、始皇、世祖），**分屏强制对照**
- 肖像：本阶段 placeholder，用剪影/后脑/手部亦可
- 地图：古名为主，今地仅角标

## 7. 关联

- 史源卡：`content/sources/{pid}/00-史源卡.md`
- 先导表：`docs/references/catalogs/先导二十人.md`
"""


def write_series_readme():
    VID.mkdir(parents=True, exist_ok=True)
    (VID / "分镜").mkdir(parents=True, exist_ok=True)
    md = """# video-01 · 皇帝图鉴先导二十 · 视频包

> 更新：2026-08-06  
> 数据：`data/catalog/video20.json`  
> 史料：`content/sources/{id}/`  
> 分镜：`content/video/video-01/分镜/{id}.md`

## 产品定位

- **形态**：竖屏或 16:9 短片，单人 **60–75 秒**
- **不是**：正史纪录片长片；**是**：图鉴抽卡 + 六维雷达 + 一个记忆点
- **史实底线**：关键年份/结局/名场面有史料卡支撑；演义标「演绎」
- **月旦 ≠ 知名度**：褒贬轴；与后效剪刀差是内容引擎

## 统一版式（每集必有）

1. **0–3s 片头印**：四字号金/朱印砸落（材质随人变）
2. **中段 1 个记忆核**：只打透一个钩（可副钩 1 个，≤5s）
3. **六维雷达 8–12s**：后效/月旦若反差大，分屏拉扯
4. **片尾图鉴卡**：姓名·政权·四字号·记忆点·六维条

### 字幕层

| 层 | 用途 |
|----|------|
| 大字 | 四字号、记忆点年 |
| 中字 | 旁白要点 |
| 角标 | 史料 E 编号（可选，硬核向） |
| 慎用 | 戏说、网络梗（最多 1 处） |

### 音乐气质分轨建议

| 类型 | 代表 |
|------|------|
| 纪念碑/制度 | 始皇、隋文、元世祖 |
| 燃/铁骑 | 太武、石勒、世宗 |
| 冷核吏治 | 宣帝、宪宗、太祖酒桌 |
| 悲剧/水 | 炀帝、苻坚、后主 |
| 礼佛金粉 | 梁武 |
| 女帝神都 | 武则天 |
| 中兴晴 | 光武、太宗 |

## 系列叙事弧（发布顺序建议）

可按 `video20.json` 列表序，也可主题连播：

| 专辑 | 人 |
|------|-----|
| 混一三连 | 始皇 → 隋文 → 元世祖 |
| 汉家双峰 | 汉武 → 宣帝 → 光武 |
| 南北悲剧 | 苻坚 → 炀帝 → 梁武 |
| 变革之刃 | 孝文 → 武周 → 太祖 |
| 小众硬核 | 石勒 → 元昊 → 太武 → 宪宗 → 世宗 |
| 词与儒 | 王莽 → 后主 |

## 背景图生产提示（通用）

- **优先**：地图色块、建筑剪影、器物特写、天气/材质（避免争议「真实肖像」）
- **AI 底图**：只作气氛，人脸不锁定历史真人照片
- **地图**：谭图/CHGIS 风格简化；朝代边界示意即可
- **统一噪点**：宣纸/绢/夯土纹理压在画面 8–12% 透明度，系列辨识度

## 本批完成度

| 项 | 状态 |
|----|------|
| video20 数值 | ✅ |
| 分镜 20 篇 | ✅ 见 `分镜/` |
| 史料卡（先导） | ✅ 三人 12 条；其余核心 6–8 条 in-progress |
| 配音成片 | ☐ |
| 正式画像 | ☐ 暂缓 |

## 文件索引

见 `分镜/README.md`
"""
    (VID / "README.md").write_text(md, encoding="utf-8")


def write_storyboard_index():
    rows = [
        "| # | id | 人物 | 四字号 | 分镜 | 史料 |",
        "|---|-----|------|--------|------|------|",
    ]
    for pid, s in sorted(STORY.items(), key=lambda x: x[1]["order"]):
        rows.append(
            f"| {s['order']} | `{pid}` | {s['display']} | {s['epithet']} | [{pid}.md](./{pid}.md) | `content/sources/{pid}/` |"
        )
    (VID / "分镜" / "README.md").write_text(
        "# 分镜索引 · video-01\n\n" + "\n".join(rows) + "\n",
        encoding="utf-8",
    )


def fix_typos_in_story():
    """Clean accidental garbage tokens in story text if any slipped in."""
    # written via story_md from STORY; clean STORY fields
    for pid, s in STORY.items():
        for k in ("tone", "idea", "motif", "char_hooks"):
            if k in s and isinstance(s[k], str):
                s[k] = s[k].replace(" thr", "").replace(" fort", "").replace("  ", " ").strip()
        if "bg_list" in s:
            s["bg_list"] = [
                x.replace(" thr", "").replace(" fort", "").replace("  ", " ").strip()
                for x in s["bg_list"]
            ]
        new_beats = []
        for beat in s["beats"]:
            new_beats.append(tuple(
                (b.replace(" thr", "").replace(" fort", "").replace(" bell", "铃").replace(" quant ", "倾 ")
                 if isinstance(b, str) else b)
                for b in beat
            ))
        s["beats"] = new_beats
        # fix known bad strings in n-tang
        if pid == "n-tang-houzhu":
            pass


def main():
    fix_typos_in_story()

    # sources for 17
    for pid, pack in PEOPLE.items():
        if pid in ALREADY_COMPLETE:
            continue
        write_scaffold(pid, pack["meta"], pack["events"])
        print("sources", pid, len(pack["events"]))

    # touch storyboards for complete three: still write story
    write_series_readme()
    for pid, s in STORY.items():
        path = VID / "分镜" / f"{pid}.md"
        path.write_text(story_md(pid, s), encoding="utf-8")
        print("story", pid)

    write_storyboard_index()

    # update content/sources/README.md
    lines = [
        "# 史源 / 史料工作区",
        "",
        "规范：`docs/05-史源卡工作规范.md`",
        "",
        "## 状态总览（video-01 + 首批三人）",
        "",
        "| id | 人物 | status | 史料卡 | 备注 |",
        "|----|------|--------|--------|------|",
        "| qin-shi-huang | 秦始皇 | dossier-complete | 12 | 史记 |",
        "| han-wu-di | 汉武帝 | dossier-complete | 12 | 汉书 |",
        "| tang-tai-zong | 唐太宗 | dossier-complete | 12 | 两唐书 |",
    ]
    for pid, pack in PEOPLE.items():
        m = pack["meta"]
        n = len(pack["events"])
        lines.append(
            f"| {pid} | {m['display']} | in-progress | {n} | video-01 先导 |"
        )
    lines += [
        "",
        "分镜总包：`content/video/video-01/`",
        "全量索引：`data/catalog/emperors_master.json`",
        "",
    ]
    (SRC / "README.md").write_text("\n".join(lines), encoding="utf-8")

    # update 先导二十人.md tail
    cat = ROOT / "docs" / "references" / "catalogs" / "先导二十人.md"
    extra = """

## 史料与分镜（2026-08-06）

| 资源 | 路径 |
|------|------|
| 系列视频包 | `content/video/video-01/README.md` |
| 二十人分镜 | `content/video/video-01/分镜/` |
| 史料卡 | `content/sources/{id}/证据/`（三人 12 条；余 6–8 条先导） |

下一步：配音稿精修 / 扩证据至 dossier-complete / YAML 同步。
"""
    text = cat.read_text(encoding="utf-8")
    if "系列视频包" not in text:
        cat.write_text(text.rstrip() + extra, encoding="utf-8")

    # fix n-tang typo in generated event if any
    bad = SRC / "n-tang-houzhu" / "证据"
    for f in bad.glob("*.md"):
        t = f.read_text(encoding="utf-8")
        if " quant" in t or "倾 力" in t:
            t = t.replace(" quant 力", "倾力").replace("倾 力", "倾力")
            f.write_text(t, encoding="utf-8")

    print("done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="video-01 先导二十人史源卡/分镜种子脚本。默认 dry-run;--apply 写入;--force 允许覆盖。"
    )
    parser.add_argument("--apply", action="store_true", help="真正写入文件（默认仅 dry-run 打印计划）")
    parser.add_argument("--force", action="store_true", help="允许覆盖已存在文件（危险，慎用）")
    cli = parser.parse_args()
    guard_stats = _install_write_guard(cli.apply, cli.force)
    main()
    print(
        "write-guard: planned={planned} written={written} skipped={skipped}".format(
            **guard_stats
        )
    )
