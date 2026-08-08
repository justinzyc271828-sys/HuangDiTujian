# video-01 帝王插画固定生产包

当前版本：`v2.3 camera-palette-identity-physics`。旧版提示词已经废止，不得从聊天缓存或旧复制文本继续生成。先读 `MASTER-VISUAL-GRAMMAR.md`、`CAMERA-MATRIX.md` 和 `PALETTE-MATRIX.md`，再按 `prompts/` 的编号逐张生成。

## 唯一输出目录

```text
D:\Workspaces\Github\HuangDiTujian\assets\video-01\emperor-illustrations\outputs
```

所有最终 PNG 必须直接保存在这个文件夹，不得另建日期目录、临时成品目录或放回工具默认目录。

## 生产顺序

1. `01-qin-shi-huang.png` 至 `06-h-zhao-shi-le.png` 已批准，**禁止重生成或覆盖**。
2. 从 `prompts/07-liang-wu.txt` 开始，一次只处理一张；旧版退稿保存在 `rejected/` 的对应原因目录中。
3. 每次必须重新打开单人提示词，确认顶部是 `PROMPT_VERSION: 2.3-camera-palette-identity-physics`，再复制 `POSITIVE PROMPT`。
4. 同时加载主锚点和辅助锚点；只继承材质、笔触和成年漫画造型，不复制秦始皇机位或黑金密度。
5. 生成前同时核对 `SHOT_CODE`、`COLOR_CODE` 及两张矩阵的相邻行；生成 16:9 PNG。
6. 按十三项硬验收检查；若回到正面低机位伸手构图、统一金粉层，或器物不服从重力与单一透视，直接判退。
7. 通过后按 `OUTPUT_PATH` 精确保存，再进入下一人。

## 文件命名

固定格式：`NN-id.png`，例如：

- `01-qin-shi-huang.png`
- `02-han-xuan-di.png`
- `17-n-tang-houzhu.png`

不得在正式输出中使用 `final-final`、日期、随机串或中文文件名。

## 边界

- 统一的是岩彩、裂壁、墨势和成年漫画造型，不是秦始皇的道具、构图或黑金比例。
- 不生成名字、代表事、雷达图或任何 UI；全部后期叠加。
- 不覆盖已有文件。若某编号已存在，先停止并报告。
- 不修改 `prompts/`、Style Bible、史料文件或网页数据。
