#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为始皇/汉武/太宗写入首批史料卡，并刷新史源卡索引。"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "content" / "sources"


def card(
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
        "- [x] routes" if on_map == "yes" else "- [ ] routes",
        "- [x] relations" if related else "- [ ] relations",
        "",
    ]
    return "\n".join(lines)


QIN = [
    ("E001", "-259", "约前259", "邯郸出生", "生于邯郸，名政，庄襄王子。", "yes", "其他", "邯郸", "handan", [], "high", [("史记", "卷006·始皇帝", "二十四史-简体")], "「以秦昭王四十八年正月生于邯郸…名为政」"),
    ("E002", "-246", "前246", "即位为秦王", "年十三即位，国事委大臣，吕不韦为相。", "yes", "都城", "咸阳", "xianyang", [], "high", [("史记", "卷006·始皇帝", "简体md")], "「年十三岁，庄襄王死，政代立为秦王」"),
    ("E003", "-238", "前238", "王冠亲政", "王冠带剑；平嫪毐之乱，强化王权。", "yes", "都城", "咸阳", "xianyang", [], "high", [("史记", "卷006·始皇帝", "九年条")], "「己酉，王冠，带剑…长信侯毐作乱」"),
    ("E004", "-230", "前230", "灭韩", "灭六国战争展开，韩先亡。", "yes", "亲征", "新郑", "xinzheng", [], "medium", [("史记", "卷006·始皇帝", "灭国编年"), ("资治通鉴", "秦纪", "可对年")], "本纪灭国序列，韩为序幕"),
    ("E005", "-221", "前221", "称始皇帝", "并天下，号始皇帝，分三十六郡。", "yes", "都城", "咸阳", "xianyang", [], "high", [("史记", "卷006·始皇帝", "二十六年")], "「初并天下为三十六郡，号为始皇帝」"),
    ("E006", "-221", "前221前后", "统一制度", "书同文、车同轨等统一措施（择要）。", "no", "", "咸阳", "xianyang", [], "high", [("史记", "卷006·始皇帝", "统一措施")], "制度条可再拆细"),
    ("E007", "-219", "前219", "封禅泰山", "东巡郡县，上泰山立石。", "yes", "巡狩", "泰山", "taishan", ["han-wu-di"], "high", [("史记", "卷006·始皇帝", "二十八年")], "东巡封禅"),
    ("E008", "-213", "前213", "焚书", "李斯议烧诗书百家语。", "no", "", "咸阳", "xianyang", [], "high", [("史记", "卷006·始皇帝", "三十四年")], "据本纪，避免演义化"),
    ("E009", "-212", "前212", "坑术士", "坑杀为妖言的诸生（对象/人数有争议）。", "no", "", "咸阳", "xianyang", [], "medium", [("史记", "卷006·始皇帝", "三十五年")], "见争议表"),
    ("E010", "-210", "前210", "沙丘崩", "出巡途中崩于沙丘平台。", "yes", "巡狩", "沙丘", "shaqiu", ["qin-er-shi"], "high", [("史记", "卷006·始皇帝", "三十七年")], "崩于沙丘平台"),
    ("E011", "-210", "前210", "沙丘嗣位", "矫诏立胡亥，二世即位。", "yes", "都城", "沙丘", "shaqiu", ["qin-er-shi"], "medium", [("史记", "卷006·始皇帝", "附二世")], "关联二世"),
    ("E012", "-207", "前207前后", "秦亡对照", "子婴降、刘邦入关（跨页）。", "yes", "其他", "咸阳", "xianyang", ["han-gao-zu", "qin-er-shi"], "high", [("史记", "高祖本纪", "对照")], "跳转汉高祖"),
]

WU = [
    ("E001", "-156", "约前156", "出生与立储", "景帝中子，后为皇太子。", "no", "", "长安", "chang-an", [], "high", [("汉书", "卷006·武帝", "简体md")], "景帝中子…皇太子"),
    ("E002", "-141", "建元元年", "即位", "景帝崩，太子即位，改元建元。", "yes", "都城", "长安", "chang-an", [], "high", [("汉书", "卷006·武帝", "建元元年")], "太子即皇帝位"),
    ("E003", "-141", "建元元年", "举贤良", "诏举贤良；罢治申商韩苏张之言。", "no", "", "长安", "chang-an", [], "high", [("汉书", "卷006·武帝", "建元元年十月")], "思想取向"),
    ("E004", "-136", "建元五年", "置五经博士", "置五经博士。", "no", "", "长安", "chang-an", [], "high", [("汉书", "卷006·武帝", "建元五年")], "儒学制度化"),
    ("E005", "-138", "建元三年", "东瓯告急", "闽越围东瓯，遣兵浮海。", "maybe", "其他", "东南", "", [], "medium", [("汉书", "卷006·武帝", "建元三年")], "开边序曲"),
    ("E006", "-133", "元光二年", "马邑之谋", "诱单于，汉匈战争格局开启。", "maybe", "亲征", "马邑", "", [], "high", [("汉书", "卷006·武帝", "元光"), ("资治通鉴", "汉纪", "对年")], "place 待补"),
    ("E007", "-127", "元朔二年", "河南朔方", "取河南地，经营朔方。", "yes", "亲征", "朔方", "shuofang", [], "high", [("汉书", "卷006·武帝", "元朔")], "北边节点"),
    ("E008", "-121", "元狩二年", "河西之役", "打通河西走廊方向。", "yes", "亲征", "河西", "hexi", [], "high", [("汉书", "卷006·武帝", "元狩")], "通西域前提"),
    ("E009", "-110", "元封元年", "封禅泰山", "东巡封禅。", "yes", "巡狩", "泰山", "taishan", ["qin-shi-huang"], "high", [("汉书", "卷006·武帝", "元封"), ("史记", "封禅书", "互见")], "与始皇对照"),
    ("E010", "-104", "太初元年", "太初改历", "太初历与年号时间秩序。", "no", "", "长安", "chang-an", [], "high", [("汉书", "卷006·武帝", "太初元年")], "制度史"),
    ("E011", "-91", "征和二年", "巫蛊之祸", "卫太子案，宫廷震荡（克制叙述）。", "no", "", "长安", "chang-an", [], "medium", [("汉书", "卷006·武帝", "征和")], "低戏剧化"),
    ("E012", "-89", "征和四年", "轮台诏", "悔远征伐，调整政策。", "no", "", "长安", "chang-an", [], "high", [("汉书", "卷006·武帝", "征和末")], "晚岁转向"),
]

TANG = [
    ("E001", "598", "开皇十八年", "生于武功", "高祖第二子李世民。", "yes", "其他", "武功", "chang-an", [], "high", [("旧唐书", "卷2·太宗上", "简体md")], "生于武功之别馆"),
    ("E002", "617", "大业末", "太原义举", "潜图义举，义兵起于太原。", "yes", "起兵", "晋阳", "jinyang", [], "high", [("旧唐书", "卷2·太宗上", "太原")], "潜图义举…义兵起"),
    ("E003", "617", "义宁元年", "霍邑之战", "力阻班师，克霍邑西进。", "yes", "起兵", "霍邑", "", [], "high", [("旧唐书", "卷2·太宗上", "霍邑")], "place 待补"),
    ("E004", "618", "武德元年", "唐朝建立", "李渊称帝，世民为秦王。", "yes", "都城", "长安", "chang-an", [], "high", [("旧唐书", "高祖本纪/太宗纪", "武德")], "即位前节点"),
    ("E005", "621", "武德四年", "定中原战功", "破王世充、窦建德系关键战役（择要）。", "maybe", "亲征", "洛阳", "luoyang", [], "medium", [("旧唐书", "卷2·太宗上", "武德")], "可再拆"),
    ("E006", "626", "武德九年", "玄武门之变", "宫变后即位。", "yes", "其他", "玄武门", "xuanwu-men", [], "high", [("旧唐书", "卷2", "武德九年"), ("资治通鉴", "唐纪", "对读")], "表述克制"),
    ("E007", "627", "贞观元年", "改元贞观", "贞观政治开端。", "yes", "都城", "长安", "chang-an", [], "high", [("旧唐书", "太宗纪", "贞观元年")], "年号"),
    ("E008", "630", "贞观四年", "破突厥", "北境大捷。", "yes", "亲征", "阴山", "yinshan", [], "high", [("旧唐书", "太宗纪", "贞观四年")], "天可汗叙事"),
    ("E009", "643", "贞观十七年", "凌烟阁", "图画功臣。", "yes", "都城", "长安", "chang-an", [], "high", [("旧唐书", "太宗纪", "凌烟")], "用人象征"),
    ("E010", "645", "贞观十九年", "亲征辽东", "御驾东征。", "yes", "亲征", "辽东", "liaodong", [], "high", [("旧唐书", "太宗纪", "贞观十九年")], "晚年军事"),
    ("E011", "649", "贞观二十三年", "崩于长安", "庙号太宗。", "yes", "都城", "长安", "chang-an", [], "high", [("旧唐书", "太宗纪", "二十三年")], "终章"),
    ("E012", "627", "贞观年间", "用人纳谏", "房杜魏徵等君臣结构（总括卡）。", "no", "", "长安", "chang-an", [], "medium", [("旧唐书", "魏徵等传", "按需")], "入 bio"),
]


def write_person(person_id: str, rows: list) -> list:
    d = SRC / person_id / "证据"
    d.mkdir(parents=True, exist_ok=True)
    for p in d.glob("E*.md"):
        p.unlink()
    index = []
    for row in rows:
        (
            eid,
            year,
            date_note,
            title,
            summary,
            on_map,
            route,
            place,
            pid,
            related,
            conf,
            sources,
            quote,
        ) = row
        text = card(
            eid,
            person_id,
            year,
            date_note,
            title,
            summary,
            on_map,
            route,
            place,
            pid,
            related,
            conf,
            sources,
            quote,
            True,
        )
        fname = f"{eid}-{title}.md"
        (d / fname).write_text(text, encoding="utf-8")
        index.append((eid, year, title, on_map, conf, fname))
    return index


def patch_source_card(person_id: str, display: str, index: list, extra_status: str) -> None:
    path = SRC / person_id / "00-史源卡.md"
    on_map_n = sum(1 for r in index if r[3] == "yes")
    table = ["| eid | 年 | 标题 | on_map | confidence | enter_product | 文件 |", "|-----|----|------|--------|------------|---------------|------|"]
    for eid, year, title, on_map, conf, fname in index:
        table.append(f"| {eid} | {year} | {title} | {on_map} | {conf} | yes | `{fname}` |")
    body = f"""---
id: "{person_id}"
display_name: "{display}"
status: dossier-complete
tier: emperor
updated: "2026-08-06"
---

# 史源卡 · {display}

> 已据「二十四史-简体 / 通鉴-简体」落成首批 12 条史料卡（可再增补）。

## 0. 状态看板

| 项 | 状态 |
|----|------|
| 材料包 | ☑ ready |
| 证据卡数量 | {len(index)} |
| 可上地图条数 | {on_map_n} |
| 产品 YAML | ☑ 将同步 timeline |
| 画像 | 暂缓 |

## 4. 证据卡索引

{chr(10).join(table)}

## 说明

- 主文本路径见 `02-书目清单.md` 与 `HuangDiTujian-Ref/11-史料卡工作台/{person_id}.md`
- {extra_status}
"""
    path.write_text(body, encoding="utf-8")


def main() -> None:
    for pid, display, rows, note in [
        ("qin-shi-huang", "秦始皇", QIN, "主据史记卷006；通鉴可对年。"),
        ("han-wu-di", "汉武帝", WU, "主据汉书卷006；史记封禅等互见。"),
        ("tang-tai-zong", "唐太宗", TANG, "主据旧唐书卷2；新唐/通鉴对照。"),
    ]:
        idx = write_person(pid, rows)
        patch_source_card(pid, display, idx, note)
        print(pid, len(idx))


if __name__ == "__main__":
    main()
