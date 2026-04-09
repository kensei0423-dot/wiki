---
title: Pay with PayPal for one-time payments
slug: /docs/checkout/standard/best-practices/one-time/
createTime: '2025-01-09T00:39:31.952Z'
updateTime: '2025-09-17T12:05:30.686Z'
---

# Pay with PayPal for one-time payments

Pay with PayPal's one-time payment flow provides a one-click solution to accelerate your buyer's checkout experience by skipping manual data entry.

### Purpose
This guide shows best practices for merchants using Pay with PayPal to accept one-time payments for physical and digital goods.

### Who is this guide for?
Developers, designers, and product managers building ecommerce solutions for businesses selling physical goods.

## Best practices for end-to-end Pay with PayPal buyer experience

## Presenting the PayPal button
Buyers can use PayPal to check out at any point in their shopping journey. Placing payment buttons on the cart, product details page, or another page as a checkout shortcut can reduce steps to pay.

### Upstream presentment
Place PayPal button as checkout shortcut before buyer enters any information (e.g. cart page).
- Buyer gets streamlined one-click purchase
- Merchant receives buyer's shipping, billing, payment info from PayPal account

Per User Agreement: treat PayPal/Venmo equally to other payment methods, show prominently, don't present other methods earlier.

#### Best practices
- PayPal button shows earlier than other checkout flows requiring data entry
- Place Pay Later messaging close to order total
- Pass data-page-type through JavaScript SDK

#### Optional placement
- Place on product description page for quick single-product checkouts
- Show item modifiers ahead of PayPal button

Enable shipping options callback: Allow buyers to choose delivery method during checkout.

### Checkout presentment
If buyer proceeds manually: enter shipping details, select shipping method, then present PayPal button.

#### Best practices
- Identify PayPal users and proactively select PayPal option
- PayPal button should be buyer's last action
- After approval, redirect to order success page
- Pass buyer's shipping address and contact info in Create order call
- Set shipping_preference to SET_PROVIDED_ADDRESS

## Implementing PayPal to deliver the highest conversion

### Optimize buyer's PayPal login experience
- Pass buyer's email in Create order call
- For web view: PayPal experience always full height, never in iframe

### Optimize buyer's PayPal Checkout experience
- Include Pay Now button on PayPal review page
- Set up to create order when buyer selects Pay Now
- No more buyer action needed after Pay Now
- Pass shipping address and contact info for checkout-initiated transactions
- For upstream transactions: create order with all shipping options, integrate shipping callbacks
- Pass invoice line items and SKU details in Create order request
- Implement App Switch for streamlined authentication

### Pay Now flow
Diagram showing Pay Now payment flow.

## Next steps
- Message placement
- Shipping Module
- Contact Module
- Pass buyer identifier
- Configure data-page-type
- Create order
- Pass line-item details
- App Switch
