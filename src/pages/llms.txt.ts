import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { SITE } from '../config/site';
import { CONDITIONS } from '../data/conditions';
import { urlFor } from '../lib/paths';
export const GET: APIRoute = async () => {
  const all = (await getCollection('articles')).filter((e) => !e.data.draft);
  const abs = (p: string) => new URL(p, SITE.url).toString();
  const lines = [
    `# ${SITE.name}`,
    '',
    `> ${SITE.description}`,
    '',
    'General health information, not medical advice. Written and fact-checked by the editorial team against CDC, WHO and USPSTF guidance.',
    '',
    '## Conditions',
    ...CONDITIONS.map((c) => `- [${c.name}](${abs(`/${c.slug}/`)}): ${c.summary}`),
    '',
    '## Key pages',
    ...all.filter((e) => ['pillar', 'hub', 'tool', 'data'].includes(e.data.pageType)).map((e) => `- [${e.data.title}](${abs(urlFor(e.id))}): ${e.data.description}`),
    '',
    '## Policies',
    `- [Editorial policy](${abs('/editorial-policy/')})`,
    `- [Medical disclaimer](${abs('/medical-disclaimer/')})`,
    '',
  ];
  return new Response(lines.join('\n'), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
