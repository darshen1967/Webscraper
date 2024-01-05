<?php

namespace App\Http\Controllers;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\Process;


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
        /*
        if (!$process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }
        $output = $process->getOutput();
        */
        //$output = null;
        //$return_var = null;
        //exec($process, $output, $return_var);
        //passthru($process, $output);

        // Handle the output of the Python script
        // This part depends on how your Python script outputs data
        // You might need to parse $output or handle errors in $return_var

        // Assuming you want to return the output to another view
        //echo ("end");
        //echo ($output);
        //var_dump($output);
        //echo ($last_line);
        return view('results', ['output' => $output]);

    }
}

