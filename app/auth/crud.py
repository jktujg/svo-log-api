from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models
from . import schemas


class AsyncOrm:

    @classmethod
    async def get_user(cls, session: AsyncSession, email: str) -> models.UserModel | None:
        query = (
            select(models.UserModel)
            .filter(models.UserModel.email == email)
        )
        resp = await session.execute(query)
        user = resp.scalars().one_or_none()

        return user

    @classmethod
    async def create_user(cls, session: AsyncSession, new_user: schemas.UserInDB) -> models.UserModel | None:
        created_user = models.UserModel(**new_user.model_dump())

        session.add(created_user)
        await session.commit()

        return created_user
