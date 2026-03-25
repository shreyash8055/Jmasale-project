from django.shortcuts import render

# Create your views here.
from .models import Product
from .serializers import ProductSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[IsAuthenticated]
    filter_backends=[DjangoFilterBackend]
    search_fields=['name', 'description']

    def perform_create(self, serializer):
      serializer.save(created_by=self.request.user)