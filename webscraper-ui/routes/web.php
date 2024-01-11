<?php
use App\Http\Controllers\ScraperController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/', function () {
    return view('view');
});


//Route::post('/submit-url', 'ScraperController@submitUrl');

//Route::post('/submit-url', [ScraperController::class, 'submitUrl']);
//Route::post('/submit-additional-details', [ScraperController::class, 'submitAdditionalDetails']);

//Route::post('/submit-additional-details', 'ScraperController@submitAdditionalDetails');

Route::get('/scrape', [ScraperController::class, 'showForm'])->name('scrape.form');
Route::post('/handle-form', [ScraperController::class, 'handleForm'])->name('handle.form');

//Route::get('/download', [ScraperController::class, 'download'])->name('download');
Route::get('/download-csv', [ScraperController::class, 'downloadCsv'])->name('download-csv');
