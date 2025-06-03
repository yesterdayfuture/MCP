# client_auto_tool.py
import asyncio
import json
from typing import Any
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from langchain_community.llms.ollama import Ollama
from langchain_community.llms.sparkllm import SparkLLM
import os
from langchain_huggingface import HuggingFaceEndpoint, HuggingFacePipeline

from dotenv import load_dotenv
load_dotenv()


# 使用星火大模型
llama3 = SparkLLM(
    model="SparkLLM/Max-32K",
    api_url="wss://spark-api.xf-yun.com/chat/max-32k"
    )

async def analyze_input_with_llm(user_input: str, tools_info: list) -> dict:
    """
    调用大模型进行工具选择决策（模拟实现）
    参考网页4的LLM集成方案和网页9的架构设计
    """
    # print(f"调用大模型进行工具选择决策，输入：{user_input}")
    # tools_info_str = json.dumps(tools_info, indent=2, ensure_ascii=False)

    # 构造提示词（需根据实际模型调整）
    prompt = f"""
    请根据用户请求选择最合适的工具：
    {tools_info}
    
    示例：

    用户请求：计算 1+1的值

    返回格式：
    [{{
        "tool": "calculate",
        "params": {{"expression": "1+1"}}
    }}]

    用户请求：{user_input}
    
    返回格式：
    [{{
        "tool": "工具名称1", 
        "params": {{"参数1":"值", "参数2":"值"}}
    }},...,{{
        "tool": "工具名称n", 
        "params": {{"参数1":"值", "参数2":"值"}}
    }}]

    你是一个简洁的助手，只需回答问题本身，不要包含任何分析过程。
    """

    # print(f"提示词：{prompt}")
    
    # # 此处应替换为真实的大模型API调用（参考网页4的代码示例）
    # # 示例模拟大模型返回结果
    # if "计算" in user_input or "算" in user_input:
    #     return {"tool": "calculate", "params": {"expression": user_input.split("：")[-1]}}
    # elif "文件" in user_input or "桌面" in user_input:
    #     return {"tool": "file_analyzer", "params": {"file_path": "~/Desktop"}}
    # else:
    #     return {"error": "未找到匹配工具"}
    # llm = Ollama(model="deepseek-r1:7b")
    result = llama3.invoke(prompt)
    # print(f"大模型返回结果：{result}")
    return result

async def main():
    # 配置服务器参数（服务器脚本为 /Users/zhangtian/work/langchain_learn/mcp学习/base_mcp_tool_study2.py）
    server_params = StdioServerParameters(
        command="/Users/zhangtian/miniforge3/envs/langchain/bin/python",     # 启动命令
        args=["/Users/zhangtian/work/langchain_learn/mcp学习/base_mcp_tool_study2.py"],  # 服务器脚本路径
        env=None              # 可选环境变量
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write, sampling_callback= None) as session:
                # 初始化连接（增加超时限制）
                await asyncio.wait_for(session.initialize(), timeout=10.0)
                
                # 获取工具元数据
                tools_res = await session.list_tools()

                # print(tools_res)

                tools_info = [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema
                    } for tool in tools_res.tools
                ]

                # print(tools_info)
                
                # 用户输入（示例）
                user_input = input("请输入需求：")

                # user_input = "请帮我写一篇关于汽车的10000字的文章，要求通俗易懂"
                
                # 大模型决策（网页9的架构流程）
                llm_decision = await analyze_input_with_llm(user_input, tools_info)
                
                print(f"大模型决策：{llm_decision}")

                if "error" in llm_decision:
                    print(f"决策错误：{llm_decision['error']}")
                    return
                
                # 执行工具调用（网页8的调用逻辑）

                results = []

                llm_decision = await analyze_output(llm_decision)

                for decision in llm_decision:
                    result = await session.call_tool(
                        decision["tool"],
                        decision["params"]
                    )

                    print(f"调用结果：{result}")
                    results.append(result)

                
                # 结果处理
                print(f"执行结果：{results}")
                # if result.error:
                #     print(f"执行错误：{result.error.message}")
                # else:
                #     print(f"\n执行结果：{result.content}")

    except Exception as e:
        print(f"连接异常：{str(e)}")

from json import JSONDecodeError

async def analyze_output(result):
    ...
    try:
        # 确保返回结果是合法 JSON
        parsed = json.loads(result.strip("`").replace("json\n", ""))
        if not isinstance(parsed, list):
            raise ValueError("响应必须是 JSON 数组")
        return parsed
    except (JSONDecodeError, ValueError) as e:
        return {"error": f"大模型返回格式错误：{str(e)}"}


if __name__ == "__main__":
    asyncio.run(main())
