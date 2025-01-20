from fastapi import FastAPI
from langchain_openai import ChatOpenAI  # 导入OpenAI聊天模型
from langserve import add_routes  # 用于添加API路由
from fastapi.middleware.cors import CORSMiddleware  # 处理跨域
from dotenv import load_dotenv  # 环境变量管理
import os

# 加载环境变量（确保你有.env文件包含 OPENAI_API_KEY=你的密钥）
load_dotenv()

# 创建FastAPI应用
app = FastAPI(
    title="简单的LangChain聊天服务器",
    version="1.0",
    description="一个基础的LangChain聊天API"
)

# 配置CORS（允许前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境建议设置具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建LLM实例
# llm = ChatOpenAI(
#     model="gpt-4o-mini",  # 使用更经济的模型
#     temperature=0.7,  # 控制回答的创造性，0更保守，1更创造性
# )

llm = ChatOpenAI(
    model="deepseek-chat",  # 替换为您想使用的模型名称
    temperature=0.7,
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),  # 使用DeepSeed API密钥
    openai_api_base="https://api.deepseek.com/v1",  # 新的 API 基础地址
)

# 添加基础聊天路由
# 这会自动创建以下端点：
# POST /chat/invoke - 单次对话
# POST /chat/stream - 流式对话（一个字一个字返回）
add_routes(
    app,
    llm,
    path="/chat",  # API路径
)

# 启动服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9012)
