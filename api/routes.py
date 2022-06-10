import logging
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from starlette import status

from api.constants import API_TITLE
from api.crud import CRUDUser
from api.db import get_session
from api import schema
from api.models import UserDBModel
from api.utils import PasswordHasher


spotapp_user_router = APIRouter(prefix="/users", tags=["SpotApp_User"])
logger = logging.getLogger(__name__)


@spotapp_user_router.get(
    path="/{user_id}",
    response_model=schema.UserOpenSchema,
    responses={
        200: {"description": "User requested by user_id"},
        404: {"model": schema.Error, "description": "Requested user was not found"},
        406: {"model": schema.Error, "description": "Input data format error"},
    },
)
async def get_user(user_id: int,
                   db: AsyncSession = Depends(get_session),
                   ) -> schema.UserOpenSchema:
    """Getting user by the user id"""

    try:
        schema.InputDataValidator(user_id=user_id)

        return await CRUDUser.get_user_by_id(db=db, user_id=user_id)

    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=exc)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified {user_id=} was not found",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc)


@spotapp_user_router.get(
    path="/all/",
    response_model=List[schema.UserOpenSchema],
    responses={
        200: {"description": "getting all users"},
    },
)
async def get_all_users(db: AsyncSession = Depends(get_session),
                        ) -> List[schema.UserOpenSchema]:
    """Getting all users"""
    try:
        return await CRUDUser.get_all_users(db=db)

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc)


@spotapp_user_router.post(
    path="/create_user/",
    response_model=schema.UserTerseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(payload: schema.UserCreationSchema,
                      db: AsyncSession = Depends(get_session),
                      ) -> schema.UserTerseSchema:
    """Creating a new user"""

    try:
        hashed_password = PasswordHasher().hash_password(payload.password)
        payload.password = hashed_password
        new_user = UserDBModel(**payload.dict())

        return await CRUDUser.add_user(db=db, user=new_user)

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc)


@spotapp_user_router.put(
    path="/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        204: {"description": "User have been deleted"},
        404: {"model": schema.Error, "description": "Requested user was not found"},
        406: {"model": schema.Error, "description": "Input data format error"},
    },
)
async def update_user(user_id: int,
                      payload: schema.UserSchema,

                      db: AsyncSession = Depends(get_session),
                      ) -> str:
    """Updating user by the user id"""

    try:
        schema.InputDataValidator(user_id=user_id)
        data_to_update = payload.dict()

        return await CRUDUser.update(db=db, user_id=user_id, data=data_to_update)

    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=exc)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified {user_id=} was not found",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc)


@spotapp_user_router.delete(
    path="/destroy_user/{user_id}",
    responses={
        204: {"description": "User have been deleted"},
        404: {"model": schema.Error, "description": "Requested user was not found"},
        406: {"model": schema.Error, "description": "Input data format error"},
    },
)
async def destroy_user(user_id: int,
                       db: AsyncSession = Depends(get_session),
                       ) -> str:
    """Getting user by the user id"""

    try:
        schema.InputDataValidator(user_id=user_id)

        return await CRUDUser.delete_user(db=db, user_id=user_id)

    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=exc)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified {user_id=} was not found",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc)
