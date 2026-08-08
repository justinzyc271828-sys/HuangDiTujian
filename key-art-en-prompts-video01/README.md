# English Image Prompts — video-01 (20 emperors)

> **⚠ 已废止（2026-08-08 标注）：** 本套为旧版存档，**勿再用于出图**。  
> 现行生产包：`assets/video-01/emperor-illustrations/`（prompt **v2.3** + `manifest.json`），真图 6/20 已出于 `outputs/`。

Prompts are **English-only** for your image model.
Chinese fields in each `.txt` are metadata for later overlay only.

## Fixed paths in this repo

- `content/video/video-01/key-art/en-prompts/`
- `key-art-en-prompts-video01/`  ← workspace-root shortcut

## How to use

1. Open `01-….txt` … `20-….txt`
2. Copy the **POSITIVE** block into Image
3. Paste **NEGATIVE** if supported
4. Aspect **16:9**
5. After generation, overlay Chinese name (personal first) + radar from `overlay-zh.json`

## Combined files

- `ALL-20-PROMPTS.md`
- `ALL-20-PROMPTS.txt`

## Index

| # | id | name | file |
|---|-----|------|------|
| 1 | `qin-shi-huang` | 嬴政 | `01-qin-shi-huang.txt` |
| 2 | `han-xuan-di` | 刘询 | `02-han-xuan-di.txt` |
| 3 | `han-wu-di` | 刘彻 | `03-han-wu-di.txt` |
| 4 | `xin-wang-mang` | 王莽 | `04-xin-wang-mang.txt` |
| 5 | `e-han-guangwu` | 刘秀 | `05-e-han-guangwu.txt` |
| 6 | `h-zhao-shi-le` | 石勒 | `06-h-zhao-shi-le.txt` |
| 7 | `liang-wu` | 萧衍 | `07-liang-wu.txt` |
| 8 | `xixia-li-yuanhao` | 李元昊 | `08-xixia-li-yuanhao.txt` |
| 9 | `q-qin-fu-jian` | 苻坚 | `09-q-qin-fu-jian.txt` |
| 10 | `n-wei-xiaowen` | 元宏 | `10-n-wei-xiaowen.txt` |
| 11 | `sui-wen` | 杨坚 | `11-sui-wen.txt` |
| 12 | `sui-yang` | 杨广 | `12-sui-yang.txt` |
| 13 | `tang-tai-zong` | 李世民 | `13-tang-tai-zong.txt` |
| 14 | `zhou-wu-zetian` | 武曌 | `14-zhou-wu-zetian.txt` |
| 15 | `tang-xian-zong` | 李纯 | `15-tang-xian-zong.txt` |
| 16 | `zhou-shi` | 柴荣 | `16-zhou-shi.txt` |
| 17 | `n-tang-houzhu` | 李煜 | `17-n-tang-houzhu.txt` |
| 18 | `n-song-tai-zu` | 赵匡胤 | `18-n-song-tai-zu.txt` |
| 19 | `yuan-shi-zu` | 忽必烈 | `19-yuan-shi-zu.txt` |
| 20 | `n-wei-taiwu` | 拓跋焘 | `20-n-wei-taiwu.txt` |

Rebuild export: `python tools/export_keyart_en_prompts.py`
