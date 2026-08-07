# 史源 / 史料工作区

规范：`docs/05-史源卡工作规范.md`  
**进度看板：** `docs/08-项目进度看板.md`

## 状态总览（2026-08-06 实测）

| id | 人物 | status | 史料卡约数 | 备注 |
|----|------|--------|------------|------|
| qin-shi-huang | 秦始皇 | **dossier-complete** | 12 | 史记 |
| han-wu-di | 汉武帝 | **dossier-complete** | 12 | 汉书 |
| tang-tai-zong | 唐太宗 | **dossier-complete** | 12 | 两唐书 |
| han-xuan-di | 汉宣帝 | in-progress | 8 | video-01 |
| xin-wang-mang | 新帝王莽 | in-progress | 7 | video-01 |
| e-han-guangwu | 汉光武帝 | in-progress | 7 | video-01 |
| h-zhao-shi-le | 后赵石勒 | in-progress | 7 | video-01 |
| liang-wu | 梁武帝 | in-progress | 6 | video-01 |
| xixia-li-yuanhao | 西夏景宗 | in-progress | 6 | video-01 |
| q-qin-fu-jian | 前秦世祖 | in-progress | 7 | video-01 |
| n-wei-xiaowen | 北魏孝文帝 | in-progress | 6 | video-01 |
| sui-wen | 隋文帝 | in-progress | 5 | video-01 |
| sui-yang | 隋炀帝 | in-progress | 6 | video-01 |
| zhou-wu-zetian | 武则天 | in-progress | 6 | video-01 |
| tang-xian-zong | 唐宪宗 | in-progress | 5 | video-01 |
| zhou-shi | 后周世宗 | in-progress | 6 | video-01 |
| n-tang-houzhu | 南唐后主 | in-progress | 6 | video-01 |
| n-song-tai-zu | 宋太祖 | in-progress | 5 | video-01 |
| yuan-shi-zu | 元世祖 | in-progress | 6 | video-01 |
| n-wei-taiwu | 北魏太武帝 | in-progress | 7 | video-01 |

**合计：** 20 目录 · 约 **142** 条 E 卡（含三人 36 条 complete）

## 关联产线

| 产线 | 路径 | 状态 |
|------|------|------|
| 六维 | `data/catalog/video20.json` | ✅ |
| 分镜 | `content/video/video-01/分镜/` | ✅ 20 |
| Key Art 规格 | `content/video/video-01/key-art/cards/` | ✅ 20 |
| 英文 prompt | `key-art-en-prompts-video01/` | ✅ 20 |
| 产品 YAML | `data/emperors/` | 仅 3/20 在 video 交集内写满 |

## 写卡时打开

1. `HuangDiTujian-Ref/11-史料卡工作台/{id}.md`  
2. 简体史书 md + `tools/search_ref.py`  
3. 本目录 `证据/` 落卡  

```bash
python tools/search_ref.py "始皇帝" --book 史记
python tools/build_ref_indexes.py
```

全量索引：`data/catalog/emperors_master.json`（269）
