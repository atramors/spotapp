RAW_USER = {
    "nickname": "rickstar",
    "first_name": "rick",
    "last_name": "morty",
    "user_pic": "fake_pic",
    "email": "rickstar@fake.com",
    "password": "strong_password",
    "premium_account_type": False,
}

EXAMPLE_USER = {
    "nickname": "test_user",
    "first_name": "test_name",
    "last_name": "test_name2",
    "user_pic": "test_pic",
    "friends": ["one_friend", "another_friend"],
    "spot_photos": ["photo", "photo1", ],
    "added_spots": ["some_test_spot", ],
    "favourite_spots": ["some_test_spot", ]
}

EXAMPLE_NEW_USER_ADD = {
    "nickname": "test_user",
    "email": "somefake@gmail.com"
}

EXAMPLE_USER_422 = {
    'detail': [
        {
            'loc': ['path', 'user_id'],
            'msg': 'value is not a valid integer',
            'type': 'type_error.integer'
        }
    ]
}

DELETED_USER = "User with user_id=123 is disappear..."
DELETED_SPOT = "Spot with spot_id=123 is destroied..."

EXAMPLE_SPOT = {
    "spot_name": "Theatr",
    "spot_pic": "https://patrick.com/",
    "spot_photos": ["https://patrick.com/some_spot/", "https://patrick.com/another_spot/"],
    "spot_country": "France",
    "spot_city": "Andresport",
    "spot_street": "Campbell Falls",
    "spot_street_number": "25",
    "spot_description": "Doe",
    "spot_raiting": 4,
    "comment": [],
    "owner_id": 1
}
EXAMPLE_SPOT_422 = {
    'detail': [
        {
            'loc': ['path', 'spot_id'],
            'msg': 'value is not a valid integer',
            'type': 'type_error.integer'
        }
    ]
}
RAW_SPOT = {
    "spot_name": "Theatr",
    "spot_pic": "https://patrick.com/",
    "spot_photos": ["https://patrick.com/some_spot/", "https://patrick.com/another_spot/"],
    "spot_country": "France",
    "spot_city": "Andresport",
    "spot_street": "Campbell Falls",
    "spot_street_number": "25",
    "spot_description": "Doe",
    "owner_id": 1
}

EXAMPLE_COMMENT = {
    "comment_id": 1,
    "body": "This is awesome spot!",
    "owner_id": 1
}
EXAMPLE_COMMENT_422 = {
    'detail': [
        {
            'loc': ['path', 'comment_id'],
            'msg': 'value is not a valid integer',
            'type': 'type_error.integer'
        }
    ]
}
