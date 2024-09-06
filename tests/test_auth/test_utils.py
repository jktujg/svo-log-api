import pytest

from app.auth.utils import password_is_valid


@pytest.mark.parametrize(
    'password, result, explain',
    [
        ('123', False, 'minimum 8 chars'),
        ('1' * 41, False, 'maximum 40 chars'),
        ('12345678', False, 'minimum 2 letters'),
        ('ab123456', False, 'minimum 1 uppercase letter'),
        ('AB123456', False, 'minimum 1 lowercase letter'),
        ('ABCDefgh', False, 'minimum 1 digit'),
        ('aB123456', True, 'valid password'),
        ('11A11a11', True, 'valid password'),
    ]
)
def test_password_pattern(password, result, explain):
    assert password_is_valid(password) == result, explain
