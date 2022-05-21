<?php

namespace App\Http\Controllers\v1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreBasketItemRequest;
use App\Http\Requests\UpdateBasketItemRequest;
use App\Models\BasketItem;

class BasketItemController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        //
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \App\Http\Requests\StoreBasketItemRequest  $request
     * @return \Illuminate\Http\Response
     */
    public function store(StoreBasketItemRequest $request)
    {
        //
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Models\BasketItem  $basketItem
     * @return \Illuminate\Http\Response
     */
    public function show(BasketItem $basketItem)
    {
        //
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  \App\Models\BasketItem  $basketItem
     * @return \Illuminate\Http\Response
     */
    public function edit(BasketItem $basketItem)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \App\Http\Requests\UpdateBasketItemRequest  $request
     * @param  \App\Models\BasketItem  $basketItem
     * @return \Illuminate\Http\Response
     */
    public function update(UpdateBasketItemRequest $request, BasketItem $basketItem)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Models\BasketItem  $basketItem
     * @return \Illuminate\Http\Response
     */
    public function destroy(BasketItem $basketItem)
    {
        //
    }
}
