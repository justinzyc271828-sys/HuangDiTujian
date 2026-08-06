import { useEffect, useState } from "react";
import { Link, Route, Routes, useLocation } from "react-router-dom";
import type { SiteData } from "./types";
import Gallery from "./pages/Gallery";
import EmperorPage from "./pages/EmperorPage";
import StandLab from "./pages/StandLab";
import { useCollection } from "./hooks/useCollection";

export default function App() {
  const [site, setSite] = useState<SiteData | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const { read } = useCollection();
  const loc = useLocation();
  const isLab = loc.pathname.startsWith("/lab");

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

  const featuredRead = site.featured_ids.filter((id) => read.includes(id)).length;
  const total = site.catalog_stats?.total ?? site.emperors.length;
  const draft = site.catalog_stats?.draft ?? 0;

  if (isLab) {
    return (
      <Routes>
        <Route path="/lab" element={<StandLab site={site} />} />
      </Routes>
    );
  }

  return (
    <div className="app-shell">
      <div className="topbar">
        <Link to="/" className="brand">
          皇帝图鉴
          <span>索引 {total}</span>
        </Link>
        <div style={{ display: "flex", gap: "0.6rem", alignItems: "center" }}>
          <Link
            to="/lab"
            className="chip"
            style={{ textDecoration: "none", color: "inherit" }}
          >
            替身档 Lab
          </Link>
          <div className="progress">
            首批 {featuredRead}/{site.featured_ids.length} · 专页 {draft}/{total}
          </div>
        </div>
      </div>
      <Routes>
        <Route path="/" element={<Gallery site={site} />} />
        <Route path="/emperor/:id" element={<EmperorPage site={site} />} />
        <Route path="/lab" element={<StandLab site={site} />} />
      </Routes>
    </div>
  );
}
