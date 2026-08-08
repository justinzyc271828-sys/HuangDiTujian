import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import type { Emperor, SiteData } from "../types";
import type { StandAxis, StandProfile } from "../standTypes";
import MemorialToc from "./MemorialToc";
import MemorialMain from "./MemorialMain";
import MemorialMap from "./MemorialMap";
import { useCollection } from "../hooks/useCollection";
import { TOC_ITEMS } from "./memorialUtils";

type Props = {
  site: SiteData;
  emperor: Emperor;
  axes: StandAxis[];
  profile: StandProfile | null;
};

export default function MemorialSpread({ site, emperor, axes, profile }: Props) {
  const { markRead, toggleStar, starred, read } = useCollection();
  const [activeSection, setActiveSection] = useState<string>("m-hero");
  const [activePlaceId, setActivePlaceId] = useState<string | null>(null);
  const rootRef = useRef<HTMLDivElement>(null);

  const isStub =
    emperor.page_status === "stub" || emperor.meta?.page_status === "stub";
  const isQuasi = emperor.tier === "quasi";

  useEffect(() => {
    markRead(emperor.id);
  }, [emperor.id, markRead]);

  // scrollspy：整页滚动，监听各节
  useEffect(() => {
    const root = rootRef.current;
    if (!root) return;
    const sections = TOC_ITEMS.map((t) => root.querySelector<HTMLElement>(`#${t.id}`)).filter(
      Boolean
    ) as HTMLElement[];
    if (sections.length === 0) return;
    const io = new IntersectionObserver(
      (entries) => {
        for (const en of entries) {
          if (en.isIntersecting) setActiveSection(en.target.id);
        }
      },
      { rootMargin: "-25% 0px -65% 0px" }
    );
    sections.forEach((s) => io.observe(s));
    return () => io.disconnect();
  }, [emperor.id]);

  return (
    <div className="memorial-spread" ref={rootRef}>
      <div className="spread-left">
        <Link to="/" className="spread-back">
          ← 返回图鉴
        </Link>
        <MemorialToc
          site={site}
          emperor={emperor}
          isStub={isStub}
          isQuasi={isQuasi}
          isRead={read.includes(emperor.id)}
          isStar={starred.includes(emperor.id)}
          activeSection={activeSection}
          onToggleStar={() => toggleStar(emperor.id)}
        />
      </div>

      <MemorialMain
        emperor={emperor}
        site={site}
        axes={axes}
        profile={profile}
        isStub={isStub}
        onSelectPlace={setActivePlaceId}
      />

      <div className="spread-right">
        <MemorialMap
          emperor={emperor}
          places={site.places}
          activePlaceId={activePlaceId}
          onSelectPlace={setActivePlaceId}
        />
      </div>
    </div>
  );
}
