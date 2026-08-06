import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import type { Emperor, SiteData } from "../types";
import { useCollection } from "../hooks/useCollection";

type Props = { site: SiteData };
type Filter =
  | "featured"
  | "all"
  | "draft"
  | "stub"
  | "quasi"
  | "emperor"
  | "read";

export default function Gallery({ site }: Props) {
  const { read, starred } = useCollection();
  const [filter, setFilter] = useState<Filter>("featured");
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
    if (filter === "featured") {
      xs = xs.filter((e) => featured.has(e.id));
    } else if (filter === "draft") {
      xs = xs.filter((e) => e.page_status === "draft" || e.page_status === "ready");
    } else if (filter === "stub") {
      xs = xs.filter((e) => e.page_status === "stub" || !e.page_status);
    } else if (filter === "quasi") {
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

  const totalFeatured = site.featured_ids.length;
  const readFeatured = site.featured_ids.filter((id) => read.includes(id)).length;

  const chips: { id: Filter; label: string }[] = [
    { id: "featured", label: "首批三人" },
    { id: "draft", label: "已有专页" },
    { id: "all", label: `全部 ${stats.total}` },
    { id: "emperor", label: `正式 ${stats.emperor}` },
    { id: "quasi", label: `准 ${stats.quasi}` },
    { id: "stub", label: `灰卡 ${stats.stub}` },
    { id: "read", label: "已读" },
  ];

  return (
    <>
      <header className="hero">
        <h1>皇帝图鉴</h1>
        <p>
          索引共 <strong>{stats.total}</strong> 人（专页草稿 {stats.draft} · 灰卡
          stub {stats.stub} · 准 {stats.quasi}）。首批三人有完整事迹/年表/地图；其余为占位灰卡，可点开查看基本信息。
        </p>
      </header>

      <div className="filters">
        {chips.map((c) => (
          <button
            key={c.id}
            type="button"
            className={`chip ${filter === c.id ? "active" : ""}`}
            onClick={() => setFilter(c.id)}
          >
            {c.label}
          </button>
        ))}
      </div>

      <div className="filters" style={{ marginTop: "-0.25rem" }}>
        <input
          className="search"
          placeholder="搜索姓名 / 朝代 / id…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
      </div>

      <p style={{ color: "var(--ink-soft)", fontSize: "0.9rem" }}>
        首批进度：{readFeatured}/{totalFeatured} 已读 · 收藏 {starred.length} ·
        当前列表 {list.length} 人
      </p>

      <div className="grid">
        {list.map((e) => {
          const isStub = e.page_status === "stub" || !e.page_status;
          const isFeatured = featured.has(e.id);
          const isQuasi = e.tier === "quasi";
          return (
            <Link
              key={e.id}
              to={`/emperor/${e.id}`}
              className={[
                "card",
                isFeatured ? "featured" : "",
                isStub ? "stub" : "",
                isQuasi ? "quasi" : "",
              ]
                .filter(Boolean)
                .join(" ")}
            >
              {isFeatured && <span className="badge">首批</span>}
              {isStub && !isFeatured && (
                <span className="badge badge-stub">索引</span>
              )}
              {isQuasi && (
                <span className="badge badge-quasi">准</span>
              )}
              <h2>{e.names.display}</h2>
              <div className="meta">
                {e.dynasty.label}
                {e.names.personal ? ` · ${e.names.personal}` : ""}
                <br />
                {e.reign.start || "?"} — {e.reign.end || "?"}
              </div>
              {!isStub && (
                <div className="tags">
                  {(e.tags || []).slice(0, 4).map((t) => (
                    <span key={t} className="tag">
                      {t}
                    </span>
                  ))}
                </div>
              )}
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
                {isStub && <span className="stub-label">待撰写</span>}
              </div>
            </Link>
          );
        })}
      </div>
    </>
  );
}
