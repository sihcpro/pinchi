from rest_framework import routers

from .views import (
    ProductDiscountViewSet,
    UserDiscountViewSet,
    UsedDiscountViewSet,
    OrderItemViewSet,
    OrderViewSet,
)


router = routers.DefaultRouter()

router.register(r"v1/product-discounts", ProductDiscountViewSet)
router.register(r"v1/user-discounts", UserDiscountViewSet)
router.register(r"v1/used-discounts", UsedDiscountViewSet)
router.register(r"v1/order-items", OrderItemViewSet)
router.register(r"v1/orders", OrderViewSet)
