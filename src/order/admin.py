from django.contrib import admin

from .models import Order, OrderItem, ProductDiscount, UsedDiscount, UserDiscount

admin.site.register(ProductDiscount)
admin.site.register(UserDiscount)
admin.site.register(UsedDiscount)

admin.site.register(Order)
admin.site.register(OrderItem)
