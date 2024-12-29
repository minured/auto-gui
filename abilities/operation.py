import random
import time
import pyautogui
import cv2
import psutil
import os
from pywinauto import application, Desktop
from abilities.interface import BaseWorker
import win32gui  # type: ignore
import win32api
import win32con
from pynput.mouse import Button, Controller
import pydirectinput

# original_width, original_height = 1440, 900  # 屏幕分辨率
original_width, original_height = 3840, 2160  # 屏幕分辨率


class Operation(BaseWorker):
    def get_xy(self, img_model_path, name):
        """
        用来判定游戏画面的点击坐标
        :param img_model_path:用来检测的图片
        :return:以元组形式返回检测到的区域中心的坐标
        """
        # 将图片截图并且保存
        pyautogui.screenshot().save("./pic/screenshot.png")
        # 待读取图像
        snapshot = cv2.imread("./pic/screenshot.png")
        # 图像模板
        img_terminal = cv2.imread(img_model_path)
        # 读取模板的高度宽度和通道数
        height, width, channel = img_terminal.shape
        h, w, channel2 = snapshot.shape

        # 计算缩放因子
        x_scale = original_width / w
        y_scale = original_height / h

        # 使用matchTemplate进行模板匹配（标准平方差匹配）
        result = cv2.matchTemplate(snapshot, img_terminal, cv2.TM_SQDIFF_NORMED)

        # 解析出匹配区域的左上角图标
        left_top_angle = cv2.minMaxLoc(result)[2]
        # 计算出匹配区域右下角图标（左上角坐标加上模板的长宽即可得到）
        bottom_right_angle = (left_top_angle[0] + width, left_top_angle[1] + height)

        # 画框
        cv2.rectangle(
            snapshot,
            (left_top_angle[0], left_top_angle[1]),
            (bottom_right_angle[0], bottom_right_angle[1]),
            (0, 255, 0),
            2,
        )

        # 计算坐标的平均值并将其返回
        coord = (
            int(((left_top_angle[0] + bottom_right_angle[0]) / 2) * x_scale),
            int(((left_top_angle[1] + bottom_right_angle[1]) / 2) * y_scale),
        )

        self.log("已找到坐标{}，{}".format(coord, name or img_model_path))
        return coord

    def switch_to_window(self, app_name):
        print("switch window", app_name)
        for proc in psutil.process_iter(["pid", "name"]):
            print("proc", proc)
            try:
                if app_name.lower() in proc.info["name"].lower():
                    # macOS
                    # os.system(
                    #     f"osascript -e 'tell application \"{app_name}\" to activate'"
                    # )
                    # Windows
                    os.startfile(proc.info["name"])  # 另一种方式打开应用
                    time.sleep(1)
                    self.log("切换到窗口 [{}]".format(proc.info["name"]))
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                self.log("未找到窗口 [{}]".format(app_name))
                pass

    def find_and_activate_window_by_title(self, title_substring):
        self.log("匹配窗口 {}".format(title_substring))

        def callback(hwnd, extra):
            window_text = win32gui.GetWindowText(hwnd)
            if title_substring.lower() in window_text.lower():
                win32gui.SetForegroundWindow(hwnd)
                self.log("切换至 {}".format(title_substring))
                self.interfaceDelay(1, 1.2)
                return False  # 找到后停止枚举
            return True

        win32gui.EnumWindows(callback, 0)
        return True  # 如果找到并激活，则返回True

    def click(self, coord):
        self.log("左击 {}".format(coord))
        x, y = coord
        pyautogui.moveTo(
            x, y, duration=random.uniform(0.1, 0.3), tween=pyautogui.easeInOutQuad
        )
        pyautogui.click(button="left")

    def moveTo(self, coord):
        self.log("移动到 {}".format(coord))
        pyautogui.moveTo(coord[0], coord[1], duration=1)

    def easeInOutQuad(self, t):
        return t * t if t < 0.5 else -1 + (2 - t) * (2 - t)

    def moveToWithRandomness(self, xy, duration=1.0):
        x, y = xy
        for t in range(int(duration * 100)):
            fraction = t / (duration * 100)
            x_pos = (
                self.easeInOutQuad(fraction) * (x - pyautogui.position().x)
                + pyautogui.position().x
            )
            y_pos = (
                self.easeInOutQuad(fraction) * (y - pyautogui.position().y)
                + pyautogui.position().y
            )
            pyautogui.moveTo(x_pos, y_pos)
            time.sleep(0.01 + random.uniform(-0.005, 0.005))  # 添加随机延迟

    def match_test(self, img_model_path):
        pyautogui.screenshot().save("./pic/screenshot.png")
        snapshot = cv2.imread("./pic/screenshot.png")
        img = cv2.imread(img_model_path)
        # 读取模板的高度宽度和通道数
        height, width, alpha = img.shape
        print("模板宽高", height, width)

        # 使用matchTemplate进行模板匹配（标准平方差匹配）
        result = cv2.matchTemplate(snapshot, img, cv2.TM_SQDIFF_NORMED)

        # 解析出匹配区域的左上角图标
        left_top_angle = cv2.minMaxLoc(result)[2]
        bottom_right_angle = (left_top_angle[0] + width, left_top_angle[1] + height)

        print("match", left_top_angle, bottom_right_angle)

        # 画框
        cv2.rectangle(
            snapshot,
            (left_top_angle[0], left_top_angle[1]),
            (bottom_right_angle[0], bottom_right_angle[1]),
            (0, 255, 0),
            2,
        )

        # 展示画框图像
        cv2.imshow("Matched Image", snapshot)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def logMousePosition(self):
        self.log("鼠标坐标 {}".format(pyautogui.position()))

    def positionMode(self):
        self.logMousePosition()
        a = 1
        while a < 99999:
            self.logMousePosition()
            time.sleep(0.1)
            a = a + 1

    def left_click(self, xy):
        # 将鼠标移动到指定位置
        win32api.SetCursorPos(xy)
        time.sleep(1)

        # 模拟鼠标左键按下
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.2)
        # 模拟鼠标左键抬起
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def logScreenMetrics(self):
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)
        print(f"屏幕分辨率: {screen_width}x{screen_height}")

    # error method
    def get_active_window_resolution(self):
        # 获取当前激活窗口的句柄
        hwnd = win32gui.GetForegroundWindow()

        # 获取窗口的设备上下文
        hdc = win32gui.GetWindowDC(hwnd)

        # 获取窗口的宽度和高度
        width = win32api.GetSystemMetrics(win32api.SM_CXSIZE)
        height = win32api.GetSystemMetrics(win32api.SM_CYSIZE)

        # 释放设备上下文
        win32gui.ReleaseDC(hwnd, hdc)

        print(f"当前激活窗口的分辨率为: {width}x{height}")

        return width, height

    # pynput
    def left_click2(self, xy):
        mouse = Controller()
        mouse.position = xy
        mouse.click(Button.left)

    def interfaceDelay(self, min=0.2, max=0.5):

        delay = random.uniform(min, max)
        self.log("wait {}s".format(delay))
        time.sleep(delay)

    # pydirectinput
    def left_click3(self, xy):
        pydirectinput.moveTo(xy[0], xy[1])  # 将鼠标移动到指定位置
        pydirectinput.click(xy[0], xy[1])  # 模拟鼠标左键点击

    def clickImage(self, img, name):
        xy = self.get_xy(img, name)
        self.click(xy)
        self.interfaceDelay(0.08, 0.2)

    def input(self, text):
        pyautogui.typewrite(text)
