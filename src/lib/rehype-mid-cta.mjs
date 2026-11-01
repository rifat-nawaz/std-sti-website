// Adds one "test at home" call to action in the middle of an article, before its
// third H2 (or the second, for short pages). Only on pages whose frontmatter has
// affiliate: light or roundup.
export default function rehypeMidCta() {
  return (tree, file) => {
    const fm = file.data?.astro?.frontmatter ?? {};
    if (!fm.affiliate || fm.affiliate === 'none') return;
    const offer = fm.offer ?? 'k1';
    const h2s = tree.children.filter((n) => n.type === 'element' && n.tagName === 'h2');
    if (h2s.length < 2) return;
    const target = h2s.length >= 4 ? h2s[2] : h2s[1];
    const html =
      '<aside class="cta-mid" aria-label="Test at home">' +
      '<p><strong>Not sure? A test is the only way to know.</strong>Order a lab-processed kit online and collect your sample at home.<br><span class="cta-note">Partner link: we may earn a commission.</span></p>' +
      `<a class="btn btn-cta" href="/go/${offer}/" rel="sponsored nofollow noopener" target="_blank" data-offer="${offer}">Order an at-home test<span class="sr-only"> (partner link, opens in a new tab)</span></a>` +
      '</aside>';
    const i = tree.children.indexOf(target);
    tree.children.splice(i, 0, { type: 'raw', value: html });
  };
}
