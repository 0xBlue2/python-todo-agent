from pathlib import Path
from models import TodoList


def read_todo_list(list_name: str) -> TodoList:
    from models import TodoList

    path = Path("todo_lists") / list_name
    if not path.exists():
        raise FileNotFoundError(f"Todo list '{list_name}' does not exist.")

    with path.open("r", encoding="utf-8") as file:
        return TodoList.model_validate_json(file.read())


def write_todo_list(todo_list: TodoList):
    path = Path("todo_lists") / todo_list.name
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        file.write(todo_list.model_dump_json())