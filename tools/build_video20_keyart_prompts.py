#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build video-01 key-art text packs: EN image prompts + ZH overlays."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "video" / "video-01" / "key-art"
CARDS = OUT / "cards"
VIDEO20 = ROOT / "data" / "catalog" / "video20.json"

PREFIX = (
    "Chinese historical epic character atlas key art, cinematic illustration, "
    "semi-realistic anime painterly style, dramatic lighting, rich atmosphere, "
    "full scene storytelling composition, one Chinese emperor as the sole main character, "
    "signature historical moment frozen in one frame, highly detailed environment that explains the event, "
    "16:9 widescreen, "
)

SUFFIX = (
    "leave darker empty space in the lower-left third for a future radar UI overlay, "
    "leave clean darker margin on the right side for Chinese title text, "
    "no readable text, no letters, no Chinese characters, no UI, no watermark, no logo, "
    "no modern objects, no photorealistic selfie look, masterpiece composition"
)

NEGATIVE = (
    "text, letters, Chinese characters, English words, watermark, logo, UI, radar chart, "
    "HUD, QR code, modern clothing, guns, cars, neon cyberpunk, chibi, deformed hands, "
    "extra limbs, duplicate faces, lowres, blurry"
)

# scene design per id
SCENES = {
    "qin-shi-huang": {
        "order": 1,
        "event_zh": ["前221称帝", "书同文·车同轨"],
        "event_label": "代表事",
        "scene_one_liner_zh": "咸阳殿上称始皇帝，六国版图在身后收束为一。",
        "props_zh": "冕旒、玄衣、权量/竹简、咸阳宫阙、统一后的暗金地图光",
        "mood_zh": "纪念碑式冷硬，鎏金与玄黑",
        "prompt": (
            "Emperor Qin Shi Huang standing alone on a high black-and-gold palace terrace of Xianyang, "
            "tall crown and black imperial robe with gold edges, stern forward gaze as if measuring the world, "
            "behind him a vast ancient China map of the six states dissolving into one unified dark gold realm, "
            "ritual bronze measuring vessels and bamboo slips glowing faintly at his feet, "
            "monumental symmetry, smoke and cold dawn light, imperial seal atmosphere without showing any seal text"
        ),
    },
    "han-xuan-di": {
        "order": 2,
        "event_zh": ["地节亲政", "综核名实"],
        "event_label": "代表事",
        "scene_one_liner_zh": "未央案牍如山，朱笔核名实；民间长养的眼神仍在。",
        "props_zh": "竹简山、朱笔、未央宫夜灯、长安街市远景虚影",
        "mood_zh": "暖灰务实，审计感",
        "prompt": (
            "Emperor Han Xuandi as a calm middle-aged ruler in plain but dignified Han dynasty robes, "
            "seated or standing beside a mountain of bamboo document slips in Weiyang Palace at night, "
            "holding a red-ink brush mid-stroke as if auditing names against reality, "
            "soft warm gray lamp light, subtle ghost image of common street life of Chang'an in the misty background, "
            "intelligent sharp eyes of someone raised among commoners, quiet power not martial spectacle"
        ),
    },
    "han-wu-di": {
        "order": 3,
        "event_zh": ["封狼居胥", "漠北勒石"],
        "event_label": "代表事",
        "scene_one_liner_zh": "漠北风烈，狼居胥山影，金甲帝君立于军旗潮上。",
        "props_zh": "狼居胥山、旌旗、战马、沙金光、远处匈奴残阵",
        "mood_zh": "大漠金红，雄开",
        "prompt": (
            "Emperor Han Wudi in golden-red armor and imperial cloak on a windy Mongolian desert ridge, "
            "the dark silhouette of Langjuxu Mountain behind him, countless Han banners and cavalry below like a tide, "
            "sand gold light and cold blue sky, victorious yet heavy atmosphere of endless northern campaigns, "
            "cinematic low angle hero shot, dust and horsehair in the wind"
        ),
    },
    "xin-wang-mang": {
        "order": 4,
        "event_zh": ["始建国元年", "托古改制"],
        "event_label": "代表事",
        "scene_one_liner_zh": "明堂礼器金光刺眼，王莽捧圭如假周公，币制碎片在脚边。",
        "props_zh": "圭、明堂、错刀钱币、周公虚影叠化",
        "mood_zh": "伪古典，铜绿惨白",
        "prompt": (
            "Wang Mang as the Xin dynasty usurper-emperor in overly perfect Confucian ritual robes, "
            "holding a jade gui tablet with an almost mask-like solemn smile inside a cold bright Mingtang hall, "
            "bronze ritual vessels gleam too cleanly, broken ancient knife-coins and failed currency shards scatter at his feet, "
            "a faint ghostly silhouette of the Duke of Zhou overlapping his shadow, copper-green and pale light, uncanny classical beauty"
        ),
    },
    "e-han-guangwu": {
        "order": 5,
        "event_zh": ["昆阳之战", "以少击众"],
        "event_label": "代表事",
        "scene_one_liner_zh": "暴雨昆阳城下，一旅冲阵，雷光中汉帜将起。",
        "props_zh": "暴雨、城墙、少骑、新军潮、雷光",
        "mood_zh": "雨战脏镜头→中兴晴意",
        "prompt": (
            "Emperor Liu Xiu (Guangwu) as a young war leader charging through torrential rain at the Battle of Kunyang, "
            "small Han cavalry spearhead smashing into a vast dark enemy army tide, city walls of Kunyang behind, "
            "lightning white against storm clouds, mud and flying water, desperate heroic energy of restoration, "
            "one clear main figure on horseback dominating the frame"
        ),
    },
    "h-zhao-shi-le": {
        "order": 6,
        "event_zh": ["襄国称赵", "奴隶天子"],
        "event_label": "代表事",
        "scene_one_liner_zh": "铁链碎落，夯土襄国城上升起赵字旗，奴隶已登帝座。",
        "props_zh": "断锁链、帝座、襄国夯土城、风沙、赵旗",
        "mood_zh": "铁锈尘黄，阶级逆袭",
        "prompt": (
            "Shi Le of Later Zhao as a rugged non-Han emperor rising from slavery to the throne, "
            "broken iron slave chains falling from his wrists as he sits or stands upon a rough imperial seat, "
            "rammed-earth fortress of Xiangguo behind him in dusty wind, a Zhao battle banner rising, "
            "rust iron and bone-white colors, hard life etched on his face, epic class-ascent atmosphere"
        ),
    },
    "liang-wu": {
        "order": 7,
        "event_zh": ["舍身同泰", "侯景将至"],
        "event_label": "代表事",
        "scene_one_liner_zh": "同泰寺金佛前帝王舍身，赎身钱山堆起；远处建康已有甲骑烟尘。",
        "props_zh": "金佛、袈裟一角、钱山、同泰寺、建康烟",
        "mood_zh": "前金后灰",
        "prompt": (
            "Emperor Liang Wudi before a colossal golden Buddha in Tongtai Temple, Jiankang, "
            "wearing imperial robes with a Buddhist kasaya edge, ritual of self-dedication, "
            "piles of ransom coins and offerings around him, holy golden light on his face, "
            "but far outside the temple gate gray smoke and armored cavalry dust of coming Hou Jing chaos, "
            "beauty and doom in one frame, lotus and ash"
        ),
    },
    "xixia-li-yuanhao": {
        "order": 8,
        "event_zh": ["1038称帝", "河西立国"],
        "event_label": "代表事",
        "scene_one_liner_zh": "贺兰山下兴庆城，元昊称制，西夏文字如刃在风中。",
        "props_zh": "贺兰山、兴庆、党项服饰、西夏文纹样光（勿写可辨字母）",
        "mood_zh": "河西硬光，砂金藏青",
        "prompt": (
            "Li Yuanhao, founder-emperor of Western Xia, standing on a fortress wall of Xingqing under Helan Mountains, "
            "distinct Tangut-inspired royal costume and fierce eagle-like eyes, desert hard sunlight, "
            "sand-gold and deep blue palette, abstract glowing glyph patterns of a unique script in the air without readable letters, "
            "sense of a new empire rising on the Hexi frontier against distant Song dynasty horizons"
        ),
    },
    "q-qin-fu-jian": {
        "order": 9,
        "event_zh": ["投鞭断流", "淝水将败"],
        "event_label": "代表事",
        "scene_one_liner_zh": "江天开阔，苻坚扬鞭指江，幻觉万鞭可断流；江水冷色已埋败兆。",
        "props_zh": "长江天堑、马鞭、密密幻觉鞭影、东岸薄雾",
        "mood_zh": "盛世金→江水冷",
        "prompt": (
            "Fu Jian of Former Qin on a high bank overlooking a wide Yangtze-like river, "
            "raising a horsewhip toward the water in the famous 'throwing whips could stop the current' hubris moment, "
            "golden late-afternoon light on his armor while the river itself is cold blue-gray foreshadowing Feishui disaster, "
            "illusory countless whip silhouettes over the current, vast army suggestion behind him, tragic pride"
        ),
    },
    "n-wei-xiaowen": {
        "order": 10,
        "event_zh": ["太和迁都", "胡骑解辫"],
        "event_label": "代表事",
        "scene_one_liner_zh": "洛阳城楼下，孝文帝解鲜卑辫、易汉服，北风与礼乐交界。",
        "props_zh": "辫发丝、汉服、洛阳城阙、南迁车队远影",
        "mood_zh": "塞外风→中原礼",
        "prompt": (
            "Emperor Xiaowen of Northern Wei at the moment of cultural reform, "
            "slowly unbraiding Xianbei hair and putting on elegant Han-style court robes upon Luoyang city tower, "
            "southern migration caravan faintly visible on the road below, cold northern wind meeting warm ritual lantern light, "
            "solemn transformative atmosphere, identity change made visual, no readable text"
        ),
    },
    "sui-wen": {
        "order": 11,
        "event_zh": ["开皇灭陈", "混一戎夏"],
        "event_label": "代表事",
        "scene_one_liner_zh": "长江上南征舰影，建康降帜；身后大兴城网格如制度蓝图。",
        "props_zh": "战船、建康、大兴规划网格、皂衣帝",
        "mood_zh": "清俭冷色，制度感",
        "prompt": (
            "Emperor Wen of Sui in relatively frugal dark imperial robes, standing above a geometric plan-like vision of Daxing City grid, "
            "while the Yangtze campaign fleet sails toward Jiankang with a falling Chen dynasty banner in the distance, "
            "cool blue-gray institutional light, reunification of north and south as calm inevitability, "
            "ruler as system-builder rather than pure warlord"
        ),
    },
    "sui-yang": {
        "order": 12,
        "event_zh": ["江都之变", "运河如带"],
        "event_label": "代表事",
        "scene_one_liner_zh": "龙舟金碧与运河玉带壮美在前，江都夜刀光已贴身——晋王余影犹在。",
        "props_zh": "龙舟、运河俯瞰、江都宫、冷刃",
        "mood_zh": "绮丽到刺眼再坠入夜",
        "prompt": (
            "Emperor Yang of Sui on a luxurious dragon boat along a luminous grand canal that looks like a jade belt from above, "
            "gorgeous gold and turquoise splendor, yet a cold dagger glint and night shadows of Jiangdu palace close in on him, "
            "split mood of magnificent infrastructure legacy and personal doom, weary imperial face, "
            "cinematic color contrast between canal beauty and murderous night"
        ),
    },
    "tang-tai-zong": {
        "order": 13,
        "event_zh": ["天可汗", "贞观纳谏"],
        "event_label": "代表事",
        "scene_one_liner_zh": "金甲未卸，手中却是谏纸；远处突厥旗倒，凌烟虚影。",
        "props_zh": "金甲、谏纸、天可汗气场、凌烟阁虚影",
        "mood_zh": "明朗顶格，弓马与谏争光",
        "prompt": (
            "Emperor Taizong of Tang in bright golden armor but holding an open remonstrance paper scroll instead of a weapon, "
            "wise intense eyes, behind him collapsed Turkic banners and a faint ghostly wall of meritorious ministers (Lingyan spirit), "
            "clear Zhenguan daylight, balance of martial glory and good governance, heroic yet thoughtful, "
            "high classical Tang atmosphere"
        ),
    },
    "zhou-wu-zetian": {
        "order": 14,
        "event_zh": ["天授称帝", "金轮称制"],
        "event_label": "代表事",
        "scene_one_liner_zh": "神都洛阳紫雾，女帝冕旒，金轮法器光轮在背。",
        "props_zh": "冕旒、金轮、洛阳明堂想象、紫雾",
        "mood_zh": "神都纪念碑，不宫斗",
        "prompt": (
            "Wu Zetian as sole female emperor of Zhou, wearing full imperial mianguan crown and solemn dragon-pattern robes, "
            "standing in purple mist of Luoyang divine capital, a great golden wheel mandala light behind her like political-religious authority, "
            "monumental not sensual, cold sacred power, palace silhouettes and Mingtang suggestion, "
            "no harem melodrama, pure sovereign presence"
        ),
    },
    "tang-xian-zong": {
        "order": 15,
        "event_zh": ["元和削藩", "雪夜蔡州"],
        "event_label": "代表事",
        "scene_one_liner_zh": "大明宫夜，帝指藩镇地图；叠化雪夜蔡州城下唐军。",
        "props_zh": "地图钉、雪、蔡州城、夜烛",
        "mood_zh": "中晚唐冷硬",
        "prompt": (
            "Emperor Xianzong of Tang in a dark Daming Palace night chamber, finger pressing on a military map of rebellious fanzhen provinces, "
            "candles and cold blue moonlight, double-exposure style blend with snowy night assault on Caizhou city walls, "
            "mid-Tang restoration tension, sharp determined middle-aged emperor, sparse and hard atmosphere"
        ),
    },
    "zhou-shi": {
        "order": 16,
        "event_zh": ["高平之战", "显德振旅"],
        "event_label": "代表事",
        "scene_one_liner_zh": "高平坡上亲征斩溃，青年英主甲不离身，战旗如血。",
        "props_zh": "高平坡、玄甲、战旗、溃兵",
        "mood_zh": "短促燃烧",
        "prompt": (
            "Emperor Shizong of Later Zhou, young martial sovereign Chai Rong in black-silver armor on Gaoping battlefield slope, "
            "personally rallying troops and striking down fleeing cowards, blood-red banners, autumn grass and smoke, "
            "short brilliant life energy, high action epic still frame, forever in armor"
        ),
    },
    "n-tang-houzhu": {
        "order": 17,
        "event_zh": ["975城破", "江南残梦"],
        "event_label": "代表事",
        "scene_one_liner_zh": "金陵夜雨，词人帝王倚窗；城破火光映水，墨迹在雨中化开。",
        "props_zh": "雨窗、词稿（勿显字）、秦淮、火光水影",
        "mood_zh": "水墨湿冷",
        "prompt": (
            "Li Yu, last ruler of Southern Tang, as a poet-emperor not a warrior, leaning by a rainy night window in Jinling, "
            "ink and blank paper without readable characters, distant city-fall fire reflecting on Qinhuai water, "
            "wet ink-wash melancholy blue-gray palette, soft tragic beauty, dream of Jiangnan ending"
        ),
    },
    "n-song-tai-zu": {
        "order": 18,
        "event_zh": ["杯酒释兵权", "烛宴"],
        "event_label": "代表事",
        "scene_one_liner_zh": "宫宴烛光下笑劝酒盏，宿将卸甲；黄袍只在门外一闪。",
        "props_zh": "酒盏、长案、烛、卸甲背影、门外黄袍虚影",
        "mood_zh": "温柔一刀",
        "prompt": (
            "Emperor Taizu of Song Zhao Kuangyin smiling gently while offering wine cups to senior generals at a candlelit palace banquet, "
            "generals removing armor in the background, soft gold candlelight, political soft power moment of releasing military authority, "
            "a faint yellow robe silhouette outside the door recalling Chenqiao, intimate tension under courtesy"
        ),
    },
    "yuan-shi-zu": {
        "order": 19,
        "event_zh": ["1279灭宋", "混一车书"],
        "event_label": "代表事",
        "scene_one_liner_zh": "大都中轴气象与草原风并存，崖山海浪远吞宋帜。",
        "props_zh": "大都、草原云、崖山浪、驿马虚线",
        "mood_zh": "帝国尺度",
        "prompt": (
            "Kublai Khan, Yuan Shizu, as a Eurasian-scale emperor combining Mongol and Chinese imperial presence, "
            "standing where Dadu city axis meets open steppe wind, far-southern sea waves of Yashan swallowing Song banners, "
            "relay-horse light trails suggesting empire networks, blue-silver Mongol sky and palace red accents, "
            "vast unification mood without modern flags or text"
        ),
    },
    "n-wei-taiwu": {
        "order": 20,
        "event_zh": ["灭北凉", "真君铁骑"],
        "event_label": "代表事",
        "scene_one_liner_zh": "铁骑踏雪统一北方，姑臧城破烟起；佛铃碎响在风里。",
        "props_zh": "铁骑、雪原、城破烟、碎佛铃意象（克制）",
        "mood_zh": "粗粝寒冷武巅峰",
        "prompt": (
            "Emperor Taiwu of Northern Wei Tuoba Tao as a brutal cavalry conqueror on a snowy northern campaign, "
            "iron horsemen flooding a desert fortress gate of the Northern Liang capital, smoke and winter light, "
            "hard iron-blue palette, distant cracked temple bells suggesting religious persecution without graphic gore focus, "
            "raw military peak of northern unification"
        ),
    },
}

AXIS_LABELS = [
    ("wugong", "武功"),
    ("wenzhi", "文治"),
    ("taolue", "韬略"),
    ("guozuo", "国祚"),
    ("houxiao", "后效"),
    ("yuedan", "月旦"),
]


def full_prompt(body: str) -> str:
    return PREFIX + body.strip().rstrip(",") + ", " + SUFFIX


def card_md(p: dict, sc: dict) -> str:
    scores = p["scores"]
    score_lines = " · ".join(f"{zh}{scores[k]}" for k, zh in AXIS_LABELS)
    radar_rows = "\n".join(f"| {zh} | {scores[k]} |" for k, zh in AXIS_LABELS)
    ev1, ev2 = sc["event_zh"][0], sc["event_zh"][1] if len(sc["event_zh"]) > 1 else ""
    rep_block = f"《{ev1}》" + (f"\n《{ev2}》" if ev2 else "")
    fp = full_prompt(sc["prompt"])
    return f"""---
id: "{p['id']}"
display: "{p['display']}"
epithet: "{p['epithet']}"
order: {sc['order']}
batch: video-01
type: key-art-static
---

# Key Art · {sc['order']:02d} · {p['display']}「{p['epithet']}」

## 1. 中文叠字（后期 UI，勿写入 Image）

### 右上 · 代表事

```
[{sc['event_label']}]
{rep_block}
```

### 右下 · 四字号 + 名

```
[{p['epithet']}]
{p['display']}
```

### 可选顶栏

```
《皇帝图鉴》先导 · video-01
```

### 左下雷达数字（程序绘）

| 轴 | 分 |
|----|-----|
{radar_rows}

一行速记：`{score_lines}`

## 2. 画面设计（中文说明 · 给美术/你自己）

| 项 | 内容 |
|----|------|
| 一句话场景 | {sc['scene_one_liner_zh']} |
| 代表事件 | { ' / '.join(sc['event_zh']) } |
| 关键道具 | {sc['props_zh']} |
| 气质色调 | {sc['mood_zh']} |
| 史料钩 | `content/sources/{p['id']}/` · 分镜 `content/video/video-01/分镜/{p['id']}.md` |

**综合效果目标（对标文豪图鉴井中贺知章）：**  
人物被「钉」在代表事件的空间里；环境与道具替你讲完故事；左下/右侧留给雷达与中文标题。

## 3. English image prompt（复制给 Image）

### Positive

```
{fp}
```

### Negative

```
{NEGATIVE}
```

### Settings hint

- Aspect: **16:9**
- Style strength: high illustration / cinematic
- Do **not** ask the model to render Chinese text or radar

## 4. Post checklist

- [ ] 底板无字无 UI  
- [ ] 雷达六维与 video20 一致  
- [ ] 右上代表事、右下四字号+姓名  
- [ ] 暗角与参考帧同级  
"""


def main():
    data = json.loads(VIDEO20.read_text(encoding="utf-8"))
    profiles = {p["id"]: p for p in data["profiles"]}
    CARDS.mkdir(parents=True, exist_ok=True)

    overlay = {"version": "1.0", "batch": "video-01", "axes": [zh for _, zh in AXIS_LABELS], "cards": []}
    table_rows = [
        "| # | id | 人物 | 四字号 | 代表事 | 卡 |",
        "|---|-----|------|--------|--------|-----|",
    ]
    en_only = [
        "# video-01 key-art EN prompts only",
        "# Each block: id | display | then positive prompt",
        "",
    ]

    missing = []
    for pid, sc in sorted(SCENES.items(), key=lambda x: x[1]["order"]):
        if pid not in profiles:
            missing.append(pid)
            continue
        p = profiles[pid]
        md = card_md(p, sc)
        (CARDS / f"{pid}.md").write_text(md, encoding="utf-8")
        fp = full_prompt(sc["prompt"])
        en_only += [
            f"## {sc['order']:02d} | {pid} | {p['display']} | {p['epithet']}",
            "",
            fp,
            "",
            f"NEGATIVE: {NEGATIVE}",
            "",
            "---",
            "",
        ]
        ev = " / ".join(sc["event_zh"])
        table_rows.append(
            f"| {sc['order']} | `{pid}` | {p['display']} | {p['epithet']} | {ev} | [cards/{pid}.md](cards/{pid}.md) |"
        )
        overlay["cards"].append(
            {
                "id": pid,
                "order": sc["order"],
                "display": p["display"],
                "epithet": p["epithet"],
                "dynasty": p.get("dynasty"),
                "event_label": sc["event_label"],
                "event_lines": sc["event_zh"],
                "scores": p["scores"],
                "scene_one_liner_zh": sc["scene_one_liner_zh"],
                "prompt_en": fp,
                "negative_en": NEGATIVE,
            }
        )

    (OUT / "01-二十人主画面总表.md").write_text(
        "# 二十人静态主画面总表\n\n"
        "> 每人一张 Key Art；英文 prompt 在 `cards/` 与 `prompts-en-only.txt`\n\n"
        + "\n".join(table_rows)
        + "\n\n叠字 JSON：`overlay-zh.json`\n",
        encoding="utf-8",
    )
    (OUT / "prompts-en-only.txt").write_text("\n".join(en_only), encoding="utf-8")
    (OUT / "overlay-zh.json").write_text(
        json.dumps(overlay, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    readme = f"""# Key Art · 静态主画面文字包（video-01）

> 对标文豪图鉴：**一人一静帧 = 人物 + 代表事件场景 + 背景综合**；雷达与中文后期叠。  
> **不在此生成图片**——只准备文案与英文 Image 提示词。

## 怎么用

1. 读 [`00-版式对照文豪图鉴.md`](00-版式对照文豪图鉴.md) 定构图习惯  
2. 打开 [`01-二十人主画面总表.md`](01-二十人主画面总表.md) 选人  
3. 进 [`cards/{{id}}.md`](cards/) 复制 **English prompt** 到 Image  
4. 出图后用 [`overlay-zh.json`](overlay-zh.json) 叠中文与六维分  
5. 批跑可用 [`prompts-en-only.txt`](prompts-en-only.txt)

## 原则（你提的要求）

| 要求 | 落地 |
|------|------|
| 静态主画面 | 每人 1 张 16:9 事件综合场景 |
| 人物+代表事件+背景 | 已写进中文场景说明 + 英文 prompt |
| 中文 | 仅叠字层（代表事/四字号/姓名/六维标签） |
| 英文 | 全部出图 prompt 与 negative |
| 先不生成图 | 本目录只有 md/json/txt |

## 完成度

- 卡片数：{len(overlay['cards'])} / 20  
- 缺场景设计：{missing or '无'}  

## 与分镜关系

- 分镜动态片：`../分镜/`  
- Key Art 可作片头定格、片尾图鉴卡、封面缩略图  
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")
    print("cards", len(overlay["cards"]), "missing", missing)


if __name__ == "__main__":
    main()
