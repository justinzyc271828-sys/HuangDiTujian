#!/usr/bin/env python3
"""生成前端简体→繁体转换表 apps/web/src/tradTable.ts。

数据源：OpenCC STCharacters.txt / STPhrases.txt（Apache-2.0，
已下载到 tools/_tmp/；缺失时重新下载）。

策略：
- 单字表：全量导出（简≠繁 的条目），取 OpenCC 第一个繁体候选
- 词表：只导出本项目语料（data/ content/ apps/web/src）里实际出现的词，
  控制包体积；FORCED 列表里的高风险词（姓氏/地名/经典虚词）强制收录并校对
- 运行时算法：词级最长匹配 → 单字映射 → 项目 WORD_FIX 覆盖（在 i18n.tsx）

用法：python tools/build_trad_table.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TMP = ROOT / "tools" / "_tmp"
OUT = ROOT / "apps" / "web" / "src" / "tradTable.ts"

CHAR_URL = "https://raw.githubusercontent.com/BYVoid/OpenCC/master/data/dictionary/STCharacters.txt"
PHRASE_URL = "https://raw.githubusercontent.com/BYVoid/OpenCC/master/data/dictionary/STPhrases.txt"

CORPUS_GLOBS = [
    ("data", (".yaml", ".json")),
    ("content", (".md",)),
    ("apps/web/src", (".ts", ".tsx")),
]

# 高风险词强制表：简→繁 必须精确如此（姓氏、地名、经典虚词等，
# OpenCC 单字首选在这些词上会出错；词表本身也可能漏收）
FORCED: dict[str, str] = {
    # 「后」：君主配偶/先後
    "皇后": "皇后", "皇太后": "皇太后", "太后": "太后", "王后": "王后",
    "后妃": "后妃", "后土": "后土", "后羿": "后羿", "后稷": "后稷",
    "先后": "先後", "以后": "以後", "之后": "之後", "然后": "然後",
    "最后": "最後", "前后": "前後", "日后": "日後", "今后": "今後",
    "午后": "午後", "随后": "隨後", "幕后": "幕後", "尔后": "爾後",
    "之后": "之後",
    # 「咸」：地名/年号不取「鹹」
    "咸阳": "咸陽", "咸丰": "咸豐", "咸宁": "咸寧", "咸安": "咸安",
    # 「姜」姓氏
    "姜子牙": "姜子牙", "姜太公": "姜太公", "姜维": "姜維", "姜姓": "姜姓",
    # 「范」姓氏
    "范蠡": "范蠡", "范增": "范增", "范仲淹": "范仲淹", "范晔": "范曄",
    # 「岳」姓氏
    "岳飞": "岳飛",
    # 「于」姓氏/介词兼形
    "于禁": "于禁", "于谦": "于謙",
    # 「任于」恒等：OpenCC 收「任于→任於」，语料中全是「任+于谦（人名）」
    # 语境，词级最长匹配会吃掉人名首字；强制不转，保护「于谦」
    "任于": "任于",
    # 「或云」说义不转雲；「拓跋余」人名不转餘
    "或云": "或云", "拓跋余": "拓跋余",
    # 「种」姓氏（北宋将门）
    "种师道": "种師道",
    # 「云」言说义常见组合
    "诗云": "詩云", "书云": "書云", "云云": "云云",
    # 「余」我义残留保护（「其余/剩余」走词表正常转「餘」）
    # 无强制项，词表兜底
    # 其他高频项目词校对
    "统一": "統一", "书同文": "書同文", "中央集权": "中央集權",
    "巡狩": "巡狩", "封面": "封面", "下面": "下面", "里面": "裏面",
    # 后妃家族保护（OpenCC 词表倾向「後」，帝王配偶必须保「后」）
    "吕后": "呂后", "高后": "高后", "窦后": "竇后", "武后": "武后",
    "韦后": "韋后", "薄后": "薄后", "赵后": "趙后", "卫后": "衛后",
    "头发": "頭髮", "亲征": "親征", "出征": "出征", "征服": "征服",
    "象征": "象徵", "征税": "徵稅", "征收": "徵收", "特征": "特徵",
    "干扰": "干擾", "干涉": "干涉", "干戈": "干戈", "干预": "干預",
    "关系": "關係", "系统": "系統", "世系": "世系",
    "发现": "發現", "发动": "發動", "发展": "發展", "爆发": "爆發",
    "千里": "千里", "故里": "故里", "里程碑": "里程碑",
    "放松": "放鬆", "轻松": "輕鬆", "松树": "松樹",
    "万历": "萬曆", "日历": "日曆", "历史": "歷史", "经历": "經歷",
}

# 自测用例：转换后必须等于期望值（含 WORD_FIX 效果）
SELF_TEST: dict[str, str] = {
    "结束列国分立、建立中央集权帝制的秦帝国开创者":
        "結束列國分立、建立中央集權帝制的秦帝國開創者",
    "统一": "統一",
    "书同文": "書同文",
    "巡狩": "巡狩",
    "中央集权": "中央集權",
    "皇后": "皇后",
    "皇太后": "皇太后",
    "以后": "以後",
    "在位": "在位",
    "亲征": "親征",
    "咸阳": "咸陽",
    "头发": "頭髮",
    "奏折": "奏摺",       # WORD_FIX
    "画像在制": "畫像在製",  # WORD_FIX
    "事迹": "事蹟",        # WORD_FIX
    "想象": "想像",        # WORD_FIX
    "称始皇帝": "稱始皇帝",
    "并天下，号始皇帝，分三十六郡": "並天下，號始皇帝，分三十六郡",
}

# 与 i18n.tsx 保持一致的项目词级覆盖
WORD_FIX = [("奏折", "奏摺"), ("在制", "在製"), ("想象", "想像"), ("事迹", "事蹟")]


def download(path: Path, url: str) -> None:
    import urllib.request
    path.parent.mkdir(parents=True, exist_ok=True)
    print(f"下载 {url} -> {path}")
    urllib.request.urlretrieve(url, path)


def parse_table(path: Path, keep_identity: bool = False) -> dict[str, str]:
    table: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            continue
        simp, trads = parts[0].strip(), parts[1].strip().split()
        if not simp or not trads:
            continue
        if simp != trads[0] or (keep_identity and len(simp) >= 2):
            table[simp] = trads[0]
    return table


def collect_corpus() -> str:
    chunks: list[str] = []
    for sub, exts in CORPUS_GLOBS:
        base = ROOT / sub
        for p in sorted(base.rglob("*")):
            if (p.is_file() and p.suffix in exts and "node_modules" not in p.parts
                    and p.name != "tradTable.ts"):  # 排除生成物自身，避免自我引用
                try:
                    chunks.append(p.read_text(encoding="utf-8", errors="ignore"))
                except OSError:
                    pass
    return "\n".join(chunks)


def main() -> int:
    char_path, phrase_path = TMP / "STCharacters.txt", TMP / "STPhrases.txt"
    if not char_path.exists():
        download(char_path, CHAR_URL)
    if not phrase_path.exists():
        download(phrase_path, PHRASE_URL)

    chars = parse_table(char_path)
    phrases_all = parse_table(phrase_path)
    corpus = collect_corpus()
    # 恒等词（简=繁，如「皇后」「吕后」）：语料中出现过就收入词表当「保护壳」，
    # 让最长匹配先命中它们，挡住单字首选的误转（后→後 之类）
    shields_all = parse_table(phrase_path, keep_identity=True)
    shields = {k: v for k, v in shields_all.items() if k == v and k in corpus}
    print(f"单字条目 {len(chars)}；词表原始 {len(phrases_all)}；"
          f"恒等保护壳 {len(shields)}；语料 {len(corpus)} 字")

    # 词表：语料中出现的 + 恒等保护壳 + FORCED 强制
    phrases = {k: v for k, v in phrases_all.items() if k in corpus}
    phrases.update(shields)
    forced_missing = [k for k in FORCED if k not in phrases_all]
    phrases.update(FORCED)
    print(f"词表收录 {len(phrases)}（FORCED {len(FORCED)}，其中 OpenCC 未收 {len(forced_missing)}：{forced_missing}）")

    # FORCED 与 OpenCC 冲突检查
    conflicts = [(k, phrases_all[k], v) for k, v in FORCED.items()
                 if k in phrases_all and phrases_all[k] != v]
    for k, a, b in conflicts:
        print(f"  注意：FORCED[{k}]={b} 覆盖 OpenCC 的 {a}")

    # —— 用与前端一致的算法做自测 ——
    max_len = max(len(p) for p in phrases)
    bucket: dict[str, list[tuple[str, str]]] = {}
    for p, t in phrases.items():
        bucket.setdefault(p[0], []).append((p, t))
    for lst in bucket.values():
        lst.sort(key=lambda x: -len(x[0]))

    def convert(s: str) -> str:
        out: list[str] = []
        i = 0
        while i < len(s):
            hit = None
            for p, t in bucket.get(s[i], []):
                if s.startswith(p, i):
                    hit = (p, t)
                    break
            if hit:
                out.append(hit[1])
                i += len(hit[0])
            else:
                out.append(chars.get(s[i], s[i]))
                i += 1
        res = "".join(out)
        for a, b in WORD_FIX:
            res = res.replace(a, b)
        return res

    bad = 0
    for simp, expect in SELF_TEST.items():
        got = convert(simp)
        mark = "OK " if got == expect else "✗✗"
        if got != expect:
            bad += 1
        print(f"  [{mark}] {simp} -> {got}" + ("" if got == expect else f"（期望 {expect}）"))
    if bad:
        print(f"自测失败 {bad} 条，修表后再写盘")
        return 1

    # —— 写 TS ——
    def ts_map(d: dict[str, str]) -> str:
        lines = [f"  {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)},"
                 for k, v in sorted(d.items())]
        return "{\n" + "\n".join(lines) + "\n}"

    header = (
        "/* ============================================================\n"
        "   生成文件，勿手改 —— python tools/build_trad_table.py\n"
        "   数据源：OpenCC STCharacters/STPhrases（Apache-2.0），\n"
        "   词表按本项目语料过滤 + FORCED 高风险词校对。\n"
        "   新增内容后若发现繁体误转，重新生成或加 FORCED。\n"
        "   ============================================================ */\n\n"
    )
    OUT.write_text(
        header
        + "/** 单字映射（简→繁，取 OpenCC 首选） */\n"
        + "export const TRAD_CHARS: Record<string, string> = " + ts_map(chars) + ";\n\n"
        + "/** 词级映射（最长匹配优先于单字） */\n"
        + "export const TRAD_PHRASES: Record<string, string> = " + ts_map(phrases) + ";\n",
        encoding="utf-8",
    )
    print(f"已写出 {OUT}（{OUT.stat().st_size} 字节）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
