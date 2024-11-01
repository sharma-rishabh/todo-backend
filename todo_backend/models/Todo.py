from typing import List
from pydantic import BaseModel

from todo_backend.models import Task


class Todo(BaseModel):
    id: int
    title: str
    deleted: bool
    priority: int
    latest_task_id: int = 0
    least_task_priority: int = 0
    tasks: List[Task]

    def add_task(self, title: str) -> Task:
        self.latest_task_id += 1
        self.least_task_priority += 1
        task = Task(
            id=self.latest_task_id,
            title=title,
            deleted=False,
            completed=False,
            priority=self.least_task_priority,
        )
        self.tasks.append(task)
        return task

    @staticmethod
    def serialize(obj: dict):
        return Todo(
            id=obj["id"],
            title=obj["title"],
            deleted=obj["deleted"],
            priority=obj["priority"],
            latest_task_id=obj["latest_task_id"],
            least_task_priority=obj["least_task_priority"],
            tasks=[Task.serialize(task) for task in obj["tasks"]],
        )

    @staticmethod
    def to_titles(obj: dict):
        return Title(id=obj["id"], title=obj["title"], priority=obj["priority"])


class Title(BaseModel):
    id: int
    title: str
    priority: int
