import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.constants import API_TITLE
from api.crud import CRUDUser
from api.db import get_session
from api import schema
from api.models import UserDBModel


spotapp_router = APIRouter(tags=[API_TITLE])
logger = logging.getLogger(__name__)


@spotapp_router.get(
    path="/user/{user_id}",
    response_model=schema.ShowUserSchema,
    responses={
        200: {"description": "requested user by user_id"},
        404: {"model": schema.Error, "description": "requested user was not found"},
        406: {"model": schema.Error, "description": "input data format error"},
    },
)
async def get_user(user_id: int,
                   db: AsyncSession = Depends(get_session),
                   ) -> schema.ShowUserSchema:
    """Getting user by the user id"""

    return await CRUDUser.get_user_by_id(db=db, user_id=user_id)


@spotapp_router.get(
    path="/users",
    response_model=List[schema.ShowUserSchema],
    responses={
        200: {"description": "getting all users"},
        404: {"model": schema.Error, "description": "there are no users found"},
        406: {"model": schema.Error, "description": "input data format error"},
    },
)
async def get_all_user(db: AsyncSession = Depends(get_session),
                       ) -> List[schema.ShowUserSchema]:
    """Getting all users"""

    return await CRUDUser.get_all_users(db=db)


@spotapp_router.post(
    path="/signup",
    response_model=schema.UserCreatedSchema
)
async def create_user(request: schema.NewUserSchema,
                      db: AsyncSession = Depends(get_session),
                      ) -> schema.UserCreatedSchema:
    """Creating a new user"""

    new_user = UserDBModel(**request.dict())
    created_user = await CRUDUser.add_user(db=db, user=new_user)

    return created_user


@spotapp_router.delete(
    path="/destroy_user/{user_id}",
    # response_model=schema.ShowUserSchema,
    responses={
        200: {"description": "requested user by user_id"},
        404: {"model": schema.Error, "description": "requested user was not found"},
        406: {"model": schema.Error, "description": "input data format error"},
    },
)
async def destroy_user(user_id: int,
                       db: AsyncSession = Depends(get_session),
                       ) -> str:
    """Getting user by the user id"""

    return await CRUDUser.delete_user(db=db, user_id=user_id)
