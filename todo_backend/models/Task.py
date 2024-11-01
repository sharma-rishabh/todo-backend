from pydantic import BaseModel


class Task(BaseModel):
    id: int
    title: str
    deleted: bool
    completed: bool
    priority: int

    @staticmethod
    def serialize(obj: dict):
        return Task(
            id=obj["id"],
            title=obj["title"],
            deleted=obj["deleted"],
            completed=obj["completed"],
            priority=obj["priority"],
        )
