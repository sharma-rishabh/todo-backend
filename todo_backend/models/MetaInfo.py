from pydantic import BaseModel


class MetaInfo(BaseModel):
    id: int = 1
    latest_todo_id: int = 0
    least_priority: int = 0

    def increment_todo_id(self):
        self.latest_todo_id += 1

    def increment_priority(self):
        self.least_priority += 1

    @staticmethod
    def serialize(obj: dict):
        return MetaInfo(
            id=obj["id"],
            latest_todo_id=obj["latest_todo_id"],
            least_priority=obj["least_priority"],
        )
