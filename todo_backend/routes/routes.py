from typing import List
from fastapi import APIRouter

from todo_backend.models import AddTodoRequest, Task, Todo
from todo_backend.models.Todo import Title
from todo_backend.service import TodoService


def get_router(todoService: TodoService) -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.get("/all-todos")
    async def all_todos() -> List[Title]:
        return await todoService.get_titles()

    @router.post("/add-todo")
    async def add_todo(title: AddTodoRequest) -> Title:
        print("title", title)
        return await todoService.add_todo(title.title)

    @router.put("/edit-title/{todo_id}")
    async def edit_title(todo_id: int, title: AddTodoRequest) -> Title:
        return await todoService.edit_title(todo_id, title.title)

    @router.put("/delete-title/{todo_id}")
    async def delete_title(todo_id: int) -> List[Title]:
        return await todoService.delete_title(todo_id)

    @router.get("/todo/{todo_id}")
    async def get_todo_by_id(todo_id: int) -> Todo:
        return await todoService.get_todo_by_id(todo_id)

    @router.post("/add-task/{todo_id}")
    async def add_task(todo_id: int, title: str) -> Task:
        return await todoService.add_task(todo_id, title)

    return router
