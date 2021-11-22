"""
создайте асинхронные функции для выполнения запросов к ресурсам (используйте aiohttp)
"""

import asyncio
from dataclasses import dataclass
from aiohttp import ClientSession
from homework_04.main import async_session
from models import User

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


@dataclass
class Resource:
    name: str
    url: str


RESOURCE = [
    Resource("Users", "https://jsonplaceholder.typicode.com/users"),
    Resource("Posts", "https://jsonplaceholder.typicode.com/posts"),
]


async def fetch_json(url: str):
    async with ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def run_main():
    for resource in RESOURCE:
        res = await fetch_json(resource.url)
        async with async_session() as session:
            async with session.begin():
                for user in res:
                    user = User(
                        user_id=user["id"],
                        name=user["name"],
                        username=user["username"],
                        email=user["email"])
                    session.add(user)


def main():
    asyncio.run(run_main())


if __name__ == '__main__':
    main()

