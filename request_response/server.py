from aiohttp import web

app = web.Application()
print('Application: создали экземпляр web.Application')


async def view(request: web.Request):
    print(f'Application.view: принял новый {request.method}-запрос по пути {request.path}')
    if request.query:
        print(f'Application.view: в запросе есть query-строка, после парсинга она выглядит так {request.query}')
    if request.headers.get('Content-Type') == 'application/json':
        print(f'Application.view: в запросе есть json-данные, потому что Content-Type == application/json')
        print(f'Application.view: ждем их получения в сокете и считываем')
        json_data = await request.json()
        print(f'Application.view: считали json-данные: {json_data}')

    resp = web.Response(status=200, text='hello')
    print(f'Application.view: подготовили response со статусом ответа {resp.status} и текстом {resp.text}')
    print(f'Application.view: возвращаем ответ из view, чтобы он был преобразован в http и был записан в сокет')
    return resp


print('Application: создали function-based handler, который будет обрабатывать запросы')

app.router.add_get('/method', view)
print('Application: добавили Route, который при GET-запросе на 127.0.0.1:9090/method вызовет view')

app.router.add_post('/method', view)
print('Application: добавили Route, который при POST-запросе на 127.0.0.1:9090/method вызовет view. '
      'Ничего не мешает, использовать для одинакового пути (/method) разные http-методы (GET, POST)')

if __name__ == '__main__':
    web.run_app(app, port=9090, print=lambda _: _)
