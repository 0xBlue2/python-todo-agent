from pydantic import BaseModel

class TodoList(BaseModel):
    name: str
    list: list[TodoItem] = []
    def add_todo(self, todo_text: str):
        item: TodoItem = TodoItem(text=todo_text, id=len(self.list))

class TodoItem(BaseModel):
    text: str
    id: int
    isCompleted: bool = False