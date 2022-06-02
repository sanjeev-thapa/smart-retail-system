<?php

namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Customer>
 */
class CustomerFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition()
    {
        return [
            'name' => $this->faker->name(),
            'email' => $this->faker->unique()->safeEmail(),
            'phone' => $this->getPhone(),
            'address' => $this->faker->address(),
            'gender' => rand() % 2 == 0 ? 'm' : 'f',
            'is_walk_in' => 'f',
            'user_id' => User::first()->id,
        ];
    }

    public function getPhone()
    {
        $postNumber = substr(str_replace('.', '', microtime(true)), 5, -1);
        if (strlen($postNumber) != 6)
            $this->getPhone();
        return 98 . $postNumber;
    }
}
