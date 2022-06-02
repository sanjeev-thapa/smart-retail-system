<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdateCustomerRequest extends FormRequest
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
            'name' => 'sometimes|required|max:255',
            'email' => 'sometimes|nullable|email|max:255|unique:customers,email,' . $this->customer->id,
            'phone' => 'sometimes|nullable|integer|unique:customers,phone,' . $this->customer->id,
            'address' => 'sometimes|nullable|max:255',
            'gender' => 'sometimes|nullable|max:1',
            'is_walk_in' => 'sometimes|required|max:1',
        ];
    }
}
