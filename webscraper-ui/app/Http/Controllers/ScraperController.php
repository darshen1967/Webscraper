<?php

namespace App\Http\Controllers;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\Process;
use Illuminate\Support\Facades\Storage;
use Illuminate\Http\Response;
use App\Models\Tender;
use League\Csv\Reader;


use Illuminate\Http\Request;

class ScraperController extends Controller
{
    public function showForm()
    {
        return view('view'); // Assuming your blade file is named 'view.blade.php'
    }

    public function handleForm(Request $request)
    {
        // Extracting details from the request
        $url = $request->input('url');
        $continueScraping = $request->input('continue_scraping');
        $nextButtonXpath = $request->input('next_button_xpath');
        $disabledClass = $request->input('disabled_class');
        //dd($url,$continueScraping,$nextButtonXpath,$disabledClass );

        $input1 = escapeshellarg($url);
        $input2 = escapeshellarg($continueScraping);
        $input3 = escapeshellarg($nextButtonXpath);
        $input4 = escapeshellarg($disabledClass);


        // Prepare the command to run the Python script
        //$process = escapeshellcmd("C:\Users\User\AppData\Local\Microsoft\WindowsApps\python3.10.exe   C:\Users\User\Desktop\FYP\Webscraper\test.py --url $url --continue $continueScraping --xpath $nextButtonXpath --disabled $disabledClass");

        //$process = escapeshellcmd('C:\Users\User\AppData\Local\Microsoft\WindowsApps\python3.10.exe'." ".'C:\Users\User\Desktop\FYP\Webscraper\webscraper-ui\test.py'. " ".$input1. " " .$input2." ". $input3." ". $input4);
        //$output = shell_exec('C:\Users\User\AppData\Local\Microsoft\WindowsApps\python3.10.exe'." ".'C:\Users\User\Desktop\FYP\Webscraper\webscraper-ui\test.py');
        //$process = new Process("C:\Users\User\AppData\Local\Microsoft\WindowsApps\python3.10.exe C:\Users\User\Desktop\FYP\Webscraper\test.py $url $continueScraping $nextButtonXpath $disabledClass");
        $pythonPath = escapeshellarg('C:\Users\User\AppData\Local\Microsoft\WindowsApps\python3.10.exe');
        $scriptPath = escapeshellarg('C:\Users\User\Desktop\FYP\Webscraper\pagination2.py');
        //$process->run();
        $command = "$pythonPath $scriptPath $input1 $input2 $input3 $input4";
        $output = shell_exec($command);
        //dd($output);


        #return view('results', ['output' => $output]);
        $data = $this->getTableData(); // Assume this is a method that retrieves your table data

        //DATABASE PART
        $csvFilePath = storage_path('app\public\download\Final_tender_list.csv');

        // Read CSV file
        $csv = Reader::createFromPath($csvFilePath, 'r');
        $csv->setHeaderOffset(0); // assuming the first row of your CSV file contains headers

        $records = $csv->getRecords();

        // Insert data into the database
        foreach ($records as $row) {
            Tender::create([
                'final' => $row['Final'],
                'label' => $row['Label'] ?? null,
            ]);
        }

        return view('results', compact('output', 'data'));

    }


        public function downloadCsv()
        {
            // Define the file path
            $filePath = "public\download\Final_tender_list.csv"; // Update 'yourfile.csv' to your actual file name

            // Check if file exists
            if (!Storage::exists($filePath)) {

                abort(404, 'File not found');
            }

            // Get file content
            $fileContent = Storage::get($filePath);

            // Create a response and force download
            return (new Response($fileContent, 200))
                  ->header('Content-Type', 'text/csv')
                  ->header('Content-Disposition', 'attachment; filename="Tender.csv"');
        }

        private function getTableData()
        {
            $filePath = storage_path("app\public\download\Final_tender_list.csv");

            // Open the file for reading
            $handle = fopen($filePath, 'r');

            $data = [];
            while (($row = fgetcsv($handle, 1000, ",")) !== FALSE) {
                $data[] = $row;
            }
            fclose($handle);

            return $data;

        }



        public function showResults(){
            // Initialize an empty collection for $results
            $results = collect();

            // Your logic here...

            // Pass $results to the view
            return view('results', compact('results'));
        }



}

