# STD/STI information website (Astro)

Static site built with Astro 6. Content lives in `src/content/articles/` as Markdown.

## Commands

| Command | What it does |
|---|---|
| `npm install` | Install dependencies (Node 22.12+) |
| `npm run dev` | Local preview at http://localhost:4321 |
| `npm run build` | Build to `dist/` and run the site checks |
| `npm run check:links` | Check every external link (needs internet access) |
| `npm run check:launch` | Strict launch check: fails on any missing page, placeholder or preview block |

Preview builds tell search engines not to index the site. For the live launch, build with
`SITE_ENV=production npm run build`.

## Change the brand

Edit `src/config/site.ts`: site name, domain, company details, contact form endpoint,
policy date and affiliate offers. Every page reads from this file.

## Calls to action

Pages with `affiliate: light` or `roundup` get a test button near the top, one in the
middle of the article (added automatically before the third H2), one in "Your next step"
and a sticky box in the sidebar. Pages with `affiliate: none` get none of these.

## Add an article

Create `src/content/articles/<section>/<slug>.md`. The URL is `/<section>/<slug>/`;
`index.md` is the section's main page. Frontmatter fields are defined in
`src/content.config.ts` (title, SEO title, description, answer, takeaways, urgent signs,
FAQ, at least 2 sources, related pages, dates).

## Rules the build enforces

- One H1, unique title and description, canonical tag on every page.
- No unfinished text, no "medically reviewed" claims without a named reviewer, no
  hands-on testing claims.
- **No treatment details:** the build fails if a page names a medicine or a dose.
  Pages say whether an infection is curable and send readers to a clinician.
- Every internal link and in-page anchor must point to something that exists.
- External links are checked by `npm run check:links` and by a weekly GitHub Action
  (`.github/workflows/check-links.yml`). Affiliate URLs are never fetched.
- Affiliate links go through `/go/<code>/` (noindex, no referrer).
