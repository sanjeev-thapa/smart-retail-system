<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class RFID extends Model
{
    use HasFactory;

    protected $table = 'rfids';

    protected $fillable = [
        'rfid',
        'is_paid',
        'product_id'
    ];

    protected $appends = ['linked_date'];

    protected $with = ['product'];

    public function getLinkedDateAttribute()
    {
        return $this->created_at->diffForHumans();
    }

    public function product()
    {
        return $this->belongsTo(Product::class);
    }

    public function orderItems()
    {
        return $this->hasMany(OrderItem::class);
    }
}
