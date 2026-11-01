"""Builds content-plan/content-plan.csv: the revised article plan after the
no-medication-names rule. Run: python3 content-plan/build_plan.py <source.xlsx>"""
import csv, re, sys, openpyxl

SRC = sys.argv[1]
wb = openpyxl.load_workbook(SRC, read_only=True)
rows = list(wb['All Articles'].iter_rows(values_only=True))
head = rows[0]
data = [dict(zip(head, r)) for r in rows[1:] if r and r[0]]

DROP = {  # needs a medicine name, dose or brand to answer the query
 'CHL-049':'Medicine dosage', 'CHL-050':'Names antibiotics', 'CHL-051':'Missed-dose advice', 'CHL-055':'Medicine and alcohol interaction',
 'CHL-063':'Drug interactions', 'CHL-060':'Merged into HUB-030 (online STD care)',
 'GON-036':'About a specific injection', 'GON-037':'Names new drugs', 'GON-044':'Names antibiotics', 'GON-056':'Off-label vaccine use',
 'SYP-029':'Names alternative antibiotics', 'SYP-030':'About a drug shortage', 'SYP-034':'About a specific injection',
 'HPV-033':'Merged into HPV-032 (getting care for warts)', 'HPV-038':'Names drugs in development', 'HPV-052':'Vaccine side effects (medicine-specific)',
 'HPV-056':'Vaccine dose schedule', 'HPV-058':'Brand-name legal topic',
 'HSV-036':'Medicine dosage', 'HSV-037':'Daily medicine regimen', 'HSV-039':'OTC medicines', 'HSV-040':'Names drugs in development',
 'HSV-042':'Merged into HUB-030 (online STD care)',
 'HIV-036':'Names HIV medicines', 'HIV-039':'Names new medicines', 'HIV-051':'PrEP brand comparison', 'HIV-052':'PrEP brand page',
 'HIV-054':'Medicine side effects', 'HIV-055':'Dosing schedule', 'HIV-056':'Merged into HIV-050 (PrEP basics)', 'HIV-059':'Merged into HIV-057 (PEP)',
 'HIV-062':'Dosing before sex',
 'TRI-019':'Medicine side effects and alcohol',
 'HBV-021':'Post-exposure medicines', 'HBV-022':'Medicine-triggered reactivation', 'HBV-028':'Vaccine dose schedule', 'HBV-029':'Vaccine side effects',
 'HBV-030':'Vaccine dose schedule', 'HBV-031':'Vaccine booster dosing',
 'HUB-034':'Topic is an antibiotic regimen (doxy-PEP)',
}

REFRAME = {  # new H1 and query, no medicine names or doses
 'CHL-048':('Getting Treated for Chlamydia: What to Expect From Diagnosis to All-Clear','chlamydia treatment'),
 'CHL-052':('How Long Does Chlamydia Take to Go Away After Treatment?','how long does chlamydia take to go away'),
 'CHL-054':('How Long to Wait Before Having Sex After Chlamydia Treatment','how long after chlamydia treatment can i have sex'),
 'CHL-056':('Still Have Symptoms After Chlamydia Treatment? When to Go Back','chlamydia symptoms after treatment'),
 'CHL-057':('Chlamydia Came Back? Reinfection, Retesting and Next Steps','chlamydia treatment not working'),
 'CHL-058':('Pain After Chlamydia: When Symptoms Linger and When to See a Doctor','pain after chlamydia treatment'),
 'CHL-059':('Retesting After Chlamydia: When and Why','retest after chlamydia treatment'),
 'CHL-061':("Why Home Remedies and Online Antibiotics Don't Work for Chlamydia",'chlamydia treatment over the counter'),
 'CHL-062':('Is Chlamydia Becoming Harder to Treat? What We Know','chlamydia antibiotic resistance'),
 'GON-035':('Getting Treated for Gonorrhea: What to Expect at Your Visit','gonorrhea treatment'),
 'GON-040':('Still Have Symptoms After Gonorrhea Treatment? When to Go Back','gonorrhea symptoms after treatment'),
 'GON-041':('Retesting After Gonorrhea: Test of Cure and the 3-Month Retest','gonorrhea test of cure'),
 'GON-042':('Where to Get Seen for Gonorrhea Fast: Clinics, Urgent Care and Telehealth','where to get gonorrhea treatment'),
 'GON-043':("Why Home Remedies Don't Work for Gonorrhea",'gonorrhea home remedy'),
 'SYP-028':('Getting Treated for Syphilis: What to Expect and Follow-Up Tests','syphilis treatment'),
 'SYP-031':('Fever or Chills After Starting Syphilis Care: What It Means and When to Call','jarisch herxheimer reaction'),
 'SYP-032':('Follow-Up Blood Tests After Syphilis: When Your RPR Should Drop','syphilis follow up rpr'),
 'SYP-035':('How Long Do Syphilis Sores, Rashes and Hair Loss Take to Heal?','how long after syphilis treatment do symptoms go away'),
 'SYP-036':("Why Home Remedies and Self-Treatment Fail for Syphilis",'syphilis home remedy'),
 'HPV-032':('Getting Care for HPV: Warts, Abnormal Results and Follow-Up','hpv treatment'),
 'HPV-034':("Why You Shouldn't Use Over-the-Counter Wart Removers on Genital Warts",'otc genital wart treatment'),
 'HPV-035':('Do Genital Warts Come Back? What to Expect','genital warts come back'),
 'HPV-036':('LEEP Procedure: What to Expect, Recovery and Precautions','leep procedure'),
 'HPV-037':('Can You Clear HPV Faster? What the Evidence Says','how to clear hpv faster'),
 'HPV-039':('When Can You Have Sex Again After Genital Wart Removal?','sex after wart removal'),
 'HPV-049':('HPV Vaccine: Who Should Get It and How It Protects You','hpv vaccine'),
 'HSV-035':('Getting Care for Genital Herpes: What a Clinician Can Do','herpes treatment'),
 'HSV-038':('Herpes Outbreak Self-Care: Comfort, Hygiene and What to Avoid','how to heal herpes faster'),
 'HSV-046':('Frequent Herpes Outbreaks: Common Triggers and When to See Your Clinician','frequent herpes outbreaks'),
 'HSV-059':("How to Prevent Herpes: Condoms, Timing and What Doesn't Work",'how to prevent herpes'),
 'HIV-035':('Starting HIV Care: What to Expect After a Diagnosis','hiv treatment'),
 'HIV-038':('Paying for HIV Care: Insurance, Ryan White and ADAP','hiv treatment cost'),
 'HIV-050':('PrEP for HIV Prevention: What It Is, Who It Is For and How to Ask','prep'),
 'HIV-057':('HIV PEP: Emergency Medicine to Prevent HIV Within 72 Hours','hiv pep'),
 'HIV-063':('Can PrEP Fail? How Rare It Is and How to Stay Protected','prep failure'),
 'TRI-018':('Getting Treated for Trichomoniasis: What to Expect','trich treatment'),
 'TRI-023':('Trich Keeps Coming Back? Reinfection and Next Steps','trich treatment not working'),
 'TRI-024':("Why Home Remedies Don't Work for Trich",'trich home remedy'),
 'HBV-019':('Chronic Hepatitis B Care: Monitoring and What to Expect','hepatitis b treatment'),
 'HBV-027':('Hepatitis B Vaccine: Who Needs It and How Long It Protects','hepatitis b vaccine'),
 'HUB-030':('Online STD Care: How Telehealth Visits Work','online std treatment'),
 'CHL-032':('Best At-Home Chlamydia Tests: What to Look For','best at home chlamydia test'),
}

def retitle(t):
    t2 = t
    for a, b in [(', Testing and Treatment', ', Testing and Next Steps'), (' Testing and Safe Treatment', ' Testing and What to Expect'),
                 ('Risks and Safe Treatment', 'Risks and What to Expect'), ('Risks, Testing and Treatment', 'Risks and Testing'),
                 ('Signs and Treatment', 'Signs and When to Get Care'), ('Symptoms and Treatment', 'Symptoms and When to Get Care'),
                 ('Signs, Treatment and Testing', 'Signs and Testing'), ('Causes, Treatment and When', 'Causes and When'),
                 ('Testing, Window Period and Treatment', 'Testing and Window Period'), ('Testing, Vaccine and Treatment', 'Testing and Vaccine'),
                 (', Treatment and Living With It', ' and Living With It'),
                 ('Testing and Treatment to Protect', 'Testing to Protect'), ('Testing, Treatment and Prevention', 'Testing and Prevention'),
                 ('Testing, Prevention (PrEP and PEP) and Treatment', 'Testing and Prevention (PrEP and PEP)'),
                 ('How Well Treatment Works Today', 'What to Know Today'), ('How Fast Treatment Works', 'What to Know'),
                 ('What Treatment Can and Can\'t Undo', 'What Can and Can\'t Be Undone'), ('What Treatment Can and Can\'t Do', 'What Can and Can\'t Be Done'),
                 ('Reviewed by a Medical Expert', 'What to Look For'), ('Testing, Treatment', 'Testing'), (' and Treatment', ' and Next Steps')]:
        t2 = t2.replace(a, b)
    return t2

# Pages already written, by plan ID -> path
WRITTEN = {  # filled from src/content/articles
 'BV-001':'bacterial-vaginosis/index',
 'CHL-001':'chlamydia/index',
 'CHL-032':'chlamydia/at-home-test',
 'CHL-048':'chlamydia/treatment',
 'CHL-052':'chlamydia/how-long-to-go-away',
 'CHL-054':'chlamydia/sex-after-treatment',
 'CHL-056':'chlamydia/symptoms-after-treatment',
 'CHL-057':'chlamydia/reinfection',
 'CHL-058':'chlamydia/pain-after-treatment',
 'CHL-059':'chlamydia/retesting',
 'CHL-061':'chlamydia/home-remedies',
 'CHL-062':'chlamydia/antibiotic-resistance',
 'GDE-HUB':'guides/index',
 'GON-001':'gonorrhea/index',
 'GON-035':'gonorrhea/treatment',
 'GON-040':'gonorrhea/symptoms-after-treatment',
 'GON-041':'gonorrhea/test-of-cure',
 'GON-042':'gonorrhea/where-to-get-treated',
 'GON-043':'gonorrhea/home-remedies',
 'HBV-001':'hepatitis-b/index',
 'HBV-019':'hepatitis-b/treatment',
 'HBV-027':'hepatitis-b/vaccine',
 'HCV-001':'hepatitis-c/index',
 'HIV-001':'hiv/index',
 'HIV-035':'hiv/treatment',
 'HIV-038':'hiv/paying-for-care',
 'HIV-050':'hiv/prep',
 'HIV-057':'hiv/pep',
 'HIV-063':'hiv/prep-failure',
 'HPV-001':'hpv/index',
 'HPV-032':'hpv/treatment',
 'HPV-034':'hpv/otc-wart-removers',
 'HPV-035':'hpv/warts-come-back',
 'HPV-036':'hpv/leep',
 'HPV-037':'hpv/clear-faster',
 'HPV-039':'hpv/sex-after-wart-removal',
 'HPV-049':'hpv/vaccine',
 'HSV-001':'herpes/index',
 'HSV-035':'herpes/treatment',
 'HSV-038':'herpes/outbreak-self-care',
 'HSV-046':'herpes/frequent-outbreaks',
 'HSV-059':'herpes/prevention',
 'HUB-001':'guides/curable-stds',
 'HUB-004':'guides/std-symptoms-in-men',
 'HUB-005':'guides/std-symptoms-in-women',
 'HUB-006':'guides/stds-without-symptoms',
 'HUB-007':'guides/symptom-checker',
 'HUB-009':'mycoplasma-genitalium/index',
 'HUB-010':'std-testing/best-at-home-std-tests',
 'HUB-019':'std-testing/at-home-test-accuracy',
 'HUB-022':'std-testing/free-testing',
 'HUB-024':'std-testing/window-period',
 'HUB-025':'std-testing/when-to-test',
 'HUB-030':'std-testing/online-std-care',
 'HUB-031':'guides/telling-a-partner',
 'SYP-001':'syphilis/index',
 'SYP-028':'syphilis/treatment',
 'SYP-031':'syphilis/fever-after-treatment',
 'SYP-032':'syphilis/follow-up-rpr',
 'SYP-035':'syphilis/healing-time',
 'SYP-036':'syphilis/home-remedies',
 'TRI-001':'trichomoniasis/index',
 'TRI-018':'trichomoniasis/treatment',
 'TRI-023':'trichomoniasis/keeps-coming-back',
 'TRI-024':'trichomoniasis/home-remedies',
 'TST-HUB':'std-testing/index',
 'TST-RES':'std-testing/reading-results',
 'VVC-001':'yeast-infection/index',
}

out = []
for d in data:
    i = d['ID']; t = d['Article title (H1)']; q = d['Primary target query']
    if i in DROP:
        action, nt, nq, note = 'drop', '', '', DROP[i]
    elif i in REFRAME:
        action, (nt, nq), note = 'reframe', REFRAME[i], 'No medicine names or doses: what to expect, when to retest, partners, precautions'
    else:
        nt, nq = retitle(t), q
        action, note = ('retitle', 'Removed "treatment" promise from title') if nt != t else ('keep', '')
    out.append({'ID': i, 'Condition': d['Condition'], 'Cluster': d['Cluster'], 'Page type': d['Page type'], 'Priority': d['Priority'],
                'Action': action, 'Final title (H1)': nt, 'Primary query': nq, 'Original title': t, 'Note': note,
                'Questions to cover': '' if action == 'drop' else (d.get('Merged intents (answer as H2s / FAQs - not separate posts)') or ''),
                'Lead sources': d.get('Lead citation sources') or '',
                'Written': 'yes' if i in WRITTEN else '', 'Path': WRITTEN.get(i, '')})

NEW = [  # (ID, condition, cluster, type, priority, title, query, path-if-written)
 ('TST-RES','All STDs (hub pages)','Testing & kits','Cluster article','P1','How to Read Your STD Test Results: Positive, Negative, Reactive and More','how to read std test results','std-testing/reading-results'),
 ('TST-HUB','All STDs (hub pages)','Testing & kits','Cluster hub','P1','STD Testing: When, Where and How to Get Tested','std testing','std-testing/index'),
 ('GDE-HUB','All STDs (hub pages)','Guides','Cluster hub','P1','STD Guides: Symptoms, Partners, Prevention and Support','std guides','guides/index'),
 ('HCV-001','Hepatitis C','Pillar','Category page (pillar)','P1','Hepatitis C: How It Spreads, Testing and Why It\'s Curable','hepatitis c','hepatitis-c/index'),
 ('HCV-002','Hepatitis C','Transmission','Cluster article','P1','Can You Get Hepatitis C From Sex?','can you get hepatitis c from sex',''),
 ('HCV-003','Hepatitis C','Symptoms','Cluster article','P1','Hepatitis C Symptoms: Why Most People Have None','hepatitis c symptoms',''),
 ('HCV-004','Hepatitis C','Testing','Cluster hub','P1','Hepatitis C Testing: Antibody and RNA Tests Explained','hepatitis c test',''),
 ('HCV-005','Hepatitis C','Testing','Cluster article','P1','How to Read Hepatitis C Test Results','hepatitis c test results',''),
 ('HCV-006','Hepatitis C','Testing','Cluster article','P2','Hepatitis C Window Period: When to Test After Exposure','hepatitis c window period',''),
 ('HCV-007','Hepatitis C','Testing','Cluster article','P2','Who Should Get Tested for Hepatitis C?','hepatitis c screening',''),
 ('HCV-008','Hepatitis C','Testing','Product roundup (affiliate)','P2','At-Home Hepatitis C Tests: Options and Accuracy','at home hepatitis c test',''),
 ('HCV-009','Hepatitis C','Basics','Cluster article','P1','Is Hepatitis C Curable? What a Cure Means','is hepatitis c curable',''),
 ('HCV-010','Hepatitis C','Basics','Comparison article','P2','Acute vs Chronic Hepatitis C: What\'s the Difference?','acute vs chronic hepatitis c',''),
 ('HCV-011','Hepatitis C','Complications','Cluster article','P2','Hepatitis C and Liver Damage: Why Early Testing Matters','hepatitis c liver damage',''),
 ('HCV-012','Hepatitis C','Pregnancy','Cluster article','P2','Hepatitis C and Pregnancy: Testing and Protecting Your Baby','hepatitis c pregnancy',''),
 ('HCV-013','Hepatitis C','Partners & relationships','Cluster article','P2','My Partner Has Hepatitis C: How to Lower Your Risk','partner has hepatitis c',''),
 ('HCV-014','Hepatitis C','Next steps & wellbeing','Checklist article','P2','Just Diagnosed With Hepatitis C? What to Do Next','diagnosed with hepatitis c',''),
 ('HCV-015','Hepatitis C','Prevention','Cluster article','P2','Can You Get Hepatitis C Again After a Cure?','hepatitis c reinfection',''),
 ('MGN-002','Mycoplasma genitalium','Basics','Comparison article','P2','Mycoplasma Genitalium vs Chlamydia vs Gonorrhea: How They Differ','mycoplasma genitalium vs chlamydia',''),
 ('MGN-003','Mycoplasma genitalium','Symptoms','Cluster article','P2','Mycoplasma Genitalium Symptoms in Men','mycoplasma genitalium symptoms male',''),
 ('MGN-004','Mycoplasma genitalium','Symptoms','Cluster article','P2','Mycoplasma Genitalium Symptoms in Women','mycoplasma genitalium symptoms female',''),
 ('MGN-005','Mycoplasma genitalium','Testing','Cluster article','P2','Mycoplasma Genitalium Testing: Who Needs It and How It Works','mycoplasma genitalium test',''),
 ('MGN-006','Mycoplasma genitalium','Symptoms','Cluster article','P2','NGU (Non-Gonococcal Urethritis): Causes and When to Get Tested','ngu',''),
 ('MGN-007','Mycoplasma genitalium','Basics','Cluster article','P3','Why Mycoplasma Genitalium Is Hard to Treat: Resistance Explained','mycoplasma genitalium resistance',''),
 ('MGN-008','Mycoplasma genitalium','Partners & relationships','Cluster article','P3','Mycoplasma Genitalium and Partners: Testing and Retesting','mycoplasma genitalium partner',''),
 ('BV-001','Bacterial vaginosis','Pillar','Category page (pillar)','P1','Bacterial Vaginosis (BV): Symptoms, Causes and Testing','bacterial vaginosis','bacterial-vaginosis/index'),
 ('BV-002','Bacterial vaginosis','Basics','Cluster article','P1','Is BV an STD? How Sex Affects Bacterial Vaginosis','is bv an std',''),
 ('BV-003','Bacterial vaginosis','Basics','Comparison article','P1','BV vs Trichomoniasis: How to Tell the Difference','bv vs trich',''),
 ('BV-004','Bacterial vaginosis','Testing','Cluster article','P2','At-Home BV Tests: pH Strips, Lab Kits and Accuracy','at home bv test',''),
 ('BV-005','Bacterial vaginosis','Next steps & wellbeing','Cluster article','P2','Why BV Keeps Coming Back: Common Triggers and When to See a Doctor','recurrent bv',''),
 ('BV-006','Bacterial vaginosis','Pregnancy','Cluster article','P2','BV During Pregnancy: Risks and Why Testing Matters','bv pregnancy',''),
 ('VVC-001','Yeast infection','Pillar','Category page (pillar)','P1','Yeast Infection vs STD: Symptoms and When to Test','yeast infection vs std','yeast-infection/index'),
 ('VVC-002','Yeast infection','Basics','Comparison article','P1','Yeast Infection vs BV: How to Tell Them Apart','yeast infection vs bv',''),
 ('VVC-003','Yeast infection','Symptoms','Cluster article','P2','Male Yeast Infection or STD? Itching and Redness on the Penis','male yeast infection',''),
 ('VVC-004','Yeast infection','Next steps & wellbeing','Cluster article','P2','Recurring Yeast Infections: Triggers and When to See a Doctor','recurring yeast infections',''),
]
for (i, c, cl, ty, p, t, q, path) in NEW:
    out.append({'ID': i, 'Condition': c, 'Cluster': cl, 'Page type': ty, 'Priority': p, 'Action': 'new', 'Final title (H1)': t,
                'Primary query': q, 'Original title': '', 'Note': 'Added after original plan', 'Questions to cover': '', 'Lead sources': '', 'Written': 'yes' if path else '', 'Path': path})

with open('content-plan/content-plan.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader(); w.writerows(out)

from collections import Counter
c = Counter(o['Action'] for o in out)
live = [o for o in out if o['Action'] != 'drop']
print(dict(c), '| articles to publish:', len(live), '| written:', sum(1 for o in live if o['Written']))
