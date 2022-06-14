from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from tests import sample


async def get_user_by_id_empty_stub(db: AsyncSession,
                                    user_id: int):
    return []


async def get_user_by_id_stub(db: AsyncSession,
                              user_id: int):
    return sample.EXAMPLE_USER_GET


async def get_all_users_stub(db: AsyncSession):
    return [sample.EXAMPLE_USER_GET, sample.EXAMPLE_USER_GET]


async def create_new_user_stub(db: AsyncSession,
                               user):
    return sample.EXAMPLE_NEW_USER_ADD


async def delete_user_stub(db: AsyncSession,
                           user_id: int):
    return sample.DELETED_USER
