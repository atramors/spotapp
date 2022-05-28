from typing import Dict
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import UserDBModel
from api.schema import UserModel


class CRUDSpotApp:
    model = UserDBModel

    async def get_user_by_user_id(self,
                                  db: AsyncSession,
                                  user_id: int,
                                  ) -> Dict:
        query = select(self.model).filter(self.model.user_id == user_id)
        result = await db.execute(query)

        return result.mappings().one()

    async def post_user(self,
                        db: AsyncSession,
                        user: UserModel
                        ) -> Dict:
        # query = users.insert().values(text=note.text, completed=note.completed)

        query = text(
            """INSERT INTO table_name
            (nickname, first_name, last_name, user_pic, email,
            hashed_password, friends, spot_photos, added_spots, favourite_spots,
            premium_account_type)
               VALUES (value1, value2, …)
               RETURNING username;"""
        )
        result = await db.execute(query)
        return {**user.dict(), "id": result}
