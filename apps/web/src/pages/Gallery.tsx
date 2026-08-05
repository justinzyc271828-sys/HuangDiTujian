import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import type { Emperor, SiteData } from "../types";
import { useCollection } from "../hooks/useCollection";

type Props = { site: SiteData };

export default function Gallery({ site }: Props) {
  const { read, starred } = useCollection();
  const [filter, setFilter] = useState<"all" | "featured" | "read">("featured");

  const featured = useMemo(
    () => new Set(site.featured_ids),
    [site.featured_ids]
  );

  const list = useMemo(() => {
    let xs: Emperor[] = site.emperors;
    if (filter === "featured") {
      xs = xs.filter((e) => featured.has(e.id));
    } else if (filter === "read") {
      xs = xs.filter((e) => read.includes(e.id));
    }
    return xs;
  }, [site.emperors, filter, read, featured]);

  const totalFeatured = site.featured_ids.length;
  const readFeatured = site.featured_ids.filter((id) => read.includes(id)).length;

  return (
    <>
      <header className="hero">
        <h1>皇帝图鉴</h1>
        <p>
          最简闭环版：图鉴总览 → 人物卡（事迹 / 年表 / 关联）→ 正文跳转 →
          侧栏示意地图 → 本地收集进度。画像暂用占位。准帝王入口已预留。
        </p>
      </header>

      <div className="filters">
        <button
          type="button"
          className={`chip ${filter === "featured" ? "active" : ""}`}
          onClick={() => setFilter("featured")}
        >
          首批三人
        </button>
        <button
          type="button"
          className={`chip ${filter === "all" ? "active" : ""}`}
          onClick={() => setFilter("all")}
        >
          全部（含关联人物）
        </button>
        <button
          type="button"
          className={`chip ${filter === "read" ? "active" : ""}`}
          onClick={() => setFilter("read")}
        >
          已读
        </button>
        <span className="chip" style={{ cursor: "default", opacity: 0.7 }}>
          准帝王 · 入口预留
        </span>
      </div>

      <p style={{ color: "var(--ink-soft)", fontSize: "0.9rem" }}>
        首批进度：{readFeatured}/{totalFeatured} 已读 · 收藏 {starred.length}
      </p>

      <div className="grid">
        {list.map((e) => (
          <Link
            key={e.id}
            to={`/emperor/${e.id}`}
            className={`card ${featured.has(e.id) ? "featured" : ""}`}
          >
            {featured.has(e.id) && <span className="badge">首批</span>}
            <h2>{e.names.display}</h2>
            <div className="meta">
              {e.dynasty.label} · {e.names.personal}
              <br />
              {e.reign.start} — {e.reign.end}
            </div>
            <div className="tags">
              {(e.tags || []).slice(0, 4).map((t) => (
                <span key={t} className="tag">
                  {t}
                </span>
              ))}
            </div>
            <p className="meta" style={{ margin: 0 }}>
              {e.summary}
            </p>
            <div className="status-row">
              {read.includes(e.id) && (
                <span>
                  <i className="dot read" />
                  已读
                </span>
              )}
              {starred.includes(e.id) && (
                <span>
                  <i className="dot star" />
                  收藏
                </span>
              )}
            </div>
          </Link>
        ))}
      </div>
    </>
  );
}
