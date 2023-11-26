import logging
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from api import schema
from api.authentication import get_current_user
from api.crud import CRUDSpot, CRUDUser, CRUDComment
from api.db import get_session
from api.models import SpotDBModel, UserDBModel, CommentDBModel
from api.utils import PasswordHasher, UserExistException


spotapp_user_router = APIRouter(prefix="/users", tags=["Users"])
spotapp_spot_router = APIRouter(prefix="/spots", tags=["Spots"])
spotapp_comment_router = APIRouter(prefix="/comments", tags=["Comments"])
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
    path="/create/",
    response_model=schema.UserTerseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(payload: schema.UserCreationSchema,
                      db: AsyncSession = Depends(get_session),
                      ) -> schema.UserTerseSchema:
    """Creating a new user"""
    try:
        checked_user = await db.execute(
            select(UserDBModel).where(UserDBModel.nickname == payload.nickname))
        if checked_user.fetchone():
            raise UserExistException(
                f"User with nickname={payload.nickname} already exist!")
        hashed_password = PasswordHasher().hash_password(payload.password)
        payload.password = hashed_password
        new_user = UserDBModel(**payload.dict())

        return await CRUDUser.add_user(db=db, user=new_user)

    except UserExistException as exc:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=exc)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc)


@spotapp_user_router.put(
    path="/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202: {"description": "User have been updated"},
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
    path="/destroy/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "User have been deleted"},
        404: {"model": schema.Error, "description": "Requested user was not found"},
        406: {"model": schema.Error, "description": "Input data format error"},
    },
)
async def destroy_user(user_id: int,
                       db: AsyncSession = Depends(get_session),
                       ) -> Response:
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


@spotapp_spot_router.post(
    path="/create/",
    response_model=schema.SpotSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_spot(payload: schema.SpotSchema,
                      db: AsyncSession = Depends(get_session),
                      current_user: UserDBModel = Depends(get_current_user),
                      ) -> schema.SpotSchema:
    """Creating a new spot"""

    try:
        new_spot = SpotDBModel(
            **payload.dict(),
            spot_full_address=f"{payload.spot_street}, {payload.spot_street_number}. "
                              f"{payload.spot_country}, {payload.spot_city},")

        return await CRUDSpot.add_spot(db=db, spot=new_spot)

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc)


@spotapp_spot_router.get(
    path="/{spot_id}",
    response_model=schema.SpotSchema,
    responses={
        200: {"description": "Spot requested by spot_id"},
        404: {"model": schema.Error, "description": "Requested spot was not found"},
        406: {"model": schema.Error, "description": "Input data format error"},
    },
)
async def get_spot_by_id(spot_id: int,
                         db: AsyncSession = Depends(get_session),
                         current_user: UserDBModel = Depends(get_current_user),
                         ) -> schema.SpotSchema:
    """Getting spot by the id"""

    try:
        schema.InputDataValidator(spot_id=spot_id)

        return await CRUDSpot.get_spot_by_id(db=db,
                                             spot_id=spot_id)

    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=exc)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified {spot_id=} was not found",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc)


@spotapp_spot_router.get(
    path="/filtered/",
    response_model=List[schema.SpotSchema],
    responses={
        200: {"description": "Spot requested by spot_id"},
        404: {"model": schema.Error, "description": "Requested spot was not found"},
        406: {"model": schema.Error, "description": "Input data format error"},
    },
)
async def get_spots(spot_country: Union[str, None] = None,
                    spot_city: Union[str, None] = None,
                    spot_street: Union[str, None] = None,
                    owner_id: Union[int, None] = None,
                    db: AsyncSession = Depends(get_session),
                    current_user: UserDBModel = Depends(get_current_user),
                    ) -> List[schema.SpotSchema]:
    """Getting filtered spots"""

    try:
        filter_params = schema.SpotFilterSchema(
            spot_country=spot_country,
            spot_city=spot_city,
            spot_street=spot_street,
            owner_id=owner_id)

        result = await CRUDSpot.get_filtered_spots(db=db, filter=filter_params)

        if result:
            return result

        raise NoResultFound

    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=exc)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Specified spot was not found",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc)


@spotapp_spot_router.put(
    path="/{spot_id}",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202: {"description": "Spot have been updated"},
        404: {"model": schema.Error, "description": "Requested spot was not found"},
        406: {"model": schema.Error, "description": "Input data format error"},
    },
)
async def update_spot(spot_id: int,
                      payload: schema.SpotUpdateSchema,
                      db: AsyncSession = Depends(get_session),
                      current_user: UserDBModel = Depends(get_current_user),
                      ) -> str:
    """Updating spot by the spot id"""

    try:
        data_to_update = payload.dict()

        return await CRUDSpot.update(db=db, spot_id=spot_id, data=data_to_update)

    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=exc)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified {spot_id=} was not found",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc)


@spotapp_spot_router.delete(
    path="/destroy/{spot_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Spot have been deleted"},
        404: {"model": schema.Error, "description": "Requested spot was not found"},
        406: {"model": schema.Error, "description": "Input data format error"},
    },
)
async def destroy_spot(spot_id: int,
                       db: AsyncSession = Depends(get_session),
                       current_user: UserDBModel = Depends(get_current_user),
                       ) -> Response:
    """Getting spot by the spot id"""

    try:
        schema.InputDataValidator(spot_id=spot_id)

        return await CRUDSpot.delete_spot(db=db, spot_id=spot_id)

    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=exc)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified {spot_id=} was not found",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc)


@spotapp_comment_router.get(
    path="/{comment_id}",
    response_model=schema.CommentFullSchema,
    responses={
        200: {"description": "Comment requested by comment_id"},
        404: {"model": schema.Error, "description": "Requested comment was not found"},
        406: {"model": schema.Error, "description": "Input data format error"},
    },
)
async def get_comment(comment_id: int,
                      db: AsyncSession = Depends(get_session),
                      ) -> schema.CommentFullSchema:
    """Getting comment by the comment id"""

    try:
        schema.InputDataValidator(comment_id=comment_id)

        return await CRUDComment.get_comment_by_id(db=db, comment_id=comment_id)

    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=exc)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specified {comment_id=} was not found",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc)


@spotapp_comment_router.post(
    path="/create/",
    response_model=schema.CommentFullSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(payload: schema.CommentNewSchema,
                         db: AsyncSession = Depends(get_session),
                         ) -> schema.CommentFullSchema:
    """Creating a new comment"""

    try:
        new_comment = CommentDBModel(**payload.dict())

        return await CRUDComment.add_comment(db=db, comment=new_comment)

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exc)
