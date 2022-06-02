<?php

namespace App\Exceptions;

use Exception;
use Throwable;
use App\Traits\SystemResponse;
use Illuminate\Http\Response;
use Illuminate\Auth\AuthenticationException;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\ModelNotFoundException;
use Illuminate\Validation\ValidationException;
use Symfony\Component\HttpKernel\Exception\HttpException;
use Illuminate\Foundation\Exceptions\Handler as ExceptionHandler;
use Illuminate\Support\Facades\Http;

class Handler extends ExceptionHandler
{
    use SystemResponse;

    /**
     * A list of exception types with their corresponding custom log levels.
     *
     * @var array<class-string<\Throwable>, \Psr\Log\LogLevel::*>
     */
    protected $levels = [
        //
    ];

    /**
     * A list of the exception types that are not reported.
     *
     * @var array<int, class-string<\Throwable>>
     */
    protected $dontReport = [
        //
    ];

    /**
     * A list of the inputs that are never flashed to the session on validation exceptions.
     *
     * @var array<int, string>
     */
    protected $dontFlash = [
        'current_password',
        'password',
        'password_confirmation',
    ];

    /**
     * Register the exception handling callbacks for the application.
     *
     * @return void
     */
    public function register()
    {
        $this->reportable(function (Throwable $e) {
            //
        });

        $this->renderable(function (Exception $e, $request) {
            if($e instanceof AuthenticationException)
                return $this->error(Response::$statusTexts[Response::HTTP_UNAUTHORIZED], Response::HTTP_UNAUTHORIZED);

            if($e instanceof ValidationException)
                return $this->error($e->getMessage(), Response::HTTP_UNPROCESSABLE_ENTITY);
                // return $this->error($e->errors(), Response::HTTP_UNPROCESSABLE_ENTITY);

            if(method_exists($e, 'getPrevious') && $e->getPrevious() instanceof ModelNotFoundException)
                return $this->error(\Str::headline(class_basename($e->getPrevious()->getModel())) . ' ' . Response::$statusTexts[Response::HTTP_NOT_FOUND], Response::HTTP_NOT_FOUND);

            if($e instanceof HttpException)
                return $this->error(Response::$statusTexts[$e->getStatusCode()], $e->getStatusCode());

            \Log::error($e);
            return $this->error();
        });
    }
}
