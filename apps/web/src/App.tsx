import { useEffect, useState } from "react";
import { Route, Routes } from "react-router-dom";
import type { SiteData } from "./types";
import Gallery from "./pages/Gallery";
import StandLab from "./pages/StandLab";
import EmperorMemorialPage from "./memorial/EmperorMemorialPage";

export default function App() {
  const [site, setSite] = useState<SiteData | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    fetch("/data/site.json")
      .then((r) => {
        if (!r.ok) throw new Error(`加载 site.json 失败: ${r.status}`);
        return r.json();
      })
      .then((data: SiteData) => setSite(data))
      .catch((e: Error) => setErr(e.message));
  }, []);

  if (err) {
    return (
      <div className="error">
        {err}
        <p>请先运行：python tools/build_site_data.py</p>
      </div>
    );
  }

  if (!site) {
    return <div className="loading">加载图鉴数据…</div>;
  }

  return (
    <Routes>
      <Route path="/" element={<Gallery site={site} />} />
      <Route path="/emperor/:id" element={<EmperorMemorialPage site={site} />} />
      <Route path="/lab" element={<StandLab site={site} />} />
    </Routes>
  );
}
