import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import type { Emperor, SiteData } from "../types";
import type { StandStatsFile, StyleId } from "../standTypes";
import StandRadar from "../components/StandRadar";
import "../standLab.css";

type Props = { site: SiteData };

const STYLES: { id: StyleId; name: string; blurb: string; vibe: string }[] = [
  {
    id: "rpg-menu",
    name: "A · JRPG 状态菜单",
    vibe: "组队出战",
    blurb: "像打开了队伍界面：HP/MP 玩笑条、技能栏、六维雷达。史实在，包装是游戏。",
  },
  {
    id: "gacha",
    name: "B · 抽卡角色详情",
    vibe: "限定 UP",
    blurb: "手机二游角色页：立绘区、命座感、技能图标槽、六维。收集欲拉满。",
  },
  {
    id: "boss-raid",
    name: "C · 世界 BOSS 讨伐页",
    vibe: "团本点名",
    blurb: "像打开了副本手册：威胁等级、机制点名、狂暴提示 + 六维。",
  },
  {
    id: "dex",
    name: "D · 怪物体图鉴",
    vibe: "已登录 No.",
    blurb: "宝可梦式图鉴机：编号、属性标签、身高玩笑、捕获度 + 六维。",
  },
  {
    id: "fighter",
    name: "E · 格斗家选人",
    vibe: "VS",
    blurb: "大乱斗/无双选人：大头像、必杀名、连招梗 + 六维。对战感强。",
  },
];

function gradeOf(v: number, grades: string[]) {
  return grades[Math.max(0, Math.min(5, Math.round(v)))] ?? String(v);
}

function sumScores(scores: Record<string, number>) {
  return Object.values(scores).reduce((a, b) => a + b, 0);
}

function powerLevel(scores: Record<string, number>) {
  const s = sumScores(scores);
  // 6*5=30 max
  if (s >= 27) return "SSS";
  if (s >= 24) return "SS";
  if (s >= 21) return "S";
  if (s >= 18) return "A";
  if (s >= 15) return "B";
  return "C";
}

export default function StandLab({ site }: Props) {
  const [stats, setStats] = useState<StandStatsFile | null>(null);
  const [style, setStyle] = useState<StyleId>("rpg-menu");
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
        <p className="lab-loading">加载设定档…</p>
        <Link to="/">← 返回图鉴</Link>
      </div>
    );
  }

  const pl = powerLevel(profile.scores);
  const total = sumScores(profile.scores);
  const no = String(
    site.emperors.findIndex((e) => e.id === eid) + 1
  ).padStart(3, "0");

  return (
    <div className={`lab-wrap theme-${style}`}>
      <header className="lab-top">
        <div>
          <Link to="/" className="lab-back">
            ← 返回图鉴
          </Link>
          <h1>游戏化设定页 Lab · 第二轮</h1>
          <p className="lab-lead">
            史实骨架仍准，外壳按<strong>好玩的游戏图鉴</strong>来——不是考据论文。
            六维保留；下面 5 套都是「娱乐展示」。点风格 + 人物对比。
          </p>
        </div>
      </header>

      <section className="lab-picker">
        <h2>① 选风格（本轮全换新）</h2>
        <div className="lab-style-grid">
          {STYLES.map((s) => (
            <button
              key={s.id}
              type="button"
              className={`lab-style-card ${style === s.id ? "on" : ""}`}
              onClick={() => setStyle(s.id)}
            >
              <em className="lab-vibe">{s.vibe}</em>
              <strong>{s.name}</strong>
              <span>{s.blurb}</span>
            </button>
          ))}
        </div>
      </section>

      <section className="lab-picker">
        <h2>② 选人物</h2>
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

        {/* A JRPG */}
        {style === "rpg-menu" && (
          <article className="sheet sheet-rpg">
            <div className="rpg-window rpg-header">
              <span>PARTY STATUS</span>
              <span>EMPEROR ATLAS</span>
            </div>
            <div className="rpg-main">
              <div className="rpg-left">
                <div className="rpg-portrait">
                  <div className="rpg-face">{emperor.names.display[0]}</div>
                  <div>
                    <b>{emperor.names.display}</b>
                    <small>Lv.{Math.round(total / 3)} · {pl} 阶</small>
                  </div>
                </div>
                <div className="rpg-bars">
                  <div className="rpg-bar">
                    <span>国力 HP</span>
                    <i style={{ width: `${(profile.scores.endurance / 5) * 100}%` }} />
                  </div>
                  <div className="rpg-bar mp">
                    <span>气运 MP</span>
                    <i style={{ width: `${(profile.scores.legacy / 5) * 100}%` }} />
                  </div>
                </div>
                <div className="rpg-skills">
                  <h4>技能（史实梗）</h4>
                  <button type="button">{profile.stand_name}</button>
                  <button type="button">必杀：{profile.cry.slice(0, 12)}…</button>
                  <button type="button" className="dim">
                    破绽：{profile.weakness.slice(0, 14)}…
                  </button>
                </div>
              </div>
              <div className="rpg-center">
                <StandRadar
                  axes={stats.axes}
                  scores={profile.scores}
                  grades={stats.grades}
                  size={300}
                  stroke="#7dd3fc"
                  fill="rgba(56,189,248,0.35)"
                  grid="rgba(147,197,253,0.25)"
                  labelColor="#e0f2fe"
                />
              </div>
              <div className="rpg-right">
                <h4>STATUS</h4>
                {stats.axes.map((ax) => (
                  <div key={ax.key} className="rpg-stat-row">
                    <span>{ax.label}</span>
                    <b>{gradeOf(profile.scores[ax.key] ?? 0, stats.grades)}</b>
                  </div>
                ))}
                <p className="rpg-note">{profile.ability}</p>
              </div>
            </div>
            <p className="sheet-disclaimer">玩法包装 · {stats.note}</p>
          </article>
        )}

        {/* B Gacha */}
        {style === "gacha" && (
          <article className="sheet sheet-gacha">
            <div className="gacha-bg-orb" />
            <div className="gacha-layout">
              <div className="gacha-left">
                <div className="gacha-stars">{"★".repeat(5)}</div>
                <div className="gacha-portrait">
                  <span className="gacha-elem">
                    {emperor.dynasty.label}
                  </span>
                  <div className="gacha-name">{emperor.names.display}</div>
                  <div className="gacha-title">{profile.stand_name}</div>
                  <div className="gacha-constellation">
                    {[0, 1, 2, 3, 4, 5].map((i) => (
                      <i key={i} className={i < 3 ? "on" : ""} />
                    ))}
                  </div>
                </div>
                <div className="gacha-tags">
                  {(emperor.tags || []).slice(0, 4).map((t) => (
                    <span key={t}>{t}</span>
                  ))}
                  <span className="up">限定</span>
                </div>
              </div>
              <div className="gacha-right">
                <div className="gacha-panel">
                  <h4>角色简介</h4>
                  <p>{emperor.summary}</p>
                </div>
                <div className="gacha-panel gacha-skill">
                  <h4>元素爆发 · 史实技</h4>
                  <p className="gacha-skill-name">{profile.ability}</p>
                  <p className="gacha-weak">命座吐槽：{profile.weakness}</p>
                </div>
                <div className="gacha-radar-box">
                  <StandRadar
                    axes={stats.axes}
                    scores={profile.scores}
                    grades={stats.grades}
                    size={260}
                    stroke="#f9a8d4"
                    fill="rgba(244,114,182,0.35)"
                    grid="rgba(255,255,255,0.2)"
                    labelColor="#fce7f3"
                  />
                </div>
              </div>
            </div>
            <p className="gacha-banner-text">「{profile.cry}」</p>
            <p className="sheet-disclaimer">玩法包装 · {stats.note}</p>
          </article>
        )}

        {/* C Boss raid */}
        {style === "boss-raid" && (
          <article className="sheet sheet-boss">
            <div className="boss-top">
              <div>
                <span className="boss-pill">WORLD BOSS</span>
                <span className="boss-pill red">威胁 {pl}</span>
              </div>
              <span className="boss-id">ID #{no}</span>
            </div>
            <h3 className="boss-name">
              {emperor.names.display}
              <small>{profile.stand_type}</small>
            </h3>
            <div className="boss-hp">
              <span>气运条</span>
              <div className="boss-hp-track">
                <i style={{ width: `${(total / 30) * 100}%` }} />
              </div>
              <span>
                {total}/30
              </span>
            </div>
            <div className="boss-grid">
              <div className="boss-mech">
                <h4>机制点名（史实向）</h4>
                <ol>
                  <li>
                    <b>开场技</b> {profile.ability}
                  </li>
                  <li>
                    <b>狂暴台词</b> 「{profile.cry}」
                  </li>
                  <li>
                    <b>狂暴破绽</b> {profile.weakness}
                  </li>
                  <li>
                    <b>掉落暗示</b> 郡县制 / 年号 / 天可汗（按人不同梗，此处示意）
                  </li>
                </ol>
              </div>
              <div className="boss-radar">
                <StandRadar
                  axes={stats.axes}
                  scores={profile.scores}
                  grades={stats.grades}
                  size={280}
                  stroke="#f87171"
                  fill="rgba(248,113,113,0.3)"
                  grid="rgba(252,165,165,0.25)"
                  labelColor="#fecaca"
                />
              </div>
            </div>
            <div className="boss-loot">
              {stats.axes.map((ax) => (
                <div key={ax.key}>
                  <span>{ax.label}</span>
                  <b>{gradeOf(profile.scores[ax.key] ?? 0, stats.grades)}</b>
                </div>
              ))}
            </div>
            <p className="sheet-disclaimer">玩法包装 · {stats.note}</p>
          </article>
        )}

        {/* D Dex */}
        {style === "dex" && (
          <article className="sheet sheet-dex">
            <div className="dex-frame">
              <div className="dex-screen">
                <div className="dex-topbar">
                  <span>EMPEROR DEX</span>
                  <span>No.{no}</span>
                </div>
                <div className="dex-row">
                  <div className="dex-sprite">
                    <div className="dex-ball">{emperor.names.display[0]}</div>
                    <div className="dex-types">
                      <i className="t1">{emperor.dynasty.label}</i>
                      <i className="t2">{profile.stand_type.slice(0, 4)}</i>
                    </div>
                  </div>
                  <div className="dex-info">
                    <h3>{emperor.names.display}</h3>
                    <p className="dex-species">{profile.stand_name}</p>
                    <p>{emperor.summary}</p>
                    <div className="dex-meta">
                      <span>身高：？？丈（玩笑）</span>
                      <span>
                        捕获度：{10 - (profile.scores.control || 3)}
                      </span>
                      <span>
                        出现地：{emperor.reign.start}–{emperor.reign.end}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="dex-bottom">
                  <StandRadar
                    axes={stats.axes}
                    scores={profile.scores}
                    grades={stats.grades}
                    size={240}
                    stroke="#4ade80"
                    fill="rgba(74,222,128,0.3)"
                    grid="rgba(255,255,255,0.15)"
                    labelColor="#dcfce7"
                  />
                  <div className="dex-entry">
                    <h4>图鉴说明</h4>
                    <p>{profile.ability}</p>
                    <p className="dex-cry">「{profile.cry}」</p>
                    <p className="dex-weak">野生习性：{profile.weakness}</p>
                    <ul>
                      {stats.axes.map((ax) => (
                        <li key={ax.key}>
                          {ax.label}{" "}
                          <b>
                            {gradeOf(profile.scores[ax.key] ?? 0, stats.grades)}
                          </b>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
              <div className="dex-hinge" />
              <div className="dex-leds">
                <i />
                <i />
                <i />
              </div>
            </div>
            <p className="sheet-disclaimer">玩法包装 · {stats.note}</p>
          </article>
        )}

        {/* E Fighter */}
        {style === "fighter" && (
          <article className="sheet sheet-fighter">
            <div className="ft-vs">
              <div className="ft-side p1">
                <div className="ft-portrait">
                  <span>{emperor.names.display}</span>
                </div>
                <div className="ft-nameplate">
                  <b>{emperor.names.display}</b>
                  <em>{emperor.names.personal}</em>
                </div>
              </div>
              <div className="ft-center">
                <div className="ft-vs-badge">VS</div>
                <div className="ft-pl">战力 {pl}</div>
                <StandRadar
                  axes={stats.axes}
                  scores={profile.scores}
                  grades={stats.grades}
                  size={250}
                  stroke="#facc15"
                  fill="rgba(250,204,21,0.25)"
                  grid="rgba(255,255,255,0.2)"
                  labelColor="#fef9c3"
                />
              </div>
              <div className="ft-side p2 ghost">
                <div className="ft-portrait ghost-p">
                  <span>？？？</span>
                </div>
                <div className="ft-nameplate">
                  <b>下一任对手</b>
                  <em>从图鉴挑选</em>
                </div>
              </div>
            </div>
            <div className="ft-moves">
              <div>
                <h4>必杀技</h4>
                <p className="ft-super">{profile.stand_name}</p>
                <p>{profile.ability}</p>
              </div>
              <div>
                <h4>连招台词</h4>
                <p>「{profile.cry}」</p>
              </div>
              <div>
                <h4>被克制</h4>
                <p>{profile.weakness}</p>
              </div>
            </div>
            <div className="ft-params">
              {stats.axes.map((ax) => (
                <span key={ax.key}>
                  {ax.label}
                  <b>{gradeOf(profile.scores[ax.key] ?? 0, stats.grades)}</b>
                </span>
              ))}
            </div>
            <p className="sheet-disclaimer">玩法包装 · {stats.note}</p>
          </article>
        )}
      </section>

      <section className="lab-axes-help">
        <h2>六维仍是这些（史实向含义 / 游戏向别名）</h2>
        <table>
          <thead>
            <tr>
              <th>品藻</th>
              <th>游戏感别名</th>
              <th>含义（认真）</th>
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
        <p className="lab-lead" style={{ marginTop: "0.75rem" }}>
          选好风格字母回我；可组合例如「D 的图鉴机当总览，点进去用 A 状态菜单」。
        </p>
      </section>
    </div>
  );
}
