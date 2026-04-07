from django.core.cache import cache

# Create your views here.
from .models import Product
from .serializers import ProductSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrMember, IsOwnerOrAdmin
import logging

logger = logging.getLogger(__name__)

class ProductViewSet(ModelViewSet):
    def dispatch(self, request, *args, **kwargs):
        # Log early so we can see requests even if permissions fail.
        user = getattr(request, "user", None)
        logger.info(
            "ProductViewSet action=%s method=%s path=%s user=%s role=%s",
            getattr(self, "action", None),
            request.method,
            request.path,
            getattr(user, "username", None),
            getattr(user, "role", None),
        )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, "role", None)
        logger.info("ProductViewSet get_queryset role=%s user=%s", role, user)

        if role in ["admin", "superadmin"]:
            return Product.objects.filter(
                created_by__in=[user] + list(user.members.all())
            )

        if role == 'member':
            return Product.objects.filter(created_by=user)

        return Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    search_fields = ["name", "description"]

    def perform_create(self, serializer):
        logger.info(
            "ProductViewSet perform_create user=%s role=%s",
            getattr(self.request.user, "username", None),
            getattr(self.request.user, "role", None),
        )
        serializer.save(created_by=self.request.user)
        cache.delete("product_list")

    def get_permissions(self):
        if self.action in ["create"]:
            return [IsAuthenticated(), IsAdminOrMember()]

        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrAdmin()]

        # list/retrieve/etc: require authentication
        return [IsAuthenticated()]
    

    def list(self, request, *args, **kwargs):
        cache_key = "product_list"

        data = cache.get(cache_key)
        if not data:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set(cache_key, data, timeout=60)  # cache 60 sec

        from rest_framework.response import Response

        return Response(data)