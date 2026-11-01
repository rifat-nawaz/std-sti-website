"""Helper used while writing articles: takes a short spec and writes a Markdown file with
validated frontmatter. Title, query, cluster and page type come from content-plan.csv."""
import csv, os, re, sys, textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, 'src/content/articles')
PLAN = {r['ID']: r for r in csv.DictReader(open(os.path.join(ROOT, 'content-plan/content-plan.csv')))}
DATE = '2026-11-01'

FOLDER = {'Chlamydia': 'chlamydia', 'Gonorrhea': 'gonorrhea', 'Syphilis': 'syphilis', 'HIV': 'hiv',
          'Genital Herpes': 'herpes', 'HPV': 'hpv', 'Trichomoniasis': 'trichomoniasis', 'Hepatitis B': 'hepatitis-b',
          'Hepatitis C': 'hepatitis-c', 'Mycoplasma genitalium': 'mycoplasma-genitalium',
          'Bacterial vaginosis': 'bacterial-vaginosis', 'Yeast infection': 'yeast-infection'}
TYPE = {'Category page (pillar)': 'pillar', 'Cluster hub': 'hub', 'Cluster article': 'article',
        'Comparison article': 'comparison', 'Product roundup (affiliate)': 'roundup', 'Brand review': 'review',
        'Checklist article': 'checklist', 'Data / statistics page': 'data', 'Data / chart page': 'data',
        'Interactive tool': 'tool', 'How-to guide': 'article', 'Cross-sell article': 'article'}

# Sources that have passed the external link check.
S = {
 'cdc-chl': ('Centers for Disease Control and Prevention', 'Sexually Transmitted Infections Treatment Guidelines, 2021: Chlamydial Infections', 2021, 'https://www.cdc.gov/std/treatment-guidelines/chlamydia.htm'),
 'cdc-gon': ('Centers for Disease Control and Prevention', 'Sexually Transmitted Infections Treatment Guidelines, 2021: Gonococcal Infections Among Adolescents and Adults', 2021, 'https://www.cdc.gov/std/treatment-guidelines/gonorrhea-adults.htm'),
 'cdc-syp': ('Centers for Disease Control and Prevention', 'Sexually Transmitted Infections Treatment Guidelines, 2021: Syphilis', 2021, 'https://www.cdc.gov/std/treatment-guidelines/syphilis.htm'),
 'cdc-hsv': ('Centers for Disease Control and Prevention', 'Sexually Transmitted Infections Treatment Guidelines, 2021: Genital Herpes', 2021, 'https://www.cdc.gov/std/treatment-guidelines/herpes.htm'),
 'cdc-tri': ('Centers for Disease Control and Prevention', 'Sexually Transmitted Infections Treatment Guidelines, 2021: Trichomoniasis', 2021, 'https://www.cdc.gov/std/treatment-guidelines/trichomoniasis.htm'),
 'cdc-tri-about': ('Centers for Disease Control and Prevention', 'About Trichomoniasis', 2024, 'https://www.cdc.gov/trichomoniasis/about/index.html'),
 'cdc-mgen': ('Centers for Disease Control and Prevention', 'Sexually Transmitted Infections Treatment Guidelines, 2021: Mycoplasma genitalium', 2021, 'https://www.cdc.gov/std/treatment-guidelines/mycoplasmagenitalium.htm'),
 'cdc-ngu': ('Centers for Disease Control and Prevention', 'Sexually Transmitted Infections Treatment Guidelines, 2021: Urethritis and Cervicitis', 2021, 'https://www.cdc.gov/std/treatment-guidelines/urethritis-and-cervicitis.htm'),
 'cdc-bv': ('Centers for Disease Control and Prevention', 'Sexually Transmitted Infections Treatment Guidelines, 2021: Bacterial Vaginosis', 2021, 'https://www.cdc.gov/std/treatment-guidelines/bv.htm'),
 'cdc-bv-about': ('Centers for Disease Control and Prevention', 'About Bacterial Vaginosis (BV)', 2024, 'https://www.cdc.gov/bacterial-vaginosis/about/index.html'),
 'cdc-cand-sym': ('Centers for Disease Control and Prevention', 'Symptoms of Candidiasis', 2024, 'https://www.cdc.gov/candidiasis/signs-symptoms/index.html'),
 'cdc-cand-test': ('Centers for Disease Control and Prevention', 'Testing and Diagnosis for Candidiasis', 2024, 'https://www.cdc.gov/candidiasis/testing/index.html'),
 'cdc-hcv-std': ('Centers for Disease Control and Prevention', 'Sexually Transmitted Infections Treatment Guidelines, 2021: Hepatitis C', 2021, 'https://www.cdc.gov/std/treatment-guidelines/hcv.htm'),
 'cdc-hcv-test': ('Centers for Disease Control and Prevention', 'Clinical Screening and Diagnosis for Hepatitis C', 2025, 'https://www.cdc.gov/hepatitis-c/hcp/diagnosis-testing/index.html'),
 'cdc-hcv-screen': ('Centers for Disease Control and Prevention', 'CDC Recommendations for Hepatitis C Screening Among Adults — United States, 2020', 2020, 'https://www.cdc.gov/mmwr/volumes/69/rr/rr6902a1.htm'),
 'cdc-hbv-test': ('Centers for Disease Control and Prevention', 'Clinical Testing and Diagnosis for Hepatitis B', 2024, 'https://www.cdc.gov/hepatitis-b/hcp/diagnosis-testing/index.html'),
 'cdc-hbv-screen': ('Centers for Disease Control and Prevention', 'Screening and Testing for Hepatitis B Virus Infection: CDC Recommendations, United States, 2023', 2023, 'https://www.cdc.gov/mmwr/volumes/72/rr/rr7201a1.htm'),
 'cdc-hbv-vax': ('Centers for Disease Control and Prevention', 'Universal Hepatitis B Vaccination in Adults Aged 19–59 Years: Updated Recommendations of the ACIP, 2022', 2022, 'https://www.cdc.gov/mmwr/volumes/71/wr/mm7113a1.htm'),
 'cdc-hiv-test': ('Centers for Disease Control and Prevention', 'Getting Tested for HIV', 2024, 'https://www.cdc.gov/hiv/testing/index.html'),
 'cdc-pep': ('Centers for Disease Control and Prevention', 'Antiretroviral Postexposure Prophylaxis After Sexual, Injection Drug Use, or Other Nonoccupational Exposure to HIV: CDC Recommendations, United States, 2025', 2025, 'https://www.cdc.gov/mmwr/volumes/74/rr/rr7401a1.htm'),
 'hivgov': ('HIV.gov (US Department of Health and Human Services)', 'What Are HIV and AIDS?', 2025, 'https://www.hiv.gov/hiv-basics/overview/about-hiv-and-aids/what-are-hiv-and-aids'),
 'cdc-hpv': ('Centers for Disease Control and Prevention', 'About HPV', 2024, 'https://www.cdc.gov/hpv/about/index.html'),
 'cdc-hpv-vax': ('Centers for Disease Control and Prevention', 'Human Papillomavirus Vaccination for Adults: Updated Recommendations of the ACIP (MMWR)', 2019, 'https://www.cdc.gov/mmwr/volumes/68/wr/mm6832a3.htm'),
 'cdc-sti': ('Centers for Disease Control and Prevention', 'Sexually Transmitted Infections Treatment Guidelines, 2021 (MMWR Recommendations and Reports)', 2021, 'https://www.cdc.gov/mmwr/volumes/70/rr/rr7004a1.htm'),
 'cdc-ept': ('Centers for Disease Control and Prevention', 'Expedited Partner Therapy', 2024, 'https://www.cdc.gov/sti/hcp/clinical-guidance/expedited-partner-therapy.html'),
 'cdc-surv': ('Centers for Disease Control and Prevention', 'Sexually Transmitted Disease Surveillance, 2023', 2024, 'https://stacks.cdc.gov/view/cdc/255132'),
 'cdc-nchs-hsv': ('National Center for Health Statistics (CDC)', 'Prevalence of Herpes Simplex Virus Type 1 and Type 2 in Persons Aged 14–49: United States, 2015–2016', 2018, 'https://www.cdc.gov/nchs/products/databriefs/db304.htm'),
 'gettested': ('Centers for Disease Control and Prevention', 'GetTested: National HIV, STD and Hepatitis Testing Locator', 2025, 'https://gettested.cdc.gov/'),
 'uspstf-ctng': ('US Preventive Services Task Force', 'Chlamydia and Gonorrhea: Screening', 2021, 'https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/chlamydia-and-gonorrhea-screening'),
 'uspstf-syp': ('US Preventive Services Task Force', 'Syphilis Infection in Nonpregnant Adolescents and Adults: Screening', 2022, 'https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/syphilis-infection-nonpregnant-adults-adolescents-screening'),
 'uspstf-hiv': ('US Preventive Services Task Force', 'Human Immunodeficiency Virus (HIV) Infection: Screening', 2019, 'https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/human-immunodeficiency-virus-hiv-infection-screening'),
 'uspstf-prep': ('US Preventive Services Task Force', 'Prevention of Human Immunodeficiency Virus (HIV) Infection: Pre-Exposure Prophylaxis', 2023, 'https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/prevention-of-human-immunodeficiency-virus-hiv-infection-pre-exposure-prophylaxis'),
 'uspstf-hcv': ('US Preventive Services Task Force', 'Hepatitis C Virus Infection in Adolescents and Adults: Screening', 2020, 'https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/hepatitis-c-screening'),
 'uspstf-cerv': ('US Preventive Services Task Force', 'Cervical Cancer: Screening', 2018, 'https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/cervical-cancer-screening'),
 'who-sti': ('World Health Organization', 'Sexually transmitted infections (STIs) fact sheet', 2025, 'https://www.who.int/news-room/fact-sheets/detail/sexually-transmitted-infections-(stis)'),
 'who-chl': ('World Health Organization', 'Chlamydia fact sheet', 2024, 'https://www.who.int/news-room/fact-sheets/detail/chlamydia'),
 'who-gon': ('World Health Organization', 'Gonorrhoea (Neisseria gonorrhoeae infection) fact sheet', 2024, 'https://www.who.int/news-room/fact-sheets/detail/gonorrhoea-(neisseria-gonorrhoeae-infection)'),
 'who-syp': ('World Health Organization', 'Syphilis fact sheet', 2025, 'https://www.who.int/news-room/fact-sheets/detail/syphilis'),
 'who-hiv': ('World Health Organization', 'HIV and AIDS fact sheet', 2025, 'https://www.who.int/news-room/fact-sheets/detail/hiv-aids'),
 'who-hsv': ('World Health Organization', 'Herpes simplex virus fact sheet', 2024, 'https://www.who.int/news-room/fact-sheets/detail/herpes-simplex-virus'),
 'who-tri': ('World Health Organization', 'Trichomoniasis fact sheet', 2023, 'https://www.who.int/news-room/fact-sheets/detail/trichomoniasis'),
 'who-hbv': ('World Health Organization', 'Hepatitis B fact sheet', 2025, 'https://www.who.int/news-room/fact-sheets/detail/hepatitis-b'),
 'who-cerv': ('World Health Organization', 'Cervical cancer fact sheet', 2025, 'https://www.who.int/news-room/fact-sheets/detail/cervical-cancer'),
 'medline': ('NIH MedlinePlus', 'Sexually Transmitted Infections', 2024, 'https://medlineplus.gov/sexuallytransmittedinfections.html'),
 'fda-ctng-home': ('US Food and Drug Administration', 'FDA Grants Marketing Authorization of First Test for Chlamydia and Gonorrhea with at-home Sample Collection', 2023, 'https://www.fda.gov/news-events/press-announcements/fda-grants-marketing-authorization-first-test-chlamydia-and-gonorrhea-home-sample-collection'),
 'fda-visby': ('US Food and Drug Administration', 'FDA Grants Marketing Authorization of First Home Test for Chlamydia, Gonorrhea and Trichomoniasis', 2025, 'https://www.fda.gov/news-events/press-announcements/fda-grants-marketing-authorization-first-home-test-chlamydia-gonorrhea-and-trichomoniasis'),
 'fda-syp-home': ('US Food and Drug Administration', 'FDA Marketing Authorization Enables Increased Access to First Step of Syphilis Diagnosis', 2024, 'https://www.fda.gov/news-events/press-announcements/fda-marketing-authorization-enables-increased-access-first-step-syphilis-diagnosis'),
 'fda-rx': ('US Food and Drug Administration', 'BeSafeRx: Your Source for Online Pharmacy Information', 2025, 'https://www.fda.gov/drugs/buying-using-medicine-safely/besaferx-your-source-online-pharmacy-information'),
 'hcgov': ('HealthCare.gov', 'Preventive care benefits for adults', 2025, 'https://www.healthcare.gov/preventive-care-adults/'),
 'hrsa-hc': ('Health Resources and Services Administration', 'Find a Health Center', 2025, 'https://findahealthcenter.hrsa.gov/'),
 'ryanwhite': ('Health Resources and Services Administration', 'Ryan White HIV/AIDS Program', 2025, 'https://ryanwhite.hrsa.gov/'),
 'ndvh': ('National Domestic Violence Hotline', 'Get help 24/7', 2025, 'https://www.thehotline.org/'),
}
EXTRA = {}  # new sources added in a batch: key -> tuple; checked in CI after push

def q(s):  # YAML double-quoted string
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

def existing():
    out = set()
    for d, _, fs in os.walk(ART):
        for f in fs:
            if f.endswith('.md'):
                out.add(os.path.relpath(os.path.join(d, f), ART)[:-3])
    return out

PENDING = set()  # paths written in this batch (allowed as related)

def art(id, slug, desc, answer, takeaways, src, body, faq=(), related=(), risk='standard', aff='light',
        offer='k1', seo=None, title=None, folder=None, tool=None):
    p = PLAN[id]
    title = title or p['Final title (H1)']
    seo = seo or title
    folder = folder or FOLDER.get(p['Condition']) or ('std-testing' if p['Cluster'] in ('Testing & kits',) else 'guides')
    path = f'{folder}/{slug}'
    errs = []
    if len(title) > 110: errs.append(f'title {len(title)}')
    if len(seo) > 70: errs.append(f'seoTitle {len(seo)} "{seo}"')
    if not 70 <= len(desc) <= 170: errs.append(f'description {len(desc)}')
    srcs = [S.get(k) or EXTRA.get(k) for k in src]
    if None in srcs or len(srcs) < 2: errs.append(f'sources {src}')
    have = existing() | PENDING
    warn = []
    for r in related:
        if r not in have: warn.append(f'related not yet written: {r}')
    if re.search(r'\]\(/[^)]*/index/', body + answer): errs.append('link ends in /index/')
    for m in re.findall(r'\]\((/[^)#]*)', body + answer):
        t = m.strip('/'); t = t if t else 'index'
        if t not in have and t + '/index' not in have and t not in ('knowledge-care', 'conditions', 'about', 'contact', 'editorial-policy', 'editorial-team', 'how-we-make-money', 'privacy', 'terms', 'medical-disclaimer', 'health-data-notice', 'accessibility'):
            warn.append(f'link not yet written: {m}')
    fp = os.path.join(ART, path + '.md')
    if os.path.exists(fp): errs.append('exists')
    if errs:
        print(f'SKIP {id} {path}: ' + '; '.join(errs)); return
    pt = TYPE.get(p['Page type'], 'article')
    if p['Page type'].startswith('Cluster article'): pt = 'article'
    if p['Page type'].startswith('HowTo'): pt = 'article'
    L = ['---', f'ref: {id}', f'title: {q(title)}', f'seoTitle: {q(seo)}', f'description: {q(desc)}',
         f'cluster: {q(p["Cluster"])}', f'pageType: {pt}', f'primaryQuery: {q(p["Primary query"])}',
         f'riskLevel: {risk}', f'affiliate: {aff}']
    if aff != 'none': L.append(f'offer: {offer}')
    if tool: L.append(f'tool: {tool}')
    L.append(f'answer: {q(answer)}')
    L.append('takeaways:'); L += [f'  - {q(t)}' for t in takeaways]
    if faq:
        L.append('faq:')
        for a, b in faq: L += [f'  - q: {q(a)}', f'    a: {q(b)}']
    L.append('sources:')
    for (pub, t, y, u) in srcs:
        L += [f'  - publisher: {q(pub)}', f'    title: {q(t)}', f'    year: {y}', f'    url: {q(u)}']
    L.append('related:' + ('' if related else ' []'))
    L += [f'  - {r}' for r in related]
    L += [f'published: {DATE}', f'updated: {DATE}', '---', '', textwrap.dedent(body).strip(), '']
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w').write('\n'.join(L))
    PENDING.add(path)
    print(f'ok {id} -> /{path}/' + (('  [' + '; '.join(warn) + ']') if warn else ''))
