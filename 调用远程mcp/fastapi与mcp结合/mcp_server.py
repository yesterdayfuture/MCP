

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi_mcp import FastApiMCP
import uvicorn

app = FastAPI()


# 创建MCP实例
mcp = FastApiMCP(
    app,
    name="AI-Tool-Server",
    exclude_operations=["internal"]          # 排除内部接口
)

# 注册工具1：天气查询
@app.get("/weather/{city}", operation_id="get_weather")
async def get_weather(city: str):
    """根据城市名查询实时天气"""
    # 实际业务逻辑（模拟数据）
    return {"city": city, "temperature": 25, "condition": "晴"}

# 注册工具2：数学计算
@app.post("/calculate", operation_id="calculate")
async def calculate(a: float, b: float, operator: str):
    """执行基础数学运算"""
    if operator == "add":
        return {"result": a + b}
    elif operator == "multiply":
        return {"result": a * b}
    else:
        raise HTTPException(400, "Unsupported operator")


# 注册工具3：内部接口（不暴露给外部）
@app.get("/internal", operation_id="internal")
async def internal():
    """内部接口"""
    return {"message": "This is an internal API"}

# 动态热更新工具（新增接口时调用）
mcp.setup_server()
mcp.mount(mount_path='/haha')


#所有 API 路由将自动以 MCP 工具形式暴露，默认访问路径为 /mcp

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

