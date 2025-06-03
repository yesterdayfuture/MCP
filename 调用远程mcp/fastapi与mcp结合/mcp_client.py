


import os
from openai import OpenAI

from mcp.client.sse import sse_client
from mcp import ClientSession

from langchain_community.llms.sparkllm import SparkLLM
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor, StructuredChatAgent
from langchain_mcp_adapters.tools import load_mcp_tools
import asyncio
from dotenv import load_dotenv
load_dotenv()



# 使用星火大模型
model = SparkLLM(
    model="SparkLLM/Max-32K",
    api_url="wss://spark-api.xf-yun.com/chat/max-32k",
    
    )

prompt_template = """
你必须生成严格符合以下JSON格式的响应：

{{
    "Thought": "思考内容",
    "Action": "{tool_names}中的一个工具名",
    "Action Input": {{
        "参数1": 参数值,
        "参数2": 参数值,
        ...
    }}
}}

可用工具描述：
{tools}

问题：
{input}

已执行步骤（JSON数组）：
{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(template=prompt_template)



async def main():
    # 1. 连接MCP服务端
    async with sse_client(url="http://localhost:8000/haha") as streams:
        async with ClientSession(streams[0], streams[1]) as session:
            await session.initialize()
            # 2. 获取可用工具列表
            tools = await session.list_tools()

            print("可用工具列表：", tools)

            tool_defs = [{
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            } for tool in tools.tools]

            # 加载MCP工具
            tools = await load_mcp_tools(session)

            print("可用工具列表(load_mcp_tools)：", tools)
            
            # # 创建Agent
            # agent = StructuredChatAgent.from_llm_and_tools(llm=model, tools=tools, prompt=prompt)
            

            # # 添加记忆模块
            # from langchain.memory import ConversationBufferMemory

            # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

            # # 包装执行器
            # agent_executor = AgentExecutor(
            #     agent=agent,
            #     tools=tools,
            #     memory=memory,
            #     handle_parsing_errors=True,
            #     max_iterations=5,
            #     verbose=True  # 显示详细执行过程
            # )

asyncio.run(main())












