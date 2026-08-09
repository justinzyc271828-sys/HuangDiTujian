#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the video-01 emperor illustration handoff package.

This exporter is deliberately separate from the older key-art prompt exports.
It preserves their appearance/costume research while replacing the static atlas
composition with the approved "mineral mural + ink motion" visual grammar.
Version 2 locks the rendering medium while assigning a different camera grammar
to every emperor so the series does not collapse into one repeated hero pose.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from keyart_appearance_data import SCENES  # noqa: E402


PACKAGE = ROOT / "assets" / "video-01" / "emperor-illustrations"
PROMPTS = PACKAGE / "prompts"
OUTPUTS = PACKAGE / "outputs"
VIDEO20 = ROOT / "data" / "catalog" / "video20.json"
PRIMARY_ANCHOR = ROOT / "assets" / "style-bible" / "v1" / "approved" / "01-qin-shi-huang-final-v1.png"
SECONDARY_ANCHOR = ROOT / "assets" / "style-bible" / "v1" / "references" / "emperor-series-ink-motion-v1.png"
QIN_OUTPUT = OUTPUTS / "01-qin-shi-huang.png"
SHI_LE_REJECTED = PACKAGE / "rejected" / "v2.3-shi-le-banner-pose" / "06-h-zhao-shi-le.png"
APPROVED_IDS = {
    "qin-shi-huang",
    "han-xuan-di",
    "han-wu-di",
    "xin-wang-mang",
    "e-han-guangwu",
    "h-zhao-shi-le",
    "liang-wu",
    "xixia-li-yuanhao",
    "q-qin-fu-jian",
    "n-wei-xiaowen",
    "sui-wen",
    "sui-yang",
    "tang-tai-zong",
    "zhou-wu-zetian",
    "tang-xian-zong",
    "zhou-shi",
}


FIXED_VISUAL_GRAMMAR = """LOCKED SERIES RENDERING GRAMMAR — lock the medium, mark-making and adult character design; do not lock the camera, palette distribution or Qin-specific objects:
an adult non-photoreal Chinese historical manga illustration fused with a mineral-pigment mural and forceful expressive ink motion; aged plaster and coarse paper; visibly granular mineral pigments selected from a character-specific palette; cracked wall, flaking pigment, dry-brush edges, flying-white ink and directional brush force; fragmented distressed gold leaf appears only when the per-emperor palette plan assigns it and must never become a universal gold-splatter overlay. Use no more than the assigned gold budget. Bold designed silhouette, decisive facial planes, expressive anatomy and controlled exaggeration. The emperor must remain the unmistakable visual subject and normally occupy 48–72 percent of the visual mass, but profile, rear three-quarter, overhead, ground-level, over-the-shoulder and off-center arrangements are all valid when assigned by the per-emperor camera plan. The viewer has a precise position inside the historical event. Participation may come from proximity, occlusion, eyeline, danger crossing the frame, shared movement or spatial pressure; it does not require a hand or prop aimed at the lens. Freeze the scene before the action finishes. Make the cracks, pigment and ink carry the event's direction and force rather than act as a decorative filter. The CAMERA PLAN and COLOR PLAN below are authoritative and must visibly differ from adjacent images."""

FIXED_AVOID = """static atlas portrait, museum-display pose, repeated centered frontal emperor, repeated low-angle hero shot, repeated table-edge composition, automatic hand-or-prop thrust at the camera unless explicitly assigned, universal black-and-gold treatment, gold dust scattered uniformly over the entire frame, excessive gold leaf above the assigned budget, generic dragon, generic throne, generic palace grandeur used as identity, photoreal skin, live-action cinematic realism, glossy 3D CGI, smooth generic AI-anime polish, cute or chibi styling, idol face, plastic costume, modern objects, European armor, Japanese samurai armor, readable text, letters, Chinese characters, pseudo-writing, logo, watermark, interface, radar chart, infographic, multiple competing focal characters, cropped crown, deformed hands, extra fingers, blood or gore"""


MOMENTS = {
    "qin-shi-huang": {
        "moment": "the imperial seal has just struck the six-state map and the old borders are cracking inward before the impact completes",
    },
    "han-xuan-di": {
        "moment": "he has already crossed the Weiyang curtain into his own rule and begins to release it as the former regent's broken shadow fades across the folds behind him",
    },
    "han-wu-di": {
        "moment": "the two halves of a small dark-bronze tiger tally have just aligned at his chest, authenticating the Mobei order as two symbolic cavalry routes begin to diverge toward the northern horizon",
    },
    "xin-wang-mang": {
        "moment": "his immaculate archaizing rite reaches its most perfect pose while his real shadow slides across a faded Duke-of-Zhou mural and a single floor crack reaches grounded failed currency and a toppled bronze measure",
    },
    "e-han-guangwu": {
        "moment": "the small Kunyang cavalry wedge breaks into the massive enemy line during a lightning flash",
    },
    "h-zhao-shi-le": {
        "moment": "he climbs the final Xiangguo steps toward the viewer while the grounded slave shackle he has left behind recedes far below",
    },
    "liang-wu": {
        "moment": "during the Taicheng siege, the starving eighty-five-year-old emperor receives an empty lacquer bowl from the viewer-attendant and lifts his eyes as cold siege light cuts across a ruined Buddhist shrine",
    },
    "xixia-li-yuanhao": {
        "moment": "in a symbolic 1038 founding-state instant, he turns away from the Song envoy's offered Han-style crown and broad robe, climbs the Xingqing altar in self-declared Tangut dress, and looks back into the viewer's eyes",
    },
    "q-qin-fu-jian": {
        "moment": "in a deliberate symbolic fusion of the war council boast and the Fei River disaster, his whip completes a proud lateral sweep while the army's orderly reflection begins to fracture into the coming rout",
    },
    "n-wei-xiaowen": {
        "moment": "in a symbolic fusion of the 493 move and the 494 dress reform, he crosses the Luoyang gate threshold in complete new court dress and turns once toward the old Xianbei guard left behind",
    },
    "sui-wen": {
        "moment": "from an unfinished Daxing inspection tower, the austere ruler waits for a single bronze plumb bob to stop moving as the new capital avenue and the last lowered southern standard settle onto the same measured axis",
    },
    "sui-yang": {
        "moment": "in a symbolic Jiangdu-night fusion, the once-handsome exhausted ruler raises a bronze mirror and shifts his eyes toward the homesick guard stopping beyond the door while the canal he built still glows beyond the cabin",
    },
    "tang-tai-zong": {
        "moment": "at Hulao, the twenty-three-year-old Prince of Qin reaches a coherent full draw one breath before release as two rival eagle-shaped pigment forces align beyond the arrow",
    },
    "zhou-wu-zetian": {
        "moment": "the elderly sovereign strides across a bronze threshold from the dim cinnabar Tang court into the violet Wu-Zhou central axis while both hands remain concealed inside formal overlapping sleeves",
    },
    "tang-xian-zong": {
        "moment": "the sleepless emperor turns from a chain-bound relief map toward the snow-covered Caizhou messenger as one clamp opens and several remain shut",
    },
    "zhou-shi": {
        "moment": "at Gaoping the young emperor and his central standard stop the collapsing line while a much smaller Zhao Kuangyin leads the first countercharge from the lower-left",
    },
    "n-tang-houzhu": {
        "moment": "during Jinling's fall, a rain-soaked blank poem sheet tears from his fingers and is about to vanish into fire-reflected river wind",
    },
    "n-song-tai-zu": {
        "moment": "the smiling toast reaches the generals at the instant the friendly banquet becomes an irreversible surrender of military command",
    },
    "yuan-shi-zu": {
        "moment": "the elderly khan-emperor casts a relay paiza onto the new provincial map as steppe roads, the Dadu axis and the southern sea connect",
    },
    "n-wei-taiwu": {
        "moment": "the Northern Wei cavalry breaks through the Hexi fortress gate during a snow-and-smoke impact",
    },
}


SHOT_PLANS = {
    "qin-shi-huang": {
        "code": "S01-HIGH-FRONT3Q-MWS-RADIAL",
        "elevation": "slightly high, looking down about 12 degrees from the envoy's side of the map",
        "azimuth": "near-frontal three-quarter view; the torso faces the map while the eyes cut toward the viewer",
        "scale": "28 mm wide medium-wide composition; the foreshortened arm and map create depth without hiding the face",
        "roll": "level horizon",
        "interaction": "the viewer is the envoy on the opposite edge of the map and witnesses the irreversible seal impact",
        "motion": "radial impact travels from the seal across the six-state map toward the frame edges",
        "foreground": "cracked mineral map, seal impact and scattered bamboo slips",
    },
    "han-xuan-di": {
        "code": "S02-EYE-CORRIDOR-FRONT3Q-CURTAIN-RELEASE",
        "elevation": "human eye level from inside the dim Weiyang corridor",
        "azimuth": "front three-quarter approach as the emperor steps through the opening and releases the curtain behind his left shoulder",
        "scale": "46 mm full three-quarter environmental figure; crown, face, both hands and planted stride remain readable",
        "roll": "level wet-stone horizon with a soft vertical curtain boundary",
        "interaction": "the viewer is a senior official inside the hall whose polished report is being silently tested against the real Chang'an street outside",
        "motion": "the heavy curtain settles behind the emperor while fine rain and wet wheel tracks continue inward from the ordinary street",
        "foreground": "one small low oil lamp and curtain folds occupy the left edge; no table, report pile or hand enters the lens",
    },
    "han-wu-di": {
        "code": "S03-EYE-BESIDEOTS-3Q-MS-TWINDIVERGE",
        "elevation": "eye level inside an imperial campaign pavilion, with no low-angle hero distortion",
        "azimuth": "viewed from beside, not directly behind, a kneeling general; the emperor stands left of center in a strong right-facing three-quarter view so both eyes and most facial planes remain readable",
        "scale": "45 mm waist-up medium shot with natural proportions; the emperor occupies about 58 percent of frame height and the foreground figure occupies less than 10 percent",
        "roll": "level horizon",
        "interaction": "the viewer stands beside the general receiving the authenticated imperial order, close enough to witness the tally but never blocking the ruler",
        "motion": "two long crimson-and-black ink routes diverge from the campaign map and travel away toward two distant Han cavalry columns on the Mobei horizon",
        "foreground": "only a narrow blurred sleeve edge and the corner of a blank wooden command tablet enter the lower-left; no foreground head, helmet or large hand",
        "pose": "stand fully upright with squared shoulders and a stable vertical spine; both elbows stay naturally bent close to the torso while both hands meet at chest height to align the two small halves of the bronze tiger tally, below the chin so the face remains unobstructed; keep both forearms inside the body silhouette; no pointing finger, no long reach, no leaning across the table and no twisting wrist",
    },
    "xin-wang-mang": {
        "code": "S04-EYE-LEFT3Q-MS-DUTCH-GROUNDED",
        "elevation": "eye level in a long ritual corridor, not from below",
        "azimuth": "left-facing three-quarter view with roughly seventy percent of the face readable; his body remains ritually aligned while his eyes glance sideways",
        "scale": "50 mm medium shot with the figure off-center on the right third and no lens distortion",
        "roll": "8-degree clockwise Dutch tilt that destabilizes the otherwise perfect ritual order",
        "interaction": "the viewer watches from between court ranks as the public image of a perfect Confucian restorer separates from the shadow of the usurping emperor",
        "motion": "a single coherent cast shadow travels diagonally across the Duke-of-Zhou mural while one grounded floor crack leads toward resting failed currencies; nothing is airborne",
        "foreground": "only two thin cropped court-robe edges frame the lower corners; every coin and measure rests on the floor with contact shadows",
    },
    "e-han-guangwu": {
        "code": "S05-LOW-SIDE-TRACK-WIDE-LATERAL",
        "elevation": "ground-level tracking height beside the charging horse, looking up about 12 degrees",
        "azimuth": "clean side-on three-quarter view as horse and rider race from left to right",
        "scale": "24 mm dynamic wide shot; the full horse neck, rider torso and breach remain legible",
        "roll": "4-degree counterclockwise kinetic tilt",
        "interaction": "the viewer rides abreast inside the small Kunyang cavalry wedge",
        "motion": "rain, mane, mud and spear shafts slash laterally left-to-right past the viewer",
        "foreground": "a cropped wet horse ear and flying mud establish the neighboring rider's position",
    },
    "h-zhao-shi-le": {
        "code": "S06-HIGH-DOWNSTAIR-FRONT3Q-ASCENT",
        "elevation": "from the top platform, looking down the rammed-earth stair at about 38 degrees",
        "azimuth": "front-left three-quarter view as he climbs directly toward the viewer and raises his eyes",
        "scale": "35 mm medium-wide full-body shot; he occupies about 58 percent of the visual mass",
        "roll": "level horizon and one strict stair vanishing system",
        "interaction": "the viewer stands where Xiangguo's new court would receive him at the top of the final step",
        "motion": "his upward stride opposes the downward receding stair lines while one off-axis banner shadow cuts diagonally across the earth",
        "foreground": "only the rough lip of the top step frames the bottom edge; the old shackle remains small on the distant lowest landing",
    },
    "liang-wu": {
        "code": "S07-EYE-ATTENDANT-TIGHT3Q-EMPTY-BOWL",
        "elevation": "eye level at arm's length inside the besieged Taicheng shrine chamber",
        "azimuth": "front-left three-quarter view as the aged emperor raises his eyes directly toward the last attendant",
        "scale": "55 mm tight medium shot from waist to head; the emperor occupies about 70 percent of the visual mass",
        "roll": "level and compressed, with one narrow lattice perspective behind him",
        "interaction": "the viewer is the attendant who has just handed him the final empty food bowl",
        "motion": "cold siege light cuts right-to-left across his face while beard tips, ash and a torn kasaya edge move in the same weak draft",
        "foreground": "no foreground hand or tray; the small empty bowl remains close to his chest inside his silhouette",
    },
    "xixia-li-yuanhao": {
        "code": "S08-CHEST-ENVOY-REAR3Q-ALTAR-ASCENT",
        "elevation": "chest-height viewpoint behind the Song envoy, looking upward only eight degrees toward the founding altar",
        "azimuth": "rear-left three-quarter body moving away while the compact ruler turns his broad round face back over his left shoulder",
        "scale": "40 mm medium-wide shot from mid-thigh upward; the ruler occupies about 65 percent of frame height",
        "roll": "level altar horizon with a strong diagonal stair rise",
        "interaction": "the viewer is the Song envoy whose offered Han-style insignia has just been refused",
        "motion": "the ruler climbs away while the red cap-knot, white narrow sleeve and altar banners all snap sideways in the Helan wind",
        "foreground": "only the lower-left edge of the envoy's supported tray is visible, holding the rejected black crown and folded broad crimson robe",
    },
    "q-qin-fu-jian": {
        "code": "S09-WATERLOW-FRONT3Q-WIDE-ARC",
        "elevation": "camera almost at river-surface height among the front-rank officers, looking upward only twelve degrees",
        "azimuth": "front-left three-quarter dismounted ruler on the bank, his face and whip hand fully readable in the upper-right",
        "scale": "28 mm wide medium shot with the ruler occupying about 58 percent of frame height and cold water filling the lower 45 percent",
        "roll": "level waterline",
        "interaction": "the viewer is a skeptical front-rank officer standing ankle-deep as the emperor challenges the river and fixes him with a confident gaze",
        "motion": "one continuous leather whip sweeps laterally above the water while orderly spear reflections fracture downward into ink-dark rout lines",
        "foreground": "rippling black-blue water and two cropped officer silhouettes at the extreme edges; no foreground hand or weapon points at the lens",
    },
    "n-wei-xiaowen": {
        "code": "S10-WAIST-SIDE-TRACK-THRESHOLD-CROSS",
        "elevation": "waist-height viewpoint just inside the Luoyang gate, parallel to the threshold",
        "azimuth": "clean left-to-right side profile stride with the young emperor turning his pale face only slightly toward the old guard-viewer",
        "scale": "45 mm full three-quarter shot from boots to crown; the emperor occupies about 67 percent of frame height",
        "roll": "level architecture with one hard vertical gate-shadow division",
        "interaction": "the viewer is the old Xianbei guard inside the gate whom the emperor silently expects to follow into the new order",
        "motion": "his complete crimson wide sleeve and robe hem travel rightward while caravan dust and the strapped old riding coat recede left-to-right behind him",
        "foreground": "only a narrow blurred edge of the guard's old braid and indigo fur collar enters the far right; nothing blocks the emperor",
    },
    "sui-wen": {
        "code": "S11-EYE-85MM-THIGHUP-FRONT3Q-PLUMB-FOCUS",
        "elevation": "level human eye height on an unfinished Daxing inspection tower",
        "azimuth": "front-left three-quarter view with the ruler studying a plumb line held beside, never across, his face",
        "scale": "85 mm intimate thigh-up environmental portrait; the emperor occupies about 72–78 percent of frame height",
        "roll": "strictly level with the plumb cord forming the dominant vertical",
        "interaction": "the viewer stands beside the imperial survey point and is silently responsible for whether the new order is truly straight",
        "motion": "the bronze plumb bob completes its final small oscillation while the distant capital avenue and lowered southern standard settle into alignment",
        "foreground": "only a low parapet edge below the waist; all people and architecture begin far behind the emperor to preserve human scale",
    },
    "sui-yang": {
        "code": "S12-EYE-70MM-RIGHT3Q-MIRROR-DOOR",
        "elevation": "intimate seated eye level inside a moored Jiangdu imperial barge cabin",
        "azimuth": "right-front three-quarter view as he keeps a bronze mirror raised in his only visible hand and turns his eyes toward the approaching guard",
        "scale": "70 mm medium-close shot from just above the knees to the complete soft headcloth; the emperor occupies about 70 percent of frame height",
        "roll": "2-degree clockwise Dutch tilt",
        "interaction": "the viewer is a silent attendant at the near door-side position, sharing the instant when the emperor recognizes the guard's betrayal",
        "motion": "the mirror remains calm while a cold doorway draft and upright spear shadows push against the jade canal current",
        "foreground": "only a cropped curtain edge and low lamp plane; no cup, spill, hand or weapon enters the foreground",
    },
    "tang-tai-zong": {
        "code": "S13-FULLDRAW-EYE-LEFT3Q-NORMALARROW",
        "elevation": "level human eye height beside the Qin command position at Hulao",
        "azimuth": "strong left three-quarter archer view with the young prince's profile, drawing anchor, raised bow grip and normal arrow all readable",
        "scale": "50 mm thigh-up environmental action portrait; Li Shimin occupies about 72 percent of frame height while the Hulao gate and two eagle pigment fields remain legible",
        "roll": "level horizon",
        "interaction": "the viewer stands beside the young commander at the held breath before release and follows his sightline toward the two rival forces",
        "motion": "the drawn bowstring stores force while the indigo and cinnabar eagle-shaped pigment currents align beyond the short arrowhead without being touched",
        "foreground": "only the cropped lower edge of the vermilion cape and dark armor; no second person, horse or weapon enters the lens",
    },
    "zhou-wu-zetian": {
        "code": "S14-LOW50-THRESHOLD-STRIDE-HIDDENHANDS",
        "elevation": "restrained low view from the kneeling court axis, looking upward about eight degrees",
        "azimuth": "near-frontal three-quarter stride with the sovereign slightly left of center and the Jinlun state emblem separated on the right",
        "scale": "45–50 mm full environmental figure; the ruler occupies about seventy percent of frame height without wide-angle distortion",
        "roll": "level axial architecture and one horizontal bronze threshold",
        "interaction": "the viewer is a kneeling senior official directly confronted as the new sovereign crosses into the receiving court",
        "motion": "the leading foot crosses from cinnabar shadow into the violet aisle while robe hems trail backward and the fixed-open curtains frame the passage",
        "foreground": "two soft dark shoulders of kneeling officials frame the lower corners; no hand, decree or table enters the lens",
    },
    "tang-xian-zong": {
        "code": "S15-EYE85-PROFILE-TURN-MESSENGER",
        "elevation": "eye level from the kneeling messenger's position just inside the palace doorway",
        "azimuth": "right-facing body profile on the left third, with the emperor's head turned sharply three-quarter toward the viewer",
        "scale": "70–85 mm compressed medium-close shot separating candle, ruler, chain-bound map and snowy doorway",
        "roll": "subtle three-degree clockwise tension tilt",
        "interaction": "the viewer is the snow-covered Caizhou messenger whose arrival interrupts the ruler's sleepless watch",
        "motion": "snow ink travels from the distant gate through the doorway toward the released map clamp and across the robe edge",
        "foreground": "one soft snow-caked messenger shoulder at viewer-right and one out-of-focus iron candle cup at viewer-left",
    },
    "zhou-shi": {
        "code": "S16-EYE50-EMPERORAXIS-ZHAOCORNER",
        "elevation": "eye height from one Later Zhou soldier halted inside the retreat",
        "azimuth": "Chai Rong and black horse dominate the central-right foreground while Zhao Kuangyin remains a small mounted subordinate in the lower-left",
        "scale": "50 mm medium-wide view; the emperor occupies roughly two-thirds frame height without wide-angle distortion",
        "roll": "nearly level with only a two-degree clockwise tension tilt",
        "interaction": "the viewer is a wavering Later Zhou soldier whose retreat is stopped by the emperor's horse, gaze and central command standard",
        "motion": "pale dust and fleeing bodies move downhill while Chai Rong interrupts the current and Zhao's smaller cavalry wedge echoes the uphill countercharge",
        "foreground": "one blurred dark shield rim at the extreme lower-right, with no visible foreground face or hand",
    },
    "n-tang-houzhu": {
        "code": "S17-OUTSIDE-LATTICE-REARPROFILE-MS-LATERAL",
        "elevation": "eye level outside the rain-dark lattice window",
        "azimuth": "rear-left profile inside the room, face turned only partly toward the escaping paper",
        "scale": "50 mm medium shot through the window grid, with the figure large but interrupted by architecture and rain",
        "roll": "level melancholic frame",
        "interaction": "the viewer is outside in the storm where the lost poem sheet is about to pass, separated from the ruler by lattice and rain",
        "motion": "paper, torn silk, ink and fire-reflected rain stream sideways from the room into the night",
        "foreground": "wet lattice bars, rain beads and the blurred edge of the flying blank sheet",
    },
    "n-song-tai-zu": {
        "code": "S18-EYE-SEATEDPOV-OFFCENTER-MS-CIRCULAR",
        "elevation": "seated guest eye level at the banquet",
        "azimuth": "relaxed right three-quarter view with the emperor on the far-left third, turning across a circular table rather than facing front",
        "scale": "40 mm medium-wide composition that includes neighboring generals as cropped edge silhouettes",
        "roll": "level and deceptively calm",
        "interaction": "the viewer is one armed founding general inside the friendly circle and senses the trap closing socially rather than physically",
        "motion": "cups pass around the circle while swords and loosened armor slide away laterally under the table edge",
        "foreground": "the viewer's cup and armored wrist remain low and off-center, never blocking the emperor's face",
    },
    "yuan-shi-zu": {
        "code": "S19-HIGH-REAR3Q-WIDE-OUTWARD",
        "elevation": "slightly high 20-degree view from behind the map platform",
        "azimuth": "broad rear three-quarter silhouette with the elderly face turning over the right shoulder toward the linked horizons",
        "scale": "28 mm wide environmental composition; the ruler remains the largest single form while Dadu, steppe and sea unfold beyond",
        "roll": "level panoramic horizon",
        "interaction": "the viewer stands beside an envoy at the map edge and looks outward along the imperial network",
        "motion": "the relay paiza skids laterally across the map as horse-light trails radiate away toward distant roads and sea",
        "foreground": "map edge, saddle leather and a cropped envoy hand at rest, with no object thrown at camera",
    },
    "n-wei-taiwu": {
        "code": "S20-SADDLELOW-PASSING-WIDE-DUTCH-THROUGH",
        "elevation": "saddle-level low camera just inside the broken Hexi gate, looking up about 18 degrees",
        "azimuth": "front-side passing angle: horse and emperor enter from center-right and sweep past toward the left background instead of charging straight at camera",
        "scale": "20 mm extreme wide action shot with gate splinters, horse body and rider face all readable",
        "roll": "9-degree clockwise Dutch tilt",
        "interaction": "the viewer crouches inside the breached gate as the first cavalry rank rushes past into the fortress",
        "motion": "horse, lance, snow, smoke and shattered timber cut diagonally through and away from the camera position",
        "foreground": "broken gate beam and iron-blue snow streak across the near right edge",
    },
}


PALETTE_PLANS = {
    "qin-shi-huang": {
        "code": "C01-BLACK-OCHRE-STONEBLUE-G3",
        "dominant": "ink-black robes, earthen ochre wall, broken stone-blue and muted six-state mineral colors",
        "gold": "G3 approved-anchor density, roughly 8–12 percent, concentrated in map fissures, robe trim and impact fragments",
        "light": "dry neutral daylight with a severe bronze warmth at the seal impact",
        "surface": "large cracked mural plates and sharp radial gold fractures",
    },
    "han-xuan-di": {
        "code": "C02-RAINBLUE-SOOT-LINEN-BRONZE-G0",
        "dominant": "cold rain blue-gray, soot-brown curtain and robe, undyed linen, wet stone and restrained oxidized bronze-green",
        "gold": "G0 no gold leaf, gilded trim, gold dust or yellow-gold glow",
        "light": "cold rainy street light on the face and threshold opposed by one very small muted oil-lamp rim",
        "surface": "heavy cloth folds, wet-stone reflections, broad carbon shadow fragments and thin flying-white rain",
    },
    "han-wu-di": {
        "code": "C03-CRIMSON-IRON-SAND-COBALT-G0",
        "dominant": "deep campaign crimson and iron-black against pale desert sand and a cold cobalt northern sky",
        "gold": "G0 no gold leaf, no gilding and no floating gold dust; the tiger tally and belt hardware are dark patinated bronze, never bright yellow or shiny gold",
        "light": "cold high-altitude daylight with a hard sand-colored horizon",
        "surface": "long horizontal wind-scoured ink streaks, broad crimson cloth planes and pale sand abrasion, not map-like cracking or black-gold speckling",
    },
    "xin-wang-mang": {
        "code": "C04-VERDIGRIS-CHALK-CYAN-BRONZE-G0",
        "dominant": "oxidized verdigris, chalk white, cold cyan-gray and dull brown bronze",
        "gold": "G0 near-absent, maximum 1 percent, only a dead tarnished line on ritual hardware; absolutely no floating gold dust",
        "light": "flat cold ritual light with a faint sickly green cast",
        "surface": "rigid geometric plaster seams interrupted by vertical bronze and currency fragments",
    },
    "e-han-guangwu": {
        "code": "C05-STORMBLUE-MUD-SILVER-RED-G0",
        "dominant": "storm blue, charcoal rain, wet earth brown, lightning silver and one torn muted-red banner",
        "gold": "G0 no gold leaf; metallic accents are wet iron and lightning silver",
        "light": "blue-black thunderstorm split by a single white lightning flash",
        "surface": "wet pigment runs, mud splashes and rain-cut ink diagonals",
    },
    "h-zhao-shi-le": {
        "code": "C06-EARTH-RUST-LINEN-INK-G0",
        "dominant": "rammed-earth ochre, iron rust, coarse linen gray and heavy ink-black",
        "gold": "G0 no gold leaf or gilding",
        "light": "low dusty side light with ember-red rust highlights",
        "surface": "coarse scraped earth, worn stair edges, iron abrasion and one diagonal banner-shadow brush stroke",
    },
    "liang-wu": {
        "code": "C07-ASHCELADON-BONE-OXBLOOD-STEEL-G1",
        "dominant": "cold ash-celadon, bone white, carbon black, dead oxblood red and narrow steel-blue",
        "gold": "G1 maximum 1 percent, only a sick tarnished remnant in the cracked Buddha halo; no gold on the emperor and no speckles",
        "light": "cold steel-blue siege daylight isolates the face against a charcoal shrine interior, with one dying oxblood lamp accent",
        "surface": "large matte chalk-mineral planes, carbon-ink fractures, dry ash and sparse scraped vermilion; no sepia wash or micro-speckle texture",
    },
    "xixia-li-yuanhao": {
        "code": "C08-BONE-NAVY-CARMINE-TURQUOISE-G1",
        "dominant": "bone-white Tangut tunic and rammed earth, deep navy-black shadow, one carmine-red cap knot and tiny weathered turquoise accents",
        "gold": "G1 maximum 1 percent, only one worn line on the altar edge; no gold on costume, sky or frame",
        "light": "hard pale Hexi sun cuts the high nose and hawk eyes while banner shadows cross the white altar",
        "surface": "chalky bone-white planes, blocky carbon-ink fractures, narrow carmine wind strokes and restrained square woven motifs",
    },
    "q-qin-fu-jian": {
        "code": "C09-RIVERBLUE-PURPLE-SILVER-INK-G1",
        "dominant": "cold river blue-gray, bruised imperial purple, oxidized spear silver, charcoal armor and deep liquid ink",
        "gold": "G1 maximum 1 percent, one thin worn line on a belt fitting only; the whip is black leather, not gold",
        "light": "cold reflected river light under a bruised gray sky",
        "surface": "watery mineral blooms, one broad lateral whip stroke and downward reflections breaking from disciplined lines into chaotic liquid ink",
    },
    "n-wei-xiaowen": {
        "code": "C10-PALESTONE-INDIGO-CELADON-HANRED-G0",
        "dominant": "pale Luoyang stone, deep indigo, muted celadon and restrained Han red",
        "gold": "G0 no gold leaf; use pale stone cracks and cloth contrast instead",
        "light": "clear soft city-gate daylight",
        "surface": "architectural plaster planes, streaming migration dust and long folded-cloth strokes",
    },
    "sui-wen": {
        "code": "C11-SLATE-INK-CHALK-TEAL-CINNABAR-G0",
        "dominant": "cold slate blue-gray, ink-black cloth, chalk stone, pale rammed earth, oxidized river teal and one tiny muted-cinnabar southern standard",
        "gold": "G0 no gold leaf, gilded trim or airborne gold particles",
        "light": "cold clear construction-morning side light modeling the ruler's forehead planes and vertical plumb cord",
        "surface": "matte repaired cloth, chalky parapet stone, one taut fiber line and compressed dry-brush architectural vanishing lines",
    },
    "sui-yang": {
        "code": "C12-WINE-JADE-INDIGO-STEEL-G1",
        "dominant": "wine crimson, dark jade green, night indigo and cold blade steel",
        "gold": "G1 maximum 2 percent, confined to the bronze mirror rim and one small belt buckle",
        "light": "humid lantern red opposed by a cold steel reflection",
        "surface": "damp wine-crimson silk, dark lacquer, jade canal reflections and narrow cabin shadows over dry mural grain",
    },
    "tang-tai-zong": {
        "code": "C13-SLATE-IVORY-IRON-AZURITE-CINNABAR-G1",
        "dominant": "cold slate and mineral ivory, iron-blue armor, one azurite eagle field and one restrained cinnabar eagle field",
        "gold": "G1 maximum 2 percent, confined to dull bow and armor fasteners; no decorative gold field or uniform speckle layer",
        "light": "clear dry Hulao daylight models the young face, thumb-draw anchor, normal arrow and bow grip",
        "surface": "crisp lamellar rhythm and bow tension opposed by broad two-color eagle brush fields and chalky pass cliffs",
    },
    "zhou-wu-zetian": {
        "code": "C14-VIOLET-CINNABAR-IVORY-CLEANBRONZE-G2",
        "dominant": "deep imperial violet, aged cinnabar, cold ivory, soot black and muted teal-gray",
        "gold": "G2 restrained clean bronze reserved for the complete eight-spoke state emblem, threshold, crown hardware and curtain hooks; no random gold dust",
        "light": "dim cinnabar old-court shadow behind against a clearer cold-ivory and violet receiving axis ahead",
        "surface": "heavy tied-back curtain fields, overlapping mineral-cloth sleeves, one clean bronze threshold and a coherent polished wheel relief",
    },
    "tang-xian-zong": {
        "code": "C15-SNOWCYAN-AMBER-CHARCOAL-PURPLE-G0",
        "dominant": "cold snow cyan, charcoal-black, deep blue-purple, candle amber and one tiny oxide-red seal-cord accent",
        "gold": "G0 no gold leaf, gold glitter or scattered gold flecks",
        "light": "cold doorway light and one amber candle split the emperor's turned face",
        "surface": "dry-brush frost, flaking charcoal pigment, restrained flying-white snow ink and matte iron clamps",
    },
    "zhou-shi": {
        "code": "C16-DUST-IRONBLUE-IMPERIALRED-LEATHER-G0",
        "dominant": "dust ochre, iron blue-gray, soot charcoal, black-brown leather and disciplined deep vermilion",
        "gold": "G0 no gold leaf, glitter, gold dust or black-gold overlay",
        "light": "hard autumn side light filtered through Gaoping dust",
        "surface": "matte iron lamellae, cracked mineral dust, weathered black-vermilion command textiles and flying-white countercharge strokes",
    },
    "n-tang-houzhu": {
        "code": "C17-RAINBLUE-INK-SILKWHITE-FIREORANGE-G0",
        "dominant": "rain blue, pooled ink-black, wet silk white and distant fire orange",
        "gold": "G0 no gold leaf; distant fire supplies the only warm sparkle",
        "light": "cold rain foreground with unstable orange reflections from Jinling's fall",
        "surface": "wet paper feathering, rain beads, torn silk and diluted ink blooms",
    },
    "n-song-tai-zu": {
        "code": "C18-AMBER-LACQUERRED-UMBER-STEEL-G1",
        "dominant": "candle amber, lacquer red, deep umber and quiet sword steel",
        "gold": "G1 maximum 2 percent, limited to cup rim and belt fittings",
        "light": "warm circular banquet candlelight with a cool shadow under the table",
        "surface": "smoky circular brush currents, dark lacquer planes and restrained metallic edges",
    },
    "yuan-shi-zu": {
        "code": "C19-STEPPEGREEN-COBALT-SEA-LEATHER-G1",
        "dominant": "steppe green, sky cobalt, sea turquoise and saddle-leather brown",
        "gold": "G1 maximum 3 percent, aged bronze on the paiza and harness only",
        "light": "open panoramic daylight shifting from dry steppe to maritime haze",
        "surface": "wind-combed grass strokes, salt spray and long network trails across broad color fields",
    },
    "n-wei-taiwu": {
        "code": "C20-SNOWBLUE-SMOKEBLACK-HORSEBROWN-RUST-G0",
        "dominant": "iron snow blue, smoke black, horse brown and gate-timber rust red",
        "gold": "G0 no gold leaf; all glints are cold iron and ice",
        "light": "violent blue-white snow light cut by black smoke",
        "surface": "splintered wood grain, ice scratches, smoke drag and diagonal cavalry impact",
    },
}


IDENTITY_OVERRIDES = {
    "han-wu-di": """an East Asian man about 38, a reconstructed mature Western-Han sovereign at the height of imperial expansion, broad rectangular face, strong jaw, thick straight eyebrows, deep-set forceful eyes, high straight nose, neat short moustache and compact chin beard, wide shoulders, calm forward-driving authority rather than battlefield rage, COSTUME: deep crimson Western-Han wide-sleeve imperial court robe with sober ink-black edging, black martial court cap, broad dark leather belt and muted sash cords, no helmet, no exposed lamellar cuirass and no frontline cavalry-general costume, ACCESSORIES AND PROPS: a small palm-length dark-patinated bronze tiger tally made of two matching elongated halves aligned together, an unfolded Mobei campaign map without readable writing, a restrained imperial seal, and a Chinese ring-pommel sword resting horizontally on a stand rather than worn or brandished""",
}


CHARACTER_AVOID = {
    "han-wu-di": """frontline warrior pose, mounted emperor, general's helmet, full battlefield armor, emperor shown physically leading the distant Mobei cavalry, face hidden in side-back view, foreground general head blocking the emperor, oversized foreground officer, hunched spine, leaning over the table, stretched or elongated arm, overextended elbow, twisted wrist, pointing index finger, hand pressing a tiger statue into the map, golden tiger sculpture, shiny gold tiger figurine, oversized tiger object, ceremonial ornament mistaken for the military tally""",
}


DIRECT_PROMPT_OVERRIDES = {
    "han-xuan-di": (
        (PACKAGE / "prompts" / "revisions" / "02-han-xuan-di-v3-subtle-edit.txt")
        .read_text(encoding="utf-8")
        .split("=== EDIT PROMPT (copy verbatim) ===", 1)[1]
        .split("=== SAVE CONTRACT ===", 1)[0]
        .strip()
    ),
    "sui-wen": (
        (PACKAGE / "prompts" / "revisions" / "11-sui-wen-v3-close-identity.txt")
        .read_text(encoding="utf-8")
        .split("=== POSITIVE PROMPT (copy verbatim) ===", 1)[1]
        .split("=== SAVE CONTRACT ===", 1)[0]
        .strip()
    ),
    "sui-yang": (
        (PACKAGE / "prompts" / "revisions" / "12-sui-yang-v3-single-visible-hand.txt")
        .read_text(encoding="utf-8")
        .split("=== FINAL ENGLISH GENERATION PROMPT ===", 1)[1]
        .split("=== SAVE CONTRACT ===", 1)[0]
        .strip()
    ),
    "tang-tai-zong": (
        (PACKAGE / "prompts" / "revisions" / "13-tang-tai-zong-v6-normal-arrow-full-draw.txt")
        .read_text(encoding="utf-8")
        .split("=== FINAL ENGLISH GENERATION PROMPT ===", 1)[1]
        .split("=== QA NOTES ===", 1)[0]
        .strip()
    ),
    "zhou-wu-zetian": (
        (PACKAGE / "prompts" / "revisions" / "14-zhou-wu-zetian-v9-hidden-hands-threshold-stride.txt")
        .read_text(encoding="utf-8")
        .split("=== FINAL ENGLISH GENERATION PROMPT ===", 1)[1]
        .split("=== QA NOTES ===", 1)[0]
        .strip()
    ),
    "tang-xian-zong": (
        (PACKAGE / "prompts" / "revisions" / "15-tang-xian-zong-v2-chainbound-map-messenger.txt")
        .read_text(encoding="utf-8")
        .split("=== FINAL ENGLISH GENERATION PROMPT ===", 1)[1]
        .split("=== QA NOTES ===", 1)[0]
        .strip()
    ),
    "zhou-shi": (
        (PACKAGE / "prompts" / "revisions" / "16-zhou-shi-v4-neutral-command-banners.txt")
        .read_text(encoding="utf-8")
        .split("=== FINAL ENGLISH EDIT PROMPT ===", 1)[1]
        .split("=== QA NOTES ===", 1)[0]
        .strip()
    ),
    "han-wu-di": f"""Create one 16:9 Chinese historical action illustration with no text or interface.

SERIES STYLE: adult non-photoreal Chinese historical manga fused with an aged mineral-pigment mural. Use coarse plaster and paper grain, dry-brush edges, flaking mineral pigment, flying-white ink and long directional brush strokes. Keep the protagonist bold, mature and anatomically believable. Use reference image 1 ({PRIMARY_ANCHOR}) only for the mineral-mural material, adult graphic-novel rendering and strong character presence; do not copy its Qin props, camera angle, map impact or black-and-gold density. Use reference image 2 ({SECONDARY_ANCHOR}) only for expressive ink flow.

HISTORICAL SUBJECT: Emperor Liu Che, Han Wudi, reconstructed at about age 38 during the Western Han Mobei campaign decision. He is the sovereign authorizing the expedition, not a general physically fighting at Langjuxu. Give him a broad rectangular mature face, strong jaw, thick straight eyebrows, deep-set forceful eyes, high straight nose, neat short moustache and compact chin beard, wide shoulders and calm, relentless strategic authority. His expression is controlled and decisive, not shouting.

COSTUME: a deep crimson Western-Han wide-sleeve imperial court robe with sober ink-black edging, a black martial court cap, a broad dark leather belt and muted sash cords. No helmet, no exposed lamellar cuirass, no cavalry armor. A Chinese ring-pommel sword rests horizontally on a stand behind him; he does not wear or brandish it.

SIGNATURE MOMENT AND NATURAL POSE: freeze the instant when the two matching halves of a small palm-length dark-patinated bronze tiger tally align at his sternum to authenticate the Mobei order. The tally is a flat elongated split-tiger military token, not a sculpture or decorative figurine. He stands completely upright with squared shoulders and a stable vertical spine. Both elbows remain naturally bent close to his torso. Both hands meet comfortably at chest height below the chin, so the face is fully visible. Both forearms remain inside his body silhouette. No pointing, no reaching across the table, no hunched back, no twisted wrist.

CAMERA AND COMPOSITION: eye-level 45 mm waist-up medium shot, natural proportions, level horizon. View him from beside a kneeling general, not directly behind the general. Place the emperor slightly left of center in a strong right-facing three-quarter view; both eyes and most facial planes must remain readable. He occupies about 58 percent of frame height and is unquestionably the largest focal figure. The general is represented only by a narrow blurred dark sleeve edge and the corner of a blank wooden command tablet in the lower-left, less than 10 percent of the image. No foreground head or helmet.

EVENT ENVIRONMENT: an imperial campaign pavilion opens onto a symbolic cold northern horizon. A large unfolded campaign map lies below the emperor without readable writing. From the map, two long crimson-and-black ink routes diverge away into the distance and become two small Han cavalry columns led by generals, moving toward a dark Langjuxu mountain silhouette. The emperor remains clearly inside the pavilion; the distant cavalry is the consequence of his decision, not his physical location. Keep all secondary riders small and low-detail.

COLOR AND SURFACE: deep campaign crimson and iron-black against pale desert sand and a cold cobalt-blue sky. Cold high-altitude daylight, broad crimson cloth planes, pale wind-scoured sand abrasion and long horizontal ink streaks. G0 gold budget: absolutely no gold leaf, no gilding, no floating gold dust and no black-and-gold speckle overlay. The tiger tally, seal and belt hardware are dark oxidized bronze, never bright yellow or shiny gold.

HARD EXCLUSIONS: no generic throne portrait, no frontline warrior pose, no mounted emperor, no full battle armor, no emperor leading the distant cavalry, no hidden side-back face, no oversized foreground officer, no stretched or elongated arm, no overextended elbow, no pointing finger, no hand pressing an object into the map, no golden tiger statue, no shiny tiger figurine, no oversized tiger object, no readable letters or Chinese characters, no logo, watermark, UI, radar chart, photoreal skin, live-action realism, glossy 3D, smooth generic anime, chibi, idol face, European armor, samurai armor, extra fingers, deformed hands, blood or gore.""",
    "xin-wang-mang": f"""Create one 16:9 Chinese historical action illustration with no text or interface.

SERIES STYLE: adult non-photoreal Chinese historical manga fused with an aged mineral-pigment mural. Use cold plaster grain, flaking pigment, dry-brush edges, restrained flying-white ink and precisely controlled geometric cracks. Keep the protagonist mature, anatomically believable and visually dominant. Use reference image 1 ({PRIMARY_ANCHOR}) only for mineral-mural material, adult graphic-novel rendering and strong character presence; do not copy its Qin props, frontal camera, map impact or black-and-gold density. Use reference image 2 ({SECONDARY_ANCHOR}) only for directional ink force. This image must feel colder, more rigid and more artificially perfect than the first three approved images.

HISTORICAL SUBJECT: Wang Mang in his early fifties at the beginning of the Xin dynasty, deliberately presenting himself as a new Duke of Zhou and an impeccably orthodox Confucian restorer while using that image to legitimize usurpation. He is not a generic emperor. Give him an excessively regular pale face, narrow non-martial shoulders, a carefully trimmed Confucian moustache and beard, composed lips forming a polite mask-like smile that does not reach the eyes, faint tension at the jaw, and a calculating sideways gaze directed toward the watching court. The contrast between public humility and private control must be visible in his face.

COSTUME: hyper-correct archaizing ritual dress inspired by an imagined Zhou order: a dark blue-black ceremonial upper robe over a dull dark-red lower garment, cold intricate woven borders, complete knee-cover apron, broad sash, restrained jade pendants and a formal flat-board ceremonial crown with sparse hanging bead strings. The clothing must look over-designed and doctrinally perfect rather than luxurious. No dragon robe, no golden crown, no military armor, no weapon and no bright celebratory red-and-gold palette.

SIGNATURE MOMENT AND NATURAL POSE: freeze the instant when Wang Mang completes a perfectly measured ritual bow and straightens again. He stands fully upright, shoulders level and chin slightly lowered in performed humility. Both elbows stay close to the torso. Both hands hold one narrow pale gray-green jade gui vertically against the sternum, fingers naturally stacked around its lower third, gripping slightly too tightly so the knuckles become pale. The gui is a plain flat ceremonial tablet, not a large carved sculpture. His body remains ceremonially obedient, but his eyes cut sideways toward the court and the fixed smile remains unchanged.

CAMERA AND COMPOSITION: eye-level 50 mm medium shot in a long ritual corridor, with an 8-degree clockwise Dutch tilt that makes the perfect architecture subtly unstable. Place Wang Mang off-center on the right third in a left-facing three-quarter view, not a strict profile; approximately seventy percent of his face, both eyes and the mask-like smile must remain readable. He occupies about 58 percent of frame height and remains the largest focal subject. Receding columns and court ranks use one coherent vanishing point toward the left. The viewer stands between two court ranks; use only thin cropped dark robe edges at the extreme lower corners. No large foreground head, viewer hand or object aimed at the lens.

WANG-MANG-SPECIFIC SYMBOLISM: on the plaster wall behind him is one faded, textless archaic mural silhouette of the idealized Duke of Zhou holding a ritual tablet. Wang Mang's single anatomically plausible cast shadow crosses and partially overlaps that mural, but the shoulder line and crown do not align, exposing the gap between borrowed virtue and imperial ambition. The shadow must remain a normal human shadow cast by one cold side light, not a monster, ghost or separate person.

GROUNDED EVIDENCE OF FAILED REFORM: absolutely nothing is falling or suspended in the air. On the stone floor, one narrow crack follows the corridor's single vanishing point from Wang Mang's feet toward a small group of failed reform objects: several ancient knife-shaped bronze coins, several spade-shaped bronze coins, a few broken fragments and one toppled cracked bronze measuring vessel. Every object lies flat or rests naturally on the floor, scales down correctly with distance and has a clear contact shadow. Keep the objects sparse and clustered, not scattered everywhere. At most six distant court officials react subtly; no repeated cloned crowd.

COLOR AND SURFACE: oxidized verdigris, chalk white, cold cyan-gray, dull dark bronze, blue-black and a restrained bruised purple. One cold side light must generate the coherent cast shadow and a faint sickly green atmosphere. G0 gold budget: no gold leaf, no gilding and no floating gold dust. Use rigid plaster seams, tarnished bronze patina, one grounded floor fracture and the misaligned mural-shadow overlap instead of black-and-gold speckling. One small over-saturated cinnabar seal may provide the only warm accent.

HARD EXCLUSIONS: no strict side profile hiding the eyes, no frontal emperor portrait, no heroic low angle, no throne, no generic palace grandeur, no genuinely warm benevolent sage, no handsome warrior king, no dramatic weapon, no giant jade object, no irregular fantasy jade slab, no object thrust toward camera, no airborne object, no levitating coin, no debris shower, no exploding vessel, no falling fragments, no floating icon pattern, no impossible perspective, no multiple vanishing points, no objects without contact shadows, no repeated cloned officials, no modern round currency, no readable inscriptions or pseudo-writing, no golden ornament storm, no black-and-gold overlay, no Chinese characters, text, logo, watermark, UI or radar chart, no photoreal skin, live-action realism, glossy 3D, smooth generic anime, chibi, idol face, European armor, samurai armor, extra fingers, deformed hands, blood or gore.""",
    "e-han-guangwu": f"""Create one 16:9 Chinese historical action illustration with no text or interface.

SERIES STYLE: adult non-photoreal Chinese historical manga fused with an aged mineral-pigment mural. Use coarse wet plaster and paper grain, rain-dissolved mineral pigment, flaking edges, flying-white ink, dry-brush breaks and strong horizontal storm strokes. Keep the protagonist mature, anatomically believable and visually dominant. Use reference image 1 ({PRIMARY_ANCHOR}) only for mineral-mural material, adult graphic-novel rendering and strong character presence; do not copy its Qin props, frontal pose, map composition or black-and-gold density. Use reference image 2 ({SECONDARY_ANCHOR}) only for expressive ink force. This frame must look wet, cold, muddy and kinetic, completely different from Wang Mang's pale ritual corridor.

HISTORICAL SUBJECT: Liu Xiu, the future Emperor Guangwu, at age 28 or 29 during the Battle of Kunyang, before he became emperor. He is the young restoration commander personally leading a small cavalry wedge against an overwhelmingly larger Xin army. Use the recorded physical traits as the facial anchor: a tall East Asian man, strong handsome eyebrows and beard, a broad mouth, high prominent nose and a clearly raised central upper forehead. Give him an athletic but not bulky build, clear intelligent eyes and calm tactical concentration inside extreme danger. His wet face and beard are streaked with rain and mud. He is not wearing imperial coronation dress and must not look like a generic later emperor.

COSTUME: historically grounded late-Xin or early-Eastern-Han battlefield equipment: dark leather and restrained black-brown lamellar armor over an ochre-brown war robe, all soaked, scratched and caked with wet mud; a dark cloth neck guard, practical leather belt and a simple iron helmet sitting slightly askew, with damp hair visible at the edges. No yellow dragon robe, no imperial crown, no ornate golden armor and no later medieval Chinese armor.

SIGNATURE MOMENT AND NATURAL RIDING POSE: freeze the instant when Liu Xiu's small cavalry wedge finds a narrow break in the giant enemy line during a white lightning flash. He rides a dark chestnut warhorse from left to right in a clean side-on three-quarter view. He sits deep and balanced in the saddle, pelvis aligned with the horse, knees naturally following the horse's body and spine inclined only slightly forward from the hips. His left hand holds wet leather reins low above the horse's withers. His right hand holds a long early-Han spear diagonally forward and upward in the direction of travel, parallel to the charge, never pointed at the camera and never crossing his face. Both shoulders remain anatomically connected and both wrists are natural. His head turns slightly toward the opening so that both eyes and most of his face remain readable.

CAMERA AND COMPOSITION: ground-level tracking camera riding abreast of the charge, approximately 24 mm wide-angle, looking upward about 12 degrees with a subtle 4-degree counterclockwise kinetic tilt. Liu Xiu and the horse's head, neck and front shoulder form the dominant central-left silhouette and occupy about 62 percent of the visual mass. The horse travels across the frame, never directly toward the lens and never rears. A cropped wet horse ear at the extreme lower-left establishes the viewer as a neighboring rider, but it must remain small and out of focus. Keep Liu Xiu's face sharp; motion belongs to rain, mud, flags and the distant battle, not to the face.

EVENT SCALE AND PARTICIPATION: immediately behind Liu Xiu is one visibly small wedge of fewer than twenty low-detail Han riders following the same left-to-right axis. Farther ahead, an enormous dark Xin formation fills the rain beyond the narrow opening near Kunyang's wall, making the numerical imbalance instantly readable without turning background soldiers into individual focal figures. One soaked muted-red banner bends horizontally in the storm. White lightning reveals the breach for a single instant. No meteor, supernatural fireball or divine beam.

PHYSICS AND MOTION: rain, mane, robe edges, banner and mud all travel consistently from upper-left toward lower-right under the same crosswind. Mud leaves the hooves in low backward arcs and falls under gravity; it does not float or form a wall. Horse tack remains attached and taut. All riders, weapons and horses follow one coherent ground plane and motion direction. The foreground and distant formations use consistent scale, overlap and contact with the muddy earth.

COLOR AND SURFACE: storm blue, charcoal black, wet earth brown, iron gray, lightning white and one muted-red banner. G0 gold budget: no gold leaf, no gilding, no golden sparks and no black-and-gold speckle overlay. Use wet pigment runs, dark mud splashes, silver rain scratches and broad cobalt storm fields. The only bright region is the white lightning opening behind the rider's silhouette.

HARD EXCLUSIONS: no crowned emperor, no throne, no palace, no yellow robe, no polished ceremonial armor, no generic fantasy general, no old man, no giant muscular body, no frontal horse charge, no rearing horse, no horse facing camera, no spear aimed at lens, no spear crossing the face, no impossible riding posture, no detached shoulder, no stretched arm, no twisted wrist, no floating mud, no rain frozen as beads everywhere, no extra horse legs, no merged horse-and-rider anatomy, no cloned cavalry, no impossible perspective, no multiple motion directions, no meteor, no magic lightning striking the rider, no readable text, Chinese characters, logo, watermark, UI or radar chart, no photoreal skin, live-action realism, glossy 3D, smooth generic anime, chibi, idol face, European plate armor, samurai armor, blood or gore.""",
    "h-zhao-shi-le": f"""Create one 16:9 Chinese historical action illustration with no text or interface.

SERIES STYLE: adult non-photoreal Chinese historical manga fused with an aged mineral-pigment mural. Use rough rammed-earth plaster, coarse paper grain, scraped mineral color, flaking edges, dry-brush abrasion, flying-white ink and forceful diagonal strokes. Keep the protagonist mature, anatomically believable and visually dominant. Use reference image 1 ({PRIMARY_ANCHOR}) only for mineral-mural material, adult graphic-novel rendering and strong character presence; do not copy its Qin map, seal impact, frontal pose or black-and-gold density. Use reference image 2 ({SECONDARY_ANCHOR}) only for expressive ink force. Use the rejected Shi Le image ({SHI_LE_REJECTED}) only as a reference for his rugged mature facial identity, rough Hu-Han costume material, rammed-earth Xiangguo setting and rust-ochre palette. Do not preserve its low camera, wide-legged flag-bearer pose, giant banner, cheering rally crowd or foreground shackle composition.

HISTORICAL SUBJECT: Shi Le in his mid-to-late forties at Xiangguo in 319, the formerly enslaved northern frontier man who has just founded the Later Zhao regime as King of Zhao. This is a historically grounded reconstruction, not a claim of photographic likeness. Give him deep-set alert eyes, high cheekbones, a prominent nose, a coarse curly moustache and short beard, dark weathered skin, a broad labor-built torso and pale old shackle scars around both wrists. His expression is cold, watchful and self-possessed: a survivor reading the new court above him, not a soldier enjoying applause. He must read as the "slave who became ruler," not as a generic frontier general and not as an exotic caricature.

COSTUME: a rough Hu-Han frontier synthesis appropriate to the Sixteen Kingdoms: dark iron lamellar and plate sections over a coarse charcoal wool-and-linen long robe, restrained rust-red inner layers, a broad worn leather belt, patched edges, dust abrasion and a simple dark leather cap with one narrow iron band. A heavy ring-pommel sword remains fully sheathed at his left hip. His clothing is powerful but still bears the material memory of hardship. No refined southern silk dragon robe, no Ming or Qing court costume, no elaborate bead crown, no bright gold armor and no fantasy fur barbarian costume.

SIGNATURE MOMENT: freeze Shi Le halfway through the final upward stride onto the rough Xiangguo audience platform. The viewer occupies the position of the newly assembled court at the top. Shi Le climbs alone toward the viewer and raises his eyes directly to meet the viewer's gaze at the instant his leading foot takes the last step. The social ascent must be communicated by real height, distance and eyeline, not by him holding a symbolic prop.

NATURAL BODY MECHANICS: his right boot is planted flat and weight-bearing on the final visible stair; his left boot pushes naturally from the stair immediately below. His pelvis, knees and feet all align with the same upward direction. His torso inclines forward only eight degrees from the hips and remains stable. His left hand stabilizes the sheathed sword scabbard at his left hip, with the cuff pulled back just enough to reveal an old wrist scar; his right arm makes a small natural counter-swing with a relaxed open hand close to the body. Both shoulders remain connected, elbows and wrists natural, and neither hand reaches toward the lens. No wide-legged stance, no torso twisting and no ceremonial pose.

CAMERA AND COMPOSITION: high viewpoint from the upper-right edge of the top platform, approximately 35 mm, looking down the staircase at about thirty-eight degrees. The long earthen stair descends diagonally from the near upper-right platform toward the distant lower-left landing. Show Shi Le in a front-left three-quarter view, climbing diagonally upward through the frame toward the viewer. Both eyes and at least seventy percent of his face remain readable. His complete figure occupies about fifty-eight percent of the visual mass; he is large and dominant, not a small figure lost in architecture. Use one strict stair vanishing system, a level camera and no wide-angle stretching. Only the rough lip of the top platform may enter the nearest edge; no foreground person, hand or weapon blocks him.

DISTANT EVIDENCE OF HIS PAST: far behind Shi Le on the lowest landing, small in scale and separated from him by many steps, one old open iron shackle with a short grounded chain rests in dust beside a rough wooden slave-market post. It is background evidence, never a foreground icon. Every link lies flat with contact shadow. Nothing is attached to Shi Le, airborne, breaking, falling or exploding. The long physical distance between the shackle and his present position is the visual story.

EVENT ENVIRONMENT AND PARTICIPATION: Xiangguo is a raw northern power base, not a polished imperial palace: worn rammed-earth stairs, rough timber parapets, leather shields, unfinished towers and wind-cut walls. At the distant lower landing, two irregular banks of former dependents and soldiers have silently parted to leave the stair open. They look upward without raised fists, celebration gestures or cloned faces. At the top-right parapet, a black-and-rust-red Zhao banner is fixed to the architecture rather than held by Shi Le; show only a restrained edge of the cloth. Its long diagonal shadow crosses the steps behind him without covering his face or body. The audience feels that he is climbing into their space and taking power.

COLOR, LIGHT AND SURFACE: rammed-earth ochre, iron rust, charcoal black, coarse linen gray, bone-white dust and restrained dark blood-red. A narrow hard side light from the top platform catches Shi Le's eyes, cheekbone, wrist scar and worn armor edges, while the lower landing remains dusty and subdued. G0 gold budget: absolutely no gold leaf, gilding, golden sparks or black-and-gold speckle overlay. Use scraped earth plates, worn stair edges, iron abrasion, dry dust veils and one diagonal ink-shadow stroke. Dust stays low, sparse and physically directional.

HARD EXCLUSIONS: no flag in Shi Le's hands, no flag-bearer pose, no giant banner covering half the frame, no cheering rally, no raised fists, no victory celebration, no wide-legged stance, no twisted torso, no unstable center of gravity, no seated throne portrait, no coronation ceremony, no generic frontier general, no handsome young prince, no ethnic caricature, no fantasy barbarian, no frontal symmetrical pose, no hidden face, no foreground shackle, no oversized chain, no chain attached to his wrist, no airborne link, no floating prop, no impossible staircase, no mismatched vanishing points, no hovering foot, no stretched limb, no weapon toward the camera, no readable banner glyph, no Chinese characters, text, logo, watermark, UI or radar chart, no photoreal skin, live-action realism, glossy 3D, smooth generic anime, chibi, idol face, Ming or Qing costume, European armor, samurai armor, blood or gore.""",
    "liang-wu": f"""Create one 16:9 Chinese historical action illustration with no text or interface.

USE CASE AND REFERENCE ROLES: historical-scene key art for a fast emperor montage. Use reference image 1 ({PRIMARY_ANCHOR}) only for the adult historical manga anatomy, strong protagonist presence, aged mineral-mural material and forceful large shapes. Do not copy its Qin map, seal impact, frontal pose, warm ochre cast, black-gold density or scattered gold flakes. Use reference image 2 ({SECONDARY_ANCHOR}) only for carbon-ink force and flying-white brush rhythm. Create a completely new camera, palette and event composition.

CORE HISTORICAL IDEA: show Xiao Yan, Emperor Wu of Southern Liang, at age eighty-five during the 549 siege and collapse of Taicheng. He is confined, starving, sick and furious, after decades in which sincere Buddhist devotion and repeated self-dedication at Tongtai Temple became entangled with imperial rule. This is a deliberate symbolic composite: the besieged Taicheng chamber contains the visual memory of his Buddhist obsession, but it is not claiming that the final confinement literally occurred inside Tongtai Temple.

CHARACTER IDENTITY — THE FACE MUST DOMINATE: Xiao Yan is not a generic old monk. Make him unmistakably an aged sovereign: an extremely gaunt narrow face, high exposed cheekbones, a distinctly raised bony crown of the skull beneath sparse disordered white hair, deep-set sharp intelligent eyes, heavy lower eyelids, a long thin nose, hollow temples, a sparse drooping white moustache and a long divided white beard. His body is thin from age and hunger, but his gaze still carries pride, command and offended imperial will. He looks directly at the viewer with exhausted anger and lucid disbelief, not kindness, vacancy or pious serenity. The face is the highest-contrast and most detailed region in the image.

COSTUME AND IDENTITY CONTRADICTION: a faded dead-oxblood Southern Liang imperial robe with dark plum-black borders remains visible at the collar and sleeves. Over one shoulder lies a worn ash-celadon Buddhist kasaya strip, faded almost gray, not yellow and not gold. A narrow imperial sash survives at the waist, but no crown is worn. Sparse white hair is tied badly after confinement. The costume must communicate emperor plus Buddhist devotee plus prisoner at the same time. No luxurious dragon robe, no bright monk robe, no Qing court costume and no generic fantasy sage clothing.

SIGNATURE FREEZE MOMENT AND VIEWER PARTICIPATION: the viewer is the last palace attendant standing at arm's length inside the stripped Taicheng shrine chamber. Freeze the instant after the attendant has handed Xiao Yan a small black-lacquer food bowl and the emperor realizes it is empty. Xiao Yan holds the bowl close to the center of his chest, then lifts his eyes directly into the viewer's eyes. His lips are slightly parted as if a final demand has stopped before becoming words. This single exchange must feel intimate, accusatory and dangerous: the audience is personally confronted by the ruler's hunger and the collapse outside.

NATURAL HANDS AND BOWL PHYSICS: both elbows stay close to his ribs. His left palm supports the bowl from below; the fingers of his right hand rest naturally around the near rim. The small bowl remains horizontal, fully supported by both hands and entirely inside his torso silhouette. Its dark empty interior is visible but it is never thrust toward the lens. Keep both wrists straight, all fingers anatomically distinct, and the bowl smaller than the width of his chest. No reaching pose, no giant hand, no floating bowl, no tilting spill gesture and no prayer gesture.

CAMERA AND COMPOSITION: eye-level 55 mm tight medium shot from the waist upward, at arm's length. Use a front-left three-quarter view with both eyes and at least eighty percent of the face readable. Xiao Yan occupies about seventy percent of the visual mass; his face alone occupies roughly one quarter of the frame height. Place him slightly right of center so the battered Buddhist shrine remains legible behind his left shoulder. No full-body view, no doorway portrait and no high-angle camera. Compress the background with a narrow depth of field while preserving the mural silhouette and siege opening.

BUDDHIST SHRINE AND SIEGE ENVIRONMENT: inside Taicheng, a once-refined private Buddhist shrine has been stripped and damaged by the siege. Behind Xiao Yan's left shoulder, show only a large faded ash-celadon mural fragment: part of a Buddha halo and one lowered stone hand, cracked and flaking, with no bright face and no gold statue. Behind his right shoulder, one narrow broken wooden lattice reveals cold steel-blue smoke, a section of the besieging palisade and three very small armored silhouettes outside. One arrow shaft is embedded firmly in the lattice at a physically correct angle; it is not flying. A nearly extinguished oxblood-red oil lamp rests on a wall shelf. No mountain, open courtyard, money chests or ransom scene.

LIGHTING AND EMOTIONAL CONTRAST: one hard strip of cold steel-blue siege daylight enters through the broken lattice and cuts across Xiao Yan's eyes, cheekbone and empty bowl. The shrine behind him remains deep charcoal and ash-celadon. The dying lamp provides only a tiny dull oxblood accent. The cold light must isolate the emperor's face instead of filling the entire room. Keep smoke and ash sparse; never hide his eyes.

COLOR SYSTEM — DO NOT RETURN TO WARM BROWN: use approximately forty-five percent cold ash-celadon gray, twenty-five percent carbon black, fifteen percent bone white, ten percent dead oxblood red and a narrow steel-blue light accent. G1 gold budget is below one percent: only one sick tarnished trace may remain in the cracked Buddha halo. There is no gold on the emperor, bowl, robe or frame. Absolutely no warm ochre wash, beige monochrome, sepia grading, yellow kasaya, orange temple glow, gold dust, gold speckles or black-and-gold overlay.

MATERIAL AND MARK-MAKING: matte chalky mineral pigment, coarse plaster, visible paper fiber, broad dry-gouache blocks, decisive carbon-ink fractures and a few flying-white brush cuts driven from the siege opening toward the emperor. Use large designed color masses and sharp value separation around the face. Avoid uniform micro-detail, photographic rendering, muddy brown blending, metallic gloss, excessive granular noise and decorative texture pasted equally over every surface.

HARD EXCLUSIONS: no generic benevolent old monk, no ordinary sage portrait, no smiling or tranquil expression, no young emperor, no plump face, no crown, no throne, no praying, no kneeling, no raised hands, no reaching hand, no giant hand, no giant bowl, no foreground tray, no full-body doorway scene, no temple-entry scene, no surrendering crown, no ransom chests, no loose coins, no mounted army inside the room, no giant Buddha statue, no bright golden Buddha, no halo centered behind the emperor's head, no warm brown palette, no ochre-dominant image, no sepia, no pervasive gold, no gold flecks, no floating ash storm, no arrow in flight, no blood or gore, no readable inscriptions, no Chinese characters, text, logo, watermark, UI or radar chart, no photoreal skin, live-action realism, glossy 3D, smooth generic anime, chibi, idol face, Ming or Qing costume, European armor or samurai armor.""",
    "xixia-li-yuanhao": f"""Create one 16:9 Chinese historical action illustration with no text or interface.

USE CASE AND REFERENCE ROLES: historical-scene key art for a fast emperor montage. Use reference image 1 ({PRIMARY_ANCHOR}) only for adult historical manga anatomy, bold protagonist scale, aged mineral-mural material and decisive graphic shapes. Do not copy its Qin map, seal, frontal camera, black robe, ochre field, gold density or scattered gold fragments. Use reference image 2 ({SECONDARY_ANCHOR}) only for directional ink force and flying-white brush rhythm. This image must look radically different from both the previous cold indoor close-up and the rejected red-robed archer: a bone-white Tangut costume, rear three-quarter ascent, hard altar geometry and a face turning back toward the viewer.

CORE HISTORICAL IDEA: show Li Yuanhao at about thirty in a deliberate symbolic composite of his state-building acts: replacing Han-style dress with a self-declared Tangut system, promoting a new Tangut script and ascending the altar as emperor of the Great Xia at Xingqing in 1038. The image does not claim that a Song envoy literally offered these garments at the coronation. It visualizes the documented political break expressed by his own declaration that he had created a new script and changed Han dress. The moment must communicate a ruler deliberately manufacturing a separate state identity, not merely a warrior displaying archery.

CHARACTER IDENTITY — THE FACE AND BODY MUST MATCH THE RECORDED DESCRIPTION: Li Yuanhao is a compact, visibly short Tangut East Asian ruler around thirty, with a broad round face, unusually high prominent nose bridge, narrow hawk-like eyes, heavy straight brows, strong cheek muscles, short black moustache and a small clipped chin beard. His head is slightly large relative to his short powerful frame. The scalp around the felt crown is closely shaven rather than arranged in a Han topknot; only restrained dark side hair remains. His expression combines fierce intelligence, invention and calculated defiance. As he looks back over his shoulder, at least sixty percent of the round face, the entire high nose silhouette and both intense eyes must remain readable. Do not turn him into a tall narrow-faced fantasy prince, Mongol khan, Song official or generic frontier general.

HISTORICALLY SPECIFIC SELF-DECLARED DRESS — THIS IS THE PRIMARY IDENTITY HOOK: he wears the costume recorded after taking power, not his earlier youthful red robe. Use a fitted bone-white narrow-sleeved tunic over dark navy trousers, a broad black leather belt and a compact dark felt crown with a clearly visible carmine-red lining. From the rear crown top hangs one long red knotted cord and tassel, streaming sideways in the wind. The white sleeves fit closely enough to separate this outfit from Song broad-sleeved court dress. A short unstrung bow and compact quiver hang naturally at the rear belt as secondary identity evidence only; he is not shooting. Use tiny weathered turquoise plaques on the belt. No armor, no dragon embroidery, no Song winged hat, no black Qin crown and no dominant red robe on his body.

SIGNATURE FREEZE MOMENT AND VIEWER PARTICIPATION: the viewer is the Song envoy standing at the foot of the rough founding altar. Freeze the instant Li Yuanhao rejects the old identity and takes the first step upward in his new Tangut dress. His body moves away from the viewer, but he snaps his broad round face back over the left shoulder and fixes both hawk eyes directly on the envoy. In the lower-left foreground, the envoy's two hands support a shallow dark tray holding a compact black Han-style crown and one neatly folded broad crimson robe that Li Yuanhao has refused. The protagonist's look says that outside investiture is no longer required. This must feel like the viewer has personally lost political control of the frontier ruler.

BODY, GARMENT AND TRAY PHYSICS — MUST BE CORRECT: Li Yuanhao's leading right boot is planted flat on the first altar step while the left foot pushes from the ground behind. His pelvis and shoulders continue upward, but his neck alone turns far enough to show the face; do not twist the torso unnaturally. His right hand closes naturally around the front of his belt and his left hand hangs relaxed beside the short sheathed bow. Both arms stay close to the body. The red crown cord and narrow white sleeve hems stream in one consistent right-to-left wind. The foreground tray is horizontal and firmly supported by the envoy's two ordinary-sized hands; the folded robe and crown rest on its surface with contact shadows. Nothing floats, falls, breaks or points toward the lens.

CAMERA AND COMPOSITION: chest-height 40 mm medium-wide shot from directly behind and slightly left of the envoy, looking upward only eight degrees. Frame Li Yuanhao from mid-thigh upward in a rear-left three-quarter ascent. He occupies about sixty-five percent of frame height and roughly sixty percent of the visual mass. His compact back and bone-white tunic form one strong central shape; the turned face sits in the upper-left third, unobstructed against deep navy shadow. The tray occupies no more than twelve percent of the lower-left frame. A diagonal altar stair rises from lower right to upper center, creating forward movement without a repeated low-angle hero pose. Keep four clean depth layers: envoy tray, Li Yuanhao, altar officers and wind banners, then Xingqing walls and Helan Mountains.

EVENT ENVIRONMENT AND CULTURAL STATE-BUILDING: the rough white-plastered altar stands inside Xingqing's rammed-earth court with the Helan Mountains forming a hard dark sawtooth in the distance. Two banks of Tangut civil and military officers wait above, small and simplified, wearing sharply differentiated narrow garments rather than cloned Song robes. A scribe at the far altar holds closed blank tablets; beside him stand twelve stacked dark teaching boards whose square block rhythms suggest a newly organized script system without displaying any actual letters or pseudo-writing. One bone-white banner with a nonlinguistic interlocking woven border and one narrow carmine banner snap sideways. No readable script, no giant calligraphy, no palace throne, no battlefield melee and no army panorama.

LIGHTING AND COLOR SYSTEM: hard pale Hexi sunlight comes from high right, carving the high nose, both hawk eyes, shaved temple and red-lined crown into sharp graphic planes. Use approximately fifty percent bone white and pale rammed earth, twenty-five percent deep navy-black shadow, twelve percent charcoal, eight percent carmine red and no more than five percent muted turquoise. The bone-white tunic is the dominant character mass; carmine appears only in the crown lining, long back knot, rejected folded robe and one narrow banner. G1 gold budget is below one percent and may appear only as a worn altar edge. No gold on the ruler, sky, sand or frame. Avoid orange sunset, sepia, yellow desert wash, red-dominant composition, universal black-and-gold grading and decorative gold speckles.

MATERIAL AND MARK-MAKING: adult non-photoreal Chinese historical manga fused with aged mineral-pigment mural painting. Use broad matte chalk-white planes, deep navy mineral shadow, blocky carbon-ink fractures, coarse paper fiber and a few long carmine flying-white strokes driven by the Helan wind. Make the compact white body, dark altar steps and red crown knot three instantly readable graphic shapes. Use restrained square woven rhythms in architecture and belts to echo state construction without becoming writing. Texture follows surface and wind; it is never a universal speckle layer. Keep the face designed, forceful and painterly, never photographic, waxy, glossy or over-smoothed.

HARD EXCLUSIONS: no archery pose, no drawn bow, no red-robed archer, no generic emperor portrait, no throne, no frontal centered coronation, no kneeling, no raised sword, no generic armored warlord, no lamellar armor on Li Yuanhao, no Mongol helmet, no Song winged official hat on Li Yuanhao, no Qin crown, no Qing clothing, no dragon robe, no broad crimson robe on Li Yuanhao, no long tall body, no narrow elongated face, no young idol face, no smiling, no full beard, no Han topknot, no completely bald monk, no exaggerated ethnic caricature, no severed hair, no barber, no scissors, no weapon pointed at the viewer, no giant tray, no floating crown, no falling garments, no twisted torso, no broken wrists, no giant hands, no banner held in his hands, no giant flag covering the face, no readable Tangut glyphs, no pseudo-writing, no Chinese characters, text, logo, watermark, UI or radar chart, no photoreal skin, live-action realism, glossy 3D CGI, smooth generic anime, chibi, European armor, Japanese samurai armor, blood or gore.""",
    "q-qin-fu-jian": f"""Create one 16:9 Chinese historical action illustration with no text or interface.

USE CASE AND REFERENCE ROLES: historical-scene key art for a fast emperor montage. Use reference image 1 ({PRIMARY_ANCHOR}) only for adult historical manga anatomy, dominant protagonist scale, aged mineral-mural material and decisive large shapes. Do not copy its Qin seal, map, frontal camera, black robe, warm ochre field, gold density or scattered gold fragments. Use reference image 2 ({SECONDARY_ANCHOR}) only for liquid ink force and flying-white motion. This image must immediately differ from the previous bone-white mountain altar: cold river blue-gray fills nearly half the frame, the emperor is a dark purple-and-iron figure on the bank, and the visual drama lives in one black whip arc plus a collapsing reflection.

CORE HISTORICAL IDEA: show Fu Jian, ruler of Former Qin, at about forty-five in a deliberate symbolic fusion of two documented 383 moments: his boast during the decision to invade Eastern Jin that the army's whips could stop the river, and the catastrophic defeat at the Fei River that followed. Do not claim the boast was literally spoken at this riverbank. The editorial image freezes the instant supreme confidence first contains its own omen. It must portray the tragedy of an able unifier who trusted scale more than judgment, not a simple foolish villain and not a generic battle commander.

CHARACTER IDENTITY AND EMOTIONAL SPLIT: Fu Jian is a mature northern East Asian ruler of upright medium-tall build, around forty-five, with a broad open forehead, straight heavy brows, deep intelligent almond eyes, a strong nose, firm square jaw, neat medium moustache and a short pointed beard. His reconstructed face should look like a once-open, capable and commanding ruler whose certainty has hardened into stubbornness. Keep the mouth tight with absolute confidence while a very small tension enters the eyes as he notices the water. He is not shouting, laughing or raging. Make his face the sharpest warm-value region against the cold river and keep both eyes readable in front-left three-quarter view.

PERIOD COSTUME — PROUD BUT NOT GOLDEN FANTASY ARMOR: use historically plausible late-fourth-century northern Chinese lamellar armor in oxidized charcoal iron and muted brown-bronze, constructed from many small overlapping plates with real cords and weight. Over it lies a restrained bruised-imperial-purple cloak, heavy and wind-pulled toward the left. Use a compact dark imperial helmet-crown without wings, horns or fantasy ornaments. A straight period sword remains fully sheathed at the left hip. Metal highlights are cold iron-silver, not polished yellow gold. No dragon robe, no giant shoulder armor, no European plate construction and no generic barbarian fur costume.

SIGNATURE FREEZE MOMENT AND VIEWER PARTICIPATION: the viewer is a skeptical front-rank officer standing ankle-deep at the Fei River edge. Fu Jian has dismounted and stepped onto a low dark bank stone directly ahead. Freeze the end of one proud lateral sweep of his riding whip as if demonstrating that the massed army could overwhelm the river. His body faces diagonally left toward the water, but he turns his face toward the viewer-officer with a controlled challenging gaze. The audience must feel personally addressed by the boast while being close enough to see that the river reflection below him has already begun to contradict it.

WHIP, HAND AND BODY PHYSICS — MUST BE CORRECT: Fu Jian grips one short wooden whip handle in his right hand at shoulder height. A single continuous black leather lash curves in a broad sideways arc from upper right toward upper left, remaining above the water and outside the viewer's path. The wrist stays straight, elbow naturally bent and shoulder connected. His left hand rests open near the sheathed sword belt without gripping another prop. The leading boot is planted flat on the bank stone and the rear foot bears weight on compact earth; hips, knees and shoulders share one stable direction. The cloak, beard tips and whip tassel all move in the same right-to-left wind. No thrown whip, no floating handle, no duplicate lash, no giant hand, no extreme torso twist and no rearing horse.

CAMERA AND COMPOSITION: 28 mm waterline-height wide medium shot with a level horizon, looking upward only twelve degrees. Place Fu Jian in the upper-right third, occupying about fifty-eight percent of frame height and roughly fifty-two percent of the visual mass. Cold rippling water fills the lower forty-five percent. His readable face sits close to the center, while the whip arc crosses the upper third without covering it. Two very small soft-focus officer silhouettes crop the extreme lower edges to establish the viewer's place but never compete. Build four clean parallax layers: near ripples, Fu Jian on the bank, the dense but low-detail Qin spear formation, then the misty far bank.

THE REFLECTION IS THE STORY — ONE WORLD, NOT A FANTASY SPLIT SCREEN: above the waterline the real Former Qin ranks remain disciplined, dense and still, a forest of spears behind Fu Jian. Below the waterline, their physically aligned silver reflections begin as straight vertical lines near the bank, then break downstream into widening black-blue zigzags and chaotic brush streaks. Fu Jian has only one distorted reflection; do not create a second emperor. On the far bank, natural reeds, trees and distant birds create an ambiguous pattern that can momentarily resemble enemy ranks, but they remain real landscape elements, never ghosts or supernatural soldiers. The omen is carried by water distortion, value and shape—not literal prophecy, floating weapons or a battle already in progress.

LIGHTING AND COLOR SYSTEM: cold reflected river light rises into Fu Jian's face and lower armor beneath a bruised gray sky. Use approximately forty-five percent cold river blue-gray, twenty-five percent carbon and liquid ink black, fifteen percent muted imperial purple, ten percent oxidized iron silver and five percent dry earthen brown. G1 gold budget is below one percent: at most one worn dull line on a belt fitting, never on the whip, armor, sky or water. The only slightly warm area is the face. No golden hero glow, no ochre-dominant wash, no sepia, no bright red banner and no universal black-and-gold treatment.

MATERIAL AND MARK-MAKING: adult non-photoreal Chinese historical manga fused with an aged mineral-pigment mural. Use broad watery azurite-gray mineral blooms, coarse plaster grain, matte oxidized armor plates, heavy purple mineral cloth, carbon-black ink fractures and downward spear reflections that dissolve into liquid flying-white strokes. Keep the real army above crisp and rhythmically ordered while the reflection below becomes increasingly broken and empty. Texture follows water, metal and cloth separately; never paste one speckle layer over everything. The result must feel painterly, graphic and tragic rather than photographic or cinematic live action.

HARD EXCLUSIONS: no generic mounted emperor, no horse as a major subject, no rearing horse, no throne, no frontal centered hero pose, no triumphant smile, no open-mouth shouting, no cartoon villain, no elderly frail ruler, no young idol face, no massive gold armor, no yellow-gold cloak, no fantasy helmet, no horned crown, no European plate armor, no Japanese samurai armor, no whip thrown into the river, no multiple whips, no floating whips, no literal dam of whips, no lash aimed toward the camera, no broken whip geometry, no giant hand, no raised sword, no battle melee, no corpses, no panic in the real army above the water, no duplicate emperor except one physically distorted reflection, no mirror-perfect reflection, no supernatural ghosts, no phantom soldiers, no readable banner marks, no Chinese characters, text, logo, watermark, UI or radar chart, no photoreal skin, live-action realism, glossy 3D CGI, smooth generic anime, chibi, blood or gore.""",
    "n-wei-xiaowen": f"""Create one 16:9 Chinese historical action illustration with no text or interface.

USE CASE AND REFERENCE ROLES: historical-scene key art for a fast emperor montage. Use reference image 1 ({PRIMARY_ANCHOR}) only for adult historical manga anatomy, dominant protagonist scale, aged mineral-mural material and decisive graphic shapes. Do not copy its Qin map, seal, frontal camera, black robe, warm ochre field, gold density or scattered gold fragments. Use reference image 2 ({SECONDARY_ANCHOR}) only for directional ink force and flying-white cloth motion. This image must be a visual reset after the dark Fei River scene: clear pale architecture, a strict side-tracking stride, one deep restrained cinnabar robe and a sharp gate-shadow threshold.

CORE HISTORICAL IDEA: show Yuan Hong, Emperor Xiaowen of Northern Wei, at about twenty-seven in a deliberate symbolic fusion of the 493 move of the capital to Luoyang and the 494 reform of court language and dress. The image does not claim that he changed clothes while literally crossing this gate. It visualizes his political decision to move an entire ruling culture across a threshold. The moment must communicate active reform, personal conviction and the cost of leaving the old Xianbei order behind—not a passive costume portrait and not a simplistic claim that one culture merely replaced another.

CHARACTER IDENTITY — PALE, REFINED AND RESOLUTE: Yuan Hong is a young Xianbei East Asian ruler around twenty-seven, notably pale-skinned as described in the historical record, with refined high cheekbones, a straight narrow nose, long dark almond eyes, fine but decisive brows, a clear jaw and a slender tall body. His face is elegant but not pretty, fragile, soft or idol-like. Use no heavy beard; at most a faint disciplined moustache shadow. His expression is calm, intellectually severe and final. As he strides rightward, he turns only his eyes and pale face slightly toward the old guard-viewer, making the viewer feel the reform is also a direct command.

COMPLETE REFORMED COURT DRESS — NEVER A SPLIT COSTUME: Yuan Hong wears one fully coherent Northern Wei adaptation of Han-style court clothing: a muted deep-cinnabar crossed-collar robe with broad but weighty sleeves, a pale stone inner collar, a dark indigo lower panel, a broad black belt and a compact simplified black court cap with no long horizontal wings. The tailoring should feel fifth-century and transitional, not Ming, Tang or Song. His hair is completely gathered beneath the court cap in a coherent high arrangement; no visible long Xianbei braid remains on him. The body is never divided into half riding coat and half court robe. No armor, dragon embroidery, imperial yellow, dangling jade curtain or fantasy crown.

SIGNATURE FREEZE MOMENT AND VIEWER PARTICIPATION: the viewer is an elderly Xianbei palace guard standing just inside the Luoyang gate. Freeze the instant Yuan Hong's leading boot crosses the hard gate-shadow line from the cold migration road into the ordered city. His body remains in a clean left-to-right side stride, but his face turns slightly back toward the viewer with quiet expectation: follow, change and enter. Only a very narrow blurred edge of the guard's indigo fur collar and intact old braid enters the extreme right foreground. The emperor is not leaving the audience behind as decoration; he is making the audience decide whether to cross.

NATURAL WALKING AND CLOTH PHYSICS: Yuan Hong's right boot is planted flat just beyond the stone threshold while the left heel lifts naturally behind. Hips, knees, shoulders and head share the same rightward travel. His front arm makes a small natural counter-swing inside the broad sleeve; the rear hand gathers no object and remains relaxed near the belt. The heavy cinnabar sleeve and lower robe trail leftward with gravity and one consistent gate wind, never floating like flags. Keep both hands ordinary-sized and mostly contained within the sleeves. No reaching, pointing, ceremonial presentation or impossible twisting.

OLD ORDER AS GROUNDED BACKGROUND EVIDENCE: behind Yuan Hong on the cold outer road, one old Xianbei narrow-sleeved indigo riding coat is tightly rolled and physically strapped to the side of a southbound pack cart. A dark braid cord is wrapped around that rolled coat as a practical tie; it lies against the fabric with contact shadow. Nothing is held up for display, severed, flying or thrown away. A few migration carts and mounted escorts move toward the gate in a long shallow diagonal, small and low-detail. This evidence must remain secondary to the emperor's face and stride.

CAMERA AND COMPOSITION: waist-height 45 mm side-tracking shot parallel to the threshold, with a level architectural frame and no heroic low angle. Show Yuan Hong from boots to crown in clean left-facing-to-right motion, occupying about sixty-seven percent of frame height and fifty-eight percent of the visual mass. Place his pale turned face near the upper-center and keep it unobstructed against deep indigo gate shadow. A single vertical gate-shadow band divides the frame near the left third, while the road and new Luoyang avenue continue horizontally through it. Build four parallax layers: the narrow old-guard edge, Yuan Hong, the migrating cart line, then pale Luoyang towers and distant road.

ENVIRONMENT AND CULTURAL TRANSITION: the outer left side of the Luoyang gate carries cold blue-brown migration dust, rough timber, horse tack and the last muted northern wind. The inner right side opens into newly ordered pale-stone avenues, low early-medieval tiled towers, measured colonnades and a few restrained celadon ritual banners with no writing. Do not create a magical before-and-after split screen; this is one continuous physical gate and one consistent daylight. Use architecture, clothing and movement to show transition. No Dragon Gate grottoes as a personal portrait, no giant palace, no cheering crowd and no modern boulevard.

LIGHTING AND COLOR SYSTEM: clear soft daylight enters from inside Luoyang and catches Yuan Hong's pale face, inner collar and front sleeve, while the old guard and migration road remain in cool indigo shadow. Use approximately forty percent pale Luoyang stone, twenty-five percent deep indigo, fifteen percent muted celadon, fifteen percent restrained deep cinnabar and five percent charcoal black. G0 gold budget: absolutely no gold leaf, gilded sparks, golden costume trim or black-and-gold speckle overlay. The pale face and cinnabar robe must separate cleanly without glowing. Avoid sepia, orange sunset, imperial yellow and pervasive red.

MATERIAL AND MARK-MAKING: adult non-photoreal Chinese historical manga fused with aged mineral-pigment mural painting. Use broad pale plaster planes, matte cinnabar mineral cloth, deep indigo gate shadow, soft celadon dust, coarse paper fiber, straight architectural cracks and long horizontal flying-white strokes carried by the migration road. The hard threshold line, the flowing robe and the departing carts form three distinct graphic rhythms. Texture follows stone, cloth and dust separately; never paste uniform flecks over the entire frame. Keep the face elegant, graphic and painterly rather than photographic, glossy or over-smoothed.

HARD EXCLUSIONS: no static city-tower portrait, no standing-and-holding-braid pose, no rear-three-quarter altar ascent, no repeated tray, no frontal centered emperor, no throne, no ceremonial hand aimed at the viewer, no split old-and-new costume on the body, no half-Xianbei half-Han robe, no flying coat, no floating braid cord, no severed hair, no barber, no scissors, no discarded garments in midair, no kneeling guard, no generic migration crowd, no armor on Yuan Hong, no dragon robe, no imperial yellow, no Ming winged hat, no tall Qin crown, no Tang imperial cap, no Qing clothing, no heavy beard, no idol face, no ghostly cultural transformation, no magical color division, no readable banners, no Chinese characters, text, logo, watermark, UI or radar chart, no photoreal skin, live-action realism, glossy 3D CGI, smooth generic anime, chibi, European armor, Japanese samurai armor, blood or gore.""",
    "sui-wen": f"""Create one 16:9 Chinese historical action illustration with no text or interface.

USE CASE AND REFERENCE ROLES: historical-scene key art for a fast emperor montage. Use reference image 1 ({PRIMARY_ANCHOR}) only for adult historical manga anatomy, dominant protagonist scale, aged mineral-mural material and decisive graphic shapes. Do not copy its Qin map, seal, desk impact, frontal symmetry, black-and-gold density or scattered gold fragments. Use reference image 2 ({SECONDARY_ANCHOR}) only for directional ink force, dry-brush architecture and flying-white motion. This image must not resemble the preceding Luoyang walking scene: change to a cold ground-level construction viewpoint, a crouched middle-aged ruler, chalk stone and oxidized teal, with one severe straight cinnabar survey line and absolutely no gold.

CORE HISTORICAL IDEA: show Yang Jian, Emperor Wen and founder of Sui, around age fifty in a deliberate symbolic fusion of the construction of Daxing in 583, the mature Kaihuang institutional order and the reunification of north and south in 589. The image does not claim that Yang Jian personally snapped a survey line at this exact ceremony. It visualizes his defining character as an austere system-builder who forces city, administration and reunited territory onto one measured axis. Make him active inside the work, not a portrait standing in front of a blueprint and not a general posing after victory.

CHARACTER IDENTITY — AUSTERE, HEAVY AND PENETRATING: Yang Jian is a mature East Asian ruler around fifty with a long upper body and comparatively compact lower body, broad shoulders, a heavy square authoritative face, a strongly modeled forehead with five subtle vertical bony ridges rising toward the crown, thick level brows, piercing outward-looking eyes, a high broad nose, compressed lips, a controlled short moustache and a compact pointed chin beard. The forehead ridges are anatomical planes under skin, never horns, scars or supernatural marks. His gaze tracks the new capital's central axis just past the viewer with exacting suspicion and concentration. He is severe and disciplined, not furious, theatrical, benevolent-smiling or elderly-frail.

FRUGAL SUI COURT DRESS: give him a historically grounded early-Sui tongtian crown in matte black lacquer, tall but proportionate, without bead curtains, horizontal Ming wings or fantasy spikes. He wears a plain dark slate-black crossed-collar imperial robe with restrained deep-maroon inner edging, broad weighty sleeves, a substantial dark sash and a large muted seal pouch or ribbon assembly at the waist. Ornament is minimal and dull. No dragon robe, imperial yellow, jeweled spectacle, bright gold embroidery, armor, general's helmet or luxurious throne imagery. His clothing must visibly express the contrast between imperial authority and personal frugality.

SIGNATURE FREEZE MOMENT AND VIEWER PARTICIPATION: the viewer is a Daxing construction surveyor standing inside a shallow foundation trench. Yang Jian crouches on the trench edge above and slightly beyond the viewer, one knee firmly bent and the other foot planted, personally checking the imperial central axis. Freeze the instant just after he releases the middle of one pigment-coated survey cord: the cord rebounds against a long pale foundation stone and leaves one perfectly straight muted-cinnabar line. Yang Jian's eyes continue along that line beyond the viewer, making the audience feel personally responsible for whether the new order is straight. The action is precise, quiet and irreversible rather than heroic spectacle.

CORD, HAND AND BODY PHYSICS — MUST BE COHERENT: use exactly one thin survey cord, anchored to exactly two ordinary wooden pegs that are both visibly fixed into the stone bed at opposite sides of the frame. The cord forms one taut, nearly horizontal straight line between them, with only a very small central rebound vibration above the new pigment mark. It is not a whip, ribbon, weapon, glowing laser or floating calligraphy stroke. Yang Jian's near hand has just released the cord and remains naturally open two or three centimeters above it; his far hand rests flat and weight-bearing on his raised knee. Show five normal fingers on each visible hand, correct wrist direction and believable contact shadows. His crouch has one planted foot, one bent knee, level hips and balanced weight. No impossible twist, giant hand, broken rope, extra cord, loose loop, floating peg or ruler driven toward the camera.

CAMERA AND COMPOSITION: use a ground-level 42 mm medium-close environmental shot from inside the trench, looking upward only about twelve degrees. This is not a monumental low-angle hero shot; the trench position creates participation, while Yang Jian remains human-scale and physically close. Show the complete tongtian crown, face, long torso, both hands, one raised knee and enough of the planted lower leg to make the posture readable. He occupies roughly sixty-four percent of frame height and fifty-eight percent of visual mass, set slightly left of center. His face sits in the upper-left central zone against a clean cold slate wall. Keep the frame level. The taut cord and fresh cinnabar line form the dominant horizontal axis across the lower middle, then align with the new avenue beyond. Build four separable parallax layers: rough trench lip and fixed pegs, Yang Jian, ordered construction works, then the distant river-gate horizon.

ENVIRONMENT — DAXING ORDER BECOMES REUNIFIED ORDER: behind Yang Jian, the foundation trench opens into the early construction of Daxing: rammed-earth ward walls, pale stone bases, measured timber frames, survey stakes, straight drainage channels and labor teams reduced to small low-detail silhouettes. Do not show a completed Tang Chang'an skyline. The new central avenue continues in rigorous one-point perspective toward a distant river gate. Beyond that gate, use only a narrow symbolic glimpse of oxidized-teal water, several tiny southern campaign vessel masts and one small muted southern standard being lowered by gravity. The standard has no writing or emblem and does not dominate. Stone grooves, drainage lines, river wake and the lowered standard all converge on the same physical axis; there is no floating map, hologram, tabletop miniature or magical city grid.

LIGHTING AND COLOR SYSTEM: clear cold construction-morning light from the distant gate grazes Yang Jian's forehead planes, eyes, near cheek, plain sleeve and chalk foundation stone. Soft oxidized-teal river reflection rises into the trench shadow. Use approximately thirty-five percent cold slate blue-gray, twenty-five percent chalk and pale stone, eighteen percent earthen clay and rammed-earth brown, twelve percent oxidized river teal, eight percent charcoal-black robe and no more than two percent muted cinnabar confined to the one survey mark and a very thin inner collar edge. G0 gold budget: absolutely no gold leaf, gilded trim, metallic gold flecks, yellow-gold glow or black-and-gold speckle overlay. Avoid the preceding image's large red robe, warm pale city field and gate-shadow split; avoid the following image's wine-red lantern mood.

MATERIAL AND MARK-MAKING: adult non-photoreal Chinese historical manga fused with an aged mineral-pigment mural. Use chalky cracked stone, compressed rammed-earth strata, coarse paper fibers, matte carbon-black cloth, granular azurite-gray and oxidized teal washes, strict dry-brush architectural vanishing lines and a single dense cinnabar cord snap. Make the straight axis cut through irregular handmade texture. Let wall cracks and flying-white strokes run toward the distant gate rather than scatter decoratively. Texture follows skin, cloth, stone, soil, cord and water separately; never paste uniform grit or gold flecks across everything. The face must remain graphic, mature and painterly, not photographic, waxy, glossy or softly beautified.

HARD EXCLUSIONS: no map table, no planning desk, no seal strike, no emperor pointing at a map, no standing portrait before a city, no completed grand palace, no generic founder throne pose, no centered frontal symmetry, no towering heroic skyline angle, no sword, no battle armor, no battlefield command pose, no giant fleet, no cheering crowd, no floating city diagram, no glowing grid, no magical transport lines, no repeated Qin composition, no repeated Luoyang walking composition, no dominant red robe, no yellow or gold costume, no gold leaf or gold dust, no whip-like cord, no coiled rope, no multiple cords, no broken cord, no floating peg, no giant foreground tool, no hands aimed at the lens, no horns or scars on the forehead, no fantasy crown, no bead-curtain mian crown, no Ming winged hat, no Tang or Song official cap, no Qing clothing, no idol face, no smiling benevolent sage, no elderly frail man, no readable banner marks, no Chinese characters, text, pseudo-writing, logo, watermark, UI or radar chart, no photoreal skin, live-action cinematic realism, glossy 3D CGI, smooth generic anime, chibi, European armor, Japanese samurai armor, blood or gore.""",
}


def split_old_prompt(prompt: str) -> tuple[str, str, str]:
    """Return identity block, background block and old accent direction."""
    identity, rest = prompt.split("POSE:", 1)
    _old_pose, rest = rest.split("BACKGROUND SET:", 1)
    background, old_style = rest.split("ART DIRECTION:", 1)
    return identity.strip().rstrip(","), background.strip().rstrip(","), old_style.strip().rstrip(",")


def build_prompt(pid: str, sc: dict) -> str:
    if pid in DIRECT_PROMPT_OVERRIDES:
        return DIRECT_PROMPT_OVERRIDES[pid].strip() + "\n"
    beat = MOMENTS[pid]
    shot = SHOT_PLANS[pid]
    palette = PALETTE_PLANS[pid]
    identity, background, old_style = split_old_prompt(sc["prompt"])
    identity = IDENTITY_OVERRIDES.get(pid, identity)
    pose_section = (
        f"\nPOSE AND ANATOMY — LOCKED:\n{shot['pose']}.\n"
        if shot.get("pose")
        else ""
    )
    specific_avoid = CHARACTER_AVOID.get(pid)
    avoid = f"{FIXED_AVOID}, {specific_avoid}" if specific_avoid else FIXED_AVOID
    return f"""Use case: historical-scene
Asset type: 16:9 emperor montage key art
Reference image 1: {PRIMARY_ANCHOR} — primary series anchor for mineral mural material, adult manga rendering, character dominance and event participation only. Do not copy its camera composition, gold density or Qin-specific props.
Reference image 2: {SECONDARY_ANCHOR} — secondary anchor only for ink force, flying-white brush texture and motion flow.

{FIXED_VISUAL_GRAMMAR}

SUBJECT IDENTITY AND PERIOD CONSTRUCTION:
{identity}.

SIGNATURE FREEZE MOMENT:
Freeze the scene as {beat['moment']}.

CAMERA PLAN — LOCKED FOR THIS EMPEROR, DO NOT REVERT TO A GENERIC FRONTAL HERO SHOT:
- Shot code: {shot['code']}
- Elevation and pitch: {shot['elevation']}.
- Subject azimuth and orientation: {shot['azimuth']}.
- Shot scale and lens behavior: {shot['scale']}.
- Camera roll: {shot['roll']}.
{pose_section}

AUDIENCE PARTICIPATION MODE:
{shot['interaction']}.

EVENT MOTION THROUGH THE FRAME:
{shot['motion']}.

EXTREME FOREGROUND DESIGN:
{shot['foreground']}.

COLOR AND GOLD BUDGET — LOCKED FOR THIS EMPEROR:
- Color code: {palette['code']}
- Dominant palette: {palette['dominant']}.
- Gold allocation: {palette['gold']}.
- Lighting logic: {palette['light']}.
- Surface rhythm: {palette['surface']}.

HISTORICAL EVENT ENVIRONMENT:
{background}.

CHARACTER-SPECIFIC ACCENT:
Use only the emotional implication of "{old_style}" as a secondary accent. Its old palette wording is subordinate to the locked COLOR AND GOLD BUDGET and must not replace the mineral-mural and expressive-ink medium.

COMPOSITION AND DELIVERY:
Follow the assigned camera and color plans literally before adding detail. One clearly dominant emperor, with contextual people only as cropped foreground framing, edge silhouettes or distant low-detail figures. Keep the face readable without forcing it frontal. Build at least four separable depth layers for parallax: assigned foreground frame, emperor, event action, distant environment. Preserve some lower-left and upper-right low-detail areas when possible, but never weaken the action merely to create empty overlay boxes. No text is generated inside the image. Before rendering, compare this shot and color code with the adjacent prompt files: at least two camera dimensions must visibly differ, and the dominant hue or gold density must also change. Do not reuse the approved images' black-gold speckle distribution as a series-wide overlay.

AVOID:
{avoid}.
"""


def prompt_file_text(pid: str, sc: dict, profile: dict) -> str:
    order = sc["order"]
    shot = SHOT_PLANS[pid]
    palette = PALETTE_PLANS[pid]
    output = OUTPUTS / f"{order:02d}-{pid}.png"
    status = "APPROVED — DO NOT REGENERATE" if pid in APPROVED_IDS else "PENDING GENERATION"
    return f"""PROMPT_VERSION: 2.3-camera-palette-identity-physics
ID: {pid}
ORDER: {order:02d}
PERSONAL_NAME_ZH: {profile.get('personal') or profile.get('display')}
DISPLAY_ZH: {profile.get('display')}
STATUS: {status}
SHOT_CODE: {shot['code']}
COLOR_CODE: {palette['code']}
OUTPUT_PATH: {output}
PRIMARY_STYLE_ANCHOR: {PRIMARY_ANCHOR}
SECONDARY_MOTION_ANCHOR: {SECONDARY_ANCHOR}

=== POSITIVE PROMPT (copy verbatim) ===

{build_prompt(pid, sc)}

=== SAVE CONTRACT ===

Save one final PNG exactly to:
{output}

Do not save the final image anywhere else. Do not overwrite an existing output. Generate at 16:9, visually compare against both anchors, and complete the thirteen-point QA in MASTER-VISUAL-GRAMMAR.md before moving to the next emperor.
"""


def master_doc() -> str:
    return f"""# 固定视觉语法与母提示词

版本：`v2.3 camera-palette-identity-physics`  
风格名：**岩彩裂壁 · 墨势入场**

## 两张权威锚点

- 主锚点：`{PRIMARY_ANCHOR}`
- 辅助墨势锚点：`{SECONDARY_ANCHOR}`

主锚点只控制材质、人物主导性、成年漫画造型和事件参与原则，**不控制具体机位**；辅助锚点只控制泼墨、飞白和运动方向。其他帝王不得复制秦始皇的构图、帝印、地图、权量或车辙。

## v2.3 的核心边界

统一的是 **岩彩材质、裂壁肌理、墨势笔触、成年历史漫画造型**；不统一机位、人物姿态和整幅配色。每个人必须同时执行自己提示词内的 `CAMERA PLAN` 与 `COLOR AND GOLD BUDGET`。金色不是系列滤镜，只能按个人额度出现在有意义的位置。参与感可以来自遮挡、共同移动、空间威胁、旁观压力或视线关系，禁止把它自动翻译成“人物正面伸手抓向镜头”。

## 锁定母提示词

```text
{FIXED_VISUAL_GRAMMAR}
```

## 固定禁项

```text
{FIXED_AVOID}
```

## 十三项硬验收

1. 人物是否仍是最大单一视觉主体，脸部是否清楚可读？
2. 不看标题，能否从动作和道具认出此人，而不只是“某位皇帝”？
3. 观众能否说出自己在事件中站在哪里？
4. 参与方式是否符合本人 `AUDIENCE PARTICIPATION MODE`，而不是默认伸手或道具冲镜头？
5. 是否定格在动作尚未完成的一瞬？
6. 岩彩、裂壁和墨势是否参与动作，而不是表面滤镜？
7. 是否无真人写实、平滑 3D、通用龙椅、可读文字和伪字？
8. 是否能拆成前景冲击、人物、事件、远景至少四层？
9. 俯仰、人物朝向、景别、镜头滚转、运动轴及专属姿势是否执行了本人的 `SHOT_CODE` 与 `POSE AND ANATOMY`？
10. 与前后相邻图片相比，上述五个维度是否至少有两个发生肉眼可见的改变？
11. 是否执行本人的 `COLOR_CODE` 与金色额度，且金色只落在被指定的叙事物件上？
12. 与前后相邻图片相比，主色温或金色密度是否明显改变，并且没有套用统一黑金飞溅层？
13. 所有器物、影子和环境线条是否服从同一透视与光源；贴地物是否有接触阴影，未指定的物体是否绝不悬空？

任一项为“否”，不得保存为正式输出。
"""


def camera_matrix_doc() -> str:
    rows = [
        "# 二十帝王镜头矩阵",
        "",
        "版本：`v2.3 camera-palette-identity-physics`。此表锁定镜头差异，不锁定秦始皇构图。生成每张图前先读本行，并与前后两行比较。",
        "",
        "| # | ID | Shot code | Elevation | Azimuth | Scale | Interaction | Motion axis |",
        "|---:|---|---|---|---|---|---|---|",
    ]
    for pid, sc in sorted(SCENES.items(), key=lambda item: item[1]["order"]):
        shot = SHOT_PLANS[pid]
        rows.append(
            f"| {sc['order']:02d} | `{pid}` | `{shot['code']}` | {shot['elevation']} | "
            f"{shot['azimuth']} | {shot['scale']} | {shot['interaction']} | {shot['motion']} |"
        )
    rows.extend(
        [
            "",
            "## 反同质化硬规则",
            "",
            "- 不得连续两张都使用正面或近正面人物。",
            "- 不得连续两张都使用低机位、桌沿机位或手持道具冲镜头。",
            "- 相邻两张至少改变俯仰、方位、景别、滚转、运动轴中的两项。",
            "- 若生成器自动回到居中正面英雄照，判定为未执行提示词，直接退稿。",
        ]
    )
    return "\n".join(rows) + "\n"


def palette_matrix_doc() -> str:
    rows = [
        "# 二十帝王色彩与金色额度矩阵",
        "",
        "版本：`v2.3 camera-palette-identity-physics`。岩彩媒介保持统一，但主色、光线、表面节奏和金色密度按人物分配。01–16 已批准，不作为后续模板。",
        "",
        "| # | ID | Color code | Dominant palette | Gold budget | Lighting | Surface rhythm |",
        "|---:|---|---|---|---|---|---|",
    ]
    for pid, sc in sorted(SCENES.items(), key=lambda item: item[1]["order"]):
        palette = PALETTE_PLANS[pid]
        rows.append(
            f"| {sc['order']:02d} | `{pid}` | `{palette['code']}` | {palette['dominant']} | "
            f"{palette['gold']} | {palette['light']} | {palette['surface']} |"
        )
    rows.extend(
        [
            "",
            "## 反黑金同质化硬规则",
            "",
            "- 03 以后禁止把金色颗粒均匀撒满全画面；金色必须落在指定物件或结构上。",
            "- `G0` 不使用金箔；`G1` 为局部微量；`G2`、`G3` 只保留给明确指定的少数画面。",
            "- 相邻两张必须改变主色温或金色密度，最好同时改变表面纹理节奏。",
            "- 如果去掉人物后仍像同一张黑金底图换道具，判定为同质化退稿。",
        ]
    )
    return "\n".join(rows) + "\n"


def readme() -> str:
    return f"""# video-01 帝王插画固定生产包

当前版本：`v2.3 camera-palette-identity-physics`。旧版提示词已经废止，不得从聊天缓存或旧复制文本继续生成。先读 `MASTER-VISUAL-GRAMMAR.md`、`CAMERA-MATRIX.md` 和 `PALETTE-MATRIX.md`，再按 `prompts/` 的编号逐张生成。

## 唯一输出目录

```text
{OUTPUTS}
```

所有最终 PNG 必须直接保存在这个文件夹，不得另建日期目录、临时成品目录或放回工具默认目录。

## 生产顺序

1. `01-qin-shi-huang.png` 至 `16-zhou-shi.png` 已批准，**禁止重生成或覆盖**。
2. 从 `prompts/17-n-tang-houzhu.txt` 开始，一次只处理一张；旧版退稿保存在 `rejected/` 的对应原因目录中。
3. 每次必须重新打开单人提示词，确认顶部是 `PROMPT_VERSION: 2.3-camera-palette-identity-physics`，再复制 `POSITIVE PROMPT`。
4. 同时加载主锚点和辅助锚点；只继承材质、笔触和成年漫画造型，不复制秦始皇机位或黑金密度。
5. 生成前同时核对 `SHOT_CODE`、`COLOR_CODE` 及两张矩阵的相邻行；生成 16:9 PNG。
6. 按十三项硬验收检查；若回到正面低机位伸手构图、统一金粉层，或器物不服从重力与单一透视，直接判退。
7. 通过后按 `OUTPUT_PATH` 精确保存，再进入下一人。

## 文件命名

固定格式：`NN-id.png`，例如：

- `01-qin-shi-huang.png`
- `02-han-xuan-di.png`
- `17-n-tang-houzhu.png`

不得在正式输出中使用 `final-final`、日期、随机串或中文文件名。

## 边界

- 统一的是岩彩、裂壁、墨势和成年漫画造型，不是秦始皇的道具、构图或黑金比例。
- 不生成名字、代表事、雷达图或任何 UI；全部后期叠加。
- 不覆盖已有文件。若某编号已存在，先停止并报告。
- 不修改 `prompts/`、Style Bible、史料文件或网页数据。
"""


def main() -> None:
    if not PRIMARY_ANCHOR.exists() or not SECONDARY_ANCHOR.exists():
        raise SystemExit("Missing approved style anchors")
    if not SHI_LE_REJECTED.exists():
        raise SystemExit(f"Missing Shi Le identity reference: {SHI_LE_REJECTED}")
    if set(MOMENTS) != set(SCENES):
        missing = sorted(set(SCENES) - set(MOMENTS))
        extra = sorted(set(MOMENTS) - set(SCENES))
        raise SystemExit(f"Moment mapping mismatch; missing={missing}, extra={extra}")
    if set(SHOT_PLANS) != set(SCENES):
        missing = sorted(set(SCENES) - set(SHOT_PLANS))
        extra = sorted(set(SHOT_PLANS) - set(SCENES))
        raise SystemExit(f"Shot-plan mapping mismatch; missing={missing}, extra={extra}")
    if set(PALETTE_PLANS) != set(SCENES):
        missing = sorted(set(SCENES) - set(PALETTE_PLANS))
        extra = sorted(set(PALETTE_PLANS) - set(SCENES))
        raise SystemExit(f"Palette-plan mapping mismatch; missing={missing}, extra={extra}")
    ordered_ids = [
        pid for pid, _sc in sorted(SCENES.items(), key=lambda item: item[1]["order"])
    ]
    camera_dimensions = ("elevation", "azimuth", "scale", "roll", "motion")
    for previous, current in zip(ordered_ids, ordered_ids[1:]):
        differences = sum(
            SHOT_PLANS[previous][key] != SHOT_PLANS[current][key]
            for key in camera_dimensions
        )
        if differences < 2:
            raise SystemExit(
                f"Adjacent shot plans are too similar: {previous} -> {current}"
            )
    palette_dimensions = ("dominant", "gold", "light", "surface")
    for previous, current in zip(ordered_ids, ordered_ids[1:]):
        differences = sum(
            PALETTE_PLANS[previous][key] != PALETTE_PLANS[current][key]
            for key in palette_dimensions
        )
        if differences < 2:
            raise SystemExit(
                f"Adjacent palette plans are too similar: {previous} -> {current}"
            )

    data = json.loads(VIDEO20.read_text(encoding="utf-8"))
    profiles = {p["id"]: p for p in data["profiles"]}
    PROMPTS.mkdir(parents=True, exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    if not QIN_OUTPUT.exists():
        shutil.copy2(PRIMARY_ANCHOR, QIN_OUTPUT)
    for pid in APPROVED_IDS:
        sc = SCENES[pid]
        approved_output = OUTPUTS / f"{sc['order']:02d}-{pid}.png"
        if not approved_output.exists():
            raise SystemExit(f"Approved output is missing: {approved_output}")

    manifest = {
        "version": "2.3-camera-palette-identity-physics",
        "style": "岩彩裂壁 · 墨势入场",
        "package_root": str(PACKAGE),
        "output_directory": str(OUTPUTS),
        "primary_anchor": str(PRIMARY_ANCHOR),
        "secondary_anchor": str(SECONDARY_ANCHOR),
        "items": [],
    }

    combined = ["# video-01 emperor illustration prompts — v2.3 camera, palette, identity and grounded physics", ""]
    for pid, sc in sorted(SCENES.items(), key=lambda item: item[1]["order"]):
        profile = profiles[pid]
        order = sc["order"]
        filename = f"{order:02d}-{pid}.txt"
        output_name = f"{order:02d}-{pid}.png"
        text = prompt_file_text(pid, sc, profile)
        (PROMPTS / filename).write_text(text, encoding="utf-8")
        combined.extend([f"## {order:02d} {pid}", "", text, "", "---", ""])
        manifest["items"].append(
            {
                "order": order,
                "id": pid,
                "personal": profile.get("personal") or profile.get("display"),
                "display": profile.get("display"),
                "prompt": str(PROMPTS / filename),
                "output": str(OUTPUTS / output_name),
                "shot_code": SHOT_PLANS[pid]["code"],
                "shot_plan": SHOT_PLANS[pid],
                "color_code": PALETTE_PLANS[pid]["code"],
                "palette_plan": PALETTE_PLANS[pid],
                "status": "approved" if pid in APPROVED_IDS else "pending",
            }
        )

    (PACKAGE / "README.md").write_text(readme(), encoding="utf-8")
    (PACKAGE / "MASTER-VISUAL-GRAMMAR.md").write_text(master_doc(), encoding="utf-8")
    (PACKAGE / "CAMERA-MATRIX.md").write_text(camera_matrix_doc(), encoding="utf-8")
    (PACKAGE / "PALETTE-MATRIX.md").write_text(palette_matrix_doc(), encoding="utf-8")
    (PACKAGE / "ALL-20-PROMPTS.md").write_text("\n".join(combined), encoding="utf-8")
    (PACKAGE / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"package={PACKAGE}")
    print(f"prompts={len(manifest['items'])}")
    print(f"output={OUTPUTS}")


if __name__ == "__main__":
    main()
