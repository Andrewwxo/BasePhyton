"""
Домашнее задание №3
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""

import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import joinedload, selectinload, sessionmaker

from homework_04.models import Base, User, Post


engine = create_async_engine(
    "postgresql+asyncpg://postgres:12345678@localhost/postgres",
)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def create_tables():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_admin_user():
    user = User(username="admin", is_staff=True)

    async with async_session() as session:  # type: AsyncSession
        async with session.begin():
            session.add(user)


async def create_some_users():
    user_sam = User(username="sam")

    async with async_session() as session:  # type: AsyncSession
        async with session.begin():
            session.add_all([
                user_sam,
                User(username="john"),
            ])

    print("user_sam", user_sam)


async def create_posts_for_users():
    # stmt_q_users = select(User)
    stmt_user_sam = select(User).where(User.username == "sam")
    stmt_user_john = select(User).where(User.username == "john")

    async with async_session() as session:  # type: AsyncSession
        async with session.begin():
            user_sam = (await session.execute(stmt_user_sam)).scalar_one_or_none()
            user_john = (await session.execute(stmt_user_john)).scalar_one_or_none()

            print(user_sam)
            print(user_john)

            # noinspection PyArgumentList
            post_django = Post(
                title="Django lesson",
                body="Hello Django..",
                author=user_john,
            )

            post_news = Post(
                title="Python news",
                body="Hello Python news..",
                author=user_sam,
            )

            # noinspection PyArgumentList
            session.add_all([
                Post(title="Flask lesson", body="Hello Flask..", author=user_sam),
                post_django,
                post_news,
            ])

    print(post_django.id, post_django.title, post_django.author)
    print(post_news.id, post_news.title, post_news.author)


async def fetch_posts_with_authors():
    stmt = select(Post).options(joinedload(Post.author)).order_by(Post.id)
    async with async_session() as session:  # type: AsyncSession
        result = await session.execute(stmt)

    # select users by ids
    # stmt = select(User).where(User.id.in_([1, 3, 5, 7]))

    for post in result.scalars():  # type: Post
        print("Post", post.id, post.title, post.author)


async def fetch_users_with_posts():
    stmt_users_with_posts = (
        select(User)
        .options(selectinload(User.posts))
        .order_by(User.id)
    )

    print("stmt_users_with_posts", stmt_users_with_posts)
    async with async_session() as session:  # type: AsyncSession
        result = await session.execute(stmt_users_with_posts)

    for user in result.scalars():  # type: User
        print(user)
        for post in user.posts:
            print("--", post.id, post.title)


async def async_main():
    await create_admin_user()
    await get_user_by_pk()
    await create_some_users()
    await create_posts_for_users()
    await fetch_posts_with_authors()
    await fetch_users_with_posts()


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
