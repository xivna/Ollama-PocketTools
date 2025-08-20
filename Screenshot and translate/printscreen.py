import tkinter as tk
from PIL import Image
from mss import mss
from pyautogui import position

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-alpha', 0.3)       # 设置窗口半透明；这里的 -alpha 参数调整窗口的透明度，取值范围从0.0（完全透明）到1.0（完全不透明）
        self.root.attributes('-fullscreen', True) # 全屏显示；将 -fullscreen 设置为 True 可以让窗口扩展至覆盖整个屏幕，去除边框和标题栏。
        # self.root.config(cursor="cross")          # 设置整个窗口光标为十字准星
        self.root.bind("<ButtonPress-1>", self.start)     # 鼠标左键<ButtonPress-1>按下事件
        self.root.bind("<B1-Motion>", self.draw)     # 鼠标拖动事件
        self.root.bind("<ButtonRelease-1>", self.release) # 鼠标释放事件
        # 绑定退出事件
        self.root.bind("<Button-3>", self.exit_app)  # 右键
        self.root.bind("<Escape>", self.exit_app)    # Esc键
        
        # 创建了一个Canvas小部件，它是Tkinter中的一个绘图区域，可用于绘制图形、文本、线条等。这里的 bg='white' 设置背景颜色为白色，而 highlightthickness=0 去除了Canvas的小部件边框，使得Canvas看起来更整洁。
        self.canvas = tk.Canvas(self.root, bg='white', cursor="cross", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.image = None  # 存储截图结果

    def start(self, event):
        """记录起始坐标并开始绘制选择框 左键按下"""
        self.start_x, self.start_y = position()
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, # 矩形起点
            event.x, event.y, # 矩形终点
            outline='red', width=2
        )

    def draw(self, event):
        """实时更新选择框"""
        if not self.start_x or not self.start_y:
            return
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def release(self, event):
        """完成截图并关闭窗口 左键释放"""
        # 计算选择区域的坐标。转换为屏幕绝对坐标
        x1, y1 = self.start_x, self.start_y
        x2, y2 = position()
        
        # 使用 self.root.withdraw() 方法临时隐藏Tkinter主窗口，以确保截图不会包含用于选择区域的选择框。
        self.root.withdraw()
        
        # 使用mss进行区域截图
        with mss() as sct:
            monitor = {
                "top": min(y1, y2), # 起始纵坐标
                "left": min(x1, x2), # 起始横坐标
                "width": abs(x1 - x2), # 截图宽度
                "height": abs(y1 - y2) # 截图高度
            }
            # 使用 grab 方法根据给定的 monitor 参数进行屏幕截图
            sct_img = sct.grab(monitor)
            # 将 mss 捕捉到的 BGRA 格式的图像数据转换为 PIL 图像对象
            self.image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        # 在完成截图后，使用 self.root.destroy() 彻底关闭Tkinter窗口。
        self.root.destroy()
    
    # 退出截图
    def exit_app(self, event):
        """退出截图程序"""
        self.root.destroy()

def capture_screenshot():
    """启动截图功能并返回结果"""
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()
    return app.image

if __name__ == "__main__":
    # 截图并获取图像对象
    image = capture_screenshot()
    image.save(r"D:\temp.png")
