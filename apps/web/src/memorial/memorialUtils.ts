export const DIRECT_KEY = "hdtj-memorial-direct";

/** 百分制评分 → 品第（stand_stats.json 为 0–100） */
export function gradeOfScore(v: number): string {
  if (v >= 90) return "S";
  if (v >= 75) return "A";
  if (v >= 60) return "B";
  if (v >= 45) return "C";
  if (v >= 30) return "D";
  return "E";
}

export const REL_LABEL: Record<string, string> = {
  predecessor: "前任",
  successor: "后任",
  kinship: "亲属",
  minister: "权臣/重臣",
  rival: "对手",
  related_emperor: "相关帝王",
  other: "其他",
};

export const TOC_ITEMS = [
  { id: "m-hero", label: "速览" },
  { id: "m-radar", label: "六维品藻" },
  { id: "m-bio", label: "事迹" },
  { id: "m-timeline", label: "年表" },
  { id: "m-relations", label: "关联" },
  { id: "m-sources", label: "出处" },
];

/** stub 灰卡下禁用跳转的目录项 */
export const STUB_DISABLED = new Set([
  "m-radar",
  "m-bio",
  "m-timeline",
  "m-relations",
]);
