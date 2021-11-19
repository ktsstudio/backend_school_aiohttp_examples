import asyncio

import aiohttp


async def make_requests():
    session = aiohttp.ClientSession()

    requests = [
        'http://127.0.0.1:9090/common_path',
        'http://127.0.0.1:9090/variable_path/1',
        'http://127.0.0.1:9090/regexp_path/name',
        'http://127.0.0.1:9090/regexp_path/123',
    ]

    for i, request in enumerate(requests):
        input(f'>>> послать GET-запрос на {request} ?')
        async with session.request('GET', request) as resp:
            print(f'Client: получили ответ с match_info = {await resp.text()}')
            if i == 3:
                print('Client: потому что regexp-паттерн '
                      'Route включает в себя только буквы от a до z, а мы передали цифры')
            print('\n')

    await session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_requests())
