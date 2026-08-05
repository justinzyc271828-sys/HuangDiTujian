import { useEffect, useState } from "react";
import { Link, Route, Routes } from "react-router-dom";
import type { SiteData } from "./types";
import Gallery from "./pages/Gallery";
import EmperorPage from "./pages/EmperorPage";
import { useCollection } from "./hooks/useCollection";

export default function App() {
  const [site, setSite] = useState<SiteData | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const { read } = useCollection();

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

  return (
    <div className="app-shell">
      <div className="topbar">
        <Link to="/" className="brand">
          皇帝图鉴
          <span>MVP 闭环</span>
        </Link>
        <div className="progress">
          首批收集 {featuredRead}/{site.featured_ids.length}
        </div>
      </div>
      <Routes>
        <Route path="/" element={<Gallery site={site} />} />
        <Route path="/emperor/:id" element={<EmperorPage site={site} />} />
      </Routes>
    </div>
  );
}
