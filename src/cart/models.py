from django.db import models

from helpers.models import TrackingModel
from order.models import ProductDiscount, UserDiscount
from product.models import Product
from user.models import User


class CartItem(TrackingModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    user_discount = models.ForeignKey(UserDiscount, on_delete=models.CASCADE, null=True)
    product_discount = models.ForeignKey(ProductDiscount, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = True
        db_table = "cart_item"
