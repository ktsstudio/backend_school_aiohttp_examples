from aiohttp import web
from aiohttp.web_response import json_response
from aiohttp_apispec import docs, querystring_schema, response_schema, validation_middleware, json_schema
from aiohttp_apispec import setup_aiohttp_apispec
from marshmallow import Schema, fields, validate

print('создали экземпляр web.Application')
app = web.Application()

print('настроили aiohttp_apispec ДО настройки routes. Путь для SwaggerUI = /swagger, для json-Swagger = /swagger.json')
setup_aiohttp_apispec(app, title='Documentation', swagger_path='/swagger', url='/swagger.json')


class RequestSchema(Schema):
    first_name = fields.String(required=True)
    height = fields.Float(validate=validate.Range(min=150, max=210), load_default=170)
    birthdate = fields.DateTime(format='%d.%M.%Y', required=False)
    know_aiohttp = fields.Boolean(load_default=False)


class UserView(web.View):
    @docs(tags=['users'], summary='Получает информацию о пользователе и валидирует ее')
    @querystring_schema(RequestSchema)
    async def get(self):
        print(f'Данные, которые validation_middleware положила '
              f'в querystring {self.request.get("querystring")} при запросе {self.request.path}\n')
        return web.Response(text=str(self.request.get("querystring")))


class TestViewResponseSchema(Schema):
    class DataSchema(Schema):
        first_name = fields.Str()
        height = fields.Float()
        birthdate = fields.DateTime(allow_none=True)
        know_aiohttp = fields.Bool()

    status = fields.String(validate=validate.OneOf(('ok', 'error')))
    data = fields.Nested(DataSchema)


class TestView(web.View):
    @docs(tags=['users'], summary='Нужен для демонстрации того, как Swagger отобразит этот View')
    @json_schema(RequestSchema)
    @response_schema(TestViewResponseSchema)
    async def post(self):
        return json_response(data={
            'status': 'ok',
            'data': {
                'first_name': 'lexa',
                'height': 184,
                'birthdate': '30.06.1990',
                'know_aiohttp': True,
            },
        })


print('добавили Route /user')
app.router.add_view('/user', UserView)

print('добавили Route /test_route, чтобы показать как он отобразится в Swagger-документации')
app.router.add_view('/test_route', TestView)

print('добавили aiohttp_apispec.validation_middleware')
app.middlewares.append(validation_middleware)

if __name__ == '__main__':
    web.run_app(app, port=9090)
