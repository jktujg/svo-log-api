import random
from string import digits, ascii_lowercase, ascii_uppercase
from typing import Any

from app.auth.service import register_user


def random_string(n_digit: int = 0, n_lower: int = 0, n_upper: int = 0) -> str:
    chars = [
        *random.choices(digits, k=n_digit),
        *random.choices(ascii_lowercase, k=n_lower),
        *random.choices(ascii_uppercase, k=n_upper),
    ]
    random.shuffle(chars)

    return ''.join(chars)


async def registered_user(session, role, state):
    email = f'{random_string(n_lower=10)}@mail.com'
    password = random_string(n_digit=2, n_lower=5, n_upper=3)

    user = await register_user(session, email, password, role=role, state=state)
    return email, password, user


def compare(data: dict, target: Any, include: set | None = None, exclude: set | None = None,
            from_attributes: bool = False) -> bool:
    """ Used to compare sent data with recieved data """
    keys = {k for k in data.keys() if (not include or k in include)} - set(exclude or [])

    if from_attributes is True:
        try:
            for k in keys:
                if data[k] != getattr(target, k):
                    return False
        except AttributeError:
            return False
    else:
        for k in keys:
            if data[k] != target[k]:
                return False

    return True


def get_recursive_value(item: dict, key: str):
    for k in key.split('.'):
        item = item[k]
    return item
