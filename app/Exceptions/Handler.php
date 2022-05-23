<?php

namespace App\Exceptions;

use App\Traits\SystemResponse;
use Exception;
use Illuminate\Auth\AuthenticationException;
use Throwable;
use Illuminate\Foundation\Exceptions\Handler as ExceptionHandler;
use Illuminate\Http\Exceptions\HttpResponseException;
use Illuminate\Validation\ValidationException;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Exception\MethodNotAllowedHttpException;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

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
            if($e instanceof ValidationException){
                return $this->error($e->errors(), Response::HTTP_UNPROCESSABLE_ENTITY);
            }

            return $this->error($this->getMessage($e), $this->getStatusCode($e));
        });
    }

    private function getMessage($exception)
    {
        if(!empty($exception->getMessage())) {
            return $exception->getMessage();
        }

        if(!empty($exception->getStatusCode()) && array_key_exists($exception->getStatusCode(), Response::$statusTexts)) {
            return Response::$statusTexts[$exception->getStatusCode()];
        }

        return "Internal Server Error";
    }

    private function getStatusCode($exception)
    {
        if(method_exists($exception, 'getStatusCode') && !empty($exception->getStatusCode())) {
            return $exception->getStatusCode();
        }

        if(method_exists($exception, 'getCode') && !empty($exception->getCode())) {
            return $exception->getCode();
        }

        if($exception instanceof AuthenticationException) {
            return Response::HTTP_UNAUTHORIZED;
        }

        return 500;
    }
}
