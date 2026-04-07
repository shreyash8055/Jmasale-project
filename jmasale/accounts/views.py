from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from orders.models import Order
from product.models import Product

from .serializers import RegisterSerializer
from .services import create_user, authenticate_user
import logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
def register(request):
    logger.info(f"Request Data: {request.data}")
    logger.info(f"Request User: {request.user}")
    logger.info(f"Incoming request data: {request.data}")
    logger.info(f"Request made by: {request.user}")
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = create_user(serializer.validated_data)

        # If an admin is creating a member using this endpoint (by mistake),
        # ensure the new member is linked under that admin.
        if (
            request.user
            and getattr(request.user, "is_authenticated", False)
            and getattr(request.user, "role", None) in ["admin", "superadmin"]
            and user.role == "member"
            and user.parent_id is None
        ):
            user.parent = request.user
            user.save(update_fields=["parent"])
            logger.info(f"Member {user} linked to admin {request.user}")

        return Response({"message": "User created successfully"})
    logger.error(f"Validation failed: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate_user(username, password)

    if not user:
        return Response({"error": "Invalid credentials"}, status=400)

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "role": user.role
})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_member(request):
    if request.user.role not in ["admin", "superadmin"]:
        return Response({"error": "Only admin can create members"}, status=status.HTTP_403_FORBIDDEN)
    data = request.data.copy()
    data['role'] = 'member'   # force role

    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        user = create_user(serializer.validated_data)
        # Always link the created member under the logged-in admin user.
        user.parent = request.user
        user.save(update_fields=["parent"])

        logger.info(f"Admin {request.user.username} created a member")

        return Response({
            "message": "Member created successfully",
            "user_id": user.id,
            "username": user.username
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

# Admin Dash-board
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard(request):
    if request.user.role not in ["admin", "superadmin"]:
        return Response({"error": "Access denied"}, status=403)

    total_products = Product.objects.filter(
        created_by__in=[request.user] + list(request.user.members.all())
    ).count()

    total_members = request.user.members.count()

    total_orders = Order.objects.filter(user=request.user).count()

    return Response({
        "total_products": total_products,
        "product_id's": [p.id for p in Product.objects.filter(created_by=request.user)],
        "total_members": total_members,
        "total_orders": total_orders
    })