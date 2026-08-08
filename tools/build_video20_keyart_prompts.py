#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build video-01 key-art: appearance-grounded EN prompts + ZH overlays."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from keyart_appearance_data import NEGATIVE, PREFIX, SCENES, SUFFIX  # noqa: E402

OUT = ROOT / "content" / "video" / "video-01" / "key-art"
CARDS = OUT / "cards"
VIDEO20 = ROOT / "data" / "catalog" / "video20.json"

AXIS_LABELS = [
    ("wugong", "武功"),
    ("wenzhi", "文治"),
    ("taolue", "韬略"),
    ("guozuo", "国祚"),
    ("houxiao", "后效"),
    ("yuedan", "月旦"),
]


def full_prompt(body: str) -> str:
    return PREFIX + body.strip().rstrip(",") + ", " + SUFFIX


def personal_name(p: dict) -> str:
    raw = (p.get("personal") or p.get("display") or "").strip()
    if "（" in raw:
        raw = raw.split("（", 1)[0].strip()
    if "(" in raw:
        raw = raw.split("(", 1)[0].strip()
    return raw


def name_title_line(p: dict) -> str:
    name = personal_name(p)
    title = (p.get("display") or "").strip()
    if not title or title == name:
        return name
    return f"{name}\n{title}"


def card_md(p: dict, sc: dict) -> str:
    scores = p["scores"]
    score_lines = " · ".join(f"{zh}{scores[k]}" for k, zh in AXIS_LABELS)
    radar_rows = "\n".join(f"| {zh} | {scores[k]} |" for k, zh in AXIS_LABELS)
    rep_block = "\n".join(sc["event_zh"])
    name_block = name_title_line(p)
    pname = personal_name(p)
    fp = full_prompt(sc["prompt"])
    src_lines = "\n".join(f"- {x}" for x in sc["appearance_sources_zh"])
    costume_src_lines = "\n".join(f"- {x}" for x in sc.get("costume_sources_zh", []) or ["- （见外貌史源）"])
    return f"""---
id: "{p['id']}"
display: "{p['display']}"
personal: "{pname}"
epithet: "{p['epithet']}"
order: {sc['order']}
batch: video-01
type: key-art-static
appearance_level: "{sc['appearance_level']}"
naming: "personal-first then title; no book-title marks on events"
prompt_rule: "self-contained description; do not rely on model recognizing the name"
---

# Key Art · {sc['order']:02d} · {pname}（{p['display']}）「{p['epithet']}」

## 1. 中文叠字（后期 UI，勿写入 Image）

> **命名**：本名在上，称号在下；代表事**无书名号**。

### 右上 · 代表事

```
[{sc['event_label']}]
{rep_block}
```

### 右下 · 四字号 + 姓名

```
[{p['epithet']}]
{name_block}
```

### 可选顶栏

```
皇帝图鉴 · 先导 video-01
```

### 左下雷达

| 轴 | 分 |
|----|-----|
{radar_rows}

`{score_lines}`

## 2. 造型总规格（外貌·冠服·饰品·背景·画风）

| 项 | 内容 |
|----|------|
| 定格年龄 | {sc['age_moment_zh']} |
| 外貌证据 | **{sc['appearance_level']}** |
| 冠服证据 | **{sc.get('costume_level', sc['appearance_level'])}** |
| 一句话场景 | {sc['scene_one_liner_zh']} |
| 势力画风 | {sc['style_faction_zh']} |
| 气质 | {sc['mood_zh']} |

### 2.1 史源

**外貌：**
{src_lines}

**冠服：**
{costume_src_lines}

### 2.2 外貌（脸·体）

{sc['appearance_zh']}

### 2.3 冠服（必须设计进画面）

{sc.get('costume_zh', '（见英文 COSTUME 段）')}

### 2.4 饰品与道具

{sc.get('accessories_zh', sc.get('props_zh', ''))}

### 2.5 背景空间

{sc.get('background_zh', '')}

### 2.6 画风·势力气质

{sc['style_faction_zh']} · {sc['mood_zh']}

> **A**=正史明文 · **B**=制度/族属/纪年可限定 · **C**=时代合理重建（勿伪称写真）

## 3. English image prompt（COSTUME / ACCESSORIES / BACKGROUND / STYLE 分段写死）

### Positive

```
{fp}
```

### Negative

```
{NEGATIVE}
```

### Settings

- Aspect **16:9**
- Do **not** only type the historical name and hope the model knows him
- Face / body / clothes / set / style are all spelled out above

## 4. Post checklist

- [ ] 脸：鼻/须/体型/年龄  
- [ ] 冠服：朝代对、颜色对、有「禁项」没画错  
- [ ] 饰品道具：与代表事件咬合  
- [ ] 背景：地点事件可读  
- [ ] 画风：势力气质（不是统一皮肤）  
- [ ] 无字无 UI；左下右缘留暗  
- [ ] 叠字：本名优先 + 代表事无书名号  
"""


def main():
    data = json.loads(VIDEO20.read_text(encoding="utf-8"))
    profiles = {p["id"]: p for p in data["profiles"]}
    CARDS.mkdir(parents=True, exist_ok=True)

    overlay = {
        "version": "2.1",
        "batch": "video-01",
        "prompt_rule": "appearance-grounded composition-safe EN; no name-only prompts",
        "axes": [zh for _, zh in AXIS_LABELS],
        "cards": [],
    }
    table_rows = [
        "| # | id | 本名/称号 | 外貌证据 | 定格年龄 | 势力画风 | 卡 |",
        "|---|-----|-----------|----------|----------|----------|-----|",
    ]
    en_only = [
        "# video-01 key-art EN prompts v4 — appearance-grounded, composition-safe",
        "# Do not rely on the model recognizing historical names",
        "",
    ]

    missing = []
    for pid, sc in sorted(SCENES.items(), key=lambda x: x[1]["order"]):
        if pid not in profiles:
            missing.append(pid)
            continue
        p = profiles[pid]
        (CARDS / f"{pid}.md").write_text(card_md(p, sc), encoding="utf-8")
        fp = full_prompt(sc["prompt"])
        en_only += [
            f"## {sc['order']:02d} | {pid} | {personal_name(p)} | level {sc['appearance_level']}",
            f"# face note: {sc['appearance_zh'][:80]}...",
            "",
            fp,
            "",
            f"NEGATIVE: {NEGATIVE}",
            "",
            "---",
            "",
        ]
        table_rows.append(
            f"| {sc['order']} | `{pid}` | **{personal_name(p)}** / {p['display']} | "
            f"{sc['appearance_level']} | {sc['age_moment_zh']} | {sc['style_faction_zh'][:24]}… | "
            f"[cards/{pid}.md](cards/{pid}.md) |"
        )
        overlay["cards"].append(
            {
                "id": pid,
                "order": sc["order"],
                "personal": personal_name(p),
                "display": p["display"],
                "name_lines": name_title_line(p).split("\n"),
                "epithet": p["epithet"],
                "appearance_level": sc["appearance_level"],
                "costume_level": sc.get("costume_level"),
                "age_moment_zh": sc["age_moment_zh"],
                "appearance_zh": sc["appearance_zh"],
                "costume_zh": sc.get("costume_zh"),
                "accessories_zh": sc.get("accessories_zh"),
                "background_zh": sc.get("background_zh"),
                "style_faction_zh": sc["style_faction_zh"],
                "appearance_sources_zh": sc["appearance_sources_zh"],
                "costume_sources_zh": sc.get("costume_sources_zh"),
                "event_lines": sc["event_zh"],
                "scores": p["scores"],
                "prompt_en": fp,
                "negative_en": NEGATIVE,
            }
        )

    (OUT / "01-二十人主画面总表.md").write_text(
        "# 二十人静态主画面总表（v2 外貌史证）\n\n"
        "> 英文 prompt **自足描写**，不靠模型「认出人名」。\n"
        "> 数据源：`tools/keyart_appearance_data.py`\n\n"
        + "\n".join(table_rows)
        + "\n\n- 叠字 JSON：`overlay-zh.json`\n"
        "- 批跑：`prompts-en-only.txt`\n",
        encoding="utf-8",
    )
    (OUT / "prompts-en-only.txt").write_text("\n".join(en_only), encoding="utf-8")
    (OUT / "overlay-zh.json").write_text(
        json.dumps(overlay, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # appearance + costume index
    app_idx = [
        "# 外貌·冠服·背景·画风索引（v3）\n",
        "> 从 `tools/keyart_appearance_data.py` 生成\n",
    ]
    for pid, sc in sorted(SCENES.items(), key=lambda x: x[1]["order"]):
        p = profiles.get(pid, {})
        app_idx += [
            f"## {sc['order']:02d} {personal_name(p)}（{p.get('display','')}）",
            "",
            f"- 外貌证据：{sc['appearance_level']} · 冠服证据：{sc.get('costume_level','')}",
            f"- 年龄定格：{sc['age_moment_zh']}",
            f"- 画风：{sc['style_faction_zh']}",
            "",
            "### 外貌",
            sc["appearance_zh"],
            "",
            "### 冠服",
            sc.get("costume_zh", ""),
            "",
            "### 饰品道具",
            sc.get("accessories_zh", ""),
            "",
            "### 背景",
            sc.get("background_zh", ""),
            "",
            "---",
            "",
        ]
    (OUT / "02-外貌史证索引.md").write_text("\n".join(app_idx), encoding="utf-8")

    readme = f"""# Key Art · 静态主画面文字包 v4

> **v4**：保留外貌与冠服史证，统一人物尺度、雷达/标题安全区，并修正事件归属与易漂移服制。
> 不在此生成图片。

## 硬规则

1. 叠字：本名在上，称号在下；代表事无 `《》`
2. 出图必须覆盖：脸、冠服、饰品、背景、势力画风——**禁止只喊人名**
3. 证据 A/B/C 上卡；C=重建

## 文件

| 文件 | 用途 |
|------|------|
| [`00-版式对照文豪图鉴.md`](00-版式对照文豪图鉴.md) | 构图 |
| [`01-二十人主画面总表.md`](01-二十人主画面总表.md) | 总表 |
| [`02-外貌史证索引.md`](02-外貌史证索引.md) | 外貌+冠服+背景速查 |
| [`cards/`](cards/) | 单人全卡 |
| [`prompts-en-only.txt`](prompts-en-only.txt) | 批跑 |
| [`overlay-zh.json`](overlay-zh.json) | 叠字+造型字段 |
| 数据源 | `tools/keyart_appearance_data.py` |

## 完成度

- 卡片：{len(overlay['cards'])} / 20
- 缺：{missing or '无'}
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")

    # update layout doc snippet
    layout = OUT / "00-版式对照文豪图鉴.md"
    if layout.exists():
        t = layout.read_text(encoding="utf-8")
        if "v2 外貌自足" not in t:
            t += """

---

## 7. v2 出图规则（外貌自足）

- 英文 prompt **必须**包含：年龄段、五官、须眉、体型、发型冠式、服色材质、姿态、场景光色、势力画风  
- **禁止**只写 `Emperor Qin Shi Huang standing...` 而不写鼻子眼睛  
- 史证等级见 `02-外貌史证索引.md` 与各 `cards/`  
- 数据：`tools/keyart_appearance_data.py`  
"""
            layout.write_text(t, encoding="utf-8")

    print("cards", len(overlay["cards"]), "missing", missing)


if __name__ == "__main__":
    main()
