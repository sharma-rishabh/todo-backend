import os
import random
import requests
from jwt import InvalidSignatureError, encode, decode
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from todo_backend.models import TitleRequest, Task, Todo
from todo_backend.models.Todo import Title
from todo_backend.service import TodoService

load_dotenv()
users = {}
sessions = {}


def get_access_token(sessionCode: str) -> str:
    params = {
        "client_id": os.getenv("GITHUB_CLIENT_ID"),
        "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
        "code": sessionCode,
    }
    headers = {
        "Accept": "application/json",
    }
    r = requests.post(
        "https://github.com/login/oauth/access_token",
        params=params,
        headers=headers,
    )
    r = r.json()

    if "access_token" not in r:
        raise HTTPException(status_code=400, detail="Invalid session code")

    return r["access_token"]


def get_username(access_token: str) -> str:
    user_res = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    user = user_res.json()
    if "login" not in user:
        raise HTTPException(status_code=400, detail="Couldn't get user info")

    return user["login"]


def create_session(username: str) -> str:
    session_id = len(sessions) + random.randint(0, 1000000)
    sessions[session_id] = username
    return session_id


def get_user_from_session_id(request: Request) -> str:
    print(request.headers)
    token = request.headers.get("Authorization")

    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        session_id = decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])[
            "session_id"
        ]
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return sessions[int(session_id)]


def get_token(username: str) -> str:
    session_id = create_session(username)
    token = encode(
        {"session_id": session_id}, os.getenv("JWT_SECRET"), algorithm="HS256"
    )
    return token


def get_router(todoService: TodoService) -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.get("/all-todos")
    async def all_todos(user: dict = Depends(get_user_from_session_id)) -> List[Title]:
        print("user", user)
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
        todoId: int,
        taskId: int,
        newPriority: int,
    ) -> List[Task]:
        return await todoService.update_task_priority(todoId, taskId, newPriority)

    @router.get("/login")
    async def login(
        sessionCode: str,
    ):
        access_token = get_access_token(sessionCode)
        username = get_username(access_token)
        token = get_token(username)
        response = JSONResponse(content={"username": username, "token": token})
        return response

    return router
