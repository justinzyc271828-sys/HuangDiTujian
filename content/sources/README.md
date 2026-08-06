# 史源 / 史料工作区

规范：`docs/05-史源卡工作规范.md`  
**参考库入口（已整理）：** `HuangDiTujian-Ref/11-史料卡工作台/README.md`

## 状态总览

| id | 人物 | status | 主文本（简体 md） |
|----|------|--------|-------------------|
| qin-shi-huang | 秦始皇 | ready-to-fill | 史记·卷006·始皇帝 |
| han-wu-di | 汉武帝 | ready-to-fill | 汉书·卷006·武帝 |
| tang-tai-zong | 唐太宗 | ready-to-fill | 旧唐·卷2·太宗上 |

`ready-to-fill` = 脚手架齐，**证据卡正文未填**。

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
