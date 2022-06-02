from typing import Dict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import UserDBModel
from api import schema


class CRUDSpotApp:
    model = UserDBModel

    @classmethod
    async def get_user_by_id(cls, db: AsyncSession,
                             user_id: int) -> Dict:
        query = select(cls.model).filter(cls.model.user_id == user_id)
        result = await db.execute(query)

        return result.mappings().one()

    @classmethod
    async def post_user(cls, db: AsyncSession,
                        user: schema.NewUserSchema) -> schema.UserCreatedSchema:
        db.add(user)
        return schema.UserCreatedSchema(nickname=user.nickname, email=user.email)
