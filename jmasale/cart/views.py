from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
# Create your views here.
from .models import Cart, CartItem
from product.models import Product
from .serializers import CartItemSerializer
# Create your views here.
class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    def list(self, request):
        cart = self.get_cart(request.user)
        items = cart.items.all()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    def create(self, request):
        cart = self.get_cart(request.user)
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))

        product = Product.objects.get(id=product_id)

        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product
        )


        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity

        item.save()

        return Response({"message": "Added to cart"})
    
    def destroy(self, request, pk=None):
        item = CartItem.objects.get(id=pk)
        item.delete()
        return Response({"message": "Item removed"})