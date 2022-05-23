<?php

namespace App\Traits;

use Illuminate\Http\Response;

trait SystemResponse
{
    public function success($message, $statusCode = 200)
    {
        return $this->format($message, $statusCode);
    }

    public function error($message = 'Internal Server Error', $statusCode = 500)
    {
        return $this->format($message, $statusCode);
    }

    private function format($message, $statusCode)
    {
        $statusCode = array_key_exists($statusCode, Response::$statusTexts) ? $statusCode : 500;

        return response()->json([
            'error' => !($statusCode >= 200 && $statusCode < 300),
            'message' => $message
        ], $statusCode);
    }
}