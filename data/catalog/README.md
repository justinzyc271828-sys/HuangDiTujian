# 帝王目录数据

| 文件 | 说明 |
|------|------|
| `emperors_master.json` | 全量索引（程序生成，约 268 人） |
| `emperors_master.yaml` | 同上 YAML |
| **`video20.json`** | **先导二十人：四字号 + 文言六维 + 记忆点** |
| `stand_stats.json` | 六维轴定义 + 部分人 Lab 用简表（与 video20 对齐） |
| 可读总表 | `docs/references/catalogs/皇帝索引总表.md` |
| 先导二十可读 | `docs/references/catalogs/先导二十人.md` |

重建全库索引：

```bash
python tools/build_emperors_master_index.py
```

`page_status`：`stub` 仅索引 · `draft` 已有人物 YAML · `ready` 可发布。

## 文言六维（video-01）

武功 · 文治 · 韬略 · 国祚 · **后效** · **月旦**

- 后效：客观遗产  
- 月旦：褒贬（**不是**知名度）  
