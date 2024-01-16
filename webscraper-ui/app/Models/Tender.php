<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Tender extends Model
{
    use HasFactory;
    // Assuming your table name is 'tenders'. If it's different, specify it here
    protected $table = 'tenders';

    // Specify the fields that can be filled via mass assignment
    protected $fillable = ['final', 'label'];

    // If you have timestamps in your table (created_at and updated_at), leave this line
    // If not, you can disable timestamps by setting it to false
    public $timestamps = true;

    // Add other model properties and methods as needed
}
