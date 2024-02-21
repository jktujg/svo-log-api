from fastapi import HTTPException, status


def auth_erorr_factory(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={'WWW-Authenticate': 'Bearer'},
    )


credential_exception = auth_erorr_factory('Could not validate credentials')
login_error = auth_erorr_factory('Incorrect username or password')
register_login_error = auth_erorr_factory('Login already in use')


permission_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='You don\'t have permission for this operation'
)
