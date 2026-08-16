#!/usr/bin/env python3
from agent_framework import Agent
from agent_framework_gemini import GeminiChatClient
from agent_framework.devui import serve


from dotenv import load_dotenv
load_dotenv()

from models import TOOLS

client = GeminiChatClient()
agent = Agent(
    client=client,
    name="Todo Assistant",
        instructions="You are a helpful assistant for todo lists. Use tools to create or modify the user's todo lists. Keep responses short.",
        tools=TOOLS
)

serve(entities=[agent], auto_open=True)