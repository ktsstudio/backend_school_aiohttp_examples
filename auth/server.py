import datetime

from aiohttp import web
from aiohttp.web_exceptions import HTTPUnauthorized
from aiohttp_session import get_session, setup as setup_aiohttp_session, SimpleCookieStorage

app = web.Application()


class UnsecuredView(web.View):
    """незащищенный метод, доступный всем пользователям"""

    async def get(self):
        session = await get_session(self.request)
        print(f'UnsecuredView: сессия запроса {session}')
        return web.Response(text='данные доступные для неавторизованного пользователя')


class SecuredView(web.View):
    """защищенный метод, доступный только авторизованным пользователям"""

    async def get(self):
        session = await get_session(self.request)  # пытаемся загрузить объект сессии из куки
        if session.new:  # если куки нет или она не валидна, то aiohttp-session создаст новую сессию
            print('SecuredView: Пользователь не авторизован, отдаю 401')
            raise HTTPUnauthorized(reason='Нет авторизации')

        # можно получить данные из сессии как из словаря
        print(f'SecuredView: пришел пользователь {session["user"]["username"]}, '
              f'последний раз он логинился {session["user"]["last_login"]}')
        return web.Response(text='данные доступные только для авторизованного пользователя')


class AuthView(web.View):
    """метод авторизации"""

    async def get(self):
        data = self.request.query
        print(f'AuthView: пользователь логинится с данными {data}')

        assert data['username'] == 'admin'
        assert data['password'] == 'admin'
        # создаем новую сессию
        session = await get_session(self.request)

        # дополняем данными
        session['user'] = {
            'username': data['username'],
            'last_login': datetime.datetime.now().isoformat(),
        }
        print(f'AuthView: теперь в сессии хранится объект пользователя: {session["user"]=}')

        # отдаем успешный ответ с этой сессией
        return web.Response(text='пользователь авторизован')


# SimpleCookieStorage - данные сессии в незашифрованном виде хранятся в куки
setup_aiohttp_session(app, SimpleCookieStorage())

app.router.add_view('/no_auth', UnsecuredView)
app.router.add_view('/need_auth', SecuredView)
app.router.add_view('/auth', AuthView)

if __name__ == '__main__':
    print()
    web.run_app(app, port=9090, print=lambda _: _)
