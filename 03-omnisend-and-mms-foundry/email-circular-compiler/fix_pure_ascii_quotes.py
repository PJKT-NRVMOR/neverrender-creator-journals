import glob

files = glob.glob(r'C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\drafts-for-chapman-marshall-college-approval\2026-10-23-*Omnisend*.html')
for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
    html = (
        html.replace('&#8217;', "'")
            .replace('&#8216;', "'")
            .replace('&#8220;', '"')
            .replace('&#8221;', '"')
            .replace('&#8243;', '"')
            .replace('&#8242;', "'")
            .replace('’', "'")
            .replace('‘', "'")
            .replace('“', '"')
            .replace('”', '"')
            .replace('″', '"')
            .replace('′', "'")
    )
    assert '&#' not in html, "Found numeric HTML entity!"
    assert all(ord(c) < 128 for c in html), "Found non-ASCII char!"
    with open(fp, 'w', encoding='ascii') as f:
        f.write(html)
    print("Clean 1-byte ASCII (zero numeric entities, zero UTF-8 multibyte):", fp.split('\\')[-1])
