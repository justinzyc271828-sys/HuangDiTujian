/* 全库繁体终审:真实 tradTable + i18n 转换全量 site.json(269 人语料)
   构建:npx esbuild tools/_tmp/trad_full_audit.ts --bundle --platform=node --outfile=tools/_tmp/trad_full_audit.cjs && node tools/_tmp/trad_full_audit.cjs */
import { readFileSync } from "node:fs";
import { toTrad, tradDeep } from "../../apps/web/src/i18n";

let fail = 0;
const eq = (simp: string, expect: string) => {
  const got = toTrad(simp);
  const ok = got === expect;
  if (!ok) fail++;
  console.log(`  [${ok ? "OK " : "✗✗"}] ${simp} -> ${got}${ok ? "" : `（期望 ${expect}）`}`);
};

console.log("—— 一词多繁·新语料词对 ——");
// 云:地名/人名转雲,说义不转
eq("云州", "雲州"); eq("云中", "雲中"); eq("云南", "雲南"); eq("云冈石窟", "雲岡石窟");
eq("燕云十六州", "燕雲十六州"); eq("赵云", "趙雲"); eq("或云", "或云");
// 准/沈
eq("准噶尔", "準噶爾"); eq("沈阳", "瀋陽");
// 于:人名不转
eq("于谦", "于謙"); eq("单于", "單于");
// 余:人名不转
eq("拓跋余", "拓跋余");
// 新语料专名
eq("刘䶮", "劉龑"); eq("蒙逊", "蒙遜"); eq("完颜", "完顏"); eq("爱新觉罗", "愛新覺羅");
eq("噶尔丹", "噶爾丹"); eq("赫图阿拉", "赫圖阿拉"); eq("宁远", "寧遠"); eq("萨尔浒", "薩爾滸");
eq("会稽", "會稽"); eq("临安", "臨安"); eq("襄阳", "襄陽"); eq("钓鱼城", "釣魚城");
eq("乐安", "樂安"); eq("土木堡", "土木堡"); eq("宣政院", "宣政院"); eq("澎湖", "澎湖");

console.log("—— site.json 全量深度转换扫描 ——");
const site = JSON.parse(readFileSync("apps/web/public/data/site.json", "utf-8"));
const simp = JSON.stringify(site);
const conv = JSON.stringify(tradDeep(site));
const badList = ["皇後","太後","呂後","竇後","高後","武後","範曄","薑維","於禁","封麵","裏程碑",
  "或雲","詩雲","史雲","書雲","語雲","於謙","單於","拓跋餘",
  "云州","云中","云南","准噶尔","沈阳", "趙云"];
for (const bad of badList) {
  const n = conv.split(bad).length - 1;
  if (n) {
    fail++;
    console.log(`  [✗✗] 出现 ${n} 次: ${bad}`);
    let i = -1, shown = 0;
    while ((i = conv.indexOf(bad, i + 1)) >= 0 && shown < 4) {
      console.log(`       上下文: ${JSON.stringify(conv.slice(Math.max(0, i - 14), i + bad.length + 6))}`);
      shown++;
    }
  }
}
console.log("  黑名单扫描完成(误转+残留)");
const diff = [...simp].filter((c, i) => conv[i] !== c).length;
console.log(`  转换差异字符数: ${diff}(简体 ${simp.length} 字)`);
if (fail === 0) console.log("✓ 全库繁体终审通过");
else { console.log(`✗ ${fail} 项失败`); process.exit(1); }
