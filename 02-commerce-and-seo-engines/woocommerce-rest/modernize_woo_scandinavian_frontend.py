#!/usr/bin/env python3
"""
Modernize live WooCommerce product & archive frontend on https://thechapmancollection.com
via Code Snippet #24 (and purge the 16 inactive Temp NRL FB debug snippets):
1. Preserve Meta Catalog Weapons/Wildlife guard (WC-3211 & WC-3327).
2. Preserve & restore full Zero-Dash Filter (the_title, the_content, the_excerpt,
   woocommerce_short_description, and gettext/ngettext for WooCommerce result counts).
3. Restore Beaver Themer top-navbar clearance on Shop/Archive/Category pages.
4. Enshrine the 5-Swatch Chaphavian (Chapman + Safe Haven + Gustavian) WooCommerce Palette & UX Polish:
   - Deep Iron (#2B2F32) ADD TO CART button with #F7F5F2 Alabaster text (ghost-to-iron hover).
   - Chaphavian Rose (#B35A5E) Sale prices & Chaphavian Slate (#8A8F97) Was prices.
   - Equal-height 3-column Beaver Builder Post Grid cards (.fl-post-grid-post) with aligned
     square gallery frames and bottom-locked ADD TO CART buttons.
   - Pixel-locked vertical alignment of the right-hand Product Categories sidebar card
     (.fl-node-eswn0av89612 > .fl-col-content) with the top of the product card grid, plus
     indented parent/child category hierarchy and active category highlighting.
   - Remove the empty 'Reviews (0)' tab on one-of-a-kind antique listings.
   - Hide the visual SEO tag cloud dump (span.tagged_as) below Add to Cart while keeping
     tags intact for Yoast and search engines.
   - Render a gracious Rancho Santa Fe Showroom Concierge card below Add to Cart.
"""

import os
import sys
import json
import base64
import urllib.request
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(r"c:\Users\Saturn\Desktop\project-marshall-college\.env")

WP_BASE = "https://thechapmancollection.com/wp-json"
USER = os.getenv("WP_REST_USER", "neverrender-labs")
APP_PASS = os.getenv("WP_REST_APP_PASSWORD", "")
AUTH_HEADER = "Basic " + base64.b64encode(f"{USER}:{APP_PASS}".encode("utf-8")).decode("utf-8")


def api_request(url, method="GET", data=None):
    headers = {
        "Authorization": AUTH_HEADER,
        "User-Agent": "NRL-WooCommerce-Scandinavian-Modernizer/2.0",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=45) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else {}


PHP_CODE = r"""
// 1. Permanently block sensitive items (WC-3211 Sword, WC-3327 Tusks) and all purged Hand-Finished Silk Qum rugs from syncing to Meta Catalog (Facebook & Instagram)
define('NRL_PURGED_SILK_QUM_IDS', array(3192, 3105, 3103, 3101, 3098, 3095, 3092, 3090, 3088, 3081));
add_filter('wc_facebook_should_sync_product', function ($should_sync, $product) {
    $blocked = array_merge(array(3211, 3327), NRL_PURGED_SILK_QUM_IDS);
    if ($product && in_array((int) $product->get_id(), $blocked, true)) {
        return false;
    }
    return $should_sync;
}, 999, 2);

// 1b. Redirect any clicks on purged Hand-Finished Silk Qum carpet URLs (including the 2026-11-08 09:02 AM email blast blue runner link) straight to /product-category/carpets/
function nrl_redirect_purged_silk_qum_urls() {
    if (is_admin()) {
        return;
    }
    $req_uri = isset($_SERVER['REQUEST_URI']) ? strtolower((string) $_SERVER['REQUEST_URI']) : '';
    if (strpos($req_uri, '/wp-json/') !== false) {
        return;
    }
    if (
        strpos($req_uri, 'new-persian-hand-finished-silk-qum') !== false ||
        strpos($req_uri, 'hand-finished-silk-qum') !== false ||
        (function_exists('is_singular') && is_singular('product') && in_array((int) get_queried_object_id(), NRL_PURGED_SILK_QUM_IDS, true))
    ) {
        wp_redirect('https://thechapmancollection.com/product-category/carpets/', 302);
        exit;
    }
}
add_action('init', 'nrl_redirect_purged_silk_qum_urls', 1);
add_action('template_redirect', 'nrl_redirect_purged_silk_qum_urls', 1);

// 2. Never render em-dashes, en-dashes, broken Windows-1252 replacement chars, or legacy CTA/trial phrases anywhere on the frontend
function nrl_strip_rendered_dashes($text) {
    if (!is_string($text) || $text === '') {
        return $text;
    }
    $text = str_replace(
        array('&#8212;', '&#8211;', '&mdash;', '&ndash;', "\xE2\x80\x94", "\xE2\x80\x93", "\xEF\xBF\xBD"),
        array(', ', ' to ', ', ', ' to ', ', ', ' to ', '"'),
        $text
    );
    $text = str_ireplace(
        array(
            'call or text Melissa directly',
            'call or text Melissa',
            'contact Melissa directly',
            'contact Melissa',
            'text Melissa',
            'have Melissa arrange',
            '48-hour in-home trial',
            '48 hour in home trial',
            'complimentary in-home trial',
            'complimentary in-home preview',
            'free in-home trial',
            'free in home trial'
        ),
        array(
            'contact us',
            'contact us',
            'contact us',
            'contact us',
            'contact us',
            'contact us to arrange',
            'private showroom appointment',
            'private showroom appointment',
            'private showroom appointment',
            'private showroom appointment',
            'private showroom appointment',
            'private showroom appointment'
        ),
        $text
    );
    if (stripos($text, 'Silk Qum') !== false || stripos($text, 'hand-finished silk') !== false || stripos($text, 'hand finished silk') !== false) {
        $text = preg_replace('/\bhand[- ]woven\b/i', 'hand-finished', $text);
        $text = preg_replace('/\bwoven\b/i', 'hand-finished', $text);
    }
    return $text;
}
add_filter('the_title', 'nrl_strip_rendered_dashes', 999);
add_filter('woocommerce_product_get_name', function ($name) {
    return str_replace(array('&amp;', '&#038;'), '&', nrl_strip_rendered_dashes((string) $name));
}, 999);
add_filter('woocommerce_product_title', function ($title) {
    return str_replace(array('&amp;', '&#038;'), '&', nrl_strip_rendered_dashes((string) $title));
}, 999);
add_filter('the_content', 'nrl_strip_rendered_dashes', 999);
add_filter('the_excerpt', 'nrl_strip_rendered_dashes', 999);
add_filter('woocommerce_short_description', 'nrl_strip_rendered_dashes', 999);
add_filter('gettext', function ($translated, $text, $domain) {
    if ($domain === 'woocommerce') {
        return nrl_strip_rendered_dashes($translated);
    }
    return $translated;
}, 999, 3);
add_filter('ngettext', function ($translation, $single, $plural, $number, $domain) {
    if ($domain === 'woocommerce') {
        return nrl_strip_rendered_dashes($translation);
    }
    return $translation;
}, 999, 5);

// 3. Remove empty 'Reviews (0)' tab on one-of-a-kind showroom antiques
add_filter('woocommerce_product_tabs', function ($tabs) {
    unset($tabs['reviews']);
    return $tabs;
}, 98);

// 3b. Dynamic "Show: 24 / 48 / 100 / 200 (All)" Per-Page Selector on Shop & Category Archives (including Beaver Themer Post Grid)
function nrl_get_requested_per_page() {
    if (isset($_GET['per_page'])) {
        $val = (int) $_GET['per_page'];
        if (in_array($val, array(16, 24, 48, 100, 200), true)) {
            return $val;
        }
    }
    return 24;
}
add_filter('loop_shop_per_page', function ($cols) {
    return nrl_get_requested_per_page();
}, 999);
add_action('pre_get_posts', function ($query) {
    if (is_admin() || !$query->is_main_query()) {
        return;
    }
    $existing_not_in = (array) $query->get('post__not_in');
    $query->set('post__not_in', array_values(array_unique(array_merge($existing_not_in, NRL_PURGED_SILK_QUM_IDS))));
    if (function_exists('is_woocommerce') && (is_shop() || is_product_category() || is_product_tag())) {
        $query->set('posts_per_page', nrl_get_requested_per_page());
    }
}, 999);
add_filter('fl_builder_loop_query_args', function ($args) {
    $existing_not_in = isset($args['post__not_in']) ? (array) $args['post__not_in'] : array();
    $args['post__not_in'] = array_values(array_unique(array_merge($existing_not_in, NRL_PURGED_SILK_QUM_IDS)));
    if (function_exists('is_woocommerce') && (is_shop() || is_product_category() || is_product_tag())) {
        $args['posts_per_page'] = nrl_get_requested_per_page();
    }
    return $args;
}, 999);

// 4. Add understated Rancho Santa Fe Showroom Concierge note below Add to Cart
add_action('woocommerce_after_add_to_cart_form', function () {
    echo '<div class="nrl-rsf-concierge-note">'
       . '<strong>Rancho Santa Fe Showroom Concierge</strong><br>'
       . 'Private showroom consultations, white-glove delivery and showroom pickup at 6014 La Granada, Rancho Santa Fe. '
       . 'For additional photographs, condition details or white-glove delivery arrangements, please '
       . '<a href="https://thechapmancollection.com/contact-us/">contact us</a> at '
       . '<a href="tel:+18583492638">(858) 349-2638</a> or visit our Rancho Santa Fe showroom.'
       . '</div>';
});

// 5. Enshrined 5-Swatch Chaphavian (Chapman + Safe Haven + Gustavian) WooCommerce & Beaver Themer Archive Styling
add_action('wp_head', function () {
    if (function_exists('is_woocommerce') && (is_woocommerce() || is_shop() || is_product_category() || is_product_tag() || is_product() || is_cart() || is_checkout())) {
        echo '<style id="nrl-scandinavian-gustavian-woo">
            /* Chaphavian Alabaster (#F7F5F2) Page Canvas & Editorial Typography on All Product & Shop Pages */
            body.woocommerce,
            body.woocommerce-page,
            body.woocommerce .fl-page,
            body.woocommerce-page .fl-page,
            body.woocommerce .fl-page-content,
            body.woocommerce-page .fl-page-content,
            .fl-builder-content-370 .fl-row-content-wrap {
                background-color: #F7F5F2 !important;
                color: #2B2F32 !important;
                font-family: "Cormorant Garamond", Georgia, serif !important;
            }

            /* Top navbar clearance on Beaver Themer archives & single product pages */
            body.fl-theme-builder-archive .fl-page-content,
            body.woocommerce-page.archive .fl-page-content,
            body.single-product .fl-page-content {
                padding-top: 78px !important;
            }
            @media (max-width: 768px) {
                body.fl-theme-builder-archive .fl-page-content,
                body.woocommerce-page.archive .fl-page-content,
                body.single-product .fl-page-content {
                    padding-top: 58px !important;
                }
            }

            /* ==========================================================================
               ARCHIVE / CATEGORY HEADER & PRODUCT GRID (Beaver Themer Layout 370)
               ========================================================================== */
            div.fl-node-x9jdom6vwbfs .pp-heading-content .pp-heading .heading-title,
            div.fl-node-x9jdom6vwbfs .pp-heading-content .pp-heading .heading-title span.pp-primary-title,
            .woocommerce div.product .product_title,
            .fl-module-woo-product-title h1,
            .woocommerce-products-header__title,
            .woocommerce ul.products li.product .woocommerce-loop-product__title,
            .woocommerce div.product .woocommerce-tabs .panel h2,
            .woocommerce .related.products > h2 {
                font-family: "Cormorant Garamond", Georgia, serif !important;
                color: #2B2F32 !important;
                font-weight: 600 !important;
                letter-spacing: 0.04em !important;
                line-height: 1.2 !important;
            }
            div.fl-node-x9jdom6vwbfs .pp-heading-content .pp-heading .heading-title,
            div.fl-node-x9jdom6vwbfs .pp-heading-content .pp-heading .heading-title span.pp-primary-title {
                font-size: 42px !important;
                margin-top: 0 !important;
                margin-bottom: 8px !important;
            }
            @media (max-width: 768px) {
                div.fl-node-x9jdom6vwbfs .pp-heading-content .pp-heading .heading-title,
                div.fl-node-x9jdom6vwbfs .pp-heading-content .pp-heading .heading-title span.pp-primary-title {
                    font-size: 32px !important;
                }
            }
            /* Chaphavian Rose 48px accent line under Category Title */
            div.fl-node-x9jdom6vwbfs .pp-heading-content .pp-heading-separator .pp-separator-line {
                border-bottom: 2px solid #B35A5E !important;
                width: 48px !important;
                margin-bottom: 10px !important;
            }
            /* Hairline Putty rule below breadcrumb */
            .fl-node-3t9ygfn8s7bp .fl-separator {
                border-top: 1px solid #D5D3CC !important;
            }

            /* Result Count ("Showing all 16 results") & Ordering Dropdown ("Sort by latest") */
            .fl-post-module-woo-ordering {
                display: flex !important;
                align-items: center !important;
                justify-content: space-between !important;
                flex-wrap: wrap !important;
                gap: 12px !important;
                padding-bottom: 24px !important;
                margin-bottom: 0 !important;
            }
            .fl-post-module-woo-ordering::before,
            .fl-post-module-woo-ordering::after,
            .fl-post-module-woo-ordering .fl-clear {
                display: none !important;
            }
            .fl-post-module-woo-ordering p.woocommerce-result-count,
            .woocommerce p.woocommerce-result-count {
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-size: 18px !important;
                font-style: italic !important;
                color: #8A8F97 !important;
                margin: 0 !important;
                float: none !important;
            }
            .fl-post-module-woo-ordering form.woocommerce-ordering,
            .woocommerce form.woocommerce-ordering {
                margin: 0 !important;
                float: none !important;
            }
            .fl-post-module-woo-ordering form.woocommerce-ordering select.orderby,
            .woocommerce form.woocommerce-ordering select.orderby,
            select.nrl-per-page-select {
                background-color: #F7F5F2 !important;
                border: 1px solid #D5D3CC !important;
                border-radius: 0 !important;
                color: #2B2F32 !important;
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-size: 16px !important;
                font-weight: 600 !important;
                padding: 8px 32px 8px 14px !important;
                height: auto !important;
                box-shadow: none !important;
                cursor: pointer !important;
            }
            .nrl-ordering-controls-wrap {
                display: inline-flex !important;
                align-items: center !important;
                gap: 12px !important;
                flex-wrap: wrap !important;
            }
            .nrl-per-page-label {
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-size: 16px !important;
                font-style: italic !important;
                color: #8A8F97 !important;
                margin-right: 4px !important;
            }

            /* Equal-Height 3-Column Flexbox Product Grid (.fl-node-x3fzctub4wrq .fl-post-grid) */
            .fl-node-x3fzctub4wrq .fl-post-grid {
                display: flex !important;
                flex-wrap: wrap !important;
                align-items: stretch !important;
                margin-left: -12px !important;
                margin-right: -12px !important;
            }
            .fl-node-x3fzctub4wrq .fl-post-grid::before,
            .fl-node-x3fzctub4wrq .fl-post-grid::after {
                display: none !important;
            }
            .fl-node-x3fzctub4wrq .fl-post-column {
                float: none !important;
                display: flex !important;
                flex-direction: column !important;
                width: 33.333333% !important;
                padding: 0 12px 24px 12px !important;
                margin: 0 !important;
                box-sizing: border-box !important;
            }
            @media (max-width: 992px) {
                .fl-node-x3fzctub4wrq .fl-post-column {
                    width: 50% !important;
                }
            }
            @media (max-width: 768px) {
                .fl-node-x3fzctub4wrq .fl-post-column {
                    width: 100% !important;
                }
            }

            /* Chaphavian Card Frame & Rose-Tinted Shadow on Archive Cards & Single Product Gallery */
            .fl-node-x3fzctub4wrq .fl-post-grid-post,
            .woocommerce ul.products li.product {
                display: flex !important;
                flex-direction: column !important;
                flex: 1 1 auto !important;
                height: 100% !important;
                background: #F7F5F2 !important;
                border: 1px solid #D5D3CC !important;
                padding: 0 !important;
                box-shadow: 0 10px 26px -10px rgba(179, 90, 94, 0.16),
                            0 4px 12px -4px rgba(179, 90, 94, 0.08) !important;
                transition: border-color 0.28s ease, box-shadow 0.28s ease !important;
            }
            .fl-node-x3fzctub4wrq .fl-post-grid-post:hover,
            .woocommerce ul.products li.product:hover {
                border-color: #B35A5E !important;
                box-shadow: 0 18px 36px -8px rgba(179, 90, 94, 0.28) !important;
            }

            /* Uniform Square Gallery Thumbnail Frame inside each Archive Card */
            .fl-node-x3fzctub4wrq .fl-post-grid-image {
                position: relative !important;
                margin: 16px 16px 0 16px !important;
                padding: 0 !important;
                aspect-ratio: 1 / 1 !important;
                background-color: #EFECE6 !important;
                border: 1px solid #D5D3CC !important;
                overflow: hidden !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }
            .fl-node-x3fzctub4wrq .fl-post-grid-image a {
                display: flex !important;
                width: 100% !important;
                height: 100% !important;
                align-items: center !important;
                justify-content: center !important;
            }
            .fl-node-x3fzctub4wrq .fl-post-grid-image img {
                width: 100% !important;
                height: 100% !important;
                object-fit: cover !important;
                display: block !important;
                transition: none !important;
                transform: none !important;
            }

            /* Card Body Flex Layout so ADD TO CART Locks to the Bottom Line */
            .fl-node-x3fzctub4wrq .fl-post-grid-text {
                display: flex !important;
                flex-direction: column !important;
                flex: 1 1 auto !important;
                padding: 20px 20px 22px 20px !important;
                text-align: center !important;
            }
            .fl-node-x3fzctub4wrq h2.fl-post-grid-title {
                margin: 0 0 10px 0 !important;
                padding: 0 !important;
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-size: 21px !important;
                font-weight: 600 !important;
                line-height: 1.28 !important;
                letter-spacing: 0.02em !important;
            }
            .fl-node-x3fzctub4wrq h2.fl-post-grid-title a {
                font-family: "Cormorant Garamond", Georgia, serif !important;
                color: #2B2F32 !important;
                text-decoration: none !important;
                transition: color 0.2s ease !important;
            }
            .fl-node-x3fzctub4wrq h2.fl-post-grid-title a:hover {
                color: #B35A5E !important;
            }

            /* Card Excerpt Copy */
            .fl-node-x3fzctub4wrq .fl-post-grid-content {
                margin-top: 6px !important;
                margin-bottom: 18px !important;
            }
            .fl-node-x3fzctub4wrq .fl-post-grid-content p {
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-size: 16.5px !important;
                line-height: 1.56 !important;
                color: #4A4F54 !important;
                font-weight: 500 !important;
            }

            /* Lock ADD TO CART Wrapper to Card Bottom */
            .fl-node-x3fzctub4wrq .fl-post-grid-woo-button {
                margin-top: auto !important;
                padding-top: 12px !important;
                width: 100% !important;
            }

            /* ==========================================================================
               RIGHT-HAND "PRODUCT CATEGORIES" SIDEBAR (.fl-node-eswn0av89612.prod-sdbr)
               Aesthetically Aligned with the Top of the Product Cards Grid
               ========================================================================== */
            /* Hide empty spacer widget at top of sidebar */
            .fl-node-sa1gbpod3vci {
                display: none !important;
            }
            @media (min-width: 993px) {
                /* Baseline CSS offset so the sidebar starts aligned with the product cards even before JS refines to 0px */
                .fl-node-eswn0av89612.prod-sdbr > .fl-col-content {
                    margin-top: 196px;
                    margin-right: 0 !important;
                    margin-left: 16px !important;
                }
            }
            @media (max-width: 992px) {
                .fl-node-eswn0av89612.prod-sdbr > .fl-col-content {
                    margin-top: 24px !important;
                    margin-left: 0 !important;
                    margin-right: 0 !important;
                }
            }
            .fl-node-eswn0av89612.prod-sdbr > .fl-col-content {
                background-color: #F7F5F2 !important;
                border: 1px solid #D5D3CC !important;
                box-shadow: 0 10px 26px -10px rgba(179, 90, 94, 0.16),
                            0 4px 12px -4px rgba(179, 90, 94, 0.08) !important;
                padding: 26px 24px !important;
            }
            .fl-node-sky6mranxejq .widget_product_categories h2.widgettitle {
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-size: 21px !important;
                font-weight: 600 !important;
                letter-spacing: 0.10em !important;
                text-transform: uppercase !important;
                color: #2B2F32 !important;
                margin: 0 0 16px 0 !important;
                padding-bottom: 12px !important;
                border-bottom: 1px solid #D5D3CC !important;
                position: relative !important;
            }
            .fl-node-sky6mranxejq .widget_product_categories h2.widgettitle::after {
                content: "" !important;
                position: absolute !important;
                left: 0 !important;
                bottom: -1px !important;
                width: 42px !important;
                height: 2px !important;
                background-color: #B35A5E !important;
            }

            /* Structured Parent / Child Category Tree inside Product Categories */
            .fl-node-sky6mranxejq .widget_product_categories ul.product-categories {
                list-style: none !important;
                margin: 0 !important;
                padding: 0 !important;
            }
            .fl-node-sky6mranxejq .widget_product_categories ul.product-categories > li.cat-item {
                margin: 0 0 12px 0 !important;
                padding: 0 0 12px 0 !important;
                border-bottom: 1px solid rgba(213, 211, 204, 0.65) !important;
                line-height: 1.4 !important;
            }
            .fl-node-sky6mranxejq .widget_product_categories ul.product-categories > li.cat-item:last-child {
                margin-bottom: 0 !important;
                padding-bottom: 0 !important;
                border-bottom: none !important;
            }
            /* Parent Category Links */
            .fl-node-sky6mranxejq .widget_product_categories ul.product-categories > li.cat-item > a {
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-size: 19px !important;
                font-weight: 600 !important;
                color: #2B2F32 !important;
                text-decoration: none !important;
                letter-spacing: 0.02em !important;
                transition: color 0.2s ease !important;
            }
            /* Indented Child Subcategories */
            .fl-node-sky6mranxejq .widget_product_categories ul.product-categories ul.children {
                list-style: none !important;
                margin: 8px 0 2px 4px !important;
                padding: 2px 0 2px 14px !important;
                border-left: 1.5px solid #D5D3CC !important;
            }
            .fl-node-sky6mranxejq .widget_product_categories ul.product-categories ul.children > li.cat-item {
                margin: 5px 0 !important;
                padding: 0 !important;
                border: none !important;
                line-height: 1.42 !important;
            }
            .fl-node-sky6mranxejq .widget_product_categories ul.product-categories ul.children > li.cat-item > a {
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-size: 16.5px !important;
                font-weight: 500 !important;
                color: #52575C !important;
                text-decoration: none !important;
                transition: color 0.2s ease !important;
            }
            /* Hover & Current Category Highlight in Chaphavian Rose (#B35A5E) */
            .fl-node-sky6mranxejq .widget_product_categories ul.product-categories li.cat-item > a:hover,
            .fl-node-sky6mranxejq .widget_product_categories ul.product-categories li.current-cat > a {
                color: #B35A5E !important;
                font-weight: 700 !important;
            }
            .fl-node-sky6mranxejq .widget_product_categories ul.product-categories span.count {
                font-family: "Montserrat", sans-serif !important;
                font-size: 11px !important;
                font-weight: 500 !important;
                color: #8A8F97 !important;
                margin-left: 4px !important;
            }

            /* ==========================================================================
               SINGLE PRODUCT PAGES & GLOBAL WOOCOMMERCE ELEMENTS
               ========================================================================== */
            .woocommerce div.product .product_title,
            .fl-module-woo-product-title h1 {
                font-size: 32px !important;
                margin-bottom: 12px !important;
            }
            .woocommerce ul.products li.product .woocommerce-loop-product__title {
                font-size: 20px !important;
            }

            /* Product Description & Short Description Body Copy in Cormorant Garamond */
            .woocommerce div.product .woocommerce-product-details__short-description,
            .woocommerce div.product .woocommerce-product-details__short-description p,
            .woocommerce div.product .woocommerce-tabs .panel,
            .woocommerce div.product .woocommerce-tabs .panel p,
            .woocommerce div.product .woocommerce-tabs .panel li {
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-size: 19px !important;
                line-height: 1.72 !important;
                color: #2B2F32 !important;
                font-weight: 500 !important;
            }

            /* Breadcrumbs & Product Meta (SKU / Category) */
            .woocommerce .woocommerce-breadcrumb,
            .woocommerce .woocommerce-breadcrumb a,
            .fl-module-fl-woo-breadcrumb .woocommerce-breadcrumb,
            .fl-module-fl-woo-breadcrumb .woocommerce-breadcrumb a,
            .woocommerce div.product .product_meta,
            .woocommerce div.product .product_meta a {
                font-family: "Montserrat", sans-serif !important;
                font-size: 10.5px !important;
                letter-spacing: 0.14em !important;
                text-transform: uppercase !important;
                color: #8A8F97 !important;
            }
            .woocommerce .woocommerce-breadcrumb a:hover,
            .fl-module-fl-woo-breadcrumb .woocommerce-breadcrumb a:hover,
            .woocommerce div.product .product_meta a:hover {
                color: #B35A5E !important;
            }

            /* Enshrined Chaphavian Price Palette (#8A8F97 Slate "Was " / #B35A5E Rose "Is ") */
            .woocommerce div.product p.price,
            .woocommerce div.product span.price,
            .woocommerce ul.products li.product .price,
            .fl-post-grid-text .price,
            .fl-module-fl-woo-product-price .price {
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-size: 22px !important;
            }
            html body .fl-module-fl-woo-product-price .price del,
            html body .woocommerce ul.products li.product .price del,
            html body .fl-post-grid-text .price del,
            html body .woocommerce div.product p.price del,
            html body .woocommerce div.product span.price del {
                color: #8A8F97 !important;
                opacity: 1 !important;
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-weight: 500 !important;
                margin-right: 8px !important;
                display: inline-block !important;
            }
            html body .fl-module-fl-woo-product-price .price del::before,
            html body .woocommerce ul.products li.product .price del::before,
            html body .fl-post-grid-text .price del::before,
            html body .woocommerce div.product p.price del::before,
            html body .woocommerce div.product span.price del::before {
                content: "Was " !important;
                color: #8A8F97 !important;
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-weight: 500 !important;
            }
            html body .fl-module-fl-woo-product-price .price ins,
            html body .woocommerce ul.products li.product .price ins,
            html body .fl-post-grid-text .price ins,
            html body .woocommerce div.product p.price ins,
            html body .woocommerce div.product span.price ins,
            html body .fl-module-woo-product-price .price ins .woocommerce-Price-amount {
                color: #B35A5E !important;
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-weight: 600 !important;
                text-decoration: none !important;
                display: inline-block !important;
            }
            html body .fl-module-fl-woo-product-price .price ins::before,
            html body .woocommerce ul.products li.product .price ins::before,
            html body .fl-post-grid-text .price ins::before,
            html body .woocommerce div.product p.price ins::before,
            html body .woocommerce div.product span.price ins::before {
                content: "Is " !important;
                color: #B35A5E !important;
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-weight: 600 !important;
            }

            /* Ghost-to-Dark-Iron CTA Button matching the Circular & About/Services Pages */
            .woocommerce div.product form.cart .button.single_add_to_cart_button,
            .woocommerce ul.products li.product .button,
            .fl-node-x3fzctub4wrq .fl-post-grid-woo-button a.button,
            .fl-post-grid-woo-button a.add_to_cart_button {
                display: inline-block !important;
                width: 100% !important;
                box-sizing: border-box !important;
                text-align: center !important;
                background-color: #2B2F32 !important;
                color: #F7F5F2 !important;
                border: 1px solid #2B2F32 !important;
                border-radius: 0 !important;
                padding: 12px 24px !important;
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-size: 13.5px !important;
                font-weight: 600 !important;
                letter-spacing: 0.18em !important;
                text-transform: uppercase !important;
                transition: all 0.22s ease !important;
            }
            .woocommerce div.product form.cart .button.single_add_to_cart_button {
                width: auto !important;
                padding: 12px 32px !important;
            }
            .woocommerce div.product form.cart .button.single_add_to_cart_button:hover,
            .woocommerce ul.products li.product .button:hover,
            .fl-node-x3fzctub4wrq .fl-post-grid-woo-button a.button:hover,
            .fl-post-grid-woo-button a.add_to_cart_button:hover {
                background-color: #F7F5F2 !important;
                color: #2B2F32 !important;
                border-color: #2B2F32 !important;
            }

            /* Single Product Gallery Frame */
            .woocommerce div.product div.images .woocommerce-product-gallery__wrapper {
                background: #F7F5F2 !important;
                border: 1px solid #D5D3CC !important;
                padding: 14px !important;
                box-shadow: 0 10px 26px -10px rgba(179, 90, 94, 0.16),
                            0 4px 12px -4px rgba(179, 90, 94, 0.08) !important;
            }

            /* WooCommerce Tabs (Description / Additional Information) in Chaphavian Palette */
            .woocommerce div.product .woocommerce-tabs ul.tabs::before {
                border-bottom: 1px solid #D5D3CC !important;
            }
            .woocommerce div.product .woocommerce-tabs ul.tabs li {
                background-color: #EFECE6 !important;
                border: 1px solid #D5D3CC !important;
                border-radius: 0 !important;
            }
            .woocommerce div.product .woocommerce-tabs ul.tabs li.active {
                background-color: #F7F5F2 !important;
                border-bottom-color: #F7F5F2 !important;
            }
            .woocommerce div.product .woocommerce-tabs ul.tabs li a {
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-size: 15px !important;
                font-weight: 600 !important;
                letter-spacing: 0.14em !important;
                text-transform: uppercase !important;
                color: #2B2F32 !important;
            }

            /* Hide visual SEO tag dump below Add to Cart (tags remain in HTML head/schema for Yoast) */
            .woocommerce div.product .product_meta .tagged_as {
                display: none !important;
            }

            /* Understated Rancho Santa Fe Showroom Concierge box */
            .nrl-rsf-concierge-note {
                margin-top: 18px;
                margin-bottom: 18px;
                padding: 16px 18px;
                background-color: #EFECE6;
                border: 1px solid #D5D3CC;
                border-left: 3px solid #B35A5E;
                color: #2B2F32;
                font-family: "Cormorant Garamond", Georgia, serif !important;
                font-size: 17px;
                line-height: 1.6;
            }
            .nrl-rsf-concierge-note strong {
                display: inline-block;
                font-family: "Montserrat", sans-serif !important;
                font-size: 10.5px;
                letter-spacing: 0.16em;
                text-transform: uppercase;
                color: #B35A5E;
                margin-bottom: 6px;
            }
            .nrl-rsf-concierge-note a {
                color: #2B2F32;
                text-decoration: underline;
                text-decoration-color: #B35A5E;
                font-weight: 600;
            }
        </style>';
    }
}, 999);

// 6. Pixel-Lock the Right-Hand "Product Categories" Sidebar Card to the Top Border of the Product Grid on Desktop
add_action('wp_footer', function () {
    if (function_exists('is_woocommerce') && (is_shop() || is_product_category() || is_product_tag())) {
        echo '<script id="nrl-archive-sidebar-align-js">
        (function() {
            function alignArchiveSidebar() {
                var sidebarCol = document.querySelector(".fl-node-eswn0av89612.prod-sdbr");
                var sidebarBox = document.querySelector(".fl-node-eswn0av89612.prod-sdbr > .fl-col-content");
                var firstCard  = document.querySelector(".fl-node-x3fzctub4wrq .fl-post-grid-post");
                if (!sidebarCol || !sidebarBox || !firstCard) return;
                if (window.innerWidth <= 992) {
                    sidebarBox.style.marginTop = "24px";
                    return;
                }
                var colTop  = sidebarCol.getBoundingClientRect().top;
                var cardTop = firstCard.getBoundingClientRect().top;
                var delta   = Math.max(0, Math.round(cardTop - colTop));
                sidebarBox.style.marginTop = delta + "px";
            }
            function injectPerPageSelector() {
                var orderingForm = document.querySelector(".fl-post-module-woo-ordering form.woocommerce-ordering, .woocommerce form.woocommerce-ordering");
                if (!orderingForm || document.querySelector(".nrl-per-page-select")) return;

                var params = new URLSearchParams(window.location.search);
                var currentPerPage = parseInt(params.get("per_page") || "24", 10);
                if ([16, 24, 48, 100, 200].indexOf(currentPerPage) === -1) {
                    currentPerPage = 24;
                }

                // Preserve per_page when changing Sort By dropdown
                if (!orderingForm.querySelector("input[name=per_page]")) {
                    var hiddenPerPage = document.createElement("input");
                    hiddenPerPage.type = "hidden";
                    hiddenPerPage.name = "per_page";
                    hiddenPerPage.value = String(currentPerPage);
                    orderingForm.appendChild(hiddenPerPage);
                }

                var wrap = document.createElement("div");
                wrap.className = "nrl-ordering-controls-wrap";
                orderingForm.parentNode.insertBefore(wrap, orderingForm);

                var perPageBox = document.createElement("div");
                perPageBox.style.display = "inline-flex";
                perPageBox.style.alignItems = "center";

                var label = document.createElement("span");
                label.className = "nrl-per-page-label";
                label.textContent = "Show:";

                var select = document.createElement("select");
                select.className = "nrl-per-page-select";
                select.setAttribute("aria-label", "Products per page");

                var options = [
                    { val: 24,  text: "24 per page" },
                    { val: 48,  text: "48 per page" },
                    { val: 100, text: "100 per page" },
                    { val: 200, text: "200 (Show All)" }
                ];
                options.forEach(function(opt) {
                    var o = document.createElement("option");
                    o.value = String(opt.val);
                    o.textContent = opt.text;
                    if (opt.val === currentPerPage) {
                        o.selected = true;
                    }
                    select.appendChild(o);
                });

                select.addEventListener("change", function() {
                    var nextUrl = new URL(window.location.href);
                    nextUrl.pathname = nextUrl.pathname.replace(/\/page\/\d+\/?$/, "/");
                    nextUrl.searchParams.set("per_page", select.value);
                    nextUrl.searchParams.delete("paged");
                    window.location.href = nextUrl.toString();
                });

                perPageBox.appendChild(label);
                perPageBox.appendChild(select);
                wrap.appendChild(perPageBox);
                wrap.appendChild(orderingForm);
            }
            document.addEventListener("DOMContentLoaded", function() {
                injectPerPageSelector();
                alignArchiveSidebar();
            });
            window.addEventListener("load", alignArchiveSidebar);
            window.addEventListener("resize", alignArchiveSidebar);
            setTimeout(alignArchiveSidebar, 250);
        })();
        </script>';
    }
}, 999);
"""


def main():
    res = api_request(
        f"{WP_BASE}/code-snippets/v1/snippets/24",
        method="PUT",
        data={
            "name": "NRL Meta Catalog Policy Guard, Zero-Dash Filter & Scandinavian Frontend Polish",
            "code": PHP_CODE,
            "scope": "global",
            "active": True,
        },
    )
    print(f"[UPDATED SNIPPET #24] {res.get('name')} (active={res.get('active')}, modified={res.get('modified')})")


if __name__ == "__main__":
    main()
