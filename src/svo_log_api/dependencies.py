from .database import session


def get_session(**params):
    def session_gen():
        with session(**params) as conn:
            yield conn
    return session_gen
