from rest_framework import DefaultRouter
from .views import CartViewSet

router=DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = router.urls