## 本文件夹存放 从零开始学习 mcp server 的过程
** mcp是用来规范agent 开发的协议 **
## 1. 下载mcp server

** pip install "mcp[cli]" httpx **

## 2. 配置mcp server

** 在cline插件中的配置如下：
{
  "mcpServers": {
    "myserver": {
      "command": "/Users/zhangtian/miniforge3/envs/langchain/bin/python",
      "args": [
        "/Users/zhangtian/work/langchain_learn/mcp学习/base_mcp_tool_study.py"
      ],
      "disabled": false,
      "autoApprove": [
        "multiplay"
      ]
    },
    "myserver2": {
      "command": "/Users/zhangtian/miniforge3/envs/langchain/bin/python",
      "args": [
        "/Users/zhangtian/work/langchain_learn/mcp学习/base_mcp_tool_study2.py"
      ],
      "disabled": false,
      "autoApprove": [
        "multiplay"
      ],
      "description": "演示服务器（含文件查询和计算）"
    },
    "fastapi_mcptool": {
      "command": "/Users/zhangtian/miniforge3/envs/langchain/bin/mcp-proxy",
      "args": [
        "http://127.0.0.1:8080/mcp"
      ],
      "description": "获取当前服务器时间"
    }
  }
}

参数描述：
- command: mcp server的启动命令，上述示例中填写的是指定虚拟环境下的 python 解释器，你也可以使用 uv
- args: mcp server的启动参数 ，上述示例中填写的是 自定义编写的 mcp server 文件的绝对路径
- disabled: 是否禁用该mcp server
- autoApprove: 自动批准的命令列表
- description: mcp server的描述
- myserver、myserver2、fastapi_mcptool:自定义的 mcp server的名称，与文件名字无关，在调用时需要使用该名称

- 其中 fastapi_mcptool 服务器是 将 mcp server 挂载在 fastapi项目上， 是使用 mcp-proxy 启动的，mcp-proxy 是一个用于将 FastAPI 应用程序转换为 mcp server 的工具，可以方便地将 FastAPI 应用程序部署为 mcp server。  
需要 pip install fastapi_mcp mcp-proxy
 **

## 3. 启动mcp server

## 4. 使用mcp server

## 5. 使用mcp server的python客户端

## 6. 使用mcp server的python客户端调用ollama模型