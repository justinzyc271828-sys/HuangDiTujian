#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 emperors_master 中尚无 content/sources 的条目批量生成
与 video-01 同结构的史源包 + 史料卡（短祚 6 条 / 一般 12 条）。

性质：索引驱动的「dossier-scaffold」——
- 年号/在位起讫取自 master
- 出处锚定各朝正史本纪/载记入口
- 中段事件为可扩写骨架（confidence: medium），待本纪精读后替换为 A 级细卡

已有 sources 的 id 一律跳过。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "content" / "sources"
MASTER = ROOT / "data" / "catalog" / "emperors_master.json"
REF_WB = ROOT / "HuangDiTujian-Ref" / "11-史料卡工作台"
TPL = SRC / "_templates" / "史料卡.template.md"

# dynasty_id -> (A书, A篇提示, B书)
DYNASTY_SRC: dict[str, tuple[str, str, str]] = {
    "qin": ("史记", "秦始皇本纪/相关", "资治通鉴"),
    "w-han": ("汉书", "本纪", "资治通鉴"),
    "xin": ("汉书", "王莽传", "资治通鉴"),
    "e-han": ("后汉书", "本纪", "资治通鉴"),
    "cao-wei": ("三国志", "魏书本纪", "资治通鉴"),
    "shu-han": ("三国志", "蜀书先主/后主传", "资治通鉴"),
    "sun-wu": ("三国志", "吴书本纪", "资治通鉴"),
    "w-jin": ("晋书", "帝纪", "资治通鉴"),
    "e-jin": ("晋书", "帝纪", "资治通鉴"),
    "liu-song": ("宋书", "本纪", "资治通鉴"),
    "nan-qi": ("南齐书", "本纪", "资治通鉴"),
    "liang": ("梁书", "本纪", "资治通鉴"),
    "chen": ("陈书", "本纪", "资治通鉴"),
    "n-wei": ("魏书", "本纪", "资治通鉴"),
    "e-wei": ("魏书/北史", "本纪", "资治通鉴"),
    "w-wei": ("周书/北史", "本纪", "资治通鉴"),
    "n-qi": ("北齐书", "本纪", "资治通鉴"),
    "n-zhou": ("周书", "本纪", "资治通鉴"),
    "sui": ("隋书", "本纪", "资治通鉴"),
    "tang": ("旧唐书", "本纪", "新唐书/资治通鉴"),
    "zhou-wu": ("旧唐书", "则天皇后纪", "新唐书"),
    "hou-liang": ("旧五代史", "梁书", "新五代史/资治通鉴"),
    "hou-tang": ("旧五代史", "唐书", "新五代史"),
    "hou-jin": ("旧五代史", "晋书", "新五代史"),
    "hou-han": ("旧五代史", "汉书", "新五代史"),
    "hou-zhou": ("旧五代史", "周书", "新五代史"),
    "n-song": ("宋史", "本纪", "续资治通鉴"),
    "s-song": ("宋史", "本纪", "续资治通鉴"),
    "liao": ("辽史", "本纪", "契丹国志等"),
    "jin": ("金史", "本纪", "大金国志等"),
    "yuan": ("元史", "本纪", "新元史/通鉴续编等"),
    "ming": ("明史", "本纪", "明实录入口"),
    "qing": ("清史稿", "本纪", "清实录入口"),
    "xixia": ("宋史", "夏国传", "西夏书事等"),
    # 十六国/十国等
    "q-zhao": ("晋书", "载记", "资治通鉴"),
    "h-zhao": ("晋书", "载记", "资治通鉴"),
    "q-yan": ("晋书", "载记", "资治通鉴"),
    "h-yan": ("晋书", "载记", "资治通鉴"),
    "b-yan": ("晋书", "载记", "资治通鉴"),
    "q-qin": ("晋书", "载记", "资治通鉴"),
    "h-qin": ("晋书", "载记", "资治通鉴"),
    "x-qin": ("晋书", "载记", "资治通鉴"),
    "q-liang": ("晋书", "载记", "资治通鉴"),
    "h-liang": ("晋书", "载记", "资治通鉴"),
    "n-liang": ("晋书", "载记", "资治通鉴"),
    "b-liang": ("晋书", "载记", "资治通鉴"),
    "x-liang": ("晋书", "载记", "资治通鉴"),
    "cheng-han": ("晋书", "载记", "资治通鉴"),
    "xia": ("晋书/魏书", "赫连等", "资治通鉴"),
    "dai": ("魏书", "序纪等", "资治通鉴"),
    "shi-wu": ("晋书", "载记", "资治通鉴"),
    "n-tang": ("宋史", "南唐世家", "马令/陆游南唐书"),
    "wuyue": ("宋史", "吴越世家", "十国春秋"),
    "min": ("宋史", "闽世家", "十国春秋"),
    "chu": ("宋史", "楚世家", "十国春秋"),
    "n-han": ("宋史", "北汉/南汉世家", "十国春秋"),
    "b-han": ("宋史", "北汉世家", "十国春秋"),
    "q-shu": ("宋史", "前蜀世家", "十国春秋"),
    "h-shu": ("宋史", "后蜀世家", "十国春秋"),
    "jingnan": ("宋史", "荆南世家", "十国春秋"),
}


def parse_year(s: str | None) -> int | None:
    if s is None or s == "" or s == "null":
        return None
    s = str(s).strip()
    try:
        return int(s)
    except ValueError:
        m = re.match(r"^-?\d+", s)
        return int(m.group(0)) if m else None


def year_span(start: str, end: str) -> int | None:
    a, b = parse_year(start), parse_year(end)
    if a is None or b is None:
        return None
    return abs(b - a)


def safe_name(s: str) -> str:
    """Filename-safe title fragment."""
    s = re.sub(r'[\\/:*?"<>|]', "", s)
    s = s.replace(" ", "")
    return s[:24] if len(s) > 24 else s


def card_md(pid, eid, year, date_note, title, summary, on_map, route, place, conf, book_a, juan_a, note):
    return f"""---
eid: {eid}
person_id: "{pid}"
year: "{year}"
date_note: "{date_note}"
title: "{title}"
on_map: {on_map}
route_group: "{route}"
place_ancient: "{place}"
place_id_candidate: ""
related_ids: []
confidence: {conf}
enter_product: true
status: draft
batch: master-bulk-scaffold
---

# {eid} · {title}

## 史实摘要

{summary}

## 地点

- 古名：{place or "—"}
- place_id：—
- 上地图：{on_map}
- 路线组：{route or "—"}

## 关联人物

—

## 出处

| 文献 | 篇卷 | 笔记 |
|------|------|------|
| {book_a} | {juan_a} | {note} |

## 自用要点

骨架卡：请据本纪原文改写摘要并升 confidence。

## 是否进入产品

- [x] timeline
- [x] bio
- [ ] routes
- [ ] relations
"""


def build_events(emp: dict) -> list[dict]:
    """Lifecycle skeleton events."""
    display = emp["display"]
    personal = emp.get("personal") or display
    dynasty = emp["dynasty"]
    start = emp.get("reign_start") or "undated"
    end = emp.get("reign_end") or "undated"
    span = year_span(str(start), str(end))
    short = span is not None and span <= 1
    note = emp.get("note") or ""
    tier = emp.get("tier", "emperor")

    book_a, juan_a, book_b = DYNASTY_SRC.get(
        emp["dynasty_id"], ("正史", "本纪/载记", "资治通鉴")
    )
    juan = f"{juan_a}（{display}）"

    def ev(year, date_note, title, summary, on_map="maybe", route="", place="", conf="medium"):
        return {
            "year": str(year),
            "date_note": date_note,
            "title": title,
            "summary": summary,
            "on_map": on_map,
            "route": route,
            "place": place,
            "conf": conf,
            "book": book_a,
            "juan": juan,
            "src_note": f"master 索引驱动；对照 {book_b}",
        }

    if short or tier == "quasi" and span is not None and span <= 2:
        # 6 cards
        events = [
            ev(start, f"在位起 {start}", "即位或主政", f"{personal}（{display}）于{dynasty}进入在位/主政阶段。{note}".strip(), "yes", "都城", "", "medium"),
            ev(start, f"{start}", "年号与名分", f"{display}确立年号/名号，{dynasty}政权序列中的定位见本纪。", "no", "", "", "medium"),
            ev("undated", "在位间", "中枢与用人", f"{display}在位期间的中枢决策与重要人事，细节待本纪精填。", "no", "", "", "low"),
            ev("undated", "在位间", "边事或内政", f"{display}任内边防、藩镇/部族或国内重大政务节点（待补）。", "maybe", "其他", "", "low"),
            ev(end, f"在位讫 {end}", "在位结束", f"{display}在位结束于 {end}（崩/逊/废/亡，以本纪为准）。", "yes", "都城", "", "medium"),
            ev(end, f"{end}", "继统与史评", f"{display}身后继统与史臣评价入口；准帝/短祚者见 note：{note or '无'}。", "no", "", "", "medium"),
        ]
        return events

    # 12 cards standard
    mid = "undated"
    if span is not None and span >= 4:
        a, b = parse_year(str(start)), parse_year(str(end))
        if a is not None and b is not None:
            mid_y = a + (b - a) // 2 if b >= a else a - (a - b) // 2
            mid = str(mid_y)

    events = [
        ev(start, f"在位起 {start}", "即位", f"{personal}即{dynasty}帝位/主位，是为{display}。", "yes", "都城", "", "medium"),
        ev(start, f"{start}", "建元改元", f"{display}建元或改元，开启本朝年号纪年。", "no", "", "", "medium"),
        ev(start, f"{start}初", "初政措置", f"{display}即位初期人事、大赦、礼仪等初政（待本纪条列）。", "yes", "都城", "", "low"),
        ev("undated", "在位前中期", "中枢制度", f"{display}任内官制、财政或礼法相关措置（骨架）。", "no", "", "", "low"),
        ev("undated", "在位前中期", "边事武功", f"{display}任内征伐、和议或边防节点（有则填实，无则标待考）。", "maybe", "亲征", "", "low"),
        ev(mid, f"约 {mid}", "中期政务高峰", f"{display}在位中期的代表性政务或危机处理（待精读）。", "yes", "都城", "", "low"),
        ev("undated", "在位中期", "封赏与宗室", f"宗室、功臣封赏与藩王安排等（待补）。", "no", "", "", "low"),
        ev("undated", "在位中期", "文教礼乐", f"学校、科举端倪、修史、礼乐等文治面向（有则写，无则弱化）。", "no", "", "", "low"),
        ev("undated", "在位后期", "危机与应对", f"{display}后期天灾、兵变、权臣或外患等压力点（待本纪）。", "maybe", "其他", "", "low"),
        ev(end, f"在位讫 {end}", "崩或逊位", f"{display}于 {end} 结束在位（崩/禅/废）。", "yes", "都城", "", "medium"),
        ev(end, f"{end}", "储位继统", f"继承人选立与交接；与前后任交叉引用待补。", "yes", "都城", "", "medium"),
        ev("undated", "史评", "史臣总评入口", f"正史本纪赞/论及通鉴史评入口；note：{note or '无特殊注'}。", "no", "", "", "medium"),
    ]
    return events


def write_person(emp: dict) -> int:
    pid = emp["id"]
    d = SRC / pid
    if (d / "00-史源卡.md").exists():
        return 0

    events = build_events(emp)
    book_a, juan_a, book_b = DYNASTY_SRC.get(
        emp["dynasty_id"], ("正史", "本纪/载记", "资治通鉴")
    )
    display = emp["display"]
    personal = emp.get("personal") or ""
    dynasty = emp["dynasty"]
    tier = emp.get("tier", "emperor")
    start, end = emp.get("reign_start", ""), emp.get("reign_end", "")

    evid = d / "证据"
    evid.mkdir(parents=True, exist_ok=True)
    (d / "摘录").mkdir(exist_ok=True)
    (d / "摘录" / ".gitkeep").write_text("", encoding="utf-8")
    if TPL.exists():
        (evid / "_template.md").write_text(TPL.read_text(encoding="utf-8"), encoding="utf-8")

    index_rows = []
    map_n = 0
    for i, ev in enumerate(events, 1):
        eid = f"E{i:03d}"
        title = ev["title"]
        fname = f"{eid}-{safe_name(title)}.md"
        if ev["on_map"] == "yes":
            map_n += 1
        md = card_md(
            pid,
            eid,
            ev["year"],
            ev["date_note"],
            title,
            ev["summary"],
            ev["on_map"],
            ev["route"],
            ev["place"],
            ev["conf"],
            ev["book"],
            ev["juan"],
            ev["src_note"],
        )
        (evid / fname).write_text(md, encoding="utf-8")
        index_rows.append(
            f"| {eid} | {ev['year']} | {title} | {ev['on_map']} | {ev['conf']} | yes | `{fname}` |"
        )

    n = len(events)
    # scaffold: ready-to-fill if only skeleton; mark dossier-scaffold-complete for structure
    status = "dossier-scaffold"
    dossier = f"""---
id: "{pid}"
display_name: "{display}"
status: {status}
tier: {tier}
dynasty: "{dynasty}"
updated: "2026-08-06"
batch: master-bulk-scaffold
---

# 史源卡 · {display}

> **批量脚手架**（master-bulk-scaffold）：结构与 video-01 对齐（{n} 条史料卡），  
> 摘要多为在位生命周期骨架，**须据 {book_a}·{juan_a} 精读后改写** 方可升为 dossier-complete。

## 0. 状态看板

| 项 | 状态 |
|----|------|
| 材料包 | ☑ scaffold（{n} 条） |
| 证据卡数量 | {n} |
| 可上地图条数 | {map_n}（多为占位） |
| 产品 YAML | ☐ 多数未建 |
| 精读升格 | ☐ 待办 |

## 1. 身份速查

| 字段 | 内容 |
|------|------|
| id | `{pid}` |
| 显示名 | {display} |
| 姓名 | {personal} |
| 王朝 | {dynasty} |
| 序列 | {emp.get('sequence', '')} |
| 在位起 | {start} |
| 在位讫 | {end} |
| tier | {tier} |
| note | {emp.get('note') or '—'} |

## 2. 主文献地图

| 优先级 | 文献 | 篇卷 | 用途 |
|--------|------|------|------|
| A | {book_a} | {juan_a} | 主叙事 |
| B | {book_b} | 对应年段 | 编年 |

本地：`HuangDiTujian-Ref/01-史书全文与扫描/`

## 3. 证据卡索引

| eid | 年 | 标题 | on_map | confidence | enter_product | 文件 |
|-----|----|------|--------|------------|---------------|------|
{chr(10).join(index_rows)}

## 4. 升格清单（scaffold → complete）

- [ ] 每条摘要改为本纪可核对的具体史实  
- [ ] confidence 升 medium/high，补 place_id  
- [ ] 至少 5 条 on_map=yes 且有古地名  
- [ ] 06-争议非空或写「暂无」  
- [ ] status 改为 `dossier-complete`

## 5. 下一步

1. `python tools/search_ref.py "{display}"` 或本纪关键词  
2. 改 E00x 正文  
3. 同步 `data/emperors/{pid}.yaml`  
"""
    (d / "00-史源卡.md").write_text(dossier, encoding="utf-8")
    (d / "01-阅读顺序.md").write_text(
        f"# 阅读顺序 · {display}\n\n1. {book_a} {juan_a}\n2. {book_b}\n3. 本夹 `证据/` 逐条升格\n",
        encoding="utf-8",
    )
    (d / "02-书目清单.md").write_text(
        f"# 书目 · {display}\n\n| 级 | 书 | 状态 |\n|----|-----|------|\n| A | {book_a} {juan_a} | 库内可检索 |\n| B | {book_b} | 库内/待标卷 |\n",
        encoding="utf-8",
    )
    (d / "03-地点候选表.md").write_text(
        f"# 地点候选 · {display}\n\n| 古名 | 今地猜想 | place_id | 备注 |\n|------|----------|----------|------|\n| （待填） | | | 都城/崩地 |\n",
        encoding="utf-8",
    )
    (d / "04-关联人物候选表.md").write_text(
        f"# 关联人物 · {display}\n\n| 关系 | 人物 | 备注 |\n|------|------|------|\n| 前任/后任 | （master 同朝序列） | 待填 |\n",
        encoding="utf-8",
    )
    (d / "05-路线草稿.md").write_text(
        f"# 路线草稿 · {display}\n\n骨架阶段仅占位；升格后据 on_map 条整理。\n",
        encoding="utf-8",
    )
    (d / "06-争议与待考.md").write_text(
        f"# 争议与待考 · {display}\n\n- master.note：{emp.get('note') or '（无）'}\n- 本包为批量脚手架，史实细节待考。\n",
        encoding="utf-8",
    )
    (d / "README.md").write_text(
        f"# {display} / `{pid}`\n\n- status: **{status}**（{n} 条骨架史料卡）\n- 升格后改 `00-史源卡.md` status → dossier-complete\n",
        encoding="utf-8",
    )

    REF_WB.mkdir(parents=True, exist_ok=True)
    (REF_WB / f"{pid}.md").write_text(
        f"# 工作台 · {display}\n\n- sources: `content/sources/{pid}/`\n- A: {book_a} {juan_a}\n- batch: master-bulk-scaffold\n",
        encoding="utf-8",
    )
    return n


def main():
    data = json.loads(MASTER.read_text(encoding="utf-8"))
    emps = data["emperors"]
    have = {
        d.name
        for d in SRC.iterdir()
        if d.is_dir() and not d.name.startswith("_") and (d / "00-史源卡.md").exists()
    }
    missing = [e for e in emps if e["id"] not in have]
    print(f"master={len(emps)} have={len(have)} missing={len(missing)}")

    total_cards = 0
    for i, emp in enumerate(missing, 1):
        n = write_person(emp)
        total_cards += n
        if i % 50 == 0 or i == len(missing):
            print(f"  … {i}/{len(missing)} cards_so_far={total_cards}")

    # refresh sources README summary
    statuses = {}
    card_sum = 0
    for d in sorted(SRC.iterdir()):
        if not d.is_dir() or d.name.startswith("_") or not (d / "00-史源卡.md").exists():
            continue
        st = "?"
        for line in (d / "00-史源卡.md").read_text(encoding="utf-8").splitlines()[:15]:
            if line.startswith("status:"):
                st = line.split(":", 1)[1].strip()
                break
        n = len([p for p in (d / "证据").glob("E*.md") if p.name != "_template.md"])
        statuses[st] = statuses.get(st, 0) + 1
        card_sum += n

    readme = f"""# 史源 / 史料工作区

规范：`docs/05-史源卡工作规范.md`  
看板：`docs/08-项目进度看板.md`

## 状态总览（master 全量批量后）

| status | 人数 |
|--------|------|
"""
    for k, v in sorted(statuses.items()):
        readme += f"| {k} | {v} |\n"
    readme += f"""
| **合计目录** | **{sum(statuses.values())}** |
| **E 卡合计** | **{card_sum}** |

### 说明

- `dossier-complete`：先导样板（video-01 等），可支撑产品精写  
- `dossier-scaffold`：**master 全量脚手架**——结构齐、出处锚定本纪入口，摘要待精读升格  
- 生成脚本：`tools/seed_master_all_sources.py`  

### 升格命令提示

```bash
python tools/search_ref.py "帝号或姓名" --book 史记
```
"""
    (SRC / "README.md").write_text(readme, encoding="utf-8")
    print("DONE", "dirs", sum(statuses.values()), "cards", card_sum, statuses)


if __name__ == "__main__":
    main()
