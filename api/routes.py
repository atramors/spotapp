import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.constants import API_TITLE
from api.crud import CRUDSpotApp
from api.db import get_session
from api.schema import UserModel, SpotModel, CommentModel, Error


spotapp_router = APIRouter(tags=[API_TITLE])
logger = logging.getLogger(__name__)


@spotapp_router.get(
    path="/user/{user_id}",
    response_model=UserModel,
    responses={
        200: {"description": "requested user by user_id"},
        404: {"model": Error, "description": "requested user was not found"},
        406: {"model": Error, "description": "input data format error"},
    },
)
async def get_user(user_id: int,
                   db: AsyncSession = Depends(get_session),
                   ):
    result = await CRUDSpotApp.get_user_by_user_id(db=db,
                                                   user_id=user_id)
    return result
