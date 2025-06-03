# client_demo.py
import asyncio
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

async def main():
    # 配置服务器参数（假设服务器脚本为 server_demo.py）
    server_params = StdioServerParameters(
        command="/Users/zhangtian/miniforge3/envs/langchain/bin/python",     # 启动命令
        args=["/Users/zhangtian/work/langchain_learn/mcp学习/base_mcp_tool_study2.py"],  # 服务器脚本路径
        env=None              # 可选环境变量
    )

    try:
        # 建立与服务器的连接（异步上下文管理器）
        async with stdio_client(server_params) as (read_stream, write_stream):
            # 创建客户端会话
            async with ClientSession(
                read_stream,
                write_stream,
                sampling_callback=None  # 采样回调（可选）
            ) as session:
                
                # 初始化会话
                await session.initialize()
                print("[STATUS] 已成功连接 MCP 服务器")

                # 获取可用工具列表
                tools_response = await session.list_tools()
                print("\n可用工具列表：")
                for tool in tools_response.tools:
                    print(f"- {tool.name}: {tool.description}")

                print(tools_response)
                # # 调用计算器工具示例
                # print("\n正在执行计算：(188 * 23-34)/5")
                # result = await session.call_tool(
                #     "calculate",          # 工具名称
                #     {"expression": "(188 * 23-34)/5"}  # 参数（需符合工具输入模式）
                # )

                # # 处理响应
                # if result.error:
                #     print(f"错误：{result.error.message}")
                # else:
                #     print(f"计算结果：{result.content}")

    except Exception as e:
        print(f"连接失败：{str(e)}")
        print("请检查：1.服务器路径是否正确 2.服务器是否已启动")

if __name__ == "__main__":
    # 启动异步事件循环
    asyncio.run(main())