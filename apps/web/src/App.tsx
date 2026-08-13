import { Suspense, lazy, useEffect, useMemo, useRef, useState } from "react";
import { Route, Routes } from "react-router-dom";
import type { SiteData } from "./types";
import { LangSwitch, tradDeep, useLang } from "./i18n";
import BgMusic from "./components/BgMusic";
import Gallery from "./pages/Gallery";
import EmperorMemorialPage from "./memorial/EmperorMemorialPage";

const StandLab = lazy(() => import("./pages/StandLab"));

export default function App() {
  const { lang, t } = useLang();
  const [raw, setRaw] = useState<SiteData | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const hantCache = useRef<SiteData | null>(null);

  // 轻量 index.json 只拉一次,与语言无关;详情页按需再拉 emperor/<id>.json 与 places.json
  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/index.json`)
      .then((r) => {
        if (!r.ok) throw new Error(String(r.status));
        return r.json();
      })
      .then((data: Omit<SiteData, "places">) => setRaw({ places: {}, ...data }))
      .catch((e: Error) => setErr(e.message));
  }, []);

  // 繁体模式:整棵内容层深度转繁,只算一次并缓存;简体/英文用原始数据(英文走 _en 字段渲染)
  const site = useMemo(() => {
    if (!raw) return null;
    if (lang !== "hant") return raw;
    if (!hantCache.current) hantCache.current = tradDeep(raw);
    return hantCache.current;
  }, [raw, lang]);

  let body;
  if (err) {
    body = (
      <div className="error">
        {t("app.loadError")}: {err}
        <p>{t("app.hint")}</p>
      </div>
    );
  } else if (!site) {
    body = <div className="loading">{t("app.loading")}</div>;
  } else {
    body = (
      <Routes>
        <Route path="/" element={<Gallery site={site} />} />
        <Route path="/emperor/:id" element={<EmperorMemorialPage site={site} />} />
        <Route
          path="/lab"
          element={
            <Suspense fallback={<div className="loading">{t("app.loading")}</div>}>
              <StandLab site={site} />
            </Suspense>
          }
        />
      </Routes>
    );
  }

  return (
    <>
      <div className="corner-stack">
        <LangSwitch />
        <BgMusic />
      </div>
      {body}
    </>
  );
}
