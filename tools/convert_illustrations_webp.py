# -*- coding: utf-8 -*-
# 将两个来源目录的成品 PNG 转成网页用 WebP(入库)+ OG 分享卡 JPG 缩略图(入库)。
# 原始 PNG 体量大,仅本地保留,不入库;重跑幂等,直接覆盖同名产物。
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC_DIRS = [
    ROOT / "assets" / "video-01" / "emperor-illustrations" / "outputs",
    ROOT / "key-art-en-prompts-all" / "outputs",
]
OUT = ROOT / "apps" / "web" / "public" / "illustrations"
OG_WIDTH = 1200
WEBP_QUALITY = 82
OG_JPG_QUALITY = 82


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    og_dir = OUT / "og"
    og_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for src in SRC_DIRS:
        if not src.is_dir():
            continue
        for png in sorted(src.glob("*.png")):
            m = re.fullmatch(r"\d+-(.+)\.png", png.name)
            if not m:
                continue
            eid = m.group(1)
            im = Image.open(png).convert("RGB")
            im.save(OUT / f"{eid}.webp", "WEBP", quality=WEBP_QUALITY, method=4)
            if im.width > OG_WIDTH:
                im_og = im.resize((OG_WIDTH, round(im.height * OG_WIDTH / im.width)), Image.LANCZOS)
            else:
                im_og = im
            im_og.save(og_dir / f"{eid}.jpg", "JPEG", quality=OG_JPG_QUALITY, optimize=True, progressive=True)
            n += 1
            if n % 25 == 0:
                print(f"...{n}", flush=True)
    print(f"OK -> {n} illustrations -> {OUT} (+og/)")


if __name__ == "__main__":
    main()
