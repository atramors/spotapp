import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.constants import API_TITLE
from api.crud import CRUDSpotApp
from api.db import get_session
from api import schema
from api.models import UserDBModel


spotapp_router = APIRouter(tags=[API_TITLE])
logger = logging.getLogger(__name__)


@spotapp_router.get(
    path="/user/{user_id}",
    # response_model=NewUserSchema,
    responses={
        200: {"description": "requested user by user_id"},
        404: {"model": schema.Error, "description": "requested user was not found"},
        406: {"model": schema.Error, "description": "input data format error"},
    },
)
async def get_user(user_id: int,
                   db: AsyncSession = Depends(get_session),
                   ):
    result = await CRUDSpotApp.get_user_by_id(db=db,
                                              user_id=user_id)
    return result


@spotapp_router.post(
    path="/signup",
    response_model=schema.UserCreatedSchema
)
async def create_user(request: schema.NewUserSchema,
                      db: AsyncSession = Depends(get_session),
                      ) -> schema.UserCreatedSchema:
    "Creating a new user"

    new_user = UserDBModel(**request.dict())
    created_user = await CRUDSpotApp.post_user(db=db, user=new_user)

    return created_user
