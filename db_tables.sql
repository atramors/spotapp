CREATE TABLE IF NOT EXISTS users(
    user_id serial PRIMARY KEY,
    nickname varchar(30) NOT NULL,
    first_name varchar(30) NULL,
    last_name varchar(30) NULL,
    user_pic varchar(30) NULL,
    email varchar(30) NULL,
    hashed_password varchar(80) NULL,
    friends text NULL,
    spot_photos text NULL,
    added_spots text NULL,
    favourite_spots text NULL,
    premium_account_type boolean DEFAULT FALSE,
    created_at timestamp NOT NULL DEFAULT now(),
    updated_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS spots(
    spot_id serial PRIMARY KEY,
    spot_name varchar(30) NOT NULL,
    spot_pic text NOT NULL,
    spot_photos text NOT NULL,

    spot_country varchar(20),
    spot_city varchar(20),
    spot_street varchar(30),
    spot_street_number varchar(10),
    spot_full_address varchar(80),

    spot_description = text NOT NULL,
    spot_raiting decimal NOT NULL,
    user_added_spot varchar(30) NOT NULL,
    comment text NULL,

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="spots")
    comments = relationship("Comment", back_populates="spot_comment")
    created_at timestamp NOT NULL DEFAULT now(),
    updated_at timestamp NOT NULL DEFAULT now()
);