import type { Emperor } from "../types";
import type { StandProfile } from "../standTypes";
import { dynastyLabel, fmtReign, useLang } from "../i18n";

type Props = {
  emperor: Emperor;
  profile: StandProfile | null;
  isQuasi: boolean;
  onOpen: () => void;
  onDirect: () => void;
};

export default function MemorialCover({ emperor, profile, isQuasi, onOpen, onDirect }: Props) {
  const { lang, t } = useLang();
  const isEn = lang === "en";
  const display = isEn ? (emperor.names.display_en ?? emperor.names.display) : emperor.names.display;
  const personal = isEn ? (emperor.names.personal_en ?? emperor.names.personal) : emperor.names.personal;
  const reignText = isEn
    ? fmtReign(emperor.reign.start, emperor.reign.end)
    : `${emperor.reign.start}—${emperor.reign.end}`;
  const standName = profile
    ? isEn
      ? (profile.stand_name_en ?? profile.stand_name)
      : profile.stand_name
    : null;
  const summary = isEn ? (emperor.summary_en ?? emperor.summary) : emperor.summary;
  return (
    <div className="memorial-cover">
      <div className="cover-inner">
        <div className="cover-top">
          <span className="cover-dynasty">{dynastyLabel(emperor.dynasty.label, lang)}</span>
          {isQuasi && <span className="cover-quasi">{t("cover.quasi")}</span>}
        </div>

        <h1 className="cover-name">{display}</h1>
        <div className="cover-titles">
          {emperor.names.temple ? `${t("temple")}${emperor.names.temple}` : ""}
          {emperor.names.temple && emperor.names.posthumous ? " · " : ""}
          {emperor.names.posthumous ? `${t("posthumous")}${emperor.names.posthumous}` : ""}
        </div>
        <div className="cover-meta">
          {personal || "—"} · {t("reign")} {reignText}
        </div>

        {standName && <div className="cover-stand">{standName}</div>}

        <p className="cover-summary">{summary}</p>

        <button type="button" className="cover-open" onClick={onOpen}>
          {t("cover.open")}
        </button>
        <button type="button" className="cover-direct" onClick={onDirect}>
          {t("cover.direct")}
        </button>
      </div>
    </div>
  );
}
