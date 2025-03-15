import uvicorn
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from src.router.router import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo_client = AsyncIOMotorClient("mongodb://admin:123@localhost:27017")
    app.state.mongodb_client = mongo_client
    app.state.mongo_db = mongo_client["coderbuddy"]

    yield

    mongo_client.close()


def api():
    fast_api = FastAPI(
        title="modelhub-api", description="ModelHub API", lifespan=lifespan
    )
    fast_api.include_router(main_router)
    return fast_api


if __name__ == "__main__":
    uvicorn.run(
        api(),
        host="0.0.0.0",
        port=8080,
    )
