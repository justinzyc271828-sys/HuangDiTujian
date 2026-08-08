import { useCallback, useEffect, useState } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";
import type { SiteData } from "../types";
import type { StandStatsFile } from "../standTypes";
import MemorialCover from "./MemorialCover";
import MemorialSpread from "./MemorialSpread";
import { DIRECT_KEY } from "./memorialUtils";
import "./memorial.css";

type Props = { site: SiteData };

type Phase = "cover" | "opening" | "spread";

export default function EmperorMemorialPage({ site }: Props) {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const [stats, setStats] = useState<StandStatsFile | null>(null);
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
      <div className="memorial-root">
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
    <div className="memorial-root">
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
