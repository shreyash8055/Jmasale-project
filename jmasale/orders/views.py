from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .tasks import send_order_confirmation
from orders.models import Order, OrderItem
import logging
logger = logging.getLogger(__name__)
class OrderViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def create(self, request):
        user = request.user
        cart = user.cart
        items = cart.items.all()
        if not items:
            return Response({"error": "Cart is empty"}, status=400)

        total_price = 0
        order = Order.objects.create(user=user, total_price=0)

        for item in items:
            product = item.product

            if product.stock < item.quantity:
                raise Exception(f"{product.name} out of stock")

            product.stock -= item.quantity
            product.save(update_fields=["stock"])

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price=product.price,
            )

            total_price += product.price * item.quantity

        order.total_price = total_price
        order.save(update_fields=["total_price"])

        items.delete()
        logger.info(f"Order placed for user {request.user}")
        send_order_confirmation.delay(user.email)
        return Response({"message": "Order placed successfully"})