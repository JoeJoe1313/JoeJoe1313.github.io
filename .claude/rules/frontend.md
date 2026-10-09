---
paths:
  - "web/**/*"
---

# `/web` rules — JoJo's Blog (Astro + MDX), path-scoped

> Enforceable rules for the blog in `/web`. The "why" lives in `web/docs/`. This is a
> **content blog** (static-first), not an app — auto-loaded when you touch any `web/**` file.
>
> Migration in progress: the blog is being rewritten from Pelican (repo root) to Astro here.
> During migration the root Pelican site stays live; see `web/docs/orientation.md`.

## Stack (don't substitute without a decision)

Astro 6 · MDX (`@astrojs/mdx`) · React 19 islands (`@astrojs/react`) · TypeScript ·
build-time MathJax (`remark-math` + `rehype-mathjax`) · Shiki (built-in highlighting) ·
Pagefind (search) · Supabase (comments). **Static output (SSG), no SSR/adapter.**
Rationale: [web/docs/stack-decisions.md](../../web/docs/stack-decisions.md).

## Core principle: static-first, React only for islands

- Pages render to **static HTML at build**. Default to `.astro` components (zero JS).
- Reach for a React island **only** for genuine client interactivity (search box, comments).
  Add a `client:*` directive (`client:visible` / `client:idle`) only on those islands.
- Never make the whole page a SPA. No client-side router. No global client data store.

## Content & authoring

- Articles live in `src/content/articles/` as `.md` (or `.mdx` when a component is embedded);
  pages in `src/content/pages/`. Frontmatter is validated by the Zod schema in
  `src/content.config.ts` — add a field to the schema before using it.
- **Frontmatter is lowercase** (`title`, `pubDate`, `category`, `tags`, `slug`, `status`,
  `series?`, `comments?`). Don't reintroduce Pelican's capitalized keys.
- **Math:** only `$…$` (inline) and `$$…$$` (display) reach the renderer. Do **not** use
  `\[ \]`, `\( \)`, or bare `\begin{equation}` — the migration normalizes these to `$`/`$$`.
- **Assets:** static files (images, embedded `*_animation.html`, notebooks, PDFs) live under
  `web/public/{images,code,docs}/<date-slug>/` and are referenced with absolute paths
  (`/images/...`), never `{static}/...`.
- **URLs are preserved** from the Pelican site (flat `{slug}.html` via `build.format: 'file'`).
  Don't change an article's `slug`, or add a redirect if you must.

## Code conventions

- `.astro` files: default-export markup is the Astro norm — fine here (this is NOT the old
  SPA's "named-exports-only" rule).
- React islands: `PascalCase.tsx`, TypeScript, no `any`. Keep them small and self-contained.
- Use the `@/` alias for `src/` (configured in `tsconfig.json`); avoid deep `../../..`.
- Prefer Astro built-ins before adding deps: Content Collections, `<Image>`, Shiki, `paginate()`.

## Quality gate

`npm run check` (astro check / typecheck) and `npm run build` must pass. The build runs
`astro build && pagefind --site dist`; confirm `dist/` has real static HTML per article
(view-source shows full text + pre-rendered math + per-page `<title>`/OG meta).

## Out of scope / retired

The previous Anchor Loans React-platform rules that lived here are archived in
`.anchor-loans-docs-backup/`. They do **not** apply to this blog.
