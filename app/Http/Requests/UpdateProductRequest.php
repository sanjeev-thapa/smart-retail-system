<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdateProductRequest extends FormRequest
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
            'image' => 'sometimes|nullable|max:255',
            'stock' => 'sometimes|nullable|integer|max:255',
            'price' => 'sometimes|required|numeric|max:255',
            'category_id' => 'sometimes|required|exists:categories,id',
        ];
    }
}
