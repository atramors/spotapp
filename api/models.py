import asyncio
from datetime import datetime

from sqlalchemy import ARRAY, Boolean, Column, DateTime, ForeignKey, Integer, String, Float, Text
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class UserDBModel(Base):

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(30), unique=True, nullable=False, index=True)
    first_name = Column(String(30), unique=False, nullable=False, )
    last_name = Column(String(30), unique=False, nullable=False, )
    user_pic = Column(String, nullable=True, )
    email = Column(String, unique=True, nullable=False, )
    hashed_password = Column(String, nullable=False)
    friends = Column(ARRAY(String), nullable=True, )
    spot_photos = Column(ARRAY(String), nullable=True, )
    added_spots = Column(ARRAY(String), nullable=True, )
    favourite_spots = Column(ARRAY(String), nullable=True, )
    premium_account_type = Column(Boolean, default=False)

    # spots = relationship("Spots", back_populates="users")
    # comments = relationship("Comment", back_populates="users")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class SpotDBModel(Base):

    __tablename__ = "spots"

    spot_id = Column(Integer, primary_key=True, index=True)
    spot_name = Column(String(30))
    spot_pic = Column(String(50))

    spot_photos = Column(String)

    spot_country = Column(String(20))
    spot_city = Column(String(20))
    spot_street = Column(String(30))
    spot_street_number = Column(String(10))
    spot_full_address = Column(String(80))

    spot_description = Column(Text)
    spot_raiting = Column(Float)
    user_added_spot = Column(String(20))
    comment = Column(Text)

    owner_id = Column(Integer, ForeignKey("users.user_id"))

    # owner = relationship("Users", back_populates="spots")
    # comments = relationship("Comment", back_populates="comments")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class CommentDBModel(Base):

    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, index=True)
    body = Column(Text)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.user_id"))

    # owner = relationship("User", back_populates="spots")
    # spots = relationship("Spot", back_populates="comments")


async def async_create_tables():
    """Main program function."""
    from sqlalchemy.ext.asyncio import create_async_engine
    from api.settings import settings

    engine = create_async_engine(settings.db_dsn)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(async_create_tables())
