import os
import requests
auth = ('neverrender-labs', os.getenv('WP_REST_APP_PASSWORD', ''))
base_yoast = 'https://thechapmancollection.com/wp-json/yoast/v1/bulk_editor'
r3 = requests.post(f'{base_yoast}/update_scores', auth=auth, json={
    'items': [
        {'id': 3193, 'seo_title_score': 9, 'meta_description_score': 9},
        {'id': 10, 'seo_title_score': 9, 'meta_description_score': 9},
        {'id': 16, 'seo_title_score': 9, 'meta_description_score': 9},
        {'id': 374, 'seo_title_score': 9, 'meta_description_score': 9}
    ]
})
print('update_scores:', r3.status_code, r3.text)
