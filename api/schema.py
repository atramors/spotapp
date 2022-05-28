from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class Error(BaseModel):
    message: str = Field(description="Error description",
                         examples=[404, 406, 500])
    code: int = Field(description="Error status code",
                      examples=["Not found",
                                "<Validation error description>",
                                "<Internal server error description>"],
                      )


class UserModel(BaseModel):
    nickname: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_pic: Optional[str] = None
    email: str = Field(repr=False)
    hashed_password: str = Field(repr=False)
    friends: Optional[List[str]] = None
    spot_photos: Optional[str] = None
    added_spots: Optional[List[str]] = None
    favourite_spots: Optional[List[str]] = None
    premium_account_type: bool = False

    class Config:
        sample_schema = {
            "example": {
                "nickname": "Some cool user",
                "first_name": "John",
                "last_name": "Doe",
                "user_pic": "link with an image",
                "friends": ["user1", "user2", ],
                "spot_photos": ["spot1_img", "spot2_img", ],
                "added_spots": ["spot_name1", "spot_name2", ],
                "favourite_spots": ["spot_name1", ],
                "premium_account_type": False
            }
        }


class SpotModel(BaseModel):
    spot_name: Optional[str] = None
    spot_pic: Optional[str] = None
    spot_photos: Optional[List[str]] = None
    spot_country: Optional[str] = None
    spot_city: Optional[str] = None
    spot_street: Optional[str] = None
    spot_street_number: Optional[str] = None
    spot_full_address: Optional[str] = None
    spot_description: Optional[str] = None
    spot_raiting: Optional[float] = None
    user_added_spot: Optional[str] = None
    comments: Optional[List[str]] = None

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


class CommentModel(BaseModel):
    body: Optional[str] = None
    created_at: datetime
