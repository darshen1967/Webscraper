<!DOCTYPE html>
<html>
<head>
    <title>Scraping Results</title>
    <!-- Add any additional head content here -->
</head>
<body>
    <div class="container">
        <h1>Scraping Results</h1>
        @if(!empty($output))
            <h2>Output from Python Script:</h2>
            <pre>{{ print_r($output) }}</pre>
        @else
            <p>No results to display.</p>
        @endif
    </div>
</body>
</html>
