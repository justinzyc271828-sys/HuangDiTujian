# 帝王目录数据

| 文件 | 说明 |
|------|------|
| `emperors_master.json` | 全量索引（程序生成） |
| `emperors_master.yaml` | 同上 YAML |
| 可读总表 | `docs/references/catalogs/皇帝索引总表.md` |

重建：

```bash
python tools/build_emperors_master_index.py
```

`page_status`：`stub` 仅索引 · `draft` 已有人物 YAML · `ready` 可发布。
