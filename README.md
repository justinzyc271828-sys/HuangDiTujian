# 皇帝图鉴 · HuangDiTujian

把中国历史上的**正式帝王**与后期扩展的**准帝王**，做成一本可交互的「收集图鉴」：

- AI 史书想象画像（先导二十：英文 prompt 已备）  
- 主要事迹 + 年表大事表 + 关联表  
- `[[其他皇帝]]` 交叉跳转  
- 侧栏古地图：一生主要地点与路线  
- **video-01**：文言六维 + 分镜 + Key Art  

> **进度以看板为准（与仓库事实同步）：**  
> → [`docs/08-项目进度看板.md`](docs/08-项目进度看板.md)  
> **工作区边界：** 仅本仓库；见 [docs/06-工作区边界.md](docs/06-工作区边界.md)。

### 当前快照（2026-08-06）

| 项 | 状态 |
|----|------|
| 全库索引 | **269** 人 · `data/catalog/emperors_master.*` |
| video-01 | **20** 人六维/分镜/史料先导/英文 prompt ✅ · 真图/成片 ☐ |
| 产品 YAML+bio | **5** 人（含始皇、汉武、太宗） |
| 史料卡 | **3** 人 dossier-complete（各 12 条）· **17** 人 in-progress（各 5–8 条） |
| 前端 | `apps/web` 可 dev · **奏折专页未落地**（见 07 / FRONTEND-SLOT） |
| 英文出图固定目录 | `key-art-en-prompts-video01/` |

---

## 产品一句话

**可跳转、可地图化的中国帝王人物图鉴 Web 应用**；数据与素材全部版本化在本仓库。  
先导产线同时服务 **短视频图鉴卡**（文豪图鉴式 Key Art + 六维）。

详细框架见：[docs/00-总框架.md](docs/00-总框架.md)

---

## 仓库结构（现行）

```
HuangDiTujian/
├── README.md
├── docs/                         # 00–08 框架与进度看板
├── data/
│   ├── catalog/                  # master 269 · video20 · stand_stats
│   ├── emperors/                 # 产品 YAML（现 5）
│   ├── places/                   # 地点（现 15）
│   └── templates/
├── content/
│   ├── bios/                     # 现 5
│   ├── sources/                  # video-01 二十人史源/史料
│   └── video/video-01/           # 分镜 · key-art 规格
├── key-art-en-prompts-video01/   # ★ 英文出图 prompt 固定目录（20）
├── assets/portraits/             # 画像（待生成）
├── HuangDiTujian-Ref/            # 二十四史/通鉴等参考全文
├── tools/                        # 构建与导出脚本
└── apps/web/                     # Vite+React 预览
```

---

## 已有产品层示例

| id | 显示名 | 说明 |
|----|--------|------|
| `qin-shi-huang` | 秦始皇 | YAML+bio+12 史料+分镜+prompt |
| `han-wu-di` | 汉武帝 | 同上 |
| `tang-tai-zong` | 唐太宗 | 同上 |
| `han-gao-zu` | 汉高祖 | 早期骨架 YAML（不在 video20） |
| `qin-er-shi` | 秦二世 | 早期骨架 YAML（不在 video20） |

video-01 其余 17 人：**有史料/分镜/prompt，尚无 `data/emperors` YAML**。

---

## 文档导航

| 文档 | 内容 |
|------|------|
| **[进度看板](docs/08-项目进度看板.md)** | **与仓库对齐的唯一进度总表** |
| [总框架](docs/00-总框架.md) | 定位、交付物、架构 |
| [数据模型](docs/01-数据模型.md) | YAML 字段、链接、校验 |
| [素材规范](docs/02-素材与生产规范.md) | 文风、画像、地图 |
| [路线图](docs/03-路线图与任务拆分.md) | M0–M5 |
| [参考库指南](docs/04-参考库建设指南.md) | 史书/地图/参考库 |
| [史源卡规范](docs/05-史源卡工作规范.md) | 史源/史料状态机 |
| [工作区边界](docs/06-工作区边界.md) | 仅本仓库可写 |
| [奏折布局](docs/07-专页奏折布局设计.md) | 正式 UI |
| [FRONTEND-SLOT](docs/FRONTEND-SLOT.md) | 前端实现槽 |
| [先导二十人](docs/references/catalogs/先导二十人.md) | 六维总表 |
| [史源工作区](content/sources/README.md) | 二十人史料状态 |
| [视频包](content/video/video-01/README.md) | 分镜 + Key Art |
| [英文 prompt](key-art-en-prompts-video01/README.md) | Image 用 |

---

## 贡献一条人物（产品层）

1. 先写/扩 `content/sources/{id}/` 史料卡  
2. 复制 `data/templates/emperor.template.yaml` → `data/emperors/{id}.yaml`  
3. 写 `content/bios/{id}.md`  
4. 补 `data/places/`  
5. 画像：用 `key-art-en-prompts-video01/` 或 `tools/prompts/portrait-v1.md`  
6. `python tools/build_site_data.py` 后本地预览  

---

## 本地运行预览

```bash
python tools/build_site_data.py
cd apps/web
npm install
npm run dev
```

常用导出：

```bash
python tools/export_keyart_en_prompts.py   # 英文出图 20 份
python tools/build_video20_keyart_prompts.py
python tools/build_emperors_master_index.py
```
