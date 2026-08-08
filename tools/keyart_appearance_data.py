# -*- coding: utf-8 -*-
"""
video-01 Key Art 造型总表 v3
每项强制拆开：外貌 | 冠服 | 饰品道具 | 背景空间 | 画风
史证：A 明文 / B 制度·族属·纪年可限定 / C 无明文的时代合理重建（须标明）
英文 prompt 由各块拼接，自足描写，不靠认出人名。
"""

PREFIX = (
    "16:9 cinematic Chinese historical character-atlas key art, "
    "highly stylized semi-realistic painterly editorial illustration (not photo), "
    "cohesive hand-painted historical graphic-novel rendering across the series, "
    "one clearly dominant emperor with at most indistinct contextual figures, "
    "historically grounded costume construction, one readable action, one dominant background motif, "
    "controlled depth, dramatic cinematic light, medium-wide hero framing, "
)

SUFFIX = (
    "the protagonist occupies 45 to 60 percent of frame height and the face stays in the central picture area, "
    "keep the lower-left 30 by 38 percent visually quiet and dark with no face hands or weapons for a radar overlay, "
    "keep the upper-right 25 percent clean and darker for Chinese titles, "
    "no readable text no letters no Chinese characters no UI no watermark no logo, "
    "no modern objects, no European plate armor, no celebrity face, "
    "accurate ancient East Asian tailoring, masterpiece"
)

NEGATIVE = (
    "text, letters, Chinese characters, watermark, logo, UI, radar, "
    "modern clothes, suit, jeans, sneakers, glasses, guns, cars, neon, cyberpunk, "
    "European medieval plate armor, Roman toga, Japanese samurai armor, "
    "chibi, idol face, crowded composition, multiple focal characters, cropped head, "
    "extra fingers, deformed anatomy, blurry, lowres, "
    "wrong dynasty bright plastic costume"
)


def P(
    order,
    event_zh,
    age_moment_zh,
    appearance_level,
    appearance_sources_zh,
    appearance_zh,
    costume_level,
    costume_sources_zh,
    costume_zh,
    accessories_zh,
    background_zh,
    style_faction_zh,
    mood_zh,
    scene_one_liner_zh,
    # English blocks for assembly
    en_who,
    en_face_body,
    en_costume,
    en_accessories,
    en_pose,
    en_background,
    en_style,
    event_label="代表事",
):
    prompt = (
        f"{en_who}, {en_face_body}, "
        f"COSTUME: {en_costume}, "
        f"ACCESSORIES AND PROPS: {en_accessories}, "
        f"POSE: {en_pose}, "
        f"BACKGROUND SET: {en_background}, "
        f"ART DIRECTION: {en_style}"
    )
    return {
        "order": order,
        "event_zh": event_zh,
        "event_label": event_label,
        "scene_one_liner_zh": scene_one_liner_zh,
        "age_moment_zh": age_moment_zh,
        "appearance_level": appearance_level,
        "appearance_sources_zh": appearance_sources_zh,
        "appearance_zh": appearance_zh,
        "costume_level": costume_level,
        "costume_sources_zh": costume_sources_zh,
        "costume_zh": costume_zh,
        "accessories_zh": accessories_zh,
        "background_zh": background_zh,
        "style_faction_zh": style_faction_zh,
        "mood_zh": mood_zh,
        "props_zh": accessories_zh,  # back-compat
        "prompt": prompt,
    }


SCENES = {
    # ------------------------------------------------------------------
    "qin-shi-huang": P(
        order=1,
        event_zh=["前221称帝", "书同文·车同轨"],
        age_moment_zh="约四十（前221）",
        appearance_level="A/B",
        appearance_sources_zh=[
            "A《史记·秦始皇本纪》尉缭：蜂准、长目、挚鸟膺、豺声",
            "B 同纪：水德，衣服旄旌节旗皆上黑；数以六为纪",
        ],
        appearance_zh="蜂准长目，精瘦中年，少恩薄唇，短髭或无须，冷白肤，猛禽般肩背。",
        costume_level="A/B",
        costume_sources_zh=[
            "A/B 水德尚黑：袍、旗、节以玄黑为主",
            "B 秦皇冠服系统：高冠（通天/远游想象）、玄衣纁裳传统向简化为玄衣金缘",
            "B 不用汉以后大红龙袍脸谱",
        ],
        costume_zh=(
            "【冠】高耸玄黑漆冠，冠梁挺直，无华丽珠旒堆砌（秦冷制）。"
            "【衣】通体玄黑宽袖袍，仅极窄鎏金缘；内层深灰中衣隐约可见；腰大带黑色。"
            "【履】翘头黑舄。"
            "【禁】朱红汉袍、清代朝珠、欧式披风。"
        ),
        accessories_zh=(
            "权（青铜权）与方形量器；成捆竹简；黑旌旗（六为纪可暗示旗幅比例）；"
            "玉具或素带钩低调；手不持长剑为主——权力在制度器物。"
        ),
        background_zh=(
            "咸阳宫高台，中轴对称夯土+木构斗拱剪影；远景六国旧色地图块熄灭收成玄金一统；"
            "晨雾冷、地平线干净；地面青石与漆反射。"
        ),
        style_faction_zh="秦水德纪念碑：玄黑+冷金+对称；制度感，拒绝暖红热闹。",
        mood_zh="冷硬、度量、压迫",
        scene_one_liner_zh="黑冠玄衣的中年秦王立在咸阳中轴高台，权量竹简在脚边。",
        en_who="a stern East Asian man about 40, Qin unifier king-emperor type",
        en_face_body=(
            "sharp high beak-like nose, long narrow piercing eyes, thin hard lips, "
            "lean wiry body, slightly raptor-hunched shoulders, cold pale skin, sparse short facial hair"
        ),
        en_costume=(
            "tall rigid black lacquer ceremonial crown without hanging pearl strings, "
            "full black wide-sleeve Warring-States/Qin robe with only razor-thin gold edge, "
            "dark gray inner layer, black large sash belt, black upturned ceremonial shoes, "
            "NO bright red Han dragon robe, NO Qing court beads"
        ),
        en_accessories=(
            "bronze weight and measuring vessels, stacked bamboo slips, black ritual banners, "
            "simple jade belt-hook, hands empty of sword or near the measuring tools"
        ),
        en_pose="standing alone centered on a high terrace as if measuring the world, frontal monumental stance",
        en_background=(
            "symmetrical Xianyang palace terrace of rammed earth and dark timber architecture, "
            "cold dawn fog, behind him six colored ancient-state map fragments collapsing into one dark-gold realm, "
            "stone floor with lacquer reflections"
        ),
        en_style="austere black-and-cold-gold seal-monument painting, extreme symmetry, institutional coldness",
    ),
    # ------------------------------------------------------------------
    "han-xuan-di": P(
        order=2,
        event_zh=["地节亲政", "综核名实"],
        age_moment_zh="约三十余（地节）",
        appearance_level="C",
        appearance_sources_zh=["C 本纪无细貌；B 长于民间→神态市井洞察"],
        appearance_zh="清瘦中年，颧骨显，短须整齐，锐眼熬夜感，非肥环龙颜。",
        costume_level="B",
        costume_sources_zh=[
            "B 西汉中期冕服/常朝：进贤冠或介帻、深衣袍、佩绶",
            "B 宣帝务实形象：冠服整洁但少奢金玉堆砌",
        ],
        costume_zh=(
            "【冠】黑色进贤冠（梁冠），简。"
            "【衣】深褐/皂色曲裾或直裾深衣，领袖缘暗红极窄；内中衣本白。"
            "【带】革带+绶（青紫系低饱和）；"
            "【禁】金光闪闪龙袍满身、明清补服。"
        ),
        accessories_zh="朱笔、满案竹简木牍、油灯、简册绳、铜印绶在腰侧可隐；无长兵器。",
        background_zh="未央宫夜殿内部：藻井与柱列在暗处；灯火暖而空间冷；远门外隐约长安街市虚影（其出身）。",
        style_faction_zh="西汉吏治暖灰：案牍、朱砂、油灯，办公美学。",
        mood_zh="核名实、冷静",
        scene_one_liner_zh="皂袍进贤冠的清瘦皇帝在竹简山前落朱笔。",
        en_who="an East Asian man mid-thirties, Western-Han auditing emperor type",
        en_face_body="lean face, visible cheekbones, sharp inspector eyes, slight sleepless shadows, neat short beard, slender build",
        en_costume=(
            "black Western-Han jinxian guan, a tall narrow ribbed cloth-and-lacquer cap with no long horizontal wings, "
            "dark brown or sooty deep-robe with tiny dark-red trim, plain white inner collar, "
            "leather belt with muted sash cords, modest not gaudy"
        ),
        en_accessories="red-ink brush mid-stroke, mountain of bamboo slips and wooden tablets, oil lamp, rope-bound archives, small seal cord at waist, no weapons",
        en_pose="standing or half-seated at a document table, body lean forward checking slips",
        en_background="night interior of Weiyang Palace halls, dark pillars, warm lamp pool, faint misty memory of common street life beyond the door",
        en_style="muted warm-gray bureaucratic drama painting, paper dust atmosphere",
    ),
    # ------------------------------------------------------------------
    "han-wu-di": P(
        order=3,
        event_zh=["漠北决战", "霍去病封狼居胥"],
        age_moment_zh="约三十八（元狩四年/前119）",
        appearance_level="C",
        appearance_sources_zh=[
            "C 本纪无细貌；按前119年年龄作盛年雄主重建",
            "A/B 漠北主帅为卫青、霍去病；汉武帝未亲临狼居胥",
        ],
        appearance_zh="三十八岁盛年，阔脸浓眉，短须整齐，肩宽，神情进取而强硬。",
        costume_level="B",
        costume_sources_zh=[
            "B 西汉皇帝军议可用绛袍、武冠与轻甲元素，不作前线骑将装扮",
            "B 禁欧式板甲、明清大铠脸谱",
        ],
        costume_zh=(
            "【衣】深绛色西汉宽袖袍，玄缘，外加克制的轻札甲肩护；"
            "【冠】黑色武冠，不戴前线兜鍪；"
            "【带】革带与低饱和绶；"
            "【禁】把皇帝画成亲临狼居胥的骑将。"
        ),
        accessories_zh="漠北军图、虎符、印玺、搁置的环首刀；远景汉旌与骑兵仅作战略意象。",
        background_zh="帝国军议高台或行殿；远处以象征性画面呈现卫青、霍去病铁骑进入漠北与狼居胥山影。",
        style_faction_zh="西汉漠北史诗：沙金+朱红，油彩颗粒。",
        mood_zh="雄开、决断",
        scene_one_liner_zh="盛年汉武帝在军案前下令，远景霍去病铁骑奔向狼居胥。",
        en_who="an East Asian man about 38, Western-Han emperor directing the Mobei campaign from an imperial war council",
        en_face_body="broad mature face, thick brows, neat short beard, strong wide shoulders, alert forceful eyes",
        en_costume=(
            "deep crimson Western-Han wide-sleeve court robe with black trim, restrained dark lamellar shoulder guards, "
            "black martial cap, leather belt and muted sash cords, NOT dressed as a frontline cavalry general"
        ),
        en_accessories="Mobei campaign map, tiger tally, imperial seal, resting Chinese ring-pommel sword, Han standards",
        en_pose="standing at a campaign table, one hand pressing the northern route on the map, the other holding a tiger tally",
        en_background=(
            "imperial campaign pavilion opening onto a clearly symbolic distant vision of Han cavalry led by generals, "
            "a dark Langjuxu mountain silhouette far beyond, sand-gold light under a cold blue sky"
        ),
        en_style="dusty epic strategic panorama, crimson and sand-gold oil-paint grain",
    ),
    # ------------------------------------------------------------------
    "xin-wang-mang": P(
        order=4,
        event_zh=["始建国元年", "托古改制"],
        age_moment_zh="约五十余（始建国）",
        appearance_level="B",
        appearance_sources_zh=["B《汉书》被服如儒生；外恭内深"],
        appearance_zh="五官端正过度，假笑眼不笑，齐整儒须，肩不武。",
        costume_level="B",
        costume_sources_zh=[
            "B 新朝托古：仿《周礼》冕服、韨、佩玉系统（示意级）",
            "B 对比脚边乱币：服越整齐，制越碎",
        ],
        costume_zh=(
            "【冠】冕板（前後延）或极考究的爵弁式；"
            "【衣】玄衣纁裳式仿古礼服，纹样繁而冷；蔽膝、大带齐全；"
            "【色】青黑绛搭配，拒绝喜庆金红堆；"
            "看似周公，实则新室。"
        ),
        accessories_zh="双手捧圭；满堂青铜礼器过亮；脚边错刀、契刀等乱币碎片；佩玉组缓。",
        background_zh="明堂/辟雍式建筑透视，柱列过满，光线惨白偏铜绿。",
        style_faction_zh="伪古典铜绿：礼器过精=政权虚。",
        mood_zh="端正的不安",
        scene_one_liner_zh="冕服捧圭的中年儒帝立在过亮礼器中间。",
        en_who="an East Asian man early fifties, usurper in perfect Confucian ritual dress",
        en_face_body="overly correct face, fixed smile not reaching eyes, neat Confucian beard, pale skin, thin non-martial shoulders",
        en_costume=(
            "archaic Zhou-imitating mian crown with flat top board, "
            "layered dark ceremonial robes with complex cold-colored patterns, knee-cover apron, large sash, "
            "hyper-correct ritual completeness"
        ),
        en_accessories="jade gui tablet held in both hands, too-clean bronze ritual vessels, broken knife-coins and failed currency shards at feet, jade pendants",
        en_pose="frontal formal standing like a ritual statue, slightly too perfect",
        en_background="cold bright Mingtang-like hall, excessive columns and ritual geometry, copper-green pale light",
        en_style="uncanny pseudo-antiquity still-life of power, beautiful and wrong",
    ),
    # ------------------------------------------------------------------
    "e-han-guangwu": P(
        order=5,
        event_zh=["昆阳之战", "以少击众"],
        age_moment_zh="约二十八九（昆阳）",
        appearance_level="A",
        appearance_sources_zh=["A《后汉书》：身长七尺三寸，美须眉，大口，隆准，日角"],
        appearance_zh="高大正脸青年，美须眉，大口隆准日角，雨水泥污。",
        costume_level="B",
        costume_sources_zh=["B 更始/新汉之际军容：皮甲/札甲、战袍", "B 此帧是战场非登基龙袍"],
        costume_zh=(
            "【甲】早期东汉皮甲/玄色札甲，泥浆开裂；"
            "【袍】甲下赭褐战袍；"
            "【冠】兜鍪歪斜或发髻湿乱；"
            "【禁】黄袍加身、云台功臣锦衣。"
        ),
        accessories_zh="长矛/环首刀；湿旗；缰绳；飞溅泥水。",
        background_zh="昆阳城墙雨幕，敌阵如潮，雷光白，少骑突击楔形。",
        style_faction_zh="中兴雨战脏镜头：水、泥、雷。",
        mood_zh="以少击众",
        scene_one_liner_zh="泥甲湿须的高大青年在雷雨里冲锋。",
        en_who="a tall East Asian man 28-29, Eastern-Han restoration war leader",
        en_face_body=(
            "above-average height, thick handsome brows and beard, wide mouth, high nose, "
            "raised central forehead bone boss, athletic body, rain-soaked muddy face"
        ),
        en_costume=(
            "early Eastern-Han leather and dark lamellar armor caked with mud and rain, "
            "brown war robe under armor, helmet askew or wet hair bun, battlefield filth, "
            "NOT coronation dragon robe"
        ),
        en_accessories="spear or ring-pommel sword, soaked battle flag, reins, flying mud droplets",
        en_pose="horse charge spearhead through rain, body leaning into storm",
        en_background="Kunyang city walls in torrential rain, vast dark enemy tide, white lightning, small cavalry wedge",
        en_style="wet dirty heroic storm painting, high motion blur on rain",
    ),
    # ------------------------------------------------------------------
    "h-zhao-shi-le": P(
        order=6,
        event_zh=["襄国称赵", "奴隶天子"],
        age_moment_zh="约五十（称赵/帝）",
        appearance_level="A/B",
        appearance_sources_zh=["A/B《晋书》羯人、胡雏、壮健雄武、状貌奇异"],
        appearance_zh="深目高颧，虬须，肤深，横壮，腕有锁痕。",
        costume_level="B/C",
        costume_sources_zh=["B 十六国胡汉杂糅甲胄；C 夯土宫廷粗服"],
        costume_zh=(
            "【甲/袍】半甲半袍：铁片甲+粗毛布长袍；"
            "【冠】简易帝王冠或皮弁式，不精工；"
            "【质】锈、补丁、风沙磨损；"
            "【禁】南宋精工龙袍。"
        ),
        accessories_zh="腕间断铁链；粗柄剑；赵字军旗；夯土殿粗糙扶手。",
        background_zh="襄国夯土城垒，黄尘，旗升，天空干裂感。",
        style_faction_zh="十六国铁锈风沙：阶级逆袭粗粝。",
        mood_zh="奴隶→天子",
        scene_one_liner_zh="断链壮汉坐在夯土王座上。",
        en_who="a rugged middle-aged Jie-related northern man about 50",
        en_face_body="deep-set eyes, high cheekbones, higher nose, coarse curly beard, darker weather skin, broad slave-built body, chain scars on wrists",
        en_costume=(
            "mixed Hu-Han armor: iron plates over coarse wool robe, rough simple crown or leather cap, "
            "rust patches and sand wear, not refined southern silk dragon robe"
        ),
        en_accessories="broken iron slave chains on wrists, heavy crude sword, Zhao battle banner, rough rammed-earth throne arms",
        en_pose="seated or rising on crude throne, chains falling, chin high",
        en_background="rammed-earth fortress of Xiangguo, dusty yellow wind, dry sky, banner rising",
        en_style="harsh rust-and-dust fortress painting, class-ascent epic",
    ),
    # ------------------------------------------------------------------
    "liang-wu": P(
        order=7,
        event_zh=["舍身同泰", "侯景将至"],
        age_moment_zh="约七十余（舍身年段）",
        appearance_level="A/B",
        appearance_sources_zh=["A《梁书》顶上隆起等；B 蔬食佞佛→清癯"],
        appearance_zh="清癯老脸，白须，顶骨隆，瘦。",
        costume_level="B",
        costume_sources_zh=["B 梁帝通天冠服+佛事袈裟叠穿（舍身名场面）"],
        costume_zh=(
            "【外】土黄/藕荷色袈裟斜披；"
            "【内】梁代帝袍（绛/紫系可低饱和）仍在；"
            "【冠】通天冠或佛事时免冠见白发；"
            "金粉沾衣。"
        ),
        accessories_zh="念珠；金佛脚前钱山（赎身）；香炉青烟；远处甲骑反光。",
        background_zh="同泰寺大殿金佛巨像；梁柱飞檐南朝细；门外建康天际已有烟尘。",
        style_faction_zh="南朝金粉佛光+腐朽灰边。",
        mood_zh="舍身与将乱",
        scene_one_liner_zh="袈裟压帝袍的清瘦老帝立在金佛与钱山前。",
        en_who="an East Asian man 70-75, Southern Liang Buddhist emperor",
        en_face_body="gaunt aged face, white drooping beard, raised bony skull crown, thin ascetic body",
        en_costume=(
            "Buddhist kasaya in dusty gold-lotus tones draped over Liang imperial robes, "
            "tongtian crown or bare gray hair under temple light, gold leaf dust on fabric"
        ),
        en_accessories="prayer beads, mountain of ransom coins before Buddha, incense smoke, distant glint of armor outside",
        en_pose="devout standing before colossal Buddha, hands in dedication gesture",
        en_background="Tongtai Temple interior, huge golden Buddha, refined Southern-dynasty timber hall, gray cavalry smoke beyond the gate",
        en_style="gilded Buddhist tragedy, gold versus ash",
    ),
    # ------------------------------------------------------------------
    "xixia-li-yuanhao": P(
        order=8,
        event_zh=["1038称帝", "河西立国"],
        age_moment_zh="约三十五（1038）",
        appearance_level="A",
        appearance_sources_zh=["A《宋史·夏国传》圆面高准，身长五尺余；长袖绯衣，冠黑冠，佩弓矢"],
        appearance_zh="偏矮，圆面高鼻，鹰目，精悍。",
        costume_level="A",
        costume_sources_zh=["A 明文绯衣黑冠；B 党项发式/服饰去宋化（示意）"],
        costume_zh=(
            "【衣】长袖绯（大红/朱红）袍，袖肥而长；"
            "【冠】黑冠（圆顶/平顶党项式，勿宋进贤）；"
            "【腰】革带；"
            "【禁】宋朝官服、龙袍满绣。"
        ),
        accessories_zh="弓、矢、箭袋；青盖意象可远；西夏文抽象纹样光（不可辨认字形）。",
        background_zh="兴庆城墙+贺兰山硬轮廓；河西硬光；砂金与藏青对比。",
        style_faction_zh="西夏民族国家硬光：砂金藏青。",
        mood_zh="称制自立",
        scene_one_liner_zh="黑冠绯袖矮壮君主立在贺兰风里。",
        en_who="a short Tangut East Asian man about 35",
        en_face_body="short stature, round face, high nose bridge, hawk eyes, compact athletic body, short facial hair",
        en_costume=(
            "long-sleeved bright crimson robe with long full sleeves, black Tangut-style crown-cap, "
            "leather belt, NOT Song Chinese civil official robe"
        ),
        en_accessories="bow, arrows, quiver at belt, distant blue canopy suggestion, abstract unreadable Tangut-glyph light patterns",
        en_pose="standing on fortress battlement facing desert wind, chin set",
        en_background="Xingqing fortress walls under Helan Mountains, hard desert sunlight, sand-gold and deep navy palette",
        en_style="hard-light Hexi national founding painting",
    ),
    # ------------------------------------------------------------------
    "q-qin-fu-jian": P(
        order=9,
        event_zh=["投鞭断流", "淝水将败"],
        age_moment_zh="约四十五（383）",
        appearance_level="C",
        appearance_sources_zh=["C 无细貌；B 氐秦共主、盛极转刚愎"],
        appearance_zh="堂堂明君骨相转执拗，中须，体中上。",
        costume_level="B/C",
        costume_sources_zh=["B 十六国帝王甲+披风；C 前秦金赭色系"],
        costume_zh=(
            "【甲】金赭鱼鳞/札甲，精细于石勒；"
            "【披】赭金披风；"
            "【冠】帝王兜鍪或冠；"
            "盛时装，不是败逃破衣（败兆在江水颜色）。"
        ),
        accessories_zh="马鞭高扬；佩剑；身后密密兵器林；江面幻觉鞭影。",
        background_zh="大江天堑（淝水/长江意象），金光在甲、冷灰在水；东岸薄雾。",
        style_faction_zh="盛极金光切冷江：悲剧骄兵。",
        mood_zh="投鞭",
        scene_one_liner_zh="金甲帝王扬鞭指着冷色大江。",
        en_who="an East Asian man about 45, Former Qin Di northern ruler",
        en_face_body="open-browed once-handsome face turning stubborn, medium neat beard, tight mouth, upright noble build",
        en_costume="ornate ochre-gold Former Qin lamellar armor, matching cloak, imperial helmet-crown, polished still-proud metal",
        en_accessories="raised horsewhip, sword, forest of spears behind, illusory whip silhouettes over the river",
        en_pose="on high riverbank, arm extended whip toward water, tragic pride",
        en_background="vast cold blue-gray river, gold light only on armor, mist on far bank, huge army mass",
        en_style="tragic hubris landscape, gold cut by cold water",
    ),
    # ------------------------------------------------------------------
    "n-wei-xiaowen": P(
        order=10,
        event_zh=["太和迁都", "胡骑解辫"],
        age_moment_zh="约二十七（太和迁洛）",
        appearance_level="A/B",
        appearance_sources_zh=["A《魏书》生而洁白有异姿"],
        appearance_zh="白皙青年，秀挺骨相，发式已整为汉式高髻，神情坚决。",
        costume_level="B",
        costume_sources_zh=["B 太和服制改革：禁胡服、着汉衣冠——画面用「换装过程」"],
        costume_zh=(
            "【身上】完整连贯的绛红汉式宽袖朝服与简化进贤冠；"
            "【旧服】鲜卑窄袖骑装与蹀躞带折叠搭在城楼栏杆，不与身上服装拼接；"
            "色彩从背景苍褐过渡到人物绛红。"
        ),
        accessories_zh="解下的辫绳置于手中；折叠胡服；南迁车队铃；洛阳城砖。",
        background_zh="洛阳新建宫阙城楼；官道车队向南；北风与礼乐灯同时存在。",
        style_faction_zh="胡汉渐变滤镜：笳→雅乐。",
        mood_zh="解辫更张",
        scene_one_liner_zh="白皙青年已着完整汉服立于洛阳城楼，手中握着解下的辫绳。",
        en_who="a fair young Xianbei East Asian man about 27",
        en_face_body="notably pale fair skin, refined elegant bones, slender tall body, hair already arranged in a coherent Han-style topknot",
        en_costume=(
            "one fully coherent ritual-crimson Han-style wide-sleeve court robe and a simplified jinxian cap, "
            "an old northern Xianbei narrow-sleeve riding coat and belt folded over the stone parapet, never split across his body"
        ),
        en_accessories="removed braid cord held in one hand, folded riding coat, distant cart bells of southern migration, Luoyang bricks",
        en_pose="standing on a city tower in completed new court dress, looking south while holding the removed braid cord",
        en_background="Luoyang palace towers, official road with migration caravan southward, cold wind meets lantern ritual light",
        en_style="gradient cultural-reform lyrical painting, old and new dress separated cleanly between figure and prop",
    ),
    # ------------------------------------------------------------------
    "sui-wen": P(
        order=11,
        event_zh=["开皇灭陈", "混一戎夏"],
        age_moment_zh="约五十（开皇九年）",
        appearance_level="A",
        appearance_sources_zh=["A《隋书》龙颜，五柱入顶，目光外射，长上短下"],
        appearance_zh="威重，额骨棱，目光外射，长上短下。",
        costume_level="B",
        costume_sources_zh=["B 开皇制度：通天冠、绛纱袍系统；史载节俭→少珠宝"],
        costume_zh=(
            "【冠】通天冠；"
            "【衣】深色/绛皂帝袍，裁剪合隋，少金玉堆；"
            "【带】大型绶；"
            "对比炀帝奢：此帧清俭。"
        ),
        accessories_zh="圭或无；背后大兴城规划网格光；江上舰队模型感远景。",
        background_zh="半实半图：大兴里坊网格+长江灭陈舰队+建康降帜。",
        style_faction_zh="制度青灰：建筑网格史诗。",
        mood_zh="混一",
        scene_one_liner_zh="清俭通天冠的长躯帝王立在都城网格与江景前。",
        en_who="an East Asian man about 50, Sui founding system-builder emperor",
        en_face_body="heavy authoritative face, five vertical forehead ridges, piercing outward eyes, longer torso shorter legs proportion",
        en_costume="tongtian crown, dark frugal Sui imperial robe with limited gold, large sash, modest jewelry",
        en_accessories="optional gui tablet, glowing city-grid diagram light, distant fleet silhouettes",
        en_pose="standing above geometric city plan, calm command",
        en_background="Daxing ward grid vision plus Yangtze campaign fleet and falling Jiankang banner, cool blue-gray light",
        en_style="cold architectural statecraft painting",
    ),
    # ------------------------------------------------------------------
    "sui-yang": P(
        order=12,
        event_zh=["江都之变", "运河如带"],
        age_moment_zh="约四十八（江都）",
        appearance_level="A/B",
        appearance_sources_zh=["A 美姿仪；B 大业极奢"],
        appearance_zh="曾极俊美，近五十疲态腐蚀英俊，修长。",
        costume_level="B",
        costume_sources_zh=["B 大业行幸：冕服/龙袍金碧、仙幢华饰；龙舟卤簿"],
        costume_zh=(
            "【衣】大业极致：金线龙纹袍、青绿缘；"
            "【冠】通天/远游高冠珠翠（可克制但华）；"
            "【质】织金、轻纱、反光强；"
            "与隋文清俭对打。"
        ),
        accessories_zh="龙舟阑干；羽扇或玉笏；背后运河；近景冷刃反光；酒器可有。",
        background_zh="俯瞰运河如玉带+近景龙舟舱；江都宫夜影压过来。",
        style_faction_zh="绮丽切断：金碧→磷火青。",
        mood_zh="壮美与杀机",
        scene_one_liner_zh="金碧龙舟上的倦帝，运河美，刃光近。",
        en_who="an East Asian man about 48, once-beautiful Sui touring emperor",
        en_face_body="refined handsome features now hollow-eyed exhausted, neat beard, slender graceful body",
        en_costume=(
            "extremely luxurious Sui imperial robe with gold dragon embroidery and turquoise trim, "
            "tall beaded crown, shimmering brocade, maximum splendor"
        ),
        en_accessories="dragon-boat rail, jade tablet or feather fan, wine vessel, cold dagger glint nearby",
        en_pose="standing at dragon-boat prow, weary upright",
        en_background="luminous grand canal like jade belt from above, Jiangdu palace night shadows closing in, toxic beauty",
        en_style="gorgeous-to-toxic color tragedy, gold versus murder blue",
    ),
    # ------------------------------------------------------------------
    "tang-tai-zong": P(
        order=13,
        event_zh=["天可汗", "贞观纳谏"],
        age_moment_zh="约三十六至四十（贞观盛）",
        appearance_level="A/B",
        appearance_sources_zh=["A/B 龙凤之姿天日之表；虬须传统"],
        appearance_zh="虬须英武，天庭开，精悍。",
        costume_level="B",
        costume_sources_zh=["B 唐初明光甲/山文甲系统；常朝亦可绛袍——本帧甲+谏纸"],
        costume_zh=(
            "【甲】唐金/石青明光甲，护心镜可有；"
            "【袍】甲上可披白袍或衔白色谏纸；"
            "【冠】兜鍪可卸置一旁，露发与虬须；"
            "【禁】宋以后补子官服。"
        ),
        accessories_zh="展开的白色谏书卷；弓；远处突厥旗倒；凌烟虚影壁。",
        background_zh="长安宫阙晴空；或便桥意象简化；日光硬朗。",
        style_faction_zh="贞观金石青：明朗顶格。",
        mood_zh="武与谏同光",
        scene_one_liner_zh="虬须金甲帝王手握谏纸立于晴光。",
        en_who="an East Asian man 36-40, early-Tang Zhenguan-era archer-emperor",
        en_face_body="dragon-phoenix bearing, sun-like open forehead, curly coiling martial beard, fierce-intelligent eyes, athletic body",
        en_costume=(
            "early Tang golden and stone-blue armor with chest mirrors, "
            "optional white cloak, helmet set aside, NOT Song rank-badge robes"
        ),
        en_accessories="open white remonstrance paper scroll in hands, bow, collapsed northern banners, faint meritorious-minister wall ghosts",
        en_pose="standing in clear daylight, armor on, paper forward as main prop",
        en_background="Chang'an palace under bright Zhenguan sun, clean heroic sky",
        en_style="luminous early-Tang Zhenguan heroic-governance painting",
    ),
    # ------------------------------------------------------------------
    "zhou-wu-zetian": P(
        order=14,
        event_zh=["天授称帝", "金轮称制"],
        age_moment_zh="约六十六（690）",
        appearance_level="C",
        appearance_sources_zh=["C 无细貌；B 女帝称制用皇帝冠服系统"],
        appearance_zh="六十五+方权脸，斑白，冷目，无媚态。",
        costume_level="B",
        costume_sources_zh=["B 武周皇帝冕服：冕旒、衮服，非后妃袆衣主视觉"],
        costume_zh=(
            "【冠】十二旒冕（女帝仍用皇帝冕）；"
            "【衣】深青/绛的衮冕龙纹；"
            "【禁】低胸宫装、狐媚披帛当主服。"
        ),
        accessories_zh="金轮法器光（背光）；圭；神都紫雾；无铜匦也可远。",
        background_zh="洛阳神都宫阙剪影，紫雾金轮，纪念碑构图。",
        style_faction_zh="神都紫金：女帝纪念碑。",
        mood_zh="称制",
        scene_one_liner_zh="冕旒衮服的老年女帝立在金轮紫雾中。",
        en_who="an East Asian woman 65-67 as sole female Chinese emperor",
        en_face_body="square powerful aged face, age lines, cold steady eyes, gray-streaked hair, dignified heavy posture",
        en_costume=(
            "full male-style imperial mian crown with hanging jade/pearl strings, "
            "dark blue and crimson dragon imperial robes, solemn not sensual, NO harem dress"
        ),
        en_accessories="golden wheel mandala backlight, gui tablet, purple mist, palace silhouettes",
        en_pose="frontal monument stance, absolute sovereignty",
        en_background="Luoyang divine capital silhouettes in purple fog, sacred political light",
        en_style="purple-gold divine-capital monument portrait",
    ),
    # ------------------------------------------------------------------
    "tang-xian-zong": P(
        order=15,
        event_zh=["元和削藩", "雪夜蔡州"],
        age_moment_zh="约四十（元和）",
        appearance_level="C",
        appearance_sources_zh=["C 无细貌"],
        appearance_zh="瘦长脸，紧眉血丝眼，短黑须。",
        costume_level="B",
        costume_sources_zh=["B 中晚唐常朝：襆头、圆领缺胯袍、蹀躞带"],
        costume_zh=(
            "【头】黑色硬脚襆头；"
            "【衣】深青/紫圆领缺胯袍；"
            "【带】蹀躞带（可挂小囊）；"
            "夜殿，无大朝会卤簿。"
        ),
        accessories_zh="手指按着藩镇地图钉；烛台；窗外雪；隐约甲士。",
        background_zh="大明宫夜室；地图墙；雪光与烛红对切；可叠蔡州城剪影。",
        style_faction_zh="中晚唐冷硬夜：烛红雪青。",
        mood_zh="鞭藩",
        scene_one_liner_zh="襆头圆领的中年唐帝在烛下按死地图上的藩镇。",
        en_who="an East Asian man about 40, late-Tang restoration emperor",
        en_face_body="lean elongated face, tight brows, bloodshot eyes, short dark beard, thin intense jaw",
        en_costume="black hard-winged futou headwear, dark blue or purple round-collar Tang robe with side slits, belt with small pouches",
        en_accessories="finger on military map with pins, candlesticks, snow light at window, faint armored guards",
        en_pose="leaning over map table at night, decisive press of finger",
        en_background="Daming Palace night chamber, map wall, candle red versus snow cyan, ghost image of snowy city assault",
        en_style="cold candlelit strategy painting",
    ),
    # ------------------------------------------------------------------
    "zhou-shi": P(
        order=16,
        event_zh=["高平之战", "显德振旅"],
        age_moment_zh="约三十三（高平）",
        appearance_level="C",
        appearance_sources_zh=["C 无细貌；B 五代亲征英主"],
        appearance_zh="方脸青年，竖眉短髭，满面征尘。",
        costume_level="B/C",
        costume_sources_zh=["B 五代禁军甲：玄甲银缘、战袍"],
        costume_zh=(
            "【甲】玄黑甲，银/铁边；"
            "【袍】战袍赤缘可裂；"
            "【盔】兜鍪系带；"
            "从头到脚可战，无儒服。"
        ),
        accessories_zh="马鞭/刀；军旗；禁军阵列；逃将背影。",
        background_zh="高平坡地秋草，烟尘，旗如血。",
        style_faction_zh="五代短燃战绘。",
        mood_zh="振旅",
        scene_one_liner_zh="玄甲青年皇帝在坡上重整溃兵。",
        en_who="an East Asian man 33-34, Five Dynasties young martial emperor",
        en_face_body="square heroic young face, upright fierce eyes, short stubble, battle dust on skin, compact explosive body",
        en_costume="black-and-silver Chinese Five-Dynasties full armor, red-trimmed war robe, tied helmet, ready to fight",
        en_accessories="sword or whip, blood-red banners, imperial guard ranks, fleeing coward silhouettes",
        en_pose="on slope rallying troops, dynamic stride",
        en_background="Gaoping autumn grass slope, smoke, wind, raw battlefield",
        en_style="high-action short-burn war painting",
    ),
    # ------------------------------------------------------------------
    "n-tang-houzhu": P(
        order=17,
        event_zh=["975城破", "江南残梦"],
        age_moment_zh="约三十八九（975）",
        appearance_level="B/C",
        appearance_sources_zh=["B 词人皇帝传统；C 无严格五官尺寸"],
        appearance_zh="秀软文士脸，淡髭或无须，肩窄指长。",
        costume_level="B/C",
        costume_sources_zh=["B 南唐文人帝服：软脚襆头/巾，细布袍，非甲"],
        costume_zh=(
            "【头】软巾或软脚襆头，雨湿；"
            "【衣】月白/黛青细布交领袍，薄；"
            "【履】软履；"
            "【禁】横刀金甲。"
        ),
        accessories_zh="空白纸绢与墨（勿显字）；窗棂；远处火光映水。",
        background_zh="金陵夜雨窗；秦淮水火倒影；水墨空间。",
        style_faction_zh="江南水墨湿冷。",
        mood_zh="残梦",
        scene_one_liner_zh="湿巾细袍的文士帝王倚在雨窗前。",
        en_who="an East Asian man 38-39, Southern Tang poet-emperor",
        en_face_body="soft refined scholar face, melancholy brows, little beard, pale skin, narrow shoulders, long ink-stained fingers",
        en_costume="soft rain-wet headcloth or soft futou, moon-white or blue-gray fine cloth cross-collar robe, soft shoes, NO armor",
        en_accessories="blank paper and ink without characters, window lattice, distant fire on water",
        en_pose="leaning by rainy window, literati posture",
        en_background="Jinling night rain, Qinhuai reflections of city fire, wet ink-wash space",
        en_style="Jiangnan tragic literati watercolor",
    ),
    # ------------------------------------------------------------------
    "n-song-tai-zu": P(
        order=18,
        event_zh=["杯酒释兵权", "烛宴"],
        age_moment_zh="约三十四（杯酒传统年）",
        appearance_level="A",
        appearance_sources_zh=["A《宋史》隆准龙颜"],
        appearance_zh="高鼻龙颜，笑里有算，军人肩背。",
        costume_level="B",
        costume_sources_zh=["B 宋初帝常服：幞头、绛纱/赤袍；宴饮便装感"],
        costume_zh=(
            "【头】硬脚幞头；"
            "【衣】赤/绛圆领袍，织纹克制；"
            "【带】金/犀带；"
            "不是大朝会冕服满身。"
        ),
        accessories_zh="酒盏连连；长案；对面卸甲的宿将；门外黄袍虚影一点。",
        background_zh="宫宴内室烛光；暖金；门缝夜色。",
        style_faction_zh="烛宴室内剧：温柔一刀。",
        mood_zh="释兵",
        scene_one_liner_zh="赤袍皇帝笑劝酒，将军们在卸甲。",
        en_who="an East Asian man about 34, early Song general-emperor",
        en_face_body="high nose, dragon-like imposing face, friendly smile with cold eyes, medium beard, strong general body",
        en_costume="hard-winged futou, restrained crimson round-collar early Song imperial robe, ornate belt, banquet dress not full mian ceremonial",
        en_accessories="wine cups offered, long table, generals removing armor, faint yellow robe silhouette outside door",
        en_pose="smiling toast gesture, soft body language over hard politics",
        en_background="candlelit palace banquet room, soft gold, dark doorway",
        en_style="candlelit interior political still",
    ),
    # ------------------------------------------------------------------
    "yuan-shi-zu": P(
        order=19,
        event_zh=["1279灭宋", "混一车书"],
        age_moment_zh="约六十四（崖山）",
        appearance_level="B/C",
        appearance_sources_zh=["B 蒙古皇族体貌传统+元帝质孙/汉地龙袍混一"],
        appearance_zh="宽脸深目，花白须，体厚，肤红褐。",
        costume_level="B",
        costume_sources_zh=["B 质孙（只孙）织金锦+汉地龙袍元素混搭；蒙古冠帽"],
        costume_zh=(
            "【帽】蒙古式冬帽/宝里冠元素；"
            "【衣】织金锦质孙袍 + 汉式龙纹缘；"
            "【色】蓝、银、宫红；"
            "体现混一，不是纯汉唐帝。"
        ),
        accessories_zh="玉带；驿马远影光迹；地图式行省色块可抽象。",
        background_zh="大都中轴建筑+草原云；远南方海浪吞旗（崖山）。",
        style_faction_zh="欧亚帝国全景：蒙古蓝宫红。",
        mood_zh="混一",
        scene_one_liner_zh="织金混一服的老年大汗立在大都与草原交界。",
        en_who="an elderly Mongol man about 64, Yuan universal ruler",
        en_face_body="broad square face, high cheekbones, deeper-set eyes, sparse gray beard, heavy body, weather-reddened skin",
        en_costume=(
            "Mongol-style hat elements plus gold-woven jisun robe with Chinese dragon-border motifs, "
            "blue silver and palace red, hybrid empire dress"
        ),
        en_accessories="jade belt, relay-horse light trails, abstract province color blocks",
        en_pose="standing where city axis meets steppe wind, vast scale",
        en_background="Dadu central axis architecture, open steppe clouds, far southern sea swallowing banners",
        en_style="vast Eurasian unification panorama",
    ),
    # ------------------------------------------------------------------
    "n-wei-taiwu": P(
        order=20,
        event_zh=["灭北凉", "真君铁骑"],
        age_moment_zh="约三十五至四十（439）",
        appearance_level="A/B",
        appearance_sources_zh=["A 体貌瓌异"],
        appearance_zh="魁伟瓌异，方脸凶目，密须，风雪肤。",
        costume_level="B",
        costume_sources_zh=["B 北魏重骑兵甲、毛领、马具"],
        costume_zh=(
            "【甲】北魏铁骑重甲，冷青铁色；"
            "【领】毛皮领；"
            "【盔】高兜鍪；"
            "全身可战。"
        ),
        accessories_zh="长矛；马；碎佛铃远意象；城破烟。",
        background_zh="雪原/河西城破；铁骑洪流；铁青天空。",
        style_faction_zh="真君铁青雪原武史诗。",
        mood_zh="铁骑统一",
        scene_one_liner_zh="毛领铁甲的壮帝率骑冲向城门。",
        en_who="a huge Xianbei East Asian man 36-40, Northern Wei cavalry emperor",
        en_face_body="extraordinary imposing physique, broad fierce face, thick brows, predatory eyes, dense beard, snow-rough skin",
        en_costume="heavy Northern Wei iron cavalry armor, fur collar, tall helmet, full war kit",
        en_accessories="lance, warhorse, distant cracked temple bells hint, fortress smoke",
        en_pose="leading charge at fortress gate, horse large in frame",
        en_background="winter light on northern fortress gate, iron horsemen flood, iron-blue sky, snow and smoke",
        en_style="raw cold cavalry-unification epic",
    ),
}
