from helpers.enums import ExtendedEnum


class UserType(ExtendedEnum):
    INTERNAL_STAFF = "I"
    EXTERNAL_CUSTOMER = "E"


class UserCategory(ExtendedEnum):
    GOLD = 3
    SILVER = 2
    BRONZE = 1
