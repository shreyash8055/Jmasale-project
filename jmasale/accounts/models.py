from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from core.constants import ROLE_CHOICES, ROLE_CUSTOMER, ROLE_SUPERADMIN
from core.models import BaseModel

class User(AbstractUser, BaseModel):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = ROLE_SUPERADMIN
        super().save(*args, **kwargs)

    parent = models.ForeignKey(
    'self',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='members'
)