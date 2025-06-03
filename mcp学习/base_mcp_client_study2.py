import os
from typing import Any
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from langchain_community.llms.sparkllm import SparkLLM
import asyncio
from mcp import ClientSession, StdioServerParameters
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_react_agent, AgentExecutor, StructuredChatAgent
from langchain.prompts import PromptTemplate


from dotenv import load_dotenv
load_dotenv()

# MCP服务端配置
MCP_SERVER_SCRIPT = "/Users/zhangtian/work/langchain_learn/mcp学习/base_mcp_tool_study2.py"
PYTHON_PATH = "/Users/zhangtian/miniforge3/envs/langchain/bin/python"

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


#运行报错，需要修改
async def run_agent():
    
    # 连接MCP服务器
    server_params = StdioServerParameters(
        command=PYTHON_PATH,
        args=[MCP_SERVER_SCRIPT],  # 确保路径正确
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # 加载MCP工具
            tools = await load_mcp_tools(session)
            
            # 创建Agent
            agent = StructuredChatAgent.from_llm_and_tools(llm=model, tools=tools, prompt=prompt)
            

            # 添加记忆模块
            from langchain.memory import ConversationBufferMemory

            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

            # 包装执行器
            agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                memory=memory,
                handle_parsing_errors=True,
                max_iterations=5,
                verbose=True  # 显示详细执行过程
)

            # 执行查询
            response = await agent_executor.arun({
                "input": "请列出 /Users/zhangtian/work/langchain_learn 文件夹的文件，并计算 (15**2 - 3)/4 的值"
            })
            return response

if __name__ == "__main__":
    result = asyncio.run(run_agent())
    print("最终结果：", result)
