from django.db import transaction
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action

from helpers.exceptions import BadRequestException
from helpers.responses import AppResponse
from order.enums import OrderStatus
from order.models import Order, OrderItem, UsedDiscount
from .models import CartItem
from .serializers import CartItemSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    authentication_classes = [SessionAuthentication]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    @transaction.atomic
    def checkout(self, request):
        """This is the checkout method for the cart.
        Step:
        0. Create a pending order.
        1. Check if the product is available
        2. Create an order item
        3. Check if the discount is available
        4. Apply the discount to the order item
        5. Update the final total of the order item and the order
        6. Delete the cart item
        """
        cart_items = list(self.get_queryset())
        if not cart_items:
            raise BadRequestException(400001, message="Cart is empty", request=request)

        user = request.user
        order = Order.objects.create(user=user, quantity=len(cart_items), total=0, final_total=0)
        for item in cart_items:
            # Step:
            # 1. Check if the product is available
            # 2. Create an order item
            # 3. Check if the discount is available
            # 4. Apply the discount to the order item
            # 5. Update the final total of the order item and the order
            # 6. Delete the cart item

            if item.product.quantity < item.quantity:
                raise BadRequestException(
                    400004,
                    message=f"Product {item.product.name} is no longer available",
                    request=request,
                )
            item.product.quantity -= item.quantity
            item.product.save()

            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                total=item.product.price * item.quantity,
                final_total=item.product.price * item.quantity,
            )

            discount_apply = 1
            if item.user_discount:
                dsc = item.user_discount
                if dsc.remaining_uses <= 0:
                    raise BadRequestException(
                        400002,
                        message=f"Discount {dsc.percentage}% is no longer available for user",
                        request=request,
                    )
                dsc.remaining_uses -= 1
                dsc.save()
                UsedDiscount.objects.create(
                    user_discount=dsc,
                    user=user,
                    order=order_item,
                )
                discount_apply *= 1 - dsc.percentage / 100

            if item.product_discount:
                dsc = item.product_discount
                if dsc.remaining_uses <= 0:
                    raise BadRequestException(
                        400003,
                        message=f"Discount {dsc.percentage}% is no longer available for product",
                        request=request,
                    )
                dsc.remaining_uses -= 1
                dsc.save()
                UsedDiscount.objects.create(
                    product_discount=dsc,
                    user=user,
                    order=order_item,
                )
                discount_apply *= 1 - dsc.percentage / 100

            order_item.final_total *= discount_apply
            order_item.save()

            order.total += order_item.total
            order.final_total += order_item.final_total

            item.delete()

        order.status = OrderStatus.ACCEPTED.value
        order.save()

        return AppResponse({"order_id": order.id})
