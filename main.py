#!/usr/bin/env python3.14

import asyncio
from typing import Any
from agent_framework import Agent, AgentResponseUpdate, ResponseStream, AgentResponse
from agent_framework_ollama import OllamaChatClient

from tools import TOOLS
from chat import stream_response

MODEL = "llama3.2"
async def main():
    agent = Agent(
        client=OllamaChatClient(model=MODEL),
        name="Todo Assistant",
        instructions="You are a helpful assistant for todo lists. Use the create_todo_list tool when necessary. Keep responses short.",
        tools=TOOLS
    )

    await stream_response(agent, input("> "))

asyncio.run(main())