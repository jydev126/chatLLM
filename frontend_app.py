import gradio as gr
import requests

BACKEND_URL = "http://localhost:9012"


def chat_with_llm(message):
    """与LLM进行对话"""
    response = requests.post(
        f"{BACKEND_URL}/chat/invoke",
        json={"input": message}
    )
    # 从响应中提取实际的消息内容
    response_data = response.json()["output"]
    if isinstance(response_data, dict):
        return response_data.get("content", str(response_data))
    return str(response_data)


# 创建Gradio界面
with gr.Blocks() as demo:
    gr.Markdown("# LangChain Chat Demo")

    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="输入消息", placeholder="在这里输入您的问题...")
    clear = gr.Button("清除对话")

    def user(message, history):
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
