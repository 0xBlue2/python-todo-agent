from pydantic import BaseModel

class TodoItem(BaseModel):
    text: str
    id: int
    isCompleted: bool = False

class TodoList(BaseModel):
    name: str
    items: list[TodoItem] = []
    def add_todo(self, todo_text: str):
        item: TodoItem = TodoItem(text=todo_text, id=len(self.list))
        self.items.append(item)

    def get_todos(self):
        return self.items