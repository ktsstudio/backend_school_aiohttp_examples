import asyncio

import aiohttp


async def make_requests():
    # aiohttp client по умолчанию не ставит куки на IP адреса,
    # для этого нужно задать параметр unsafe в aiohttp.CookieJar
    jar = aiohttp.CookieJar(unsafe=True)
    session = aiohttp.ClientSession(cookie_jar=jar)

    requests = [
        'http://127.0.0.1:9090/no_auth',
        'http://127.0.0.1:9090/need_auth',
        'http://127.0.0.1:9090/auth?username=admin&password=admin',
        'http://127.0.0.1:9090/need_auth',
    ]

    for i, request in enumerate(requests):
        input(f'>>> послать GET-запрос на {request} ?')
        async with session.request('GET', request) as resp:
            print(f'Client: получили ответ со статусом {resp.status} и текстом "{await resp.text()}"')
            if resp.cookies:
                print(f'Client: в запросе были присланы cookie: {resp.cookies}')
        print('\n')
    await session.close()


def run_request():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_requests())


if __name__ == '__main__':
    run_request()
