import re


PASSWORD_PATTERN = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,40}$")


def password_is_valid(password: str) -> bool:
    return True if PASSWORD_PATTERN.fullmatch(password) else False
