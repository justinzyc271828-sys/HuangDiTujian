import { useEffect, useRef, useState } from "react";
import { useLang } from "../i18n";

/* ============================================================
   全局背景音乐
   - 默认自动播放（循环，音量 0.35）；localStorage hd-music=off 时不播
   - 浏览器拦截自动播放（NotAllowedError）→ 挂一次性 pointerdown/keydown，
     用户首次交互即开播
   - preload="none"：关闭状态下不产生音频请求，不阻塞首屏
   - Audio 为模块级单例：StrictMode 双挂载 / 组件重挂载都共用同一个
     音频元素，不会出现两条音轨重叠；卸载时不 pause，换页音乐不断
   ============================================================ */

const STORAGE_KEY = "hd-music";
const SRC = "/music/the-last-emperors-march.mp3";

let sharedAudio: HTMLAudioElement | null = null;

function getAudio(): HTMLAudioElement {
  if (!sharedAudio) {
    sharedAudio = new Audio();
    sharedAudio.src = SRC;
    sharedAudio.preload = "none";
    sharedAudio.loop = true;
    sharedAudio.volume = 0.35;
  }
  return sharedAudio;
}

export default function BgMusic() {
  const { t } = useLang();
  const gestureCleanup = useRef<() => void>(() => {});
  const [playing, setPlaying] = useState(
    () => sharedAudio !== null && !sharedAudio.paused
  );

  useEffect(() => {
    const audio = getAudio();
    let disposed = false;

    const onPlay = () => setPlaying(true);
    const onPause = () => setPlaying(false);
    audio.addEventListener("play", onPlay);
    audio.addEventListener("pause", onPause);
    // 重挂载时同步真实播放状态（单例可能已在播）
    setPlaying(!audio.paused);

    /* 自动播放被拦截：等用户首次交互（一次性，触发后自摘） */
    const kick = () => {
      window.removeEventListener("pointerdown", kick);
      window.removeEventListener("keydown", kick);
      gestureCleanup.current = () => {};
      audio.play()?.catch(() => {});
    };
    const armGesture = () => {
      window.addEventListener("pointerdown", kick);
      window.addEventListener("keydown", kick);
      gestureCleanup.current = () => {
        window.removeEventListener("pointerdown", kick);
        window.removeEventListener("keydown", kick);
      };
    };

    let saved: string | null = null;
    try {
      saved = localStorage.getItem(STORAGE_KEY);
    } catch {
      /* 读不到按默认 on */
    }

    if (saved !== "off" && audio.paused) {
      audio.play()?.catch(() => {
        /* play() 的拒绝是异步的，可能发生在 cleanup 之后；
           已卸载就不再挂监听，避免废弃音频被复活成第二条音轨 */
        if (!disposed && audio.paused) armGesture();
      });
    }

    return () => {
      disposed = true;
      gestureCleanup.current();
      gestureCleanup.current = () => {};
      audio.removeEventListener("play", onPlay);
      audio.removeEventListener("pause", onPause);
      /* 不 pause：单例音频跨挂载存活，换页 / 重挂载音乐不中断 */
    };
  }, []);

  const toggle = () => {
    const a = getAudio();
    try {
      if (playing) {
        gestureCleanup.current(); // 关掉待触发的自动开播，避免关了又被点响
        gestureCleanup.current = () => {};
        a.pause();
        localStorage.setItem(STORAGE_KEY, "off");
      } else {
        a.play()?.catch(() => {});
        localStorage.setItem(STORAGE_KEY, "on");
      }
    } catch {
      /* localStorage 写失败不影响本次播放 */
    }
  };

  return (
    <div className="lang-switch music-switch">
      <button
        type="button"
        className={playing ? "on" : "off"}
        onClick={toggle}
        title={playing ? t("music.stop") : t("music.play")}
        aria-label={playing ? t("music.stop") : t("music.play")}
        aria-pressed={playing}
      >
        <span className="music-ico" aria-hidden="true">
          ♪
        </span>
      </button>
    </div>
  );
}
