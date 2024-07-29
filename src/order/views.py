from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action

from helpers.exceptions import BadRequestException
from helpers.responses import AppResponse
from order.enums import OrderStatus
from user.enums import UserCategory
from user.models import User
from .models import Order, OrderItem, ProductDiscount, UsedDiscount, UserDiscount
from .serializers import (
    OrderDetailSerializer,
    OrderItemSerializer,
    OrderSerializer,
    ProductDiscountSerializer,
    UsedDiscountSerializer,
    UserDiscountSerializer,
)


class ProductDiscountViewSet(viewsets.ModelViewSet):
    queryset = ProductDiscount.objects.all()
    serializer_class = ProductDiscountSerializer
    permission_classes = []


class UserDiscountViewSet(viewsets.ModelViewSet):
    queryset = UserDiscount.objects.all()
    serializer_class = UserDiscountSerializer
    permission_classes = []

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
        return self.queryset.filter(user=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        return self.queryset.filter(order__user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        return AppResponse(OrderDetailSerializer(self.get_object()).data)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def finish(self, request, pk):
        order = Order.objects.filter(id=pk, status=OrderStatus.ACCEPTED.value).first()
        if not order:
            raise BadRequestException(400006, message="Shipping Order not found", request=request)
        order.status = OrderStatus.SHIPPED.value
        order.save()

        total_success_order = Order.objects.filter(
            user=request.user, status=OrderStatus.SHIPPED.value
        ).count()
        if total_success_order >= 50:
            request.user.category = UserCategory.GOLD.value
            request.user.save()
        elif total_success_order >= 20:
            request.user.category = UserCategory.SILVER.value
            request.user.save()

        return AppResponse({})
