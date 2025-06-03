#mcpo --port 8000 -- /Users/zhangtian/miniforge3/envs/langchain/bin/python /Users/zhangtian/work/langchain_learn/mcp学习/math_server.py
#执行上述命令后， 使用浏览器访问 http://localhost:8000/docs

from mcp.server.fastmcp import FastMCP

mcp_server = FastMCP("MathServer")

@mcp_server.tool()
def add(a: int, b: int) -> int:
    """执行两个整数的加法运算"""
    return a + b

@mcp_server.tool()
def multiply(a: int, b: int) -> int:
    """执行两个整数的乘法运算"""
    return a * b

if __name__ == "__main__":
    mcp_server.run(transport="stdio")