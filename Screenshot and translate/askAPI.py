import base64
import requests
import json
import tempfile
import sys
from openai import OpenAI

class ASKAI:
    def __init__(self, image):
        # tempfile.gettempdir()获取临时目录的路径
        self.image_path = tempfile.gettempdir() + "\\temp.png"
        # 将图片编码为base64字符串
        try:
            image.save(self.image_path)
            with open(self.image_path, "rb") as image_file:
                self.encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"截图失败，程序退出: {e}")
            sys.exit(1)

    def request_api(self,
                    prompt="提取图中文本并输出，接着输出一行`---`，然后换行，再输出翻译后的文字（重要）。不要做多余的解释。如果图中存在多处文字，翻译时请注意上下文关联。",
                    model_name='qwen2.5vl:7b',
                    url='http://localhost:11435/api/chat'
                    ):
        payload = {
            "model": model_name,
            "messages": [{
                    "role": "user",
                    "content": prompt,  # 用户问题/提示
                    "images": [self.encoded_image]  # 传入Base64编码的图片（列表形式，支持多图） # {"url": f"data:image/{"PNG".lower()};base64,{self.encoded_image}"}
                }],
            "stream": False  # 关闭流式传输，一次性返回完整结果
        }
        headers = {"Content-Type": "application/json"}

        try:
                # 3. 发送请求并获取完整响应
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()  # 检查请求是否成功
                
                # 4. 解析响应（非流式响应直接返回完整JSON）
                result = response.json()
                return result
            
        except Exception as e:
                return f"请求失败：{str(e)}"
