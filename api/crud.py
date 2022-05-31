from typing import Dict
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import UserDBModel
from api.schema import UserSchema


class CRUDSpotApp:
    model = UserDBModel

    async def get_user_by_user_id(self,
                                  db: AsyncSession,
                                  id: int,
                                  ) -> Dict:
        query = select(self.model).filter(self.model.user_id == id)
        result = await db.execute(query)

        return result.mappings().one()

    async def post_user(self,
                        db: AsyncSession,
                        user: UserSchema
                        ) -> Dict:
        return db.add(user)
