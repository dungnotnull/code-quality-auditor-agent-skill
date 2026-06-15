<?php
// index.php - Legacy PHP E-Commerce Entry Point (CRITICAL STATE - INTENTIONALLY TERRIBLE)
// Written in 2009, patched by multiple contractors. No framework. Procedural style.

session_start();

// FLAW: No CSRF protection on any form
// FLAW: No Content-Security-Policy headers
// FLAW: No X-Frame-Options header

// Database connection - FLAW: Hardcoded credentials
mysql_connect('localhost', 'root', '');  // FLAW: mysql_* deprecated since PHP 5.5, removed in PHP 7
mysql_select_db('shop_db');  // FLAW: No error handling on connection failure

// FLAW: No autoloader, manual includes with relative paths
include('config.php');
include('functions.php');
include('header.php');

// FLAW: Global state everywhere
global , , , ;

 = isset(['page']) ? ['page'] : 'home';

// FLAW: Path traversal - user input directly in include
if (file_exists( . '.php')) {
    include( . '.php');  // FLAW: LFI vulnerability - ?page=../../etc/passwd%00
} else {
    include('404.php');
}

include('footer.php');
?>
