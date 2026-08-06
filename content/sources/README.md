# 史源 / 史料工作区

规范：`docs/05-史源卡工作规范.md`  
**参考库入口（已整理）：** `HuangDiTujian-Ref/11-史料卡工作台/README.md`

## 状态总览

| id | 人物 | status | 史料卡 | 主文本 |
|----|------|--------|--------|--------|
| qin-shi-huang | 秦始皇 | dossier-complete | 12 条 | 史记·卷006 |
| han-wu-di | 汉武帝 | dossier-complete | 12 条 | 汉书·卷006 |
| tang-tai-zong | 唐太宗 | dossier-complete | 12 条 | 旧唐·卷2 |

全量皇帝索引：`docs/references/catalogs/皇帝索引总表.md` · `data/catalog/emperors_master.json`

## 写卡时打开

1. `HuangDiTujian-Ref/11-史料卡工作台/{id}.md` — 锚点  
2. 对应简体史书 md  
3. 本目录 `证据/` 落卡  

检索：

```bash
python tools/search_ref.py "始皇帝" --book 史记
python tools/build_ref_indexes.py   # 重建卷目录
```

## 目录

```
_templates/
qin-shi-huang/  han-wu-di/  tang-tai-zong/
  00–06 …  证据/  摘录/
```
