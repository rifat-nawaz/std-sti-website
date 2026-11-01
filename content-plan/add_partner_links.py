"""Adds one natural in-text partner link to articles that offer partner links but don't
mention a home test in their text. Inserted at the end of the first testing-related section.
Safe to rerun: skips files that already contain a /go/ link."""
import glob, re, zlib, os, sys
NO_OFFER = {'HIV-057', 'HIV-058', 'HIV-066', 'HIV-067', 'HIV-069', 'HUB-036', 'HUB-039', 'CHL-087'}
PHRASE = re.compile(r"\b(lab-processed (?:home |at-home )?(?:test )?kits?|at-home (?:\w+ )?(?:test(?:ing)? )?kits?|at-home (?:\w+ )?tests?|home (?:test )?kits?|mail-in (?:lab )?kits?|home tests?|home testing|test at home|testing at home)\b", re.I)
VARIANTS = [
 "If you'd rather test privately, a [lab-processed home kit](/go/{o}/) uses the same type of lab test as a clinic.",
 "Prefer to test at home? A [lab-processed home test](/go/{o}/) lets you collect a sample in private and get results online.",
 "You can also order a [home test kit](/go/{o}/), collect your sample yourself and mail it to a certified lab.",
 "For privacy and convenience, an [at-home test kit](/go/{o}/) processed by a certified lab is another option.",
]
HEAD = re.compile(r'^## .*(test|Test|What to do|Next step|next step|Get checked|Who should|Screening|Prevention|When to)', re.M)
changed = skipped = 0
for f in sorted(glob.glob('src/content/articles/**/*.md', recursive=True)):
    s = open(f).read()
    fm, body = s.split('\n---\n', 1)
    ref = re.search(r'^ref: (\S+)', fm, re.M).group(1)
    aff = re.search(r'^affiliate: (\S+)', fm, re.M)
    if not aff or aff.group(1) == 'none' or ref in NO_OFFER or ref.startswith('HSV-') or '](/go/' in body:
        continue
    # Already has a natural phrase in a paragraph or list? The build step links it.
    prose_lines = [l for l in body.split('\n') if l.strip() and not l.lstrip().startswith(('|', '#', '>'))]
    if any(PHRASE.search(l) for l in prose_lines):
        continue
    offer = (re.search(r'^offer: (\S+)', fm, re.M) or [None, 'k1'])[1]
    m = HEAD.search(body)
    sentence = VARIANTS[zlib.crc32(ref.encode()) % len(VARIANTS)].format(o=offer)
    if m:
        nxt = re.search(r'^## ', body[m.end():], re.M)
        end = m.end() + nxt.start() if nxt else len(body)
        sect = body[m.end():end].rstrip('\n')
        body = body[:m.end()] + sect + '\n\n' + sentence + '\n\n' + body[end:].lstrip('\n')
    else:
        # No testing section: add after the first section.
        first = re.search(r'^## ', body, re.M)
        nxt = re.search(r'^## ', body[first.end():], re.M) if first else None
        if not nxt:
            body = body.rstrip('\n') + '\n\n' + sentence + '\n'
        else:
            end = first.end() + nxt.start()
            body = body[:end].rstrip('\n') + '\n\n' + sentence + '\n\n' + body[end:]
    open(f, 'w').write(fm + '\n---\n' + body)
    changed += 1
print('added links to', changed, 'articles')
