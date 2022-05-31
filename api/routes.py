import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.constants import API_TITLE
from api.crud import CRUDSpotApp
from api.db import get_session
from api.schema import UserSchema, Error
from api.models import UserDBModel


spotapp_router = APIRouter(tags=[API_TITLE])
logger = logging.getLogger(__name__)


@spotapp_router.get(
    path="/user/{user_id}",
    # response_model=UserSchema,
    responses={
        200: {"description": "requested user by user_id"},
        404: {"model": Error, "description": "requested user was not found"},
        406: {"model": Error, "description": "input data format error"},
    },
)
async def get_user(user_id: int,
                   db: AsyncSession = Depends(get_session),
                   ):
    result = await CRUDSpotApp().get_user_by_user_id(db=db,
                                                     id=user_id)
    return result


@spotapp_router.post(
    path="/signup",
)
async def create_user(request: UserSchema,
                      db: AsyncSession = Depends(get_session),):
    new_user = UserDBModel(**request.dict())
        # nickname=request.nickname,
        #                    first_name=request.first_name,
        #                    last_name=request.last_name,
        #                    user_pic=request.user_pic,
        #                    email=request.email,
        #                    hashed_password=request.hashed_password,
        #                    premium_account_type=request.premium_account_type)
    # import pdb; pdb.set_trace()
    # query = UserDBModel.insert().values(new_user)

    result = await CRUDSpotApp().post_user(db=db, user=new_user)

    return result
