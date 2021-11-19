import asyncio
from pprint import pprint

import aiohttp


async def make_requests():
    session = aiohttp.ClientSession()

    requests = [
        'http://127.0.0.1:9090/user',
        'http://127.0.0.1:9090/user?first_name=vasya&height=1000000',
        'http://127.0.0.1:9090/user?first_name=vasya&birthdate=10.12.1990',
        'http://127.0.0.1:9090/user?first_name=vasya',
        'http://127.0.0.1:9090/user?first_name=vasya&height=193&birthdate=10.12.1990&know_aiohttp=true',
    ]

    for request in requests:
        input(f'послать GET-запрос на {request} ?')
        async with session.request('GET', request) as resp:
            print(f'>>> получили ответ со статусом {resp.status} и текстом {await resp.text()}', end='\n\n')

    input(f'послать GET-запрос на http://127.0.0.1:9090/swagger.json?')
    async with session.request('GET', 'http://127.0.0.1:9090/swagger.json') as resp:
        print(f'Получили такую swagger-документацию')
        pprint(await resp.json())
    await session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_requests())
