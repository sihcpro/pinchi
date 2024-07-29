from rest_framework import serializers

from product.serializers import ProductSerializer
from user.serializers import UserSerializer
from .models import Order, OrderItem, ProductDiscount, UsedDiscount, UserDiscount

discount_info_fields = [
    "id",
    "code",
    "percentage",
    "status",
    "remaining_uses",
    "deadline",
    "_created",
    "_updated",
]


class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDiscount
        fields = discount_info_fields + ["product", "category", "department"]


class UserDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDiscount
        fields = discount_info_fields + ["user_type", "user_category", "user"]


class UsedDiscountSerializer(serializers.ModelSerializer):
    product_discount = ProductDiscountSerializer()
    user_discount = UserDiscountSerializer()

    class Meta:
        model = UsedDiscount
        fields = ["id", "cancelled", "product_discount", "user_discount", "_created", "_updated"]


class OrderItemSerializer(serializers.ModelSerializer):
    discounts = UsedDiscountSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "quantity",
            "total",
            "final_total",
            "order",
            "product",
            "discounts",
            "_created",
            "_updated",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["product"] = ProductSerializer(instance.product).data
        # data["discounts"] = UsedDiscountSerializer(instance.discounts).data
        return data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "quantity", "total", "final_total", "status", "_created", "_updated"]


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "quantity", "total", "final_total", "status", "_created", "_updated"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["items"] = OrderItemSerializer(instance.orderitem_set.all(), many=True).data
        return data
