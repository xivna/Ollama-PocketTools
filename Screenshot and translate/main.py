from askAPI import ASKAI
from printscreen import capture_screenshot

image = capture_screenshot()
data = ASKAI(image).request_api(
    prompt="翻译图中文字为中文。注意先输出原文本，之后换行输出`---`隔开下文，接着换行输出翻译后的文字。不要做多余的解释。如果图中存在多处文字，翻译时请注意上下文关联。",
    model_name='qwen2.5vl:7b',
    url='http://localhost:11434/api/chat'
)
content = data['message']['content']
prompt_tokens = data['prompt_eval_count']
completion_tokens = data['eval_count']

if __name__ == "__main__":
    print(f"{content}\n")
    print(f"prompt_tokens: {prompt_tokens}")
    print(f"completion_tokens: {completion_tokens}")
