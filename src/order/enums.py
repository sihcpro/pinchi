from helpers.enums import ExtendedEnum


class OrderStatus(ExtendedEnum):
    PENDING = "P"
    ACCEPTED = "A"
    SHIPPED = "S"
    CANCELED = "C"


class DiscountStatus(ExtendedEnum):
    ACTIVE = "A"
    INACTIVE = "I"
