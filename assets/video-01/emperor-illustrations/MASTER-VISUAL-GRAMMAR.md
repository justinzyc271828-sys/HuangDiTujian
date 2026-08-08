# 固定视觉语法与母提示词

版本：`v2.3 camera-palette-identity-physics`  
风格名：**岩彩裂壁 · 墨势入场**

## 两张权威锚点

- 主锚点：`D:\Workspaces\Github\HuangDiTujian\assets\style-bible\v1\approved\01-qin-shi-huang-final-v1.png`
- 辅助墨势锚点：`D:\Workspaces\Github\HuangDiTujian\assets\style-bible\v1\references\emperor-series-ink-motion-v1.png`

主锚点只控制材质、人物主导性、成年漫画造型和事件参与原则，**不控制具体机位**；辅助锚点只控制泼墨、飞白和运动方向。其他帝王不得复制秦始皇的构图、帝印、地图、权量或车辙。

## v2.3 的核心边界

统一的是 **岩彩材质、裂壁肌理、墨势笔触、成年历史漫画造型**；不统一机位、人物姿态和整幅配色。每个人必须同时执行自己提示词内的 `CAMERA PLAN` 与 `COLOR AND GOLD BUDGET`。金色不是系列滤镜，只能按个人额度出现在有意义的位置。参与感可以来自遮挡、共同移动、空间威胁、旁观压力或视线关系，禁止把它自动翻译成“人物正面伸手抓向镜头”。

## 锁定母提示词

```text
LOCKED SERIES RENDERING GRAMMAR — lock the medium, mark-making and adult character design; do not lock the camera, palette distribution or Qin-specific objects:
an adult non-photoreal Chinese historical manga illustration fused with a mineral-pigment mural and forceful expressive ink motion; aged plaster and coarse paper; visibly granular mineral pigments selected from a character-specific palette; cracked wall, flaking pigment, dry-brush edges, flying-white ink and directional brush force; fragmented distressed gold leaf appears only when the per-emperor palette plan assigns it and must never become a universal gold-splatter overlay. Use no more than the assigned gold budget. Bold designed silhouette, decisive facial planes, expressive anatomy and controlled exaggeration. The emperor must remain the unmistakable visual subject and normally occupy 48–72 percent of the visual mass, but profile, rear three-quarter, overhead, ground-level, over-the-shoulder and off-center arrangements are all valid when assigned by the per-emperor camera plan. The viewer has a precise position inside the historical event. Participation may come from proximity, occlusion, eyeline, danger crossing the frame, shared movement or spatial pressure; it does not require a hand or prop aimed at the lens. Freeze the scene before the action finishes. Make the cracks, pigment and ink carry the event's direction and force rather than act as a decorative filter. The CAMERA PLAN and COLOR PLAN below are authoritative and must visibly differ from adjacent images.
```

## 固定禁项

```text
static atlas portrait, museum-display pose, repeated centered frontal emperor, repeated low-angle hero shot, repeated table-edge composition, automatic hand-or-prop thrust at the camera unless explicitly assigned, universal black-and-gold treatment, gold dust scattered uniformly over the entire frame, excessive gold leaf above the assigned budget, generic dragon, generic throne, generic palace grandeur used as identity, photoreal skin, live-action cinematic realism, glossy 3D CGI, smooth generic AI-anime polish, cute or chibi styling, idol face, plastic costume, modern objects, European armor, Japanese samurai armor, readable text, letters, Chinese characters, pseudo-writing, logo, watermark, interface, radar chart, infographic, multiple competing focal characters, cropped crown, deformed hands, extra fingers, blood or gore
```

## 十三项硬验收

1. 人物是否仍是最大单一视觉主体，脸部是否清楚可读？
2. 不看标题，能否从动作和道具认出此人，而不只是“某位皇帝”？
3. 观众能否说出自己在事件中站在哪里？
4. 参与方式是否符合本人 `AUDIENCE PARTICIPATION MODE`，而不是默认伸手或道具冲镜头？
5. 是否定格在动作尚未完成的一瞬？
6. 岩彩、裂壁和墨势是否参与动作，而不是表面滤镜？
7. 是否无真人写实、平滑 3D、通用龙椅、可读文字和伪字？
8. 是否能拆成前景冲击、人物、事件、远景至少四层？
9. 俯仰、人物朝向、景别、镜头滚转、运动轴及专属姿势是否执行了本人的 `SHOT_CODE` 与 `POSE AND ANATOMY`？
10. 与前后相邻图片相比，上述五个维度是否至少有两个发生肉眼可见的改变？
11. 是否执行本人的 `COLOR_CODE` 与金色额度，且金色只落在被指定的叙事物件上？
12. 与前后相邻图片相比，主色温或金色密度是否明显改变，并且没有套用统一黑金飞溅层？
13. 所有器物、影子和环境线条是否服从同一透视与光源；贴地物是否有接触阴影，未指定的物体是否绝不悬空？

任一项为“否”，不得保存为正式输出。
