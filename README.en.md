# HuangDiTujian (皇帝图鉴) — An Interactive Compendium of Chinese Emperors

**HuangDiTujian** ("Illustrated Compendium of Emperors") turns the rulers of Chinese history — formal emperors plus an extended ring of "quasi-emperors" — into a browsable, map-linked, collectible digital compendium, backed by a fully versioned, source-cited dataset.

[中文 README](README.md)

## What it is

- **269 rulers indexed**, each with a source dossier built from the Twenty-Four Histories (二十四史) and other primary texts — every claim traces back to a cited passage.
- **A React + Vite front end** (`apps/web`) presenting each emperor as a memorial-style ("奏折") page: portrait, six-dimension radar stats, chronological timeline, relationship graphs, and an annotated life-route map.
- **AI-painted portraits** in a locked "mineral-mural / cracked-wall" (岩彩裂壁) art style, produced through a versioned prompt-and-manifest pipeline with a style bible, camera matrix, and palette matrix.
- **A short-video production line** (`video-01`): the pilot batch of 20 emperors gets storyboards, key-art specs, and classical-Chinese six-dimension stat cards.

## Current snapshot

| Area | Status |
|------|--------|
| Master index | **269** rulers (`data/catalog/emperors_master.*`) |
| Source dossiers | 269 dossiers, ~1,950 evidence cards, scaffold-free |
| Video-01 pilot | 20 emperors: stats / storyboards / prompts done; illustrations in progress |
| Product pages (YAML + bio) | Growing curated set, incl. Qin Shi Huang, Han Wudi, Tang Taizong |
| Front end | Gallery index + memorial-style emperor pages, running dev-previewable |

## Repository layout

```
HuangDiTujian/
├── docs/                     # Framework, data model, roadmap, progress board (00–08)
├── data/
│   ├── catalog/              # Master 269 · video20 · six-dimension stats
│   ├── emperors/             # Curated product YAML (one file per emperor)
│   ├── places/               # Historical places with coordinates
│   └── templates/            # YAML schemas
├── content/
│   ├── bios/                 # Long-form biographies
│   ├── sources/              # Source dossiers & evidence cards (per emperor)
│   └── video/video-01/       # Storyboards & key-art specs
├── assets/
│   ├── style-bible/          # Locked illustration style system
│   ├── video-01/             # Current illustration pipeline (prompts + manifest + outputs)
│   └── maps/                 # Historical map material
├── HuangDiTujian-Ref/        # Primary-source reference library (local research material)
├── tools/                    # Python build / validation / export scripts
└── apps/web/                 # React + TypeScript + Vite front end
```

## How it works

1. **Source-first research** — every ruler starts as a source dossier (`content/sources/{id}/`) with evidence cards quoting primary histories, each card carrying a citation and a state-machine status.
2. **Curated data layer** — dossiers are distilled into one-YAML-per-emperor records (`data/emperors/`), biographies (`content/bios/`), and places (`data/places/`), with `[[cross-link]]` syntax between rulers.
3. **Build & validate** — `tools/validate_data.py` checks IDs, references, links, and asset declarations; `tools/build_site_data.py` compiles everything into the JSON the front end serves.
4. **Presentation** — the web app renders the gallery index, memorial-style pages, radar stats, and historical maps.

## Run locally

```bash
python tools/validate_data.py        # data integrity checks
python tools/build_site_data.py      # compile site data
cd apps/web
npm ci
npm run dev                          # http://localhost:5173
```

## Design principles

- **No claim without a source** — if it isn't in a primary text, it isn't in the dataset.
- **Everything versioned** — texts, data, prompts, rejected image drafts, and decisions all live in git.
- **Regenerate, don't hand-edit** — derived web data is rebuilt from source by scripts.

## License / usage

Personal research and creative project; historical source texts are public domain, AI-generated artwork and all curation are the author's own work in progress.
