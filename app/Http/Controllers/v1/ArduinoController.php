<?php

namespace App\Http\Controllers\v1;

use App\Models\RFID;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use App\Traits\SystemResponse;

class ArduinoController extends Controller
{
    use SystemResponse;

    public function scan(Request $request)
    {
        if(!empty($request->rfid)){
            cache()->forget('scan');
        }
    
        return cache()->remember('scan', 5, function () use ($request) {
            return $request->rfid;
        });
    }

    public function get()
    {
        return $this->success(RFID::where('rfid', cache()->get('scan'))->firstOrFail());
    }

    public function paidStatus($rfid)
    {
        $rfid = RFID::where('rfid', $rfid)->first();
        if(!$rfid){
            return 'n';
        }
        return $rfid->is_paid;
    }
}
