
from fastapi import FastAPI

app = FastAPI()


todos = [
        {"id": 1, "title": "Buy Milk", "description": "Buy Milk from the store"}, { "id": 2, "title": "Buy Bread", "description": "Buy Bread from the store"}
    ]

@app.get("/api/all-todos")
async def read_root():
    return todos

@app.get("/api/todo/{todo_id}")
async def read_item(todo_id: int):
    return todos[todo_id]