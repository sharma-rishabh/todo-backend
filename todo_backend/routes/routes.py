from typing import List
from fastapi import APIRouter

from todo_backend.models import Task, Todo
from todo_backend.models.Todo import Title
from todo_backend.service import TodoService


def get_router(todoService: TodoService) -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.get("/all-todos")
    async def all_todos() -> List[Title]:
        return await todoService.get_titles()

    @router.post("/add-todo")
    async def add_todo(title: str) -> Title:
        return await todoService.add_todo(title)

    @router.get("/todo/{todo_id}")
    async def get_todo_by_id(todo_id: int) -> Todo:
        return await todoService.get_todo_by_id(todo_id)

    @router.post("/add-task/{todo_id}")
    async def add_task(todo_id: int, title: str) -> Task:
        return await todoService.add_task(todo_id, title)

    return router
