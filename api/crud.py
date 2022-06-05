from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import UserDBModel
from api import schema


class CRUDUser:
    model = UserDBModel

    @classmethod
    async def get_user_by_id(cls, db: AsyncSession,
                             user_id: int) -> schema.ShowUserSchema:
        """Get user by id"""

        query = select(cls.model).filter(cls.model.user_id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            # TODO: fix esceptions
            raise Exception

        return user

    @classmethod
    async def get_all_users(cls,
                            db: AsyncSession) -> List[schema.ShowUserSchema]:
        """Get all users"""

        query = select(cls.model)
        result = await db.execute(query)
        # TODO: check if scalars will work without list
        return [user[cls.model] for user in result.mappings().all()]

    @classmethod
    async def add_user(cls, db: AsyncSession,
                       user: schema.NewUserSchema) -> schema.UserCreatedSchema:
        """Add new user to data base"""

        await db.add(user)
        await db.commit()

        return schema.UserCreatedSchema(nickname=user.nickname,
                                        email=user.email)

    @classmethod
    async def delete_user(cls, db: AsyncSession,
                          user_id: int) -> str:
        """Delete user from data base"""

        query = select(cls.model).filter(cls.model.user_id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            # TODO: fix esceptions
            raise Exception

        await db.delete(user)
        await db.commit()

        return f"User with {user_id=} is disappear..."
