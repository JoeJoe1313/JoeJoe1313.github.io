# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Two unrelated projects share this working tree:

1. **The Pelican blog (repo root)** — "JoJo's Blog", a static site generator that compiles
   Markdown into HTML and deploys to GitHub Pages at `JoeJoe1313.github.io`. This is the
   tracked, primary project and the subject of everything below unless noted.
2. **`/web`** — a separate, self-contained React platform (an "Anchor Loans" portfolio
   chatbot rebuild) that happens to live inside this tree. It has a **different owner, stack,
   OS (Windows/PowerShell), and rule set**. Do not apply blog conventions to it. Its rules
   are path-scoped in `.claude/rules/frontend.md` (auto-loaded when you touch `web/**`), and
   its docs live in `web/docs/` (start with `web/docs/orientation.md`). Currently only
   `web/docs/` is checked in; the React `src/` is not yet present here.

## Build & local development (Pelican blog)

Install deps into a virtualenv (`.venv` exists in-tree), then:

```sh
pip install -r requirements.txt
make devserver PORT=8000   # build + autoregenerate + serve at localhost:8000 (live editing)
make html                  # one-off build (this is exactly what CI runs)
make clean                 # delete the build output
```

There is no test suite; **`make html` with zero metadata warnings is the validation step.**
Plugins ship their own pytest files (e.g. `plugins/render_math/test_render_math.py`) but
they are not wired into a project-wide runner.

### Critical gotchas (these will bite you)

- **Two build tools write to different output directories.** The `make` targets pass
  `-o output/` and build to **`output/`** (gitignored). The `invoke` tasks in `tasks.py`
  honor `OUTPUT_PATH = "docs"` from `pelicanconf.py` and build to **`docs/`** instead.
  **CI and deployment use `make` → `output/`, so prefer the `make` targets** to match
  production. (Note: `content/docs/` is unrelated source PDFs, and `OUTPUT_PATH="docs"` is
  the `invoke` output dir — three different "docs" meanings.)
- **Stork is a hard build dependency.** `plugins/search` shells out to the `stork` binary and
  raises `"Stork must be installed and available on $PATH"` if it is missing, failing the
  whole build. Install it (`cargo install stork-search --locked`) before building locally.
- **`publishconf.py` does not exist.** Any command that references it — `make publish`,
  `make github`, `invoke preview`, `invoke gh_pages` — will fail. Use `make html`.
  (The Copilot instructions describe a `docs/`→`main`-branch deploy via `invoke gh-pages`;
  that is **stale** — see Deployment below for the real pipeline.)

## Deployment & CI (`.github/workflows/main.yml`)

Deployment is fully automated via GitHub Actions on **push to `master`** (the active dev
branch) — not a manual branch push. The pipeline is a conditional DAG:

1. **`changes`** — diffs the pushed range to detect edits under `supabase/migrations/` and
   `supabase/functions/`.
2. **`migrations`** (only if migrations changed) — `supabase db push`.
3. **`edge-functions`** (only if functions changed) — `supabase functions deploy`.
4. **`build`** — installs Python deps + Rust + Stork, then runs `make html` (output → `output/`)
   with the Supabase env vars injected, and uploads `output/` as the Pages artifact.
5. **`deploy`** — `actions/deploy-pages` publishes the artifact to GitHub Pages.

A second workflow, `update-game.yml`, regenerates `game.gif` (a GitHub-activity space-shooter)
on a daily cron and commits it.

## Content authoring model

Articles are `content/articles/YYYY-MM-DD-<slug>.md`; pages are `content/pages/<name>.md`.
Both render to a flat `{slug}.html` URL (no date in the path). Front matter is Markdown-meta
style (not YAML fences):

```
Title: Lissajous Curves
Date: 2025-04-22 07:00
Category: Mathematics
Tags: mathematics, python
Slug: lissajous-curves
Status: draft        # omit to publish; `draft` keeps it out of listings
```

- **`WITH_FUTURE_DATES = False`** — future-dated articles stay unpublished until their date.
- **Math:** `$...$` inline, `$$...$$` block, rendered by the `render_math` (MathJax) plugin.
- **Table of contents:** put a literal `[TOC]` marker where you want it.
- **Assets are co-located by date-slug:** code in `content/code/<date-slug>/`, images in
  `content/images/<date-slug>/`. Reference them with Pelican's `{static}/...` substitution,
  never hardcoded paths. `STATIC_PATHS` (in `pelicanconf.py`) controls what gets copied —
  currently `images`, `code`, and `theme/images`.
- **Embedding source files:** the `include_code` / `include_code_collapsible` liquid tags
  pull a file from `content/code/` into a fenced block.
- **Content can use Jinja2** (via the `jinja2content` plugin) in addition to Markdown.

## Plugins

All plugins live in `plugins/` and are activated by the `PLUGINS` list in `pelicanconf.py`
(adding a folder there does nothing until it is listed). Beyond `render_math` and `search`
(Stork) covered above: `summary` (first-paragraph summaries), `series` (link posts via a
`Series:` front-matter key), `statistics`, `extract_toc`, and `goodreads_activity` /
`goodreads_quotes` (fetch RSS feeds configured by `GOODREADS_*` settings).

## Comments (Supabase)

Optional, env-gated comment widget — see `SUPABASE_COMMENTS.md` for the full setup. Config
is read in `pelicanconf.py` from `SUPABASE_URL` / `SUPABASE_ANON_KEY` /
`SUPABASE_COMMENTS_*` env vars; `pelicanconf.py` auto-loads a local `.env` file (via its
`load_local_env` helper) so values can live there for local builds, and come from repo
Secrets in CI. The SQL schema lives in `supabase/migrations/`; changes there are auto-applied
by the CI `migrations` job. Disable comments on a single page with `Comments: False` in front
matter.

## Theme

`themes/elegant/` is the active theme (set by `THEME`); `themes/notmyidea/` is unused.
Templates are in `themes/elegant/templates/` (`base.html` is the global layout), static
assets in `themes/elegant/static/`.
