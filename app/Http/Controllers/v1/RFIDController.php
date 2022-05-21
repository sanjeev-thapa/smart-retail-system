<?php

namespace App\Http\Controllers\v1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreRFIDRequest;
use App\Http\Requests\UpdateRFIDRequest;
use App\Models\RFID;

class RFIDController extends Controller
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
     * @param  \App\Http\Requests\StoreRFIDRequest  $request
     * @return \Illuminate\Http\Response
     */
    public function store(StoreRFIDRequest $request)
    {
        //
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Models\RFID  $rFID
     * @return \Illuminate\Http\Response
     */
    public function show(RFID $rFID)
    {
        //
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  \App\Models\RFID  $rFID
     * @return \Illuminate\Http\Response
     */
    public function edit(RFID $rFID)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \App\Http\Requests\UpdateRFIDRequest  $request
     * @param  \App\Models\RFID  $rFID
     * @return \Illuminate\Http\Response
     */
    public function update(UpdateRFIDRequest $request, RFID $rFID)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Models\RFID  $rFID
     * @return \Illuminate\Http\Response
     */
    public function destroy(RFID $rFID)
    {
        //
    }
}
