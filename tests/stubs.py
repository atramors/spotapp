
from sqlalchemy.ext.asyncio import AsyncSession
from tests import sample


async def get_user_by_id_stub(db: AsyncSession,
                              user_id: int):
    return sample.EXAMPLE_USER_GET
