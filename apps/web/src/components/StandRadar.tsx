import type { StandAxis, StandScores } from "../standTypes";
import { axisLabel, useLang } from "../i18n";

type Props = {
  axes: StandAxis[];
  scores: StandScores;
  size?: number;
  stroke?: string;
  fill?: string;
  grid?: string;
  labelColor?: string;
  showGrades?: boolean;
  grades?: string[];
};

function polar(cx: number, cy: number, r: number, i: number, n: number) {
  const a = -Math.PI / 2 + (i * 2 * Math.PI) / n;
  return { x: cx + r * Math.cos(a), y: cy + r * Math.sin(a) };
}

export default function StandRadar({
  axes,
  scores,
  size = 280,
  stroke = "#e8c76b",
  fill = "rgba(232,199,107,0.35)",
  grid = "rgba(255,255,255,0.25)",
  labelColor = "#f5e6c8",
  showGrades = true,
  grades = ["E", "D", "C", "B", "A", "A+"],
}: Props) {
  const { lang, t } = useLang();
  const n = axes.length;
  const cx = size / 2;
  const cy = size / 2;
  const maxR = size * 0.34;
  const levels = 5;

  const rings = Array.from({ length: levels }, (_, li) => {
    const r = (maxR * (li + 1)) / levels;
    const pts = Array.from({ length: n }, (__, i) => polar(cx, cy, r, i, n));
    return pts.map((p) => `${p.x},${p.y}`).join(" ");
  });

  const valuePts = axes.map((ax, i) => {
    const v = Math.max(0, Math.min(5, scores[ax.key] ?? 0));
    const r = (maxR * v) / 5;
    return polar(cx, cy, r, i, n);
  });
  const valuePoly = valuePts.map((p) => `${p.x},${p.y}`).join(" ");

  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      className="stand-radar"
      role="img"
      aria-label={t("radar.aria")}
    >
      {rings.map((poly, i) => (
        <polygon
          key={i}
          points={poly}
          fill="none"
          stroke={grid}
          strokeWidth={i === levels - 1 ? 1.5 : 1}
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
            stroke={grid}
            strokeWidth={1}
          />
        );
      })}
      <polygon
        points={valuePoly}
        fill={fill}
        stroke={stroke}
        strokeWidth={2.5}
        strokeLinejoin="round"
      />
      {valuePts.map((p, i) => (
        <circle key={i} cx={p.x} cy={p.y} r={4} fill={stroke} />
      ))}
      {axes.map((ax, i) => {
        const p = polar(cx, cy, maxR + 28, i, n);
        const v = scores[ax.key] ?? 0;
        const g = showGrades ? grades[Math.max(0, Math.min(5, Math.round(v)))] : String(v);
        return (
          <g key={ax.key}>
            <text
              x={p.x}
              y={p.y - 4}
              textAnchor="middle"
              fill={labelColor}
              fontSize={12}
              fontWeight={700}
            >
              {lang === "hans" ? ax.label : axisLabel(ax.key, lang)}
            </text>
            <text
              x={p.x}
              y={p.y + 12}
              textAnchor="middle"
              fill={stroke}
              fontSize={14}
              fontWeight={800}
              fontFamily="Georgia, 'Times New Roman', serif"
            >
              {g}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
