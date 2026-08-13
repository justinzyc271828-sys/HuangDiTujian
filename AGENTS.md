# Repository Guidelines

## Project Structure & Module Organization

`apps/web/` contains the React, TypeScript, and Vite frontend; code lives in `src/`, while generated browser data is written to `public/data/`. Canonical data belongs in `data/`: use `data/emperors/` and `data/places/` for one-record-per-file YAML, and copy schemas from `data/templates/`. Biographies and source dossiers live under `content/`. Keep versioned images, maps, and style references in `assets/`, decisions in `docs/`, and Python utilities in `tools/`. Large local research material belongs in the ignored `reference/` tree.

## Build, Test, and Development Commands

Run commands from the repository root unless noted:

```powershell
python tools/validate_data.py          # Check IDs, references, links, and asset declarations
python tools/build_site_data.py        # Generate apps/web/public/data/{site,index,places,emperor/*}.json (maps illustrations/<id>.webp when present; site.json is tooling-only, pruned from dist)
python tools/convert_illustrations_webp.py  # Convert key-art PNG masters into public/illustrations/*.webp + og/*.jpg
cd apps/web; npm ci; npm run dev       # Install locked dependencies and start Vite on port 5173
npm run build                          # Type-check, create the production bundle, then postbuild per-emperor OG share pages + 404.html + sitemap/robots + font subsetting (needs pip: pyyaml fonttools brotli)
npm run preview                        # Serve the built bundle for final inspection (base path /HuangDiTujian/)
```

`npm run dev` and `npm run build` automatically rebuild site data through their `pre*` scripts. Pushing `master` triggers `.github/workflows/pages.yml`, which builds and deploys `apps/web/dist` to GitHub Pages at `https://justinzyc271828-sys.github.io/HuangDiTujian/`; production builds use base path `/HuangDiTujian/` (dev stays at `/`).

## Coding Style & Naming Conventions

Use four-space indentation and `snake_case` for Python. Follow existing TypeScript style: two spaces, double quotes, semicolons, strict typing, `PascalCase` React components, and `useCamelCase` hooks. Use lowercase kebab-case IDs and filenames such as `qin-shi-huang.yaml`; YAML `id` values must match their filename stem. Preserve UTF-8 Chinese content and existing `[[target-id|显示名]]` cross-link syntax. No formatter or linter is configured, so match neighboring files and keep diffs focused.

## Testing Guidelines

There is currently no unit-test framework or coverage threshold. Every data or content change must pass `python tools/validate_data.py`; every frontend change must pass `npm run build`. For UI changes, manually check `/`, `/emperor/qin-shi-huang`, and `/lab`, including navigation, data loading, and responsive layout. Add automated tests alongside any future test infrastructure and document the new command here.

## Commit & Pull Request Guidelines

Recent commits use short, imperative, sentence-style summaries, for example: `Add video-01 evidence cards and storyboards.` Keep each commit scoped to one coherent change. Pull requests should explain the purpose, list affected data/content areas, record validation commands run, and link relevant issues or docs. Include before/after screenshots for visible UI changes and flag generated files separately.

## Repository Boundaries

Write only inside this repository. Do not commit secrets, `.env` files, build output, caches, or large ignored reference material. Treat files in `data/`, `content/`, and `docs/` as source; regenerate derived web data instead of hand-editing it.
