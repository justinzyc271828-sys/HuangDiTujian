import { useState } from "react";
import { useLang } from "../i18n";

// 分享链接固定指向线上 Pages 地址(本地调试时复制的也是可公开访问的链接)
const SITE_SHARE_BASE = "https://justinzyc271828-sys.github.io/HuangDiTujian";

export function emperorShareUrl(id: string): string {
  return `${SITE_SHARE_BASE}/emperor/${id}`;
}

function legacyCopy(text: string): boolean {
  const ta = document.createElement("textarea");
  ta.value = text;
  ta.style.position = "fixed";
  ta.style.opacity = "0";
  document.body.appendChild(ta);
  ta.select();
  let ok = false;
  try {
    ok = document.execCommand("copy");
  } catch {
    ok = false;
  }
  document.body.removeChild(ta);
  return ok;
}

/** 详情页小箭头分享按钮:点击复制该帝线上专页链接,成功后图标变勾并浮出提示 */
export function ShareButton({ id }: { id: string }) {
  const { t } = useLang();
  const [copied, setCopied] = useState(false);

  const onClick = (ev: React.MouseEvent) => {
    ev.preventDefault();
    ev.stopPropagation();
    const url = emperorShareUrl(id);
    const done = () => {
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    };
    if (navigator.clipboard?.writeText) {
      navigator.clipboard.writeText(url).then(done, () => {
        if (legacyCopy(url)) done();
      });
    } else if (legacyCopy(url)) {
      done();
    }
  };

  return (
    <button
      type="button"
      className={`share-btn${copied ? " copied" : ""}`}
      title={t("share.hint")}
      aria-label={t("share.hint")}
      onClick={onClick}
    >
      {copied ? (
        <svg viewBox="0 0 16 16" width="15" height="15" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
          <path d="M3 8.5l3.4 3.4L13 4.5" />
        </svg>
      ) : (
        <svg viewBox="0 0 16 16" width="15" height="15" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round">
          <path d="M6 3.5H2.5v10h11V10" />
          <path d="M9.5 2h4.5v4.5" />
          <path d="M14 2L7.5 8.5" />
        </svg>
      )}
      {copied && <span className="share-toast">{t("share.copied")}</span>}
    </button>
  );
}
