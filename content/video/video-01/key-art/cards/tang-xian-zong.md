---
id: "tang-xian-zong"
display: "唐宪宗"
personal: "李纯"
epithet: "元和鞭藩"
order: 15
batch: video-01
type: key-art-static
naming: "personal-first then title; no book-title marks on events"
---

# Key Art · 15 · 李纯（唐宪宗）「元和鞭藩」

## 1. 中文叠字（后期 UI，勿写入 Image）

> **命名规则**：先出**本人姓名**，再出庙号/通行称号；代表事**不加书名号**。

### 右上 · 代表事

```
[代表事]
元和削藩
雪夜蔡州
```

### 右下 · 四字号 + 姓名（本名在上）

```
[元和鞭藩]
李纯
唐宪宗
```

### 可选顶栏

```
皇帝图鉴 · 先导 video-01
```

### 左下雷达数字（程序绘）

| 轴 | 分 |
|----|-----|
| 武功 | 76 |
| 文治 | 87 |
| 韬略 | 90 |
| 国祚 | 48 |
| 后效 | 78 |
| 月旦 | 80 |

一行速记：`武功76 · 文治87 · 韬略90 · 国祚48 · 后效78 · 月旦80`

## 2. 画面设计（中文说明 · 给美术/你自己）

| 项 | 内容 |
|----|------|
| 一句话场景 | 大明宫夜，帝指藩镇地图；叠化雪夜蔡州城下唐军。 |
| 代表事件 | 元和削藩 / 雪夜蔡州 |
| 关键道具 | 地图钉、雪、蔡州城、夜烛 |
| 气质色调 | 中晚唐冷硬 |
| 史料钩 | `content/sources/tang-xian-zong/` · 分镜 `content/video/video-01/分镜/tang-xian-zong.md` |

**综合效果目标（对标文豪图鉴井中贺知章）：**  
人物被「钉」在代表事件的空间里；环境与道具替你讲完故事；左下/右侧留给雷达与中文标题。  
叠字像「贺知章」那样出**人名**，不拿「文豪称号」当主名；四字号只当绰号框。

## 3. English image prompt（复制给 Image）

### Positive

```
Chinese historical epic character atlas key art, cinematic illustration, semi-realistic anime painterly style, dramatic lighting, rich atmosphere, full scene storytelling composition, one Chinese emperor as the sole main character, signature historical moment frozen in one frame, highly detailed environment that explains the event, 16:9 widescreen, Emperor Xianzong of Tang in a dark Daming Palace night chamber, finger pressing on a military map of rebellious fanzhen provinces, candles and cold blue moonlight, double-exposure style blend with snowy night assault on Caizhou city walls, mid-Tang restoration tension, sharp determined middle-aged emperor, sparse and hard atmosphere, leave darker empty space in the lower-left third for a future radar UI overlay, leave clean darker margin on the right side for Chinese title text, no readable text, no letters, no Chinese characters, no UI, no watermark, no logo, no modern objects, no photorealistic selfie look, masterpiece composition
```

### Negative

```
text, letters, Chinese characters, English words, watermark, logo, UI, radar chart, HUD, QR code, modern clothing, guns, cars, neon cyberpunk, chibi, deformed hands, extra limbs, duplicate faces, lowres, blurry
```

### Settings hint

- Aspect: **16:9**
- Style strength: high illustration / cinematic
- Do **not** ask the model to render Chinese text or radar

## 4. Post checklist

- [ ] 底板无字无 UI  
- [ ] 雷达六维与 video20 一致  
- [ ] 右上代表事（无书名号）  
- [ ] 右下：四字号 + **本名在上** + 称号在下  
- [ ] 暗角与参考帧同级  
