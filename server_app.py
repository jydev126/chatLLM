from fastapi import FastAPI, HTTPException
from langchain_openai import ChatOpenAI  # 导入OpenAI聊天模型
from fastapi.middleware.cors import CORSMiddleware  # 处理跨域
from dotenv import load_dotenv  # 环境变量管理
import os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from pydantic import BaseModel

# 加载环境变量（确保你有.env文件包含 OPENAI_API_KEY=你的密钥）
load_dotenv()

class ChatInput(BaseModel):
    message: str

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

llm = ChatOpenAI(
    model="deepseek-chat",  
    temperature=0.7,
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),  # 使用DeepSeed API密钥
    openai_api_base="https://api.deepseek.com/v1",  # 新的 API 基础地址
)

# 创建记忆实例
memory = ConversationBufferMemory()

# 创建带记忆的对话链
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/chat")
async def chat_endpoint(chat_input: ChatInput):
    try:
        # Get response from conversation chain
        response = conversation.predict(input=chat_input.message)
        
        # Ensure response is properly formatted
        if not response:
            raise HTTPException(status_code=500, detail="No response generated")
            
        # Return structured response
        return {
            "status": "success",
            "output": response,
            "history": memory.chat_memory.messages
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing chat: {str(e)}"
        )

# 启动服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9012)
