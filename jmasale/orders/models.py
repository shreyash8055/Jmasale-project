from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User
from product.models import Product
from core.models import BaseModel

class Order(BaseModel):
    STATUS_CHOICES=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_price=models.DecimalField(max_digits=10, decimal_places=2)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

class OrderItem(BaseModel):
    order=models.ForeignKey(Order,on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.FloatField()

   