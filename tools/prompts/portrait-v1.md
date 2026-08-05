# 帝王画像 Prompt 模板 v1

在生成前，把 `{}` 替换为该人物 YAML 中的字段。保持全库同一套前缀/后缀，以稳定风格。

## 正面主图（3:4）

```text
Chinese historical emperor portrait illustration, half-body, face clearly visible,
subject: {names.display} ({names.personal}), dynasty: {dynasty.label},
era-accurate ceremonial robe and crown simplified for readability,
dignified presence, subtle ink-wash and xuan paper texture background,
soft side-top lighting, muted mineral pigment palette, no modern elements,
no text, no watermark, not a real photograph of a living person,
art style locked to project Style Bible v1 (fine-line gongbi leaning),
character basis: {portrait.appearance_basis}
```

## 负向提示（通用）

```text
anime, chibi, cyberpunk, neon, photoreal celebrity lookalike,
english letters, chinese watermark, extra fingers, deformed face,
western plate armor, modern suit, selfie, 3d cgi plastic skin
```

## 选图标准

1. 像「图鉴立绘」而不是剧照  
2. 脸部可识别、可做成圆形头像裁切  
3. 服饰大时代不穿帮  
4. 与已有锚点图色温一致  
