#!/usr/bin/env python3
"""为 HuangDiTujian-Ref 下 Markdown 史库生成卷目索引，方便写史料卡。"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "HuangDiTujian-Ref"
OUT = REF / "10-索引"
CORPORA = [
    ("二十四史-简体", REF / "01-史书全文与扫描" / "二十四史-简体", "写卡默认（简体）"),
    ("二十四史", REF / "01-史书全文与扫描" / "二十四史", "繁体对照"),
    ("资治通鉴-简体", REF / "01-史书全文与扫描" / "资治通鉴-简体", "编年钉年默认"),
    ("资治通鉴", REF / "01-史书全文与扫描" / "资治通鉴", "繁体对照"),
    ("十三经-简体", REF / "01-史书全文与扫描" / "十三经-简体", "经部辅证"),
    ("十三经", REF / "01-史书全文与扫描" / "十三经", "繁体对照"),
]

H2_RE = re.compile(r"^## (.+)$", re.M)
H3_RE = re.compile(r"^### (.+)$", re.M)


def index_file(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    rows: list[dict] = []
    matches = list(H2_RE.finditer(text))
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chunk = text[start:end]
        h3s = H3_RE.findall(chunk)[:12]
        # 1-based line number
        line = text.count("\n", 0, start) + 1
        rows.append(
            {
                "title": m.group(1).strip(),
                "line": line,
                "chars": end - start,
                "h3": h3s,
            }
        )
    return rows


def write_book_index(corpus_name: str, md_path: Path, note: str) -> Path:
    rows = index_file(md_path)
    out_dir = OUT / corpus_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{md_path.stem}.目录.md"
    lines = [
        f"# 目录 · {md_path.name}",
        "",
        f"- 语料：`{corpus_name}`",
        f"- 源文件：`{md_path.relative_to(REF).as_posix()}`",
        f"- 备注：{note}",
        f"- 二级标题数：{len(rows)}",
        "",
        "| # | 卷/篇标题 | 约行号 | 篇幅(字) | 下辖 ###（节选） |",
        "|---|-----------|--------|----------|------------------|",
    ]
    for i, r in enumerate(rows, 1):
        h3 = "、".join(r["h3"][:6]) if r["h3"] else "—"
        h3 = h3.replace("|", "\\|")
        lines.append(
            f"| {i} | {r['title']} | {r['line']} | {r['chars']} | {h3} |"
        )
    lines.append("")
    lines.append("> 行号为近似定位，用编辑器搜索 `## 标题` 最稳。")
    lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def write_corpus_readme(corpus_name: str, folder: Path, note: str, book_outs: list[Path]) -> None:
    out = OUT / corpus_name / "README.md"
    files = sorted(folder.glob("*.md"))
    lines = [
        f"# {corpus_name}",
        "",
        f"- 路径：`{folder.relative_to(REF).as_posix()}`",
        f"- 用途：{note}",
        f"- 书/文件数：{len(files)}",
        "",
        "## 文件列表",
        "",
        "| 文件 | 大小 | 卷目索引 |",
        "|------|------|----------|",
    ]
    for f in files:
        idx = OUT / corpus_name / f"{f.stem}.目录.md"
        link = f"{f.stem}.目录.md" if idx.exists() else "—"
        lines.append(
            f"| `{f.name}` | {f.stat().st_size/1e6:.2f} MB | [{link}]({link}) |"
        )
    lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")


def write_master() -> None:
    lines = [
        "# 参考库索引总表",
        "",
        "由 `tools/build_ref_indexes.py` 生成。写史料卡时：",
        "",
        "1. 默认用 **简体** 语料（`二十四史-简体`、`资治通鉴-简体`）",
        "2. 打开下方对应「目录」用搜索跳卷",
        "3. 摘句进 `content/sources/{id}/证据/` 或 `摘录/`",
        "4. 繁体目录仅作对照",
        "",
        "## 语料包",
        "",
        "| 语料 | 说明 | 索引 |",
        "|------|------|------|",
    ]
    for name, folder, note in CORPORA:
        if not folder.is_dir():
            continue
        lines.append(
            f"| `{name}` | {note} | [{name}/README.md]({name}/README.md) |"
        )
    lines.append("")
    lines.append("## 三人快捷")
    lines.append("")
    lines.append("见 `../11-史料卡工作台/README.md`")
    lines.append("")
    (OUT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, folder, note in CORPORA:
        if not folder.is_dir():
            print("skip missing", folder)
            continue
        book_outs: list[Path] = []
        for md in sorted(folder.glob("*.md")):
            # skip tiny junk
            if md.stat().st_size < 500:
                continue
            out = write_book_index(name, md, note)
            book_outs.append(out)
            print("OK", out.relative_to(REF))
        write_corpus_readme(name, folder, note, book_outs)
    write_master()
    print("OK", OUT / "README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
