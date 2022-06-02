<?php

namespace Database\Seeders;

use App\Models\User;
use App\Models\Product;
use App\Models\Category;
use Illuminate\Database\Seeder;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;

class ProductSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        // Electronics
        $electronics = Category::create(['name' => 'Electronics',  'user_id' => User::first()->id]);

        Product::create([
            'name' => 'Smart Watch',
            'stock' => rand(0,100),
            'price' => rand(),
            'category_id' => $electronics->id,
            'user_id' => User::first()->id
        ]);

        Product::create([
            'name' => 'Cooling Fan',
            'stock' => rand(0,100),
            'price' => rand(),
            'category_id' => $electronics->id,
            'user_id' => User::first()->id
        ]);


        // Clothing
        $fashion = Category::create(['name' => 'Fashion',  'user_id' => User::first()->id]);

        Product::create([
            'name' => 'Shirt',
            'stock' => rand(0,100),
            'price' => rand(),
            'category_id' => $electronics->id,
            'user_id' => User::first()->id
        ]);

        Product::create([
            'name' => 'Shoe',
            'stock' => rand(0,100),
            'price' => rand(),
            'category_id' => $electronics->id,
            'user_id' => User::first()->id
        ]);


        // Gaming Accessories
        $clothing = Category::create(['name' => 'Gaming Accessories',  'user_id' => User::first()->id]);

        Product::create([
            'name' => 'Gaming Headset',
            'stock' => rand(0,100),
            'price' => rand(),
            'category_id' => $electronics->id,
            'user_id' => User::first()->id
        ]);

        Product::create([
            'name' => 'Gaming Chair',
            'stock' => rand(0,100),
            'price' => rand(),
            'category_id' => $electronics->id,
            'user_id' => User::first()->id
        ]);
    }
}
