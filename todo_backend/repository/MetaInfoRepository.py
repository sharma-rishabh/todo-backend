from motor.motor_asyncio import AsyncIOMotorClient
from todo_backend.models import MetaInfo, Todo


class MetaInfoRepository:
    def __init__(self, db_client: AsyncIOMotorClient):
        self.client = db_client
        self.db = self.client["todo_db"]
        self.collection = self.db["meta_info"]

    def insert(self, meta_info: MetaInfo):
        return self.collection.insert_one(meta_info.model_dump())

    def get_meta_info(self) -> dict:
        return self.collection.find_one()

    def update_meta_info(self, meta_info: MetaInfo):
        return self.collection.replace_one({"id": 1}, meta_info.model_dump())
