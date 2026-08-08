import { useMemo } from "react";
import type { Emperor, Place, RoutePoint } from "../types";

const GROUP_COLOR: Record<string, string> = {
  都城: "#6b5c42",
  巡狩: "#9e2b22",
  亲征: "#3d5a45",
  起兵: "#6b4c9a",
  入关: "#b45309",
  其他: "#6b7280",
  迁都: "#2f4b5c",
  流徙: "#9ca3af",
};

type Bounds = { lng0: number; lng1: number; lat0: number; lat1: number };

/** 按实际点位自适应视野；最小跨度防止单区域过度放大 */
function fitBounds(coords: { lng: number; lat: number }[]): Bounds {
  const lngs = coords.map((c) => c.lng);
  const lats = coords.map((c) => c.lat);
  const lngC = (Math.min(...lngs) + Math.max(...lngs)) / 2;
  const latC = (Math.min(...lats) + Math.max(...lats)) / 2;
  const lngSpan = Math.max(Math.max(...lngs) - Math.min(...lngs), 7);
  const latSpan = Math.max(Math.max(...lats) - Math.min(...lats), 4.5);
  const padLng = lngSpan * 0.2;
  const padLat = latSpan * 0.2;
  return {
    lng0: lngC - lngSpan / 2 - padLng,
    lng1: lngC + lngSpan / 2 + padLng,
    lat0: latC - latSpan / 2 - padLat,
    lat1: latC + latSpan / 2 + padLat,
  };
}

function project(lng: number, lat: number, b: Bounds, w: number, h: number, pad = 30) {
  const x = pad + ((lng - b.lng0) / (b.lng1 - b.lng0)) * (w - pad * 2);
  const y = pad + ((b.lat1 - lat) / (b.lat1 - b.lat0)) * (h - pad * 2);
  return { x, y };
}

function arcPath(x1: number, y1: number, x2: number, y2: number): string {
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
  activePlaceId: string | null;
  onSelectPlace: (placeId: string) => void;
};

export default function MemorialMap({ emperor, places, activePlaceId, onSelectPlace }: Props) {
  const routes = useMemo(
    () => [...(emperor.routes || [])].sort((a, b) => (a.order ?? 0) - (b.order ?? 0)),
    [emperor.routes]
  );
  const w = 340;
  const h = 400;

  const raw = useMemo(
    () =>
      routes
        .map((r) => {
          const pl = places[r.place_id];
          return pl ? { r, pl } : null;
        })
        .filter(Boolean) as { r: RoutePoint; pl: Place }[],
    [routes, places]
  );

  const bounds = useMemo(
    () => (raw.length > 0 ? fitBounds(raw.map((p) => p.pl.coords)) : null),
    [raw]
  );

  const pts = bounds
    ? raw.map((p) => {
        const { x, y } = project(p.pl.coords.lng, p.pl.coords.lat, bounds, w, h);
        return { ...p, x, y };
      })
    : [];

  /* 标签避让：按 y 升序逐个放置，重叠时下移或再推 */
  const labelY = useMemo(() => {
    const pos = new Map<number, number>();
    const placed: { x: number; y: number }[] = [];
    const sorted = pts.map((p, i) => ({ ...p, i })).sort((a, b) => a.y - b.y);
    for (const p of sorted) {
      let ly = p.y - 8;
      for (const q of placed) {
        if (Math.abs(p.x - q.x) < 48 && Math.abs(ly - q.y) < 11) ly = p.y + 17;
      }
      for (const q of placed) {
        if (Math.abs(p.x - q.x) < 48 && Math.abs(ly - q.y) < 11) ly = q.y + 12;
      }
      placed.push({ x: p.x, y: ly });
      pos.set(p.i, ly);
    }
    return pos;
  }, [pts]);

  const groups = [...new Set(pts.map((p) => p.r.group))];

  if (pts.length === 0) {
    return (
      <aside className="memorial-map">
        <h2 className="map-title">一生地图</h2>
        <p className="map-hint">路线未录入。</p>
      </aside>
    );
  }

  return (
    <aside className="memorial-map">
      <h2 className="map-title">一生地图</h2>
      <p className="map-hint">示意底图（非严肃 GIS）。点击事件与年表联动。</p>
      <div className="map-frame">
        <svg
          className="map-svg"
          viewBox={`0 0 ${w} ${h}`}
          role="img"
          aria-label={`${emperor.names.display}路线图`}
        >
          <rect width={w} height={h} fill="var(--map-bg)" />
          <rect
            x={20}
            y={20}
            width={w - 40}
            height={h - 40}
            fill="none"
            stroke="var(--panel-line)"
            strokeDasharray="4 4"
            rx={6}
          />

          {pts.slice(0, -1).map((p, i) => {
            const np = pts[i + 1];
            const color = GROUP_COLOR[p.r.group] || GROUP_COLOR.其他;
            return (
              <path
                key={`arc-${i}`}
                d={arcPath(p.x, p.y, np.x, np.y)}
                fill="none"
                stroke={color}
                strokeWidth={2.2}
                opacity={0.85}
              />
            );
          })}

          {pts.map((p, i) => {
            const color = GROUP_COLOR[p.r.group] || GROUP_COLOR.其他;
            const isActive = p.r.place_id === activePlaceId;
            return (
              <g
                key={p.r.place_id + p.r.order}
                onClick={() => onSelectPlace(p.r.place_id)}
                style={{ cursor: "pointer" }}
              >
                <circle
                  cx={p.x}
                  cy={p.y}
                  r={isActive ? 7.5 : 5}
                  fill={color}
                  stroke="var(--map-bg)"
                  strokeWidth={isActive ? 2.5 : 1.5}
                />
                {isActive && (
                  <circle cx={p.x} cy={p.y} r={12} fill="none" stroke="#c0392b" strokeWidth={1.2} opacity={0.7} />
                )}
                <text
                  x={p.x + 9}
                  y={labelY.get(i) ?? p.y - 8}
                  fontSize={10.5}
                  fill="var(--ink)"
                  fontWeight={isActive ? 700 : 400}
                >
                  {p.pl.names.historical}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      <div className="map-legend">
        {groups.map((g) => (
          <span key={g}>
            <i className="swatch" style={{ background: GROUP_COLOR[g] || GROUP_COLOR.其他 }} />
            {g}
          </span>
        ))}
      </div>

      <ul className="map-events">
        {pts.map((p) => (
          <li
            key={p.r.place_id + p.r.order}
            className={p.r.place_id === activePlaceId ? "active" : ""}
            onClick={() => onSelectPlace(p.r.place_id)}
          >
            <strong>
              {p.r.year ? `${p.r.year} · ` : ""}
              {p.r.event}
            </strong>
            <div>
              {p.pl.names.historical}
              {p.pl.names.modern ? `（${p.pl.names.modern}）` : ""} · {p.r.group}
            </div>
          </li>
        ))}
      </ul>
    </aside>
  );
}
