<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class OrderItem extends Model
{
    use HasFactory;

    protected $fillable = [
        'product_id',
        'rfid',
        'order_id'
    ];

    protected $with = ['product', 'rfid', 'order'];

    public function product()
    {
        return $this->belongsTo(Product::class);
    }

    public function rfid()
    {
        return $this->belongsTo(RFID::class, 'rfid', 'rfid');
    }

    public function order()
    {
        return $this->belongsTo(Order::class);
    }
}
