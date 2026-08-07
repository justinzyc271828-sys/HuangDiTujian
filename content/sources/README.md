# 史源 / 史料工作区

规范：docs/05-史源卡工作规范.md  
看板：docs/08-项目进度看板.md

## 状态总览（本纪升格进行中）

| status | 人数 | 含义 |
|--------|------|------|
| dossier-complete | 47 | 本纪精读级具体史实卡 |
| dossier-scaffold | 222 | 全库结构脚手架，待升格 |
| **合计** | **269** | 与 master 269 对齐 |
| **E 卡** | **3008** | |

### 本纪精读已完成批次

- video-01 二十人 + 高祖 + 二世（先导样板）
- **西汉余部 + 东汉全朝**（	ools/upgrade_benji_dossiers.py，batch: benji-upgrade）

### 脚本

`ash
python tools/upgrade_benji_dossiers.py              # 两汉升格
python tools/upgrade_benji_dossiers.py --only han-wen-di
python tools/seed_master_all_sources.py             # 仅补缺目录
`
