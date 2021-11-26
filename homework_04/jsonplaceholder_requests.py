"""
создайте асинхронные функции для выполнения запросов к ресурсам (используйте aiohttp)
"""

import asyncio
from aiohttp import ClientSession
from homework_04.models import async_session, User, Post


USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def fetch_json(url: str):
    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def fetch_data():
    users_data, posts_data = await asyncio.gather(
        fetch_users_data(),
        fetch_posts_data(),
    )
    async with async_session() as session:
        async with session.begin():
            for user in users_data:
                user = User(
                    user_id=user["id"],
                    name=user["name"],
                    username=user["username"],
                    email=user["email"]
                )
                session.add(user)
            for post in posts_data:
                post = Post(
                    user_id=post["userId"],
                    title=post["title"],
                    body=post["body"],
                    id=post["id"]
                )
                session.add(post)


async def fetch_users_data():
    return await fetch_json(USERS_DATA_URL)


async def fetch_posts_data():
    return await fetch_json(POSTS_DATA_URL)


def main():
    asyncio.run(fetch_data())


if __name__ == '__main__':
    main()

