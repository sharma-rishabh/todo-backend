from typing import List
from todo_backend.models import Task, Todo, Title, MetaInfo
from todo_backend.repository import MetaInfoRepository, TodoMongoRepository


class TodoService:
    def __init__(
        self,
        todo_repository: TodoMongoRepository,
        meta_info_repository: MetaInfoRepository,
    ) -> None:
        self.repository = todo_repository
        self.meta_info_repository = meta_info_repository

    async def get_titles(self, user: str) -> List[Title]:
        res = await self.repository.get_all(user)
        return [Todo.to_titles(todo) for todo in res if not todo["deleted"]]

    async def get_meta_info(self, user: str) -> MetaInfo:
        raw_meta_info = await self.meta_info_repository.get_meta_info(user)
        if raw_meta_info is None:
            meta_info = MetaInfo(user=user)
            await self.meta_info_repository.insert(meta_info)
            return meta_info

        return MetaInfo.serialize(raw_meta_info)

    async def add_todo(self, title: str, user: str) -> Todo:
        meta_info = await self.get_meta_info(user)
        meta_info.increment_todo_id()
        meta_info.increment_priority()

        todo = Todo(
            user=user,
            id=meta_info.latest_todo_id,
            title=title,
            deleted=False,
            priority=meta_info.least_priority,
            tasks=[],
        )

        await self.repository.insert_one(todo)
        await self.meta_info_repository.update_meta_info(meta_info)
        return todo

    async def edit_title(self, todo_id: int, title: str, user: str) -> Title:
        todo = await self.get_todo_by_id(todo_id, user)
        todo.title = title
        await self.repository.update(todo_id, todo)
        return Title(id=todo_id, title=title, priority=todo.priority)

    async def delete_title(self, todo_id: int, user: str) -> List[Title]:
        todo = await self.get_todo_by_id(todo_id, user)
        todo.deleted = True
        await self.repository.update(todo_id, todo)
        return await self.get_titles(user)

    async def get_todo_by_id(self, todo_id: int, user: str) -> Todo:
        res = await self.repository.get_by_id(todo_id, user)
        serialized = Todo.serialize(res)
        return serialized

    async def add_task(self, todo_id: int, title: str, user: str) -> Task:
        todo = await self.get_todo_by_id(todo_id, user)
        task = todo.add_task(title)
        await self.repository.update(todo_id, todo)
        return task

    async def toggle_completed(self, todo_id: int, task_id: int, user: str) -> Task:
        todo = await self.get_todo_by_id(todo_id, user)
        task = todo.toggle_completed(task_id)
        await self.repository.update(todo_id, todo)
        return task

    async def edit_task_title(
        self, todo_id: int, task_id: int, title: str, user: str
    ) -> Task:
        todo = await self.get_todo_by_id(todo_id, user)
        task = todo.update_task_title(task_id, title)
        await self.repository.update(todo_id, todo)
        return task

    async def delete_task(self, todo_id: int, task_id: int, user: str) -> List[Task]:
        todo = await self.get_todo_by_id(todo_id, user)
        todo.delete_task(task_id)
        await self.repository.update(todo_id, todo)
        return todo.active_tasks()

    async def update_task_priority(
        self, todo_id: int, task_id: int, new_priority: int, user: str
    ) -> List[Task]:
        todo = await self.get_todo_by_id(todo_id, user)
        todo.update_task_priority(task_id, new_priority)
        await self.repository.update(todo_id, todo)
        return todo.active_tasks()
