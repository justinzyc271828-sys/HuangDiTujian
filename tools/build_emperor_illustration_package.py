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
}


FIXED_VISUAL_GRAMMAR = """LOCKED SERIES RENDERING GRAMMAR — lock the medium, mark-making and adult character design; do not lock the camera, palette distribution or Qin-specific objects:
an adult non-photoreal Chinese historical manga illustration fused with a mineral-pigment mural and forceful expressive ink motion; aged plaster and coarse paper; visibly granular mineral pigments selected from a character-specific palette; cracked wall, flaking pigment, dry-brush edges, flying-white ink and directional brush force; fragmented distressed gold leaf appears only when the per-emperor palette plan assigns it and must never become a universal gold-splatter overlay. Use no more than the assigned gold budget. Bold designed silhouette, decisive facial planes, expressive anatomy and controlled exaggeration. The emperor must remain the unmistakable visual subject and normally occupy 48–72 percent of the visual mass, but profile, rear three-quarter, overhead, ground-level, over-the-shoulder and off-center arrangements are all valid when assigned by the per-emperor camera plan. The viewer has a precise position inside the historical event. Participation may come from proximity, occlusion, eyeline, danger crossing the frame, shared movement or spatial pressure; it does not require a hand or prop aimed at the lens. Freeze the scene before the action finishes. Make the cracks, pigment and ink carry the event's direction and force rather than act as a decorative filter. The CAMERA PLAN and COLOR PLAN below are authoritative and must visibly differ from adjacent images."""

FIXED_AVOID = """static atlas portrait, museum-display pose, repeated centered frontal emperor, repeated low-angle hero shot, repeated table-edge composition, automatic hand-or-prop thrust at the camera unless explicitly assigned, universal black-and-gold treatment, gold dust scattered uniformly over the entire frame, excessive gold leaf above the assigned budget, generic dragon, generic throne, generic palace grandeur used as identity, photoreal skin, live-action cinematic realism, glossy 3D CGI, smooth generic AI-anime polish, cute or chibi styling, idol face, plastic costume, modern objects, European armor, Japanese samurai armor, readable text, letters, Chinese characters, pseudo-writing, logo, watermark, interface, radar chart, infographic, multiple competing focal characters, cropped crown, deformed hands, extra fingers, blood or gore"""


MOMENTS = {
    "qin-shi-huang": {
        "moment": "the imperial seal has just struck the six-state map and the old borders are cracking inward before the impact completes",
    },
    "han-xuan-di": {
        "moment": "he has just pulled one falsified bamboo dossier from a mountain of memorials and is about to expose the official responsible",
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
        "moment": "he removes the final imperial object before offering himself to Tongtai Temple while distant military danger first appears through the gate",
    },
    "xixia-li-yuanhao": {
        "moment": "the new ruler of Hexi releases a signal arrow from the Xingqing rampart as the Helan wind catches every banner",
    },
    "q-qin-fu-jian": {
        "moment": "his raised whip begins the boast that the army could dam the river, one instant before the water image turns ominous",
    },
    "n-wei-xiaowen": {
        "moment": "he completes the public break with the old court dress during the move to Luoyang",
    },
    "sui-wen": {
        "moment": "the final southern banner falls onto the Daxing city grid and the unified transport lines lock together",
    },
    "sui-yang": {
        "moment": "on the Jiangdu dragon boat, the exhausted ruler turns at the first flash of a nearby blade while wine spills and the canal still glows outside",
    },
    "tang-tai-zong": {
        "moment": "the warrior-emperor sets aside martial pride and takes a sharply worded remonstrance before the court can fall silent",
    },
    "zhou-wu-zetian": {
        "moment": "the elderly sovereign extends the first decree of her new imperial order as the golden wheel turns behind the crown beads",
    },
    "tang-xian-zong": {
        "moment": "a snowy-night messenger arrives as his finger drives the decisive Caizhou marker into the rebel map",
    },
    "zhou-shi": {
        "moment": "at Gaoping he physically turns the first fleeing guard back toward the battle before the formation recovers",
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
        "code": "S02-BIRDSEYE-LEFT3Q-MS-LATERAL",
        "elevation": "strong 50-degree bird's-eye view from above the archive shelves",
        "azimuth": "the emperor sits in the upper-left of frame in left three-quarter orientation and looks diagonally across the desk, never frontally down the lens",
        "scale": "35 mm medium shot with a broad diagonal field of dossiers; no oversized hand",
        "roll": "level frame organized by slanting bamboo-slip rows",
        "interaction": "the viewer is the audited official below the desk edge, trapped by the geometry of evidence rather than physically grabbed",
        "motion": "the red brush stroke and released document cords sweep left-to-right across the frame",
        "foreground": "overlapping blank bamboo slips and one cropped official sleeve form a lower diagonal frame",
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
        "code": "S07-HIGH-ALTAR-LEFT3Q-MS-DOWNWARD",
        "elevation": "high 40-degree view from just behind the temple altar",
        "azimuth": "left three-quarter view of the aged emperor below, lifting his eyes and hands toward the altar",
        "scale": "35 mm medium shot with crown, prayer beads and hands forming a triangular rise",
        "roll": "level and solemn",
        "interaction": "the viewer occupies the monk's position above the offered imperial objects",
        "motion": "incense and falling coins drift downward while a cold military reflection enters laterally through the gate",
        "foreground": "cropped altar cloth, incense burner rim and prayer beads frame the lower edge",
    },
    "xixia-li-yuanhao": {
        "code": "S08-EYE-PROFILE-TELE-LATERAL",
        "elevation": "eye level on the Xingqing rampart",
        "azimuth": "exact right-facing profile silhouette, bow fully drawn across the width of the image",
        "scale": "70 mm telephoto medium-wide shot that compresses ruler, banners and Helan Mountains",
        "roll": "level horizon",
        "interaction": "the viewer stands beside an envoy close enough to feel the bowstring tension but outside its path",
        "motion": "the released signal arrow, sleeve and sand-laden banner wind travel right-to-left across the frame",
        "foreground": "a soft-focus battlement notch and envoy shoulder crop the near left edge",
    },
    "q-qin-fu-jian": {
        "code": "S09-WATERLOW-FRONT3Q-WIDE-ARC",
        "elevation": "camera almost at river-surface height, looking up about 15 degrees",
        "azimuth": "front-left three-quarter figure on horseback, placed in the upper-right rather than centered",
        "scale": "28 mm wide shot with cold water occupying the lower half and the army compressed behind",
        "roll": "level waterline",
        "interaction": "the viewer stands ankle-deep among front-rank officers at the river edge",
        "motion": "the whip makes a broad black-gold arc across the sky and exits sideways; spear reflections fracture downward in the water",
        "foreground": "rippling black water and one reflected spear point, not a hand reaching at the viewer",
    },
    "n-wei-xiaowen": {
        "code": "S10-EYE-OTS-REAR3Q-MS-AWAY",
        "elevation": "eye level inside the Luoyang gate",
        "azimuth": "over the shoulder of an old Xianbei guard; the emperor is rear three-quarter walking away, turning his face back to the left",
        "scale": "35 mm medium-wide shot that keeps the reforming ruler large while opening the migration road",
        "roll": "level architectural frame",
        "interaction": "the viewer shares the resisting guard's viewpoint as the old order is left behind",
        "motion": "the discarded riding coat and braid cord fly sideways across the threshold while the ruler's new sleeve moves away into the city",
        "foreground": "guard shoulder, old fur collar and gate shadow create an over-the-shoulder frame",
    },
    "sui-wen": {
        "code": "S11-TOPDOWN-OBLIQUE-MWS-CONVERGENT",
        "elevation": "near top-down 45-degree planning view",
        "azimuth": "the emperor's head and shoulders enter from the upper edge in oblique three-quarter, not facing the viewer",
        "scale": "35 mm medium-wide tableau; hands and transport grid share focus but the face remains readable",
        "roll": "level geometric plan",
        "interaction": "the viewer leans over the same planning surface as a minister witnessing reunification",
        "motion": "river wakes, city-grid lines and mineral cracks converge inward on the final southern marker",
        "foreground": "large abstract planning grid and fleet wakes, with no single object protruding at the lens",
    },
    "sui-yang": {
        "code": "S12-EYE-RIGHTPROFILE-CLOSE-LATERAL",
        "elevation": "intimate seated eye level inside the Jiangdu boat cabin",
        "azimuth": "tight right profile and partial rear three-quarter as he turns toward a blade reflection behind him",
        "scale": "50 mm close shot with face, wet hair, cup and reflection compressed into a narrow cabin corridor",
        "roll": "3-degree Dutch tilt",
        "interaction": "the viewer is trapped at the cabin's side, close enough to hear the overturned cup but not directly confronted",
        "motion": "wine, sleeve and blade reflection sweep horizontally across the image behind the face",
        "foreground": "soft-focus wine cup rim and curtain edge obscure part of the lower frame",
    },
    "tang-tai-zong": {
        "code": "S13-EYE-MINISTERPOV-LEFT3Q-MS-CROSSFRAME",
        "elevation": "seated eye level in court",
        "azimuth": "left three-quarter view, emperor off-center and leaning across the composition toward a minister outside frame",
        "scale": "35 mm medium shot; the paper plane forms a diagonal foreground without enlarging the imperial hand",
        "roll": "level horizon",
        "interaction": "the viewer stands just behind the minister who offers the remonstrance, sharing the risk of the exchange",
        "motion": "the blank sheet passes across the frame from lower-left to upper-right while helmet and bow are pushed away in the opposite direction",
        "foreground": "the minister's sleeve and broad blank paper edge frame the bottom-left",
    },
    "zhou-wu-zetian": {
        "code": "S14-EXTREMELOW-LEFT3Q-WIDE-DOWNWARD",
        "elevation": "extreme low view from the base of the Luoyang audience steps, looking up about 28 degrees",
        "azimuth": "left-facing three-quarter sovereign high in the frame, with crown-bead lines breaking the sky",
        "scale": "24 mm wide medium-full view using monumental steps rather than a frontal close-up",
        "roll": "level axial architecture",
        "interaction": "the viewer is one official within the kneeling ranks and experiences the decree descending through space",
        "motion": "the sealed blank decree and purple-gold wheel rays descend diagonally from upper-right to lower-left, not straight at camera",
        "foreground": "blurred shoulders of two kneeling officials create a low human frame",
    },
    "tang-xian-zong": {
        "code": "S15-EYE-PROFILE-TELE-CLOSE-DEPTH",
        "elevation": "eye level beside a candle in the strategy room",
        "azimuth": "strong right profile seen through the candle flame, with the ruler on the left third looking toward the snowy window",
        "scale": "85 mm compressed close shot; shallow depth separates flame, profile, marker hand and messenger",
        "roll": "level intimate frame",
        "interaction": "the viewer is the newly arrived messenger watching the decision crystallize across the room",
        "motion": "snow-charged ink lines travel from the distant window toward the map while wax sparks rise vertically between viewer and face",
        "foreground": "large out-of-focus candle flame and wax rim partially veil the profile",
    },
    "zhou-shi": {
        "code": "S16-GROUND-FRONTDIAG-WIDE-DUTCH-COLLISION",
        "elevation": "ground-level battlefield camera looking up about 10 degrees",
        "azimuth": "front diagonal three-quarter as the emperor lunges from upper-right toward a fleeing soldier at lower-left",
        "scale": "28 mm dynamic wide shot with both action vectors visible but the emperor dominant",
        "roll": "12-degree counterclockwise Dutch tilt",
        "interaction": "the viewer occupies the wavering soldier's unstable position and is physically pulled back toward the battle",
        "motion": "the grab closes across the frame from right to left while whip and banners point back toward the battlefield depth",
        "foreground": "the fleeing soldier's cropped forearm and shield edge enter from the lower-left",
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
        "code": "C02-SOOT-BAMBOO-VERMILION-G2",
        "dominant": "soot black, bamboo ochre, dusty umber and one decisive vermilion brush stroke",
        "gold": "G2 approved-image density, roughly 5–8 percent; preserve the accepted image but do not use it as the default for later emperors",
        "light": "small warm oil-lamp pools inside a cool gray archive",
        "surface": "dense narrow bamboo-slip rhythm, dry paper dust and diagonal red ink",
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
        "code": "C07-IVORY-VERMILION-CELADON-BRONZE-G1",
        "dominant": "incense ivory, temple vermilion, faded celadon green and muted bronze",
        "gold": "G1 maximum 4 percent, localized to worn Buddha-halo remnants and the surrendered crown; no frame-wide speckles",
        "light": "warm incense haze cut by one cold steel-blue reflection from the gate",
        "surface": "soft ash bloom, worn devotional pigment and thin vertical incense currents",
    },
    "xixia-li-yuanhao": {
        "code": "C08-BONE-BLACK-BLOODRED-TURQUOISE-G1",
        "dominant": "desert bone, soot black, blood-red cloth and small weathered turquoise accents",
        "gold": "G1 maximum 2 percent, only on bow fittings and crown details",
        "light": "hard pale Hexi sun with black banner shadows",
        "surface": "sand abrasion, angular dry-brush gusts and taut horizontal bow rhythm",
    },
    "q-qin-fu-jian": {
        "code": "C09-RIVERBLUE-PURPLE-SILVER-INK-G1",
        "dominant": "cold river blue, imperial purple, spear silver and deep black ink",
        "gold": "G1 maximum 2 percent, one thin aged-gold edge on the whip arc only",
        "light": "cold reflected river light under a bruised gray sky",
        "surface": "watery mineral blooms, downward spear reflections and broad liquid ink arcs",
    },
    "n-wei-xiaowen": {
        "code": "C10-PALESTONE-INDIGO-CELADON-HANRED-G0",
        "dominant": "pale Luoyang stone, deep indigo, muted celadon and restrained Han red",
        "gold": "G0 no gold leaf; use pale stone cracks and cloth contrast instead",
        "light": "clear soft city-gate daylight",
        "surface": "architectural plaster planes, streaming migration dust and long folded-cloth strokes",
    },
    "sui-wen": {
        "code": "C11-SLATE-TEAL-CLAY-CINNABAR-G1",
        "dominant": "slate blue, river teal, clay brown and one muted cinnabar southern marker",
        "gold": "G1 maximum 2 percent, thin transport-grid joins only; no airborne gold particles",
        "light": "cool even planning-room light with a quiet river sheen",
        "surface": "topographic mineral washes, fine converging grid incisions and compact map texture",
    },
    "sui-yang": {
        "code": "C12-WINE-JADE-INDIGO-STEEL-G1",
        "dominant": "wine crimson, dark jade green, night indigo and cold blade steel",
        "gold": "G1 maximum 3 percent, confined to jewelry and cup rim",
        "light": "humid lantern red opposed by a cold steel reflection",
        "surface": "glossy wine arcs, damp silk folds and narrow cabin shadows over dry mural grain",
    },
    "tang-tai-zong": {
        "code": "C13-IRONBLUE-PAPERIVORY-VERMILION-ASH-G0",
        "dominant": "iron blue, paper ivory, restrained Tang vermilion and court ash-gray",
        "gold": "G0 functional hardware only, maximum 1 percent; no decorative gold leaf",
        "light": "balanced court daylight concentrated on the blank remonstrance sheet",
        "surface": "broad paper planes, disciplined armor lines and opposing cross-frame brush currents",
    },
    "zhou-wu-zetian": {
        "code": "C14-PURPLE-CINNABAR-IVORY-GOLD-G3",
        "dominant": "imperial purple, dark cinnabar, ivory and deep ink-black",
        "gold": "G3 deliberate 8–10 percent, reserved for the geometric wheel, crown beads and decree seal; large controlled shapes, never random speckles",
        "light": "monumental purple-gold backlight descending along the steps",
        "surface": "rotating geometric rays, broad purple mineral fields and clean monumental breaks",
    },
    "tang-xian-zong": {
        "code": "C15-SNOWCYAN-AMBER-CHARCOAL-OXIDERED-G0",
        "dominant": "snow cyan, candle amber, charcoal and a small oxide-red map marker",
        "gold": "G0 no gold leaf; warmth comes entirely from flame and wax",
        "light": "single amber candle against cold blue snow light",
        "surface": "frosted dry pigment, shallow-focus wax haze and fine wind-driven snow ink",
    },
    "zhou-shi": {
        "code": "C16-DUST-IRONBLUE-BANNERRED-LEATHER-G0",
        "dominant": "battle dust ochre, iron blue, torn banner red and black-brown leather",
        "gold": "G0 no gold leaf or gilded atmosphere",
        "light": "hard autumn side light filtered through dust",
        "surface": "impact scuffs, ripped-banner strokes and diagonal dust sheets",
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
        "版本：`v2.3 camera-palette-identity-physics`。岩彩媒介保持统一，但主色、光线、表面节奏和金色密度按人物分配。01–03 已批准，不作为后续模板。",
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

1. `01-qin-shi-huang.png` 至 `06-h-zhao-shi-le.png` 已批准，**禁止重生成或覆盖**。
2. 从 `prompts/07-liang-wu.txt` 开始，一次只处理一张；旧版退稿保存在 `rejected/` 的对应原因目录中。
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
