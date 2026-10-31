// One place for every site-wide value. Change the brand here and it updates everywhere.
export const SITE = {
  name: '[Site Name]',
  shortName: '[Site Name]',
  url: 'https://www.example.com',
  tagline: 'Clear, judgment-free answers about STDs',
  description:
    'Plain-language guides to STD symptoms, testing and treatment for people in the US, fact-checked against CDC, WHO and USPSTF guidance.',
  editorialTeam: 'Editorial Team',
  language: 'en-US',
  launchDate: '2027-08-09',
  // Date shown on the policy pages. Change it whenever a policy changes.
  policiesUpdated: '2026-10-31',
  // Business details. Required before launch: the build prints a warning while any
  // value still starts with "[", and `npm run check:launch` fails.
  company: {
    legalName: '[Company legal name]',
    address: '[Street address, City, State ZIP]',
    email: '[contact email]',
    privacyEmail: '[privacy email]',
  },
  // Contact form endpoint (Formspree, Netlify Forms, Cloudflare Worker...). Leave empty
  // until hosting is chosen; the Contact page then shows the email address only.
  contactFormEndpoint: '',
  replyDays: 3,
  // Optional outside medical advisors. Add someone only after their license and degree
  // are verified (see /editorial-policy/). Empty list = the section is hidden.
  advisors: [] as { name: string; credentials: string; role: string; license: string; verifiedOn: string }[],
} as const;

export const editorialByline = `${SITE.name} ${SITE.editorialTeam}`;

// Affiliate offers. Codes are neutral: they never name a condition or page.
// Brand stays null until confirmed in the affiliate dashboard.
export const OFFERS = {
  k1: {
    label: 'At-home STD test',
    brand: null as string | null,
    url: 'https://www.kqzyfj.com/click-101241683-15733880',
    note: 'Evergreen offer. Default for general CTAs.',
  },
  k2: {
    label: 'At-home STD test',
    brand: null as string | null,
    url: 'https://www.dpbolvw.net/click-101241683-11648965',
    note: 'Second offer. Used on the kit roundups.',
  },
  k3: {
    label: 'At-home STD test, 10% off',
    brand: null as string | null,
    url: 'https://www.dpbolvw.net/click-101241683-13498256',
    note: '10% off offer: confirm terms and end date before promoting the discount in copy.',
  },
} as const;

export type OfferId = keyof typeof OFFERS;
export const PRIMARY_OFFER: OfferId = 'k1';
