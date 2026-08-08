import { useCallback, useEffect, useState } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";
import type { SiteData } from "../types";
import type { StandStatsFile } from "../standTypes";
import MemorialCover from "./MemorialCover";
import MemorialSpread from "./MemorialSpread";
import { DIRECT_KEY, THEME_KEY, THEMES, type MemorialTheme } from "./memorialUtils";
import "./memorial.css";

type Props = { site: SiteData };

type Phase = "cover" | "opening" | "spread";

function loadTheme(raw: string | null): MemorialTheme {
  if (raw === "ink" || raw === "paper" || raw === "frame") return raw;
  return "frame";
}

export default function EmperorMemorialPage({ site }: Props) {
  const { id } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();
  const [stats, setStats] = useState<StandStatsFile | null>(null);
  const [theme, setTheme] = useState<MemorialTheme>(() =>
    loadTheme(searchParams.get("theme") ?? localStorage.getItem(THEME_KEY))
  );
  const [phase, setPhase] = useState<Phase>(() => {
    const forceCover = searchParams.get("cover") === "1";
    const direct = localStorage.getItem(DIRECT_KEY) === "1";
    return !forceCover && direct ? "spread" : "cover";
  });

  const emperor = site.emperors.find((e) => e.id === id);

  useEffect(() => {
    fetch("/data/stand_stats.json")
      .then((r) => (r.ok ? r.json() : null))
      .then((d: StandStatsFile | null) => setStats(d))
      .catch(() => setStats(null));
  }, []);

  useEffect(() => {
    localStorage.setItem(THEME_KEY, theme);
    const p = new URLSearchParams(searchParams);
    p.set("theme", theme);
    setSearchParams(p, { replace: true });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [theme]);

  // 换人物时回到封面（除非已设直接展开）
  useEffect(() => {
    const direct = localStorage.getItem(DIRECT_KEY) === "1";
    setPhase(direct ? "spread" : "cover");
  }, [id]);

  const open = useCallback(() => {
    setPhase("opening");
    window.setTimeout(() => setPhase("spread"), 980);
  }, []);

  const direct = useCallback(() => {
    localStorage.setItem(DIRECT_KEY, "1");
    setPhase("spread");
  }, []);

  if (!emperor) {
    return (
      <div className="memorial-root" data-theme={theme}>
        <div className="memorial-error">
          未找到人物 <code>{id}</code>。<Link to="/">返回图鉴</Link>
        </div>
      </div>
    );
  }

  const profile = stats?.profiles?.[emperor.id] ?? null;
  const axes = stats?.axes ?? [];
  const isQuasi = emperor.tier === "quasi";

  return (
    <div className="memorial-root" data-theme={theme}>
      <div className="theme-switch" role="group" aria-label="视觉主题">
        {THEMES.map((t) => (
          <button
            key={t.id}
            type="button"
            className={theme === t.id ? "on" : ""}
            onClick={() => setTheme(t.id)}
          >
            {t.label}
          </button>
        ))}
      </div>

      {phase !== "spread" ? (
        <div className={`cover-stage ${phase === "opening" ? "is-opening" : ""}`}>
          <div className="cover-half half-left" aria-hidden="true" />
          <div className="cover-half half-right" aria-hidden="true" />
          <Link to="/" className="cover-back">
            ← 返回图鉴
          </Link>
          <MemorialCover
            emperor={emperor}
            profile={profile}
            isQuasi={isQuasi}
            onOpen={open}
            onDirect={direct}
          />
        </div>
      ) : (
        <div className="spread-stage">
          <MemorialSpread site={site} emperor={emperor} axes={axes} profile={profile} />
        </div>
      )}
    </div>
  );
}
