<?php

use Illuminate\Support\Facades\Route;


Route::get('/', function () {
    return 'Welcome to ' . env('APP_NAME');
});

Route::group([
    'namespace' => 'App\Http\Controllers\v1',
    'prefix' => 'v1'
], function() {
    // Authentication
    Route::group(['namespace' => 'Auth'], function() {
        Route::post('login', 'LoginController@login')->name('login');
    });

    Route::group(['middleware' => 'auth'], function() {
        // Categories
        Route::apiResource('categories', 'CategoryController');

        // Products
        Route::apiResource('products', 'ProductController');

        // RFIDs
        Route::apiResource('rfids', 'RFIDController');

        // Customers
        Route::apiResource('customers', 'CustomerController');

        // Baskets
        Route::apiResource('baskets', 'BasketController');
    });
});