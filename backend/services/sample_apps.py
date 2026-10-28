"""
Built-in Demo Applications for Hackathon Demonstrations.
Provides local targets with realistic UI and intentional edge-case bugs
to showcase TestPilot AI's autonomous test execution and bug reproduction.
"""

def get_demo_shop_html(base_url: str = "") -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AeroMart - Premium Tech Store (Demo Target)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b0f19;
      --card-bg: rgba(23, 30, 48, 0.75);
      --border: rgba(255, 255, 255, 0.1);
      --text: #f3f4f6;
      --text-muted: #9ca3af;
      --primary: #3b82f6;
      --primary-hover: #2563eb;
      --danger: #ef4444;
      --success: #10b981;
      --accent: #8b5cf6;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background: radial-gradient(circle at 50% 0%, #1e1e38 0%, #0b0f19 75%);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 40px 20px;
    }
    .badge {
      display: inline-block;
      padding: 4px 12px;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      border-radius: 9999px;
      background: rgba(139, 92, 246, 0.15);
      color: #c084fc;
      border: 1px solid rgba(139, 92, 246, 0.3);
      margin-bottom: 12px;
    }
    .header { text-align: center; margin-bottom: 30px; }
    .header h1 { font-size: 32px; font-weight: 800; letter-spacing: -0.02em; }
    .header p { color: var(--text-muted); margin-top: 6px; font-size: 15px; }

    .shop-container {
      width: 100%;
      max-width: 900px;
      display: grid;
      grid-template-columns: 1fr 1.1fr;
      gap: 24px;
    }
    @media (max-width: 768px) { .shop-container { grid-template-columns: 1fr; } }

    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px;
      backdrop-filter: blur(12px);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    .product-img {
      width: 100%;
      height: 200px;
      border-radius: 12px;
      background: linear-gradient(135deg, #2563eb, #7c3aed);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 64px;
      margin-bottom: 16px;
      box-shadow: 0 8px 24px rgba(59, 130, 246, 0.25);
    }
    .product-title { font-size: 20px; font-weight: 700; }
    .product-price { font-size: 24px; font-weight: 800; color: #60a5fa; margin: 8px 0; }
    .product-desc { font-size: 14px; color: var(--text-muted); line-height: 1.5; margin-bottom: 16px; }

    .qty-control {
      display: flex;
      align-items: center;
      gap: 12px;
      margin: 16px 0;
    }
    .qty-btn {
      width: 36px;
      height: 36px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: rgba(255, 255, 255, 0.05);
      color: var(--text);
      font-size: 18px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.2s;
    }
    .qty-btn:hover { background: rgba(255, 255, 255, 0.15); }
    .qty-val { font-size: 16px; font-weight: 700; min-width: 24px; text-align: center; }

    .form-group { margin-bottom: 16px; }
    .form-group label {
      display: block;
      font-size: 13px;
      font-weight: 600;
      color: #d1d5db;
      margin-bottom: 6px;
    }
    .form-control {
      width: 100%;
      padding: 10px 14px;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text);
      font-size: 14px;
      outline: none;
      transition: border-color 0.2s;
    }
    .form-control:focus { border-color: var(--primary); }

    .promo-row { display: flex; gap: 8px; }
    .btn-apply {
      padding: 10px 16px;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: #fff;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
    }
    .btn-apply:hover { background: rgba(255, 255, 255, 0.2); }

    .checkout-btn {
      width: 100%;
      padding: 14px;
      background: linear-gradient(135deg, var(--primary), var(--accent));
      border: none;
      border-radius: 10px;
      color: #fff;
      font-size: 16px;
      font-weight: 700;
      cursor: pointer;
      margin-top: 12px;
      transition: transform 0.15s, opacity 0.2s;
    }
    .checkout-btn:hover { opacity: 0.95; transform: translateY(-1px); }
    .checkout-btn:disabled { opacity: 0.5; cursor: not-allowed; }

    .summary-box {
      border-top: 1px solid var(--border);
      padding-top: 14px;
      margin-top: 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .summary-line { display: flex; justify-content: space-between; font-size: 14px; color: var(--text-muted); }
    .summary-total { font-size: 18px; font-weight: 800; color: #fff; border-top: 1px dashed var(--border); padding-top: 8px; }

    .banner {
      display: none;
      padding: 12px 16px;
      border-radius: 8px;
      margin-top: 16px;
      font-size: 14px;
      font-weight: 600;
    }
    .banner.success { display: block; background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .banner.error { display: block; background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }

    .hint-box {
      margin-top: 24px;
      max-width: 900px;
      width: 100%;
      background: rgba(30, 41, 59, 0.4);
      border: 1px dashed rgba(255, 255, 255, 0.15);
      border-radius: 12px;
      padding: 14px 20px;
      font-size: 13px;
      color: #94a3b8;
    }
    .hint-box code { color: #60a5fa; background: rgba(96, 165, 250, 0.1); padding: 2px 6px; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="header">
    <div class="badge">Live Testbed Environment</div>
    <h1>AeroMart Pro Store</h1>
    <p>Target web application for TestPilot AI automated crawl, test generation, and bug reproduction</p>
  </div>

  <div class="shop-container">
    <!-- Product Showcase -->
    <div class="card">
      <div class="product-img">🎧</div>
      <div class="product-title" id="product-name" data-testid="product-name">AeroPulse Noise-Cancelling Pro</div>
      <div class="product-price" id="unit-price" data-testid="unit-price">$199.00</div>
      <p class="product-desc">Next-generation spatial audio headset with dual-driver precision acoustics and 40-hour wireless battery life.</p>
      
      <label style="font-size: 13px; font-weight: 600; color: #d1d5db;">Quantity</label>
      <div class="qty-control">
        <button type="button" class="qty-btn" id="btn-qty-minus" data-testid="btn-qty-minus" onclick="adjustQty(-1)">−</button>
        <span class="qty-val" id="qty-display" data-testid="qty-display">1</span>
        <button type="button" class="qty-btn" id="btn-qty-plus" data-testid="btn-qty-plus" onclick="adjustQty(1)">+</button>
      </div>

      <div class="summary-box">
        <div class="summary-line"><span>Subtotal:</span><span id="subtotal-display" data-testid="subtotal-display">$199.00</span></div>
        <div class="summary-line"><span>Discount:</span><span id="discount-display" data-testid="discount-display">$0.00</span></div>
        <div class="summary-line summary-total"><span>Total:</span><span id="total-display" data-testid="total-display">$199.00</span></div>
      </div>
    </div>

    <!-- Checkout Form -->
    <div class="card">
      <h2 style="font-size: 18px; font-weight: 700; margin-bottom: 16px;">Express Checkout</h2>
      <form id="checkout-form" onsubmit="event.preventDefault(); handleCheckout();">
        <div class="form-group">
          <label for="customer-name">Full Name *</label>
          <input type="text" id="customer-name" name="customerName" data-testid="customer-name" class="form-control" placeholder="Jane Doe" required />
        </div>

        <div class="form-group">
          <label for="customer-email">Email Address *</label>
          <input type="email" id="customer-email" name="customerEmail" data-testid="customer-email" class="form-control" placeholder="jane@example.com" required />
        </div>

        <div class="form-group">
          <label for="promo-code">Promo Code</label>
          <div class="promo-row">
            <input type="text" id="promo-code" name="promoCode" data-testid="promo-code" class="form-control" placeholder="Try DISCOUNT50 or BUGGY200" />
            <button type="button" class="btn-apply" id="btn-apply-promo" data-testid="btn-apply-promo" onclick="applyPromo()">Apply</button>
          </div>
          <span id="promo-feedback" style="font-size: 12px; margin-top: 4px; display: block;"></span>
        </div>

        <div class="form-group">
          <label for="card-number">Card Number *</label>
          <input type="text" id="card-number" name="cardNumber" data-testid="card-number" class="form-control" placeholder="4242 •••• •••• 4242" required />
        </div>

        <button type="submit" id="btn-submit-order" data-testid="btn-submit-order" class="checkout-btn">
          Complete Purchase (<span id="btn-price-display">$199.00</span>)
        </button>

        <div id="status-banner" class="banner" data-testid="status-banner"></div>
      </form>
    </div>
  </div>

  <div class="hint-box">
    <strong>💡 Built-in Edge Case Bugs for Live Hackathon Testing:</strong><br>
    • <b>Zero-Quantity Bug:</b> Decreasing quantity below 1 allows placing an order for <b>$0.00</b> without blocking.<br>
    • <b>Promo Crash Bug:</b> Applying promo code <code>BUGGY200</code> results in a negative total and triggers an unhandled JavaScript calculation crash.<br>
    • <b>Email Formatting Edge Case:</b> Entering <code>admin@</code> without top-level domain passes HTML5 but fails downstream validation with error alert.
  </div>

  <script>
    let unitPrice = 199.00;
    let qty = 1;
    let discount = 0;

    function updateCalculations() {
      // Intentional edge-case flaw: does not prevent qty <= 0 from producing $0 totals
      const subtotal = Math.max(0, qty * unitPrice);
      let total = subtotal - discount;

      // Intentional Bug when total is negative: throws JS error if BUGGY200 is used
      if (discount > 199 && total < 0) {
        console.error("Uncaught RangeError: Checkout total cannot be negative (-$" + Math.abs(total) + ") at recalculateCart()");
        throw new Error("Critical Checkout Math Error: Total is negative");
      }

      document.getElementById('qty-display').innerText = qty;
      document.getElementById('subtotal-display').innerText = '$' + subtotal.toFixed(2);
      document.getElementById('discount-display').innerText = '-$' + discount.toFixed(2);
      document.getElementById('total-display').innerText = '$' + total.toFixed(2);
      document.getElementById('btn-price-display').innerText = '$' + total.toFixed(2);
    }

    function adjustQty(delta) {
      // Intentional Bug: Quantity can drop to 0 or negative!
      qty += delta;
      updateCalculations();
    }

    function applyPromo() {
      const code = document.getElementById('promo-code').value.trim().toUpperCase();
      const feedback = document.getElementById('promo-feedback');

      if (code === 'DISCOUNT50') {
        discount = 50.00;
        feedback.style.color = '#34d399';
        feedback.innerText = '✓ Promo applied: $50 off!';
      } else if (code === 'BUGGY200') {
        discount = 300.00; // Will cause negative total and JS crash
        feedback.style.color = '#f87171';
        feedback.innerText = 'Warning: Over-discount promo triggered';
      } else {
        discount = 0;
        feedback.style.color = '#f87171';
        feedback.innerText = 'Invalid promo code.';
      }
      try {
        updateCalculations();
      } catch (err) {
        const banner = document.getElementById('status-banner');
        banner.className = 'banner error';
        banner.innerText = 'Application Exception: ' + err.message;
      }
    }

    function handleCheckout() {
      const name = document.getElementById('customer-name').value.trim();
      const email = document.getElementById('customer-email').value.trim();
      const card = document.getElementById('card-number').value.trim();
      const banner = document.getElementById('status-banner');

      // Edge case bug: Qty 0 allows order placement
      if (qty <= 0) {
        banner.className = 'banner error';
        banner.innerText = 'BUG DETECTED: Order processed with invalid quantity ' + qty + ' ($0.00 checkout allowed)!';
        return;
      }

      if (!name || !email || !card) {
        banner.className = 'banner error';
        banner.innerText = 'Please complete all required fields.';
        return;
      }

      // Successful order
      banner.className = 'banner success';
      banner.innerText = '🎉 Order Confirmed! Order #AP-' + Math.floor(100000 + Math.random() * 900000) + ' for ' + name;
    }
  </script>
</body>
</html>
"""
