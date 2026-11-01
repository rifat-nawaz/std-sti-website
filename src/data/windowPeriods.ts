// Window periods used by the calculator and the chart page.
// "earliest" = days after exposure when some infections can first be detected.
// "reliable" = days after which a negative result is considered reliable for most people.
// Sources: CDC HIV testing guidance (window periods for NAT, lab Ag/Ab, rapid Ag/Ab, antibody tests);
// CDC STI Treatment Guidelines 2021; CDC viral hepatitis clinical overviews.
export type WindowRow = {
  key: string;
  name: string;
  test: string;
  earliest: number;
  reliable: number;
  link: string;
  note?: string;
};

export const WINDOW_PERIODS: WindowRow[] = [
  { key: 'chlamydia', name: 'Chlamydia', test: 'NAAT (urine or swab)', earliest: 7, reliable: 14, link: '/chlamydia/testing/' },
  { key: 'gonorrhea', name: 'Gonorrhea', test: 'NAAT (urine or swab)', earliest: 7, reliable: 14, link: '/gonorrhea/testing/' },
  { key: 'trichomoniasis', name: 'Trichomoniasis', test: 'NAAT (urine or swab)', earliest: 7, reliable: 28, link: '/trichomoniasis/testing/' },
  { key: 'syphilis', name: 'Syphilis', test: 'Blood antibody test', earliest: 21, reliable: 90, link: '/syphilis/testing/', note: 'A sore can appear before the blood test turns positive. A clinician can test a sore directly.' },
  { key: 'hiv-nat', name: 'HIV', test: 'Lab nucleic acid test (NAT)', earliest: 10, reliable: 33, link: '/hiv/testing/' },
  { key: 'hiv-lab', name: 'HIV', test: 'Lab antigen/antibody blood draw', earliest: 18, reliable: 45, link: '/hiv/testing/' },
  { key: 'hiv-rapid', name: 'HIV', test: 'Finger-prick antigen/antibody', earliest: 18, reliable: 90, link: '/hiv/testing/' },
  { key: 'hiv-ab', name: 'HIV', test: 'Antibody test (incl. oral self-test)', earliest: 23, reliable: 90, link: '/hiv/testing/' },
  { key: 'herpes', name: 'Herpes (HSV-1, HSV-2)', test: 'IgG blood antibody test', earliest: 21, reliable: 112, link: '/herpes/testing/', note: 'If you have a sore now, a swab of the sore is the better test.' },
  { key: 'hepatitis-b', name: 'Hepatitis B', test: 'Surface antigen (HBsAg) blood test', earliest: 7, reliable: 63, link: '/hepatitis-b/' },
  { key: 'hepatitis-c', name: 'Hepatitis C', test: 'Antibody blood test', earliest: 28, reliable: 84, link: '/hepatitis-c/', note: 'An HCV RNA test can find the virus 1 to 2 weeks after exposure.' },
];

export const NOT_IN_CALCULATOR = [
  { name: 'HPV', reason: 'There is no window-period test. People with a cervix are checked through routine cervical screening; there is no approved HPV test for people with a penis.', link: '/hpv/' },
  { name: 'Mycoplasma genitalium', reason: 'Testing is advised only for ongoing symptoms, not as a timed screening test.', link: '/mycoplasma-genitalium/' },
];
