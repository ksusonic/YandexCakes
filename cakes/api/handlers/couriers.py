from http import HTTPStatus
from typing import Generator

from aiohttp.web_response import Response
from aiohttp_apispec import docs, request_schema, response_schema
from aiomisc import chunk_list

from cakes.api.schema import CourierResponseSchema, CourierSchema
from cakes.db.schema import couriers_table as couriers_t
from cakes.utils.pg import SelectQuery, MAX_QUERY_ARGS

from .base import BaseView
from .query import COURIERS_QUERY


class CouriersView(BaseView):
    URL_PATH = '/couriers'

    # Так как данных может быть много, а postgres поддерживает только
    # MAX_QUERY_ARGS аргументов в одном запросе, писать в БД необходимо
    # частями.
    # Максимальное кол-во строк для вставки можно рассчитать как отношение
    # MAX_QUERY_ARGS к кол-ву вставляемых в таблицу столбцов.
    MAX_COURIERS_PER_INSERT = MAX_QUERY_ARGS // len(couriers_t.columns)

    @classmethod
    def make_couriers_table_rows(cls, couriers) -> Generator:
        """
        Генерирует данные готовые для вставки в таблицу couriers.
        """
        for courier in couriers:
            yield {
                'courier_id': couriers['courier_id'],
                'courier_type': couriers['courier_type'],
                'regions': couriers['regions'],
                'working_hours': couriers['working_hours']
            }

    @docs(summary='Добавить информацию о курьерах')
    @request_schema(CourierSchema())
    @response_schema(CourierResponseSchema(), code=HTTPStatus.CREATED.value)
    async def post(self):
        # Транзакция требуется чтобы в случае ошибки (или отключения клиента,
        # не дождавшегося ответа) откатить частично добавленные изменения.
        async with self.pg.transaction() as conn:
            query = couriers_t.insert().returning(couriers_t.c.courier_id)
            courier_id = await conn.fetchval(query)

            couriers = self.request['data']['couriers']
            courier_rows = self.make_couriers_table_rows(couriers)

            # Чтобы уложиться в ограничение кол-ва аргументов в запросе к
            # postgres, а также сэкономить память и избежать создания полной
            # копии данных присланных клиентом во время подготовки - используем
            # генератор chunk_list.
            # Он будет получать из генератора make_citizens_table_rows только
            # необходимый для 1 запроса объем данных.
            chunked_couriers_rows = chunk_list(courier_rows, self.MAX_COURIERS_PER_INSERT)

            query = couriers_t.insert()
            for chunk in chunked_couriers_rows:
                await conn.execute(query.values(list(chunk)))

        return Response(body={'data': {'courier_id': courier_id}},
                        status=HTTPStatus.CREATED)
