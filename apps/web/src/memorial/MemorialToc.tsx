import { useMemo } from "react";
import { Link } from "react-router-dom";
import type { Emperor, SiteData } from "../types";
import { STUB_DISABLED, TOC_ITEMS } from "./memorialUtils";
import { dynastyLabel, useLang } from "../i18n";

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
  const { lang, t } = useLang();
  const nameOf = (e: Emperor) =>
    lang === "en" ? (e.names.display_en ?? e.names.display) : e.names.display;
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
    <nav className="memorial-toc" aria-label={t("toc.aria")}>
      <div className="toc-identity">
        <div className="toc-display">{nameOf(emperor)}</div>
        <div className="toc-meta">
          {emperor.names.personal || "—"}
          <br />
          {t("reign")} {emperor.reign.start}—{emperor.reign.end}
        </div>
        <div className="toc-flags">
          {isQuasi && <span className="flag flag-quasi">{t("flag.quasi")}</span>}
          {isStub && <span className="flag flag-stub">stub</span>}
          {isRead && <span className="flag flag-read">{t("flag.read")}</span>}
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
                {t(`toc.${item.id}`)}
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
        {isStar ? t("toc.starred") : t("toc.star")}
      </button>

      <div className="toc-index">
        <div className="toc-index-title">
          {t("toc.index")} · {dynastyLabel(emperor.dynasty.label, lang)}
        </div>
        <ul className="toc-index-list">
          {siblings.map((s) => {
            const current = s.id === emperor.id;
            return (
              <li key={s.id}>
                {current ? (
                  <span className="idx-current">
                    {nameOf(s)}
                    <em>
                      {s.reign.start}—{s.reign.end}
                    </em>
                  </span>
                ) : (
                  <Link className="idx-link" to={`/emperor/${s.id}`}>
                    {nameOf(s)}
                    <em>
                      {s.reign.start}—{s.reign.end}
                    </em>
                    {(s.page_status === "stub" || !s.page_status) && (
                      <i className="idx-stub">{t("toc.stub")}</i>
                    )}
                  </Link>
                )}
              </li>
            );
          })}
        </ul>
        <Link to="/" className="idx-all">
          {t("toc.all")}
        </Link>
      </div>
    </nav>
  );
}
