import { useEffect, useMemo, useRef, useState } from "react";
import { Route, Routes } from "react-router-dom";
import type { SiteData } from "./types";
import { LangSwitch, tradDeep, useLang } from "./i18n";
import BgMusic from "./components/BgMusic";
import Gallery from "./pages/Gallery";
import StandLab from "./pages/StandLab";
import EmperorMemorialPage from "./memorial/EmperorMemorialPage";

export default function App() {
  const { lang, t } = useLang();
  const [raw, setRaw] = useState<SiteData | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const hantCache = useRef<SiteData | null>(null);

  // site.json 只拉一次,与语言无关;繁体由 tradDeep 派生(见下)
  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}data/site.json`)
      .then((r) => {
        if (!r.ok) throw new Error(String(r.status));
        return r.json();
      })
      .then((data: SiteData) => setRaw(data))
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
        <Route path="/lab" element={<StandLab site={site} />} />
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
