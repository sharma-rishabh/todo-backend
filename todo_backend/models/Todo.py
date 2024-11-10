from typing import List
from pydantic import BaseModel

from todo_backend.models import Task


class Todo(BaseModel):
    user: str
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

    def find_task(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"Task with id {task_id} not found")

    def toggle_completed(self, task_id: int) -> Task:
        task = self.find_task(task_id)
        task.completed = not task.completed
        return task

    def update_task_title(self, task_id: int, title: str) -> Task:
        task = self.find_task(task_id)
        task.title = title
        return task

    def delete_task(self, task_id: int) -> Task:
        task = self.find_task(task_id)
        task.deleted = True
        return task

    def active_tasks(self) -> List[Task]:
        return [task for task in self.tasks if not task.deleted]

    def update_task_priority(self, task_id: int, new_priority: int) -> List[Task]:
        task_to_update = next((task for task in self.tasks if task.id == task_id), None)

        if not task_to_update:
            raise ValueError(f"Task with id {task_id} not found")

        task_to_update.priority = new_priority
        other_tasks = [task for task in self.tasks if task.id != task_id]
        new_priority_set = set([new_priority])
        updated_tasks = [task_to_update]
        next_free_priority = 1

        for task in sorted(other_tasks, key=lambda t: t.priority):

            while next_free_priority in new_priority_set:
                next_free_priority += 1
            task.priority = next_free_priority
            new_priority_set.add(task.priority)
            updated_tasks.append(task)
            next_free_priority += 1

        self.tasks = sorted(updated_tasks, key=lambda t: t.priority)
        return self.tasks

    @staticmethod
    def serialize(obj: dict):
        return Todo(
            user=obj["user"],
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
        return Title(
            id=obj["id"], title=obj["title"], priority=obj["priority"], user=obj["user"]
        )


class Title(BaseModel):
    id: int
    title: str
    priority: int
