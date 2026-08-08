# 帝王插画统一母风格 v1

## 定位与锚点

风格名：**岩彩裂壁 · 墨势入场**。它不是静态帝王图鉴，而是把成年历史漫画人物、矿物岩彩和泼墨动势结合成一帧正在发生的历史事件。

- 主锚点：`approved/01-qin-shi-huang-final-v1.png`
- 辅助锚点：`references/emperor-series-ink-motion-v1.png`
- 主锚点决定整体完成度；辅助锚点只补充墨势、飞白和动作流向。

## 固定视觉语法

1. **人物主导**：16:9；人物占画面视觉质量的 55%–70%，采用中近景或大半身。脸、手、冠服剪影必须先于背景被看到。
2. **人物在做事**：选择该帝王独有的成就、危机、作品或转折。事件必须由人物动作触发，不能只放在身后当说明图。
3. **观众在现场**：明确观众站位，并让一只手、宽袖、兵器或关键道具朝镜头运动。定格在动作尚未完成的一瞬。
4. **岩彩骨架**：旧壁、粗纸、矿物颗粒、石青、石绿、朱砂、赭石、墨黑和旧金；允许剥落、裂纹、金箔碎屑及不均匀覆盖。
5. **墨势驱动**：焦墨、飞白、干刷与泼墨负责连接人物、事件和前景冲击，不作为无意义装饰。
6. **成年漫画造型**：五官有明确线面和情绪，适度夸张透视；禁止真人皮肤、摄影光影、光滑 3D 和常见平滑 AI 国漫质感。

## 每位帝王必须重新设计的变量

- `signature_moment`：只属于此人的代表瞬间。
- `viewer_position`：观众在事件空间中的位置。
- `action_to_camera`：朝镜头发生的动作或冲击物。
- `identity_props`：最多三件具有史实依据的独有道具。
- `event_layers`：两到四层参与叙事的环境信息。
- `accent_palette`：除墨黑、旧纸和旧金外的一至三种人物专属色。
- `motion_material`：裂壁、墨浪、烟尘、风雪、火光、水势等与事件相符的运动介质。

不得把秦始皇的帝印、六国地图、权量和车辙复制给其他人物；统一的是视觉语法，不是道具模板。

## 通用生成提示词骨架

```text
Use case: historical-scene
Asset type: 16:9 key art for an emperor montage video

Create [EMPEROR] at the unfinished instant of [SIGNATURE_MOMENT].
The viewer stands at [VIEWER_POSITION]. [ACTION_TO_CAMERA] crosses into the extreme foreground so the audience feels physically inside the event.

[EMPEROR] is a mature, non-photoreal historical manga character wearing period-correct [COSTUME_AND_IDENTITY_DETAILS]. The character occupies 55–70% of the visual mass in a medium-close or large three-quarter composition. Preserve a large readable face, expressive hands, a distinctive silhouette, and a decisive emotional state.

The historical event is caused by the character's action: [EVENT_ACTION]. Surround the character with only [IDENTITY_PROPS] and [EVENT_LAYERS]. Every object must explain this specific person rather than generic imperial status.

Visual system: mineral-pigment mural fused with expressive Chinese ink motion; aged plaster and rough paper, visible stone-blue, mineral-green, cinnabar, ochre, ink-black and distressed antique gold; cracked wall, flaking pigment, fragmented gold leaf, dry-brush edges, flying-white ink and forceful directional strokes. Adult historical comic linework, bold shape design, controlled exaggeration, strong foreground perspective.

Freeze the action before completion. No static portrait, no museum-display pose, no generic dragon or throne, no photoreal skin, no cinematic live-action rendering, no smooth 3D CGI, no generic AI-anime polish, no readable text, pseudo-writing, interface, chart, logo or watermark.
```

## 验收门槛

生成后必须同时回答“是”：

1. 缩小观看时，人物是否仍是第一视觉层？
2. 不看标题，能否从动作和道具识别此人，而不只是“某位皇帝”？
3. 观众能否说出自己站在事件中的哪里？
4. 是否至少有一个动作或物体朝镜头发生？
5. 是否定格在动作尚未完成的瞬间？
6. 岩彩、裂壁或墨势是否参与叙事，而非表面滤镜？
7. 是否避开真人写实、平滑 3D、通用龙椅和伪字？
8. 是否可拆成至少四层进行视差、推拉、墨尘或碎片动画？

任一项为“否”，不得进入批量生产。
