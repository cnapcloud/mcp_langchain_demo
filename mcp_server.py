from fastmcp import FastMCP

print("[INIT] MCP Server starting...")
mcp = FastMCP("example-mcp",)

# 툴 등록
@mcp.tool
def echo(text: str) -> str:
    """Echoes back the input text."""
    print(f"[CALL] echo() called with text='{text}'")
    return text

@mcp.tool
def add(a: float, b: float) -> float:
    """Adds two numbers and returns the sum."""
    print(f"[CALL] add() called with a={a}, b={b}")
    result = a + b
    print(f"[RESULT] add() = {result}")
    return result

@mcp.tool
def greet(name: str) -> str:
    """Returns a greeting message."""
    print(f"[CALL] greet() called with name='{name}'")
    message = f"Hello, {name}!"
    print(f"[RESULT] greet() = {message}")
    return message

# 서버 실행
if __name__ == "__main__":
    print("[START] Running MCP Server on http://0.0.0.0:8001 (transport=SSE)")
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=8001,
    )
