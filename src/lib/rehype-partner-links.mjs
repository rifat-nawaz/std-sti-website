// Partner links in article text.
// 1. Any Markdown link to /go/... gets rel="sponsored nofollow noopener" and opens in a new tab.
// 2. On pages with partner offers, the first natural mention of a home test kit in a
//    paragraph or list item becomes a partner link (one per page). Pages about
//    emergencies, assault or crisis never get one.
const NO_OFFER = new Set(['HIV-057', 'HIV-058', 'HIV-066', 'HIV-067', 'HIV-069', 'HUB-036', 'HUB-039', 'CHL-087']);
const PHRASE = /\b(lab-processed (?:home |at-home )?(?:test )?kits?|lab-processed home tests?|at-home (?:STD |chlamydia |gonorrhea |syphilis |HIV |herpes |trich |hepatitis [BC] )?(?:test(?:ing)? )?kits?|at-home (?:STD |chlamydia |gonorrhea |syphilis |HIV |herpes )?tests?|home (?:STD )?(?:test )?kits?|mail-in (?:lab )?kits?|home tests?|home testing|test at home|testing at home|self-collected (?:vaginal )?swabs?)\b/i;

function walk(node, fn, parent = null, ancestors = []) {
  fn(node, parent, ancestors);
  if (node.children) for (const c of [...node.children]) walk(c, fn, node, [...ancestors, node]);
}

export default function rehypePartnerLinks() {
  return (tree, file) => {
    const fm = file.data?.astro?.frontmatter ?? {};
    const offer = fm.offer ?? 'k1';
    let hasLink = false;
    walk(tree, (n) => {
      if (n.type === 'element' && n.tagName === 'a' && String(n.properties?.href ?? '').startsWith('/go/')) {
        n.properties.rel = ['sponsored', 'nofollow', 'noopener'];
        n.properties.target = '_blank';
        hasLink = true;
      }
    });
    if (hasLink) return;
    // Herpes pages: the right test is usually a swab of a sore, so no automatic kit links.
    if (!fm.affiliate || fm.affiliate === 'none' || NO_OFFER.has(fm.ref) || /^(HSV|HPV)-/.test(String(fm.ref))) return;
    let done = false;
    walk(tree, (n, parent, anc) => {
      if (done || n.type !== 'text' || !parent) return;
      if (anc.some((a) => a.type === 'element' && ['a', 'h1', 'h2', 'h3', 'h4', 'table', 'code', 'blockquote'].includes(a.tagName))) return;
      if (!anc.some((a) => a.type === 'element' && ['p', 'li'].includes(a.tagName))) return;
      const m = n.value.match(PHRASE);
      if (!m) return;
      const i = parent.children.indexOf(n);
      const before = n.value.slice(0, m.index), after = n.value.slice(m.index + m[0].length);
      const link = { type: 'element', tagName: 'a', properties: { href: `/go/${offer}/`, rel: ['sponsored', 'nofollow', 'noopener'], target: '_blank', dataOffer: offer }, children: [{ type: 'text', value: m[0] }] };
      parent.children.splice(i, 1, ...(before ? [{ type: 'text', value: before }] : []), link, ...(after ? [{ type: 'text', value: after }] : []));
      done = true;
    });
  };
}
