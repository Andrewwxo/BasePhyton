"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_async_engine(
    "postgresql+asyncpg://postgres:12345678@localhost/postgres",
)

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ ="users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)

    posts = relationship("Post", back_populates="author")

    def __str__(self):
        return f"{self.__class__.__name__}(user_id={self.user_id}," \
               f"name={self.name!r}, " \
               f"username={self.username!r}, " \
               f"email={self.email})"

    def __repr__(self):
        return str(self)


class Post(Base):
    __tablename__ = "posts"

    user_id = Column(Integer, ForeignKey(User.user_id))
    title = Column(String, nullable=False, default="", server_default="")
    body = Column(Text, nullable=False, default="", server_default="" )
    id = Column(Integer, primary_key=True)

    author = relationship(User, back_populates="posts")

    def __str__(self):
        return f"{self.__class__.__name__}(user_id={self.user_id}, " \
               f"title={self.title!r}, " \
               f"body={self.body})"

    def __repr__(self):
        return str(self)

