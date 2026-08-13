# -*- coding: utf-8 -*-
# postbuild:为每位皇帝生成带独立 OG/Twitter 分享卡 meta 的静态页,并产出 404.html 回退。
# 静态托管(GitHub Pages)上爬虫不执行 JS,分享卡 meta 必须落在静态 HTML 里。
# 产物:apps/web/dist/emperor/<id>/index.html ×269 + dist/404.html + sitemap.xml + robots.txt
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "apps" / "web" / "dist"
SITE_JSON = ROOT / "apps" / "web" / "public" / "data" / "index.json"

SITE_ORIGIN = "https://justinzyc271828-sys.github.io"
BASE_PATH = "/HuangDiTujian"
SITE_NAME_ZH = "皇帝图鉴"
DEFAULT_TITLE = "皇帝图鉴 · Imperial Compendium"

META_RE = re.compile(
    r'\s*<meta (?:name="description"|property="og:|name="twitter:)[^>]*>'
)
TITLE_RE = re.compile(r"<title>.*?</title>")


def emperor_meta(e: dict) -> str:
    eid = e["id"]
    display = e["names"]["display"]
    dynasty = e["dynasty"]["label"]
    title = f"{display} · {dynasty} | {SITE_NAME_ZH}"
    desc = (e.get("summary") or "").strip() or title
    url = f"{SITE_ORIGIN}{BASE_PATH}/emperor/{eid}"
    image = f"{SITE_ORIGIN}{BASE_PATH}/illustrations/og/{eid}.jpg"
    t = html.escape(title, quote=True)
    d = html.escape(desc, quote=True)
    return (
        f"<title>{t}</title>\n"
        f'    <meta name="description" content="{d}" />\n'
        f'    <meta property="og:type" content="article" />\n'
        f'    <meta property="og:site_name" content="{SITE_NAME_ZH}" />\n'
        f'    <meta property="og:title" content="{t}" />\n'
        f'    <meta property="og:description" content="{d}" />\n'
        f'    <meta property="og:url" content="{url}" />\n'
        f'    <meta property="og:image" content="{image}" />\n'
        f'    <meta property="og:image:width" content="1200" />\n'
        f'    <meta property="og:image:height" content="675" />\n'
        f'    <meta name="twitter:card" content="summary_large_image" />\n'
        f'    <meta name="twitter:title" content="{t}" />\n'
        f'    <meta name="twitter:description" content="{d}" />\n'
        f'    <meta name="twitter:image" content="{image}" />'
    )


def main() -> None:
    index = (DIST / "index.html").read_text(encoding="utf-8")
    site = json.loads(SITE_JSON.read_text(encoding="utf-8"))
    # 去掉默认 meta,换成每帝专属;保留资源引用等其余 head 内容
    stripped = META_RE.sub("", index)
    n = 0
    for e in site["emperors"]:
        page = TITLE_RE.sub(emperor_meta(e), stripped, count=1)
        out = DIST / "emperor" / e["id"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        n += 1
    # SPA 回退:Pages 对未命中路径返回 404.html,前端路由接管
    shutil.copy2(DIST / "index.html", DIST / "404.html")
    # site.json 全量包仅供工具链,不随站发布(前端走 index/places/emperor 拆包)
    bundled = DIST / "data" / "site.json"
    if bundled.exists():
        bundled.unlink()
    # SEO:sitemap.xml(首页 + lab + 全部帝王页)+ robots.txt 指 sitemap
    urls = [f"{SITE_ORIGIN}{BASE_PATH}/", f"{SITE_ORIGIN}{BASE_PATH}/lab"]
    urls += [f"{SITE_ORIGIN}{BASE_PATH}/emperor/{e['id']}" for e in site["emperors"]]
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    xml += [f"  <url><loc>{html.escape(u)}</loc></url>" for u in urls]
    xml.append("</urlset>")
    (DIST / "sitemap.xml").write_text("\n".join(xml) + "\n", encoding="utf-8")
    (DIST / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_ORIGIN}{BASE_PATH}/sitemap.xml\n",
        encoding="utf-8",
    )
    print(f"OK -> share pages: {n}, 404.html, sitemap.xml ({len(urls)} urls), robots.txt written")


if __name__ == "__main__":
    main()
