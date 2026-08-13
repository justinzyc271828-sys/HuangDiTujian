import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";
import type { Emperor, Place, SiteData } from "../types";
import type { StandStatsFile } from "../standTypes";
import MemorialCover from "./MemorialCover";
import MemorialSpread from "./MemorialSpread";
import { DIRECT_KEY } from "./memorialUtils";
import { tradDeep, useLang } from "../i18n";
import "./memorial.css";

type Props = { site: SiteData };

type Phase = "cover" | "opening" | "spread";

/* 按需加载的模块级缓存:raw 存原文,hant 存转繁结果;切语言/回看不重取不重算 */
const rawEmp = new Map<string, Emperor>();
const hantEmp = new Map<string, Emperor>();
const placesCache: { raw: Record<string, Place> | null; hant: Record<string, Place> | null } = {
  raw: null,
  hant: null,
};

export default function EmperorMemorialPage({ site }: Props) {
  const { lang, t } = useLang();
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const [stats, setStats] = useState<StandStatsFile | null>(null);
  const [full, setFull] = useState<Emperor | null>(null);
  const [places, setPlaces] = useState<Record<string, Place> | null>(null);
  const [gone, setGone] = useState(false);
  const [phase, setPhase] = useState<Phase>(() => {
    const forceCover = searchParams.get("cover") === "1";
    const direct = localStorage.getItem(DIRECT_KEY) === "1";
    return !forceCover && direct ? "spread" : "cover";
  });

  const inCatalog = Boolean(id && site.emperors.some((e) => e.id === id));

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/stand_stats.json`)
      .then((r) => (r.ok ? r.json() : null))
      .then((d: StandStatsFile | null) => setStats(d))
      .catch(() => setStats(null));
  }, []);

  // 地点库:全站共享一份,只拉一次;切繁体仅换缓存视图
  useEffect(() => {
    if (placesCache.raw) {
      setPlaces(lang === "hant" ? (placesCache.hant ??= tradDeep(placesCache.raw)) : placesCache.raw);
      return;
    }
    fetch(`${import.meta.env.BASE_URL}data/places.json`)
      .then((r) => (r.ok ? r.json() : null))
      .then((d: Record<string, Place> | null) => {
        if (!d) return;
        placesCache.raw = d;
        setPlaces(lang === "hant" ? (placesCache.hant ??= tradDeep(d)) : d);
      })
      .catch(() => {});
  }, [lang]);

  // 帝王详情:按 id 拉取;raw/hant 双缓存,切语言与回看零成本
  useEffect(() => {
    if (!id || !inCatalog) return;
    setGone(false);
    const cached = lang === "hant" ? hantEmp.get(id) : rawEmp.get(id);
    if (cached) {
      setFull(cached);
      return;
    }
    if (!rawEmp.has(id)) setFull(null);
    fetch(`${import.meta.env.BASE_URL}data/emperor/${id}.json`)
      .then((r) => {
        if (!r.ok) throw new Error(String(r.status));
        return r.json();
      })
      .then((d: Emperor) => {
        rawEmp.set(id, d);
        if (lang === "hant") {
          let v = hantEmp.get(id);
          if (!v) {
            v = tradDeep(d);
            hantEmp.set(id, v);
          }
          setFull(v);
        } else {
          setFull(d);
        }
      })
      .catch(() => setGone(true));
  }, [id, lang, inCatalog]);

  // 换人物时回到封面(除非已设直接展开)
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

  // 详情就位后合并成全量 SiteData,下游组件(MemorialSpread/Main/Map/Toc)零改动
  const merged = useMemo<SiteData | null>(() => {
    if (!full || !places) return null;
    return {
      ...site,
      places,
      emperors: site.emperors.map((e) => (e.id === full.id ? full : e)),
    };
  }, [site, places, full]);

  if (!inCatalog || gone) {
    return (
      <div className="memorial-root">
        <div className="memorial-error">
          {t("nf.title")} <code>{id}</code>
          {lang === "en" ? "." : "。"}
          <Link to="/">{t("backPlain")}</Link>
        </div>
      </div>
    );
  }

  if (!merged || !full) {
    return <div className="memorial-root loading">{t("app.loading")}</div>;
  }

  const emperor = full;
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
            {t("back")}
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
          <MemorialSpread site={merged} emperor={emperor} axes={axes} profile={profile} />
        </div>
      )}
    </div>
  );
}
