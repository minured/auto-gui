import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import time
import threading


# 在 Tkinter 中，当你调用 mainloop() 方法时，
# 它会启动事件循环并开始处理 GUI 事件。
# 这是一个阻塞调用，意味着它会阻止后续的代码执行，直到你关闭窗口或者结束事件循环


class TransparentLoggerWindow:
    def __init__(self, title="Logger", width=300, height=200, transparency=0.8):
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title(title)

        # 设置窗口大小
        self.root.geometry(f"{width}x{height}")

        # 去掉标题栏（无边框）
        # self.root.overrideredirect(True)

        # 设置窗口置顶和透明度
        self.root.attributes("-topmost", True)  # 保持置顶
        self.root.attributes("-alpha", transparency)  # 设置透明度 (0-1之间)
        self.root.config(bg='black')  # 设置完全透明

        # 只在windows生效
        # self.root.attributes("-transparentcolor", "black")  # 设置透明度 (0-1之间)

        # 禁止调整窗口大小
        self.root.resizable(False, False)

        # 创建不可编辑的文本框（没有滚动条）
        self.log_area = tk.Text(
            self.root, wrap=tk.WORD, state=tk.DISABLED, fg='white', font=('Arial', 12))
        self.log_area.pack(expand=True, fill=tk.BOTH)

    def log(self, message):
        """
        输出日志到窗口
        :param message: 日志内容
        """
        print('[logger]:', message)
        self.log_area.config(state=tk.NORMAL)  # 解锁文本框，用于写入
        self.log_area.insert(tk.END, message + "\n")  # 插入日志
        self.log_area.see(tk.END)  # 滚动到最后一行
        self.log_area.config(state=tk.DISABLED)  # 禁用文本框，防止用户编辑

    def start(self):
        """
        启动Tkinter主循环
        """
        self.root.mainloop()

# 导出一个方法，用于创建并启动半透明悬浮窗
def create_transparent_logger(title="Logger", transparency=0.8):
    logger_window = TransparentLoggerWindow(
        title=title, transparency=transparency)
    return logger_window


def log_messages(logger):
    # 模拟日志输出
    for i in range(30):
        logger.log(f"日志信息 {i + 1}: 这是一个示例日志。")
        time.sleep(0.1)  # 模拟延迟

logger = create_transparent_logger(title="日志窗口", transparency=0.8)

# # 使用示例
# if __name__ == "__main__":
#     # 创建一个日志窗口实例
#     logger = create_transparent_logger(title="日志窗口", transparency=0.8)

#     # 使用线程来模拟日志输出
#     thread = threading.Thread(target=log_messages, args=(logger,))
#     thread.start()

#     # 启动窗口
#     logger.start()
