from rest_framework import routers

from .views import ProductViewSet, CategoryViewSet, DepartmentViewSet


router = routers.DefaultRouter()

router.register(r"v1/products", ProductViewSet)
router.register(r"v1/categories", CategoryViewSet)
router.register(r"v1/departments", DepartmentViewSet)
