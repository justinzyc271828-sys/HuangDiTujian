import { useMemo } from "react";
import { Link } from "react-router-dom";
import type { Emperor, SiteData } from "../types";
import { STUB_DISABLED, TOC_ITEMS } from "./memorialUtils";

type Props = {
  site: SiteData;
  emperor: Emperor;
  isStub: boolean;
  isQuasi: boolean;
  isRead: boolean;
  isStar: boolean;
  activeSection: string;
  onToggleStar: () => void;
};

export default function MemorialToc({
  site,
  emperor,
  isStub,
  isQuasi,
  isRead,
  isStar,
  activeSection,
  onToggleStar,
}: Props) {
  const jump = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  /* 图鉴索引：同朝代序列（含灰卡），当前人高亮 */
  const siblings = useMemo(() => {
    const key = (e: Emperor) =>
      e.sort_key ?? `${e.dynasty.id}-${String(e.dynasty.sequence ?? 999).padStart(3, "0")}`;
    return site.emperors
      .filter((e) => e.dynasty.id === emperor.dynasty.id)
      .sort((a, b) => key(a).localeCompare(key(b)));
  }, [site.emperors, emperor.dynasty.id]);

  return (
    <nav className="memorial-toc" aria-label="奏折目录">
      <div className="toc-identity">
        <div className="toc-display">{emperor.names.display}</div>
        <div className="toc-meta">
          {emperor.names.personal || "—"}
          <br />
          在位 {emperor.reign.start}—{emperor.reign.end}
        </div>
        <div className="toc-flags">
          {isQuasi && <span className="flag flag-quasi">准</span>}
          {isStub && <span className="flag flag-stub">stub</span>}
          {isRead && <span className="flag flag-read">已读</span>}
        </div>
      </div>

      <ul className="toc-list">
        {TOC_ITEMS.map((item) => {
          const disabled = isStub && STUB_DISABLED.has(item.id);
          return (
            <li key={item.id}>
              <button
                type="button"
                className={`toc-item ${activeSection === item.id ? "active" : ""}`}
                disabled={disabled}
                onClick={() => jump(item.id)}
              >
                {item.label}
              </button>
            </li>
          );
        })}
      </ul>

      <button
        type="button"
        className={`toc-star ${isStar ? "on" : ""}`}
        onClick={onToggleStar}
      >
        {isStar ? "★ 已收藏" : "☆ 收藏"}
      </button>

      <div className="toc-index">
        <div className="toc-index-title">图鉴索引 · {emperor.dynasty.label}</div>
        <ul className="toc-index-list">
          {siblings.map((s) => {
            const current = s.id === emperor.id;
            return (
              <li key={s.id}>
                {current ? (
                  <span className="idx-current">
                    {s.names.display}
                    <em>
                      {s.reign.start}—{s.reign.end}
                    </em>
                  </span>
                ) : (
                  <Link className="idx-link" to={`/emperor/${s.id}`}>
                    {s.names.display}
                    <em>
                      {s.reign.start}—{s.reign.end}
                    </em>
                    {(s.page_status === "stub" || !s.page_status) && (
                      <i className="idx-stub">灰</i>
                    )}
                  </Link>
                )}
              </li>
            );
          })}
        </ul>
        <Link to="/" className="idx-all">
          全部图鉴 →
        </Link>
      </div>
    </nav>
  );
}
