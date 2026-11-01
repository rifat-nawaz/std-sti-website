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
const HEADERS = {
  'user-agent': UA,
  accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'accept-language': 'en-US,en;q=0.9',
};
const bad = [];
const viaArchive = [];

// Sites like cdc.gov block automated checkers. For those, ask the Internet Archive
// whether the page returned 200 in the last two years.
async function archiveOk(u) {
  // Try the URL as written, then with or without "www.".
  const alt = u.includes('://www.') ? u.replace('://www.', '://') : u.replace('://', '://www.');
  return (await archiveOne(u)) ?? (await archiveOne(alt));
}
async function archiveOne(u) {
  try {
    const api = `https://archive.org/wayback/available?url=${encodeURIComponent(u)}`;
    const j = await (await fetch(api, { signal: AbortSignal.timeout(20000) })).json();
    const snap = j?.archived_snapshots?.closest;
    if (!snap || snap.status !== '200') return null;
    const ts = snap.timestamp; // YYYYMMDDhhmmss
    const age = (Date.now() - Date.UTC(+ts.slice(0, 4), +ts.slice(4, 6) - 1, +ts.slice(6, 8))) / 864e5;
    return age < 730 ? `${ts.slice(0, 4)}-${ts.slice(4, 6)}-${ts.slice(6, 8)}` : null;
  } catch { return null; }
}

async function check(u) {
  let last = '';
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      const res = await fetch(u, { redirect: 'follow', headers: HEADERS, signal: AbortSignal.timeout(20000) });
      if (res.status < 400) return;
      last = String(res.status);
      // Bot protection that redirects to an "apology" or challenge page counts as blocked, not missing.
      if (/apology|abuse|captcha|challenge|blocked/i.test(res.url) && res.url !== u) { last = '403'; break; }
      if (res.status === 403 || res.status === 429) break;
    } catch (e) {
      last = e.name === 'TimeoutError' ? 'timeout' : e.message;
    }
  }
  if (last === '403' || last === '429') {
    const seen = await archiveOk(u);
    if (seen) { viaArchive.push([u, seen]); return; }
  }
  bad.push([u, last]);
}
const list = [...urls.keys()].filter((u) => !skip(u));
const queue = [...list];
await Promise.all(Array.from({ length: 6 }, async () => { while (queue.length) await check(queue.shift()); }));
console.log(`External links checked: ${list.length}`);
console.log(`  OK directly: ${list.length - bad.length - viaArchive.length}`);
console.log(`  OK via Internet Archive (site blocks checkers): ${viaArchive.length}`);
for (const [u, d] of viaArchive) console.log(`    last seen ${d}  ${u}`);
const hard = bad;
for (const [u, s] of bad) console.log(`  BROKEN ${s.padEnd(10)} ${u}`);
console.log(hard.length ? `\n${hard.length} broken external links` : '\nNo broken external links');
process.exit(hard.length ? 1 : 0);
