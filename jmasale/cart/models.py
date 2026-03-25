from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User
from product.models import Product
from core.models import BaseModel

class Cart(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
class CartItem(BaseModel):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity} "