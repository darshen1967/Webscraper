<!DOCTYPE html>
<html>
<head>
    <title>Web Scraping Form</title>
    <!-- Bootstrap CSS -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/5.1.0/css/bootstrap.min.css" rel="stylesheet">
    <!-- Custom CSS for Purple Theme -->
    <style>
        body {
            background-color: #f2e6ff; /* Light purple background */
        }
        .purple-theme {
            background-color: #e6ccff; /* Lighter purple for form background */
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .btn-purple {
            background-color: #6a1b9a; /* Darker purple for buttons */
            color: white;
        }
        .btn-purple:hover {
            background-color: #5c177d;
        }
    </style>
</head>
<body>
    <div class="container my-4">
        <div class="row justify-content-center">
            <div class="col-md-6 purple-theme">
                <h1 class="text-center">Web Scraping Input Form</h1>
                <form action="/handle-form" method="POST" class="my-3">
                    {{{csrf_field()}}} <!-- CSRF token for security -->

                    <div class="mb-3">
                        <label for="url" class="form-label">Enter a URL:</label>
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
                            <label for="next_button_xpath" class="form-label">Enter the XPath for the 'Next' button:</label>
                            <input type="text" class="form-control" id="next_button_xpath" name="next_button_xpath">
                        </div>

                        <div class="mb-3">
                            <label for="disabled_class" class="form-label">Enter the class name when the 'Next' button is disabled:</label>
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
</body>
</html>
