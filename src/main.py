import uvicorn
from fastapi import FastAPI
from src.api import api_router


import logging.config
import logging.handlers
import atexit
from contextlib import asynccontextmanager
from typing import AsyncContextManager

from src.core.config import uvicorn_options
from src.core.logger import LOGGING_CONFIG

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncContextManager[None]:
    logging.config.dictConfig(LOGGING_CONFIG)
    # получаем обработчик очереди из корневого логгера
    queue_handler = logging.getHandlerByName("queue_handler")
    try:
        # если логгер есть
        if queue_handler is not None:
            # запускаем слушатель очереди
            queue_handler.listener.start()
            # регистрируем функцию, которая будет вызвана при завершении работы программы
            atexit.register(queue_handler.listener.stop)
        yield
    finally:
        # в случае ошибки выключаем слушатель
        if queue_handler is not None:
            queue_handler.listener.stop()

app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/openapi"
)

app.include_router(api_router)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        **uvicorn_options
    )