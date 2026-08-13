from typing import Annotated

from agent_framework import tool
from pydantic import Field

from models import TodoList

@tool(approval_mode="never_require")
def create_todo_list(list_name: Annotated[str, Field(description="Create a todo list with a given name")]) -> TodoList:
    return TodoList(name=list_name)

@tool(approval_mode="never_require")
def add_todo(list: TodoList, todo_text: str):
    list.add_todo(todo_text=todo_text)
    return TodoList

TOOLS = [create_todo_list, add_todo]    