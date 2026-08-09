# 史源 / 史料工作区

规范：`docs/05-史源卡工作规范.md` · 看板：`docs/08-项目进度看板.md`

## 状态（2026-08-08）

| status | 人数 | 含义 |
|--------|------|------|
| **dossier-complete** | **269** | 本纪精读级具体史实（实测 `00-史源卡.md` 全员） |
| dossier-scaffold | **0** | 已清空 |
| **合计** | **269** | 与 master 对齐；E 卡实测 1950 张 |

### 本纪精读已完成范围

| 批次 | 内容 |
|------|------|
| 样板 | video-01 二十 + 高祖 + 二世 |
| 两汉 | 西汉余部 + 东汉全朝（含 QA 复核） |
| 三国两晋 | 曹魏 5 · 蜀 2 · 吴 4 · 西晋 4 · 东晋 11 |
| **收官** | 十六国 / 南北朝 / 隋唐 / 五代十国 / 宋辽金西夏 / 元明清全员升格（120 名场面交叉核验 0 issue） |

### 脚本

```bash
python tools/upgrade_benji_3k_jin.py      # 三国两晋
python tools/upgrade_benji_dossiers.py    # 两汉
python tools/qa_benji_han_rewrite.py      # 两汉 QA
```

### 审计笔记

- `docs/references/notes/史料卡质量审计-两汉.md`
- `docs/references/notes/史料卡质量审计-三国两晋.md`
