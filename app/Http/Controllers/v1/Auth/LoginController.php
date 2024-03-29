<?php

namespace App\Http\Controllers\v1\Auth;

use App\Models\User;
use Illuminate\Http\Request;
use App\Traits\SystemResponse;
use App\Http\Controllers\Controller;

class LoginController extends Controller
{   
    use SystemResponse;

    public function username()
    {
        return 'username';
    }

    /**
     * Get a JWT via given credentials.
     *
     * @return \Illuminate\Http\JsonResponse
     */
    public function login(Request $request)
    {
        if (! $token = auth()->attempt($request->only(['username', 'password']))) {
            abort(401, 'Unauthorized');
        }

        return $this->respondWithToken($token);
    }

    public function rfidLogin(Request $request)
    {
        $user = User::where('rfid', cache()->get('scan'))->first();
        if(!$user || !cache()->get('scan')){
            abort(401, 'Unauthorized'); 
        }
        return $this->respondWithToken(auth()->login($user));
    }

    public function me()
    {
        return $this->success(auth()->user());
    }

    /**
     * Get the token array structure.
     *
     * @param  string $token
     *
     * @return \Illuminate\Http\JsonResponse
     */
    protected function respondWithToken($token)
    {
        return $this->success([
            'access_token' => $token,
            'token_type' => 'bearer',
            'expires_in' => auth()->factory()->getTTL() * 60
        ]);
    }
}
