import { useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import type { SiteData } from "../types";
import { useCollection } from "../hooks/useCollection";
import RouteMap from "../components/RouteMap";

type Props = { site: SiteData };

const REL_LABEL: Record<string, string> = {
  predecessor: "前任",
  successor: "后任",
  kinship: "亲属",
  minister: "权臣/重臣",
  rival: "对手",
  related_emperor: "相关帝王",
  other: "其他",
};

export default function EmperorPage({ site }: Props) {
  const { id } = useParams();
  const { markRead, toggleStar, starred, read } = useCollection();
  const emperor = site.emperors.find((e) => e.id === id);
  const byId = Object.fromEntries(site.emperors.map((e) => [e.id, e]));

  useEffect(() => {
    if (id) markRead(id);
  }, [id, markRead]);

  if (!emperor) {
    return (
      <div className="error">
        未找到人物 <code>{id}</code>。
        <div>
          <Link to="/">返回图鉴</Link>
        </div>
      </div>
    );
  }

  const isStar = starred.includes(emperor.id);
  const isStub =
    emperor.page_status === "stub" || emperor.meta?.page_status === "stub";
  const isQuasi = emperor.tier === "quasi";

  return (
    <>
      <Link className="back" to="/">
        ← 返回图鉴
      </Link>
      <div className="layout-person">
        <article className={`person-main ${isStub ? "person-stub" : ""}`}>
          <div className="person-head">
            <div className="portrait">
              {isStub ? (
                <>
                  索引灰卡
                  <br />
                  待撰写
                </>
              ) : (
                <>
                  画像占位
                  <br />
                  （风格暂缓）
                </>
              )}
            </div>
            <div style={{ flex: 1, minWidth: 200 }}>
              <h1>
                {emperor.names.display}
                {isQuasi ? (
                  <span className="inline-badge quasi">准</span>
                ) : null}
                {isStub ? (
                  <span className="inline-badge stub">stub</span>
                ) : null}
              </h1>
              <div className="meta" style={{ color: "var(--ink-soft)" }}>
                {emperor.dynasty.label}
                {emperor.names.temple ? ` · 庙号${emperor.names.temple}` : ""}
                {emperor.names.posthumous
                  ? ` · ${emperor.names.posthumous}`
                  : ""}
                <br />
                {emperor.names.personal || "—"} · 在位 {emperor.reign.start} —{" "}
                {emperor.reign.end}
                <br />
                id: <code>{emperor.id}</code>
                {read.includes(emperor.id) ? " · 已读" : ""}
              </div>
              <div className="tags" style={{ marginTop: "0.5rem" }}>
                {(emperor.tags || []).map((t) => (
                  <span key={t} className="tag">
                    {t}
                  </span>
                ))}
              </div>
              <div className="person-actions">
                <button
                  type="button"
                  className={`btn ${isStar ? "primary" : ""}`}
                  onClick={() => toggleStar(emperor.id)}
                >
                  {isStar ? "★ 已收藏" : "☆ 收藏"}
                </button>
              </div>
            </div>
          </div>

          {isStub && (
            <div className="stub-banner">
              本页来自<strong>全库索引</strong>，尚无专页史料卡与完整年表。你可先浏览身份信息；内容生产请走{" "}
              <code>content/sources/</code> 工作流。
              {emperor.meta?.note ? (
                <>
                  <br />
                  备注：{emperor.meta.note}
                </>
              ) : null}
            </div>
          )}

          <p style={{ marginTop: 0 }}>{emperor.summary}</p>

          <section className="section">
            <h2>主要事迹</h2>
            <div className="bio">
              {(emperor.bio_parts || []).map((part, i) => {
                if (part.type === "text") {
                  return <span key={i}>{part.value}</span>;
                }
                const exists = Boolean(byId[part.id]);
                if (!exists) {
                  return (
                    <span key={i} title="页未建">
                      {part.label}
                    </span>
                  );
                }
                return (
                  <Link
                    key={i}
                    className="emperor-link"
                    to={`/emperor/${part.id}`}
                  >
                    {part.label}
                  </Link>
                );
              })}
            </div>
          </section>

          <section className="section">
            <h2>年表大事</h2>
            {(emperor.timeline || []).length === 0 ? (
              <p className="meta">暂无年表（stub 或未同步史料卡）。</p>
            ) : (
              <ul className="timeline">
                {(emperor.timeline || []).map((ev, i) => (
                  <li key={i}>
                    <div className="year">
                      {ev.date_note || ev.year}
                      {ev.place_id && site.places[ev.place_id]
                        ? ` · ${site.places[ev.place_id].names.historical}`
                        : ""}
                      {ev.card_id ? ` · ${ev.card_id}` : ""}
                    </div>
                    <div className="title">{ev.title}</div>
                    <div className="summary">{ev.summary}</div>
                    {ev.related_person_ids &&
                      ev.related_person_ids.length > 0 && (
                        <div className="summary">
                          相关：
                          {ev.related_person_ids.map((rid, j) => {
                            const t = byId[rid];
                            return t ? (
                              <span key={rid}>
                                {j > 0 ? "、" : ""}
                                <Link to={`/emperor/${rid}`}>
                                  {t.names.display}
                                </Link>
                              </span>
                            ) : (
                              <span key={rid}>{rid}</span>
                            );
                          })}
                        </div>
                      )}
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section className="section">
            <h2>关联表</h2>
            {(emperor.relations || []).length === 0 ? (
              <p className="meta">暂无关联。</p>
            ) : (
              <table className="table">
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
                          {t ? (
                            <Link to={`/emperor/${t.id}`}>
                              {t.names.display}
                            </Link>
                          ) : (
                            r.note || "（待建）"
                          )}
                        </td>
                        <td>{r.note || "—"}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            )}
          </section>

          <section className="section">
            <h2>史料出处（工作引用）</h2>
            <ul>
              {(emperor.sources || []).map((s, i) => (
                <li key={i}>
                  {s.title}
                  {s.note ? ` — ${s.note}` : ""}
                </li>
              ))}
            </ul>
            <p className="hint" style={{ fontSize: "0.8rem", color: "var(--ink-soft)" }}>
              {emperor.portrait?.disclaimer || "画像为艺术想象，非考古复原。"}
              文稿 status={emperor.meta?.status || "draft"}。
            </p>
          </section>

          <div className="quasi-note">
            准帝王图鉴入口已预留：未来可在总览筛选「准」层级；本 MVP 仅展示正式帝王与关联页。
          </div>
        </article>

        {!isStub && (emperor.routes || []).length > 0 ? (
          <RouteMap emperor={emperor} places={site.places} />
        ) : (
          <aside className="map-panel">
            <h2>一生轨迹</h2>
            <p className="hint">
              {isStub
                ? "灰卡无路线数据。专页完成后将显示示意地图。"
                : "暂无 routes 数据。"}
            </p>
          </aside>
        )}
      </div>
    </>
  );
}
