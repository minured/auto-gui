import tkinter as tk

class TransparentLoggerWindow:
    def __init__(self, title="Logger", width=300, height=200, transparency=1.0):
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title(title)

        # 设置窗口大小
        self.root.geometry(f"{width}x{height}")

        # 去掉标题栏（无边框）
        self.root.overrideredirect(True)

        # 设置窗口置顶、透明度（全透明背景但文字可见）
        self.root.attributes("-topmost", True)  # 保持置顶
        self.root.attributes("-alpha", transparency)  # 设置透明度 (0-1之间)
        self.root.config(bg='systemTransparent')  # 设置完全透明

        # 禁止窗口接受鼠标和键盘事件
        # self.root.attributes("--transparent", "-transparent")  # 设置全透明
        # self.root.attributes("-disabled", True)  # 不响应鼠标和键盘事件

        # 创建不可编辑的文本框（没有滚动条）
        self.log_area = tk.Text(self.root, wrap=tk.WORD, state=tk.DISABLED, bg='black', fg='white', font=('Arial', 12))
        self.log_area.pack(expand=True, fill=tk.BOTH)

    def log(self, message):
        """
        输出日志到窗口
        :param message: 日志内容
        """
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
def create_transparent_logger(title="Logger", transparency=1.0):
    logger_window = TransparentLoggerWindow(title=title, transparency=transparency)
    return logger_window

# 使用示例
if __name__ == "__main__":
    # 创建一个日志窗口实例
    logger = create_transparent_logger(title="日志窗口", transparency=0.9)

    # 模拟日志输出
    logger.log("日志记录已启动...")
    logger.log("这是第一条日志。")
    logger.log("这是第二条日志。")
    logger.log
