import logging
from functools import partial
from types import AsyncGeneratorType, MappingProxyType
from typing import AsyncIterable, Mapping

from aiohttp import PAYLOAD_REGISTRY
from aiohttp.web_app import Application
from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware

from cakes.api.middleware import error_middleware, handle_validation_error
from cakes.api.payloads import AsyncGenJSONListPayload, JsonPayload
from cakes.api.handlers import HANDLERS
from cakes.utils.pg import setup_pg

log = logging.getLogger(__name__)


def create_app() -> Application:
    """
    Создает экземпляр приложения, готового к запуску.
    """
    app = Application(
        middlewares=[error_middleware, validation_middleware]
    )

    # Подключение на старте к postgres и отключение при остановке
    app.cleanup_ctx.append(partial(setup_pg))

    # Регистрация обработчиков
    for handler in HANDLERS:
        log.debug('Registering handler %r as %r', handler, handler.URL_PATH)
        app.router.add_route('*', handler.URL_PATH, handler)

    # Swagger документация
    setup_aiohttp_apispec(app=app, title='Cakes API', swagger_path='/',
                          error_callback=handle_validation_error)

    # Автоматическая сериализация в json данных в HTTP ответах
    PAYLOAD_REGISTRY.register(AsyncGenJSONListPayload,
                              (AsyncGeneratorType, AsyncIterable))
    PAYLOAD_REGISTRY.register(JsonPayload, (Mapping, MappingProxyType))
    return app
