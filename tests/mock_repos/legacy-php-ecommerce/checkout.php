<?php
// checkout.php - Legacy Checkout Page (CRITICAL SECURITY FLAWS)

include('config.php');
include('functions.php');

// FLAW: No CSRF token verification
// FLAW: No rate limiting

if (['REQUEST_METHOD'] === 'POST') {
    // FLAW: Trusts all POST data without validation
     = ['name'];
     = ['email'];
     = ['card_number'];  // FLAW: Credit card number in POST, stored in session
     = ['card_expiry'];
     = ['card_cvv'];  // FLAW: CVV should NEVER be stored

    // FLAW: Store credit card details in session (PCI-DSS violation)
    ['card_number'] = ;
    ['card_cvv'] = ;

    // FLAW: No SSL verification for payment gateway
     = curl_init();
    curl_setopt(, CURLOPT_URL, 'http://payment-gateway.example.com/charge');  // FLAW: HTTP not HTTPS
    curl_setopt(, CURLOPT_POST, true);
    curl_setopt(, CURLOPT_POSTFIELDS, array(
        'card_number' => ,
        'expiry' => ,
        'cvv' => ,
        'amount' => ['amount'],  // FLAW: Client-submitted amount
    ));
    curl_setopt(, CURLOPT_SSL_VERIFYPEER, false);  // FLAW: Disables SSL verification
    curl_setopt(, CURLOPT_SSL_VERIFYHOST, false);  // FLAW: Disables host verification
     = curl_exec();
    curl_close();

    // FLAW: No response validation
    if () {
        echo "<h1>Payment processed!</h1>";
        echo "<p>Card ending in " . substr(, -4) . "</p>";  // FLAW: Partial card display
        // FLAW: No order confirmation email
        // FLAW: No receipt generation
    }
}

// Display checkout form - FLAW: XSS in all form fields
?>
<h1>Checkout</h1>
<form method="post" action="">
    <!-- FLAW: No CSRF token -->
    <label>Name:</label>
    <input type="text" name="name" value="<?php echo ['name']; ?>" />  <!-- FLAW: XSS + Reflected XSS -->
    <label>Email:</label>
    <input type="text" name="email" value="<?php echo ['email']; ?>" />  <!-- FLAW: XSS -->
    <label>Credit Card Number:</label>
    <input type="text" name="card_number" />  <!-- FLAW: type="text" not "password" -->
    <label>Expiry:</label>
    <input type="text" name="card_expiry" />
    <label>CVV:</label>
    <input type="text" name="card_cvv" />
    <!-- FLAW: No autocomplete="off" on sensitive fields -->
    <button type="submit">Pay Now</button>
</form>
