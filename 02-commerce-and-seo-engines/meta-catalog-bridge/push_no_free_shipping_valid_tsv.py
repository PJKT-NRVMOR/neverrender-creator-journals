import os
import json
import base64
import urllib.request

WP_BASE = "https://thechapmancollection.com/wp-json"
USER = "neverrender-labs"
APP_PASS = os.getenv("WP_REST_APP_PASSWORD", "")
AUTH_HEADER = "Basic " + base64.b64encode(f"{USER}:{APP_PASS}".encode("utf-8")).decode("utf-8")


def api_request(url, method="GET", data=None):
    headers = {
        "Authorization": AUTH_HEADER,
        "User-Agent": "NRL-WooCommerce-Inspector/1.0",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else {"empty_raw": raw}


php_code = r"""
function nrl_write_no_free_shipping_meta_tsv() {
    $non_us_zones = array();
    if (function_exists('WC') && WC()->countries) {
        foreach (array_keys(WC()->countries->get_countries()) as $cc) {
            if ('US' === $cc) {
                continue;
            }
            $non_us_zones[] = array(
                'country' => $cc,
                'states' => array(),
                'applies_to_entire_country' => true,
            );
        }
    }

    $rows = array(
        array(
            'shipping_profile_id' => '1-all_products',
            'name' => 'US 50 states',
            'shipping_zones' => wp_json_encode(array(
                array(
                    'country' => 'US',
                    'states' => array(),
                    'applies_to_entire_country' => true,
                ),
            )),
            'shipping_rates' => wp_json_encode(array(
                array(
                    'name' => 'Client-Arranged White-Glove Shipping (Coordinated Post-Purchase)',
                    'has_free_shipping' => 'false',
                ),
            )),
            'applies_to_all_products' => 'true',
            'applicable_products_filter' => '',
            'applies_to_rest_of_world' => 'false',
        ),
        array(
            'shipping_profile_id' => '2-all_products',
            'name' => 'Everywhere',
            'shipping_zones' => wp_json_encode($non_us_zones),
            'shipping_rates' => wp_json_encode(array(
                array(
                    'name' => 'Client-Arranged International White-Glove Shipping',
                    'has_free_shipping' => 'false',
                ),
            )),
            'applies_to_all_products' => 'true',
            'applicable_products_filter' => '',
            'applies_to_rest_of_world' => 'false',
        ),
    );

    $writer = new \WooCommerce\Facebook\Feed\CsvFeedFileWriter(
        \WooCommerce\Facebook\Feed\FeedManager::SHIPPING_PROFILES,
        \WooCommerce\Facebook\Feed\ShippingProfilesFeed::SHIPPING_PROFILES_FEED_HEADER,
        "\t"
    );
    $writer->create_feed_directory();
    $writer->create_files_to_protect_feed_directory();
    $file_path = $writer->get_file_path();

    $headers = array(
        'shipping_profile_id',
        'name',
        'shipping_zones',
        'shipping_rates',
        'applies_to_all_products',
        'applicable_products_filter',
        'applies_to_rest_of_world',
    );

    $fp = fopen($file_path, 'w');
    if ($fp) {
        fputcsv($fp, $headers, "\t", '"', "\\");
        foreach ($rows as $r) {
            $line = array();
            foreach ($headers as $h) {
                $line[] = $r[$h] ?? '';
            }
            fputcsv($fp, $line, "\t", '"', "\\");
        }
        fclose($fp);
    }
    return $file_path;
}

add_action('woocommerce_api_wc_facebook_get_feed_data_shipping_profiles', function () {
    try {
        nocache_headers();
        nrl_write_no_free_shipping_meta_tsv();
        update_option('nrl_last_fb_shipping_feed_pull', array(
            'time' => current_time('mysql'),
            'ua'   => $_SERVER['HTTP_USER_AGENT'] ?? '',
            'ip'   => $_SERVER['REMOTE_ADDR'] ?? '',
        ));
    } catch (\Throwable $t) {
    }
}, 1);

add_action('rest_api_init', function () {
    register_rest_route('nrl/v1', '/fb-shipping-push-nofree', array(
        'methods' => 'GET',
        'permission_callback' => function () { return current_user_can('manage_options'); },
        'callback' => function ($request) {
            $file_path = nrl_write_no_free_shipping_meta_tsv();
            $cpi_id = get_option('wc_facebook_commerce_partner_integration_id');
            $secret = get_option('wc_facebook_feed_url_secret_shipping_profiles', '');
            $feed_url = add_query_arg(
                array(
                    'wc-api' => 'wc_facebook_get_feed_data_shipping_profiles',
                    'secret' => $secret,
                    'v'      => time(),
                ),
                home_url('/')
            );
            $upload_data = array(
                'url'         => $feed_url,
                'feed_type'   => 'SHIPPING_PROFILES',
                'update_type' => 'CREATE',
            );
            $res = facebook_for_woocommerce()->get_api()->create_common_data_feed_upload($cpi_id, $upload_data);
            sleep(6);
            return array(
                'head_preview' => file_exists($file_path) ? substr(file_get_contents($file_path), 0, 500) : '',
                'api_response' => $res->response_data ?? (string) $res,
                'last_pull'    => get_option('nrl_last_fb_shipping_feed_pull'),
            );
        }
    ));
});
"""

upd = api_request(
    f"{WP_BASE}/code-snippets/v1/snippets/16",
    method="PUT",
    data={
        "name": "Meta Commerce Shipping Profile Feed Override (No Free Shipping Badge)",
        "code": php_code,
        "scope": "global",
        "active": True,
    }
)
print("Updated Snippet 16:", upd.get("id"))
info = api_request(f"{WP_BASE}/nrl/v1/fb-shipping-push-nofree")
print(json.dumps(info, indent=2))
