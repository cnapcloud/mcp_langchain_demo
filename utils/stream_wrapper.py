from typing import Any, Dict
from langchain_core.runnables import Runnable

class RunnableStreamWrapper(Runnable):
    """
    Wraps an async generator to be compatible with RunnableLambda.
    Supports invoke, ainvoke, and astream.
    """
    def __init__(self, func):
        self.func = func  # async generator function

    # invoke: runs the async generator to completion and returns the combined result
    def invoke(self, input: Any, config: Dict = None):
        import asyncio
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.ainvoke(input, config))
    
    # ainvoke: runs the async generator to completion and returns the combined result
    async def ainvoke(self, input: Any, config: Dict = None):
        result = ""
        async for chunk in self.func(input):
            result += chunk
        return result

    # astream: async generator 자체를 반환
    async def astream(self, input: Any, config: Dict = None):
        async for chunk in self.func(input):
            yield chunk
