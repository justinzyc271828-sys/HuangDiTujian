#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
组装 video-01 素材包（交付视频制作助手）：
- 插画 20 张：outputs/ 原图字节级复制（清晰度与原版一致）
- 雷达图 20 张：按 data/catalog/stand_stats.json 六维分数用 PIL 现绘（绫裱暗金风格）
- 配乐：Music/The Last Emperor's March.wav 复制
- 六维数据 JSON + 包内 README 索引

只写 video-01-素材包/，不动仓库其他任何文件；素材包为交付复制品，已入 .gitignore。
运行：python tools/build_video01_media_pack.py
"""
from __future__ import annotations

import json
import math
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "video-01-素材包"
OUT_SRC = ROOT / "assets" / "video-01" / "emperor-illustrations" / "outputs"
STAND = ROOT / "data" / "catalog" / "stand_stats.json"
VIDEO20 = ROOT / "data" / "catalog" / "video20.json"
MUSIC = ROOT / "Music" / "The Last Emperor's March.wav"

GOLD = (212, 175, 106)  # #d4af6a
GOLD_DIM = (176, 141, 74)
BG = (24, 18, 14)
PAPER = (244, 239, 228)
FONT_CANDIDATES = (
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simsun.ttf",
)


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for cand in FONT_CANDIDATES:
        if Path(cand).is_file():
            return ImageFont.truetype(cand, size)
    return ImageFont.load_default()


def render_radar(out: Path, display: str, stand_name: str, axes: list, scores: dict) -> None:
    size = 1200
    cx, cy, radius = 600, 665, 350
    n = len(axes)
    img = Image.new("RGB", (size, size), BG)
    d = ImageDraw.Draw(img, "RGBA")

    def pt(i: int, r: float) -> tuple[float, float]:
        a = -math.pi / 2 + 2 * math.pi * i / n
        return (cx + r * math.cos(a), cy + r * math.sin(a))

    for k in (0.2, 0.4, 0.6, 0.8, 1.0):
        d.polygon([pt(i, radius * k) for i in range(n)], outline=(*GOLD_DIM, 90))
    for i in range(n):
        d.line([(cx, cy), pt(i, radius)], fill=(*GOLD_DIM, 70), width=2)

    vals = []
    for i, ax in enumerate(axes):
        v = max(0, min(100, int(scores.get(ax["key"], 0))))
        vals.append(pt(i, radius * v / 100))
    d.polygon(vals, fill=(*GOLD_DIM, 78))
    for i in range(n):
        d.line([vals[i], vals[(i + 1) % n]], fill=(*GOLD, 255), width=4)
    for v in vals:
        d.ellipse([v[0] - 7, v[1] - 7, v[0] + 7, v[1] + 7], fill=(*GOLD, 255))

    f_label, f_score = load_font(44), load_font(38)
    for i, ax in enumerate(axes):
        lx, ly = pt(i, radius + 85)
        d.text((lx, ly - 26), ax["label"], font=f_label, fill=PAPER, anchor="mm")
        d.text((lx, ly + 24), str(scores.get(ax["key"], 0)), font=f_score, fill=GOLD, anchor="mm")

    f_title, f_sub, f_note = load_font(64), load_font(40), load_font(26)
    d.text((cx, 70), display, font=f_title, fill=PAPER, anchor="mm")
    d.text((cx, 140), stand_name, font=f_sub, fill=GOLD, anchor="mm")
    d.text((cx, size - 25), "文言六维品藻 · 非正式史评", font=f_note, fill=(*GOLD_DIM, 200), anchor="mm")

    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)


def main() -> None:
    stand = json.loads(STAND.read_text(encoding="utf-8"))
    v20 = json.loads(VIDEO20.read_text(encoding="utf-8"))
    axes = stand["axes"]
    profiles20 = v20["profiles"]

    illu_dir = PACK / "插画-高清20"
    radar_dir = PACK / "雷达图-20"
    music_dir = PACK / "配乐"
    data_dir = PACK / "六维数据"
    for d_ in (illu_dir, radar_dir, music_dir, data_dir):
        d_.mkdir(parents=True, exist_ok=True)

    copied = 0
    for png in sorted(OUT_SRC.glob("*.png")):
        shutil.copy2(png, illu_dir / png.name)
        copied += 1

    rendered = 0
    for idx, p in enumerate(profiles20, start=1):
        pid, display = p["id"], p["display"]
        prof = stand["profiles"].get(pid)
        if not prof:
            print(f"WARN: stand_stats 缺 {pid}，跳过")
            continue
        render_radar(
            radar_dir / f"{idx:02d}-{pid}-radar.png",
            display,
            prof["stand_name"],
            axes,
            prof["scores"],
        )
        rendered += 1

    shutil.copy2(MUSIC, music_dir / MUSIC.name)
    shutil.copy2(STAND, data_dir / STAND.name)
    shutil.copy2(VIDEO20, data_dir / VIDEO20.name)

    (PACK / "README.md").write_text(
        "# video-01 素材包（交付视频制作）\n\n"
        "生成：`python tools/build_video01_media_pack.py`（可随时重跑刷新）\n\n"
        "## 内容\n\n"
        "| 目录 | 内容 | 说明 |\n"
        "|------|------|------|\n"
        f"| `插画-高清20/` | 20 张皇帝插画 | outputs 原图**字节级复制**，清晰度与原版一致，16:9 岩彩裂壁风格 |\n"
        "| `雷达图-20/` | 20 张六维雷达图 PNG（1200×1200） | 按 `stand_stats.json` 分数现绘，绫裱暗金风格 |\n"
        "| `配乐/` | The Last Emperor's March.wav | 背景音乐原文件复制 |\n"
        "| `六维数据/` | stand_stats.json · video20.json | 六维分数/品名/口号源数据，做叠字动画用 |\n\n"
        "## 二十人顺序（文件名前缀编号）\n\n"
        + "\n".join(
            f"{i:02d}. {p['display']}（{p['id']}）" for i, p in enumerate(profiles20, start=1)
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"OK -> {PACK.relative_to(ROOT)}  插画 {copied} · 雷达图 {rendered} · 配乐 1 · 数据 2")


if __name__ == "__main__":
    main()
