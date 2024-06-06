<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Diagon Alley Order Form</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Tangerine:wght@700&family=Roboto:wght@400;500&display=swap" rel="stylesheet">
    <style>
        body {
            background-color: #121212; /* Dark background */
            color: #E0E0E0; /* Lighter text */
            font-family: 'Roboto', sans-serif; /* Roboto for body text */
        }
        .container {
            max-width: 600px;
            margin: 30px auto;
            padding: 20px;
            background-color: #1E1E1E; /* Slightly lighter dark shade for the form background */
            border-radius: 8px;
        }
        h2 {
            font-family: 'Tangerine', cursive; /* Tangerine for the heading */
            font-size: 48px; /* Increased size for a dramatic effect */
            color: #FFD700; /* Magical, gold-like color */
            margin-bottom: 20px; /* Spacing below the heading */
            text-align: center;
        }
        .form-control, .btn-primary {
            background-color: #333;
            border: 1px solid #444;
            color: #FFF;
        }
        .btn-primary {
            margin-top: 10px;
        }
        label {
            color: #BDBDBD; /* Light grey for labels */
        }
    </style>
</head>
<body>
<div class="container">
    <h2>Diagon Alley Order Form</h2>
    <form action="submit.php" method="post">
        <div class="form-group">
            <label for="firstName">First Name:</label>
            <input type="text" class="form-control" id="firstName" name="firstName" required>
        </div>
        <div class="form-group">
            <label for="lastName">Last Name:</label>
            <input type="text" class="form-control" id="lastName" name="lastName" required>
        </div>
        <div class="form-group">
            <label for="phoneNumber">Phone Number:</label>
            <input type="tel" class="form-control" id="phoneNumber" name="phoneNumber" required>
        </div>
        <div class="form-group">
            <label for="item">Select an Item:</label>
            <select class="form-control" id="item" name="item">
                <option value="Owl">Owl</option>
                <option value="Wand">Wand</option>
                <option value="Caldron">Caldron</option>
                <option value="Broomstick">Broomstick</option>
                <option value="Robe">Robe</option>
            </select>
        </div>
        <button type="submit" class="btn btn-primary">Submit Order</button>
    </form>
</div>
</body>
</html>

