import asyncio

import aiohttp


async def make_requests():
    session = aiohttp.ClientSession()

    input('>>> послать GET-запрос на http://127.0.0.1:9090/method ?')
    async with session.request('GET', 'http://127.0.0.1:9090/method') as resp:
        print(f'Client: получили ответ с текстом {await resp.text()}')

    await session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_requests())
