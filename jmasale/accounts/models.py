from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from core.constants import ROLE_CHOICES, ROLE_CUSTOMER
from core.models import BaseModel

class User(AbstractUser, BaseModel):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'superadmin'
        super().save(*args, **kwargs)