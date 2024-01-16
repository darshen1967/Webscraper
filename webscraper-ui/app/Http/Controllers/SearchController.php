<?php

namespace App\Http\Controllers;
use App\Models\Tender;

use Illuminate\Http\Request;

class SearchController extends Controller
{
    public function search(Request $request){

    $keyword = $request->keyword;

    // Assuming you want to search in the 'final' column of the tenders table
    $results = Tender::where('final', 'LIKE', "%{$keyword}%")->get();

    $searchFound = !$results->isEmpty();

    return view('results', compact('results','searchFound'));
}

public function showResults(){
    // Initialize an empty collection for $results
    $results = collect();

    // Your logic here...

    // Pass $results to the view
    return view('results', compact('results'));
}

}
