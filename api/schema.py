from datetime import datetime
from typing import List, Union
from pydantic import BaseModel, Field


class Error(BaseModel):
    message: str = Field(description="Error description",
                         examples=[404, 406, 500])
    code: int = Field(description="Error status code",
                      examples=["Not found",
                                "<Validation error description>",
                                "<Internal server error description>"],
                      )


class UserSchema(BaseModel):
    nickname: str
    first_name: Union[str, None]
    last_name: Union[str, None]
    user_pic: Union[str, None]
    email: str = Field(repr=False)
    hashed_password: str = Field(repr=False)
    premium_account_type: bool = False

    class Config:
        sample_schema = {
            "example": {
                "nickname": "Some cool user",
                "first_name": "John",
                "last_name": "Doe",
                "user_pic": "link with an image",
                "premium_account_type": False
            }
        }


class SpotSchema(BaseModel):
    spot_name: Union[str, None]
    spot_pic: Union[str, None]
    spot_photos: Union[List[str], None]
    spot_country: Union[str, None]
    spot_city: Union[str, None]
    spot_street: Union[str, None]
    spot_street_number: Union[str, None]
    spot_full_address: Union[str, None]
    spot_description: Union[str, None]
    spot_raiting: Union[float, None]
    user_added_spot: Union[str, None]
    comments: Union[List[str], None]

    class Config:
        sample_schema = {
            "example": {
                "spot_name": "Theatr",
                "spot_full_address": "Ukraine, Kharkiv, Sumskaiia 25",
                "spot_description": "Doe",
                "spot_pic": "link with an image",
                "spot_photos": "link with an images",
                "spot_raiting": ["user1", "user2", ],
                "user_added_spot": "Some cool user",
                "comments": ["spot_name1", "spot_name2", ],
                "favourite_spots": ["spot_name1", ],
            }
        }


class CommentSchema(BaseModel):
    body: Union[str, None]
