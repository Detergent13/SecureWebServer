<?php
//error_reporting(E_ALL);
// Set PHP to display errors instead of hiding them
//ini_set('display_errors', 1);
// Alternatively, you can use display_startup_errors for errors that occur during PHP's startup sequence
//ini_set('display_startup_errors', 1);

// Function to generate MD5 hash and return the last 5 characters
function generateHash($phoneNumber, $filePath) {
    if (!file_exists($filePath)) {
        return false; // If the file doesn't exist, return false
    }
    $fileContent = file_get_contents($filePath);
    $fileHash = md5($fileContent);
    $combinedHash = md5($phoneNumber . $fileHash);
    return substr($combinedHash, -5); // Return last 5 characters
}

// Sanitize input data
$firstName = filter_input(INPUT_POST, 'firstName', FILTER_SANITIZE_STRING);
$lastName = filter_input(INPUT_POST, 'lastName', FILTER_SANITIZE_STRING);
$phoneNumber = filter_input(INPUT_POST, 'phoneNumber', FILTER_SANITIZE_STRING);
$item = filter_input(INPUT_POST, 'item', FILTER_SANITIZE_STRING);

// Generate hashes for each file and the phone number
$hashMainPage = generateHash($phoneNumber, '/var/www/html/index.php');
//$hashFlagRoot = generateHash($phoneNumber, '/root/flag.txt');  // Assuming access permission are correctly set
$hashFlagWww = generateHash($phoneNumber, '/var/www/flag.txt');

// Check if all hashes were generated successfully
if ($hashMainPage === false || $hashFlagWww === false) {
    die('Error generating one or more hashes. Please check file paths and permissions.');
}

// Fetch the first transaction ID from the database and generate its hash
$dbFile = '/var/db/orders.db';
$db = new SQLite3($dbFile);
$result = $db->query("SELECT transactionId FROM orders ORDER BY id ASC LIMIT 1");
$firstRecord = $result->fetchArray();
$firstTransactionHash = $firstRecord ? generateHash($phoneNumber, $firstRecord['transactionId']) : '';

// Combine the last 5 characters of each hash with a hyphen and append the first transaction hash
$transactionId = implode('-', [$hashMainPage, $hashFlagWww]);

// Prepare and execute the insert statement
$stmt = $db->prepare("INSERT INTO orders (firstName, lastName, phoneNumber, item, transactionId, clientIP, submittedAt) VALUES (?, ?, ?, ?, ?, ?, ?)");
$stmt->bindValue(1, $firstName, SQLITE3_TEXT);
$stmt->bindValue(2, $lastName, SQLITE3_TEXT);
$stmt->bindValue(3, $phoneNumber, SQLITE3_TEXT);
$stmt->bindValue(4, $item, SQLITE3_TEXT);
$stmt->bindValue(5, $transactionId, SQLITE3_TEXT);
$stmt->bindValue(6, $_SERVER['REMOTE_ADDR'], SQLITE3_TEXT);
$stmt->bindValue(7, time(), SQLITE3_INTEGER);

if ($stmt->execute()) {
    echo "Order Submitted Successfully. Your transaction ID is: $transactionId";
} else {
    echo "Failed to submit your order. Please try again. Error: " . $db->lastErrorMsg();
}

?>

