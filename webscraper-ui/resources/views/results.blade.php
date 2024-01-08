<!DOCTYPE html>
<html>
<head>
    <title>Scraping Results</title>
    <!-- Bootstrap CSS for responsive containers -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/5.1.0/css/bootstrap.min.css" rel="stylesheet">
    <!-- Custom CSS for Purple Theme -->
    <style>
        body, html {
            height: 100%;
            margin: 0;
            padding: 0; /* Ensure no padding is affecting the layout */
            font-family: Arial, sans-serif; /* Optional: Set a default font */
            background-color: #f2e6ff; /* Light purple background */
        }
        .title-container {
            background-color: #6a1b9a; /* Darker purple for title container */
            width: 100%; /* Full width */
            text-align: center; /* Center the title text */
            padding: 20px 0; /* Padding around the title */
            color: white; /* White text color */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Shadow effect */
            position: fixed; /* Fix the title to the top */
            top: 0; /* Align the title to the very top of the page */
            left: 0; /* Align the title to the left */
            z-index: 1000; /* Ensure the title stays above other content */
        }
        .output-container {
            background-color: #e6ccff; /* Lighter purple for output container */
            border-radius: 10px; /* Rounded corners */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Shadow effect */
            padding: 20px; /* Padding inside the container */
            margin-top: 80px; /* Space for the fixed title */
            padding-top: 40px; /* Additional padding to account for fixed title */
            height: calc(100% - 80px); /* Adjust height for the fixed title */
            overflow: auto; /* Enable scroll if content overflows */
        }
        pre {
            white-space: pre-wrap; /* Ensure pre-formatted text wraps */
            word-break: break-word; /* Break the word to prevent horizontal scrolling */
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="title-container">
            <h1>Scraping Results</h1>
        </div>
        <div class="output-container">
            @if(!empty($output))
                <h2>Output from Python Script:</h2>
                <pre>{{ print_r($output) }}</pre>
            @else
                <p>No results to display.</p>
            @endif
        </div>
    </div>
</body>
</html>
