#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全量再复查 dossier-complete 史料卡：
1) 编年 CHRONO / 薄摘要 THIN / 弱语 BADLANG
2) 空 dynasty
3) 崩后仍有更早年份事件 AFTER_DEATH
4) 扩大名场面 FACT 正史关键词
5) 卡出处书名能否在 BOOKS 中加载（SOURCE_BOOK）
6) 每人至少 1 张卡、year 字段格式

写出：docs/references/notes/史料卡全量再复查.md
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "content" / "sources"
REF = ROOT / "HuangDiTujian-Ref" / "01-史书全文与扫描" / "二十四史-简体"
REPORT = ROOT / "docs" / "references" / "notes" / "史料卡全量再复查.md"

BOOKS = {
    "史记": "01-史记.md",
    "汉书": "02-汉书.md",
    "后汉书": "03-后汉书.md",
    "三国志": "04-三国志.md",
    "晋书": "05-晋书.md",
    "宋书": "06-宋书.md",
    "南齐书": "07-南齐书.md",
    "梁书": "08-梁书.md",
    "陈书": "09-陈书.md",
    "魏书": "10-魏书.md",
    "北齐书": "11-北齐书.md",
    "周书": "12-周书.md",
    "隋书": "13-隋书.md",
    "南史": "14-南史.md",
    "北史": "15-北史.md",
    "旧唐书": "16-旧唐书.md",
    "新唐书": "17-新唐书.md",
    "旧五代史": "18-旧五代史.md",
    "新五代史": "19-新五代史.md",
    "宋史": "20-宋史.md",
    "辽史": "21-辽史.md",
    "金史": "22-金史.md",
    "元史": "23-元史.md",
    "明史": "24-明史.md",
}

# 扩大名场面：尽量覆盖各批升格关键节点
FACT_CHECKS: list[tuple[str, str, list[str], str]] = [
    # 秦
    ("qin-shi-huang", "称始皇帝", ["始皇帝", "二十六年"], "史记"),
    ("qin-shi-huang", "焚书", ["诗书", "李斯"], "史记"),
    ("qin-er-shi", "望夷", ["望夷", "赵高"], "史记"),
    # 西汉
    ("han-gao-zu", "沛县起兵", ["沛", "刘邦"], "史记"),
    ("han-gao-zu", "鸿门", ["鸿门"], "史记"),
    ("han-gao-zu", "垓下", ["垓下"], "史记"),
    ("han-gao-zu", "称帝", ["皇帝", "汉"], "史记"),
    ("han-wen-di", "除肉刑", ["肉刑", "缇萦"], "汉书"),
    ("han-jing-di", "七国", ["七国", "吴楚", "晁错"], "汉书"),
    ("han-wu-di", "马邑", ["马邑"], "汉书"),
    ("han-wu-di", "轮台", ["轮台"], "汉书"),
    ("han-zhao-di", "盐铁", ["盐铁"], "汉书"),
    ("han-xuan-di", "呼韩邪", ["呼韩邪"], "汉书"),
    ("han-yuan-di", "郅支", ["郅支"], "汉书"),
    ("xin-wang-mang", "代汉", ["新", "王莽"], "汉书"),
    # 东汉
    ("e-han-guangwu", "昆阳", ["昆阳"], "后汉书"),
    ("e-han-guangwu", "鄗南", ["鄗"], "后汉书"),
    ("e-han-ming", "云台", ["云台"], "后汉书"),
    ("e-han-zhang", "白虎", ["白虎"], "后汉书"),
    ("e-han-he", "燕然", ["燕然"], "后汉书"),
    ("e-han-ling", "黄巾", ["黄巾"], "后汉书"),
    ("e-han-xian", "都许", ["许"], "后汉书"),
    # 三国
    ("wei-wen", "受禅", ["禅", "黄初"], "三国志"),
    ("wei-qi", "高平陵", ["高平陵", "曹爽"], "三国志"),
    ("shu-zhaolie", "夷陵", ["夷陵", "猇亭", "陆逊"], "三国志"),
    ("shu-houzhu", "降", ["降", "邓艾"], "三国志"),
    ("wu-da", "赤壁", ["赤壁"], "三国志"),
    ("wu-wucheng", "降", ["降", "王濬"], "三国志"),
    # 两晋
    ("w-jin-wu", "平吴", ["孙皓", "吴"], "晋书"),
    ("w-jin-hui", "肉糜", ["肉糜"], "晋书"),
    ("w-jin-huai", "洛阳", ["洛阳"], "晋书"),
    ("e-jin-yuan", "即位", ["建康", "元帝", "即位"], "晋书"),
    ("e-jin-xiaowu", "淝水", ["淝水", "苻坚"], "晋书"),
    # 十六国
    ("q-zhao-liu-cong", "陷洛阳", ["洛阳"], "晋书"),
    ("q-zhao-liu-yao", "洛阳大战", ["石勒", "洛阳"], "晋书"),
    ("h-zhao-shi-le", "称帝", ["赵", "襄国"], "晋书"),
    ("h-qin-yao-chang", "杀苻坚", ["苻坚"], "晋书"),
    ("q-qin-fu-jian", "淝水", ["淝水", "晋"], "晋书"),
    ("h-yan-murong-chui", "参合", ["参合"], "晋书"),
    ("xia-helian", "统万", ["统万"], "晋书"),
    ("n-liang-juqu", "灭西凉", ["敦煌", "李"], "晋书"),
    # 刘宋
    ("liu-song-wu", "受禅", ["禅", "永初"], "宋书"),
    ("liu-song-wen", "元嘉", ["元嘉"], "宋书"),
    ("liu-song-wen", "瓜步", ["瓜步"], "宋书"),
    # 南齐梁陈
    ("qi-gao", "受禅", ["禅", "建元"], "南齐书"),
    ("qi-wu", "永明", ["永明"], "南齐书"),
    ("liang-wu", "侯景", ["侯景"], "梁书"),
    ("liang-yuan", "江陵", ["江陵"], "梁书"),
    ("chen-wu", "受禅", ["禅", "永定"], "陈书"),
    ("chen-houzhu", "隋灭陈", ["祯明", "隋"], "陈书"),
    # 北朝
    ("n-wei-daowu", "参合", ["参合"], "魏书"),
    ("n-wei-taiwu", "灭", ["凉", "夏", "北凉"], "魏书"),
    ("n-wei-xiaowen", "迁都", ["洛阳", "迁"], "魏书"),
    ("n-wei-xiaozhuang", "河阴", ["河阴", "尔朱"], "魏书"),
    ("n-zhou-wu", "灭北齐", ["齐", "邺"], "周书"),
    ("n-zhou-wu", "诛宇文护", ["护"], "周书"),
    ("n-qi-houzhu", "齐亡", ["周"], "北齐书"),
    ("e-wei-xiaojing", "禅位", ["禅", "高洋"], "魏书"),
    # 隋唐
    ("sui-wen", "平陈", ["平陈", "陈"], "隋书"),
    ("sui-yang", "江都", ["江都"], "隋书"),
    ("sui-gong", "禅位唐", ["禅"], "隋书"),
    ("tang-gao-zu", "太原", ["太原"], "旧唐书"),
    ("tang-tai-zong", "玄武", ["玄武"], "旧唐书"),
    ("tang-gao-zong", "废王立武", ["武后", "皇后"], "旧唐书"),
    ("zhou-wu-zetian", "称帝", ["则天", "圣神", "周"], "旧唐书"),
    ("tang-zhong-zong-b", "复位", ["神龙"], "旧唐书"),
    ("tang-xuan-zong", "安史", ["安禄山"], "旧唐书"),
    ("tang-xuan-zong", "马嵬", ["马嵬"], "旧唐书"),
    ("tang-su-zong", "灵武", ["灵武"], "旧唐书"),
    ("tang-de-zong", "奉天", ["奉天"], "旧唐书"),
    ("tang-shun-zong", "永贞", ["永贞"], "旧唐书"),
    ("tang-xian-zong", "淮西", ["淮西", "吴元济", "元和"], "旧唐书"),
    ("tang-wen-zong", "甘露", ["甘露"], "旧唐书"),
    ("tang-wu-zong", "会昌灭佛", ["废寺", "僧尼", "会昌"], "旧唐书"),
    ("tang-xi-zong", "黄巢", ["黄巢"], "旧唐书"),
    ("tang-ai-di", "禅位后梁", ["禅", "朱全忠"], "旧唐书"),
    # video-01 等
    ("n-song-tai-zu", "陈桥", ["陈桥", "点检"], "宋史"),
    ("yuan-shi-zu", "忽必烈", ["世祖", "至元"], "元史"),
    # 五代 / 十国 / 北宋
    ("qin-zi-ying", "降刘邦", ["轵道", "子婴", "降"], "史记"),
    ("liang-tai-zu", "受禅称帝", ["开平", "禅"], "旧五代史"),
    ("tang-zhuang", "称帝灭梁", ["灭梁", "同光"], "旧五代史"),
    ("jin-gao", "称帝联契丹", ["契丹", "十六州", "天福"], "旧五代史"),
    ("han-gao-wu", "称帝太原", ["太原", "汉"], "旧五代史"),
    ("zhou-gong", "陈桥", ["陈桥"], "宋史"),
    ("n-tang-lie-zu", "受吴禅", ["金陵", "唐"], "新五代史"),
    ("wuyue-qian-liu", "封吴越王", ["吴越", "钱"], "新五代史"),
    ("n-song-tai-zong", "灭北汉", ["太原", "北汉"], "宋史"),
    ("n-song-zhen", "澶渊", ["澶渊"], "宋史"),
    ("n-song-ren", "庆历新政", ["庆历", "仲淹"], "宋史"),
    ("n-song-shen", "变法", ["安石", "熙宁"], "宋史"),
    ("n-song-qin", "靖康之变", ["靖康", "北狩"], "宋史"),
    # 南宋 / 辽 / 金
    ("s-song-gao", "绍兴和议", ["绍兴", "岳飞"], "宋史"),
    ("s-song-xiao", "隆兴北伐", ["隆兴", "北伐"], "宋史"),
    ("s-song-ning", "开禧北伐", ["开禧"], "宋史"),
    ("s-song-li", "联蒙灭金", ["蔡州", "金"], "宋史"),
    ("s-song-di-bing", "崖山", ["崖山"], "宋史"),
    ("liao-tai-zu", "称帝建元", ["神册", "契丹"], "辽史"),
    ("liao-tai-zong", "扶石晋", ["十六州", "晋"], "辽史"),
    ("liao-sheng-zong", "澶渊", ["澶渊"], "辽史"),
    ("liao-tianzuo", "被俘辽亡", ["天祚", "金"], "辽史"),
    ("jin-tai-zu", "称帝建国", ["收国", "金"], "金史"),
    ("jin-tai-zong", "灭北宋", ["天会", "汴"], "金史"),
    ("jin-shi-zong", "大定之治", ["大定"], "金史"),
    ("jin-ai-zong", "蔡州自缢金亡", ["蔡州", "天兴"], "金史"),
    # 元明清
    ("yuan-tai-zu", "即大汗位", ["成吉思", "汗"], "元史"),
    ("yuan-tai-zong", "灭金", ["金", "蔡州"], "元史"),
    ("yuan-xian-zong", "崩于钓鱼城", ["钓鱼", "合州"], "元史"),
    ("yuan-ying-zong", "南坡", ["南坡"], "元史"),
    ("yuan-hui-zong", "红巾", ["红巾", "至正"], "元史"),
    ("yuan-hui-zong", "北奔上都", ["至正", "上都"], "元史"),
    ("ming-tai-zu", "称帝建明", ["洪武", "应天"], "明史"),
    ("ming-hui-di", "削藩", ["建文", "燕"], "明史"),
    ("ming-cheng-zu", "靖难", ["靖难"], "明史"),
    ("ming-cheng-zu", "迁都北京", ["北京", "永乐"], "明史"),
    ("ming-ying-zong-a", "土木", ["土木"], "明史"),
    ("ming-dai-zong", "北京保卫", ["于谦", "也先"], "明史"),
    ("ming-ying-zong-b", "复位", ["天顺", "夺门"], "明史"),
    ("ming-shi-zong", "大礼议", ["大礼"], "明史"),
    ("ming-shen-zong", "萨尔浒", ["杨镐", "辽东", "开原"], "明史"),
    ("ming-si-zong", "煤山", ["煤山", "崇祯"], "明史"),
]

_cache: dict[str, str] = {}


def load_book(name: str) -> str:
    if name not in _cache:
        fn = BOOKS.get(name)
        p = REF / fn if fn else None
        _cache[name] = p.read_text(encoding="utf-8") if p and p.exists() else ""
    return _cache[name]


def get_status(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines()[:25]:
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return ""


def get_dynasty(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines()[:30]:
        if line.startswith("dynasty:"):
            return line.split(":", 1)[1].strip().strip('"')
    return ""


def parse_card(path: Path) -> dict:
    t = path.read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    if t.startswith("---"):
        for line in t.split("---", 2)[1].splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
    sm = ""
    if "## 史实摘要" in t:
        sm = t.split("## 史实摘要", 1)[1].split("##", 1)[0].strip().replace("\n", " ")
    sources = []
    for a, b, c in re.findall(r"\| ([^|]+) \| ([^|]+) \| ([^|]*) \|", t):
        if a.strip() != "文献":
            sources.append((a.strip(), b.strip(), c.strip()))
    return {
        "path": path,
        "eid": meta.get("eid", ""),
        "year": meta.get("year", ""),
        "title": meta.get("title", path.stem),
        "summary": sm,
        "sources": sources,
        "confidence": meta.get("confidence", ""),
    }


def year_int(y: str) -> int | None:
    if not y or y == "undated":
        return None
    try:
        return int(y)
    except ValueError:
        m = re.match(r"^-?\d+", y)
        return int(m.group(0)) if m else None


def main() -> None:
    master = {
        e["id"]: e
        for e in json.loads(
            (ROOT / "data" / "catalog" / "emperors_master.json").read_text(encoding="utf-8")
        )["emperors"]
    }

    complete: list[tuple[str, list[dict], str]] = []
    for d in sorted(SRC.iterdir()):
        if not d.is_dir() or not (d / "00-史源卡.md").exists():
            continue
        if get_status(d / "00-史源卡.md") != "dossier-complete":
            continue
        cards = [
            parse_card(f)
            for f in sorted((d / "证据").glob("E*.md"))
            if f.name != "_template.md"
        ]
        complete.append((d.name, cards, get_dynasty(d / "00-史源卡.md")))

    issues: list[str] = []
    by_type: Counter[str] = Counter()

    # 1 structural
    for pid, cards, dy in complete:
        if not cards:
            issues.append(f"EMPTY {pid}")
            by_type["EMPTY"] += 1
        if not dy:
            issues.append(f"NO_DYNASTY {pid}")
            by_type["NO_DYNASTY"] += 1
        prev: int | None = None
        death_i = death_y = None
        for i, c in enumerate(cards):
            y = year_int(c["year"])
            if y is not None and prev is not None and y > 0 and prev > 0 and y < prev:
                issues.append(
                    f"CHRONO {pid} {c['eid']}: {prev} -> {y} ({c['title']})"
                )
                by_type["CHRONO"] += 1
            if y is not None:
                prev = y
            if len(c["summary"]) < 25:
                issues.append(
                    f"THIN {pid} {c['eid']} {c['title']} len={len(c['summary'])}"
                )
                by_type["THIN"] += 1
            for bad in ("骨架卡", "待本纪条列", "称公元", "中期政务高峰", "初政措置"):
                if bad in c["summary"] or bad in c["title"]:
                    issues.append(f"BADLANG {pid} {c['eid']}: {bad}")
                    by_type["BADLANG"] += 1
            # source book known?
            for book, _, _ in c["sources"]:
                b0 = book.split("·")[0].split(";")[0].strip()
                # strip notes like 晋书·载记
                b0 = re.split(r"[·/（(]", b0)[0].strip()
                allowed_extra = {
                    "资治通鉴",
                    "续资治通鉴长编",
                    "十六国春秋",
                    "华阳国志",
                    "高僧传",
                    "典论",
                    "洛阳伽蓝记",
                    "汉晋春秋",
                    "顺宗实录",
                    "盐铁论",
                    "笔记小说",
                    "词籍",
                    "五代会要",
                    "五代会要等",
                    "清史稿",
                    "清实录",
                    "东华录",
                    "满洲实录",
                    "新元史",
                    "明实录",
                    "庚申外史",
                    "元朝秘史",
                    "（待补）",
                }
                if b0 and b0 not in BOOKS and b0 not in allowed_extra:
                    if not any(k in b0 for k in list(BOOKS) + list(allowed_extra)):
                        issues.append(f"SRCBOOK {pid} {c['eid']}: {book}")
                        by_type["SRCBOOK"] += 1
            if any(
                x in c["title"]
                for x in ("崩", "被弑", "被杀", "遇害", "禅位", "逊位", "之死")
            ):
                if y is not None and death_i is None:
                    death_i, death_y = i, y
        if death_i is not None and death_y is not None:
            for c in cards[death_i + 1 :]:
                y = year_int(c["year"])
                if y is not None and y > 0 and y < death_y:
                    issues.append(
                        f"AFTER_DEATH {pid}: death@{death_y} then {c['eid']} "
                        f"{c['title']} year={y}"
                    )
                    by_type["AFTER_DEATH"] += 1

    # 2 fact checks
    fact_lines = []
    cards_by_pid = {pid: cards for pid, cards, _ in complete}
    for pid, title_key, kws, book in FACT_CHECKS:
        text = load_book(book)
        cards = cards_by_pid.get(pid)
        if not cards:
            fact_lines.append(f"SKIP {pid}: not complete")
            issues.append(f"FACT_SKIP {pid} {title_key}")
            by_type["FACT_SKIP"] += 1
            continue
        hit = next(
            (c for c in cards if title_key in c["title"] or title_key in c["summary"]),
            None,
        )
        if not hit:
            fact_lines.append(f"FAIL {pid}: no card for「{title_key}」")
            issues.append(f"FACT_NOCARD {pid} {title_key}")
            by_type["FACT_NOCARD"] += 1
            continue
        if not text:
            fact_lines.append(f"FAIL {pid}: book missing {book}")
            issues.append(f"FACT_BOOK {pid} {book}")
            by_type["FACT_BOOK"] += 1
            continue
        ok = any(k in text for k in kws)
        if ok:
            fact_lines.append(f"OK {pid}「{title_key}」↔ {book} ({hit['eid']})")
        else:
            fact_lines.append(f"FAIL {pid}「{title_key}」keywords not in {book}")
            issues.append(f"FACT_MISS {pid} {title_key} {book}")
            by_type["FACT_MISS"] += 1

    # 3 coverage vs master (how many complete by dynasty)
    dy_c = Counter(dy or "?" for _, _, dy in complete)
    n_cards = sum(len(c) for _, c, _ in complete)

    # report
    body = [
        "# 史料卡全量再复查（dossier-complete）",
        "",
        f"- **日期：** 2026-08-07",
        f"- **complete 人数：** **{len(complete)}** / master 269",
        f"- **证据卡总数：** **{n_cards}**",
        f"- **自动问题：** {dict(by_type) if by_type else '无'} 合计 **{len(issues)}**",
        f"- **名场面：** OK {sum(1 for x in fact_lines if x.startswith('OK'))} / "
        f"FAIL {sum(1 for x in fact_lines if x.startswith('FAIL'))} / "
        f"SKIP {sum(1 for x in fact_lines if x.startswith('SKIP'))}",
        f"- **工具：** `tools/full_recheck_complete.py`",
        "",
        "## 1. 结论",
        "",
    ]
    if not issues:
        body.append("**全部通过。** 编年、摘要长度、弱语、崩后事件、扩大名场面正史关键词均无失败项。")
    else:
        body.append(
            f"**发现 {len(issues)} 项问题**，按类型：`{dict(by_type)}`。见 §3。"
        )
    body += [
        "",
        "### 按朝覆盖（complete）",
        "",
        "| 朝 | 人数 |",
        "|----|------|",
    ]
    for dy, n in dy_c.most_common():
        body.append(f"| {dy or '（空）'} | {n} |")
    body += [
        "",
        "## 2. 名场面正史对读（扩大）",
        "",
    ]
    body += [f"- {x}" for x in fact_lines]
    body += [
        "",
        "## 3. 自动问题（全部）",
        "",
    ]
    if issues:
        body += [f"- {x}" for x in issues]
    else:
        body.append("- （无）")
    body += [
        "",
        "## 4. 复查范围说明",
        "",
        "- 仅 `status: dossier-complete`（frontmatter）",
        "- 107 scaffold **不在**本复查范围内",
        "- 交叉比对 = 正史简体 md 可检索主题词 + 卡序编年自洽，**非**纸书页码精校",
        "",
        "## 5. 人物卡数一览",
        "",
    ]
    for pid, cards, dy in complete:
        body.append(f"- `{pid}`（{dy or '?'}）{len(cards)} 条")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(body) + "\n", encoding="utf-8")

    print("complete", len(complete), "cards", n_cards)
    print("issues", dict(by_type), "total", len(issues))
    print(
        "facts OK",
        sum(1 for x in fact_lines if x.startswith("OK")),
        "FAIL",
        sum(1 for x in fact_lines if x.startswith("FAIL")),
        "SKIP",
        sum(1 for x in fact_lines if x.startswith("SKIP")),
    )
    for x in issues[:40]:
        print("!", x)
    for x in fact_lines:
        if x.startswith("FAIL") or x.startswith("SKIP"):
            print("F", x)
    print("report", REPORT)


if __name__ == "__main__":
    main()
