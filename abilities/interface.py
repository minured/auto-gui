import importlib
import os
import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QDesktopWidget, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QThread
import time
from PyQt5.QtGui import QTextCursor

from utils.common import snake_to_pascal_case


"""
基类，连接日志窗口，更新UI
操作类，基本点击移动，找图
任务类，规划任务流程（签到，活动任务等）
全部任务自动加载
"""


class BaseWorker(QThread):
    log_ = pyqtSignal(str)

    def __init__(self, ui_update_callback):
        super().__init__()
        self.ui_update_callback = ui_update_callback

    def log(self, message):
        self.log_.emit(message)


class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.create_ui()
        self.workers = self.load_workers()

    def create_ui(self):
        # 设置窗口标题和大小
        self.resize(300, 30)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # 创建中央小部件和布局
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 创建不可编辑的文本框
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)  # 设置为只读
        self.text_edit.setStyleSheet(
            # 设置背景透明和字体颜色
            "background-color: rgba(0, 0, 0, 150); color: white;")
        self.text_edit.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff)  # 去掉垂直滚动条
        layout.addWidget(self.text_edit)

        # 设置窗口的鼠标穿透
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 使窗口背景透明
        # self.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # 使鼠标事件穿透窗口
        self.setWindowFlags(self.windowFlags() |
                            Qt.FramelessWindowHint)  # 去掉标题栏
        self.setWindowOpacity(0.8)  # 设置窗口的整体透明度

    def start_tasks(self):
        for worker in self.workers:
            # 注意，这里调用的是threading的start, 不是类方法run
            worker.start()

    def load_workers(self):
        workers = []
        workers_dir = "tasks"

        # 遍历 workers 目录下的所有 .py 文件
        for file in os.listdir(workers_dir):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]
                module = importlib.import_module(
                    f"{workers_dir}.{module_name}")

                # 查找模块中的所有类，并确保它继承自 BaseWorker
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, BaseWorker) and attr is not BaseWorker and attr_name == snake_to_pascal_case(module_name):
                        # 实例化 Worker 类，并传入 UI 更新方法
                        worker = attr(self.log)
                        worker.log_.connect(self.log)
                        workers.append(worker)

        return workers

    def log(self, message):
        self.text_edit.append('-{}'.format(message))
        # 将光标移动到文本的末尾，确保滚动到底部
        self.text_edit.moveCursor(QTextCursor.End)

    def move_to_bottom_left(self):
        # 获取屏幕的尺寸
        screen_geometry = QDesktopWidget().availableGeometry()
        screen_height = screen_geometry.height()

        # 获取窗口的宽高
        window_height = self.frameGeometry().height()

        # 计算左下角的位置
        x = 0  # 左边
        y = screen_height - window_height  # 下边

        # 移动窗口到指定位置
        self.move(x, y)

    def keyPressEvent(self, event):
        # if event.key() == Qt.Key_F4 and event.modifiers() == Qt.ControlModifier:
        if event.key() == Qt.Key_F4:
            self.quit()

    def quit():
        sys.exit()

    def showEvent(self, event):
        self.move_to_bottom_left()
        self.start_tasks()
