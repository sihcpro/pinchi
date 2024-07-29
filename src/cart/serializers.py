from rest_framework import serializers

from product.serializers import ProductSerializer
from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CartItem
        fields = [
            "id",
            "user",
            "product",
            "quantity",
            "user_discount",
            "product_discount",
            "_created",
            "_updated",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data["product"] = ProductSerializer(instance.product).data
        return data
