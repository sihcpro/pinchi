from django.contrib.auth.models import AbstractUser
from django.db import models

from helpers.models import TrackingModel
from .enums import UserType, UserCategory


class User(AbstractUser, TrackingModel):
    type = models.CharField(
        max_length=1, default=UserType.EXTERNAL_CUSTOMER.value, choices=UserType.list()
    )
    category = models.SmallIntegerField(
        default=UserCategory.BRONZE.value, choices=UserCategory.list()
    )

    _created = models.DateTimeField(auto_now_add=True)
    _updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "user"
