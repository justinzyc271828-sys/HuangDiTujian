#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Spot-check years/summaries for key complete dossiers after sort fix."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "content" / "sources"

PIDS = [
    "e-han-guangwu",
    "han-wu-di",
    "e-han-ming",
    "shu-zhaolie",
    "w-jin-hui",
    "qin-shi-huang",
    "e-jin-ai",
    "tang-tai-zong",
    "sui-yang",
    "xin-wang-mang",
]


def dump(pid: str) -> None:
    print("===", pid)
    evid = SRC / pid / "证据"
    for f in sorted(evid.glob("E*.md")):
        if f.name == "_template.md":
            continue
        t = f.read_text(encoding="utf-8")
        meta: dict[str, str] = {}
        for line in t.split("---", 2)[1].splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"')
        sm = ""
        if "## 史实摘要" in t:
            sm = (
                t.split("## 史实摘要", 1)[1]
                .split("##", 1)[0]
                .strip()
                .replace("\n", " ")[:90]
            )
        print(
            f"  {meta.get('eid')} year={meta.get('year')} "
            f"note={meta.get('date_note', '')[:24]} "
            f"| {meta.get('title')} | conf={meta.get('confidence')}"
        )
        print(f"    {sm}")


def check_known_facts() -> list[str]:
    """Manual year anchors that must match well-known chronology."""
    expect = {
        ("e-han-guangwu", "昆阳"): "23",
        ("e-han-guangwu", "鄗南称帝"): "25",
        ("e-han-guangwu", "定都洛阳"): "25",
        ("e-han-guangwu", "光武崩"): "57",
        ("e-han-guangwu", "封禅"): "56",
        ("han-wu-di", "马邑"): "-133",
        ("han-wu-di", "巫蛊"): "-91",
        ("han-wu-di", "轮台"): "-89",
        ("qin-shi-huang", "称始皇帝"): "-221",
        ("qin-shi-huang", "沙丘崩"): "-210",
        ("tang-tai-zong", "玄武"): "626",
        ("shu-zhaolie", "夷陵"): "222",
        ("w-jin-hui", "肉糜"): "undated",  # may be undated anecdote
        ("sui-yang", "江都之变"): "618",
        ("sui-yang", "幸江都"): "616",
        ("xin-wang-mang", "称帝"): "9",
        ("e-han-ming", "云台"): "60",  # 永平中 ~60; may be 58-75 range
    }
    problems = []
    for pid in PIDS:
        cards = []
        for f in sorted((SRC / pid / "证据").glob("E*.md")):
            if f.name == "_template.md":
                continue
            t = f.read_text(encoding="utf-8")
            meta = {}
            for line in t.split("---", 2)[1].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"')
            cards.append(meta)
        for (ep, key), ey in expect.items():
            if ep != pid:
                continue
            hit = next(
                (c for c in cards if key in c.get("title", "")),
                None,
            )
            if not hit:
                problems.append(f"MISS {pid} key={key}")
                continue
            y = hit.get("year", "")
            if ey == "undated":
                continue
            if y != ey:
                # allow loose match for 云台 永平中
                if key == "云台" and y in ("60", "58", "61", "62", "65", "undated"):
                    continue
                problems.append(
                    f"YEAR {pid}「{hit.get('title')}」got {y} expect {ey}"
                )
    return problems


def same_year_death_before_event() -> list[str]:
    """Flag death card before same-or-earlier life event when years wrong."""
    out = []
    for d in sorted(SRC.iterdir()):
        if not d.is_dir():
            continue
        p0 = d / "00-史源卡.md"
        if not p0.exists():
            continue
        st = ""
        for line in p0.read_text(encoding="utf-8").splitlines()[:20]:
            if line.startswith("status:"):
                st = line.split(":", 1)[1].strip()
        if st != "dossier-complete":
            continue
        cards = []
        for f in sorted((d / "证据").glob("E*.md")):
            if f.name == "_template.md":
                continue
            t = f.read_text(encoding="utf-8")
            meta = {}
            for line in t.split("---", 2)[1].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"')
            cards.append(meta)
        death_i = None
        death_y = None
        for i, c in enumerate(cards):
            if any(x in c.get("title", "") for x in ("崩", "被弑", "被杀", "禅位", "逊位", "降魏", "降晋")):
                try:
                    death_y = int(c.get("year", "x"))
                    death_i = i
                    break
                except ValueError:
                    pass
        if death_i is None or death_y is None:
            continue
        for c in cards[death_i + 1 :]:
            try:
                y = int(c.get("year", "x"))
            except ValueError:
                continue
            if y < death_y and y > 0:
                out.append(
                    f"AFTER_DEATH {d.name}: death@{death_y} then "
                    f"{c.get('eid')} {c.get('title')} year={y}"
                )
            if 0 > y > death_y:  # BCE death more negative? skip complex
                pass
    return out


def main():
    for pid in PIDS:
        dump(pid)
    print("\n## known year anchors")
    for p in check_known_facts():
        print("!", p)
    print("\n## events after death (by year)")
    after = same_year_death_before_event()
    for p in after[:40]:
        print("!", p)
    print("count_after_death", len(after))


if __name__ == "__main__":
    main()
