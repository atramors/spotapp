from typing import List, Optional, Union
from pydantic import BaseModel, Field


class Error(BaseModel):
    message: str = Field(description="Error description",
                         examples=[404, 406, 500])
    code: int = Field(description="Error status code",
                      examples=["Not found",
                                "<Validation error description>",
                                "<Internal server error description>"],
                      )


class InputDataValidator(BaseModel):
    user_id: Optional[int] = Field(gt=0, le=2147483647)  # check int32 range


class InputSpotDataValidator(BaseModel):
    spot_id:  Union[int, None] = Field(gt=0, le=2147483647)  # check int32 range
    spot_country: Union[str, None] = None
    spot_city: Union[str, None] = None
    spot_street: Union[str, None] = None
    owner_id: Union[int, None] = Field(gt=0, le=2147483647)  # check int32 range


class UserCreationSchema(BaseModel):
    nickname: str
    first_name: str
    last_name: str
    user_pic: Union[str, None]
    email: str
    password: str
    premium_account_type: bool = False

    class Config:
        orm_mode = True


class UserTerseSchema(BaseModel):
    nickname: str
    email: str

    class Config:
        orm_mode = True


class UserOpenSchema(BaseModel):
    nickname: str
    first_name: str
    last_name: str
    user_pic: Union[str, None]
    friends: Union[List[str], None] = []
    spot_photos: Union[List[str], None] = []
    added_spots: Union[List[str], None] = []
    favourite_spots: Union[List[str], None] = []

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    nickname: Union[str, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    user_pic: Union[str, None] = None
    email: Union[str, None] = None
    password: Union[str, None] = None
    premium_account_type: Union[bool, None] = None

    class Config:
        orm_mode = True


class SpotSchema(BaseModel):
    spot_name: str
    spot_pic: Union[str, None] = None
    spot_photos: List[str]
    spot_country: str
    spot_city: str
    spot_street: str
    spot_street_number: str
    spot_description: Union[str, None] = None
    spot_raiting: Union[int, None] = None
    comment: Union[List[str], None]
    owner_id: int

    class Config:
        orm_mode = True
        sample_schema = {
            "example": {
                "spot_name": "Theatr",
                "spot_pic": "https://patrick.com/",
                "spot_photos": ["https://patrick.com/some_spot/", "https://patrick.com/another_spot/"],
                "spot_country": "France",
                "spot_city": "Andresport",
                "spot_street": "Campbell Falls",
                "spot_street_number": "25",
                "spot_description": "Doe",
                "spot_raiting": 4.8,
                "comment": ["spot_name1", "spot_name2", ],
                "owner_id": 1
            }
        }


class SpotFilterSchema(BaseModel):
    spot_id:  Union[int, None] = Field(gt=0, le=2147483647)  # check int32 range
    spot_country: Union[str, None] = None
    spot_city: Union[str, None] = None
    spot_street: Union[str, None] = None
    owner_id: Union[int, None] = Field(gt=0, le=2147483647)  # check int32 range

    class Config:
        orm_mode = True
        sample_schema = {
            "example": {
                "spot_id": 1,
                "spot_country": "France",
                "spot_city": "Andresport",
                "spot_street": "Campbell Falls",
                "owner_id": 1
            }
        }


class CommentSchema(BaseModel):
    body: Union[str, None]
