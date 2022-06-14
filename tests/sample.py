RAW_USER = {
    "nickname": "test_user",
    "first_name": "fake_name",
    "last_name": "fake_name2",
    "user_pic": "fake_pic",
    "email": "somefake@gmail.com",
    "password": "strong_password",
    "premium_account_type": False,
}

EXAMPLE_USER_GET = {
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
