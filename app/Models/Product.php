<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Product extends Model
{
    use HasFactory;

    protected $fillable = [
        'name',
        'image',
        'stock',
        'price',
        'user_id',
        'category_id'
    ];

    protected $with = ['user', 'category'];

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function category()
    {
        return $this->belongsTo(Category::class);
    }

    public function rfid()
    {
        return $this->hasMany(RFID::class);
    }

    public function basketItems()
    {
        return $this->hasMany(BasketItem::class);
    }

    public function orderItems()
    {
        return $this->hasMany(OrderItem::class);
    }
}
