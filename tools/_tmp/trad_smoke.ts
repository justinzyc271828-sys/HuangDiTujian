/* 繁体转换端到端冒烟：用真实 tradTable + i18n 代码转换真实 site.json
   构建：npx esbuild tools/_tmp/trad_smoke.ts --bundle --platform=node --outfile=tools/_tmp/trad_smoke.cjs && node tools/_tmp/trad_smoke.cjs */
import { readFileSync } from "node:fs";
import { toTrad, tradDeep } from "../../apps/web/src/i18n";

let fail = 0;
const eq = (simp: string, expect: string) => {
  const got = toTrad(simp);
  const ok = got === expect;
  if (!ok) fail++;
  console.log(`  [${ok ? "OK " : "✗✗"}] ${simp} -> ${got}${ok ? "" : `（期望 ${expect}）`}`);
};

console.log("—— 单元用例 ——");
eq("结束列国分立、建立中央集权帝制的秦帝国开创者", "結束列國分立、建立中央集權帝制的秦帝國開創者");
eq("统一", "統一");
eq("书同文", "書同文");
eq("中央集权", "中央集權");
eq("皇后", "皇后");
eq("皇太后", "皇太后");
eq("吕太后", "呂太后");
eq("高后", "高后");
eq("以后", "以後");
eq("亲征", "親征");
eq("咸阳", "咸陽");
eq("称始皇帝", "稱始皇帝");
eq("奏折三栏专页", "奏摺三欄專頁");
eq("画像在制", "畫像在製");
eq("王莽", "王莽");
eq("皇帝菩萨", "皇帝菩薩");

console.log("—— site.json 深度转换 ——");
const site = JSON.parse(readFileSync("apps/web/public/data/site.json", "utf-8"));
const conv = tradDeep(site);
const blob = JSON.stringify(conv);
for (const bad of ["皇後", "太後", "呂後", "竇後", "高後", "武後", "範曄", "薑維", "於禁", "封麵", "裏程碑"]) {
  const n = blob.split(bad).length - 1;
  if (n) {
    fail++;
    const i = blob.indexOf(bad);
    console.log(`  [✗✗] 误转 ${bad} ×${n}  例 …${blob.slice(Math.max(0, i - 20), i + 20)}…`);
  } else {
    console.log(`  [OK ] 无 ${bad}`);
  }
}
// 抽查秦始皇卡片字段
const qin = (conv.emperors ?? conv).find?.((e: any) => e.id === "qin-shi-huang") ?? null;
if (qin) {
  console.log("  秦始皇 summary:", qin.summary);
  console.log("  秦始皇 tags:", JSON.stringify(qin.tags));
} else {
  console.log("  （emperors 结构不同，跳过卡片抽查；看上方整体误转检查即可）");
}
console.log(fail ? `✗ 失败 ${fail} 处` : "✓ 全部通过");
process.exit(fail ? 1 : 0);
