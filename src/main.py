from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi_cache import FastAPICache
import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool
from fastapi_cache.backends.redis import RedisBackend

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate

from src.operations.router import router as router_operation

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    pool = ConnectionPool.from_url(url="redis://localhost")
    r = redis.Redis(connection_pool=pool)
    FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")
    yield

app = FastAPI(
    title="Trading App",
    lifespan=lifespan
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)
