# 导入必要模块
import os
from typing import Optional
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器实例，指定服务器名称和版本
mcp_server = FastMCP(name="DemoServer", version="1.0.0")

@mcp_server.tool()
def list_files(directory: str = "/work/langchain_learn") -> list:
    """
    获取指定目录的文件列表（默认查看桌面）
    Args:
        directory (str): 要查询的目录路径，支持 ~ 符号
    Returns:
        list: 文件名列表
    """
    try:
        # 处理跨平台路径格式
        expanded_path = os.path.expanduser(directory)
        return os.listdir(expanded_path)
    except Exception as e:
        return [f"Error: {str(e)}"]

@mcp_server.tool()
def calculate(expression: str) -> Optional[float]:
    """
    执行数学计算（支持加减乘除）
    Args:
        expression (str): 数学表达式，如 "3 + 5 * 2"
    Returns:
        float: 计算结果（保留两位小数）
    """
    try:
        # 安全计算实现（实际生产环境应使用更安全的计算方式）
        result = eval(expression)
        return round(float(result), 2)
    except:
        return None


if __name__ == "__main__":
    # 启动服务器，使用 stdio 传输协议
    mcp_server.run(
        transport='stdio',   # 标准输入输出通信
    )