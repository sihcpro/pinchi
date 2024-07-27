from django.db import models
from helpers.models import TrackingModel


class Department(TrackingModel):
    name = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = "department"


class Category(TrackingModel):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = "category"


class Product(TrackingModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = "product"
