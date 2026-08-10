import { useMemo, useState } from "react";
import type { Emperor, Place, RoutePoint } from "../types";
import { groupLabel, useLang } from "../i18n";

/** China-ish bbox for schematic projection */
const LNG0 = 73;
const LNG1 = 135;
const LAT0 = 18;
const LAT1 = 54;

const GROUP_COLOR: Record<string, string> = {
  都城: "#2a241c",
  巡狩: "#8b1e1e",
  亲征: "#3d5a45",
  起兵: "#6b4c9a",
  入关: "#b45309",
  其他: "#6b7280",
  迁都: "#0f766e",
  流徙: "#9ca3af",
};

function project(lng: number, lat: number, w: number, h: number, pad = 28) {
  const x = pad + ((lng - LNG0) / (LNG1 - LNG0)) * (w - pad * 2);
  const y = pad + ((LAT1 - lat) / (LAT1 - LAT0)) * (h - pad * 2);
  return { x, y };
}

function arcPath(
  x1: number,
  y1: number,
  x2: number,
  y2: number
): string {
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2;
  const dx = x2 - x1;
  const dy = y2 - y1;
  const len = Math.hypot(dx, dy) || 1;
  const lift = Math.min(40, len * 0.25);
  const cx = mx - (dy / len) * lift;
  const cy = my + (dx / len) * lift;
  return `M ${x1} ${y1} Q ${cx} ${cy} ${x2} ${y2}`;
}

type Props = {
  emperor: Emperor;
  places: Record<string, Place>;
};

export default function RouteMap({ emperor, places }: Props) {
  const { lang, t } = useLang();
  const routes = useMemo(
    () =>
      [...(emperor.routes || [])].sort(
        (a, b) => (a.order ?? 0) - (b.order ?? 0)
      ),
    [emperor.routes]
  );
  const [active, setActive] = useState<number>(0);
  const w = 320;
  const h = 380;

  const pts = routes
    .map((r) => {
      const pl = places[r.place_id];
      if (!pl) return null;
      const { x, y } = project(pl.coords.lng, pl.coords.lat, w, h);
      return { r, pl, x, y };
    })
    .filter(Boolean) as {
    r: RoutePoint;
    pl: Place;
    x: number;
    y: number;
  }[];

  const groups = [...new Set(pts.map((p) => p.r.group))];

  return (
    <div className="map-panel">
      <h2>{t("rmap.title")}</h2>
      <p className="hint">{t("rmap.hint")}</p>
      <div className="map-svg-wrap">
        <svg
          className="map-svg"
          viewBox={`0 0 ${w} ${h}`}
          role="img"
          aria-label={t("map.aria", { name: emperor.names.display })}
        >
          <rect width={w} height={h} fill="#fbf8f0" />
          {/* simple coastline box decoration */}
          <rect
            x={20}
            y={20}
            width={w - 40}
            height={h - 40}
            fill="none"
            stroke="#d9cbb0"
            strokeDasharray="4 4"
            rx={8}
          />
          <text x={28} y={38} fontSize={10} fill="#8a7d68">
            {t("rmap.scope")}
          </text>

          {pts.slice(0, -1).map((p, i) => {
            const n = pts[i + 1];
            const color = GROUP_COLOR[p.r.group] || GROUP_COLOR.其他;
            return (
              <path
                key={`arc-${i}`}
                d={arcPath(p.x, p.y, n.x, n.y)}
                fill="none"
                stroke={color}
                strokeWidth={2.2}
                opacity={0.85}
              />
            );
          })}

          {pts.map((p, i) => {
            const color = GROUP_COLOR[p.r.group] || GROUP_COLOR.其他;
            const isActive = i === active;
            return (
              <g
                key={p.r.place_id + i}
                onClick={() => setActive(i)}
                style={{ cursor: "pointer" }}
              >
                <circle
                  cx={p.x}
                  cy={p.y}
                  r={isActive ? 7 : 5}
                  fill={color}
                  stroke="#fffdf7"
                  strokeWidth={isActive ? 2.5 : 1.5}
                />
                <text
                  x={p.x + 8}
                  y={p.y - 8}
                  fontSize={10}
                  fill="#2a241c"
                  fontWeight={isActive ? 700 : 400}
                >
                  {p.pl.names.historical}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      <div className="legend">
        {groups.map((g) => (
          <span key={g}>
            <i
              className="swatch"
              style={{ background: GROUP_COLOR[g] || GROUP_COLOR.其他 }}
            />
            {groupLabel(g, lang)}
          </span>
        ))}
      </div>

      <ul className="event-list">
        {pts.map((p, i) => (
          <li
            key={i}
            className={i === active ? "active" : ""}
            onClick={() => setActive(i)}
          >
            <strong>
              {p.r.year ? `${p.r.year} · ` : ""}
              {p.r.event}
            </strong>
            <div>
              {p.pl.names.historical}
              {p.pl.names.modern ? `（${p.pl.names.modern}）` : ""}
              · {groupLabel(p.r.group, lang)}
            </div>
          </li>
        ))}
        {pts.length === 0 && <li>{t("rmap.empty")}</li>}
      </ul>
    </div>
  );
}
