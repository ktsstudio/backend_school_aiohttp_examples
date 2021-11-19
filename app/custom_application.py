from aiohttp import web
from aiohttp.web_response import json_response


class Store:
    def fetch_data(self):
        return 'data fetched from store'


# унаследовали Application от web.Application
class Application(web.Application):
    """класс, в котором мы используем тайпинги для удобства написания кода"""
    store: Store  # добавили к классу Application поле store


# унаследовали Request от web.Request
class Request(web.Request):

    # переопределили property для подмены тайпингов для Application
    # request.app все еще возвращает обычное web.Application, но IDE будет подсказывать тайпинги нашего Application
    @property
    def app(self) -> Application:
        return super().app


# унаследовали View от web.View
class View(web.View):
    # переопределили property request для подмены тайпингов для Request
    @property
    def request(self) -> Request:
        return super().request

    # сократили путь для получения app: вместо self.request.app теперь можно писать просто self.app
    @property
    def app(self) -> Application:
        return self.request.app

    # сократили путь для получения store, используя предыдущее property:
    # вместо self.request.app.store теперь можно писать просто self.store
    @property
    def store(self) -> 'Store':
        return self.app.store


# унаследовали MethodView от нашего View
class MethodView(View):
    async def get(self):
        print(f'CustomApplication.MethodView: приняли новый {self.request.method}-запрос по пути {self.request.path}')
        print('CustomApplication.MethodView: пробуем вызвать '
              'метода store.fetch_data(), IDE подсказывает, что такой метод есть')
        data = self.store.fetch_data()
        print(
            'CustomApplication.MethodView: метод вызван и IDE не ругается, '
            'что такого метода нет, ведь мы следовали соглашению с тайпингом Application '
            'и добавили реальное поле Store при настройке приложения'
        )

        print(
            'CustomApplication.MethodView: вернем json-ответ, воспользуюсь функцией json_response из aiohttp.web_response. '
            'Передадим в нее словарь с данными из Store'
        )

        # формирует обычный web.Response,
        # но берет на себя проставление заголовка Content-Type и преобразование данных в json
        return json_response(data={'data': data})


app: Application = web.Application()
print('CustomApplication: создали экземпляр web.Application и подменили его тайпинг на наше Application')
try:
    print('CustomApplication: пробуем обратиться к store - полю, '
          'которое есть только в Application, но нет в web.Application')
    print(app.store)
except AttributeError:
    print(f'CustomApplication: получили AttributeError - поля store нет, '
          f'потому что на самом деле в питоне {type(app)=}, a не {Application}')

print('CustomApplication: добавили атрибут store к app')
app.store = Store()

print('CustomApplication: пробуем опять обратиться к store')
print(app.store)
print('CustomApplication: ошибки теперь нет')

print('CustomApplication: добавили Route, '
      'который при запросах на 127.0.0.1:9090/method вызовет нужный метод MethodView')
app.router.add_view('/method', MethodView)

if __name__ == '__main__':
    web.run_app(app, port=9090, print=lambda _: _)
