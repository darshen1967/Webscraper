<!DOCTYPE html>
<html>
<head>
    <title>Web Scraping Form</title>
    <!-- Bootstrap CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/5.1.0/css/bootstrap.min.css" rel="stylesheet">
    <!-- Custom CSS for Purple Theme -->
    <style>
        /* Full page container */
        html, body {
            height: 100%;
            margin: 0;
        }
        body {
            background-color: #f2e6ff; /* Light purple background */
            display: flex; /* Use flexbox for centering */
            justify-content: center; /* Center horizontally */
            align-items: center; /* Center vertically */
        }
        /* Main form container styling */
        .purple-theme {
            background-color: #e6ccff; /* Lighter purple for form background */
            border-radius: 25px; /* Rounded corners */
            padding: 60px; /* Padding around the form */
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2); /* Stronger shadow for 'floating' effect */
            margin: auto; /* Auto margins for centering */
            width: 80%; /* Width of the form container */
            transform: translateY(-50%); /* Center vertically */
            max-width: 800px;
        }
        /* Button styling */
        .d-grid {
        display: flex; /* Use flexbox */
        justify-content: center; /* Center button horizontally */
        margin-top: 30px; /* Add space between the form and the button */
        }
        /* Button styling */
        .btn-purple {
            background-color: #6a1b9a; /* Darker purple for buttons */
            color: white;
            border: none; /* Remove border */
            padding: 15px 30px; /* Button padding */
            font-size: 18px; /* Larger font size */
            border-radius: 5px; /* Rounded corners for button */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for button */
            cursor: pointer; /* Cursor changes to pointer when hovering over the button */
        }
        .btn-purple:hover {
            background-color: #5c177d;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* Stronger shadow on hover */
        }
    </style>
</head>
<body>
    <!-- Main form container -->
    <div class="container my-4">
        <div class="row justify-content-center">
            <!-- Form styling class 'purple-theme' applied here -->
            <div class="shadow-lg p-3 col-md-8 purple-theme">
                <h1 class="text-center">Web Scraping Input Form</h1>
                <form action="/handle-form" method="POST" class="my-3">
                    {{{csrf_field()}}} <!-- CSRF token for security -->

                    <div class="mb-3">
                        <label for="url" class="form-label">Enter a URL:</label><br />
                        <input type="text" class="form-control" id="url" name="url" required>
                    </div>

                    <div class="mb-3">
                        <label for="continue_scraping" class="form-label">Do you want to scrape from other pages?</label>
                        <select class="form-select" id="continue_scraping" name="continue_scraping" required>
                            <option value="yes">Yes</option>
                            <option value="no" selected>No</option>
                        </select>
                    </div>

                    <div id="additional-fields" class="mb-3" style="display: none;">
                        <div class="mb-3">
                            <label for="next_button_xpath" class="form-label">Enter the XPath for the 'Next' button:</label><br />
                            <input type="text" class="form-control" id="next_button_xpath" name="next_button_xpath">
                        </div>

                        <div class="mb-3">
                            <label for="disabled_class" class="form-label">Enter the class name when the 'Next' button is disabled:</label><br />
                            <input type="text" class="form-control" id="disabled_class" name="disabled_class">
                        </div>
                    </div>

                    <div class="d-grid">
                        <button type="submit" class="btn btn-purple">Submit</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('continue_scraping').addEventListener('change', function() {
            var display = this.value === 'yes' ? 'block' : 'none';
            document.getElementById('additional-fields').style.display = display;
        });
    </script>
    <!-- JavaScript unchanged -->
</body>
</html>
