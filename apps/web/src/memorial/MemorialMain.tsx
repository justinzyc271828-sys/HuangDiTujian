import { Link } from "react-router-dom";
import type { Emperor, SiteData } from "../types";
import type { StandAxis, StandProfile } from "../standTypes";
import StandPlate from "./StandPlate";
import { REL_LABEL } from "./memorialUtils";

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
  const byId = Object.fromEntries(site.emperors.map((e) => [e.id, e]));

  return (
    <main className="memorial-main">
      {/* 卷首 */}
      <section className="m-section m-hero" id="m-hero">
        <div className="hero-kicker">
          {emperor.dynasty.label}
          {emperor.names.temple ? ` · 庙号${emperor.names.temple}` : ""}
          {emperor.names.posthumous ? ` · 谥${emperor.names.posthumous}` : ""}
        </div>
        <h1 className="hero-name">{emperor.names.display}</h1>
        <div className="hero-sub">
          {emperor.names.personal || "—"} · 在位 {emperor.reign.start}—{emperor.reign.end}
        </div>
        <p className="hero-summary">{emperor.summary}</p>
        {(emperor.tags || []).length > 0 && (
          <div className="hero-tags">
            {(emperor.tags || []).map((t) => (
              <span key={t} className="hero-tag">
                {t}
              </span>
            ))}
          </div>
        )}
        {emperor.illustration ? (
          <figure className="hero-illu">
            <img src={`/${emperor.illustration}`} alt={`${emperor.names.display}插画（AI 艺术想象）`} />
            <figcaption>AI 史书想象插画 · 岩彩裂壁 · 非考古复原</figcaption>
          </figure>
        ) : (
          <div className="hero-illu hero-illu-empty">
            <span>{isStub ? "索引灰卡 · 待撰写" : "画像待补"}</span>
          </div>
        )}
      </section>

      {/* 六维品藻 */}
      <section className="m-section" id="m-radar">
        <h2 className="m-h2">六维品藻</h2>
        {isStub ? (
          <p className="m-empty">灰卡无品藻。</p>
        ) : (
          <StandPlate axes={axes} profile={profile} />
        )}
      </section>

      {/* 事迹 */}
      <section className="m-section" id="m-bio">
        <h2 className="m-h2">主要事迹</h2>
        <div className="m-bio">
          {(emperor.bio_parts || []).map((part, i) => {
            if (part.type === "text") {
              return <span key={i}>{part.value}</span>;
            }
            const exists = Boolean(byId[part.id]);
            if (!exists) {
              return (
                <span key={i} title="页未建" className="bio-dead">
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
        <h2 className="m-h2">年表大事</h2>
        {(emperor.timeline || []).length === 0 ? (
          <p className="m-empty">暂无年表（stub 或未同步史料卡）。</p>
        ) : (
          <ul className="m-timeline">
            {(emperor.timeline || []).map((ev, i) => {
              const place = ev.place_id ? site.places[ev.place_id] : null;
              const clickable = Boolean(place);
              return (
                <li
                  key={i}
                  className={clickable ? "has-place" : ""}
                  onClick={() => ev.place_id && clickable && onSelectPlace(ev.place_id)}
                  title={clickable ? "点击在地图中高亮" : undefined}
                >
                  <div className="tl-year">
                    {ev.date_note || ev.year}
                    {place ? ` · ${place.names.historical}` : ""}
                    {ev.card_id ? ` · ${ev.card_id}` : ""}
                  </div>
                  <div className="tl-title">{ev.title}</div>
                  <div className="tl-summary">{ev.summary}</div>
                  {ev.related_person_ids && ev.related_person_ids.length > 0 && (
                    <div className="tl-summary">
                      相关：
                      {ev.related_person_ids.map((rid, j) => {
                        const t = byId[rid];
                        return t ? (
                          <span key={rid}>
                            {j > 0 ? "、" : ""}
                            <Link to={`/emperor/${rid}`}>{t.names.display}</Link>
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
        <h2 className="m-h2">关联表</h2>
        {(emperor.relations || []).length === 0 ? (
          <p className="m-empty">暂无关联。</p>
        ) : (
          <table className="m-table">
            <thead>
              <tr>
                <th>类型</th>
                <th>人物</th>
                <th>说明</th>
              </tr>
            </thead>
            <tbody>
              {(emperor.relations || []).map((r, i) => {
                const t = r.target_id ? byId[r.target_id] : null;
                return (
                  <tr key={i}>
                    <td>{REL_LABEL[r.type] || r.type}</td>
                    <td>
                      {t ? <Link to={`/emperor/${t.id}`}>{t.names.display}</Link> : r.note || "（待建）"}
                    </td>
                    <td>{r.note || "—"}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </section>

      {/* 出处 */}
      <section className="m-section" id="m-sources">
        <h2 className="m-h2">史料出处</h2>
        {(emperor.sources || []).length === 0 ? (
          <p className="m-empty">暂无出处。</p>
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
        <p className="m-disclaimer">
          {emperor.portrait?.disclaimer || "画像为艺术想象，非考古复原。"}
          文稿 status={emperor.meta?.status || "draft"}。
        </p>
      </section>
    </main>
  );
}
