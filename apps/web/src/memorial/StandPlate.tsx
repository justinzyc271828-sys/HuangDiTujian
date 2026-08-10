import type { StandAxis, StandProfile } from "../standTypes";
import { gradeOfScore } from "./memorialUtils";
import { axisLabel, useLang } from "../i18n";

type Props = {
  axes: StandAxis[];
  profile: StandProfile | null;
};

function polar(cx: number, cy: number, r: number, i: number, n: number) {
  const a = -Math.PI / 2 + (i * 2 * Math.PI) / n;
  return { x: cx + r * Math.cos(a), y: cy + r * Math.sin(a) };
}

function Radar({ axes, scores }: { axes: StandAxis[]; scores: Record<string, number> }) {
  const { lang, t } = useLang();
  const size = 300;
  const cx = size / 2;
  const cy = size / 2;
  const maxR = size * 0.33;
  const n = axes.length;
  const levels = 5;

  const rings = Array.from({ length: levels }, (_, li) => {
    const r = (maxR * (li + 1)) / levels;
    return Array.from({ length: n }, (__, i) => polar(cx, cy, r, i, n))
      .map((p) => `${p.x},${p.y}`)
      .join(" ");
  });

  const valuePts = axes.map((ax, i) => {
    const v = Math.max(0, Math.min(100, scores[ax.key] ?? 0));
    return polar(cx, cy, (maxR * v) / 100, i, n);
  });

  return (
    <svg
      viewBox={`0 0 ${size} ${size}`}
      className="plate-radar"
      role="img"
      aria-label={t("plate.aria")}
    >
      {rings.map((poly, i) => (
        <polygon
          key={i}
          points={poly}
          fill="none"
          stroke="rgba(212,175,106,0.22)"
          strokeWidth={i === levels - 1 ? 1.4 : 1}
        />
      ))}
      {axes.map((_, i) => {
        const p = polar(cx, cy, maxR, i, n);
        return (
          <line
            key={i}
            x1={cx}
            y1={cy}
            x2={p.x}
            y2={p.y}
            stroke="rgba(212,175,106,0.18)"
            strokeWidth={1}
          />
        );
      })}
      <polygon
        points={valuePts.map((p) => `${p.x},${p.y}`).join(" ")}
        fill="rgba(176,141,74,0.30)"
        stroke="#d4af6a"
        strokeWidth={2.2}
        strokeLinejoin="round"
      />
      {valuePts.map((p, i) => (
        <circle key={i} cx={p.x} cy={p.y} r={3.6} fill="#c0392b" stroke="#d4af6a" strokeWidth={1} />
      ))}
      {axes.map((ax, i) => {
        const p = polar(cx, cy, maxR + 26, i, n);
        const v = scores[ax.key] ?? 0;
        return (
          <g key={ax.key}>
            <text x={p.x} y={p.y - 3} textAnchor="middle" fill="#e6d9bd" fontSize={12} fontWeight={700}>
              {lang === "hans" ? ax.label : axisLabel(ax.key, lang)}
            </text>
            <text
              x={p.x}
              y={p.y + 13}
              textAnchor="middle"
              fill="#d4af6a"
              fontSize={13}
              fontWeight={800}
              fontFamily="Georgia, 'Times New Roman', serif"
            >
              {gradeOfScore(v)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

export default function StandPlate({ axes, profile }: Props) {
  const { lang, t } = useLang();
  if (!profile) {
    return (
      <div className="stand-plate plate-empty">
        <div className="plate-name">{t("plate.unrated")}</div>
        <p className="plate-note">{t("plate.unratedNote")}</p>
      </div>
    );
  }
  /* EN 模式内容层逐字段回退中文 */
  const isEn = lang === "en";
  const standName = isEn ? (profile.stand_name_en ?? profile.stand_name) : profile.stand_name;
  const standType = isEn ? (profile.stand_type_en ?? profile.stand_type) : profile.stand_type;
  const cry = isEn ? (profile.cry_en ?? profile.cry) : profile.cry;
  const ability = isEn ? (profile.ability_en ?? profile.ability) : profile.ability;
  const weakness = isEn ? (profile.weakness_en ?? profile.weakness) : profile.weakness;
  return (
    <div className="stand-plate">
      <div className="plate-head">
        <div className="plate-name">{standName}</div>
        <div className="plate-type">{standType}</div>
      </div>
      <div className="plate-body">
        <Radar axes={axes} scores={profile.scores} />
        <ul className="plate-stats">
          {axes.map((ax) => (
            <li key={ax.key}>
              <span className="stat-label">
                {lang === "hans" ? ax.label : axisLabel(ax.key, lang)}
              </span>
              <b className="stat-grade">{gradeOfScore(profile.scores[ax.key] ?? 0)}</b>
            </li>
          ))}
        </ul>
      </div>
      <p className="plate-cry">“{cry}”</p>
      <p className="plate-line">
        <b>{t("plate.merit")}</b> {ability}
      </p>
      <p className="plate-line">
        <b>{t("plate.demerit")}</b> {weakness}
      </p>
      <p className="plate-note">{t("plate.note")}</p>
    </div>
  );
}
