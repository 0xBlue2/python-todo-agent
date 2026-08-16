from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field
from agent_framework import tool

from utils import read_todo_list, write_todo_list


class TodoItem(BaseModel):
    """A todo item with text, an ID, and isCompleted status."""

    text: str
    isCompleted: bool = False


class TodoList(BaseModel):
    """A list of TodoItems, with a name."""

    name: str
    items: list[TodoItem] = []


class CreateTodoListSchema(BaseModel):
    """Input schema when creating a new todo list."""

    name: Annotated[str, Field(description="The name of the todo list - should be slugged / sanitized to be used as a file name")]


class ReadTodoListSchema(CreateTodoListSchema):
    """Input schema when reading from a todo list."""


class CompleteTodoSchema(BaseModel):
    """Input schema when completing or uncompleting a todo item."""

    name: Annotated[str, Field(description="The name of the todo list")]
    index: Annotated[int, Field(description="The index of the todo item to be affected - first index is 1")]
    is_completed: Annotated[
        bool,
        Field(description="The value to set for the todo: true is completed, false is not completed"),
    ]


class UpdateTodoSchema(BaseModel):
    """Input schema when changing a todo item's text."""

    name: Annotated[str, Field(description="The name of the todo list")]
    index: Annotated[int, Field(description="The index of the todo item to be affected - first index is 1")]
    text: Annotated[str, Field(description="The text description to set for the todo item")]


class DeleteTodoSchema(BaseModel):
    """Input schema when deleting a todo item from a list."""

    name: Annotated[str, Field(description="The name of the todo list")]
    index: Annotated[int, Field(description="The index of the todo item to be affected - first index is 1")]


class AddTodoSchema(BaseModel):
    """Input schema when adding a todo item to a list."""

    name: Annotated[str, Field(description="The name of the todo list")]
    text: Annotated[str, Field(description="The text description for the new todo item")]

class TodoToolClass:
    @tool(
        description="Create a todo list with a name, and save it to disk.",
        schema=CreateTodoListSchema,
        approval_mode="never_require",
    )
    def create_todo_list(self, name: str):
        new_list = TodoList(name=name)
        write_todo_list(new_list)
        return f"Created todo list '{name}'."

    @tool(
        description="Add a todo item to an existing todo list",
        schema=AddTodoSchema,
        approval_mode="never_require",
    )
    def add_todo(self, name: str, text: str):
        todo_list = read_todo_list(name)
        todo_list.items.append(TodoItem(text=text))
        write_todo_list(todo_list)
        return f"Added '{text}' to list '{name}'."

    @tool(
        description="Get a comma-separated list of todos on a todo list.",
        schema=ReadTodoListSchema,
        approval_mode="never_require",
    )
    def get_todos(self, name: str):
        items = read_todo_list(name).items
        if not items:
            return f"No todos in '{name}', or couldn't find a todo list by the same name."
        return ", ".join(item.text for item in items)

    @tool(
        description="Mark a todo item as completed or not completed.",
        schema=CompleteTodoSchema,
        approval_mode="never_require",
    )
    def complete_todo(self, name: str, index: int, is_completed: bool):
        todo_list = read_todo_list(name)
        if index < 1 or index > len(todo_list.items):
            raise ValueError("Todo index out of range.")

        todo_list.items[index - 1].isCompleted = is_completed
        write_todo_list(todo_list)
        status = "completed" if is_completed else "not completed"
        return f"Set item {index} in '{name}' to {status}."

    @tool(
        description="Update a todo item's text by index.",
        schema=UpdateTodoSchema,
        approval_mode="never_require",
    )
    def update_todo(self, name: str, index: int, text: str):
        todo_list = read_todo_list(name)
        if index < 1 or index > len(todo_list.items):
            raise ValueError("Todo index out of range.")

        todo_list.items[index - 1].text = text
        write_todo_list(todo_list)
        return f"Updated item {index} in '{name}' to '{text}'."

    @tool(
        description="Delete a todo item from an existing list by index.",
        schema=DeleteTodoSchema,
        approval_mode="never_require",
    )
    def delete_todo(self, name: str, index: int):
        todo_list = read_todo_list(name)
        if index < 1 or index > len(todo_list.items):
            raise ValueError("Todo index out of range.")

        removed = todo_list.items.pop(index - 1)
        write_todo_list(todo_list)
        return f"Deleted '{removed.text}' from '{name}'."

    @tool(
        description="List all saved todo list files in the todo_lists directory.",
        approval_mode="never_require",
    )
    def list_todo_lists(self):
        todo_dir = Path("todo_lists")
        if not todo_dir.exists():
            return "No todo_lists directory exists yet."

        files = sorted(path.name for path in todo_dir.iterdir() if path.is_file())
        if not files:
            return "No todo lists have been created yet."
        return ", ".join(files)


todo_tool = TodoToolClass()
TOOLS = [
    todo_tool.create_todo_list,
    todo_tool.add_todo,
    todo_tool.get_todos,
    todo_tool.complete_todo,
    todo_tool.update_todo,
    todo_tool.delete_todo,
    todo_tool.list_todo_lists,
]