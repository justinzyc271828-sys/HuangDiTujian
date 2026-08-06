#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成中国古代帝王索引总表（工作清单，可修订）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "catalog"
MD_OUT = ROOT / "docs" / "references" / "catalogs" / "皇帝索引总表.md"

# 字段: id, display, personal, dynasty_id, dynasty, seq, reign_start, reign_end, tier, note
# tier: emperor=正式收录主线/割据正史帝纪常见者; quasi=准; honorary=追尊/未入主表
# 说明: 本表为图鉴工作索引，边界争议条目见 note；人数会随修订变化。

def E(id, display, personal, dynasty_id, dynasty, seq, start, end, tier="emperor", note=""):
    return {
        "id": id,
        "display": display,
        "personal": personal,
        "dynasty_id": dynasty_id,
        "dynasty": dynasty,
        "sequence": seq,
        "reign_start": start,
        "reign_end": end,
        "tier": tier,
        "note": note,
        "page_status": "stub",  # stub | draft | ready
    }


EMPERORS: list[dict] = []

# —— 秦 ——
EMPERORS += [
    E("qin-shi-huang", "秦始皇", "嬴政", "qin", "秦", 1, "-221", "-210"),
    E("qin-er-shi", "秦二世", "胡亥", "qin", "秦", 2, "-210", "-207"),
    E("qin-zi-ying", "秦王子婴", "子婴", "qin", "秦", 3, "-207", "-207", "quasi", "未称帝号，或入准"),
]

# —— 西汉 ——
wh = [
    ("han-gao-zu", "汉高祖", "刘邦", 1, "-202", "-195"),
    ("han-hui-di", "汉惠帝", "刘盈", 2, "-195", "-188"),
    ("han-qian-shao", "前少帝", "刘恭", 3, "-188", "-184", "quasi", "吕后临朝，名分争议"),
    ("han-hou-shao", "后少帝", "刘弘", 4, "-184", "-180", "quasi", "吕后临朝"),
    ("han-wen-di", "汉文帝", "刘恒", 5, "-180", "-157"),
    ("han-jing-di", "汉景帝", "刘启", 6, "-157", "-141"),
    ("han-wu-di", "汉武帝", "刘彻", 7, "-141", "-87"),
    ("han-zhao-di", "汉昭帝", "刘弗陵", 8, "-87", "-74"),
    ("han-changyi", "昌邑王贺", "刘贺", 9, "-74", "-74", "quasi", "在位二十余日废"),
    ("han-xuan-di", "汉宣帝", "刘询", 10, "-74", "-49"),
    ("han-yuan-di", "汉元帝", "刘奭", 11, "-49", "-33"),
    ("han-cheng-di", "汉成帝", "刘骜", 12, "-33", "-7"),
    ("han-ai-di", "汉哀帝", "刘欣", 13, "-7", "-1"),
    ("han-ping-di", "汉平帝", "刘衎", 14, "-1", "5"),
    ("han-ruzi", "孺子婴", "刘婴", 15, "6", "8", "quasi", "王莽居摄"),
]
for row in wh:
    if len(row) == 6:
        id, d, p, s, a, b = row
        EMPERORS.append(E(id, d, p, "w-han", "西汉", s, a, b))
    elif len(row) == 7:
        id, d, p, s, a, b, t = row
        EMPERORS.append(E(id, d, p, "w-han", "西汉", s, a, b, t, ""))
    else:
        id, d, p, s, a, b, t, n = row
        EMPERORS.append(E(id, d, p, "w-han", "西汉", s, a, b, t, n))
EMPERORS.append(E("xin-wang-mang", "新朝王莽", "王莽", "xin", "新", 1, "9", "23", "quasi", "新朝；是否入正式线可开关"))

# —— 东汉 ——
eh = [
    ("e-han-guangwu", "汉光武帝", "刘秀", 1, "25", "57"),
    ("e-han-ming", "汉明帝", "刘庄", 2, "57", "75"),
    ("e-han-zhang", "汉章帝", "刘炟", 3, "75", "88"),
    ("e-han-he", "汉和帝", "刘肇", 4, "88", "105"),
    ("e-han-shang", "汉殇帝", "刘隆", 5, "105", "106"),
    ("e-han-an", "汉安帝", "刘祜", 6, "106", "125"),
    ("e-han-shao-bei", "北乡侯", "刘懿", 7, "125", "125", "quasi", "在位短"),
    ("e-han-shun", "汉顺帝", "刘保", 8, "125", "144"),
    ("e-han-chong", "汉冲帝", "刘炳", 9, "144", "145"),
    ("e-han-zhi", "汉质帝", "刘缵", 10, "145", "146"),
    ("e-han-huan", "汉桓帝", "刘志", 11, "146", "168"),
    ("e-han-ling", "汉灵帝", "刘宏", 12, "168", "189"),
    ("e-han-shao-bian", "汉少帝辩", "刘辩", 13, "189", "189", "quasi"),
    ("e-han-xian", "汉献帝", "刘协", 14, "189", "220"),
]
for row in eh:
    if len(row) == 6:
        id, d, p, s, a, b = row
        EMPERORS.append(E(id, d, p, "e-han", "东汉", s, a, b))
    elif len(row) == 7:
        id, d, p, s, a, b, t = row
        EMPERORS.append(E(id, d, p, "e-han", "东汉", s, a, b, t, ""))
    else:
        id, d, p, s, a, b, t, n = row
        EMPERORS.append(E(id, d, p, "e-han", "东汉", s, a, b, t, n))
# —— 三国 ——
EMPERORS += [
    E("wei-wen", "魏文帝", "曹丕", "cao-wei", "曹魏", 1, "220", "226"),
    E("wei-ming", "魏明帝", "曹叡", "cao-wei", "曹魏", 2, "226", "239"),
    E("wei-qi", "齐王芳", "曹芳", "cao-wei", "曹魏", 3, "239", "254"),
    E("wei-gaogui", "高贵乡公", "曹髦", "cao-wei", "曹魏", 4, "254", "260"),
    E("wei-yuan", "魏元帝", "曹奂", "cao-wei", "曹魏", 5, "260", "265"),
    E("shu-zhaolie", "汉昭烈帝", "刘备", "shu-han", "蜀汉", 1, "221", "223"),
    E("shu-houzhu", "蜀后主", "刘禅", "shu-han", "蜀汉", 2, "223", "263"),
    E("wu-da", "吴大帝", "孙权", "sun-wu", "孙吴", 1, "229", "252"),
    E("wu-kuaiji", "会稽王", "孙亮", "sun-wu", "孙吴", 2, "252", "258"),
    E("wu-jing", "吴景帝", "孙休", "sun-wu", "孙吴", 3, "258", "264"),
    E("wu-wucheng", "吴末帝", "孙皓", "sun-wu", "孙吴", 4, "264", "280"),
]

# —— 西晋 / 东晋 ——
EMPERORS += [
    E("w-jin-wu", "晋武帝", "司马炎", "w-jin", "西晋", 1, "266", "290"),
    E("w-jin-hui", "晋惠帝", "司马衷", "w-jin", "西晋", 2, "290", "306"),
    E("w-jin-huai", "晋怀帝", "司马炽", "w-jin", "西晋", 3, "306", "311"),
    E("w-jin-min", "晋愍帝", "司马邺", "w-jin", "西晋", 4, "313", "316"),
    E("e-jin-yuan", "晋元帝", "司马睿", "e-jin", "东晋", 1, "317", "322"),
    E("e-jin-ming", "晋明帝", "司马绍", "e-jin", "东晋", 2, "322", "325"),
    E("e-jin-cheng", "晋成帝", "司马衍", "e-jin", "东晋", 3, "325", "342"),
    E("e-jin-kang", "晋康帝", "司马岳", "e-jin", "东晋", 4, "342", "344"),
    E("e-jin-mu", "晋穆帝", "司马聃", "e-jin", "东晋", 5, "344", "361"),
    E("e-jin-ai", "晋哀帝", "司马丕", "e-jin", "东晋", 6, "361", "365"),
    E("e-jin-fei", "晋废帝", "司马奕", "e-jin", "东晋", 7, "365", "371"),
    E("e-jin-jianwen", "晋简文帝", "司马昱", "e-jin", "东晋", 8, "371", "372"),
    E("e-jin-xiaowu", "晋孝武帝", "司马曜", "e-jin", "东晋", 9, "372", "396"),
    E("e-jin-an", "晋安帝", "司马德宗", "e-jin", "东晋", 10, "396", "418"),
    E("e-jin-gong", "晋恭帝", "司马德文", "e-jin", "东晋", 11, "418", "420"),
]

# —— 南朝 ——
EMPERORS += [
    E("liu-song-wu", "宋武帝", "刘裕", "liu-song", "刘宋", 1, "420", "422"),
    E("liu-song-shao", "宋少帝", "刘义符", "liu-song", "刘宋", 2, "422", "424"),
    E("liu-song-wen", "宋文帝", "刘义隆", "liu-song", "刘宋", 3, "424", "453"),
    E("liu-song-xiao", "宋孝武帝", "刘骏", "liu-song", "刘宋", 4, "453", "464"),
    E("liu-song-qianfei", "前废帝", "刘子业", "liu-song", "刘宋", 5, "464", "465"),
    E("liu-song-ming", "宋明帝", "刘彧", "liu-song", "刘宋", 6, "465", "472"),
    E("liu-song-houfei", "后废帝", "刘昱", "liu-song", "刘宋", 7, "472", "477"),
    E("liu-song-shun", "宋顺帝", "刘准", "liu-song", "刘宋", 8, "477", "479"),
    E("qi-gao", "齐高帝", "萧道成", "nan-qi", "南齐", 1, "479", "482"),
    E("qi-wu", "齐武帝", "萧赜", "nan-qi", "南齐", 2, "482", "493"),
    E("qi-yulin", "郁林王", "萧昭业", "nan-qi", "南齐", 3, "493", "494"),
    E("qi-hailing", "海陵王", "萧昭文", "nan-qi", "南齐", 4, "494", "494"),
    E("qi-ming", "齐明帝", "萧鸾", "nan-qi", "南齐", 5, "494", "498"),
    E("qi-donghun", "东昏侯", "萧宝卷", "nan-qi", "南齐", 6, "498", "501"),
    E("qi-he", "齐和帝", "萧宝融", "nan-qi", "南齐", 7, "501", "502"),
    E("liang-wu", "梁武帝", "萧衍", "liang", "梁", 1, "502", "549"),
    E("liang-jianwen", "梁简文帝", "萧纲", "liang", "梁", 2, "549", "551"),
    E("liang-yu", "豫章王栋", "萧栋", "liang", "梁", 3, "551", "551", "quasi"),
    E("liang-yuan", "梁元帝", "萧绎", "liang", "梁", 4, "552", "554"),
    E("liang-jing", "梁敬帝", "萧方智", "liang", "梁", 5, "555", "557"),
    E("chen-wu", "陈武帝", "陈霸先", "chen", "陈", 1, "557", "559"),
    E("chen-wen", "陈文帝", "陈蒨", "chen", "陈", 2, "559", "566"),
    E("chen-fei", "陈废帝", "陈伯宗", "chen", "陈", 3, "566", "568"),
    E("chen-xuan", "陈宣帝", "陈顼", "chen", "陈", 4, "568", "582"),
    E("chen-houzhu", "陈后主", "陈叔宝", "chen", "陈", 5, "582", "589"),
]

# —— 北朝选录（北魏—北周/北齐）——
EMPERORS += [
    E("n-wei-daowu", "道武帝", "拓跋珪", "n-wei", "北魏", 1, "386", "409"),
    E("n-wei-mingyuan", "明元帝", "拓跋嗣", "n-wei", "北魏", 2, "409", "423"),
    E("n-wei-taiwu", "太武帝", "拓跋焘", "n-wei", "北魏", 3, "423", "452"),
    E("n-wei-wencheng", "文成帝", "拓跋濬", "n-wei", "北魏", 4, "452", "465"),
    E("n-wei-xianwen", "献文帝", "拓跋弘", "n-wei", "北魏", 5, "465", "471"),
    E("n-wei-xiaowen", "孝文帝", "元宏", "n-wei", "北魏", 6, "471", "499"),
    E("n-wei-xuanwu", "宣武帝", "元恪", "n-wei", "北魏", 7, "499", "515"),
    E("n-wei-xiaoming", "孝明帝", "元诩", "n-wei", "北魏", 8, "515", "528"),
    E("n-wei-xiaozhuang", "孝庄帝", "元子攸", "n-wei", "北魏", 9, "528", "530"),
    E("n-wei-jemin", "节闵帝", "元恭", "n-wei", "北魏", 10, "531", "532", "quasi"),
    E("n-wei-xiaowu", "孝武帝", "元修", "n-wei", "北魏", 11, "532", "534"),
    E("e-wei-xiaojing", "孝静帝", "元善见", "e-wei", "东魏", 1, "534", "550"),
    E("w-wei-wen", "文帝", "元宝炬", "w-wei", "西魏", 1, "535", "551"),
    E("w-wei-fei", "废帝", "元钦", "w-wei", "西魏", 2, "551", "554"),
    E("w-wei-gong", "恭帝", "拓跋廓", "w-wei", "西魏", 3, "554", "556"),
    E("n-qi-wenxuan", "文宣帝", "高洋", "n-qi", "北齐", 1, "550", "559"),
    E("n-qi-fei", "废帝", "高殷", "n-qi", "北齐", 2, "559", "560"),
    E("n-qi-xiaozhao", "孝昭帝", "高演", "n-qi", "北齐", 3, "560", "561"),
    E("n-qi-wucheng", "武成帝", "高湛", "n-qi", "北齐", 4, "561", "565"),
    E("n-qi-houzhu", "后主", "高纬", "n-qi", "北齐", 5, "565", "577"),
    E("n-zhou-xiao-min", "孝闵帝", "宇文觉", "n-zhou", "北周", 1, "557", "557"),
    E("n-zhou-ming", "明帝", "宇文毓", "n-zhou", "北周", 2, "557", "560"),
    E("n-zhou-wu", "武帝", "宇文邕", "n-zhou", "北周", 3, "560", "578"),
    E("n-zhou-xuan", "宣帝", "宇文赟", "n-zhou", "北周", 4, "578", "579"),
    E("n-zhou-jing", "静帝", "宇文阐", "n-zhou", "北周", 5, "579", "581"),
]

# —— 十六国（准·主要称帝/称王可入图鉴者，工作选录）——
EMPERORS += [
    E("q-zhao-liu-yuan", "汉（前赵）高祖", "刘渊", "q-zhao", "前赵", 1, "304", "310", "quasi", "十六国"),
    E("q-zhao-liu-cong", "汉（前赵）烈宗", "刘聪", "q-zhao", "前赵", 2, "310", "318", "quasi", "十六国"),
    E("q-zhao-liu-yao", "赵（前赵）主", "刘曜", "q-zhao", "前赵", 3, "318", "329", "quasi", "十六国"),
    E("h-zhao-shi-le", "后赵高祖", "石勒", "h-zhao", "后赵", 1, "319", "333", "quasi", "十六国"),
    E("h-zhao-shi-hu", "后赵武帝", "石虎", "h-zhao", "后赵", 2, "334", "349", "quasi", "十六国"),
    E("cheng-han-li-xiong", "成汉太宗", "李雄", "cheng-han", "成汉", 1, "304", "334", "quasi", "十六国"),
    E("q-yan-murong-huang", "前燕文明帝", "慕容皝", "q-yan", "前燕", 1, "337", "348", "quasi", "十六国"),
    E("q-yan-murong-jun", "前燕景昭帝", "慕容儁", "q-yan", "前燕", 2, "348", "360", "quasi", "十六国"),
    E("q-qin-fu-jian-jian", "前秦高祖", "苻健", "q-qin", "前秦", 1, "351", "355", "quasi", "十六国"),
    E("q-qin-fu-jian", "前秦世祖", "苻坚", "q-qin", "前秦", 2, "357", "385", "quasi", "十六国·淝水"),
    E("h-qin-yao-chang", "后秦太祖", "姚苌", "h-qin", "后秦", 1, "384", "393", "quasi", "十六国"),
    E("h-qin-yao-xing", "后秦高祖", "姚兴", "h-qin", "后秦", 2, "394", "416", "quasi", "十六国"),
    E("h-yan-murong-chui", "后燕成武帝", "慕容垂", "h-yan", "后燕", 1, "384", "396", "quasi", "十六国"),
    E("x-qin-qifu", "西秦烈祖", "乞伏国仁", "x-qin", "西秦", 1, "385", "388", "quasi", "十六国"),
    E("h-liang-lv-guang", "后凉懿武帝", "吕光", "h-liang", "后凉", 1, "386", "399", "quasi", "十六国"),
    E("n-liang-tufa", "南凉武王", "秃发乌孤", "n-liang", "南凉", 1, "397", "399", "quasi", "十六国"),
    E("n-liang-juqu", "北凉武宣王", "沮渠蒙逊", "b-liang", "北凉", 1, "401", "433", "quasi", "十六国"),
    E("x-liang-li-hao", "西凉太祖", "李暠", "x-liang", "西凉", 1, "400", "417", "quasi", "十六国"),
    E("xia-helian", "夏世祖", "赫连勃勃", "xia", "胡夏", 1, "407", "425", "quasi", "十六国"),
    E("b-yan-feng-ba", "北燕文成帝", "冯跋", "b-yan", "北燕", 1, "409", "430", "quasi", "十六国"),
    E("q-liang-zhang-gui", "前凉武王", "张轨", "q-liang", "前凉", 1, "301", "314", "quasi", "十六国·多称王"),
    E("dai-shiyijian", "代王", "拓跋什翼犍", "dai", "代", 1, "338", "376", "quasi", "十六国·北魏先世"),
]

# —— 十国（准·选录开国/代表君主）——
EMPERORS += [
    E("wu-yang-xingmi", "吴太祖", "杨行密", "shi-wu", "杨吴", 1, "902", "905", "quasi", "十国"),
    E("wu-yang-pu", "吴睿帝", "杨溥", "shi-wu", "杨吴", 2, "920", "937", "quasi", "十国"),
    E("n-tang-lie-zu", "南唐烈祖", "李昪", "n-tang", "南唐", 1, "937", "943", "quasi", "十国"),
    E("n-tang-yuan-zong", "南唐元宗", "李璟", "n-tang", "南唐", 2, "943", "961", "quasi", "十国"),
    E("n-tang-houzhu", "南唐后主", "李煜", "n-tang", "南唐", 3, "961", "975", "quasi", "十国"),
    E("wuyue-qian-liu", "吴越太祖", "钱镠", "wuyue", "吴越", 1, "907", "932", "quasi", "十国"),
    E("min-wang-shenzhi", "闽太祖", "王审知", "min", "闽", 1, "909", "925", "quasi", "十国"),
    E("min-wang-yanjun", "闽惠宗", "王延钧", "min", "闽", 2, "926", "935", "quasi", "十国"),
    E("chu-ma-yin", "楚武穆王", "马殷", "chu", "马楚", 1, "907", "930", "quasi", "十国"),
    E("n-han-liu-yan", "南汉高祖", "刘䶮", "n-han", "南汉", 1, "917", "942", "quasi", "十国"),
    E("q-shu-wang-jian", "前蜀高祖", "王建", "q-shu", "前蜀", 1, "907", "918", "quasi", "十国"),
    E("q-shu-wang-yan", "前蜀后主", "王衍", "q-shu", "前蜀", 2, "918", "925", "quasi", "十国"),
    E("h-shu-meng-zhixiang", "后蜀高祖", "孟知祥", "h-shu", "后蜀", 1, "934", "934", "quasi", "十国"),
    E("h-shu-meng-chang", "后蜀后主", "孟昶", "h-shu", "后蜀", 2, "934", "965", "quasi", "十国"),
    E("jingnan-gao", "南平武信王", "高季兴", "jingnan", "荆南", 1, "924", "928", "quasi", "十国"),
    E("b-han-liu-chong", "北汉世祖", "刘崇", "b-han", "北汉", 1, "951", "954", "quasi", "十国"),
    E("b-han-liu-jun", "北汉睿宗", "刘钧", "b-han", "北汉", 2, "954", "968", "quasi", "十国"),
]

# —— 隋 ——
EMPERORS += [
    E("sui-wen", "隋文帝", "杨坚", "sui", "隋", 1, "581", "604"),
    E("sui-yang", "隋炀帝", "杨广", "sui", "隋", 2, "604", "618"),
    E("sui-gong", "隋恭帝", "杨侑", "sui", "隋", 3, "617", "618", "quasi"),
]

# —— 唐 ——
tang = [
    ("tang-gao-zu", "唐高祖", "李渊", 1, "618", "626"),
    ("tang-tai-zong", "唐太宗", "李世民", 2, "626", "649"),
    ("tang-gao-zong", "唐高宗", "李治", 3, "649", "683"),
    ("tang-zhong-zong-a", "唐中宗", "李显", 4, "683", "684", "emperor", "两度在位，索引分条或合并待定"),
    ("tang-rui-zong-a", "唐睿宗", "李旦", 5, "684", "690"),
    ("zhou-wu-zetian", "武则天", "武曌", 6, "690", "705", "emperor", "武周皇帝；女帝"),
    ("tang-zhong-zong-b", "唐中宗(复位)", "李显", 7, "705", "710"),
    ("tang-shang", "唐殇帝", "李重茂", 8, "710", "710", "quasi"),
    ("tang-rui-zong-b", "唐睿宗(复位)", "李旦", 9, "710", "712"),
    ("tang-xuan-zong", "唐玄宗", "李隆基", 10, "712", "756"),
    ("tang-su-zong", "唐肃宗", "李亨", 11, "756", "762"),
    ("tang-dai-zong", "唐代宗", "李豫", 12, "762", "779"),
    ("tang-de-zong", "唐德宗", "李适", 13, "779", "805"),
    ("tang-shun-zong", "唐顺宗", "李诵", 14, "805", "805"),
    ("tang-xian-zong", "唐宪宗", "李纯", 15, "805", "820"),
    ("tang-mu-zong", "唐穆宗", "李恒", 16, "820", "824"),
    ("tang-jing-zong", "唐敬宗", "李湛", 17, "824", "826"),
    ("tang-wen-zong", "唐文宗", "李昂", 18, "826", "840"),
    ("tang-wu-zong", "唐武宗", "李炎", 19, "840", "846"),
    ("tang-xuan-zong-ii", "唐宣宗", "李忱", 20, "846", "859"),
    ("tang-yi-zong", "唐懿宗", "李漼", 21, "859", "873"),
    ("tang-xi-zong", "唐僖宗", "李儇", 22, "873", "888"),
    ("tang-zhao-zong", "唐昭宗", "李晔", 23, "888", "904"),
    ("tang-ai-di", "唐哀帝", "李柷", 24, "904", "907"),
]
for row in tang:
    if len(row) == 6:
        id, d, p, s, a, b = row
        EMPERORS.append(E(id, d, p, "tang", "唐", s, a, b))
    elif len(row) == 7:
        id, d, p, s, a, b, t = row
        EMPERORS.append(E(id, d, p, "tang", "唐", s, a, b, t, ""))
    else:
        id, d, p, s, a, b, t, n = row
        EMPERORS.append(E(id, d, p, "tang", "唐", s, a, b, t, n))
# —— 五代 ——
EMPERORS += [
    E("liang-tai-zu", "后梁太祖", "朱温", "hou-liang", "后梁", 1, "907", "912"),
    E("liang-mo", "后梁末帝", "朱友贞", "hou-liang", "后梁", 2, "913", "923"),
    E("tang-zhuang", "后唐庄宗", "李存勖", "hou-tang", "后唐", 1, "923", "926"),
    E("tang-ming", "后唐明宗", "李嗣源", "hou-tang", "后唐", 2, "926", "933"),
    E("tang-min", "后唐闵帝", "李从厚", "hou-tang", "后唐", 3, "933", "934"),
    E("tang-mo", "后唐末帝", "李从珂", "hou-tang", "后唐", 4, "934", "936"),
    E("jin-gao", "后晋高祖", "石敬瑭", "hou-jin", "后晋", 1, "936", "942"),
    E("jin-chu", "后晋出帝", "石重贵", "hou-jin", "后晋", 2, "942", "947"),
    E("han-gao-wu", "后汉高祖", "刘知远", "hou-han", "后汉", 1, "947", "948"),
    E("han-yin", "后汉隐帝", "刘承祐", "hou-han", "后汉", 2, "948", "950"),
    E("zhou-tai", "后周太祖", "郭威", "hou-zhou", "后周", 1, "951", "954"),
    E("zhou-shi", "后周世宗", "柴荣", "hou-zhou", "后周", 2, "954", "959"),
    E("zhou-gong", "后周恭帝", "柴宗训", "hou-zhou", "后周", 3, "959", "960"),
]

# —— 北宋 / 南宋 ——
EMPERORS += [
    E("n-song-tai-zu", "宋太祖", "赵匡胤", "n-song", "北宋", 1, "960", "976"),
    E("n-song-tai-zong", "宋太宗", "赵光义", "n-song", "北宋", 2, "976", "997"),
    E("n-song-zhen", "宋真宗", "赵恒", "n-song", "北宋", 3, "997", "1022"),
    E("n-song-ren", "宋仁宗", "赵祯", "n-song", "北宋", 4, "1022", "1063"),
    E("n-song-ying", "宋英宗", "赵曙", "n-song", "北宋", 5, "1063", "1067"),
    E("n-song-shen", "宋神宗", "赵顼", "n-song", "北宋", 6, "1067", "1085"),
    E("n-song-zhe", "宋哲宗", "赵煦", "n-song", "北宋", 7, "1085", "1100"),
    E("n-song-hui", "宋徽宗", "赵佶", "n-song", "北宋", 8, "1100", "1125"),
    E("n-song-qin", "宋钦宗", "赵桓", "n-song", "北宋", 9, "1125", "1127"),
    E("s-song-gao", "宋高宗", "赵构", "s-song", "南宋", 1, "1127", "1162"),
    E("s-song-xiao", "宋孝宗", "赵昚", "s-song", "南宋", 2, "1162", "1189"),
    E("s-song-guang", "宋光宗", "赵惇", "s-song", "南宋", 3, "1189", "1194"),
    E("s-song-ning", "宋宁宗", "赵扩", "s-song", "南宋", 4, "1194", "1224"),
    E("s-song-li", "宋理宗", "赵昀", "s-song", "南宋", 5, "1224", "1264"),
    E("s-song-du", "宋度宗", "赵禥", "s-song", "南宋", 6, "1264", "1274"),
    E("s-song-gong", "宋恭帝", "赵㬎", "s-song", "南宋", 7, "1274", "1276"),
    E("s-song-duan", "宋端宗", "赵昰", "s-song", "南宋", 8, "1276", "1278"),
    E("s-song-di-bing", "宋帝昺", "赵昺", "s-song", "南宋", 9, "1278", "1279"),
]

# —— 辽金元（选录常见帝纪）——
EMPERORS += [
    E("liao-tai-zu", "辽太祖", "耶律阿保机", "liao", "辽", 1, "907", "926"),
    E("liao-tai-zong", "辽太宗", "耶律德光", "liao", "辽", 2, "927", "947"),
    E("liao-shi-zong", "辽世宗", "耶律阮", "liao", "辽", 3, "947", "951"),
    E("liao-mu-zong", "辽穆宗", "耶律璟", "liao", "辽", 4, "951", "969"),
    E("liao-jing-zong", "辽景宗", "耶律贤", "liao", "辽", 5, "969", "982"),
    E("liao-sheng-zong", "辽圣宗", "耶律隆绪", "liao", "辽", 6, "982", "1031"),
    E("liao-xing-zong", "辽兴宗", "耶律宗真", "liao", "辽", 7, "1031", "1055"),
    E("liao-dao-zong", "辽道宗", "耶律洪基", "liao", "辽", 8, "1055", "1101"),
    E("liao-tianzuo", "天祚帝", "耶律延禧", "liao", "辽", 9, "1101", "1125"),
    E("jin-tai-zu", "金太祖", "完颜阿骨打", "jin", "金", 1, "1115", "1123"),
    E("jin-tai-zong", "金太宗", "完颜晟", "jin", "金", 2, "1123", "1135"),
    E("jin-xi-zong", "金熙宗", "完颜亶", "jin", "金", 3, "1135", "1149"),
    E("jin-hailiing", "海陵王", "完颜亮", "jin", "金", 4, "1149", "1161"),
    E("jin-shi-zong", "金世宗", "完颜雍", "jin", "金", 5, "1161", "1189"),
    E("jin-zhang-zong", "金章宗", "完颜璟", "jin", "金", 6, "1189", "1208"),
    E("jin-wei-shao", "卫绍王", "完颜永济", "jin", "金", 7, "1208", "1213"),
    E("jin-xuan-zong", "金宣宗", "完颜珣", "jin", "金", 8, "1213", "1223"),
    E("jin-ai-zong", "金哀宗", "完颜守绪", "jin", "金", 9, "1224", "1234"),
    E("yuan-tai-zu", "元太祖", "成吉思汗", "yuan", "元", 1, "1206", "1227", "emperor", "大蒙古国；元史本纪起太祖"),
    E("yuan-tai-zong", "元太宗", "窝阔台", "yuan", "元", 2, "1229", "1241"),
    E("yuan-ding-zong", "元定宗", "贵由", "yuan", "元", 3, "1246", "1248"),
    E("yuan-xian-zong", "元宪宗", "蒙哥", "yuan", "元", 4, "1251", "1259"),
    E("yuan-shi-zu", "元世祖", "忽必烈", "yuan", "元", 5, "1260", "1294", "emperor", "至元八年建国号大元"),
    E("yuan-cheng-zong", "元成宗", "铁穆耳", "yuan", "元", 6, "1294", "1307"),
    E("yuan-wu-zong", "元武宗", "海山", "yuan", "元", 7, "1307", "1311"),
    E("yuan-ren-zong", "元仁宗", "爱育黎拔力八达", "yuan", "元", 8, "1311", "1320"),
    E("yuan-ying-zong", "元英宗", "硕德八剌", "yuan", "元", 9, "1320", "1323"),
    E("yuan-tai-ding", "泰定帝", "也孙铁木儿", "yuan", "元", 10, "1323", "1328"),
    E("yuan-tian-shun", "天顺帝", "阿速吉八", "yuan", "元", 11, "1328", "1328", "quasi"),
    E("yuan-wen-zong", "元文宗", "图帖睦尔", "yuan", "元", 12, "1328", "1332"),
    E("yuan-ming-zong", "元明宗", "和世㻋", "yuan", "元", 13, "1329", "1329"),
    E("yuan-ning-zong", "元宁宗", "懿璘质班", "yuan", "元", 14, "1332", "1332"),
    E("yuan-hui-zong", "元惠宗", "妥欢贴睦尔", "yuan", "元", 15, "1333", "1368", "emperor", "顺帝"),
]

# —— 明 ——
ming = [
    ("ming-tai-zu", "明太祖", "朱元璋", 1, "1368", "1398"),
    ("ming-hui-di", "建文帝", "朱允炆", 2, "1398", "1402"),
    ("ming-cheng-zu", "明成祖", "朱棣", 3, "1402", "1424"),
    ("ming-ren-zong", "明仁宗", "朱高炽", 4, "1424", "1425"),
    ("ming-xuan-zong", "明宣宗", "朱瞻基", 5, "1425", "1435"),
    ("ming-ying-zong-a", "明英宗", "朱祁镇", 6, "1435", "1449", "emperor", "正统；后复位天顺"),
    ("ming-dai-zong", "明代宗", "朱祁钰", 7, "1449", "1457"),
    ("ming-ying-zong-b", "明英宗(天顺)", "朱祁镇", 8, "1457", "1464"),
    ("ming-xian-zong", "明宪宗", "朱见深", 9, "1464", "1487"),
    ("ming-xiao-zong", "明孝宗", "朱祐樘", 10, "1487", "1505"),
    ("ming-wu-zong", "明武宗", "朱厚照", 11, "1505", "1521"),
    ("ming-shi-zong", "明世宗", "朱厚熜", 12, "1521", "1566"),
    ("ming-mu-zong", "明穆宗", "朱载垕", 13, "1566", "1572"),
    ("ming-shen-zong", "明神宗", "朱翊钧", 14, "1572", "1620"),
    ("ming-guang-zong", "明光宗", "朱常洛", 15, "1620", "1620"),
    ("ming-xi-zong", "明熹宗", "朱由校", 16, "1620", "1627"),
    ("ming-si-zong", "明思宗", "朱由检", 17, "1627", "1644"),
]
for row in ming:
    if len(row) == 6:
        id, d, p, s, a, b = row
        EMPERORS.append(E(id, d, p, "ming", "明", s, a, b))
    elif len(row) == 7:
        id, d, p, s, a, b, t = row
        EMPERORS.append(E(id, d, p, "ming", "明", s, a, b, t, ""))
    else:
        id, d, p, s, a, b, t, n = row
        EMPERORS.append(E(id, d, p, "ming", "明", s, a, b, t, n))
# —— 清 ——
qing = [
    ("qing-tai-zu", "清太祖", "努尔哈赤", 1, "1616", "1626", "emperor", "后金；清史稿本纪"),
    ("qing-tai-zong", "清太宗", "皇太极", 2, "1626", "1643", "emperor", "后金—清"),
    ("qing-shi-zu", "清世祖", "福临", 3, "1643", "1661", "emperor", "顺治；入关"),
    ("qing-sheng-zu", "清圣祖", "玄烨", 4, "1661", "1722", "emperor", "康熙"),
    ("qing-shi-zong-y", "清世宗", "胤禛", 5, "1722", "1735", "emperor", "雍正"),
    ("qing-gao-zong", "清高宗", "弘历", 6, "1735", "1796", "emperor", "乾隆；禅位后仍有训政"),
    ("qing-ren-zong", "清仁宗", "颙琰", 7, "1796", "1820", "emperor", "嘉庆"),
    ("qing-xuan-zong", "清宣宗", "旻宁", 8, "1820", "1850", "emperor", "道光"),
    ("qing-wen-zong", "清文宗", "奕詝", 9, "1850", "1861", "emperor", "咸丰"),
    ("qing-mu-zong", "清穆宗", "载淳", 10, "1861", "1875", "emperor", "同治"),
    ("qing-de-zong", "清德宗", "载湉", 11, "1875", "1908", "emperor", "光绪"),
    ("qing-xuan-tong", "宣统帝", "溥仪", 12, "1908", "1912", "emperor", "末帝"),
]
for row in qing:
    id, d, p, s, a, b, t, n = row
    EMPERORS.append(E(id, d, p, "qing", "清", s, a, b, t, n))

# mark existing product pages
EXISTING = {
    "qin-shi-huang",
    "qin-er-shi",
    "han-gao-zu",
    "han-wu-di",
    "tang-tai-zong",
}
for e in EMPERORS:
    if e["id"] in EXISTING:
        e["page_status"] = "draft"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # unique id check
    ids = [e["id"] for e in EMPERORS]
    assert len(ids) == len(set(ids)), "duplicate ids"

    data = {
        "version": "0.1",
        "updated": "2026-08-06",
        "description": "皇帝图鉴工作用索引总表。正式/准分层可修订；十六国·十国为准选录。",
        "notes": [
            "本表优先收录各朝正史本纪常见帝系与主流统一/对峙政权皇帝。",
            "十六国、十国已选录主要称帝/开国君主为 quasi，非该政权全谱。",
            "南明、北元等仍可后续扩展。",
            "在位年取通行近似公历，短祚/改元复杂者以 note 标明。",
            "page_status: stub=仅索引, draft=已有YAML草稿, ready=可发布。",
        ],
        "emperors": EMPERORS,
    }

    yaml_path = OUT_DIR / "emperors_master.yaml"
    # simple yaml dump without pyyaml dependency for list of dicts
    try:
        import yaml

        yaml_path.write_text(
            yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
    except ImportError:
        (OUT_DIR / "emperors_master.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    json_path = OUT_DIR / "emperors_master.json"
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # stats
    by_dyn: dict[str, list] = {}
    by_tier: dict[str, int] = {}
    for e in EMPERORS:
        by_dyn.setdefault(e["dynasty"], []).append(e)
        by_tier[e["tier"]] = by_tier.get(e["tier"], 0) + 1

    lines = [
        "# 皇帝索引总表",
        "",
        f"> 生成：`tools/build_emperors_master_index.py` · 日期 {data['updated']}",
        "",
        "## 统计",
        "",
        f"- **总条目：{len(EMPERORS)}**",
        f"- 正式 emperor：{by_tier.get('emperor', 0)}",
        f"- 准 quasi：{by_tier.get('quasi', 0)}",
        f"- 已有产品页草稿：{sum(1 for e in EMPERORS if e['page_status']!='stub')}",
        "",
        "说明：此为**工作索引**，不是封闭学术定论。十六国/十国为准选录；南明等可再扩。",
        "",
        "数据文件：",
        "",
        "- `data/catalog/emperors_master.json`",
        "- `data/catalog/emperors_master.yaml`（若环境有 PyYAML）",
        "",
        "## 分朝数量",
        "",
        "| 政权 | 条数 | 其中 emperor | 其中 quasi |",
        "|------|------|--------------|------------|",
    ]
    for dyn, xs in by_dyn.items():
        ne = sum(1 for x in xs if x["tier"] == "emperor")
        nq = sum(1 for x in xs if x["tier"] == "quasi")
        lines.append(f"| {dyn} | {len(xs)} | {ne} | {nq} |")

    lines += ["", "## 全表", "", "| # | id | 显示名 | 姓名 | 政权 | 序 | 在位 | 层级 | 页状态 | 备注 |", "|---|----|--------|------|------|----|------|------|--------|------|"]
    for i, e in enumerate(EMPERORS, 1):
        lines.append(
            f"| {i} | `{e['id']}` | {e['display']} | {e['personal']} | {e['dynasty']} | {e['sequence']} | {e['reign_start']}–{e['reign_end']} | {e['tier']} | {e['page_status']} | {e['note']} |"
        )
    lines.append("")
    MD_OUT.parent.mkdir(parents=True, exist_ok=True)
    MD_OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"total={len(EMPERORS)} emperor={by_tier.get('emperor',0)} quasi={by_tier.get('quasi',0)}")
    print("OK", json_path)
    print("OK", MD_OUT)


if __name__ == "__main__":
    main()
