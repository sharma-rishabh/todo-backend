from typing import List
from fastapi import APIRouter

from todo_backend.models import TitleRequest, Task, Todo
from todo_backend.models.Todo import Title
from todo_backend.service import TodoService


def get_router(todoService: TodoService) -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.get("/all-todos")
    async def all_todos() -> List[Title]:
        return await todoService.get_titles()

    @router.post("/add-todo")
    async def add_todo(title: TitleRequest) -> Title:
        print("title", title)
        return await todoService.add_todo(title.title)

    @router.put("/edit-title/{todo_id}")
    async def edit_title(todo_id: int, title: TitleRequest) -> Title:
        return await todoService.edit_title(todo_id, title.title)

    @router.put("/delete-title/{todo_id}")
    async def delete_title(todo_id: int) -> List[Title]:
        return await todoService.delete_title(todo_id)

    @router.get("/todo/{todo_id}")
    async def get_todo_by_id(todo_id: int) -> Todo:
        return await todoService.get_todo_by_id(todo_id)

    @router.put("/toggle-completed/{todoId}/{taskId}")
    async def toggle_completed(todoId: int, taskId: int) -> Task:
        return await todoService.toggle_completed(todoId, taskId)

    @router.post("/add-task/{todoId}")
    async def toggle_completed(todoId: int, addTaskRequest: TitleRequest) -> Task:
        return await todoService.add_task(todoId, addTaskRequest.title)

    @router.put("/edit-task-title/{todoId}/{taskId}")
    async def edit_task_title(todoId: int, taskId: int, title: TitleRequest) -> Task:
        return await todoService.edit_task_title(todoId, taskId, title.title)

    @router.put("/delete-task/{todoId}/{taskId}")
    async def delete_task(todoId: int, taskId: int) -> List[Task]:
        return await todoService.delete_task(todoId, taskId)

    @router.put("/update-task-priority/{todoId}/{taskId}/{newPriority}")
    async def update_task_priority(
        todoId: int, taskId: int, newPriority: int
    ) -> List[Task]:
        return await todoService.update_task_priority(todoId, taskId, newPriority)

    return router
