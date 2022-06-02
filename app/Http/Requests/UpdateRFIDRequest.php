<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdateRFIDRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     *
     * @return bool
     */
    public function authorize()
    {
        return auth()->check();
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, mixed>
     */
    public function rules()
    {
        return [
            'rfid' => 'sometimes|required|max:255|unique:rfids,rfid,' . $this->route()->rfid . ',rfid',
            'is_paid' => 'sometimes|required|max:1',
            'product_id' => 'sometimes|required|exists:products,id',
        ];
    }
}
