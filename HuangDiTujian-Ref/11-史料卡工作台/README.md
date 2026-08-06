# 史料卡工作台

把「参考库」接到「写卡」：这里不堆原文，只放**路径、检索锚点、推荐顺序**。

## 写卡默认语料（优先简体）

| 用途 | 路径（相对本参考库根） |
|------|------------------------|
| 正史正文 | `01-史书全文与扫描/二十四史-简体/` |
| 编年 | `01-史书全文与扫描/资治通鉴-简体/01-资治通鉴.md` |
| 经部辅证 | `01-史书全文与扫描/十三经-简体/`（一般后用） |
| 卷目索引 | `10-索引/` |
| 地图 GIS | `03-地图与GIS/CHGIS/` |
| 繁体对照 | 同名目录去掉「-简体」 |

产品侧卡片目录（Git 跟踪）：

```text
content/sources/{id}/
  00-史源卡.md
  证据/E001-….md    ← 史料卡落点
  摘录/              ← 超长自用摘句
```

规范：`docs/05-史源卡工作规范.md`

## 标准动作（一条史料卡）

1. 在简体 md 中搜索锚点（见下方三人页）  
2. 读上下文，确定年 / 事 / 地  
3. 复制 `content/sources/_templates/史料卡.template.md` → `证据/E00x-标题.md`  
4. `sources` 写清：书名·卷·小节（维基文库简体 md）  
5. 可选：通鉴同日/同年对一下  
6. 要上地图：在 `03-地点候选表` 补点  

## 三人入口

| 人物 | 工作台页 | 产品 sources |
|------|----------|--------------|
| 秦始皇 | [qin-shi-huang.md](./qin-shi-huang.md) | `content/sources/qin-shi-huang/` |
| 汉武帝 | [han-wu-di.md](./han-wu-di.md) | `content/sources/han-wu-di/` |
| 唐太宗 | [tang-tai-zong.md](./tang-tai-zong.md) | `content/sources/tang-tai-zong/` |

## 重建索引

语料增删后，在仓库根执行：

```bash
python tools/build_ref_indexes.py
```

快速检索：

```bash
python tools/search_ref.py "始皇帝" --book 史记
python tools/search_ref.py "建元元年" --book 汉书
python tools/search_ref.py "玄武门" --book 旧唐书
```
