import logging
import os
from collections import AsyncIterable
from pathlib import Path
from types import SimpleNamespace
from typing import Union

from aiohttp.web_app import Application
from asyncpgsa import PG
from asyncpgsa.transactionmanager import ConnectionTransactionContextManager
from sqlalchemy.sql import Select
from alembic.config import Config
from configargparse import Namespace

PROJECT_PATH = Path(__file__).parent.parent.resolve()
DEFAULT_PG_URL = 'postgresql://localhost:5432/yandexcakes'
MAX_QUERY_ARGS = 32767

log = logging.getLogger(__name__)


async def setup_pg(app: Application) -> PG:
    log.info('Connecting to database:')

    app['pg'] = PG()
    await app['pg'].init(
        DEFAULT_PG_URL,
    )
    await app['pg'].fetchval('SELECT 1')
    log.info('Connected to database')

    try:
        yield
    finally:
        log.info('Disconnecting from database')
        await app['pg'].pool.close()
        log.info('Disconnected from database')


def make_alembic_config(cmd_opts: Union[Namespace, SimpleNamespace],
                        base_path: str = PROJECT_PATH) -> Config:
    """
    Создает объект конфигурации alembic на основе аргументов командной строки,
    подменяет относительные пути на абсолютные.
    """
    # Подменяем путь до файла alembic.ini на абсолютный
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name,
                    cmd_opts=cmd_opts)

    # Подменяем путь до папки с alembic на абсолютный
    alembic_location = config.get_main_option('script_location')
    if not os.path.isabs(alembic_location):
        config.set_main_option('script_location',
                               os.path.join(base_path, alembic_location))
    if cmd_opts.pg_url:
        config.set_main_option('sqlalchemy.url', cmd_opts.pg_url)

    return config


class SelectQuery(AsyncIterable):
    """
    Используется чтобы отправлять данные из PostgreSQL клиенту сразу после
    получения, по частям, без буфферизации всех данных.
    """
    PREFETCH = 1000

    __slots__ = (
        'query', 'transaction_ctx', 'prefetch', 'timeout'
    )

    def __init__(self, query: Select,
                 transaction_ctx: ConnectionTransactionContextManager,
                 prefetch: int = None,
                 timeout: float = None):
        self.query = query
        self.transaction_ctx = transaction_ctx
        self.prefetch = prefetch or self.PREFETCH
        self.timeout = timeout

    async def __aiter__(self):
        async with self.transaction_ctx as conn:
            cursor = conn.cursor(self.query, prefetch=self.prefetch,
                                 timeout=self.timeout)
            async for row in cursor:
                yield row
