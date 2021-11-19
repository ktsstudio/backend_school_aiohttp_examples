from aiohttp import web

app = web.Application()
print('Application: создали экземпляр web.Application')


class MethodView(web.View):
    async def get(self):
        print('Application.MethodView: выполняется метод get у MethodView')
        print(f'Application.MethodView: во View получили данные запроса, '
              f'добавленные second_middleware: {self.request["second_middleware"]}')
        return web.Response(text=self.request['second_middleware'])


@web.middleware
async def second_middleware(request: web.Request, handler):
    print('Application.second_middleware: я выполняюсь')
    print(f'Application.second_middleware: следующим запрос будет обрабатывать {handler}')

    request['second_middleware'] = 'important_data'
    print(f'Application.second_middleware: добавила в объект запроса такие данные: {request["second_middleware"]}')

    resp = await handler(request)
    print('Application.second_middleware: выполнилась, возвращаю ответ')
    return resp


@web.middleware
async def first_middleware(request: web.Request, handler):
    print('Application.first_middleware: я выполняюсь')
    print(f'Application.first_middleware: следующим запрос будет обрабатывать {handler}')
    resp = await handler(request)
    print('Application.first_middleware: выполнилась, возвращаю ответ')
    return resp


print('Application: добавили Route /method')
app.router.add_view('/method', MethodView)

print('Application: добавили сначала first_middleware, а потом second_middleware')
app.middlewares.append(first_middleware)
app.middlewares.append(second_middleware)

if __name__ == '__main__':
    web.run_app(app, port=9090, print=lambda _: _)
