# -*- coding: utf-8 -*-
"""
video-01 Key Art：外貌史证 + 不依赖「认出人名」的英文画面描写。

证据等级：
  A = 正史明文相貌/体态
  B = 正史间接（服饰制度、族属、年龄、性情）可据以限定外形
  C = 无明文：按纪年年龄 + 时代衣冠 + 势力视觉作「历史合理重建」（卡片会标明）

英文 prompt 原则：
  - 禁止只写人名指望模型脑补
  - 必须写：年龄段、五官、须眉、体型、发型、服色材质、姿态、场景光色、画风
  - 可用 once「historical figure known as X」作次要标签，但描写须自足
"""

# 每条 prompt 前缀：系列画风壳，但不写具体人名
PREFIX = (
    "16:9 cinematic character-atlas key art illustration, "
    "semi-realistic Chinese historical painterly style with strong stylization, "
    "single main male or female protagonist filling the storytelling frame, "
    "museum-quality costume research look, dramatic cinematic lighting, "
    "environment and props fully explain the historical moment, "
)

SUFFIX = (
    "composition leaves darker empty space in lower-left third for future radar UI, "
    "darker clean margin on the right for later title text, "
    "absolutely no readable text, no letters, no Chinese characters, no UI, no watermark, no logo, "
    "no modern objects, no smartphone, no photoreal selfie, no celebrity likeness, "
    "anatomically careful hands and face, masterpiece"
)

NEGATIVE = (
    "text, letters, Chinese characters, English words, watermark, logo, UI, radar, HUD, "
    "modern clothes, suit, jeans, guns, cars, neon, cyberpunk, chibi, cute anime idol face, "
    "European medieval plate armor, wrong dynasty costume, extra fingers, deformed face, "
    "duplicate person, blurry, lowres, stock photo"
)

# id -> full design
SCENES = {
    "qin-shi-huang": {
        "order": 1,
        "event_zh": ["前221称帝", "书同文·车同轨"],
        "event_label": "代表事",
        "scene_one_liner_zh": "黑旗水德的咸阳高台，中年帝王如度量衡般冷硬站立。",
        "age_moment_zh": "约四十前后（前221称帝时）",
        "appearance_level": "A/B",
        "appearance_sources_zh": [
            "A《史记·秦始皇本纪》载尉缭语：秦王为人「蜂准、长目、挚鸟膺、豺声」（敌对侧写，作五官线索，非美化）",
            "B 同纪：水德，衣服旄旌节旗皆上黑；数以六为纪",
            "B 冕服制度向：通天冠/玄衣想象，以黑为主",
        ],
        "appearance_zh": (
            "东亚中年男性；高而尖的鼻梁（蜂准）；细长而锋利的眼睛（长目）；"
            "前胸略佝、肩背有猛禽般前倾感（挚鸟膺）；薄唇，神情少恩、刻薄镇定；"
            "无须或仅短髭，下颌线条硬；肤色偏冷白；身体精瘦而非横壮；"
            "发型：冠下束发；服：通体玄黑宽袖袍，金线窄缘，黑冠高耸；手不持剑，可近权量竹简。"
        ),
        "style_faction_zh": "秦·水德玄黑纪念碑风；对称、冷、制度感；拒绝暖红汉风。",
        "props_zh": "黑旗、权量、竹简、咸阳高台、六国地图色块收束",
        "mood_zh": "冷硬鎏金+玄黑",
        "prompt": (
            "a stern East Asian man about 40 years old as a Warring-States-to-Qin unifier king-emperor, "
            "distinctive sharp high-bridged nose (beak-like), long narrow piercing eyes, thin hard lips, "
            "slightly hunched predatory chest and shoulders like a raptor, lean wiry body not bulky, "
            "cold pale skin, short sparse facial hair or clean jaw, emotionless measuring gaze, "
            "tall black lacquered ceremonial crown, full black imperial robe with only thin gold trim (water-virtue black system), "
            "standing alone on a high symmetrical Xianyang palace terrace at cold dawn, "
            "behind him six colored state-map fragments collapsing into one dark-gold unified realm, "
            "bronze measuring vessels and bamboo slips at his feet, black banners, monumental symmetry, "
            "smoke, limestone and lacquer textures, style: austere black-gold seal-monument painting"
        ),
    },
    "han-xuan-di": {
        "order": 2,
        "event_zh": ["地节亲政", "综核名实"],
        "event_label": "代表事",
        "scene_one_liner_zh": "未央夜，中年清瘦帝王对案牍朱笔，眼神像从街市里活过来的。",
        "age_moment_zh": "约三十余（地节亲政前后）",
        "appearance_level": "C（正史无细貌；年龄+吏治气质重建）",
        "appearance_sources_zh": [
            "C《汉书·宣帝纪》详政治、不载五官尺寸",
            "B 长于民间、知闾里奸邪——神态宜「市井洞察」而非天生龙颜脸谱",
            "B 西汉中后期冠服：进贤冠/介帻、深衣袍、偏务实不奢",
        ],
        "appearance_zh": (
            "东亚男性，三十中后；脸偏清瘦，颧骨略显，不是肥环龙颜脸；"
            "眉目沉静锐利，眼袋浅，有熬夜看文书感；须短而整齐，非虬髯武夫；"
            "肤色正常偏劳，不涂脂粉；肩窄于武将，手指细长沾朱砂；"
            "服：深褐/皂色宽袖袍，冠简洁，腰间绶带不夸张。"
        ),
        "style_faction_zh": "西汉吏治暖灰；案牍美学；少战场红。",
        "props_zh": "竹简山、朱笔、油灯、未央梁柱",
        "mood_zh": "暖灰审计",
        "prompt": (
            "an East Asian man in his mid-thirties, lean intelligent face with visible cheekbones, "
            "calm sharp inspector eyes, slight sleepless shadows, neat short beard not wild, "
            "slender ink-stained fingers holding a red-ink brush, not a warrior build, "
            "wearing plain dark-brown Western-Han official deep-robe and simple black cap, "
            "standing beside a mountain of bamboo document slips inside Weiyang Palace at night, "
            "warm oil-lamp light, dusty paper atmosphere, faint misty memory of common Chang'an streets behind him, "
            "expression of auditing reality against empty titles, style: muted warm-gray bureaucratic drama painting"
        ),
    },
    "han-wu-di": {
        "order": 3,
        "event_zh": ["封狼居胥", "漠北勒石"],
        "event_label": "代表事",
        "scene_one_liner_zh": "五十上下的雄主立于漠北风口，须眉被沙打起，金红披风猎猎。",
        "age_moment_zh": "约五十前后（漠北叙事高峰期）",
        "appearance_level": "C（本纪无细貌；年龄+开边气质重建）",
        "appearance_sources_zh": [
            "C《汉书·武帝纪》不载具体五官",
            "B 在位久、开边、封禅——宜盛年转老之雄主，非少年脸",
            "B 西汉武冠甲胄、绛袍、佩剑传统图像系统（重建须标明）",
        ],
        "appearance_zh": (
            "东亚男性，四十八至五十五；脸阔而有风霜，眉浓，眼深有倦意与豪气并存；"
            "须髯较密、略染沙土，非白须老翁；鼻梁端正偏高；体格仍壮，肩背宽；"
            "肤色被漠北风吹成偏赭；服：朱红/暗金铠甲外罩披风，武冠或冕式简化，不可欧式板甲。"
        ),
        "style_faction_zh": "西汉漠北史诗；沙金+朱红；油彩颗粒风。",
        "props_zh": "狼居胥山影、汉旗海、战马、沙尘",
        "mood_zh": "大漠金红",
        "prompt": (
            "an East Asian man about 50, broad weathered face, thick dark brows, deep eyes mixing pride and exhaustion, "
            "dense wind-tangled beard with dust, strong wide shoulders still powerful, sun-scorched ruddy skin, "
            "Western-Han style layered armor in crimson and dark gold with flowing cloak, Chinese ancient helmet-crown hybrid not European plate, "
            "standing on a Mongolian desert ridge against a dark mountain silhouette, "
            "tide of Han dynasty banners and cavalry below, sand-gold light, cold blue sky, horsehair and grit in the wind, "
            "low heroic camera angle, style: dusty epic oil-paint campaign panorama"
        ),
    },
    "xin-wang-mang": {
        "order": 4,
        "event_zh": ["始建国元年", "托古改制"],
        "event_label": "代表事",
        "scene_one_liner_zh": "五十许儒服帝王捧圭，笑容标准得像面具，礼器反光发冷。",
        "age_moment_zh": "约五十余（始建国元年）",
        "appearance_level": "B",
        "appearance_sources_zh": [
            "B《汉书·王莽传》：折节恭俭，被服如儒生；侍疾时乱首垢面（非常态，见其表演性）",
            "B 无五官尺寸；性格：外恭内深——外形宜「端正过度」",
        ],
        "appearance_zh": (
            "东亚男性，五十出头；脸型中等偏长，五官端正到不自然；"
            "微笑固定、眼不笑；须修得很齐，儒生式；肤色略苍；"
            "体态不武，肩背端肃；服：仿周礼的过度考究冕服/儒服，圭板在手；"
            "可对比脚边混乱刀币——人整齐、制度碎。"
        ),
        "style_faction_zh": "伪古典铜绿；礼器过亮；不安的干净。",
        "props_zh": "圭、明堂、错刀钱碎片",
        "mood_zh": "铜绿惨白",
        "prompt": (
            "an East Asian man in early fifties, overly correct scholarly face, fixed polite smile that does not reach the eyes, "
            "neatly trimmed Confucian beard, pale slightly unhealthy skin, non-martial thin-shouldered posture, "
            "wearing hyper-ritual archaic Chinese ceremonial robes imitating Zhou classics, holding a jade tablet (gui), "
            "inside a cold bright Mingtang-like hall with too-clean bronze ritual vessels, "
            "broken ancient knife-coins scattered at his feet, copper-green and pale light, uncanny classical beauty, "
            "style: cold pseudo-antiquity still life of power"
        ),
    },
    "e-han-guangwu": {
        "order": 5,
        "event_zh": ["昆阳之战", "以少击众"],
        "event_label": "代表事",
        "scene_one_liner_zh": "二十七八的高大正脸青年，大嘴高鼻日角，雨水泥里带头冲阵。",
        "age_moment_zh": "约二十八九（昆阳，23年）",
        "appearance_level": "A",
        "appearance_sources_zh": [
            "A《后汉书·光武帝纪》：身长七尺三寸，美须眉，大口，隆准，日角",
        ],
        "appearance_zh": (
            "东亚青年男性，近三十；身高明显高于常人（七尺三寸量级的挺拔感）；"
            "浓密好看的眉与须；嘴巴宽大（大口）；鼻梁高隆（隆准）；"
            "额中央骨起如日（日角，前额中央微鼓的贵相结构）；"
            "脸被暴雨打湿，英气脏污并存；体格精悍能战；"
            "服：早期汉军皮甲/玄甲泥污，非龙袍登基像。"
        ),
        "style_faction_zh": "东汉中兴雨战；雷光写实脏镜头。",
        "props_zh": "暴雨、昆阳城、少骑、敌潮",
        "mood_zh": "雨战→将晴",
        "prompt": (
            "a tall East Asian man about 28-29, notably above-average height, handsome thick eyebrows and beard, "
            "wide mouth, high prominent nose bridge, forehead with a raised central bone boss (day-horn physiognomy), "
            "athletic warrior body, rain-soaked muddy face full of decisive fire, "
            "wearing early Eastern-Han leather-and-lamellar armor filthy with mud, not court robes, "
            "charging on horseback through torrential rain as a small spearhead against a vast dark enemy army, "
            "Kunyang city walls behind, white lightning, flying water and mud, restoration-war grit, "
            "style: wet dirty heroic storm painting"
        ),
    },
    "h-zhao-shi-le": {
        "order": 6,
        "event_zh": ["襄国称赵", "奴隶天子"],
        "event_label": "代表事",
        "scene_one_liner_zh": "深目高颧的羯族壮汉登夯土王座，断链犹在腕，风沙扑面。",
        "age_moment_zh": "约五十（称赵/称帝前后）",
        "appearance_level": "A/B",
        "appearance_sources_zh": [
            "A/B《晋书·石勒载记》：上党武乡羯人；少时「胡雏」；长而壮健有胆力，雄武好骑射；相者称「胡状貌奇异」",
            "B 非典型中原儒生脸——深目、高颧、风霜皮的游牧/杂胡感（在「奇异」范围内合理重建）",
        ],
        "appearance_zh": (
            "非纯汉外貌的中年男性；深目，颧骨高，鼻梁偏高，唇厚；"
            "须虬密、略杂；肤色深于中原儒生，风沙粗砺；"
            "体格壮健横阔，臂力感强；曾为奴——腕间可有铁链勒痕；"
            "服：胡汉混杂甲袍，襄国夯土殿，粗织物+金属，不精致龙袍。"
        ),
        "style_faction_zh": "十六国粗粝铁锈风；夯土与风沙。",
        "props_zh": "断锁、夯土城、赵旗、风沙",
        "mood_zh": "铁锈尘黄",
        "prompt": (
            "a rugged middle-aged man of Jie/Xiongnu-related northern non-Han look about 50, "
            "deep-set eyes, high cheekbones, higher nose, thick coarse curly beard, weather-beaten darker skin, "
            "broad powerful slave-built body, iron chain scars still visible on wrists, "
            "mixed Hu-Han armor and rough imperial cloak, sitting or standing on a crude throne in a rammed-earth fortress, "
            "dusty wind, Zhao battle banner rising, rust-iron and bone-white palette, "
            "epic class ascent from slavery to throne, style: harsh fortress dust painting"
        ),
    },
    "liang-wu": {
        "order": 7,
        "event_zh": ["舍身同泰", "侯景将至"],
        "event_label": "代表事",
        "scene_one_liner_zh": "七十余清癯老帝立于金佛前，顶骨异相，袈裟压帝袍。",
        "age_moment_zh": "约七十余（舍身同泰年段）",
        "appearance_level": "A/B",
        "appearance_sources_zh": [
            "A《梁书·武帝纪》：生而有奇异，两胯骈骨，顶上隆起，有文在右手曰武",
            "B 长寿佞佛、蔬食——晚年宜清瘦、须白、眼神执拗慈悲混杂",
        ],
        "appearance_zh": (
            "东亚老年男性，七十上下；脸清癯，颧骨显，须眉花白下垂；"
            "头顶中央骨隆起（顶上隆起）；体态偏瘦（长年佛事）；"
            "眼神既慈悲又固执；右手可有旧疤/纹理暗示「武」文（勿写字）；"
            "服：梁帝袍外罩袈裟一角，金粉与灰扑同在。"
        ),
        "style_faction_zh": "南朝金粉佛光，底子已腐。",
        "props_zh": "金佛、钱山、同泰寺、远处甲骑烟",
        "mood_zh": "前金后灰",
        "prompt": (
            "an East Asian man about 70-75, gaunt devout face, white drooping beard and brows, "
            "noticeably raised bony crown of the skull, thin ascetic body from long Buddhist practice, "
            "eyes mixing compassion and stubborn delusion, "
            "Liang dynasty imperial robe with a Buddhist kasaya draped over it, "
            "standing before a colossal golden Buddha in Tongtai Temple, piles of ransom coins, holy gold light on his face, "
            "far outside the gate gray smoke of approaching armored cavalry, beauty and doom, "
            "style: gilded Buddhist southern-dynasty tragedy"
        ),
    },
    "xixia-li-yuanhao": {
        "order": 8,
        "event_zh": ["1038称帝", "河西立国"],
        "event_label": "代表事",
        "scene_one_liner_zh": "身量不高的圆面高鼻党项君主立于贺兰山风中，鹰视。",
        "age_moment_zh": "约三十五（1038称帝）",
        "appearance_level": "A",
        "appearance_sources_zh": [
            "A《宋史·夏国传》：圆面高准，身长五尺余；少时好衣长袖绯衣，冠黑冠，佩弓矢",
        ],
        "appearance_zh": (
            "东亚/党项男性，三十五左右；明确偏矮（五尺余，短于中原高个武将）；"
            "脸圆；鼻梁很高（高准）；目光鹰隼；"
            "须不需很长；体格精悍；"
            "服：长袖绯衣、黑冠、佩弓矢（史文明）；背后贺兰山与兴庆城。"
        ),
        "style_faction_zh": "西夏河西硬光；砂金藏青；民族纹样抽象光（勿可辨字）。",
        "props_zh": "黑冠、绯衣、弓矢、贺兰山",
        "mood_zh": "砂金硬光",
        "prompt": (
            "a Tangut-looking East Asian man about 35, notably short stature (about five chi, shorter than typical tall generals), "
            "round face, high prominent nose bridge, hawk-sharp eyes, compact athletic body, short neat facial hair, "
            "wearing long-sleeved bright crimson robe, black crown-cap, bow and arrows at belt as described in Song sources, "
            "standing on fortress wall of Xingqing under Helan Mountains, desert hard sunlight, "
            "sand-gold and deep blue palette, abstract unreadable glyph-light of a unique script in the air, "
            "new frontier empire rising, style: hard-light Hexi national-founding painting"
        ),
    },
    "q-qin-fu-jian": {
        "order": 9,
        "event_zh": ["投鞭断流", "淝水将败"],
        "event_label": "代表事",
        "scene_one_liner_zh": "四十上下的氐秦帝王扬鞭指江，明君脸在江风里变成执拗。",
        "age_moment_zh": "约四十五（383淝水）",
        "appearance_level": "C（载记缺细貌；氐族君主+治世转冒进重建）",
        "appearance_sources_zh": [
            "C《晋书》苻坚载记详事功，缺五官尺寸",
            "B 氐人、长期为北方共主——宜明堂气度+后期刚愎神色",
        ],
        "appearance_zh": (
            "东亚男性，四十五左右；脸堂堂，眉目疏朗，本可称明君相；"
            "须中等，修剪齐；此时眼神刚愎、嘴角紧；"
            "体格中上，不像石勒粗野；"
            "服：前秦金赭甲/冕，披风扬起；手扬马鞭指大江。"
        ),
        "style_faction_zh": "前秦盛极金光切江水冷灰。",
        "props_zh": "马鞭、大江、幻觉鞭影、大军",
        "mood_zh": "金→冷江",
        "prompt": (
            "an East Asian man about 45 of Di northern ethnicity, originally handsome open-browed 'good ruler' face turning stubborn, "
            "medium well-kept beard, tight mouth, proud rigid eyes, upright noble-warrior build not barbaric, "
            "Former Qin ornate ochre-gold armor and cloak, raising a horsewhip toward a vast cold river, "
            "illusory countless whip silhouettes over the current, huge army mass behind, "
            "warm gold light on armor but icy blue-gray water foreshadowing disaster, "
            "style: tragic hubris landscape of north China unifier"
        ),
    },
    "n-wei-xiaowen": {
        "order": 10,
        "event_zh": ["太和迁都", "胡骑解辫"],
        "event_label": "代表事",
        "scene_one_liner_zh": "皮肤白皙的青年鲜卑帝在洛阳城楼解辫换汉服。",
        "age_moment_zh": "约二十七（太和迁洛前后）",
        "appearance_level": "A/B",
        "appearance_sources_zh": [
            "A《魏书·高祖纪》：帝生而洁白，有异姿……绰然有君人之表",
            "B 鲜卑拓跋系——可保留轻度北族骨相，但太和汉化场景以解辫易服为视觉核",
        ],
        "appearance_zh": (
            "东亚青年男性，二十七上下；肤色明显白皙（生而洁白）；"
            "眉清，骨相端正秀挺，非粗豪武夫；"
            "半解的鲜卑辫、发丝散落；一手持汉式冠服；"
            "身形修长；服：胡服半卸、汉袍加身的过程态。"
        ),
        "style_faction_zh": "北风转中原礼；笳声渐隐的渐变滤镜。",
        "props_zh": "辫发、汉服、洛阳城阙、南迁车队",
        "mood_zh": "塞外→礼乐",
        "prompt": (
            "a young East Asian man about 27 of Xianbei-Tabgatch origin, notably fair pale skin, refined elegant bone structure, "
            "not a crude warrior face, slender tall body, mid-action of unbraiding northern braid hair, "
            "half northern steppe dress half putting on elegant Han-style court robes, "
            "standing on Luoyang city tower, migration caravan faint on the southern road below, "
            "cold northern wind meeting warm ritual lantern light, identity transformation made visible, "
            "style: gradient cultural-reform lyrical historical painting"
        ),
    },
    "sui-wen": {
        "order": 11,
        "event_zh": ["开皇灭陈", "混一戎夏"],
        "event_label": "代表事",
        "scene_one_liner_zh": "长上短下的沈深帝王，目光外射，立于大兴网格与灭陈江景之间。",
        "age_moment_zh": "约五十（开皇九年）",
        "appearance_level": "A",
        "appearance_sources_zh": [
            "A《隋书·高祖纪》：为人龙颜，额上有五柱入顶，目光外射，有文在手曰王。长上短下，沈深严重",
        ],
        "appearance_zh": (
            "东亚男性，五十左右；「龙颜」威重；额头有明显纵向骨棱感（五柱入顶）；"
            "目光极亮、外射有神，令人不敢狎；"
            "体型特征：上身偏长、下肢偏短（长上短下）；气质沈深严重；"
            "服：开皇间相对清俭的皂/深色帝袍，不走炀帝奢。"
        ),
        "style_faction_zh": "隋文制度青灰；网格都城+江上舰队。",
        "props_zh": "大兴规划网格、长江舰队、建康降旗",
        "mood_zh": "清俭冷色",
        "prompt": (
            "an East Asian man about 50, heavy dragon-like authoritative face, forehead with five vertical bone ridges rising into the hairline, "
            "extremely piercing outward-shooting eyes, serious deep personality, "
            "distinct body proportion: longer upper torso and shorter legs (long-above short-below), "
            "frugal dark Sui imperial robe not luxurious, "
            "standing above a geometric plan-vision of Daxing city grid while Yangtze war fleet sails toward Jiankang with a falling banner, "
            "cool blue-gray institutional light, reunification as system not carnival, "
            "style: cold architectural-statecraft painting"
        ),
    },
    "sui-yang": {
        "order": 12,
        "event_zh": ["江都之变", "运河如带"],
        "event_label": "代表事",
        "scene_one_liner_zh": "美姿仪的中年帝王立龙舟头，盛装仍在，眼神已倦到死。",
        "age_moment_zh": "约四十五至五十（江都终局）",
        "appearance_level": "A/B",
        "appearance_sources_zh": [
            "A《隋书·炀帝纪》：上美姿仪，少敏慧……特所钟爱",
            "B 善文艺骑射传统记载——外形宜俊美而非魁梧莽夫；终局加疲态",
        ],
        "appearance_zh": (
            "东亚男性，近五十；史称美姿仪——五官端丽，眉目疏秀，曾是美少年帝王；"
            "此时眼窝微陷、法令纹深，英俊被疲惫腐蚀；须修整但仍整齐；"
            "体态仍修长，不横壮；"
            "服：大业极致华服/龙舟常服金碧，与背后夜刃对比。"
        ),
        "style_faction_zh": "运河绮丽切断为江都磷火。",
        "props_zh": "龙舟、运河玉带、冷刃、江都夜",
        "mood_zh": "金碧→磷火",
        "prompt": (
            "an East Asian man about 48, historically described as beautiful in appearance: refined handsome features, elegant brows and eyes, "
            "once radiant now hollow-eyed and exhausted, neat beard, slender graceful body not a brute, "
            "wearing extremely luxurious Sui imperial gold-and-turquoise dragon-boat attire, "
            "standing at the prow of a ornate dragon boat on a luminous grand canal like a jade belt from above, "
            "yet cold dagger glints and Jiangdu palace night shadows close in, split mood of infrastructure glory and murder doom, "
            "style: gorgeous-to-toxic color tragedy painting"
        ),
    },
    "tang-tai-zong": {
        "order": 13,
        "event_zh": ["天可汗", "贞观纳谏"],
        "event_label": "代表事",
        "scene_one_liner_zh": "虬须英主，龙凤姿，金甲未卸手握谏纸。",
        "age_moment_zh": "约三十五至四十（贞观盛时）",
        "appearance_level": "A/B（相学术语入史）",
        "appearance_sources_zh": [
            "A/B《旧唐书/新唐书》载书生相语：龙凤之姿，天日之表；民间/史传系统有「虬须」英武像",
            "B 弓马皇帝——体格健，眼神明锐",
        ],
        "appearance_zh": (
            "东亚男性，三十五至四十；天日之表：天庭饱满、气宇极开；"
            "虬须：须卷曲有力、英武；眉目如画而有杀气与英明并存；"
            "体格精悍善骑射；肤色健康；"
            "服：唐金明光甲可半卸，手持白色谏纸卷，非只亮兵器。"
        ),
        "style_faction_zh": "贞观明朗金石青；弓马与谏争光。",
        "props_zh": "谏纸、金甲、突厥倒旗、凌烟虚影",
        "mood_zh": "明朗顶格",
        "prompt": (
            "an East Asian man about 36-40, legendary 'dragon-phoenix bearing' and sun-like forehead presence, "
            "curly martial coiling beard (qiuxu), brilliant fierce-intelligent eyes, athletic archer-emperor body, healthy color, "
            "bright Tang golden armor partially worn, hands holding an open white remonstrance paper scroll instead of only a weapon, "
            "behind him collapsed northern steppe banners and faint ghostly meritorious ministers on a wall, "
            "clear Zhenguan daylight, balance of conquest and good governance, "
            "style: luminous High-Tang heroic-governance painting"
        ),
    },
    "zhou-wu-zetian": {
        "order": 14,
        "event_zh": ["天授称帝", "金轮称制"],
        "event_label": "代表事",
        "scene_one_liner_zh": "六十上下女帝冕旒端坐神都雾中，脸是权柄不是媚。",
        "age_moment_zh": "约六十六（天授元年 690）",
        "appearance_level": "C（本纪不细写五官；按年龄+女帝场景重建）",
        "appearance_sources_zh": [
            "C 两唐书武后纪不载具体眉目尺寸",
            "B 称帝时高龄——禁止画成年轻狐狸精；宜衰老仍压迫的女主权颜",
            "B 冕旒、袆衣、金轮象征",
        ],
        "appearance_zh": (
            "东亚女性，六十五上下；脸方圆有权，法令纹与眼袋可见；"
            "目光极稳极冷，无娇笑；唇薄；"
            "发已非青丝，冠冕下可见斑白；体态端，不纤弱；"
            "服：全套帝王冕服/龙袍系统，金轮光在背；严禁暴露宫斗造型。"
        ),
        "style_faction_zh": "神都紫金；纪念碑女帝。",
        "props_zh": "冕旒、金轮、洛阳紫雾",
        "mood_zh": "紫雾金轮",
        "prompt": (
            "an East Asian woman about 65-67 as sole female sovereign, square-powerful mature face with age lines, "
            "cold steady eyes, thin controlled lips, gray-streaked hair under full imperial mianguan crown, "
            "dignified heavy body posture not fragile, wearing complete male-style Chinese imperial dragon robes, "
            "great golden wheel mandala light behind her in purple mist of Luoyang, palace silhouettes, "
            "monumental sacred political power, absolutely not sensual harem beauty, "
            "style: purple-gold divine-capital monument portrait"
        ),
    },
    "tang-xian-zong": {
        "order": 15,
        "event_zh": ["元和削藩", "雪夜蔡州"],
        "event_label": "代表事",
        "scene_one_liner_zh": "中年清锐唐帝，指节按在藩镇图上，烛影削薄他的脸。",
        "age_moment_zh": "约四十（元和削藩高潮）",
        "appearance_level": "C",
        "appearance_sources_zh": [
            "C《旧唐书·宪宗纪》无细貌",
            "B 中晚唐中兴之主——宜清瘦锐利、有夜谈军国的青影",
        ],
        "appearance_zh": (
            "东亚男性，四十上下；脸偏瘦长，眉紧，眼有血丝；"
            "须短而黑；下颌紧；"
            "体型偏文吏而有决断肩背；"
            "服：深色常朝服/缋，大明宫夜，无华丽游行感。"
        ),
        "style_faction_zh": "中晚唐冷硬夜色；雪青+烛红。",
        "props_zh": "藩镇地图、烛、雪夜蔡州叠影",
        "mood_zh": "冷硬削藩",
        "prompt": (
            "an East Asian man about 40, lean elongated face, tight brows, bloodshot determined eyes, short dark beard, "
            "thin intense jaw, civil-military hybrid build, "
            "dark late-Tang court robe in Daming Palace night chamber, finger pressing a military map of rebel provinces, "
            "candlelight carving his face thin, double-exposure of snowy night assault on a southern city wall, "
            "sparse hard atmosphere of mid-Tang restoration, style: cold candlelit strategy painting"
        ),
    },
    "zhou-shi": {
        "order": 16,
        "event_zh": ["高平之战", "显德振旅"],
        "event_label": "代表事",
        "scene_one_liner_zh": "三十出头的青年英主，甲不离身，高平坡上目光如火。",
        "age_moment_zh": "约三十三四（高平 954）",
        "appearance_level": "C",
        "appearance_sources_zh": [
            "C 正史缺细貌；显德元年三十余，以谨厚被养为子",
            "B 五代亲征英主——年轻、精悍、风尘仆仆",
        ],
        "appearance_zh": (
            "东亚男性，三十三四；脸方而英，眉竖，眼神狠而正；"
            "须不长，短髭；满面征尘；"
            "体格精悍，行动感强；"
            "服：玄黑银边甲，战袍撕裂边缘可有，永不儒服端坐。"
        ),
        "style_faction_zh": "五代短促燃烧；秋草战旗。",
        "props_zh": "高平坡、战旗、溃兵、禁军",
        "mood_zh": "燃",
        "prompt": (
            "an East Asian man about 33-34, square heroic young face, upright fierce righteous eyes, short stubble beard, "
            "dust of battle on skin, compact explosive athletic body always in armor, "
            "black-and-silver Chinese Five-Dynasties armor, "
            "on Gaoping battlefield slope rallying troops and striking down fleeing cowards, blood-red banners, autumn grass and smoke, "
            "short brilliant martial life energy, style: high-action short-burn war painting"
        ),
    },
    "n-tang-houzhu": {
        "order": 17,
        "event_zh": ["975城破", "江南残梦"],
        "event_label": "代表事",
        "scene_one_liner_zh": "文士肩的中年南唐国主倚雨窗，眉目秀而软，全无武人骨。",
        "age_moment_zh": "约三十八九（975城破）",
        "appearance_level": "B/C",
        "appearance_sources_zh": [
            "B 史传与文学传统：工书善画、词人皇帝——外形宜秀弱文士",
            "C 正史缺严格五官尺寸；禁画成横刀武将",
        ],
        "appearance_zh": (
            "东亚男性，三十八九；脸清秀偏软，眉目如画而愁；"
            "无须或仅淡髭；肤白；肩窄，指长染墨；"
            "体态文弱，站如文人不是将军；"
            "服：南唐细布袍、软巾，雨湿贴身。"
        ),
        "style_faction_zh": "江南水墨湿冷；月白黛青。",
        "props_zh": "雨窗、空白纸绢、秦淮火光",
        "mood_zh": "残梦",
        "prompt": (
            "an East Asian man about 38-39, soft refined scholar face, painted melancholy brows and eyes, little or no beard, "
            "pale skin, narrow literary shoulders, long ink-stained fingers, weak unmilitary posture, "
            "Southern Tang fine cloth robe and soft headcloth wet with rain, "
            "leaning by a rainy night window in Jinling, blank paper and ink without readable characters, "
            "distant city-fall fire reflecting on river water, wet ink-wash blue-gray palette, "
            "style: Jiangnan tragic literati watercolor"
        ),
    },
    "n-song-tai-zu": {
        "order": 18,
        "event_zh": ["杯酒释兵权", "烛宴"],
        "event_label": "代表事",
        "scene_one_liner_zh": "隆准龙颜的中年军人皇帝，笑着劝酒，眼里全是算计的温柔。",
        "age_moment_zh": "约三十四五（杯酒释兵权传统系年）",
        "appearance_level": "A",
        "appearance_sources_zh": [
            "A《宋史·太祖纪》：及长，隆准龙颜，望之知为大人，俨如也",
        ],
        "appearance_zh": (
            "东亚男性，三十四上下；高鼻梁（隆准）；龙颜威重，远望即知非常人；"
            "脸堂堂，笑时和气但眼底冷静；须中等；"
            "体格军人出身仍壮；"
            "服：宋初帝常服/绛袍，宴席便装感，不必满身大驾卤簿。"
        ),
        "style_faction_zh": "烛金酒赤；温柔一刀的室内剧。",
        "props_zh": "酒盏、长案、卸甲将领、门外黄袍虚影",
        "mood_zh": "烛宴",
        "prompt": (
            "an East Asian man about 34, high nose bridge, dragon-like imposing face that looks non-ordinary even from afar, "
            "friendly smile with cold calculating eyes, medium beard, strong former-general body, "
            "early Northern Song imperial banquet dress in deep red and dark silk, "
            "smiling while offering wine cups to senior generals at candlelit long table, generals removing armor behind, "
            "soft gold candlelight, faint yellow-robe silhouette outside the door, intimate political soft power, "
            "style: candlelit interior political still"
        ),
    },
    "yuan-shi-zu": {
        "order": 19,
        "event_zh": ["1279灭宋", "混一车书"],
        "event_label": "代表事",
        "scene_one_liner_zh": "六十上下蒙古大汗兼汉地皇帝，方阔脸，混一服制立于大都与草原之间。",
        "age_moment_zh": "约六十四（1279崖山）",
        "appearance_level": "B/C",
        "appearance_sources_zh": [
            "B《元史·世祖纪》：及长，仁明英睿……无细五官",
            "B 蒙古皇族——方阔脸、目深、体硕的北族感 + 汉地帝服元素混搭（重建）",
        ],
        "appearance_zh": (
            "蒙古族老年男性，六十中后；脸宽阔，颧高，目较深，唇厚；"
            "须花白稀疏；体格厚重；"
            "肤色偏红褐风霜；"
            "服：蒙古冠帽元素 + 汉地龙袍/织金锦混一，体现「混一车书」。"
        ),
        "style_faction_zh": "欧亚帝国尺度；蒙古蓝+宫红。",
        "props_zh": "大都中轴、草原云、崖山远浪、驿马光迹",
        "mood_zh": "混一",
        "prompt": (
            "an elderly Mongol man about 64, broad square face, high cheekbones, deeper-set eyes, thick lips, "
            "sparse graying beard, heavy solid body, weather-reddened skin, "
            "mixed regalia: Mongol hat elements plus Chinese imperial dragon-robe gold brocade (unified empire dress), "
            "standing where Dadu city axis meets open steppe wind, far southern sea waves swallowing Song banners, "
            "relay-horse light trails of empire networks, Mongol blue sky and palace red accents, "
            "style: vast Eurasian unification panorama"
        ),
    },
    "n-wei-taiwu": {
        "order": 20,
        "event_zh": ["灭北凉", "真君铁骑"],
        "event_label": "代表事",
        "scene_one_liner_zh": "体貌瓌异的壮年鲜卑武帝，铁骑雪原，脸是征服不是礼。",
        "age_moment_zh": "约三十五至四十（灭北凉 439）",
        "appearance_level": "A/B",
        "appearance_sources_zh": [
            "A《魏书·世祖纪》：体貌瓌异，太祖奇而悦之",
            "B 鲜卑铁骑皇帝——魁伟、风霜、杀气",
        ],
        "appearance_zh": (
            "东亚/鲜卑男性，三十五至四十；体貌瓌异：骨架大、气势压人；"
            "脸方阔，眉浓，眼凶亮；须密；"
            "肤色风雪粗；"
            "服：北魏重甲、披毛领，马高于画面比例。"
        ),
        "style_faction_zh": "真君铁青雪原；粗粝武巅峰。",
        "props_zh": "铁骑、雪、城破烟、碎铃远意象",
        "mood_zh": "铁骑",
        "prompt": (
            "a Xianbei East Asian man about 36-40, extraordinary huge powerful physique (body described as rare and imposing), "
            "broad fierce face, thick brows, bright predatory eyes, dense beard, wind-and-snow rough skin, "
            "heavy Northern Wei iron cavalry armor with fur collar, "
            "leading iron horsemen flooding a desert fortress gate in winter light, smoke and snow, "
            "iron-blue palette, distant cracked temple bells as quiet religious-persecution hint without gore focus, "
            "style: raw cold cavalry-unification epic"
        ),
    },
}
