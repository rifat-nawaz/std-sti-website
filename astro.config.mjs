import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { SITE } from './src/config/site.ts';
import rehypePartnerLinks from './src/lib/rehype-partner-links.mjs';

export default defineConfig({
  site: SITE.url,
  trailingSlash: 'always',
  build: { format: 'directory' },
  markdown: { rehypePlugins: [rehypePartnerLinks] },
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/go/') && !page.includes('/404'),
    }),
  ],
});
