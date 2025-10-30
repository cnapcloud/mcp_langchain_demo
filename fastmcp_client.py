import asyncio
from fastmcp import Client
from functools import wraps

_client_instance = None  # 싱글톤 인스턴스 저장
_client_url = None       # 프로토콜/URL 저장

# 데코레이터: Client 싱글톤 사용
def with_client(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        global _client_instance, _client_url
        if _client_instance is None:
            if _client_url is None:
                raise RuntimeError("Client URL is not specified. You need to set _client_url.")
            _client_instance = Client(_client_url)
            await _client_instance.__aenter__()
            print(f"Connection URL: {_client_url}\n")

        return await func(*args, **kwargs)
    return wrapper

# 도구 목록 조회 및 출력
@with_client

async def show_tools():
    tools = await _client_instance.list_tools()  # 기존 호출
    print("Available Tools:")
    for tool in tools:
        name = tool.name
        description = tool.description or "No description"
        print(f"- {name}: {description}")
    return tools

# 도구 호출 및 결과 출력
@with_client
async def call_add_tool(a=5, b=3):
    result = await _client_instance.call_tool("add", {"a": a, "b": b})
    print(f"Call Add Tool:")
    print(f"- Input: a={a}, b={b}")
    print(f"- Output: {result.content[0].text}")
    return result


# 선택적으로 호출
if __name__ == "__main__":
    async def main():
        global _client_url

        # 연결 URL/프로토콜 한 번만 지정
        _client_url = "http://localhost:8001/sse"

        # 데코레이터로 Client 싱글톤을 자동 사용
        await show_tools()
        await call_add_tool()

        # Client 종료
        await _client_instance.__aexit__(None, None, None)

    asyncio.run(main())
