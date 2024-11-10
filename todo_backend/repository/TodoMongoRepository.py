from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from todo_backend.models import Todo


class TodoMongoRepository:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.client = db_client
        self.db = self.client["todo_db"]
        self.collection = self.db["todos"]

    async def ping(self):
        self.client.admin.command("ping")

    async def get_all(self, user: str) -> List[dict]:
        return await self.collection.find({"user": user}).to_list(length=None)

    async def insert_one(self, todo: Todo):
        return self.collection.insert_one(todo.model_dump())

    def get_by_id(self, id: int, user: str) -> dict:
        return self.collection.find_one({"id": id, "user": user})

    def update(self, id: int, todo: Todo):
        return self.collection.update_one(
            {"id": id, "user": todo.user}, {"$set": todo.model_dump()}
        )
