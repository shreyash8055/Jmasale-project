from django.db import models
from accounts.models import User

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.IntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name