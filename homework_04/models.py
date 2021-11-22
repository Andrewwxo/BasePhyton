"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""

import os
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

PG_CONN_URI = os.environ.get("SQLALCHEMY_PG_CONN_URI") or "postgresql+asyncpg://postgres:12345678@localhost/postgres"

engine = create_engine("sqlite:///homework_04.db", echo=True)
Base = declarative_base(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class User(Base):
    __tablename__ ="users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    username = Column(String(32), unique=True)
    email = Column(String(16), unique=True)

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

    user_id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False, default="", server_default="")
    body = Column(String(512), nullable=False)
    author_id = Column(Integer, ForeignKey(User.user_id), nullable=False)

    author = relationship(User, back_populates="posts")

    def __str__(self):
        return f"{self.__class__.__name__}(user_id={self.user_id}, " \
               f"title={self.title!r}, " \
               f"body={self.body}" \
               f"author_id={self.author_id},)"

    def __repr__(self):
        return str(self)


def create_user(name: str, username: str, email: str) -> User:

    session = Session()
    user = User(name=name, username=username, email=email)
    session.add(user)
    session.commit()
    session.close()
    return user


def get_user(username: str) -> User:
    """
    :param username:
    :return: User
    """
    session = Session()
    user = session.query(User).filter_by(username=username).one()
    session.close()
    return user


def create_post(author: User, title: str, body: str, author_id: int ) -> Post:
   """
   :param author:
   :param title:
   :param body:
   :param author_id:
   :return: post
   """

    session = Session()

    post = Post(
        title=title,
        author=author,
        body=body,
        author_id=author_id
    )
    session.add(post)
    session.commit()
    session.close()
    return post


def main():
    Base.metadata.create_all()
    create_user("Sam Smith", "Sam", "sam1@mail.com")
    user_sam = get_user("Sam")
    create_post(user_sam, "First lesson", "It's a short story", 1)


if __name__ == '__main__':
    main()