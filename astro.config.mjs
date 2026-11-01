import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { SITE } from './src/config/site.ts';
import rehypeMidCta from './src/lib/rehype-mid-cta.mjs';

export default defineConfig({
  site: SITE.url,
  trailingSlash: 'always',
  build: { format: 'directory' },
  markdown: { rehypePlugins: [rehypeMidCta] },
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/go/') && !page.includes('/404'),
    }),
  ],
});
