from pydantic import BaseModel

class TodoList(BaseModel):
    name: str
    list: list[TodoItem] = []

class TodoItem(BaseModel):
    text: str
    isCompleted: bool