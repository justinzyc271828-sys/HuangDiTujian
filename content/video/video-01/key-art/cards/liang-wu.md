---
id: "liang-wu"
display: "梁武帝"
personal: "萧衍"
epithet: "同泰天子"
order: 7
batch: video-01
type: key-art-static
naming: "personal-first then title; no book-title marks on events"
---

# Key Art · 07 · 萧衍（梁武帝）「同泰天子」

## 1. 中文叠字（后期 UI，勿写入 Image）

> **命名规则**：先出**本人姓名**，再出庙号/通行称号；代表事**不加书名号**。

### 右上 · 代表事

```
[代表事]
舍身同泰
侯景将至
```

### 右下 · 四字号 + 姓名（本名在上）

```
[同泰天子]
萧衍
梁武帝
```

### 可选顶栏

```
皇帝图鉴 · 先导 video-01
```

### 左下雷达数字（程序绘）

| 轴 | 分 |
|----|-----|
| 武功 | 48 |
| 文治 | 78 |
| 韬略 | 62 |
| 国祚 | 55 |
| 后效 | 72 |
| 月旦 | 50 |

一行速记：`武功48 · 文治78 · 韬略62 · 国祚55 · 后效72 · 月旦50`

## 2. 画面设计（中文说明 · 给美术/你自己）

| 项 | 内容 |
|----|------|
| 一句话场景 | 同泰寺金佛前帝王舍身，赎身钱山堆起；远处建康已有甲骑烟尘。 |
| 代表事件 | 舍身同泰 / 侯景将至 |
| 关键道具 | 金佛、袈裟一角、钱山、同泰寺、建康烟 |
| 气质色调 | 前金后灰 |
| 史料钩 | `content/sources/liang-wu/` · 分镜 `content/video/video-01/分镜/liang-wu.md` |

**综合效果目标（对标文豪图鉴井中贺知章）：**  
人物被「钉」在代表事件的空间里；环境与道具替你讲完故事；左下/右侧留给雷达与中文标题。  
叠字像「贺知章」那样出**人名**，不拿「文豪称号」当主名；四字号只当绰号框。

## 3. English image prompt（复制给 Image）

### Positive

```
Chinese historical epic character atlas key art, cinematic illustration, semi-realistic anime painterly style, dramatic lighting, rich atmosphere, full scene storytelling composition, one Chinese emperor as the sole main character, signature historical moment frozen in one frame, highly detailed environment that explains the event, 16:9 widescreen, Emperor Liang Wudi before a colossal golden Buddha in Tongtai Temple, Jiankang, wearing imperial robes with a Buddhist kasaya edge, ritual of self-dedication, piles of ransom coins and offerings around him, holy golden light on his face, but far outside the temple gate gray smoke and armored cavalry dust of coming Hou Jing chaos, beauty and doom in one frame, lotus and ash, leave darker empty space in the lower-left third for a future radar UI overlay, leave clean darker margin on the right side for Chinese title text, no readable text, no letters, no Chinese characters, no UI, no watermark, no logo, no modern objects, no photorealistic selfie look, masterpiece composition
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
