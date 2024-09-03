from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.sms.adapters.db.orm import start_mappers
from src.sms.adapters.entry_points.api.base import api_router
from src.sms.config.containers import Container


def start_application():
    container = Container()
    app_ = FastAPI()
    app_.container = container
    app_.include_router(api_router)
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    try:
        start_mappers()
    except Exception as err:
        # Checking if the mapper was already started
        if "already has a primary mapper defined" not in str(err):
            raise RuntimeError(err) from err
    return app_


app = start_application()
