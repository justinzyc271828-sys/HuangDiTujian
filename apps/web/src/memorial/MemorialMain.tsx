import { Link } from "react-router-dom";
import type { Emperor, SiteData } from "../types";
import type { StandAxis, StandProfile } from "../standTypes";
import StandPlate from "./StandPlate";
import { dynastyLabel, fmtReign, relLabel, useLang } from "../i18n";

type Props = {
  emperor: Emperor;
  site: SiteData;
  axes: StandAxis[];
  profile: StandProfile | null;
  isStub: boolean;
  onSelectPlace: (placeId: string) => void;
};

export default function MemorialMain({
  emperor,
  site,
  axes,
  profile,
  isStub,
  onSelectPlace,
}: Props) {
  const { lang, t } = useLang();
  const byId = Object.fromEntries(site.emperors.map((e) => [e.id, e]));

  /* EN 模式内容层：_en 字段优先，缺失回退中文；hans/hant 不受影响 */
  const isEn = lang === "en";
  const display = isEn ? (emperor.names.display_en ?? emperor.names.display) : emperor.names.display;
  const personal = isEn ? (emperor.names.personal_en ?? emperor.names.personal) : emperor.names.personal;
  const reignText = isEn
    ? fmtReign(emperor.reign.start, emperor.reign.end)
    : `${emperor.reign.start}—${emperor.reign.end}`;
  const summary = isEn ? (emperor.summary_en ?? emperor.summary) : emperor.summary;
  const tags = (isEn ? (emperor.tags_en ?? emperor.tags) : emperor.tags) || [];
  const bioParts = (isEn && emperor.bio_parts_en ? emperor.bio_parts_en : emperor.bio_parts) || [];
  const nameOf = (e: Emperor) => (isEn ? (e.names.display_en ?? e.names.display) : e.names.display);

  return (
    <main className="memorial-main">
      {/* 卷首 */}
      <section className="m-section m-hero" id="m-hero">
        <div className="hero-kicker">
          {dynastyLabel(emperor.dynasty.label, lang)}
          {emperor.names.temple ? ` · ${t("temple")}${emperor.names.temple}` : ""}
          {emperor.names.posthumous ? ` · ${t("posthumous")}${emperor.names.posthumous}` : ""}
        </div>
        <h1 className="hero-name">{display}</h1>
        <div className="hero-sub">
          {personal || "—"} · {t("reign")} {reignText}
        </div>
        <p className="hero-summary">{summary}</p>
        {tags.length > 0 && (
          <div className="hero-tags">
            {tags.map((tag) => (
              <span key={tag} className="hero-tag">
                {tag}
              </span>
            ))}
          </div>
        )}
        {emperor.illustration ? (
          <figure className="hero-illu">
            <img src={`${import.meta.env.BASE_URL}${emperor.illustration}`} alt={t("hero.illuAlt", { name: display })} />
          </figure>
        ) : (
          <div className="hero-illu hero-illu-empty">
            <span>{isStub ? t("hero.stubEmpty") : t("hero.noPortrait")}</span>
          </div>
        )}
      </section>

      {/* 六维品藻 */}
      <section className="m-section" id="m-radar">
        <h2 className="m-h2">{t("sec.radar")}</h2>
        {isStub ? (
          <p className="m-empty">{t("radar.stub")}</p>
        ) : (
          <StandPlate axes={axes} profile={profile} />
        )}
      </section>

      {/* 事迹 */}
      <section className="m-section" id="m-bio">
        <h2 className="m-h2">{t("sec.bio")}</h2>
        <div className="m-bio">
          {bioParts.map((part, i) => {
            if (part.type === "text") {
              return <span key={i}>{part.value}</span>;
            }
            const exists = Boolean(byId[part.id]);
            if (!exists) {
              return (
                <span key={i} title={t("bio.dead")} className="bio-dead">
                  {part.label}
                </span>
              );
            }
            return (
              <Link key={i} className="bio-link" to={`/emperor/${part.id}`}>
                {part.label}
              </Link>
            );
          })}
        </div>
      </section>

      {/* 年表 */}
      <section className="m-section" id="m-timeline">
        <h2 className="m-h2">{t("sec.timeline")}</h2>
        {(emperor.timeline || []).length === 0 ? (
          <p className="m-empty">{t("timeline.empty")}</p>
        ) : (
          <ul className="m-timeline">
            {(emperor.timeline || []).map((ev, i) => {
              const place = ev.place_id ? site.places[ev.place_id] : null;
              const clickable = Boolean(place);
              const evDate = isEn ? (ev.date_note_en ?? ev.date_note) : ev.date_note;
              const evTitle = isEn ? (ev.title_en ?? ev.title) : ev.title;
              const evSummary = isEn ? (ev.summary_en ?? ev.summary) : ev.summary;
              const placeName = place
                ? isEn
                  ? (place.names.english ?? place.names.historical)
                  : place.names.historical
                : "";
              return (
                <li
                  key={i}
                  className={clickable ? "has-place" : ""}
                  onClick={() => ev.place_id && clickable && onSelectPlace(ev.place_id)}
                  title={clickable ? t("timeline.placeHint") : undefined}
                >
                  <div className="tl-year">
                    {evDate || ev.year}
                    {place ? ` · ${placeName}` : ""}
                    {ev.card_id ? ` · ${ev.card_id}` : ""}
                  </div>
                  <div className="tl-title">{evTitle}</div>
                  <div className="tl-summary">{evSummary}</div>
                  {ev.related_person_ids && ev.related_person_ids.length > 0 && (
                    <div className="tl-summary">
                      {t("timeline.related")}
                      {ev.related_person_ids.map((rid, j) => {
                        const t2 = byId[rid];
                        return t2 ? (
                          <span key={rid}>
                            {j > 0 ? "、" : ""}
                            <Link to={`/emperor/${rid}`}>{nameOf(t2)}</Link>
                          </span>
                        ) : (
                          <span key={rid}>{rid}</span>
                        );
                      })}
                    </div>
                  )}
                </li>
              );
            })}
          </ul>
        )}
      </section>

      {/* 关联 */}
      <section className="m-section" id="m-relations">
        <h2 className="m-h2">{t("sec.relations")}</h2>
        {(emperor.relations || []).length === 0 ? (
          <p className="m-empty">{t("relations.empty")}</p>
        ) : (
          <table className="m-table">
            <thead>
              <tr>
                <th>{t("rel.type")}</th>
                <th>{t("rel.person")}</th>
                <th>{t("rel.note")}</th>
              </tr>
            </thead>
            <tbody>
              {(emperor.relations || []).map((r, i) => {
                const t2 = r.target_id ? byId[r.target_id] : null;
                const relNote = isEn ? (r.note_en ?? r.note) : r.note;
                return (
                  <tr key={i}>
                    <td>{relLabel(r.type, lang)}</td>
                    <td>
                      {t2 ? <Link to={`/emperor/${t2.id}`}>{nameOf(t2)}</Link> : relNote || t("rel.pending")}
                    </td>
                    <td>{relNote || "—"}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </section>

      {/* 出处 */}
      <section className="m-section" id="m-sources">
        <h2 className="m-h2">{t("sec.sources")}</h2>
        {(emperor.sources || []).length === 0 ? (
          <p className="m-empty">{t("sources.empty")}</p>
        ) : (
          <ul className="m-sources">
            {(emperor.sources || []).map((s, i) => (
              <li key={i}>
                {s.title}
                {s.note ? ` — ${s.note}` : ""}
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
