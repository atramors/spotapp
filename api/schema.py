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


class NewUserSchema(BaseModel):
    nickname: str
    first_name: str
    last_name: str
    user_pic: Union[str, None]
    email: str
    hashed_password: str
    premium_account_type: bool = False

    class Config:
        orm_mode = True


class UserCreatedSchema(BaseModel):
    nickname: str
    email: str

    class Config:
        orm_mode = True


class ShowUserSchema(BaseModel):
    nickname: str
    first_name: str
    last_name: str
    user_pic: Union[str, None]
    friends: Union[str, None]
    spot_photos: Union[str, None]
    added_spots: Union[str, None]
    favourite_spots: Union[str, None]

    class Config:
        orm_mode = True


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
