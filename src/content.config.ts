import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Each article is a Markdown file. Its URL comes from the file path:
//   src/content/articles/chlamydia/index.md          -> /chlamydia/
//   src/content/articles/chlamydia/symptoms-in-men.md -> /chlamydia/symptoms-in-men/
const source = z.object({
  publisher: z.string(),
  title: z.string(),
  year: z.union([z.number(), z.string()]),
  url: z.string().url(),
});

const articles = defineCollection({
  loader: glob({
    pattern: '**/*.md',
    base: './src/content/articles',
    generateId: ({ entry }) => entry.replace(/\.md$/, ''),
  }),
  schema: z.object({
    ref: z.string(), // Content-plan ID, e.g. CHL-018
    title: z.string().max(110),
    seoTitle: z.string().max(70),
    description: z.string().min(70).max(170),
    cluster: z.string(),
    pageType: z.enum(['pillar', 'hub', 'article', 'comparison', 'roundup', 'review', 'checklist', 'data', 'tool']),
    primaryQuery: z.string(),
    riskLevel: z.enum(['high', 'medium', 'standard']).default('standard'),
    affiliate: z.enum(['none', 'light', 'roundup']).default('none'),
    offer: z.enum(['k1', 'k2', 'k3']).optional(),
    tool: z.enum(['window-period', 'symptom-checker']).optional(),
    answer: z.string().optional(),
    takeaways: z.array(z.string()).default([]),
    urgent: z.array(z.string()).default([]),
    faq: z.array(z.object({ q: z.string(), a: z.string() })).default([]),
    sources: z.array(source).min(2),
    related: z.array(z.string()).default([]),
    published: z.coerce.date(),
    updated: z.coerce.date(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { articles };
