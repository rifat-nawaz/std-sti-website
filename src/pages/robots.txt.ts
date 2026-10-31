import type { APIRoute } from 'astro';
import { SITE, IS_PRODUCTION } from '../config/site';
export const GET: APIRoute = () =>
  new Response(`User-agent: *\n${IS_PRODUCTION ? 'Disallow: /go/' : 'Disallow: /'}\n\nSitemap: ${new URL('/sitemap-index.xml', SITE.url)}\n`, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
