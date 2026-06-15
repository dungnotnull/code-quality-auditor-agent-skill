<?php
// functions.php - Legacy Business Logic Functions (CRITICAL ISSUES)

// User authentication
function login(, ) {
    // FLAW: SQL injection - no parameterized query
     = "SELECT * FROM users WHERE username = '' AND password = ''";
     = mysql_query();  // FLAW: Deprecated mysql_query

    if (mysql_num_rows() > 0) {
         = mysql_fetch_assoc();
        ['user_id'] = ['id'];
        ['username'] = ['username'];
        ['is_admin'] = ['is_admin'];  // FLAW: Admin flag in session, easily spoofed
        return true;
    }
    return false;
}

// Password handling - CRITICAL FLAWS
function hash_password() {
    return md5();  // FLAW: MD5 is cryptographically broken for password hashing
    // FLAW: No salt - rainbow table attack
}

function verify_password(, ) {
    return md5() === ;  // FLAW: MD5 comparison, timing attack possible
}

// Product listing - FLAW: SQL injection
function get_products( = '') {
    if () {
        // FLAW: SQL injection via 
         = "SELECT * FROM products WHERE category = '' ORDER BY name";
    } else {
         = "SELECT * FROM products ORDER BY name";
    }
     = mysql_query();
     = array();
    while ( = mysql_fetch_assoc()) {
        [] = ;
    }
    return ;
}

// Order processing - CRITICAL FLAWS
function create_order(, , ) {
    // FLAW: No transaction - partial order creation on failure
    // FLAW: No input validation
    // FLAW: User-provided total amount
     = ['total'];  // FLAW: Trusting client-side total

     = "INSERT INTO orders (user_id, total, shipping_address, status, created_at)
              VALUES (, , '', 'pending', NOW())";
    // FLAW: SQL injection in 
    mysql_query();
     = mysql_insert_id();

    foreach ( as ) {
        // FLAW: No stock check before inserting order item
        // FLAW: No price verification - uses client-submitted price
         = "INSERT INTO order_items (order_id, product_id, quantity, price)
                  VALUES (, {['product_id']}, {['quantity']}, {['price']})";
        mysql_query();
    }

    // FLAW: No payment processing integration
    // FLAW: No email notification
    return ;
}

// Customer data handling - CRITICAL: No data protection
function get_customer() {
     = "SELECT * FROM customers WHERE id = ";  // FLAW: SQL injection
     = mysql_query();
    return mysql_fetch_assoc();
    // FLAW: Returns ALL customer data including credit card info, SSN, etc.
}

function update_customer(, ) {
    // FLAW: Mass assignment - any field can be updated including is_admin
     = array();
    foreach ( as  => ) {
        [] = " = ''";  // FLAW: SQL injection via key names AND values
    }
     = "UPDATE customers SET " . implode(', ', ) . " WHERE id = ";
    mysql_query();  // FLAW: No error handling
}

// Cart functions
function add_to_cart(, ) {
    // FLAW: No stock validation
    // FLAW: No quantity bounds
    ['cart'][] = ;
}

function get_cart_total() {
     = 0;
    foreach (['cart'] as  => ) {
        // FLAW: N+1 query - queries product price individually for each cart item
         = "SELECT price FROM products WHERE id = ";  // FLAW: SQL injection
         = mysql_query();
         = mysql_fetch_assoc();
         += ['price'] * ;  // FLAW: Float math for money
    }
    return ;
}

// XSS vulnerabilities throughout
function display_product() {
    // FLAW: No escaping of user-controlled data
    echo "<h2>" . ['name'] . "</h2>";  // FLAW: XSS via product name
    echo "<p>Price: $" . ['price'] . "</p>";  // FLAW: XSS via price
    echo "<p>" . ['description'] . "</p>";  // FLAW: XSS via description
    echo "<a href='/product.php?id=" . ['id'] . "'>View Details</a>";  // FLAW: XSS via ID
}

// Search function - CRITICAL: SQL injection
function search_products() {
    // FLAW: Direct user input in LIKE clause without escaping
     = "SELECT * FROM products WHERE name LIKE '%%' OR description LIKE '%%'";
     = mysql_query();
     = array();
    while ( = mysql_fetch_assoc()) {
        [] = ;
    }
    return ;
}

// File upload - CRITICAL: No validation
function upload_image() {
     = "uploads/";
     =  . basename(["image"]["name"]);  // FLAW: Original filename
    // FLAW: No file type validation
    // FLAW: No size limit
    // FLAW: No malware scan
    move_uploaded_file(["image"]["tmp_name"], );  // FLAW: Overwrites existing files
    return ;
}
?>
