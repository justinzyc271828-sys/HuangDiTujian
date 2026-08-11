import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import type { Emperor, SiteData } from "../types";
import { useCollection } from "../hooks/useCollection";
import { dynastyLabel, pinyinOf, useLang } from "../i18n";
import "./gallery.css";

type Props = { site: SiteData };
type Filter = "all" | "quasi" | "emperor" | "read";

export default function Gallery({ site }: Props) {
  const { lang, t } = useLang();
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
    { id: "all", label: `${t("chip.all")} ${stats.total}` },
    { id: "emperor", label: `${t("chip.emperor")} ${stats.emperor}` },
    { id: "quasi", label: `${t("chip.quasi")} ${stats.quasi}` },
    { id: "read", label: t("chip.read") },
  ];

  return (
    <div className="gallery-root">
      <div className="gallery-inner">
        <header className="g-head">
          <div className="g-title-row">
            <h1 className="g-title">{t("gallery.title")}</h1>
            <span className="g-seal">
              {t("gallery.seal")} {stats.total}
            </span>
          </div>
          <p className="g-sub">
            {t("gallery.sub", {
              draft: stats.draft,
              stub: stats.stub,
              quasi: stats.quasi,
            })}
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
            placeholder={t("gallery.searchPh")}
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
        </div>

        <div className="g-grid">
          {list.map((e) => {
            const isStub = e.page_status === "stub" || !e.page_status;
            const isFeatured = featured.has(e.id);
            const isQuasi = e.tier === "quasi";
            const isEn = lang === "en";
            const display = isEn ? (e.names.display_en ?? e.names.display) : e.names.display;
            const tags = (isEn ? (e.tags_en ?? e.tags) : e.tags) || [];
            const summary = isEn ? (e.summary_en ?? e.summary) : e.summary;
            return (
              <Link
                key={e.id}
                to={`/emperor/${e.id}`}
                className={`g-card is-draft ${isFeatured ? "is-featured" : ""} ${isQuasi ? "is-quasi" : ""}`}
              >
                <div className="g-illu">
                  {e.illustration ? (
                    <img src={`/${e.illustration}`} alt="" loading="lazy" />
                  ) : (
                    <div className="g-illu-pending">{t("gallery.portraitPending")}</div>
                  )}
                </div>
                <div className="g-card-body">
                  <div className="g-card-top">
                    <h2 className="g-name">{display}</h2>
                    <div className="g-badges">
                      {isFeatured && <span className="g-badge b-first">{t("badge.first")}</span>}
                      {isStub && <span className="g-badge b-stub">{t("badge.stub")}</span>}
                      {isQuasi && <span className="g-badge b-quasi">{t("badge.quasi")}</span>}
                    </div>
                  </div>
                  {isEn && (
                    <div className="g-pinyin">{e.names.personal_en ?? pinyinOf(e.id)}</div>
                  )}
                  <div className="g-meta">
                    {dynastyLabel(e.dynasty.label, lang)}
                    {e.names.personal ? ` · ${e.names.personal}` : ""} ·{" "}
                    {e.reign.start || "?"}—{e.reign.end || "?"}
                  </div>
                  {tags.length > 0 && (
                    <div className="g-tags">
                      {tags.slice(0, 4).map((t) => (
                        <span key={t} className="g-tag">
                          {t}
                        </span>
                      ))}
                    </div>
                  )}
                  <p className="g-summary">{summary}</p>
                  <div className="g-status">
                    {read.includes(e.id) && <span className="st-read">{t("st.read")}</span>}
                    {starred.includes(e.id) && <span className="st-star">{t("st.star")}</span>}
                    {isStub && <span className="st-wait">{t("st.wait")}</span>}
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
