from aiohttp import web
from aiohttp.web_response import json_response

# этот пример демонстрирует то, как бы мы выполняли те же действия,
# что и в custom_application.py, но без тайпингов
app = web.Application()


class Store:
    def fetch_data(self):
        return 'data fetched from store'


# первый способ добавления своих полей к Application - через аттрибут
app.store = Store()

# второй способ добавления своих полей к Application - через значение в словаре.
# Application можно воспринимать как словарь и хранить в нем нужные данные
app['store'] = Store()


# унаследовали MethodView от обычного aiohttp.web.View
class MethodView(web.View):
    async def get(self):
        # на следующую строку ругается IDE - не видит параметра store в aiohttp.web.Application
        data = self.request.app.store.fetch_data()
        print(f'CommonApplication.MethodView: получили данные с помощью доступа по аттрибуту: {data}')

        data = self.request.app['store'].fetch_data()
        print(f'CommonApplication.MethodView: получили данные с помощью доступа по ключу в словаре Application: {data}')
        return json_response(data={'data': data})


app.router.add_view('/method', MethodView)
if __name__ == '__main__':
    web.run_app(app, port=9090, print=lambda _: _)
