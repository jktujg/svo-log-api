from .database import session


def session_gen(**params):
    def _get_session():
        with session(**params) as conn:
            yield conn
    return _get_session


get_session = session_gen(expire_on_commit=False)
