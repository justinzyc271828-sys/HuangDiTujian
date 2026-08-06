import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import type { Emperor, SiteData } from "../types";
import type { StandStatsFile, StyleId } from "../standTypes";
import StandRadar from "../components/StandRadar";
import "../standLab.css";

type Props = { site: SiteData };

const STYLES: {
  id: StyleId;
  name: string;
  blurb: string;
}[] = [
  {
    id: "jojo-dark",
    name: "A · 暗紫替身档",
    blurb: "最接近「设定集/替身介绍页」：黑底、高对比、能力说明+六维。",
  },
  {
    id: "jojo-gold",
    name: "B · 黄金轰传档",
    blurb: "漫画分镜感：粗描边、斜切色块、STAND STATS 排版。",
  },
  {
    id: "memorial",
    name: "C · 奏折×品藻",
    blurb: "宣纸奏折壳 + 嵌一张「品藻雷达」，古意与六维并存。",
  },
  {
    id: "stele",
    name: "D · 金石碑阴",
    blurb: "深碑拓片风，六维像刻在碑阴的参数。",
  },
  {
    id: "tcg",
    name: "E · 集换卡牌",
    blurb: "卡牌边框+稀有度，适合图鉴收集感。",
  },
];

function gradeOf(v: number, grades: string[]) {
  return grades[Math.max(0, Math.min(5, Math.round(v)))] ?? String(v);
}

export default function StandLab({ site }: Props) {
  const [stats, setStats] = useState<StandStatsFile | null>(null);
  const [style, setStyle] = useState<StyleId>("jojo-dark");
  const [eid, setEid] = useState(site.featured_ids[0] || "qin-shi-huang");

  useEffect(() => {
    fetch("/data/stand_stats.json")
      .then((r) => r.json())
      .then(setStats)
      .catch(() => setStats(null));
  }, []);

  const emperor = useMemo(
    () => site.emperors.find((e) => e.id === eid) as Emperor | undefined,
    [site, eid]
  );

  const profile = stats?.profiles[eid];
  const featured = site.featured_ids
    .map((id) => site.emperors.find((e) => e.id === id))
    .filter(Boolean) as Emperor[];

  if (!stats || !emperor || !profile) {
    return (
      <div className="lab-wrap">
        <p className="lab-loading">加载替身档数据…</p>
        <Link to="/">← 返回图鉴</Link>
      </div>
    );
  }

  const theme = style;

  return (
    <div className={`lab-wrap theme-${theme}`}>
      <header className="lab-top">
        <div>
          <Link to="/" className="lab-back">
            ← 返回图鉴
          </Link>
          <h1>专页视觉实验 · 替身档 Lab</h1>
          <p className="lab-lead">
            模仿「角色设定页 + 六维能力图」的初级多版方案（非官方联名）。评分 1–5
            仅供品藻演示。点选风格与人物对比。
          </p>
        </div>
      </header>

      <section className="lab-picker">
        <h2>① 选风格</h2>
        <div className="lab-style-grid">
          {STYLES.map((s) => (
            <button
              key={s.id}
              type="button"
              className={`lab-style-card ${style === s.id ? "on" : ""}`}
              onClick={() => setStyle(s.id)}
            >
              <strong>{s.name}</strong>
              <span>{s.blurb}</span>
            </button>
          ))}
        </div>
      </section>

      <section className="lab-picker">
        <h2>② 选人物（首批三人）</h2>
        <div className="lab-emp-tabs">
          {featured.map((e) => (
            <button
              key={e.id}
              type="button"
              className={eid === e.id ? "on" : ""}
              onClick={() => setEid(e.id)}
            >
              {e.names.display}
            </button>
          ))}
        </div>
      </section>

      <section className="lab-stage">
        <h2>③ 预览 · {STYLES.find((s) => s.id === style)?.name}</h2>

        {/* ========== A jojo-dark ========== */}
        {style === "jojo-dark" && (
          <article className="sheet sheet-dark">
            <div className="sheet-dark-grid">
              <div className="sd-left">
                <div className="sd-portrait">
                  <span className="sd-portrait-label">USER</span>
                  <strong>{emperor.names.display}</strong>
                  <em>{emperor.names.personal}</em>
                  <small>
                    {emperor.dynasty.label} · {emperor.reign.start}–{emperor.reign.end}
                  </small>
                </div>
                <div className="sd-stand-name">{profile.stand_name}</div>
                <div className="sd-type">{profile.stand_type}</div>
                <blockquote className="sd-cry">「{profile.cry}」</blockquote>
              </div>
              <div className="sd-right">
                <div className="sd-stats-title">
                  STAND STATS
                  <span>六维品藻</span>
                </div>
                <StandRadar
                  axes={stats.axes}
                  scores={profile.scores}
                  grades={stats.grades}
                  size={300}
                />
                <ul className="sd-axis-list">
                  {stats.axes.map((ax) => (
                    <li key={ax.key}>
                      <span className="k">
                        {ax.label}
                        <i>（{ax.jojo}）</i>
                      </span>
                      <span className="g">
                        {gradeOf(profile.scores[ax.key] ?? 0, stats.grades)}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            <div className="sd-bottom">
              <div>
                <h3>ABILITY</h3>
                <p>{profile.ability}</p>
              </div>
              <div>
                <h3>WEAKNESS</h3>
                <p>{profile.weakness}</p>
              </div>
              <div>
                <h3>SUMMARY</h3>
                <p>{emperor.summary}</p>
              </div>
            </div>
            <p className="sheet-disclaimer">{stats.note}</p>
          </article>
        )}

        {/* ========== B jojo-gold ========== */}
        {style === "jojo-gold" && (
          <article className="sheet sheet-gold">
            <div className="sg-banner">
              <span>EMPEROR STAND</span>
              <span>{profile.stand_name}</span>
            </div>
            <div className="sg-body">
              <div className="sg-col">
                <div className="sg-user-box">
                  <div className="sg-slash" />
                  <h3>{emperor.names.display}</h3>
                  <p>
                    {emperor.dynasty.label} / {emperor.names.personal}
                  </p>
                  <p className="sg-years">
                    {emperor.reign.start} → {emperor.reign.end}
                  </p>
                </div>
                <div className="sg-ability">
                  <h4>必杀概念</h4>
                  <p>{profile.ability}</p>
                  <h4>破绽</h4>
                  <p>{profile.weakness}</p>
                </div>
              </div>
              <div className="sg-radar-wrap">
                <StandRadar
                  axes={stats.axes}
                  scores={profile.scores}
                  grades={stats.grades}
                  size={320}
                  stroke="#ffe566"
                  fill="rgba(255,100,60,0.45)"
                  grid="rgba(0,0,0,0.35)"
                  labelColor="#1a1208"
                />
              </div>
              <div className="sg-param">
                <h4>PARAMETERS</h4>
                {stats.axes.map((ax) => (
                  <div className="sg-bar" key={ax.key}>
                    <div className="sg-bar-top">
                      <span>{ax.label}</span>
                      <b>{gradeOf(profile.scores[ax.key] ?? 0, stats.grades)}</b>
                    </div>
                    <div className="sg-bar-track">
                      <i
                        style={{
                          width: `${((profile.scores[ax.key] ?? 0) / 5) * 100}%`,
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <p className="sg-cry">「{profile.cry}」</p>
            <p className="sheet-disclaimer">{stats.note}</p>
          </article>
        )}

        {/* ========== C memorial ========== */}
        {style === "memorial" && (
          <article className="sheet sheet-memo">
            <div className="sm-seal">品藻</div>
            <header className="sm-head">
              <h3>
                {emperor.dynasty.label}·{emperor.names.display}
              </h3>
              <p>
                {emperor.names.personal}
                {emperor.names.posthumous
                  ? ` · ${emperor.names.posthumous}`
                  : ""}
              </p>
              <p className="sm-reign">
                在位 {emperor.reign.start} — {emperor.reign.end}
              </p>
            </header>
            <p className="sm-summary">{emperor.summary}</p>
            <div className="sm-split">
              <div className="sm-text">
                <h4>替身化设定（戏作）</h4>
                <p>
                  <strong>{profile.stand_name}</strong> · {profile.stand_type}
                </p>
                <p>{profile.ability}</p>
                <p className="sm-weak">破绽：{profile.weakness}</p>
                <p className="sm-cry">「{profile.cry}」</p>
              </div>
              <div className="sm-radar">
                <StandRadar
                  axes={stats.axes}
                  scores={profile.scores}
                  grades={stats.grades}
                  size={280}
                  stroke="#8b1e1e"
                  fill="rgba(139,30,30,0.2)"
                  grid="rgba(90,70,40,0.25)"
                  labelColor="#3a2f22"
                />
              </div>
            </div>
            <table className="sm-table">
              <tbody>
                {stats.axes.map((ax) => (
                  <tr key={ax.key}>
                    <td>
                      {ax.label}
                      <small>{ax.jojo}</small>
                    </td>
                    <td>{gradeOf(profile.scores[ax.key] ?? 0, stats.grades)}</td>
                    <td>{ax.desc}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p className="sheet-disclaimer">{stats.note}</p>
          </article>
        )}

        {/* ========== D stele ========== */}
        {style === "stele" && (
          <article className="sheet sheet-stele">
            <div className="st-title">{emperor.names.display}</div>
            <div className="st-sub">
              {profile.stand_name} · {profile.stand_type}
            </div>
            <div className="st-body">
              <StandRadar
                axes={stats.axes}
                scores={profile.scores}
                grades={stats.grades}
                size={300}
                stroke="#c9b896"
                fill="rgba(201,184,150,0.2)"
                grid="rgba(180,170,150,0.2)"
                labelColor="#d8d0c0"
              />
              <div className="st-inscript">
                <p>{profile.cry}</p>
                <p>{profile.ability}</p>
                <p>破：{profile.weakness}</p>
                <ul>
                  {stats.axes.map((ax) => (
                    <li key={ax.key}>
                      {ax.label}　
                      <b>{gradeOf(profile.scores[ax.key] ?? 0, stats.grades)}</b>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            <p className="sheet-disclaimer">{stats.note}</p>
          </article>
        )}

        {/* ========== E tcg ========== */}
        {style === "tcg" && (
          <article className="sheet sheet-tcg">
            <div className="tcg-card">
              <div className="tcg-top">
                <span className="tcg-rare">SSR</span>
                <span className="tcg-cost">
                  {emperor.dynasty.label}
                </span>
              </div>
              <div className="tcg-art">
                <span>{emperor.names.display}</span>
                <small>{profile.stand_name}</small>
              </div>
              <div className="tcg-name">
                {emperor.names.display}
                <em>{profile.stand_type}</em>
              </div>
              <div className="tcg-radar">
                <StandRadar
                  axes={stats.axes}
                  scores={profile.scores}
                  grades={stats.grades}
                  size={240}
                  stroke="#6b21a8"
                  fill="rgba(107,33,168,0.25)"
                  grid="rgba(80,60,40,0.2)"
                  labelColor="#3b2f1e"
                />
              </div>
              <div className="tcg-text">
                <p className="tcg-effect">
                  <b>效果</b> {profile.ability}
                </p>
                <p className="tcg-flavor">「{profile.cry}」</p>
              </div>
              <div className="tcg-footer">
                {stats.axes.map((ax) => (
                  <span key={ax.key}>
                    {ax.label}
                    {gradeOf(profile.scores[ax.key] ?? 0, stats.grades)}
                  </span>
                ))}
              </div>
            </div>
            <p className="sheet-disclaimer">{stats.note}</p>
          </article>
        )}
      </section>

      <section className="lab-axes-help">
        <h2>六维对照（JoJo 参数 ←→ 史样品藻）</h2>
        <table>
          <thead>
            <tr>
              <th>品藻</th>
              <th>对应替身感</th>
              <th>含义</th>
            </tr>
          </thead>
          <tbody>
            {stats.axes.map((ax) => (
              <tr key={ax.key}>
                <td>{ax.label}</td>
                <td>{ax.jojo}</td>
                <td>{ax.desc}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
