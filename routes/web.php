<?php

use Illuminate\Support\Facades\Route;


Route::get('/', function () {
    return 'Welcome to ' . env('APP_NAME');
});
