import { useMemo } from "react";
import type { Emperor, Place, RoutePoint } from "../types";
import { BASE_CITIES, COAST, ISLANDS, MOUNTAINS, RANGES, RIVERS, TERRAIN } from "./chinaBase";
import { TERRITORY } from "./territory";
import { groupLabel, useLang } from "../i18n";

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
  const { lang, t } = useLang();
  const isEn = lang === "en";
  const placeName = (pl: Place) =>
    isEn ? (pl.names.english ?? pl.names.historical) : pl.names.historical;
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

  /* 地图标记：同一地点多次到访只画一个点、只标一次名（事件列表仍逐条） */
  const markers = useMemo(() => {
    const seen = new Set<string>();
    return pts.filter((p) => {
      if (seen.has(p.r.place_id)) return false;
      seen.add(p.r.place_id);
      return true;
    });
  }, [pts]);

  /* 连线路径：仅去掉连续重复的同地点段，保留 A→B→A 往返弧 */
  const seq = useMemo(
    () => pts.filter((p, i) => i === 0 || p.r.place_id !== pts[i - 1].r.place_id),
    [pts]
  );

  /* 示意底图（海岸线/河岳/参照城）与路线共用同一投影与视野；
     与路线点贴近的山岳/城市标注隐藏，避免叠字 */
  const base = useMemo(() => {
    if (!bounds) return null;
    const toPath = (coords: [number, number][]) =>
      coords
        .map(([lng, lat], i) => {
          const { x, y } = project(lng, lat, bounds, w, h);
          return `${i === 0 ? "M" : "L"} ${x.toFixed(1)} ${y.toFixed(1)}`;
        })
        .join(" ");
    const nearMarker = (x: number, y: number, r: number) =>
      markers.some((p) => Math.abs(p.x - x) < r && Math.abs(p.y - y) < r);
    const territory = TERRITORY[emperor.dynasty.id] ?? null;
    return {
      territory: territory
        ? {
            label: territory.label,
            year: territory.year,
            parts: territory.parts.map((p) => ({ kind: p.kind, d: `${toPath(p.ring)} Z` })),
          }
        : null,
      coast: toPath(COAST),
      islands: ISLANDS.map((ring) => `${toPath(ring)} Z`),
      ranges: RANGES.map((r) => ({
        name: r.name,
        d: toPath(r.pts),
        verts: r.pts.map(([lng, lat]) => project(lng, lat, bounds, w, h)),
      })),
      rivers: RIVERS.map((r) => ({ id: r.id, d: toPath(r.pts) })),
      terrain: TERRAIN.map((t) => ({ ...t, ...project(t.lng, t.lat, bounds, w, h) })),
      mountains: MOUNTAINS.map((m) => ({ ...m, ...project(m.lng, m.lat, bounds, w, h) })).filter(
        (m) => !nearMarker(m.x, m.y, 34)
      ),
      cities: BASE_CITIES.map((c) => ({ ...c, ...project(c.lng, c.lat, bounds, w, h) })).filter(
        (c) => !nearMarker(c.x, c.y, 46)
      ),
    };
  }, [bounds, markers, emperor.dynasty.id]);

  /* 标签避让：按 y 升序逐个放置，重叠时下移或再推 */
  const labelY = useMemo(() => {
    const pos = new Map<number, number>();
    const placed: { x: number; y: number }[] = [];
    const sorted = markers.map((p, i) => ({ ...p, i })).sort((a, b) => a.y - b.y);
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
  }, [markers]);

  const groups = [...new Set(pts.map((p) => p.r.group))];

  if (pts.length === 0) {
    return (
      <aside className="memorial-map">
        <h2 className="map-title">{t("map.title")}</h2>
        <p className="map-hint">{t("map.empty")}</p>
      </aside>
    );
  }

  return (
    <aside className="memorial-map">
      <h2 className="map-title">{t("map.title")}</h2>
      <div className="map-frame">
        <svg
          className="map-svg"
          viewBox={`0 0 ${w} ${h}`}
          role="img"
          aria-label={t("map.aria", {
            name: isEn ? (emperor.names.display_en ?? emperor.names.display) : emperor.names.display,
          })}
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

          {base?.territory && (
            <g className="map-territory" aria-hidden="true">
              {base.territory.parts.map((p, i) => (
                <path key={i} className={`territory-${p.kind}`} d={p.d} />
              ))}
            </g>
          )}

          {base && (
            <g className="map-base" aria-hidden="true">
              <path className="base-coast" d={base.coast} fill="none" />
              {base.islands.map((d, i) => (
                <path key={i} className="base-coast" d={d} fill="none" />
              ))}
              {base.ranges.map((r) => (
                <g key={r.name} className="base-range">
                  <path d={r.d} fill="none" />
                  {r.verts.map((v, i) => (
                    <path
                      key={i}
                      d={`M ${v.x - 3} ${v.y + 2} L ${v.x} ${v.y - 3} L ${v.x + 3} ${v.y + 2} Z`}
                    />
                  ))}
                  <text x={r.verts[Math.floor(r.verts.length / 2)].x + 6} y={r.verts[Math.floor(r.verts.length / 2)].y - 4}>
                    {r.name}
                  </text>
                </g>
              ))}
              {base.rivers.map((r) => (
                <path key={r.id} className="base-river" d={r.d} fill="none" />
              ))}
              {base.terrain.map((t) => (
                <text key={t.name} className="base-terrain" x={t.x} y={t.y} textAnchor="middle">
                  {t.name}
                </text>
              ))}
              {base.mountains.map((m) => (
                <g key={m.name} className="base-mtn">
                  <path d={`M ${m.x - 4} ${m.y + 3} L ${m.x} ${m.y - 4} L ${m.x + 4} ${m.y + 3} Z`} />
                  <text x={m.x + 6} y={m.y + 3}>
                    {m.name}
                  </text>
                </g>
              ))}
              {base.cities.map((c) => (
                <g key={c.name} className="base-city">
                  <circle cx={c.x} cy={c.y} r={1.8} />
                  <text x={c.x + 5} y={c.y + 3}>
                    {c.name}
                  </text>
                </g>
              ))}
            </g>
          )}

          {seq.slice(0, -1).map((p, i) => {
            const np = seq[i + 1];
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

          {markers.map((p, i) => {
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
                  {placeName(p.pl)}
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
            {groupLabel(g, lang)}
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
              {placeName(p.pl)}
              {p.pl.names.modern ? `（${p.pl.names.modern}）` : ""} · {groupLabel(p.r.group, lang)}
            </div>
          </li>
        ))}
      </ul>
    </aside>
  );
}
