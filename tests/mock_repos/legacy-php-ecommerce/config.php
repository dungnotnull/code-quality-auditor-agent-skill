<?php
// config.php - Legacy Configuration (CRITICAL SECURITY ISSUES)

// FLAW: Hardcoded database credentials
define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', '');  // FLAW: Empty root password
define('DB_NAME', 'shop_db');

// FLAW: Hardcoded API credentials
define('PAYPAL_API_USER', 'INTENTIONALLY_FAKE_PAYPAL_USER_FOR_AUDIT_TEST');
define('PAYPAL_API_PASSWORD', 'INTENTIONALLY_FAKE_PAYPAL_PASSWORD_FOR_AUDIT_TEST');  // FLAW: Hardcoded PayPal API password
define('PAYPAL_API_SIGNATURE', 'INTENTIONALLY_FAKE_PAYPAL_SIGNATURE_FOR_AUDIT_TEST');  // FLAW: Hardcoded API sig

// FLAW: Debug mode always on
define('DEBUG_MODE', true);
define('DISPLAY_ERRORS', true);  // FLAW: Error display in production

// FLAW: Weak session configuration
ini_set('session.cookie_httponly', '0');  // FLAW: JavaScript can access session cookie
ini_set('session.use_only_cookies', '0');  // FLAW: Session ID can come from URL
ini_set('session.cookie_secure', '0');  // FLAW: No HTTPS-only session cookie

// FLAW: No error logging configuration
error_reporting(E_ALL);  // FLAW: Reports everything including notices
?>
