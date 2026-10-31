// Post-build checks on the generated HTML in dist/.
//   node scripts/check-site.mjs           -> errors fail the build; launch blockers are warnings
//   node scripts/check-site.mjs --strict  -> launch mode: launch blockers fail too
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative } from 'node:path';

const STRICT = process.argv.includes('--strict');
const DIST = new URL('../dist/', import.meta.url).pathname;
const errors = [];
const blockers = [];

function walk(dir) {
  return readdirSync(dir).flatMap((f) => {
    const p = join(dir, f);
    return statSync(p).isDirectory() ? walk(p) : [p];
  });
}
const pages = walk(DIST).filter((f) => f.endsWith('.html'));
const titles = new Map();
const descs = new Map();
const missing = new Map();

const pick = (html, re) => (html.match(re) || [])[1]?.trim();

for (const file of pages) {
  const rel = '/' + relative(DIST, file).replace(/index\.html$/, '');
  const html = readFileSync(file, 'utf8');
  const isRedirect = rel.startsWith('/go/');
  if (isRedirect) continue;
  const text = html.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<style[\s\S]*?<\/style>/g, '');

  const title = pick(html, /<title>([^<]*)<\/title>/);
  const desc = pick(html, /<meta name="description" content="([^"]*)"/);
  if (!title) errors.push(`${rel}: missing <title>`);
  if (!desc) errors.push(`${rel}: missing meta description`);
  if (!rel.startsWith('/404') && !/<link rel="canonical"/.test(html)) errors.push(`${rel}: missing canonical`);
  const h1s = (text.match(/<h1[\s>]/g) || []).length;
  if (h1s !== 1) errors.push(`${rel}: ${h1s} <h1> tags (need exactly 1)`);
  if (title) titles.set(title, [...(titles.get(title) || []), rel]);
  if (desc) descs.set(desc, [...(descs.get(desc) || []), rel]);

  // Banned content: unfinished text and claims we can't support.
  const visible = text.replace(/<[^>]+>/g, ' ');
  for (const [re, why] of [
    [/\bTODO\b|\bTBD\b|lorem ipsum|\[x\]/i, 'unfinished text'],
    [/medically reviewed|reviewed by (a |our )?(clinician|doctor|physician)/i, 'review claim without a named reviewer'],
    [/we (have )?tested (these|this|the|every|each) (kit|test)/i, 'hands-on testing claim'],
  ]) {
    if (re.test(visible)) errors.push(`${rel}: ${why}`);
  }
  if (/\[(Site Name|Company legal name|Street address|contact email|privacy email)[^\]]*\]/.test(visible)) {
    blockers.push(rel);
  }

  // Internal links must resolve to a built page.
  for (const m of html.matchAll(/href="(\/[^"#?]*)/g)) {
    const href = m[1];
    if (/\.(svg|png|xml|txt|ico|webmanifest)$/.test(href)) continue;
    const target = join(DIST, href, href.endsWith('/') ? 'index.html' : '');
    if (!existsSync(target) && !existsSync(join(DIST, href))) {
      missing.set(href, [...(missing.get(href) || []), rel]);
    }
  }
}

for (const [t, list] of titles) if (list.length > 1) errors.push(`duplicate title "${t}": ${list.join(', ')}`);
for (const [d, list] of descs) if (list.length > 1) errors.push(`duplicate description on ${list.join(', ')}`);

const linkMsgs = [...missing].map(([href, from]) => `broken link ${href} (from ${from.length} page${from.length > 1 ? 's' : ''}, e.g. ${from[0]})`);

console.log(`\nSite check: ${pages.length} HTML files`);
if (linkMsgs.length) {
  console.log(`\n${STRICT ? 'ERROR' : 'Not yet written'}: ${linkMsgs.length} linked pages missing`);
  linkMsgs.forEach((m) => console.log('  - ' + m));
}
if (blockers.length) {
  console.log(`\n${STRICT ? 'ERROR' : 'Launch blocker'}: site name or company details are still placeholders in src/config/site.ts (${blockers.length} pages)`);
}
if (errors.length) {
  console.log(`\nERRORS (${errors.length}):`);
  errors.forEach((e) => console.log('  - ' + e));
}
const fail = errors.length > 0 || (STRICT && (linkMsgs.length > 0 || blockers.length > 0));
console.log(fail ? '\nSite check FAILED\n' : '\nSite check passed\n');
process.exit(fail ? 1 : 0);
