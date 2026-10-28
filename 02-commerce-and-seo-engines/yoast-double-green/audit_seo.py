import os
import requests, json

url = 'https://thechapmancollection.com/wp-json/wc/v3/products'
auth = ('neverrender-labs', os.getenv('WP_REST_APP_PASSWORD', ''))

all_products = []
page = 1
while True:
    r = requests.get(url, auth=auth, params={'per_page': 100, 'page': page, 'status': 'publish'})
    data = r.json()
    if not data or not isinstance(data, list):
        break
    all_products.extend(data)
    if len(data) < 100:
        break
    page += 1

with open(r'C:\Users\Saturn\.gemini\antigravity\brain\6bc72944-3e6d-4eee-bcc9-120072c5f5c2\scratch\all_wc_products.json', 'w', encoding='utf-8') as f:
    json.dump(all_products, f, indent=2)

print(f'Total published products: {len(all_products)}')

missing_kw = 0
missing_desc = 0
missing_title = 0
missing_tags = 0
missing_alt = 0
red_or_empty_linkdex = 0
grey_readability = 0
kw_counts = {}
em_dash_in_seo = 0

for p in all_products:
    meta = {m['key']: m['value'] for m in p.get('meta_data', [])}
    kw = str(meta.get('_yoast_wpseo_focuskw') or '').strip()
    desc = str(meta.get('_yoast_wpseo_metadesc') or '').strip()
    title = str(meta.get('_yoast_wpseo_title') or '').strip()
    linkdex = str(meta.get('_yoast_wpseo_linkdex') or '0')
    content_score = str(meta.get('_yoast_wpseo_content_score') or '0')
    if not kw: missing_kw += 1
    else: kw_counts[kw.lower()] = kw_counts.get(kw.lower(), []) + [(p['id'], p['name'])]
    if not desc: missing_desc += 1
    if not title: missing_title += 1
    if '—' in desc or '–' in desc or '—' in title or '–' in title or '—' in p['name'] or '–' in p['name'] or '—' in p.get('description','') or '–' in p.get('description',''):
        em_dash_in_seo += 1
    if not p.get('tags'): missing_tags += 1
    imgs = p.get('images', [])
    if any(not (img.get('alt') or '').strip() for img in imgs):
        missing_alt += 1
    if not linkdex.isdigit() or int(linkdex) < 70:
        red_or_empty_linkdex += 1
    if not content_score.isdigit() or int(content_score) < 70:
        grey_readability += 1

dups = {k: v for k, v in kw_counts.items() if len(v) > 1}
print(f'Missing Focus KW: {missing_kw}')
print(f'Missing Meta Desc: {missing_desc}')
print(f'Missing SEO Title: {missing_title}')
print(f'Missing Product Tags: {missing_tags}')
print(f'Missing Image Alt Text: {missing_alt}')
print(f'Products with Em/En-Dashes in Title/Desc/SEO: {em_dash_in_seo}')
print(f'Red/Unscored Yoast SEO dot (<70): {red_or_empty_linkdex}')
print(f'Grey/Red Yoast Readability dot (<70): {grey_readability}')
print(f'Duplicate Focus Keyphrases ({len(dups)}):')
for k, v in dups.items():
    print(f'  "{k}": {v}')

print('\n--- Newest 25 products ---')
for p in all_products[:25]:
    meta = {m['key']: m['value'] for m in p.get('meta_data', [])}
    kw = meta.get('_yoast_wpseo_focuskw', '')
    desc = meta.get('_yoast_wpseo_metadesc', '')
    title = meta.get('_yoast_wpseo_title', '')
    ld = meta.get('_yoast_wpseo_linkdex', '')
    cs = meta.get('_yoast_wpseo_content_score', '')
    tags = [t['name'] for t in p.get('tags', [])]
    print(f"ID {p['id']}: {p['name'][:42]} | KW: '{kw}' | Title: {bool(title)} | DescLen: {len(desc)} | Linkdex: '{ld}' | Read: '{cs}' | Tags: {len(tags)}")
