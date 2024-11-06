from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.configs.database import database
from app.configs.logger import configure_logging
from app.routers.post import router as post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


app.include_router(post_router)


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to Jinstagram"}
