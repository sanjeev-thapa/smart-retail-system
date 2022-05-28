<?php

namespace App\Http\Controllers\v1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreBasketRequest;
use App\Http\Requests\UpdateBasketRequest;
use App\Models\Basket;
use App\Traits\SystemResponse;

class BasketController extends Controller
{
    use SystemResponse;

    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        return $this->success(Basket::latest()->paginate(15));
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \App\Http\Requests\StoreBasketRequest  $request
     * @return \Illuminate\Http\Response
     */
    public function store(StoreBasketRequest $request)
    {
        $validated = $request->validated();
        Basket::create($validated + ['user_id' => auth()->user()->id]);
        return $this->success('Basket Created Successfully', 201);
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Models\Basket  $basket
     * @return \Illuminate\Http\Response
     */
    public function show(Basket $basket)
    {
        return $this->success($basket);
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \App\Http\Requests\UpdateBasketRequest  $request
     * @param  \App\Models\Basket  $basket
     * @return \Illuminate\Http\Response
     */
    public function update(UpdateBasketRequest $request, Basket $basket)
    {
        $validated = $request->validated();
        $basket->update($validated + ['user_id' => auth()->user()->id]);
        return $this->success('Baket Updated Successfully');
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Models\Basket  $basket
     * @return \Illuminate\Http\Response
     */
    public function destroy(Basket $basket)
    {
        $basket->delete();
        return $this->success('Basket Deleted Successfully');
    }
}
