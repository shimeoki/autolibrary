from fastapi import FastAPI
from uvicorn import run

from web.router import api_router
from web.dependencies import engine
from db import models


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(api_router)


if __name__ == '__main__':
    run('web.main:app', reload=True, log_level="info")