Integrate PayPal Checkout
Before beginning your integration, you need to set up your development environment. You can refer to this flow diagram, and watch a video demonstrating how to integrate PayPal Checkout.

Start your integration by grabbing the sample code from PayPal's GitHub repo, or visiting the PayPal GitHub Codespace. Read the Codespaces guide for more information. You can also use Postman to explore and test PayPal APIs. Read the Postman Guide for more information.

1. Integrate front end CLIENT
Set up your front end to integrate checkout payments.

Front-end process
Your app shows the PayPal checkout buttons.
Your app calls server endpoints to create the order and capture payment.

Front-end code
This example uses a index.html file to show how to set up the front end to integrate payments.

The /src/index.html and /src/app.js files handle the client-side logic and define how the PayPal front-end components connect with the back end.

Step 1. Add the script tag
Include the <script> tag on any page that shows the PayPal buttons.

Step 2. Configure your script parameters
Pass client-id and specify components (Buttons, Marks, Card Fields). Can also pass currency (USD).
Buyer Country and Currency are only for use in sandbox testing.

Step 3. Render the PayPal buttons
The paypal namespace has a Buttons function that initiates the callbacks needed to set up a payment.
- createOrder callback: launches when customer clicks payment button, returns order ID
- onApprove callback: launches when payment is completed

Step 4. Configure the layout of the Buttons component (OPTIONAL)
Style options: Button Shape (Rectangle/Pill), Color (Gold), Layout (Vertical/Horizontal), Label Text, Message.

Step 5. Support multiple shipping options (OPTIONAL)
- onShippingAddressChange callback
- onShippingOptionsChange callback

Contact Module (OPTIONAL)
Three contact preferences:
- NO_CONTACT_INFO [Default]: hidden
- UPDATE_CONTACT_INFO: buyers can add/update contact details
- RETAIN_CONTACT_INFO: buyers can see but not edit

2. Integrate back end SERVER
PayPal Server SDK provides integration access to PayPal REST APIs:
- Orders Controller: Orders API v2
- Payments Controller: Payments API v2

Backend process:
1. App creates order by calling ordersCreate method
2. App calls ordersCapture method when payer confirms

Server side code runs on port 8080.
PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET as environment variables.
SDK clients configured to connect to PayPal's sandbox API by default.

Step 1. Generate access token
Initialize Server SDK client using OAuth 2.0 Client Credentials.

Step 2. Create Order
createOrder function makes request to ordersCreate method.
Intent: CAPTURE or AUTHORIZE.

Step 3: Capture Payment
captureOrder function makes request to ordersCapture method.

Enable App Switch (OPTIONAL)
Client Side: Add appSwitchWhenAvailable: true to Buttons component.
Server Side: POST to Create order endpoint with app_switch_preference object (return_url, cancel_url).

3. Custom Integration (OPTIONAL)

Handle buyer checkout errors
Use onError callbacks and alternate checkout pages.

Handle funding failures
Orders API returns INSTRUMENT_DECLINED error. Restart payment so payer can select different option.

Show cancellation page
Show page to confirm payment was cancelled.

Refund a captured payment
Refund from seller back to buyer.

4. Test integration
Test in sandbox environment before going live.

PayPal Payment test:
1. Select PayPal button
2. Log in with personal sandbox account
3. Note purchase amount
4. Approve with Pay Now
5. Confirm money reached business account

Card payment test:
1. Go to checkout page
2. Generate test card
3. Enter card details and submit
4. Confirm order processed
5. Check merchant sandbox account

5. Go live
1. Log into PayPal Developer Dashboard with business account
2. Obtain live credentials
3. Include new credentials and update endpoint
