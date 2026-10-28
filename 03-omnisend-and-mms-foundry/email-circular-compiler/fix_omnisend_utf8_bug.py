import glob

files = glob.glob(r'C:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\drafts-for-chapman-marshall-college-approval\2026-10-23-*Omnisend*.html')
for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
    html = html.replace('’', '&#8217;').replace('‘', '&#8216;').replace('“', '&#8220;').replace('”', '&#8221;').replace('″', '&#8243;').replace('′', '&#8242;')
    non_ascii = [c for c in html if ord(c) >= 128]
    assert len(non_ascii) == 0, f"Found non-ascii: {non_ascii}"
    with open(fp, 'w', encoding='ascii') as f:
        f.write(html)
    print("100% pure ASCII verified:", fp.split('\\')[-1], "bytes == chars:", len(html) == len(html.encode('utf-8')))
