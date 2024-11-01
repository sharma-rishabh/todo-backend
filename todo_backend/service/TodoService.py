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

    async def get_titles(self) -> List[Title]:
        res = await self.repository.get_all()
        return [Todo.to_titles(todo) for todo in res if not todo["deleted"]]

    async def get_meta_info(self) -> MetaInfo:
        raw_meta_info = await self.meta_info_repository.get_meta_info()
        if raw_meta_info is None:
            meta_info = MetaInfo()
            await self.meta_info_repository.insert(meta_info)
            return meta_info

        return MetaInfo.serialize(raw_meta_info)

    async def add_todo(self, title: str) -> Todo:
        meta_info = await self.get_meta_info()
        meta_info.increment_todo_id()
        meta_info.increment_priority()

        todo = Todo(
            id=meta_info.latest_todo_id,
            title=title,
            deleted=False,
            priority=meta_info.least_priority,
            tasks=[],
        )

        await self.repository.insert_one(todo)
        await self.meta_info_repository.update_meta_info(meta_info)
        return todo

    async def edit_title(self, todo_id: int, title: str) -> Title:
        todo = await self.get_todo_by_id(todo_id)
        todo.title = title
        await self.repository.update(todo_id, todo)
        return Title(id=todo_id, title=title, priority=todo.priority)

    async def delete_title(self, todo_id: int) -> List[Title]:
        todo = await self.get_todo_by_id(todo_id)
        todo.deleted = True
        await self.repository.update(todo_id, todo)
        return await self.get_titles()

    async def get_todo_by_id(self, todo_id: int) -> Todo:
        res = await self.repository.get_by_id(todo_id)
        serialized = Todo.serialize(res)
        return serialized

    async def add_task(self, todo_id: int, title: str) -> Task:
        todo = await self.get_todo_by_id(todo_id)
        task = todo.add_task(title)
        await self.repository.update(todo_id, todo)
        return task
