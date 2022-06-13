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

EXAMPLE_USER_422 = {
    'detail': [
        {
            'loc': ['path', 'user_id'],
            'msg': 'value is not a valid integer',
            'type': 'type_error.integer'
        }
    ]
}
