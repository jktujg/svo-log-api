from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import models
from . import schemas


class SyncOrm:

    @staticmethod
    def get_user(conn: Session, email: str) -> models.UserModel | None:
        query = (
            select(models.UserModel)
            .filter(models.UserModel.email == email)
        )
        user = conn.execute(query).scalars().one_or_none()

        return user

    @staticmethod
    def create_user(conn: Session, new_user: schemas.UserInDB) -> models.UserModel | None:
        created_user = models.UserModel(**new_user.model_dump())

        conn.add(created_user)
        try:
            conn.commit()
        except IntegrityError:
            return

        return created_user
