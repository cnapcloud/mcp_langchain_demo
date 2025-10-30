import asyncio
import traceback
from typing import Any, AsyncGenerator, Dict, Generator
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from llm.manager import get_llm
from utils.stream_wrapper import RunnableStreamWrapper
from conf import config

MCP_SERVER_URL = config.MCP_SERVER_URL
_agent_instance = None

# MCP 에이전트 생성
async def create_mcp_agent():
    """Create or return a singleton MCP-based ReAct agent."""
    global _agent_instance
    if _agent_instance is not None:
        return _agent_instance

    client = MultiServerMCPClient({
        "add": {"transport": "sse", "url": MCP_SERVER_URL}
    })
    tools = await client.get_tools()

    _agent_instance = create_agent(
        model=get_llm(),
        tools=tools,
        system_prompt="You are a helpful assistant."
    )
    return _agent_instance

# MCP 에이전트 호출
async def invoke_mcp_agent(data: Dict[str, Any]) -> str:
    """Invoke the MCP agent and return the final response text."""
    messages = data.get("messages")
    if not messages:
        raise ValueError("The 'messages' field is required.")
    agent = await create_mcp_agent()
    response = await agent.ainvoke({"messages": messages})
    return response["messages"]

# MCP 에이전트 스트리밍 응답에서 텍스트 청크만 추출
async def stream_text_chunks(data: Dict[str, Any]) -> AsyncGenerator[str, None]:
    """
    agent.stream()으로부터 오는 token 중 content type이 'text'인 경우만 yield
    """
    agent = await create_mcp_agent()
    async for token, metadata in agent.astream(
        data,
        stream_mode="messages",
    ):
        for block in token.content_blocks:
            if block.get("type") == "text":
                yield block.get("text", "")
                
# 질문을 LangGraph 형식으로 변환
def to_message_format(text: str) -> Dict[str, Any]:
    """Convert input text into LangGraph message format."""
    return {"messages": [("user", text)]}

# Runnable 체인 생성
mcp_chain = RunnableLambda(to_message_format) | invoke_mcp_agent
mcp_chain_stream = RunnableLambda(to_message_format) |  RunnableStreamWrapper(stream_text_chunks)

# MCP 에이전트 실행 
async def main():
    try:
        questions = [
            "15와 27를 더하는 계산하세요.",
            "너는 뭐하는 AI야?",
        ]

        ## Message list
        q = questions[0]
        response = await mcp_chain.ainvoke(q)

        print("> Ainvoke: full message list (batch)")
        print(f"=== 질문: {q} ===")
        for i, msg in enumerate(response, start=1):
            tool_info = getattr(msg, "tool_calls", "") if isinstance(msg, AIMessage) else ""
            content = getattr(msg, "content", str(msg))
            msg_type = getattr(msg, "type", str(type(msg)))
            print(f"{i}. {msg_type}: {content}{tool_info}")
        print("\n")

        ## Streaming
        print("> Streaming: text chunks (real-time)")
        for q in questions:
            print(f"=== 질문: {q} ===")
            async for token in mcp_chain_stream.astream(q):
                print(token, end="", flush=True)
            print("\n")

    except Exception as e:
        print("\n[Error in main execution]:", e)
        traceback.print_exc()
           
if __name__ == "__main__":
    asyncio.run(main())