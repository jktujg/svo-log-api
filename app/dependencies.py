from .database import async_session


def async_session_gen(**params):

    async def _get_async_session():
        async with async_session(**params) as session:
            try:
                yield session
            except:
                await session.rollback()
                raise
            else:
                await session.commit()

    return _get_async_session


get_async_session = async_session_gen(expire_on_commit=True)
