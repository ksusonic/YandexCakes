from aiohttp.web_response import Response
from aiohttp_apispec import response_schema, docs

from cakes.api.handlers.base import BaseView
from cakes.api.handlers.query import COURIERS_QUERY
from cakes.api.schema import CourierResponseSchema
from cakes.utils.pg import SelectQuery


class CourierView(BaseView):
    URL_PATH = r'/couriers/{courier_id:\d+}'

    @docs(summary="Возвращает информацию о курьере и дополнительную статистику: рейтинг и заработок.")
    @response_schema(CourierResponseSchema())
    async def get(self):
        body = SelectQuery(COURIERS_QUERY, self.pg.transaction())
        return Response(body=body)
