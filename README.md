# 皇帝图鉴 · HuangDiTujian

把中国历史上的**正式帝王**与后期扩展的**准帝王**，做成一本可交互的「收集图鉴」：

- AI 史书想象画像  
- 主要事迹 + 年表大事表 + 关联表  
- `[[其他皇帝]]` 交叉跳转  
- 侧栏古地图：一生主要地点与路线  

> 当前阶段：**M0 立项搭架完成** → 下一步 **M1 垂直切片（可点可跳可看地图）**  
> **工作区边界：** 所有建改文件仅限本仓库目录；见 [docs/06-工作区边界.md](docs/06-工作区边界.md)。

---

## 产品一句话

**可跳转、可地图化的中国帝王人物图鉴 Web 应用**；数据与素材全部版本化在本仓库。

详细框架见：[docs/00-总框架.md](docs/00-总框架.md)

---

## 仓库结构

```
HuangDiTujian/
├── README.md
├── docs/                      # 项目文档
│   ├── 00-总框架.md
│   ├── 01-数据模型.md
│   ├── 02-素材与生产规范.md
│   ├── 03-路线图与任务拆分.md
│   └── references/            # UI 参考截图（请本地补充）
├── data/
│   ├── dynasties.yaml         # 王朝元数据
│   ├── emperors/              # 一人一 YAML
│   ├── places/                # 地点库
│   └── templates/             # 空白模板
├── content/bios/              # 主要事迹长文 Markdown
├── assets/
│   ├── portraits/             # 画像
│   ├── maps/                  # 古地图底图
│   └── style-bible/           # 画像风格锚点
├── tools/prompts/             # AI 出图模板
└── apps/web/                  # 前端（M1 初始化）
```

---

## 已有示例数据（骨架）

| id | 显示名 | 作用 |
|----|--------|------|
| `qin-shi-huang` | 秦始皇 | 完整字段示范 + 巡狩路线 |
| `qin-er-shi` | 秦二世 | 短祚 + 继承关系 |
| `han-gao-zu` | 汉高祖 | 跨朝跳转 + 起兵路线 |

交叉引用示例写在 `content/bios/*.md` 里。

---

## 文档导航

| 文档 | 内容 |
|------|------|
| [总框架](docs/00-总框架.md) | 定位、交付物、架构、素材清单、里程碑 |
| [数据模型](docs/01-数据模型.md) | YAML 字段、链接语法、校验规则 |
| [素材规范](docs/02-素材与生产规范.md) | 文风、画像、地图、质量门禁 |
| [路线图](docs/03-路线图与任务拆分.md) | M0–M5 任务与首批名单建议 |
| [参考库建设指南](docs/04-参考库建设指南.md) | 史书/地图/年表去哪找、如何建本地参考库 |
| [史源卡工作规范](docs/05-史源卡工作规范.md) | 史源卡/史料卡级别、状态机、门禁 |
| [权威资源总表](docs/references/catalogs/权威资源总表.md) | 收藏级链接与书目 |
| [材料就绪检查清单](docs/references/checklists/材料就绪检查清单.md) | **你决定是否开填三卡的决策页** |
| [所需书籍清单](docs/references/checklists/所需书籍与资料清单.md) | 已得 / 未得书目 |
| [工作区边界](docs/06-工作区边界.md) | **仅本仓库可写** |
| [史源工作区](content/sources/README.md) | 三人 ready-to-fill 脚手架 |
| [本地参考包](reference/README.md) | 大体量资料放仓库内 `reference/` |

---

## 你怎么开始贡献一条人物

1. 复制 `data/templates/emperor.template.yaml` → `data/emperors/{id}.yaml`  
2. 写 `content/bios/{id}.md`（可用 `[[other-id|显示名]]` 链接其他皇帝）  
3. 补地点：`data/places/`  
4. 按 `tools/prompts/portrait-v1.md` 出图 → `assets/portraits/{id}/primary.png`  
5. 等 Web 壳就绪后本地预览  

---

## 本地运行 MVP（闭环）

```bash
python tools/build_site_data.py
cd apps/web
npm install
npm run dev
```

打开终端提示的地址（默认 http://127.0.0.1:5173 ）。

闭环：图鉴总览 → 秦始皇 / 汉武帝 / 唐太宗人物卡 → `[[链接]]` 跳转 → 侧栏示意地图 → 本地已读/收藏。

参考库（写史料卡）：`HuangDiTujian-Ref/11-史料卡工作台/README.md`  
卷目录索引：`HuangDiTujian-Ref/10-索引/` · 总览：`HuangDiTujian-Ref/INDEX.md`  
**皇帝索引总表（全库人数）：** [`docs/references/catalogs/皇帝索引总表.md`](docs/references/catalogs/皇帝索引总表.md)  
（二十四史/通鉴等大体量 md 默认不提交 Git；索引与工作台可提交）

## 路线图（极简）

1. **M0** 框架与数据模板 ✅  
2. **M1** Web MVP 闭环 ✅（本版最简）  
3. **M2** 史源卡精修 + 秦→清抽样  
4. **M3** 正式帝王批量  
5. **M4** 视觉与移动端打磨  
6. **M5** 准帝王扩展包  

---

## 许可与声明（草案）

- 史事叙述以公开古籍与通行史学共识为骨架，欢迎纠错。  
- AI 画像均为**艺术想象**，不作相貌复原证明。  
- 开源许可证待你选定后写入本文件。  
