import random

import aiohttp
import asyncio
from faker import Faker

faker = Faker()


async def main():
    async with aiohttp.ClientSession() as session:
        username = faker.user_name()

        while True:
            try:
                ws = await session.ws_connect('ws://aiohttp:8080')
                break
            except aiohttp.client_exceptions.ClientConnectionError:
                # Retry in a sec
                asyncio.sleep(1)
        while True:
            await ws.send_json({
                'username': username,
                'message': faker.sentence(),
            })
            # random number between 0.0 - 5.0
            pause = random.randint(0, 50) / 10
            await asyncio.sleep(pause)

if __name__ == "__main__":
    asyncio.run(main())
    # main()
