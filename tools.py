from typing import Annotated

from agent_framework import tool
from pydantic import Field

from models import TodoList

@tool(approval_mode="never_require")
def create_todo_list(list_name: Annotated[str, Field(description="Create a todo list with a given name")]) -> TodoList:
    return TodoList(name=list_name)


    