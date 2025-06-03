
from mcp.server.fastmcp import FastMCP

mcp_server = FastMCP("name") # 创建一个 FastMCP 实例，并指定一个名称

# @mcp.resource 装饰器用于定义资源，它为客户端提供访问特定功能或数据的接口。
# 使用这个装饰器时，通常指定一个自定义的路径，在这个路径上，用户可以通过访问来获取资源信息。资源通常是与服务器的状态或配置相关的数据，比如个性化信息、系统状态等。



# 定义一个简单的资源函数，资源路径为 "greeting://{name}"
# 该资源将会接受一个名字作为参数，返回一个问候消息
@mcp_server.resource("greeting://{name}")
def greet_user(name: str) -> str:
    # 返回一条包含用户名称的问候消息
    return f"Hello, {name}!"

# 定义一个资源，返回一个固定的消息
@mcp_server.resource("greeting://hello")
def say_hello() -> str:
    # 返回一个固定的问候语
    return "Hello, World!"

# 另一个资源，模拟返回一个简单的加法结果
@mcp_server.resource("add_numbers://{num1}/{num2}")
def add_numbers(num1: int, num2: int) -> int:
    # 返回两个数字的和
    return num1 + num2

# 启动 MCP 服务器，设置传输方式为 'stdio'，即通过标准输入输出交互
def start_server():
    # mcp.run() 启动一个 MCP 服务器
    mcp_server.run(
        transport='stdio',   # 使用标准输入输出（stdio）进行通信
        # show_banner=True,     # 显示启动横幅信息
        # log_level="debug"     # 设置日志级别为调试模式，以便查看详细日志
    )

if __name__ == "__main__":
    # 启动服务器
    start_server()