from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.configs.logger import configure_logging
from app.routers.post import router as post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(post_router)


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}
