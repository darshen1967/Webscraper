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
            padding: 0;
            font-family: 'Segoe UI', Arial, sans-serif;
            background-color: #FAFAFA;
        }
        .title-container {
            background-color: #5D1049;
            width: 100%;
            text-align: center;
            padding: 20px 0;
            color: white;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            position: fixed;
            top: 0;
            left: 0;
            z-index: 1000;
        }
        .output-container {
            background-color: #FFFFFF;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            padding: 20px;
            margin: 20px;
            margin-top: 80px;
            height: auto;
        }
        pre {
            white-space: pre-wrap;
            word-break: break-word;
        }
        @media (max-width: 768px) {
            .output-container {
                margin: 10px;
            }
        }
        .btn-primary {
            background-color: #5D1049; /* Adjust the color to ensure text visibility */
            border: none;
            color: white; /* This will make the text stand out against a dark background */
            padding: 10px 20px; /* Add more padding for a better button shape */
            border-radius: 25px; /* This will give you the rounded corners */
            font-weight: bold; /* Optional: makes the font bold */
            font-size: 16px; /* Increase font size for better visibility */
            transition: background-color 0.3s ease; /* Adds a transition effect when hovering over the button */
        }

        .btn-primary:hover {
            background-color: #451C3F; /* A lighter color for hover state for contrast */
            cursor: pointer; /* Changes the cursor to a pointer to indicate it's clickable */
        }

        table {
            border-collapse: collapse;
            width: 100%;
        }

        table, th, td {
            border: 1px solid #ddd;
        }

        th {
            background-color: #5D1049;
            color: white;
            padding: 10px;
            text-align: left;
        }

        td {
            padding: 10px;
        }



        .buttons-wrapper {
            display: flex; /* Use flexbox to layout buttons */
            justify-content: center; /* Center buttons horizontally */
            margin-top: 20px; /* Optional: adds some space above the button wrapper */
            margin: 0 5px;
        }

        .buttons-wrapper button {
            margin: 0 10px; /* Adds 10px margin to the left and right of each button */
        }


    </style>
</head>
<body>
    <div class="container">
        <div class="title-container">
            <h1>Scraping Results</h1>
        </div><br><br>
        <div class="output-container">
            <div class="buttons-wrapper">
                <button id="showOutputBtn" class="btn btn-primary">Raw Output</button>
                <button id="showTableBtn" class="btn btn-primary">Table</button>
            </div>
            <div id="outputSection" style="display: none;">
                @if(!empty($output))
                    <h2>Output from Python Script:</h2>
                    <pre>{{ print_r($output, true) }}</pre>
                    <br><br><a href="{{ route('download-csv') }}" class="btn btn-primary">Download CSV</a>
                @else
                    <p>Error has occured. Please check your input variables.</p>
                @endif
            </div>
            <div id="tableSection" style="display: none;">
                <h2>Table Data:</h2>
                @if(!empty($output))
                    <table>
                        <thead>
                            <tr>
                                @foreach ($data[0] as $header)
                                    <th>{{ $header }}</th>
                                @endforeach
                            </tr>
                        </thead>
                        <tbody>
                            @foreach ($data as $key => $row)
                                @if ($key > 0) <!-- Skip the header row -->
                                    <tr>
                                        @foreach ($row as $cell)
                                            <td>{{ $cell }}</td>
                                        @endforeach
                                    </tr>
                                @endif
                            @endforeach
                        </tbody>
                    </table>
                    <br><br><a href="{{ route('download-csv') }}" class="btn btn-primary">Download CSV</a>
                @else
                    <p>Error has occured. Please check your input variables.</p>
                @endif
            </div>

        </div>
    </div>

    <script>
        document.getElementById('showOutputBtn').addEventListener('click', function() {
            document.getElementById('outputSection').style.display = 'block';
            document.getElementById('tableSection').style.display = 'none';
        });

        document.getElementById('showTableBtn').addEventListener('click', function() {
            document.getElementById('outputSection').style.display = 'none';
            document.getElementById('tableSection').style.display = 'block';
        });
    </script>

</body>
</html>
