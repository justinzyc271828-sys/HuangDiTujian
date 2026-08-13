# -*- coding: utf-8 -*-
# postbuild 第二步:把 dist/assets 里的 Noto Serif SC 子集化为项目实际用字。
# 语料 = 站点全部数据文本(index/places/emperor/*.json)+ 前端源码出现的字符
#        (i18n 文案/繁体表/地图标注等)+ 可打印 ASCII,保证简体/繁体/英文全覆盖。
# 文件名保持不变(CSS 里的哈希引用不受影响),仅内容收缩。
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "apps" / "web"
DIST = WEB / "dist"


def collect_corpus() -> str:
    chars: set[str] = set(chr(c) for c in range(0x20, 0x7F))  # 可打印 ASCII

    def eat_text(s: str) -> None:
        chars.update(s)

    def eat_json(obj) -> None:
        if isinstance(obj, str):
            eat_text(obj)
        elif isinstance(obj, list):
            for v in obj:
                eat_json(v)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                eat_text(str(k))
                eat_json(v)

    data = WEB / "public" / "data"
    for f in [data / "index.json", data / "places.json", data / "stand_stats.json"]:
        if f.is_file():
            eat_json(json.loads(f.read_text(encoding="utf-8")))
    emp = data / "emperor"
    if emp.is_dir():
        for f in emp.glob("*.json"):
            eat_json(json.loads(f.read_text(encoding="utf-8")))

    # 源码文本(UI 文案/繁体映射表/地图山河标注等);只取非 ASCII 部分省时间
    for f in (WEB / "src").rglob("*.*"):
        if f.suffix in (".ts", ".tsx", ".css"):
            eat_text(re.sub(r"[\x00-\x7F]", "", f.read_text(encoding="utf-8")))
    idx = WEB / "index.html"
    if idx.is_file():
        eat_text(idx.read_text(encoding="utf-8"))
    return "".join(sorted(chars))


def main() -> int:
    corpus = DIST / "assets" / ".font-corpus.txt"
    corpus.write_text(collect_corpus(), encoding="utf-8")
    total_before = total_after = 0
    for font in sorted((DIST / "assets").glob("*.woff*")):
        flavor = "woff2" if font.suffix == ".woff2" else "woff"
        before = font.stat().st_size
        total_before += before
        tmp = font.with_suffix(font.suffix + ".sub")
        subprocess.run(
            [
                sys.executable, "-m", "fontTools.subset", str(font),
                f"--text-file={corpus}",
                f"--flavor={flavor}",
                f"--output-file={tmp}",
                "--layout-features=*",
            ],
            check=True,
        )
        tmp.replace(font)
        after = font.stat().st_size
        total_after += after
        print(f"  {font.name}: {before // 1024}KB -> {after // 1024}KB")
    corpus.unlink()
    print(f"OK -> fonts subset: {total_before // 1024}KB -> {total_after // 1024}KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
