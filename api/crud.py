from typing import Dict, List
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update as sqlalchemy_update
from api.models import UserDBModel
from api import schema


class CRUDUser:
    model = UserDBModel

    @classmethod
    async def get_user_by_id(cls, db: AsyncSession,
                             user_id: int) -> schema.UserOpenSchema:
        """Get user by id"""

        query = select(cls.model).where(cls.model.user_id == user_id)
        result = await db.execute(query)

        return result.scalar_one()

    @classmethod
    async def get_all_users(cls, db: AsyncSession,
                            ) -> List[schema.UserOpenSchema]:
        """Get all users"""

        query = select(cls.model)
        result = await db.execute(query)

        return [user[cls.model] for user in result.all()]

    @classmethod
    async def add_user(cls, db: AsyncSession,
                       user) -> schema.UserTerseSchema:
        """Add new user to data base"""

        db.add(user)
        await db.flush()
        return schema.UserTerseSchema(nickname=user.nickname,
                                      email=user.email)

    @classmethod
    async def update(cls, db: AsyncSession,
                     user_id: int,
                     data: Dict,
                     ) -> str:
        """Update a user from data base"""

        query = (
            sqlalchemy_update(cls.model)
            .where(cls.model.user_id == user_id)
            .values(**{k: v for k, v in data.items() if v})
            .execution_options(synchronize_session="fetch")
        )

        result = await db.execute(query)

        rows_updated = result.rowcount
        if rows_updated:
            return f"User with {user_id=} is updated!"

        raise NoResultFound

    @classmethod
    async def delete_user(cls, db: AsyncSession,
                          user_id: int) -> str:
        """Delete user from data base"""

        query = select(cls.model).filter(cls.model.user_id == user_id)
        result = await db.execute(query)
        user = result.scalar_one()

        await db.delete(user)

        return f"User with {user_id=} is disappear..."
