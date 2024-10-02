import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt


class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("透明日志窗口")
        self.setGeometry(100, 100, 400, 300)

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

        # 添加文本框到布局
        layout.addWidget(self.text_edit)

        # 设置窗口的鼠标穿透
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 使窗口背景透明
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)  # 使鼠标事件穿透窗口
        self.setWindowFlags(self.windowFlags() |
                            Qt.FramelessWindowHint)  # 去掉标题栏
        self.setWindowOpacity(0.8)  # 设置窗口的整体透明度

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
    #         event.accept()

    # def mouseMoveEvent(self, event):
    #     if event.buttons() == Qt.LeftButton:
    #         self.move(event.globalPos() - self.drag_position)
    #         event.accept()

    def append_log(self, message):
        """追加日志信息"""
        self.text_edit.append(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    log_window = LogWindow()
    log_window.show()

    # 添加一些日志信息
    log_window.append_log("这是日志信息 1")
    log_window.append_log("这是日志信息 2")
    log_window.append_log("这是日志信息 3")

    sys.exit(app.exec_())
