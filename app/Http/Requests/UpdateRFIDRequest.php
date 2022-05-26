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
            'rfid' => 'required|max:255|unique:rfids,rfid,' . $this->route()->rfid->id,
            'is_paid' => 'required|max:1',
            'product_id' => 'required|exists:products,id',
        ];
    }
}
