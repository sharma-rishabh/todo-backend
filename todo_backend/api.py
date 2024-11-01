from fastapi import FastAPI
from todo_backend.service import TodoService
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from todo_backend.routes import get_router
from todo_backend.repository import MetaInfoRepository, TodoMongoRepository

app = FastAPI()


uri = "mongodb://localhost:27017/"
client = AsyncIOMotorClient(uri, server_api=ServerApi("1"))
repo = TodoMongoRepository(client)
meta_info_repo = MetaInfoRepository(client)
service = TodoService(repo, meta_info_repo)
router = get_router(service)

app.include_router(router)