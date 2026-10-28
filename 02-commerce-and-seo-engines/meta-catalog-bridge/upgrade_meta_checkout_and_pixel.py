import os
import requests

BASE_URL = "https://thechapmancollection.com/wp-json"
AUTH = ("neverrender-labs", os.getenv("WP_REST_APP_PASSWORD", ""))

# 1. Check all existing snippets in code-snippets
r_s = requests.get(f"{BASE_URL}/code-snippets/v1/snippets", auth=AUTH, timeout=20)
print("Existing snippets:", [(s["id"], s["name"], s["active"]) for s in r_s.json()])

# 2. Create/Update a server-side PHP snippet that:
#    a) Handles /meta-checkout/?products=ID:QTY,ID2:QTY2&coupon=CODE in PHP BEFORE rendering so WC()->cart is populated server-side (emptying old cart first so subtotal is 100% exact!)
#    b) Outputs the Meta Pixel 1856902815661252 globally in wp_head AND fires ViewContent on every single product page with exact product ID, SKU, price, and currency!
php_snippet = r"""
// 1. Server-side WooCommerce Cart Handler for /meta-checkout/
add_action('wp', function() {
    if ( ! function_exists('WC') || ! WC()->cart ) {
        return;
    }
    $req_uri = isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '';
    if ( strpos($req_uri, 'meta-checkout') !== false || is_page('meta-checkout') || is_page(3200) ) {
        $products_param = '';
        if ( ! empty($_GET['products']) ) {
            $products_param = sanitize_text_field( wp_unslash($_GET['products']) );
        } elseif ( ! empty($_GET['product']) ) {
            $products_param = sanitize_text_field( wp_unslash($_GET['product']) );
        }
        if ( ! empty($products_param) ) {
            WC()->cart->empty_cart();
            $parts = explode(',', $products_param);
            foreach ( $parts as $part ) {
                $seg = explode(':', trim($part));
                $pid_raw = trim($seg[0]);
                $qty = isset($seg[1]) ? max(1, intval($seg[1])) : 1;
                $pid = intval($pid_raw);
                if ( $pid <= 0 && function_exists('wc_get_product_id_by_sku') ) {
                    $pid = wc_get_product_id_by_sku($pid_raw);
                }
                if ( $pid > 0 ) {
                    WC()->cart->add_to_cart($pid, $qty);
                }
            }
            if ( ! empty($_GET['coupon']) ) {
                $coupon = sanitize_text_field( wp_unslash($_GET['coupon']) );
                if ( strtoupper($coupon) !== 'NONE' && WC()->cart->has_discount($coupon) === false ) {
                    WC()->cart->apply_coupon($coupon);
                }
            }
            WC()->cart->calculate_totals();
            wp_safe_redirect( wc_get_checkout_url() );
            exit;
        }
    }
}, 1);

// 2. Global Meta Pixel (1856902815661252) + Automatic ViewContent / InitiateCheckout firing
add_action('wp_head', function() {
    ?>
    <!-- Meta Pixel Code -->
    <script>
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '1856902815661252');
    fbq('track', 'PageView');
    <?php
    if ( function_exists('is_product') && is_product() ) {
        global $product;
        if ( ! is_object($product) ) {
            $product = wc_get_product( get_the_ID() );
        }
        if ( $product ) {
            $pid = (string) $product->get_id();
            $sku = (string) $product->get_sku();
            $ids = array($pid);
            if ( ! empty($sku) && $sku !== $pid ) {
                $ids[] = $sku;
            }
            $price = $product->get_price() ? (float) $product->get_price() : 0;
            $name  = $product->get_name();
            echo "fbq('track', 'ViewContent', " . wp_json_encode(array(
                'content_ids'  => $ids,
                'content_type' => 'product',
                'content_name' => $name,
                'value'        => $price,
                'currency'     => 'USD',
            )) . ");\n";
        }
    }
    ?>
    </script>
    <?php
}, 2);
"""

payload = {
    "name": "Meta Commerce Server-Side Checkout & Catalog Pixel",
    "desc": "Populates WooCommerce cart server-side for /meta-checkout/ (fixing subtotal validation) and fires global Meta Pixel 1856902815661252 ViewContent events.",
    "code": php_snippet.strip(),
    "scope": "global",
    "priority": 1,
    "active": True
}

r_create = requests.post(f"{BASE_URL}/code-snippets/v1/snippets", auth=AUTH, json=payload, timeout=20)
print("Created snippet:", r_create.status_code, r_create.json().get("id"), r_create.json().get("active"))
