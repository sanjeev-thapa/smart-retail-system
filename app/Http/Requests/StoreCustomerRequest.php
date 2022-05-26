<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreCustomerRequest extends FormRequest
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
            'name' => 'required|max:255',
            'email' => 'nullable|max:255|unique:customers,email',
            'phone' => 'nullable|integer|unique:customers,phone',
            'address' => 'nullable|max:255',
            'gender' => 'nullable|max:1',
            'is_walk_in' => 'required|max:1',
        ];
    }
}
