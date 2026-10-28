import os
import requests

auth = ('neverrender-labs', os.getenv('WP_REST_APP_PASSWORD', ''))

html_content = """<!-- wp:html -->
<style>
  .entry-header, .page-header, .entry-title, .post-edit-link, .entry-footer { display: none !important; }
  .meta-checkout-card {
    max-width: 480px;
    margin: 60px auto;
    padding: 40px 32px;
    background: #FAF6F0;
    border: 1px solid #C8A96A;
    border-radius: 6px;
    text-align: center;
    font-family: Georgia, 'Times New Roman', serif;
    box-shadow: 0 8px 28px rgba(0,0,0,0.08);
  }
</style>
<div class="meta-checkout-card">
  <p style="font-size: 12px; letter-spacing: 2px; text-transform: uppercase; color: #8C6D2F; margin: 0 0 10px 0; font-family: Arial, sans-serif; font-weight: bold;">The Chapman Collection &bull; Rancho Santa Fe</p>
  <h2 style="font-size: 24px; color: #1A1A1A; margin: 0 0 14px 0; font-weight: normal;">Preparing Your Private Checkout&hellip;</h2>
  <p style="font-size: 15px; color: #555555; margin: 0 0 20px 0; line-height: 1.6;">Adding your selected showroom piece to your bag and transferring you to secure checkout.</p>
</div>
<script>
(function() {
  var params = new URLSearchParams(window.location.search);
  var productsParam = params.get('products') || params.get('product') || '';
  var couponParam = params.get('coupon') || '';

  // Parse products=ID:QTY,ID2:QTY2
  var items = [];
  if (productsParam) {
    var parts = productsParam.split(',');
    for (var i = 0; i < parts.length; i++) {
      var seg = parts[i].trim().split(':');
      var pid = parseInt(seg[0], 10);
      var qty = seg.length > 1 ? parseInt(seg[1], 10) : 1;
      if (pid > 0) {
        items.push({ id: pid, quantity: (qty > 0 ? qty : 1) });
      }
    }
  }

  if (items.length === 1 && !couponParam) {
    // Fast single-item native WooCommerce checkout redirect
    window.location.replace('https://thechapmancollection.com/checkout/?add-to-cart=' + items[0].id + '&quantity=' + items[0].quantity);
    return;
  }

  if (items.length > 0) {
    // Multi-item or coupon: add sequentially then go to checkout
    var idx = 0;
    function addNext() {
      if (idx >= items.length) {
        window.location.replace('https://thechapmancollection.com/checkout/');
        return;
      }
      var it = items[idx++];
      fetch('https://thechapmancollection.com/?add-to-cart=' + it.id + '&quantity=' + it.quantity, { credentials: 'same-origin' })
        .then(function() { addNext(); })
        .catch(function() { addNext(); });
    }
    addNext();
  } else {
    window.location.replace('https://thechapmancollection.com/checkout/');
  }
})();
</script>
<!-- /wp:html -->"""

r = requests.post('https://thechapmancollection.com/wp-json/wp/v2/pages', auth=auth, json={
    'title': 'Meta Direct Checkout',
    'slug': 'meta-checkout',
    'status': 'publish',
    'content': html_content
})
print('Status:', r.status_code)
data = r.json()
print('Page ID:', data.get('id'), 'Link:', data.get('link'))
