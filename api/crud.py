from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import UserDBModel
from api import schema


class CRUDSpotApp:
    model = UserDBModel

    @classmethod
    async def get_user_by_id(cls, db: AsyncSession,
                             user_id: int) -> schema.ShowUserSchema:
        query = select(cls.model).filter(cls.model.user_id == user_id)
        result = await db.execute(query)

        return result.mappings().one()[cls.model]

    # TODO: fix the logic
    @classmethod
    async def get_all_users(
            cls, db: AsyncSession) -> List[schema.ShowUserSchema]:
        query = select(cls.model).filter()
        result = await db.execute(query)

        return result.mappings().all()[cls.model]

    @classmethod
    async def post_user(cls, db: AsyncSession,
                        user: schema.NewUserSchema) -> schema.UserCreatedSchema:
        db.add(user)
        return schema.UserCreatedSchema(nickname=user.nickname, email=user.email)
