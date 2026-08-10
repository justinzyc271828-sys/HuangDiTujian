import { useEffect, useState } from "react";
import { Route, Routes } from "react-router-dom";
import type { SiteData } from "./types";
import { LangSwitch, tradDeep, translate, useLang } from "./i18n";
import BgMusic from "./components/BgMusic";
import Gallery from "./pages/Gallery";
import StandLab from "./pages/StandLab";
import EmperorMemorialPage from "./memorial/EmperorMemorialPage";

export default function App() {
  const { lang, t } = useLang();
  const [site, setSite] = useState<SiteData | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    fetch("/data/site.json")
      .then((r) => {
        if (!r.ok) throw new Error(`${translate(lang, "app.loadError")}: ${r.status}`);
        return r.json();
      })
      .then((data: SiteData) =>
        // 繁体模式：整棵内容层深度转繁；简体/英文用原始数据（英文走 _en 字段渲染）
        setSite(lang === "hant" ? tradDeep(data) : data)
      )
      .catch((e: Error) => setErr(e.message));
  }, [lang]);

  let body;
  if (err) {
    body = (
      <div className="error">
        {err}
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
