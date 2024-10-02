from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class LogWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口无边框和透明
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 创建一个文本编辑框
        self.text_area = QtWidgets.QTextEdit(self)
        self.text_area.setReadOnly(True)  # 设置为只读
        self.text_area.setStyleSheet(
            "background:transparent; color:white; font-size: 12pt;")
        self.text_area.setText("这是一个透明背景的窗口，文字为黑色。")
        self.text_area.setGeometry(0, 0, 200, 300)

        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)  # 使鼠标事件穿透窗口

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def append_log(self, message):
        """追加日志信息"""
        self.text_area.append(message)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LogWindow()
    window.show()

    # 添加一些日志信息
    window.append_log("这是日志信息 1")
    window.append_log("这是日志信息 2")
    window.append_log("这是日志信息 3")

    sys.exit(app.exec_())
