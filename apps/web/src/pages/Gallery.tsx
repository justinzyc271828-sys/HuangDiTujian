import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import type { Emperor, SiteData } from "../types";
import { useCollection } from "../hooks/useCollection";
import "./gallery.css";

type Props = { site: SiteData };
type Filter = "all" | "quasi" | "emperor" | "read";

export default function Gallery({ site }: Props) {
  const { read, starred } = useCollection();
  const [filter, setFilter] = useState<Filter>("all");
  const [q, setQ] = useState("");

  const featured = useMemo(
    () => new Set(site.featured_ids),
    [site.featured_ids]
  );

  const stats = site.catalog_stats || {
    total: site.emperors.length,
    stub: 0,
    draft: 0,
    quasi: 0,
    emperor: 0,
  };

  const list = useMemo(() => {
    let xs: Emperor[] = site.emperors;
    if (filter === "quasi") {
      xs = xs.filter((e) => e.tier === "quasi");
    } else if (filter === "emperor") {
      xs = xs.filter((e) => e.tier === "emperor");
    } else if (filter === "read") {
      xs = xs.filter((e) => read.includes(e.id));
    }
    const query = q.trim();
    if (query) {
      xs = xs.filter(
        (e) =>
          e.names.display.includes(query) ||
          e.names.personal.includes(query) ||
          e.id.includes(query) ||
          (e.dynasty.label || "").includes(query)
      );
    }
    return xs;
  }, [site.emperors, filter, read, featured, q]);

  const chips: { id: Filter; label: string }[] = [
    { id: "all", label: `全部 ${stats.total}` },
    { id: "emperor", label: `正式 ${stats.emperor}` },
    { id: "quasi", label: `准 ${stats.quasi}` },
    { id: "read", label: "已读" },
  ];

  return (
    <div className="gallery-root">
      <div className="gallery-inner">
        <header className="g-head">
          <div className="g-title-row">
            <h1 className="g-title">皇帝图鉴</h1>
            <span className="g-seal">索引 {stats.total}</span>
          </div>
          <p className="g-sub">
            奏折三栏专页 · 点卡即入（专页草稿 {stats.draft} · 灰卡 stub {stats.stub} · 准{" "}
            {stats.quasi}）
          </p>
        </header>

        <div className="g-controls">
          <div className="g-chips">
            {chips.map((c) => (
              <button
                key={c.id}
                type="button"
                className={`g-chip ${filter === c.id ? "active" : ""}`}
                onClick={() => setFilter(c.id)}
              >
                {c.label}
              </button>
            ))}
          </div>
          <input
            className="g-search"
            placeholder="搜索姓名 / 朝代 / id…"
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
        </div>

        <div className="g-grid">
          {list.map((e) => {
            const isStub = e.page_status === "stub" || !e.page_status;
            const isFeatured = featured.has(e.id);
            const isQuasi = e.tier === "quasi";
            return (
              <Link
                key={e.id}
                to={`/emperor/${e.id}`}
                className={[
                  "g-card",
                  isStub ? "is-stub" : "is-draft",
                  isFeatured ? "is-featured" : "",
                  isQuasi ? "is-quasi" : "",
                ]
                  .filter(Boolean)
                  .join(" ")}
              >
                {!isStub && e.illustration && (
                  <div className="g-illu">
                    <img src={`/${e.illustration}`} alt="" loading="lazy" />
                  </div>
                )}
                <div className="g-card-body">
                  <div className="g-card-top">
                    <h2 className="g-name">{e.names.display}</h2>
                    <div className="g-badges">
                      {isFeatured && <span className="g-badge b-first">首批</span>}
                      {isStub && <span className="g-badge b-stub">索引</span>}
                      {isQuasi && <span className="g-badge b-quasi">准</span>}
                    </div>
                  </div>
                  <div className="g-meta">
                    {e.dynasty.label}
                    {e.names.personal ? ` · ${e.names.personal}` : ""} ·{" "}
                    {e.reign.start || "?"}—{e.reign.end || "?"}
                  </div>
                  {!isStub && (e.tags || []).length > 0 && (
                    <div className="g-tags">
                      {(e.tags || []).slice(0, 4).map((t) => (
                        <span key={t} className="g-tag">
                          {t}
                        </span>
                      ))}
                    </div>
                  )}
                  {!isStub && <p className="g-summary">{e.summary}</p>}
                  <div className="g-status">
                    {read.includes(e.id) && <span className="st-read">已读</span>}
                    {starred.includes(e.id) && <span className="st-star">收藏</span>}
                    {isStub && <span className="st-wait">待撰写</span>}
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
}
