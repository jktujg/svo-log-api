from enum import IntEnum


class UserRole(IntEnum):
    GUEST = 0
    USER = 1
    ADMIN = 2
    ROOT = 3


class UserState(IntEnum):
    BLOCKED = 0
    INACTIVE = 1
    ACTIVE = 2
