import os
import requests
auth = ('neverrender-labs', os.getenv('WP_REST_APP_PASSWORD', ''))
for ct in ['product', 'page']:
    for ep in ['seo_scores', 'readability_scores']:
        r = requests.get(f'https://thechapmancollection.com/wp-json/yoast/v1/{ep}', auth=auth, params={'contentType': ct})
        print(ct, ep, r.json())
