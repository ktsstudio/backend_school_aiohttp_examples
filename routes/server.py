from aiohttp import web

app = web.Application()
print('Application: создали экземпляр web.Application')


class MethodView(web.View):
    async def get(self):
        print(f'Application.MethodView: пришел запрос на такой URI {self.request.path}')
        if self.request.match_info:
            print(f'Application.MethodView: в URI пришла дополнительная информация {self.request.match_info=}')
        return web.Response(text=f'{dict(self.request.match_info)}')


app.router.add_view('/common_path', MethodView)
app.router.add_view('/variable_path/{id}', MethodView)
app.router.add_view('/regexp_path/{name:[a-z]+}', MethodView)

if __name__ == '__main__':
    web.run_app(app, port=9090, print=lambda _: _)
