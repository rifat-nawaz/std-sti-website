// Checks every external link in dist/ (sources, partner targets, resources).
// Run after a build: node scripts/check-external-links.mjs
// Exits 1 if any link returns an error. Runs weekly in GitHub Actions too.
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const DIST = new URL('../dist/', import.meta.url).pathname;
const walk = (d) => readdirSync(d).flatMap((f) => (statSync(join(d, f)).isDirectory() ? walk(join(d, f)) : [join(d, f)]));
const urls = new Map();
for (const f of walk(DIST).filter((f) => f.endsWith('.html'))) {
  const html = readFileSync(f, 'utf8');
  for (const m of html.matchAll(/href="(https?:\/\/[^"]+)"/g)) {
    const u = m[1].replace(/&amp;/g, '&');
    if (/example\.com|schema\.org/.test(u)) continue;
    urls.set(u, (urls.get(u) || 0) + 1);
  }
}
// Affiliate click URLs are skipped so we never register fake clicks.
const skip = (u) => /(dpbolvw\.net|kqzyfj\.com|anrdoezrs\.net|jdoqocy\.com|tkqlhce\.com)\//.test(u);
const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36';
const bad = [];
async function check(u) {
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const res = await fetch(u, { redirect: 'follow', headers: { 'user-agent': UA, accept: 'text/html,*/*' }, signal: AbortSignal.timeout(20000) });
      if (res.status < 400) return;
      // Some sites refuse automated requests; report them separately.
      if (res.status === 403 || res.status === 429) { bad.push([u, `${res.status} (blocked bots; check by hand)`]); return; }
      if (attempt === 1) bad.push([u, String(res.status)]);
    } catch (e) {
      if (attempt === 1) bad.push([u, e.name === 'TimeoutError' ? 'timeout' : e.message]);
    }
  }
}
const list = [...urls.keys()].filter((u) => !skip(u));
const queue = [...list];
await Promise.all(Array.from({ length: 6 }, async () => { while (queue.length) await check(queue.shift()); }));
console.log(`External links checked: ${list.length}`);
const hard = bad.filter(([, s]) => !s.includes('check by hand'));
for (const [u, s] of bad) console.log(`  ${s.padEnd(34)} ${u}`);
console.log(hard.length ? `\n${hard.length} broken external links` : '\nNo broken external links');
process.exit(hard.length ? 1 : 0);
