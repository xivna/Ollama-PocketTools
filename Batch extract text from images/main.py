# 使用本地ollamaAI批量提取图中文字
# 20250819
import base64
import requests
import time
import sys
from openai import OpenAI

class ASKAI:
    def __init__(self, 
                prompt="提取图中文字",
                model_name='qwen2.5vl:7b',
                url='http://localhost:11435/api/chat'):
        
        self.prompt = prompt
        self.model_name = model_name
        self.headers = {"Content-Type": "application/json"}
        self.url = url

    def request_api(self,image):
        # 将图片编码为base64字符串
        try:
            with open(image, "rb") as image_file:
                self.encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"读取图像文件失败，程序退出: {e}")
            sys.exit(1)
        
        payload = {
            "model": self.model_name,
            "messages": [{
                    "role": "user",
                    "content": self.prompt,  # 用户问题/提示
                    "images": [self.encoded_image]  # 传入Base64编码的图片（列表形式，支持多图） # {"url": f"data:image/{"PNG".lower()};base64,{self.encoded_image}"}
                }],
            "stream": False  # 关闭流式传输，一次性返回完整结果
        }

        try:
                # 发送请求并获取完整响应
                response = requests.post(self.url, json=payload, headers=self.headers)
                response.raise_for_status()  # 检查请求是否成功
                
                # 解析响应（非流式响应直接返回完整JSON）
                result = response.json()
                return result
        except Exception as e:
                return f"请求失败：{str(e)}"

    def saveResult(self, data, file_url):
         with open(file_url, 'a+', encoding='UTF-8') as f:
              f.write(data)

# 20250819 由`qwen3:30b-a3b-instruct-2507-q4_K_M`所作
def print_progress_bar_pro(iteration, total, prefix="进度", suffix="", length=50, decimals=1, start_time = time.time(),):
    """
    打印带时间统计的百分比进度条。
    
    参数：
    - iteration: 当前迭代次数（从 0 开始）
    - total: 总迭代次数
    - prefix: 前缀文字（如“进度”）
    - suffix: 后缀文字（如“完成”）
    - length: 进度条长度（单位：字符）
    - decimals: 时间显示的小数位数
    """
    # 计算进度
    progress = iteration / total
    filled_length = int(length * progress)
    bar = '|' * filled_length + ' ' * (length - filled_length)  # 使用方块字符`█`更美观，也可以用`|`

    # 计算已用时间
    elapsed_time = time.time() - start_time
    elapsed_str = f"{elapsed_time:.{decimals}f}s"

    # 计算剩余时间（如果还没完成）
    if iteration > 0:
        avg_time_per_iteration = elapsed_time / iteration
        remaining_time = avg_time_per_iteration * (total - iteration)
        remaining_str = f"{remaining_time:.{decimals}f}s"
    else:
        remaining_str = "未知"

    # 计算处理速度（每秒多少次）
    if iteration > 0:
        speed = iteration / elapsed_time
        speed_str = f"{speed:.{decimals}f}/s"
    else:
        speed_str = "0.0/s"

    # 构建完整输出
    print(
        f'\r{prefix} [{bar}] {int(progress * 100)}% | 用时: {elapsed_str} | 剩余: {remaining_str} | 速度: {speed_str} {suffix}',
        end='', flush=True
    )

    # 如果完成，换行
    if iteration == total:
        print()  # 换行结束

if __name__ == "__main__":
    tokens_count = [[], []]
    Cai = ASKAI(
        prompt="提取图中聊天记录，包括发言人和发言内容",
        model_name='qwen2.5vl:7b',
        url='http://localhost:11434/api/chat'
    )

    for i in range(40):
        # 这里依次获取图片url
        image = "D:\\Download\\Camera\\meet\\" + "mpv-shot00" + str(i+1).zfill(2) + ".jpg"
        data = Cai.request_api(image)
        # print(data)

        content = data['message']['content']
        prompt_tokens = data['prompt_eval_count']
        completion_tokens = data['eval_count']
        Cai.saveResult(content, file_url = r'D:\result.txt') # 保存提取文本到文本文件

        tokens_count[0].append(prompt_tokens)
        tokens_count[1].append(completion_tokens)
        print_progress_bar_pro(i+1, 40)

    print(f"prompt_tokens_count: {tokens_count[0]}")
    print(f"completion_tokens_count: {tokens_count[1]}")
    print(f"prompt_tokens_count: {sum(tokens_count[0])}")
    print(f"completion_tokens_count: {sum(tokens_count[1])}")
