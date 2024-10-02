import tkinter as tk
import time
import threading

class LogWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("日志浮窗")
        self.text_area = tk.Text(root, height=10, width=50)
        self.text_area.pack()
        self.root.geometry("300x200")  # 设置窗口大小

    def append_log(self, message):
        self.text_area.insert(tk.END, message + "\n")  # 添加日志信息
        self.text_area.see(tk.END)  # 滚动到最后一行

def log_messages(log_window):
    # 模拟日志输出
    for i in range(10):
        log_window.append_log(f"日志信息 {i + 1}: 这是一个示例日志。")
        time.sleep(1)  # 模拟延迟

if __name__ == "__main__":
    root = tk.Tk()
    log_window = LogWindow(root)

    # 使用线程来模拟日志输出
    thread = threading.Thread(target=log_messages, args=(log_window,))
    thread.start()

    root.mainloop()
