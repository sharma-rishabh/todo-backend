from pydantic import BaseModel


class AddTodoRequest(BaseModel):
    title: str