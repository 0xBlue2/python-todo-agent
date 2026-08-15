#!/usr/bin/env python3

import asyncio
from typing import Any
from agent_framework import Agent, BaseChatClient
from agent_framework_ollama import OllamaChatClient
from agent_framework_gemini import GeminiChatClient

import os
from dotenv import load_dotenv
load_dotenv()

from tools import TOOLS
from chat import stream_response
from constants import QUIT_COMMANDS

MODEL = "llama3.2" # model for local development with ollama
MODE = "remote" # or "local"

client: BaseChatClient

match MODE:
    case "remote":
        client = GeminiChatClient()
        #TOOLS.append(client.get_web_search_tool())
    case "local":
        client = OllamaChatClient(MODEL=MODEL)

async def main():
    agent = Agent(
        client=client,
        name="Todo Assistant",
        instructions="You are a helpful assistant for todo lists. Use the create_todo_list tool and web search tool when necessary. Keep responses short.",
        tools=TOOLS
    )

    while True:
        user_input = input("> ")
        if user_input.lower() in QUIT_COMMANDS:
            break
        else:
            await stream_response(agent, user_input)

asyncio.run(main())