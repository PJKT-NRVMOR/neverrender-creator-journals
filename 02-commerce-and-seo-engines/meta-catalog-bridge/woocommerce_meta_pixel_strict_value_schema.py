import os
import json
import base64
import urllib.request
from dotenv import load_dotenv

load_dotenv()

WP_BASE = os.getenv("WP_BASE_URL", "https://thechapmancollection.com/wp-json")
USER = os.getenv("WP_REST_USER", "")
APP_PASS = os.getenv("WP_REST_APP_PASSWORD", "")
PIXEL_ID = os.getenv("META_PIXEL_ID", "1856902815661252")
SNIPPET_ID = int(os.getenv("META_PIXEL_SNIPPET_ID", "6"))


def api_request(url, method="GET", data=None):
    auth_header = "Basic " + base64.b64encode(f"{USER}:{APP_PASS}".encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": auth_header,
        "User-Agent": "NRL-Meta-Pixel-Schema-Engine/1.0",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=45) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else {"empty_raw": raw}


def build_pixel_snippet(pixel_id: str) -> str:
    return f"""
// 1. Server-side WooCommerce Cart Handler for /meta-checkout/
add_action('wp', function() {{
    if ( ! function_exists('WC') || ! WC()->cart ) {{
        return;
    }}
    $req_uri = isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '';
    if ( strpos($req_uri, 'meta-checkout') !== false || is_page('meta-checkout') ) {{
        $products_param = '';
        if ( ! empty($_GET['products']) ) {{
            $products_param = sanitize_text_field( wp_unslash($_GET['products']) );
        }} elseif ( ! empty($_GET['product']) ) {{
            $products_param = sanitize_text_field( wp_unslash($_GET['product']) );
        }}
        if ( ! empty($products_param) ) {{
            WC()->cart->empty_cart();
            $parts = explode(',', $products_param);
            foreach ( $parts as $part ) {{
                $seg = explode(':', trim($part));
                $pid_raw = trim($seg[0]);
                $qty = isset($seg[1]) ? max(1, intval($seg[1])) : 1;
                $pid = intval($pid_raw);
                if ( $pid <= 0 && function_exists('wc_get_product_id_by_sku') ) {{
                    $pid = wc_get_product_id_by_sku($pid_raw);
                }}
                if ( $pid > 0 ) {{
                    WC()->cart->add_to_cart($pid, $qty);
                }}
            }}
            if ( ! empty($_GET['coupon']) ) {{
                $coupon = sanitize_text_field( wp_unslash($_GET['coupon']) );
                if ( strtoupper($coupon) !== 'NONE' && WC()->cart->has_discount($coupon) === false ) {{
                    WC()->cart->apply_coupon($coupon);
                }}
            }}
            WC()->cart->calculate_totals();
            wp_safe_redirect( wc_get_checkout_url() );
            exit;
        }}
    }}
}}, 1);

// 2. Global Meta Pixel ({pixel_id}) + Strict Value/Price Schema for ViewContent, AddToCart, InitiateCheckout & Purchase
add_action('wp_head', function() {{
    ?>
    <!-- Meta Pixel Code (NRL Strict Value & Item Price Schema) -->
    <script>
    !function(f,b,e,v,n,t,s)
    {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('set', 'autoConfig', false, '{pixel_id}');
    fbq('init', '{pixel_id}');
    fbq('track', 'PageView');
    <?php
    if ( function_exists('is_product') && is_product() ) {{
        global $product;
        if ( ! is_object($product) ) {{
            $product = wc_get_product( get_the_ID() );
        }}
        if ( $product ) {{
            $pid   = (string) $product->get_id();
            $sku   = (string) $product->get_sku();
            $ids   = array($pid);
            if ( ! empty($sku) && $sku !== $pid ) {{
                $ids[] = $sku;
            }}
            $raw_price = $product->get_price();
            if ( $raw_price === '' || $raw_price === null ) {{
                $raw_price = $product->get_regular_price();
            }}
            $price = round( max( 0.01, (float) $raw_price ), 2 );
            $name  = $product->get_name();
            $primary_id = ! empty($sku) ? $sku : $pid;
            $vc_payload = array(
                'content_ids'  => $ids,
                'content_type' => 'product',
                'content_name' => $name,
                'value'        => $price,
                'currency'     => 'USD',
                'contents'     => array(
                    array(
                        'id'         => $primary_id,
                        'quantity'   => 1,
                        'item_price' => $price,
                    ),
                ),
            );
            echo "var nrlProductPixelData = " . wp_json_encode($vc_payload) . ";\\n";
            echo "fbq('track', 'ViewContent', nrlProductPixelData);\\n";
            echo "document.addEventListener('DOMContentLoaded', function() {{\\n";
            echo "  var btn = document.querySelector('button.single_add_to_cart_button');\\n";
            echo "  if (btn) {{\\n";
            echo "    btn.addEventListener('click', function() {{\\n";
            echo "      fbq('track', 'AddToCart', nrlProductPixelData);\\n";
            echo "    }});\\n";
            echo "  }}\\n";
            echo "}});\\n";
        }}
    }}

    if ( function_exists('is_checkout') && is_checkout() && ( ! function_exists('is_order_received_page') || ! is_order_received_page() ) && function_exists('WC') && WC()->cart ) {{
        $cart_items = WC()->cart->get_cart();
        if ( ! empty($cart_items) ) {{
            $c_ids      = array();
            $contents   = array();
            $calc_total = 0.0;
            $num_items  = 0;
            foreach ( $cart_items as $item ) {{
                $p = isset($item['data']) ? $item['data'] : null;
                if ( $p && is_object($p) ) {{
                    $pid = (string) $p->get_id();
                    $sku = (string) $p->get_sku();
                    $id_str = ! empty($sku) ? $sku : $pid;
                    $qty = max(1, (int) $item['quantity']);
                    $unit_price = round( max( 0.01, (float) $p->get_price() ), 2 );
                    $c_ids[] = $id_str;
                    $contents[] = array(
                        'id'         => $id_str,
                        'quantity'   => $qty,
                        'item_price' => $unit_price,
                    );
                    $calc_total += ($unit_price * $qty);
                    $num_items  += $qty;
                }}
            }}
            $cart_val = (float) WC()->cart->get_total('edit');
            if ( $cart_val <= 0 ) {{
                $cart_val = $calc_total;
            }}
            $cart_val = round( max( 0.01, $cart_val ), 2 );
            $ic_payload = array(
                'content_ids'  => $c_ids,
                'content_type' => 'product',
                'value'        => $cart_val,
                'currency'     => 'USD',
                'num_items'    => max(1, $num_items),
                'contents'     => $contents,
            );
            echo "fbq('track', 'InitiateCheckout', " . wp_json_encode($ic_payload) . ");\\n";
        }}
    }}

    if ( function_exists('is_order_received_page') && is_order_received_page() ) {{
        global $wp;
        $order_id = isset($wp->query_vars['order-received']) ? absint($wp->query_vars['order-received']) : 0;
        if ( $order_id > 0 && function_exists('wc_get_order') ) {{
            $order = wc_get_order($order_id);
            if ( $order ) {{
                $c_ids      = array();
                $contents   = array();
                $calc_total = 0.0;
                $num_items  = 0;
                foreach ( $order->get_items() as $item ) {{
                    $p = $item->get_product();
                    $qty = max(1, (int) $item->get_quantity());
                    $line_total = (float) $item->get_total();
                    $unit_price = $qty > 0 ? round( max( 0.01, $line_total / $qty ), 2 ) : 0.01;
                    $id_str = $p ? ( $p->get_sku() ? (string) $p->get_sku() : (string) $p->get_id() ) : (string) $item->get_product_id();
                    $c_ids[] = $id_str;
                    $contents[] = array(
                        'id'         => $id_str,
                        'quantity'   => $qty,
                        'item_price' => $unit_price,
                    );
                    $calc_total += ($unit_price * $qty);
                    $num_items  += $qty;
                }}
                $order_val = (float) $order->get_total();
                if ( $order_val <= 0 ) {{
                    $order_val = $calc_total;
                }}
                $order_val = round( max( 0.01, $order_val ), 2 );
                $purchase_payload = array(
                    'content_ids'  => $c_ids,
                    'content_type' => 'product',
                    'value'        => $order_val,
                    'currency'     => 'USD',
                    'num_items'    => max(1, $num_items),
                    'contents'     => $contents,
                    'order_id'     => (string) $order_id,
                );
                $event_id = 'purchase_' . $order_id;
                echo "fbq('track', 'Purchase', " . wp_json_encode($purchase_payload) . ", {{eventID: " . wp_json_encode($event_id) . "}});\\n";
            }}
        }}
    }}
    ?>
    </script>
    <?php
}}, 2);
""".strip()


if __name__ == "__main__":
    payload = {
        "name": "Meta Commerce Server-Side Checkout & Catalog Pixel",
        "desc": "Populates WooCommerce cart server-side for /meta-checkout/ and fires Meta Pixel events with strict value, currency, and contents[].item_price schema.",
        "code": build_pixel_snippet(PIXEL_ID),
        "scope": "global",
        "priority": 1,
        "active": True,
    }
    res = api_request(f"{WP_BASE}/code-snippets/v1/snippets/{SNIPPET_ID}", method="PUT", data=payload)
    print("Updated Snippet:", res.get("id"), "Active:", res.get("active"))
