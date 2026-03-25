from rest_framework import Defaultrouter
from .views import OrderViewSet
router=Defaultrouter()
router.register(r'orders', OrderViewSet, basename='order')
urlpatterns = router.urls
