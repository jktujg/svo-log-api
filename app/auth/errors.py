from fastapi import HTTPException, status


CREDENTIAL_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)

LOGIN_ERROR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Incorrect username or password',
    headers={'WWW-Authenticate': 'Bearer'},
)

REGISTER_LOGIN_ERROR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Login already in use',
    headers={'WWW-Authenticate': 'Bearer'},
)

PASSWORD_STRENGTH_ERROR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Password must contain minimum 8 characters, maximum 40 characters, at least one uppercase letter, one lowercase letter and one number'
)

PERMISSION_ERROR = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='You don\'t have permission for this operation'
)
