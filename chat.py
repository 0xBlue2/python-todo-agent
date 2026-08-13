import asyncio
import itertools, sys
from agent_framework import AgentResponse, Agent, AgentResponseUpdate, ResponseStream
from typing import Any

# from https://stackoverflow.com/a/22616059
async def start_spinner() -> None:
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    try:
        while True:
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            await asyncio.sleep(0.1)
            sys.stdout.write('\b')
    except asyncio.CancelledError:
        sys.stdout.write('\b')
        raise


async def stream_response(ag: Agent[Any], prompt: str):
    spinning = asyncio.create_task(start_spinner(), eager_start=True)

    result: ResponseStream[AgentResponseUpdate, AgentResponse[Any]] = await ag.run(prompt, stream=True)

    async for update in result:
        if not spinning.cancelled() and not (spinning.cancelling == 0):
            spinning.cancel()
        if update.text:
            print(update.text, end="", flush=True)
    print()