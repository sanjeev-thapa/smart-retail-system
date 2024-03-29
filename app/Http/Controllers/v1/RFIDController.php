<?php

namespace App\Http\Controllers\v1;

use App\Http\Controllers\Controller;
use App\Http\Requests\StoreRFIDRequest;
use App\Http\Requests\UpdateRFIDRequest;
use App\Models\RFID;
use App\Traits\SystemResponse;

class RFIDController extends Controller
{
    use SystemResponse;

    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        return $this->success(RFID::latest()->paginate(15));
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \App\Http\Requests\StoreRFIDRequest  $request
     * @return \Illuminate\Http\Response
     */
    public function store(StoreRFIDRequest $request)
    {
        $validated = $request->validated();
        RFID::create($validated);
        return $this->success('RFID created Successfully', 201);
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Models\RFID  $rfid
     * @return \Illuminate\Http\Response
     */
    public function show($rfid)
    {
        return $this->success(RFID::where(compact('rfid'))->firstOrFail());
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \App\Http\Requests\UpdateRFIDRequest  $request
     * @param  \App\Models\RFID  $rfid
     * @return \Illuminate\Http\Response
     */
    public function update(UpdateRFIDRequest $request, $rfid)
    {
        $validated = $request->validated();
        RFID::where(compact('rfid'))->firstOrFail()->update($validated);
        return $this->success('RFID Updated Successfully');
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Models\RFID  $rfid
     * @return \Illuminate\Http\Response
     */
    public function destroy($rfid)
    {
        RFID::where(compact('rfid'))->firstOrFail()->delete();
        return $this->success('RFID Deleted Successfully');
    }
}
