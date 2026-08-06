# 前端实现槽位

**正式专页视觉与奏折交互：预留给后续前端/设计实现。**

请直接阅读并按此落地：

→ [`docs/07-专页奏折布局设计.md`](./07-专页奏折布局设计.md)

## 当前仓库已提供（可对接）

| 能力 | 位置 |
|------|------|
| 人物 YAML / 年表 / 路线 | `data/emperors/` |
| 全库索引 | `data/catalog/emperors_master.json` |
| 六维分数（三人演示） | `data/catalog/stand_stats.json` |
| 构建产物 | `apps/web/public/data/site.json` |
| 史料卡 | `content/sources/` |

## 不要做

- 把 `/lab` 多皮肤实验当正式交付  
- 在未按 07 文档的情况下继续堆「又一套风格」  

## 建议技术入口

现有 `apps/web` 可继续用，但 **Emperor 专页应按 Memorial 三栏重写**；或新开 UI 包，只消费 `site.json`。
