from rest_framework import routers

from .views import CartItemViewSet

router = routers.DefaultRouter()

router.register(r"v1/carts", CartItemViewSet)
