from django.db import models

from helpers.functions import generate_random_string
from helpers.models import TrackingModel
from order.enums import DiscountStatus, OrderStatus
from product.models import Category, Department, Product
from user.enums import UserCategory, UserType
from user.models import User


class DiscountInfo(TrackingModel):
    code = models.CharField(
        max_length=31,
        null=True,
        unique=True,
    )
    status = models.CharField(
        max_length=1, default=DiscountStatus.ACTIVE.value, choices=DiscountStatus.list()
    )
    percentage = models.DecimalField(max_digits=10, decimal_places=2)

    remaining_uses = models.IntegerField(default=1)
    deadline = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_random_string(8)

        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class ProductDiscount(DiscountInfo, TrackingModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = True
        db_table = "product_discount"


class UserDiscount(DiscountInfo, TrackingModel):
    user_type = models.CharField(max_length=1, choices=UserType.list(), null=True)
    user_category = models.SmallIntegerField(
        default=UserCategory.BRONZE.value, choices=UserCategory.list()
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = True
        db_table = "user_discount"


class Order(TrackingModel):
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    final_total = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=1, default=OrderStatus.PENDING.value, choices=OrderStatus.list()
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = "order"


class OrderItem(TrackingModel):
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    final_total = models.DecimalField(max_digits=10, decimal_places=2)

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = "order_item"


class UsedDiscount(TrackingModel):
    cancelled = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="discounts")

    product_discount = models.ForeignKey(ProductDiscount, on_delete=models.CASCADE, null=True)
    user_discount = models.ForeignKey(UserDiscount, on_delete=models.CASCADE, null=True)

    class Meta:
        managed = True
        db_table = "used_discount"
