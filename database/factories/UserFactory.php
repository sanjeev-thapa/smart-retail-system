<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\User>
 */
class UserFactory extends Factory
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
            'email_verified_at' => now(),
            'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
            'phone' => $this->getPhone(),
            'username' => $this->faker->userName(),
            'dob' => $this->faker->dateTimeBetween('1990-01-01', '2012-12-31')->format('Y/m/d'),
            'gender' => rand() % 2 == 0 ? 'M' : 'F',
            'remember_token' => Str::random(10),
        ];
    }

    /**
     * Indicate that the model's email address should be unverified.
     *
     * @return static
     */
    public function unverified()
    {
        return $this->state(function (array $attributes) {
            return [
                'email_verified_at' => null,
            ];
        });
    }

    public function getPhone()
    {
        $postNumber = substr(str_replace('.', '', microtime(true)), 5, -1);
        if (strlen($postNumber) != 6)
            $this->getPhone();
        return 98 . $postNumber;
    }
}
