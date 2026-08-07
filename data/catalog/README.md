# 帝王目录数据

| 文件 | 说明 | 状态 |
|------|------|------|
| `emperors_master.json` / `.yaml` | 全量索引 | **269** 人 |
| **`video20.json`** | 先导二十：四字号 + 文言六维 + 记忆点 | ✅ |
| `stand_stats.json` | 六维轴 + Lab 简表（对齐 video20） | ✅ |
| 可读总表 | `docs/references/catalogs/皇帝索引总表.md` | |
| 先导二十可读 | `docs/references/catalogs/先导二十人.md` | |
| **进度看板** | `docs/08-项目进度看板.md` | 以看板为准 |

重建全库索引：

```bash
python tools/build_emperors_master_index.py
```

`page_status`：`stub` 仅索引 · `draft` 已有人物 YAML · `ready` 可发布。

## 文言六维（video-01）

武功 · 文治 · 韬略 · 国祚 · **后效** · **月旦**

- 后效：客观遗产  
- 月旦：褒贬（**不是**知名度）  

## 关联产出

| 产出 | 路径 |
|------|------|
| 分镜 | `content/video/video-01/分镜/` |
| 英文出图 | `key-art-en-prompts-video01/` |
| 史料 | `content/sources/` |
