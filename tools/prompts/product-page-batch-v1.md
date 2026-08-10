# 页面升格批量生产提示词 v1（把 stub 皇帝升格为 video-01 二十人标准）

> 用途：Justin 把下面整段喂给批量助手，将 `data/catalog` 里的灰卡 stub 升格为「22 人标准」的完整产品页数据。
> 与 `evidence-card-batch-v1.md` 的关系：那个管史料层（content/sources/），这个管产品层。史料层 269 人已全部 dossier-complete，本任务直接吃它的产出。
> 使用时只需替换开头的【人物清单】。

---

# 任务：把灰卡 stub 升格为「video-01 二十人标准」完整页面数据

你在仓库 `D:/Workspaces/Github/HuangDiTujian` 中工作。终态目标：库内 269 位帝王的页面全部达到 video-01 二十人（如秦始皇、汉武帝）的成品水准。你的职责是**为清单中的每位皇帝补齐产品层数据**，原料就是该人物已完成、无需重做的史料档案。

【人物清单】：（由 Justin 填写 id 列表，每批建议 ≤10 人）

## 工作边界（先于一切）

- **只许写这四个位置**：`data/emperors/`、`content/bios/`（含 `en/`）、`data/catalog/stand_stats.json`、`data/places/`。
- **不许碰**：`apps/`（前端）、`content/sources/`（史料层，发现错误只在报告里指出）、`tools/`、`docs/`；不许 `git commit` / `git push`。
- **不做画像/插画**：`portrait` 块只写声明字段，图片文件是另一条产线，缺图页面会自动显示「画像待补」，不算缺陷。

## 第 0 步：先读标准样例（必做）

成品标准 = 下面这组文件，格式、字段、颗粒度全部照抄：

- 产品档：`data/emperors/qin-shi-huang.yaml`（273 行，逐字段读）
- 中文 bio：`content/bios/qin-shi-huang.md`（3 段叙事 + `[[id|显示名]]` 跨页链接）
- 英文 bio：`content/bios/en/qin-shi-huang.md`
- 品藻档：`data/catalog/stand_stats.json` 里 `qin-shi-huang` 那条
- 地点档：`data/places/xianyang.yaml`

再读该人物的原料：`content/sources/{id}/00-史源卡.md` + `证据/` 全部 E 卡。

## 每位皇帝的产出清单（6 件，一件不能少）

### 1. `data/emperors/{id}.yaml` —— 产品档主文件

照 `qin-shi-huang.yaml` 的字段结构写全：`names`（含 `display_en`/`personal_en`）、`dynasty`、`reign`、`life`（birth/death + 对应 place_id）、`summary`（≤40 字，一句话定性）+ `summary_en`、`tags`（4 个左右四字词）+ `tags_en`、`portrait` 声明块、`bio.file`、`timeline`、`relations`、`routes`、`sources`、`meta`。

- **timeline**：从该人物 E 卡里 `enter_product: true` 的条目转化，**≥10 条**（在位极短者 ≥6）。每条必须有：`year`、`date_note` + `date_note_en`、`title`（≤12 字）+ `title_en`、`summary`（1–2 句）+ `summary_en`、`place_id`、`sources`（书+篇卷）、`card_id`（回链 E 卡号，如 E005）。按公历年升序。
- **routes**：从 timeline 里 `on_map=yes` 的条目提取，`group` 取值限：都城/巡狩/亲征/起兵/入关/迁都/流徙/其他。
- **relations**：前后任 + 权臣/对手/跨朝对照，`target_id` 必须是 `data/catalog/emperors_master.yaml` 里存在的 id；类型限 predecessor/successor/kinship/minister/rival/related_emperor/other。
- **meta**：`status: draft`、`synced_from_cards: true`、`last_reviewed` 填当天、`inclusion_reason` 一句话。
- 英文值不确定就译保守直译，不许留空、不许写 "TODO"。

### 2. `content/bios/{id}.md` —— 中文 bio

3–5 段叙事散文（不是年表复读）：开局定身份与格局，中段展开功过张力，末段接到前后任/跨朝对读。`[[目标id|显示名]]` 链接的目标必须是库内 id。末行保留参考注记格式。

### 3. `content/bios/en/{id}.md` —— 英文 bio

中文 bio 的完整英译（不是缩写），`[[id|English Name]]` 链接格式保留。

### 4. `data/catalog/stand_stats.json` —— 品藻档（追加一条）

照 `qin-shi-huang` 条目：`stand_name`（【四字】品名）、`stand_type`、`cry`（一句判词）、`scores` 六维（wugong 武功/wenzhi 文治/taolue 韬略/guozuo 国祚/houxiao 后效/yuedan 月旦，0–100）、`ability`（**两个四字词，分号隔开**）、`weakness`（同体例两个四字词），以及 `stand_name_en`/`stand_type_en`/`cry_en`/`ability_en`/`weakness_en`。

- 评分必须有史实依据（从 E 卡读出来），国祚指政权延续长度、后效指制度/历史影响，不许拍脑袋打高分。
- ability/weakness 的「双四字对仗」体例是已定稿的硬标准（例：「混一六合；郡县立制」/「严刑峻法；二世而亡」），不许写成长句。

### 5. `data/places/` —— 缺什么补什么

timeline/routes 用到的古地名若 `data/places/` 没有对应 id，新建 `{小写kebab}.yaml`，照 `xianyang.yaml` 结构：`names.historical/modern/english`、`coords.lng/lat`（据谭其骧图册/CHGIS 给近似值）、`precision: approximate`（无把握写 `schematic`）、`map.region`、`notes`。

### 6. 索引不用动

`emperors_master` 的 `page_status` 由构建脚本根据 yaml 是否存在自动翻转，不要手改。

## 自检（全部通过才算完成）

1. 仓库根运行 `python tools/validate_data.py` —— 无新增 ERROR（Windows 先 `set PYTHONIOENCODING=utf-8`）。
2. `python tools/build_site_data.py` 跑通。
3. 逐人核对：timeline 条数达标、card_id 与 E 卡对得上、place_id 全部存在、EN 字段无空缺、品藻双四字体例。

## 节奏（每批必走）

1. **先报计划**：每人在位期、E 卡可用条数、预计 timeline 条数、需新建哪些 place、存疑点。等确认再写盘。
2. **写盘**：一人六件写完再换下一人。
3. **自检 + 交付报告**：每人一段 —— id、timeline 条数、新建 place 列表、品藻六维分值及一句依据、需要人工定夺的事。

先做计划，不要上来就写文件。
