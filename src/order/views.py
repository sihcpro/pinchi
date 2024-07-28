from django.db.models import Q
from rest_framework import viewsets

from user.enums import UserCategory
from user.models import User
from .models import Order, OrderItem, ProductDiscount, UsedDiscount, UserDiscount
from .serializers import (
    OrderItemSerializer,
    OrderSerializer,
    ProductDiscountSerializer,
    UsedDiscountSerializer,
    UserDiscountSerializer,
)


class ProductDiscountViewSet(viewsets.ModelViewSet):
    queryset = ProductDiscount.objects.all()
    serializer_class = ProductDiscountSerializer


class UserDiscountViewSet(viewsets.ModelViewSet):
    queryset = UserDiscount.objects.all()
    serializer_class = UserDiscountSerializer

    def get_queryset(self):
        # Query for anonymous users
        base_filter = Q(user=None) & Q(user_category=UserCategory.BRONZE.value) & Q(user_type=None)
        if not isinstance(self.request.user, User):
            return self.queryset.filter(base_filter)

        # Query for authenticated users
        user_filter = (
            (Q(user=self.request.user) | Q(user=None))
            & Q(Q(user_type=None) | Q(user_type=self.request.user.type))
            & Q(user_category__lte=self.request.user.category)
        )
        query = self.queryset.filter(base_filter | user_filter)
        return query


class UsedDiscountViewSet(viewsets.ModelViewSet):
    queryset = UsedDiscount.objects.all()
    serializer_class = UsedDiscountSerializer

    def get_queryset(self):
        if self.request.user is None:
            return self.queryset.filter(user=None)
        return self.queryset.filter(user=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        if self.request.user is None:
            return self.queryset.filter(order__user=None)
        return self.queryset.filter(order__user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user is None:
            return self.queryset.filter(user=None)
        return self.queryset.filter(user=self.request.user)
