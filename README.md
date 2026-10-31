# STD/STI information website (Astro)

Static site built with Astro 6. Content lives in `src/content/articles/` as Markdown.

## Commands

| Command | What it does |
|---|---|
| `npm install` | Install dependencies (Node 22.12+) |
| `npm run dev` | Local preview at http://localhost:4321 |
| `npm run build` | Build to `dist/` and run the site checks |
| `npm run check:launch` | Strict launch check: fails on any missing page or placeholder |

## Change the brand

Edit `src/config/site.ts`: site name, domain, company details, contact form endpoint,
policy date and affiliate offers. Every page reads from this file.

## Add an article

Create `src/content/articles/<section>/<slug>.md`. The URL is `/<section>/<slug>/`;
`index.md` is the section's main page. Frontmatter fields are defined in
`src/content.config.ts` (title, SEO title, description, answer, takeaways, urgent signs,
FAQ, at least 2 sources, related pages, dates).

## Rules the build enforces

- One H1, unique title and description, canonical tag on every page.
- No unfinished text, no "medically reviewed" claims without a named reviewer, no
  hands-on testing claims.
- Internal links must point to built pages (strict mode).
- Affiliate links go through `/go/<code>/` (noindex, no referrer).
