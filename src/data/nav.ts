// Header and footer menus. Every link here must point to a page that exists;
// the build check fails on a broken menu link.
export const TESTING_MENU = [
  { href: '/std-testing/best-at-home-std-tests/', label: 'Best STD test kits', desc: 'Full-panel kits compared' },
  { href: '/std-testing/window-period/', label: 'Window period calculator', desc: 'When a test can give a reliable result' },
  { href: '/std-testing/reading-results/', label: 'How to read your results', desc: 'Positive, negative, reactive and more' },
  { href: '/std-testing/', label: 'All testing guides', desc: '' },
];

export const GUIDES_MENU = [
  { href: '/guides/symptom-checker/', label: 'Symptom checker', desc: 'Which test fits your symptoms' },
  { href: '/guides/std-symptoms-in-men/', label: 'STD symptoms in men', desc: '' },
  { href: '/guides/std-symptoms-in-women/', label: 'STD symptoms in women', desc: '' },
  { href: '/guides/telling-a-partner/', label: 'Telling a partner', desc: '' },
  { href: '/guides/', label: 'All guides', desc: '' },
];

export const FOOTER_POLICIES = [
  { href: '/about/', label: 'About us' },
  { href: '/editorial-policy/', label: 'Editorial policy' },
  { href: '/how-we-make-money/', label: 'How we make money' },
  { href: '/medical-disclaimer/', label: 'Medical disclaimer' },
  { href: '/privacy/', label: 'Privacy policy' },
  { href: '/health-data-notice/', label: 'Consumer health data notice' },
  { href: '/terms/', label: 'Terms of use' },
  { href: '/accessibility/', label: 'Accessibility' },
  { href: '/contact/', label: 'Contact' },
];

export const POLICY_NAV = FOOTER_POLICIES.filter((p) => p.href !== '/contact/');
