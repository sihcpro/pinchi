from django.contrib.auth.models import AbstractUser
from django.db import models

from helpers.models import TrackingModel


class User(AbstractUser, TrackingModel):
    INTERNAL_STAFF = "I"
    EXTERNAL_CUSTOMER = "E"
    TYPES = (
        (INTERNAL_STAFF, "INTERNAL_STAFF"),
        (EXTERNAL_CUSTOMER, "EXTERNAL_CUSTOMER"),
    )

    GOLD = "G"
    SILVER = "S"
    BRONZE = "B"
    CATEGORIES = (
        (GOLD, "GOLD"),
        (SILVER, "SILVER"),
        (BRONZE, "BRONZE"),
    )

    type = models.CharField(max_length=1, default=EXTERNAL_CUSTOMER, choices=TYPES)
    category = models.CharField(max_length=1, default=BRONZE, choices=CATEGORIES)

    _created = models.DateTimeField(auto_now_add=True)
    _updated = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = "user"
