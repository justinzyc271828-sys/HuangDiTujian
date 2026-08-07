# 史源 / 史料工作区

规范：`docs/05-史源卡工作规范.md`  
看板：`docs/08-项目进度看板.md`

## 状态总览（master 全量批量后）

| status | 人数 |
|--------|------|
| dossier-complete | 22 |
| dossier-scaffold | 247 |

| **合计目录** | **269** |
| **E 卡合计** | **3020** |

### 说明

- `dossier-complete`：先导样板（video-01 等），可支撑产品精写  
- `dossier-scaffold`：**master 全量脚手架**——结构齐、出处锚定本纪入口，摘要待精读升格  
- 生成脚本：`tools/seed_master_all_sources.py`  

### 升格命令提示

```bash
python tools/search_ref.py "帝号或姓名" --book 史记
```
