#学习基础的 mcp server 的使用

from mcp.server.fastmcp import FastMCP

mcp_server = FastMCP("哈哈哈")


@mcp_server.tool(description="获取两数之和")
def multiplay(a:int, b:int):
    return a+b


def run():
    mcp_server.run(
        transport="stdio"
    )

if __name__ == '__main__':
    print("mcp server is running")
    run()