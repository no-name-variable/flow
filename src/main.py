import os

from fastapi import FastAPI, requests
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise

from apps.core import exceptions
from apps.applications import routs as app_routs
from apps.flow import routs as flow_routs

import config

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


app = FastAPI(
    title="Flow",
    version="0.1",
)


app.include_router(prefix='/api', router=app_routs.router, tags=['Application'])
app.include_router(prefix='/api', router=flow_routs.router, tags=['Flow'])


def register_db(app: FastAPI):
    Tortoise.init_models(config.DB_CONF['apps']['models']['models'], "models")
    register_tortoise(
        app,
        config=config.DB_CONF,
        generate_schemas=True,
        add_exception_handlers=False,
    )


@app.exception_handler(exceptions.SubjectNotFoundError)
async def subject_not_found_handler(request: requests.Request, exc: exceptions.SubjectNotFoundError):
    return JSONResponse(
        status_code=400,
        content={
            "code": exc.code,
            'data': None,
            'error': {
                "message": exc.description
            }
        }
    )


@app.exception_handler(exceptions.ServiceUnknownError)
async def service_unknown_error_handler(request: requests.Request, exc: exceptions.ServiceUnknownError):
    return JSONResponse(
        status_code=400,
        content={
            "code": exc.code,
            'data': None,
            'error': {
                "message": exc.description
            }
        }
    )


@app.exception_handler(exceptions.ServiceUnavailableError)
async def service_unavailable_error_handler(request: requests.Request, exc: exceptions.ServiceUnavailableError):
    return JSONResponse(
        status_code=400,
        content={
            "code": exc.code,
            'data': None,
            'error': {
                "message": exc.description
            }
        }
    )
