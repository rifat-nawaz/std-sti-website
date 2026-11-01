export type Condition = {
  slug: string;
  name: string;
  menuName: string;
  group: 'core' | 'more' | 'lookalike';
  status: string;
  statusTone: 'curable' | 'manageable' | 'notsti';
  summary: string;
};

export const CONDITIONS: Condition[] = [
  { slug: 'chlamydia', name: 'Chlamydia', menuName: 'Chlamydia', group: 'core', status: 'Curable', statusTone: 'curable', summary: 'The most commonly reported STD in the US. Most people have no symptoms.' },
  { slug: 'gonorrhea', name: 'Gonorrhea', menuName: 'Gonorrhea', group: 'core', status: 'Curable', statusTone: 'curable', summary: 'Can infect the genitals, throat or rectum. Curable, but resistance is growing.' },
  { slug: 'syphilis', name: 'Syphilis', menuName: 'Syphilis', group: 'core', status: 'Curable', statusTone: 'curable', summary: 'Moves through stages. Easy to miss early and important to treat.' },
  { slug: 'hiv', name: 'HIV', menuName: 'HIV & AIDS', group: 'core', status: 'Manageable', statusTone: 'manageable', summary: 'Treatment lets people live long, healthy lives. PrEP and PEP prevent it.' },
  { slug: 'herpes', name: 'Genital herpes', menuName: 'Genital Herpes (HSV-1 / HSV-2)', group: 'core', status: 'Manageable', statusTone: 'manageable', summary: 'Very common, often unnoticed, and manageable with care from a clinician.' },
  { slug: 'hpv', name: 'HPV', menuName: 'HPV', group: 'core', status: 'Manageable', statusTone: 'manageable', summary: 'Very common and usually clears on its own. A vaccine helps prevent it.' },
  { slug: 'trichomoniasis', name: 'Trichomoniasis', menuName: 'Trichomoniasis', group: 'core', status: 'Curable', statusTone: 'curable', summary: 'Caused by a parasite and often left out of standard STD panels.' },
  { slug: 'hepatitis-b', name: 'Hepatitis B', menuName: 'Hepatitis B', group: 'more', status: 'Preventable', statusTone: 'manageable', summary: 'A liver infection that can spread through sex. A vaccine prevents it.' },
  { slug: 'hepatitis-c', name: 'Hepatitis C', menuName: 'Hepatitis C', group: 'more', status: 'Curable', statusTone: 'curable', summary: 'A liver infection found in many full STD panels. Curable in most people.' },
  { slug: 'mycoplasma-genitalium', name: 'Mycoplasma genitalium', menuName: 'Mycoplasma genitalium (Mgen)', group: 'more', status: 'Curable', statusTone: 'curable', summary: 'A less-known STI behind symptoms that continue after negative tests.' },
  { slug: 'bacterial-vaginosis', name: 'Bacterial vaginosis (BV)', menuName: 'Bacterial vaginosis (BV)', group: 'lookalike', status: 'Not an STD', statusTone: 'notsti', summary: 'A common imbalance of vaginal bacteria that can look like an STD.' },
  { slug: 'yeast-infection', name: 'Yeast infection', menuName: 'Yeast infection', group: 'lookalike', status: 'Not an STD', statusTone: 'notsti', summary: 'A common fungal infection that can feel like an STD.' },
];

export const conditionBySlug = Object.fromEntries(CONDITIONS.map((c) => [c.slug, c]));
