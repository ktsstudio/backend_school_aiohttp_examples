import asyncio

import aiohttp


async def make_requests():
    print('Client: создали клиентскую сессию - в ней хранится '
          'общая информация для всех запросов, связанных с этой сессией. Например, там хранятся общие куки')
    session = aiohttp.ClientSession()

    input('>>> послать GET-запрос на http://127.0.0.1:9090/method c query-строкой ?a=b ?')
    async with session.request('GET', 'http://127.0.0.1:9090/method?a=b') as resp:
        print(f'Client: получили ответ со статусом {resp.status} и текстом {await resp.text()}')

    input('>>> послать GET-запрос на http://127.0.0.1:9090/method c json-данными {"data": "important"} ?')
    async with session.request('POST', 'http://127.0.0.1:9090/method', json={'data': 'important'}) as resp:
        print(f'Client: получили ответ со статусом {resp.status} и текстом {await resp.text()}')

    print('закрываем aiohttp.ClientSession, чтобы освободить ресурсы')
    await session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_requests())
