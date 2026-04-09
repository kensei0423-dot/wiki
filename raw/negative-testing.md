---
title: Test error conditions with negative testing
slug: /tools/sandbox/negative-testing/
createTime: '2024-08-15T07:22:31.755Z'
updateTime: '2024-09-24T00:48:38.008Z'
---


# Test error conditions with negative testing


**Important:** Negative testing in the sandbox is in beta.

Negative testing lets you force the flows through specific error conditions that you want to test to ensure you handle errors correctly. Use negative testing to trigger the following types of errors:

- Errors that result from calling a PayPal API.
- Errors related to Virtual Terminal and the DoDirectPayment operation, which relate to verification and credit card validation errors.

You can force two types of API errors: errors related to the transaction amount, and errors not related to the transaction amount.

## Know before you code
Negative testing is only available for use with the following:

- Sandbox environments. You cannot force or simulate error conditions in the live PayPal environment.
- Classic PayPal API versions 2.4 and later.
- Business accounts.

## Enable negative testing
- Go to the [developer.paypal.com](/) home page. Log into the Dashboard and select the menu below your name to select **Dashboard** .
- Under the **Sandbox** heading in the left navigation column, select **Accounts** .
- Locate the sandbox account for which you wish to enable negative testing. Choose a business sandbox account or you won't see the options you need.
- In the **Manage Accounts** column, select the **...** symbol to display the menu choices.
- Select **View/Edit Account** to see the **Account Details** page that has the **Profile** tab selected by default.
- Select the **Settings** tab to display a list of options you can set.
- Set the **Negative Testing** option to **On** .

The sandbox is now in the negative testing state for transactions that include the merchant. Without this configuration, the sandbox does not raise error conditions unless the error occurs through normal transaction processing.

## Test methods
In the PayPal sandbox, you can pass inputs to simulate scenarios that mimic the actual API responses without calling downstream services.

You can use the following methods to conduct negative testing in the sandbox:

- [Simulate negative responses with request headers](/tools/sandbox/negative-testing/request-headers/) .
- [Simulate negative responses with test values](/tools/sandbox/negative-testing/test-values/) .
