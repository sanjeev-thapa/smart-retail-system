<?php

namespace App\Http\Controllers\v1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreBasketItemRequest;
use App\Http\Requests\UpdateBasketItemRequest;
use App\Models\BasketItem;
use App\Traits\SystemResponse;

class BasketItemController extends Controller
{
    use SystemResponse;

    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        return $this->success(BasketItem::latest()->paginate(15));
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \App\Http\Requests\StoreBasketItemRequest  $request
     * @return \Illuminate\Http\Response
     */
    public function store(StoreBasketItemRequest $request)
    {
        $validated = $request->validated();
        BasketItem::create($validated);
        return $this->success('Basket Item Created Successfully', 201);
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Models\BasketItem  $basketItem
     * @return \Illuminate\Http\Response
     */
    public function show(BasketItem $basketItem)
    {
        return $this->success($basketItem);
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
        $validated = $request->validated();
        $basketItem->update($validated);
        return $this->success('Basket Item Updated Successfully');
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Models\BasketItem  $basketItem
     * @return \Illuminate\Http\Response
     */
    public function destroy(BasketItem $basketItem)
    {
        $basketItem->delete();
        return $this->success('Basket Item Deleted Successfully');
    }
}
