import type { Emperor } from "../types";
import type { StandProfile } from "../standTypes";

type Props = {
  emperor: Emperor;
  profile: StandProfile | null;
  isQuasi: boolean;
  onOpen: () => void;
  onDirect: () => void;
};

export default function MemorialCover({ emperor, profile, isQuasi, onOpen, onDirect }: Props) {
  return (
    <div className="memorial-cover">
      <div className="cover-inner">
        <div className="cover-top">
          <span className="cover-dynasty">{emperor.dynasty.label}</span>
          {isQuasi && <span className="cover-quasi">准帝王</span>}
        </div>

        <h1 className="cover-name">{emperor.names.display}</h1>
        <div className="cover-titles">
          {emperor.names.temple ? `庙号${emperor.names.temple}` : ""}
          {emperor.names.temple && emperor.names.posthumous ? " · " : ""}
          {emperor.names.posthumous ? `谥${emperor.names.posthumous}` : ""}
        </div>
        <div className="cover-meta">
          {emperor.names.personal || "—"} · 在位 {emperor.reign.start}—{emperor.reign.end}
        </div>

        {profile && <div className="cover-stand">{profile.stand_name}</div>}

        <p className="cover-summary">{emperor.summary}</p>

        <button type="button" className="cover-open" onClick={onOpen}>
          展开御览
        </button>
        <button type="button" className="cover-direct" onClick={onDirect}>
          直接展开，下次跳过封面
        </button>
      </div>
    </div>
  );
}
