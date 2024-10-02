
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from todo_backend.Todo import Todo
from todo_backend.TodoRepository import TodoRepository

app = FastAPI()

repository = TodoRepository()


@app.get("/api/all-todos")
async def read_root() -> List[Todo]:
    return repository.get_all_todos()

@app.get("/api/todo/{todo_id}")
async def read_item(todo_id: int) -> Todo:
    todo = repository.get_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
    