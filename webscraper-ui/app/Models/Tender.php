<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Tender extends Model
{
    use HasFactory;

    $csvData = []; // assume this is populated with CSV data
    foreach ($csvData as $row) {
        Tender::create([
            'final' => $row['Final'],
            'label' => $row['Label'],
        ]);
    }
}
