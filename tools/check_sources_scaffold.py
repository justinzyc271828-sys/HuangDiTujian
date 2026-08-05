#!/usr/bin/env python3
"""检查史源卡脚手架是否齐全（不检查正文是否填写）。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "content" / "sources"
REQUIRED_PERSONS = ("qin-shi-huang", "han-wu-di", "tang-tai-zong")
REQUIRED_FILES = (
    "README.md",
    "00-史源卡.md",
    "01-阅读顺序.md",
    "02-书目清单.md",
    "03-地点候选表.md",
    "04-关联人物候选表.md",
    "05-路线草稿.md",
    "06-争议与待考.md",
    "证据/_template.md",
)
REQUIRED_DOCS = (
    "docs/05-史源卡工作规范.md",
    "docs/references/catalogs/权威资源总表.md",
    "docs/references/catalogs/首批三人文献入口.md",
    "docs/references/checklists/材料就绪检查清单.md",
)


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED_DOCS:
        if not (ROOT / rel).is_file():
            errors.append(f"缺少文档: {rel}")

    for pid in REQUIRED_PERSONS:
        base = SOURCES / pid
        if not base.is_dir():
            errors.append(f"缺少人物目录: {pid}")
            continue
        for rel in REQUIRED_FILES:
            p = base / rel
            if not p.is_file():
                errors.append(f"缺少: {pid}/{rel}")

    print(f"检查人物: {', '.join(REQUIRED_PERSONS)}")
    if errors:
        for e in errors:
            print(f"  ERROR {e}")
        print(f"失败: {len(errors)}")
        return 1
    print("脚手架齐全 (ready-to-fill 级)")
    print("下一步: 人工勾选 docs/references/checklists/材料就绪检查清单.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
