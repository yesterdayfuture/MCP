# 文件名：mcp_server.py
from mcp.server.fastmcp import FastMCP
import asyncio

mcp = FastMCP("Weather-Tool-Server", port=8008)

# 注册天气查询工具
@mcp.tool()
async def get_weather(city: str) -> str:
    """根据城市名查询实时天气（模拟实现）"""
    await asyncio.sleep(1)  # 模拟网络延迟
    return f"{city}天气：25℃ 晴"

# 注册加法计算器
@mcp.tool()
def add(a: int, b: int) -> int:
    """计算两数之和"""
    return a + b

if __name__ == "__main__":
    # 启动SSE服务（远程调用）
    mcp.run(transport="sse") 