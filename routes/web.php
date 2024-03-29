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
        Route::post('rfid-login', 'LoginController@rfidLogin');
        Route::get('me', 'LoginController@me')->middleware('auth');
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

        // Basket Item
        Route::apiResource('basket-items', 'BasketItemController');

        // Orders
        Route::apiResource('orders', 'OrderController');

        // Order Items
        Route::apiResource('order-items', 'OrderItemController');
    });

    // Arduino
    Route::group(['prefix' => 'arduino'], function(){
        Route::get('get', 'ArduinoController@get');
        Route::get('scan', 'ArduinoController@scan');
        Route::get('paid-status/{rfid}', 'ArduinoController@paidStatus');
    });
});