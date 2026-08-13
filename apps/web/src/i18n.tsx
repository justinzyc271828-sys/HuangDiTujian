import { useSyncExternalStore } from "react";
import { TRAD_CHARS, TRAD_PHRASES } from "./tradTable";

/* ============================================================
   轻量手写 i18n：简体 / 繁體 / EN 三语 UI
   - localStorage 键 hd-lang 优先；否则按 navigator.language：
     zh 且含 hant/tw/hk/mo → 繁体；其余 zh → 简体；非 zh → 英文
   - t(key) 查 STR 字典（简体+英文两列）；繁体由 toTrad 转换生成
   - 繁体转换覆盖 UI + 内容层：App 加载 site.json 后按 lang 做
     tradDeep 深度转换（人名/摘要/年表/bio/地名/品藻全部转繁）
   ============================================================ */

export type Lang = "hans" | "hant" | "en";

const STORAGE_KEY = "hd-lang";

function detect(): Lang {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === "hans" || saved === "hant" || saved === "en") return saved;
    if (saved === "zh") return "hans"; // 旧版双语取值迁移
  } catch {
    /* localStorage 不可用时按系统语言 */
  }
  const nav =
    typeof navigator !== "undefined"
      ? (navigator.languages?.[0] ?? navigator.language ?? "")
      : "";
  const n = nav.toLowerCase();
  if (!n.startsWith("zh")) return "en";
  return /hant|tw|hk|mo/.test(n) ? "hant" : "hans";
}

let current: Lang = detect();
const listeners = new Set<() => void>();

export function setLang(l: Lang) {
  current = l;
  try {
    localStorage.setItem(STORAGE_KEY, l);
  } catch {
    /* 忽略写入失败 */
  }
  listeners.forEach((f) => f());
}

function subscribe(f: () => void) {
  listeners.add(f);
  return () => {
    listeners.delete(f);
  };
}

export function useLang(): {
  lang: Lang;
  setLang: (l: Lang) => void;
  t: (key: string, vars?: Record<string, string | number>) => string;
} {
  const lang = useSyncExternalStore(subscribe, () => current);
  return {
    lang,
    setLang,
    t: (key, vars) => translate(lang, key, vars),
  };
}

export function translate(
  lang: Lang,
  key: string,
  vars?: Record<string, string | number>
): string {
  const entry = STR[key];
  // 先定文案并做繁体转换，再插值——保证 {name} 等动态数据保持简体原文
  let s = entry
    ? lang === "en"
      ? entry.en
      : lang === "hant"
        ? toTrad(entry.zh)
        : entry.zh
    : key;
  if (vars) {
    for (const [k, v] of Object.entries(vars)) {
      s = s.replaceAll(`{${k}}`, String(v));
    }
  }
  return s;
}

/* ============================================================
   简体 → 繁体 转换层
   算法：词级最长匹配（tradTable.ts，OpenCC 词表按项目语料过滤
   + 姓氏/地名/虚词保护壳）→ 单字映射 → WORD_FIX 项目覆盖。
   标 ⚖ 的「一简对多繁」取舍由词表与 FORCED 在生成期解决。
   ============================================================ */

/* ⚖ 项目词级覆盖（无论词表给什么，最终强制本项目取舍）：
   - 奏折→奏摺：奏折（上呈文书）繁体标准作「摺」；折（折断/折扣）不动
   - 在制→在製：「画像在制」=制作中，取「製」；机制/克制/制度保持「制」
   - 想象→想像：台湾标准作「想像」；其余「象」（象征/形象）不动
   - 事迹→事蹟：功业义台湾标准作「蹟」；轨迹仍走字级映射作「軌跡」 */
const WORD_FIX: [string, string][] = [
  ["奏折", "奏摺"],
  ["在制", "在製"],
  ["想象", "想像"],
  ["事迹", "事蹟"],
];

/* 词表按首字分桶 + 长度降序，模块加载时建一次 */
const PHRASE_BUCKET = new Map<string, [string, string][]>();
for (const [p, t] of Object.entries(TRAD_PHRASES)) {
  const list = PHRASE_BUCKET.get(p[0]) ?? [];
  list.push([p, t]);
  PHRASE_BUCKET.set(p[0], list);
}
for (const list of PHRASE_BUCKET.values()) {
  list.sort((a, b) => b[0].length - a[0].length);
}

/** 简体字符串 → 繁体（词级最长匹配 → 单字映射 → 项目词级覆盖） */
export function toTrad(s: string): string {
  let out = "";
  let i = 0;
  while (i < s.length) {
    const cands = PHRASE_BUCKET.get(s[i]);
    let matched = false;
    if (cands) {
      for (const [p, t] of cands) {
        if (s.startsWith(p, i)) {
          out += t;
          i += p.length;
          matched = true;
          break;
        }
      }
    }
    if (!matched) {
      out += TRAD_CHARS[s[i]] ?? s[i];
      i += 1;
    }
  }
  for (const [a, b] of WORD_FIX) out = out.replaceAll(a, b);
  return out;
}

/** 深度转换：对象/数组中所有字符串值转繁（键不动；id/URL 等 ASCII
    天然不受影响）。hant 模式下整棵 site.json 内容层过一次。 */
export function tradDeep<T>(value: T): T {
  if (typeof value === "string") return toTrad(value) as T;
  if (Array.isArray(value)) return value.map((v) => tradDeep(v)) as T;
  if (value !== null && typeof value === "object") {
    const out: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
      out[k] = tradDeep(v);
    }
    return out as T;
  }
  return value;
}

/* ---------------- 朝代名 ---------------- */

const DYNASTY_EN: Record<string, string> = {
  秦: "Qin",
  西汉: "Western Han",
  新: "Xin",
  东汉: "Eastern Han",
  曹魏: "Cao Wei",
  蜀汉: "Shu Han",
  孙吴: "Sun Wu",
  西晋: "Western Jin",
  东晋: "Eastern Jin",
  前赵: "Former Zhao",
  后赵: "Later Zhao",
  前凉: "Former Liang",
  成汉: "Cheng Han",
  前燕: "Former Yan",
  前秦: "Former Qin",
  后燕: "Later Yan",
  后秦: "Later Qin",
  西秦: "Western Qin",
  后凉: "Later Liang",
  南凉: "Southern Liang",
  北凉: "Northern Liang",
  西凉: "Western Liang",
  胡夏: "Hu Xia",
  北燕: "Northern Yan",
  代: "Dai",
  刘宋: "Liu Song",
  南齐: "Southern Qi",
  梁: "Liang",
  陈: "Chen",
  北魏: "Northern Wei",
  东魏: "Eastern Wei",
  西魏: "Western Wei",
  北齐: "Northern Qi",
  北周: "Northern Zhou",
  隋: "Sui",
  唐: "Tang",
  武周: "Wu Zhou",
  后梁: "Later Liang",
  后唐: "Later Tang",
  后晋: "Later Jin",
  后汉: "Later Han",
  后周: "Later Zhou",
  前蜀: "Former Shu",
  后蜀: "Later Shu",
  杨吴: "Yang Wu",
  南唐: "Southern Tang",
  吴越: "Wuyue",
  闽: "Min",
  马楚: "Ma Chu",
  南汉: "Southern Han",
  荆南: "Jingnan",
  北汉: "Northern Han",
  北宋: "Northern Song",
  南宋: "Southern Song",
  辽: "Liao",
  金: "Jin",
  西夏: "Western Xia",
  元: "Yuan",
  明: "Ming",
  清: "Qing",
};

/** 朝代名：en→译名；hant→toTrad(简体)；hans→原文；查不到回退原文 */
export function dynastyLabel(zhLabel: string, lang: Lang): string {
  if (lang === "en") return DYNASTY_EN[zhLabel] ?? zhLabel;
  if (lang === "hant") return toTrad(zhLabel);
  return zhLabel;
}

/* ---------------- 六维品藻轴 ---------------- */

const AXIS: Record<string, { zh: string; en: string }> = {
  wugong: { zh: "武功", en: "Might" },
  wenzhi: { zh: "文治", en: "Governance" },
  taolue: { zh: "韬略", en: "Cunning" },
  guozuo: { zh: "国祚", en: "Longevity" },
  houxiao: { zh: "后效", en: "Legacy" },
  yuedan: { zh: "月旦", en: "Repute" },
};

/** 六维轴标签（jojo 戏作标签不在此列，保留中文） */
export function axisLabel(key: string, lang: Lang): string {
  const ax = AXIS[key];
  if (!ax) return key;
  if (lang === "en") return ax.en;
  if (lang === "hant") return toTrad(ax.zh);
  return ax.zh;
}

/* ---------------- 路线分组 ---------------- */

const GROUP: Record<string, { zh: string; en: string }> = {
  都城: { zh: "都城", en: "Capital" },
  巡狩: { zh: "巡狩", en: "Tour" },
  亲征: { zh: "亲征", en: "Campaign" },
  起兵: { zh: "起兵", en: "Uprising" },
  入关: { zh: "入关", en: "Pass Entry" },
  迁都: { zh: "迁都", en: "Capital Move" },
  流徙: { zh: "流徙", en: "Exile" },
  其他: { zh: "其他", en: "Other" },
};

/** 地图路线分组图例 */
export function groupLabel(g: string, lang: Lang): string {
  const gr = GROUP[g];
  if (!gr) return g;
  if (lang === "en") return gr.en;
  if (lang === "hant") return toTrad(gr.zh);
  return gr.zh;
}

/* ---------------- 关联类型 ---------------- */

const REL: Record<string, { zh: string; en: string }> = {
  predecessor: { zh: "前任", en: "Predecessor" },
  successor: { zh: "后任", en: "Successor" },
  kinship: { zh: "亲属", en: "Kin" },
  minister: { zh: "权臣/重臣", en: "Powerful Minister" },
  rival: { zh: "对手", en: "Rival" },
  related_emperor: { zh: "相关帝王", en: "Related Emperor" },
  other: { zh: "其他", en: "Other" },
};

/** 关联表「类型」列 */
export function relLabel(type: string, lang: Lang): string {
  const r = REL[type];
  if (!r) return type;
  if (lang === "en") return r.en;
  if (lang === "hant") return toTrad(r.zh);
  return r.zh;
}

/* ---------------- 人名拼音注音 ---------------- */

/** qin-shi-huang → Qin Shi Huang（机械分段首字母大写） */
export function pinyinOf(id: string): string {
  return id
    .split("-")
    .filter(Boolean)
    .map((seg) => seg[0].toUpperCase() + seg.slice(1))
    .join(" ");
}

/* ---------------- 在位年英文格式 ---------------- */

/** 在位年英文化："-221","-210" → "221–210 BC"；"-9","23" → "9 BC–23"；
    "618","626" → "618–626"（AD 不加后缀）；非数字原样回退 */
export function fmtReign(start: string, end: string): string {
  const s = parseInt(start, 10);
  const e = parseInt(end, 10);
  if (Number.isNaN(s) || Number.isNaN(e)) return `${start}—${end}`;
  if (s < 0 && e < 0) return `${-s}–${-e} BC`;
  if (s < 0) return `${-s} BC–${e}`;
  return `${s}–${e}`;
}

/* ---------------- 语言切换按钮 ---------------- */

export function LangSwitch() {
  const { lang } = useLang();
  return (
    <div className="lang-switch" role="group" aria-label="语言 / Language">
      <button
        type="button"
        className={lang === "hans" ? "on" : ""}
        onClick={() => setLang("hans")}
      >
        简体
      </button>
      <span className="lang-sep">/</span>
      <button
        type="button"
        className={lang === "hant" ? "on" : ""}
        onClick={() => setLang("hant")}
      >
        繁體
      </button>
      <span className="lang-sep">/</span>
      <button
        type="button"
        className={lang === "en" ? "on" : ""}
        onClick={() => setLang("en")}
      >
        EN
      </button>
    </div>
  );
}

/* ---------------- UI 文案字典 ---------------- */

export const STR: Record<string, { zh: string; en: string }> = {
  /* App */
  "app.loading": { zh: "加载图鉴数据…", en: "Loading compendium data…" },
  "app.loadError": { zh: "加载 site.json 失败", en: "Failed to load site.json" },
  "app.hint": {
    zh: "请先运行：python tools/build_site_data.py",
    en: "Run first: python tools/build_site_data.py",
  },

  /* 通用 */
  back: { zh: "← 返回图鉴", en: "← Compendium" },
  backPlain: { zh: "返回图鉴", en: "Back to Compendium" },
  reign: { zh: "在位", en: "r." },
  temple: { zh: "庙号", en: "Temple: " },
  posthumous: { zh: "谥", en: "Posthumous: " },
  "nf.title": { zh: "未找到人物", en: "Emperor not found" },
  "music.play": { zh: "播放背景音乐", en: "Play background music" },
  "music.stop": { zh: "关闭背景音乐", en: "Mute background music" },

  /* Gallery */
  "gallery.title": { zh: "皇帝图鉴", en: "Imperial Compendium" },
  "gallery.seal": { zh: "索引", en: "Index" },
  "gallery.sub": {
    zh: "奏折三栏专页 · 点卡即入",
    en: "Three-column memorial pages · click a card to enter",
  },
  "gallery.searchPh": {
    zh: "搜索姓名 / 朝代 / id…",
    en: "Search name / dynasty / id…",
  },
  "gallery.portraitPending": { zh: "画像在制", en: "Portrait in progress" },
  "share.copied": { zh: "已复制", en: "Copied" },
  "share.hint": { zh: "复制本页分享链接", en: "Copy the share link" },
  "chip.all": { zh: "全部", en: "All" },
  "chip.emperor": { zh: "正式", en: "Full" },
  "chip.quasi": { zh: "准", en: "Quasi" },
  "chip.read": { zh: "已读", en: "Read" },
  "badge.stub": { zh: "索引", en: "Index" },
  "badge.quasi": { zh: "准", en: "Quasi" },
  "st.read": { zh: "已读", en: "Read" },
  "st.star": { zh: "收藏", en: "Starred" },
  "st.wait": { zh: "待撰写", en: "Pending" },

  /* 封面 */
  "cover.quasi": { zh: "准帝王", en: "Quasi-Emperor" },
  "cover.open": { zh: "展开御览", en: "Unfold for Review" },
  "cover.direct": {
    zh: "直接展开，下次跳过封面",
    en: "Open directly and skip the cover next time",
  },

  /* 专页主文 */
  "hero.illuAlt": {
    zh: "{name}插画（AI 艺术想象）",
    en: "{name} — illustration (AI artistic reimagining)",
  },
  "hero.stubEmpty": { zh: "索引灰卡 · 待撰写", en: "Index stub · to be written" },
  "hero.noPortrait": { zh: "画像待补", en: "Portrait pending" },
  "sec.radar": { zh: "六维品藻", en: "Six-Axis Appraisal" },
  "radar.stub": { zh: "灰卡无品藻。", en: "Stub card: no appraisal." },
  "sec.bio": { zh: "主要事迹", en: "Key Deeds" },
  "bio.dead": { zh: "页未建", en: "page not built" },
  "sec.timeline": { zh: "年表大事", en: "Timeline" },
  "timeline.empty": {
    zh: "暂无年表（stub 或未同步史料卡）。",
    en: "No timeline yet (stub, or source cards not synced).",
  },
  "timeline.placeHint": {
    zh: "点击在地图中高亮",
    en: "Click to highlight on the map",
  },
  "timeline.related": { zh: "相关：", en: "Related: " },
  "sec.relations": { zh: "关联表", en: "Relations" },
  "relations.empty": { zh: "暂无关联。", en: "No relations." },
  "rel.type": { zh: "类型", en: "Type" },
  "rel.person": { zh: "人物", en: "Person" },
  "rel.note": { zh: "说明", en: "Note" },
  "rel.pending": { zh: "（待建）", en: "(pending)" },
  "sec.sources": { zh: "史料出处", en: "Sources" },
  "sources.empty": { zh: "暂无出处。", en: "No sources cited." },

  /* 目录 */
  "toc.aria": { zh: "奏折目录", en: "Memorial contents" },
  "toc.star": { zh: "☆ 收藏", en: "☆ Star" },
  "toc.starred": { zh: "★ 已收藏", en: "★ Starred" },
  "toc.index": { zh: "图鉴索引", en: "Compendium Index" },
  "toc.stub": { zh: "灰", en: "stub" },
  "toc.all": { zh: "全部图鉴 →", en: "All Emperors →" },
  "flag.quasi": { zh: "准", en: "Quasi" },
  "flag.read": { zh: "已读", en: "Read" },
  "toc.m-hero": { zh: "速览", en: "Overview" },
  "toc.m-radar": { zh: "六维品藻", en: "Six-Axis" },
  "toc.m-bio": { zh: "事迹", en: "Deeds" },
  "toc.m-timeline": { zh: "年表", en: "Timeline" },
  "toc.m-relations": { zh: "关联", en: "Relations" },
  "toc.m-sources": { zh: "出处", en: "Sources" },

  /* 地图 */
  "map.title": { zh: "一生地图", en: "Life Map" },
  "map.empty": { zh: "路线未录入。", en: "Routes not recorded." },
  "map.aria": { zh: "{name}路线图", en: "Route map of {name}" },
  "rmap.title": { zh: "一生轨迹 · 示意地图", en: "Life Route · Schematic Map" },
  "rmap.hint": {
    zh: "2D 弧线示意（非精确历史疆界）。点击下方事件可高亮对应点。坐标精度见地点库 schematic / approximate。",
    en: "2D arc schematic (not precise historical borders). Click an event below to highlight its point. For coordinate precision see the place library: schematic / approximate.",
  },
  "rmap.scope": {
    zh: "示意范围 · 中国历史地理",
    en: "Schematic extent · Historical geography of China",
  },
  "rmap.empty": { zh: "暂无路线数据", en: "No route data yet" },

  /* 品藻牌 */
  "plate.aria": { zh: "六维品藻图", en: "Six-axis appraisal chart" },
  "plate.unrated": { zh: "品藻未评", en: "Not Yet Appraised" },
  "plate.unratedNote": {
    zh: "此人尚无六维评分（video-01 二十人之外）。",
    en: "No six-axis scores for this emperor yet (beyond the video-01 twenty).",
  },
  "plate.merit": { zh: "功", en: "Merit" },
  "plate.demerit": { zh: "过", en: "Demerit" },
  "plate.note": {
    zh: "品藻戏作；史实见年表与出处。",
    en: "Appraisal is tongue-in-cheek; see the timeline and sources for history.",
  },
  "radar.aria": { zh: "六维能力图", en: "Six-axis ability chart" },

  /* StandLab */
  "lab.loading": { zh: "加载设定档…", en: "Loading profiles…" },
  "lab.title": { zh: "游戏化设定页 Lab · 第二轮", en: "Gamified Profile Lab · Round 2" },
  "lab.lead1": { zh: "史实骨架仍准，外壳按", en: "The historical skeleton stays accurate; the shell is a " },
  "lab.leadStrong": { zh: "好玩的游戏图鉴", en: "playful game dex" },
  "lab.lead2": {
    zh: "来——不是考据论文。六维保留；下面 5 套都是「娱乐展示」。点风格 + 人物对比。",
    en: ", not a research paper. The six axes remain; all five skins below are entertainment displays. Pick a style and compare emperors.",
  },
  "lab.pickStyle": { zh: "① 选风格（本轮全换新）", en: "① Pick a style (all new this round)" },
  "lab.pickEmperor": { zh: "② 选人物", en: "② Pick an emperor" },
  "lab.preview": { zh: "③ 预览 · ", en: "③ Preview · " },
  "lab.level": { zh: "Lv.{lv} · {pl} 阶", en: "Lv.{lv} · Tier {pl}" },
  "lab.hp": { zh: "国力 HP", en: "Power HP" },
  "lab.mp": { zh: "气运 MP", en: "Fortune MP" },
  "lab.skills": { zh: "技能（史实梗）", en: "Skills (history memes)" },
  "lab.ult": { zh: "必杀：", en: "Ult: " },
  "lab.weak": { zh: "破绽：", en: "Weakness: " },
  "lab.disclaimer": { zh: "玩法包装", en: "Entertainment wrap" },
  "lab.limited": { zh: "限定", en: "Limited" },
  "lab.charIntro": { zh: "角色简介", en: "Profile" },
  "lab.burst": { zh: "元素爆发 · 史实技", en: "Elemental Burst · Historical Skill" },
  "lab.constel": { zh: "命座吐槽：", en: "Constellation snark: " },
  "lab.threat": { zh: "威胁", en: "Threat" },
  "lab.hubar": { zh: "气运条", en: "Fortune" },
  "lab.mech": { zh: "机制点名（史实向）", en: "Mechanics (historical)" },
  "lab.openSkill": { zh: "开场技", en: "Opener" },
  "lab.enrageCry": { zh: "狂暴台词", en: "Enrage line" },
  "lab.enrageWeak": { zh: "狂暴破绽", en: "Enrage flaw" },
  "lab.lootHint": { zh: "掉落暗示", en: "Loot hint" },
  "lab.height": { zh: "身高：？？丈（玩笑）", en: "Height: ?? zhang (joke)" },
  "lab.catch": { zh: "捕获度：", en: "Catch rate: " },
  "lab.habitat": { zh: "出现地：", en: "Habitat: " },
  "lab.dexEntry": { zh: "图鉴说明", en: "Dex Entry" },
  "lab.wild": { zh: "野生习性：", en: "Wild behavior: " },
  "lab.power": { zh: "战力", en: "Power" },
  "lab.nextFoe": { zh: "下一任对手", en: "Next Opponent" },
  "lab.pickFrom": { zh: "从图鉴挑选", en: "Pick from the compendium" },
  "lab.super": { zh: "必杀技", en: "Super Move" },
  "lab.combo": { zh: "连招台词", en: "Combo Line" },
  "lab.countered": { zh: "被克制", en: "Countered By" },
  "lab.axesTitle": {
    zh: "六维仍是这些（史实向含义 / 游戏向别名）",
    en: "The six axes, unchanged (historical meaning / game alias)",
  },
  "lab.axAxis": { zh: "品藻", en: "Axis" },
  "lab.axAlias": { zh: "游戏感别名", en: "Game alias" },
  "lab.axMeaning": { zh: "含义（认真）", en: "Meaning (serious)" },
  "lab.tail": {
    zh: "选好风格字母回我；可组合例如「D 的图鉴机当总览，点进去用 A 状态菜单」。",
    en: "Reply with your chosen style letter; combos are fine, e.g. “D's dex machine as the overview, A's status menu inside”.",
  },
};
