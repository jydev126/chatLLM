import gradio as gr
import requests

BACKEND_URL = "http://localhost:9012"

def chat_with_llm(message):
    """与LLM进行对话"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",  # 修改为正确的端点
            json={"message": message}  # 修改为正确的请求格式
        )
        response.raise_for_status()  # 检查HTTP错误
        
        # 解析响应
        response_data = response.json()
        if "output" not in response_data:
            raise ValueError("Invalid response format")
            
        return response_data["output"]
        
    except requests.RequestException as e:
        return f"Error communicating with server: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

# 创建Gradio界面
with gr.Blocks() as demo:
    gr.Markdown("# LangChain Chat Demo")

    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="输入消息", placeholder="在这里输入您的问题...")
    clear = gr.Button("清除对话")

    def user(message, history):
        if not message.strip():  # 避免空消息
            return "", history
        return "", history + [[message, None]]

    def bot(history):
        if not history:
            return history
            
        response = chat_with_llm(history[-1][0])
        history[-1][1] = response
        return history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8090)
