import time
import pyautogui
import cv2
import psutil
import os

from abilities.interface import BaseWorker

original_width, original_height = 1440, 900  # 屏幕分辨率


class Operation(BaseWorker):
    def get_xy(self, img_model_path):
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
        result = cv2.matchTemplate(
            snapshot, img_terminal, cv2.TM_SQDIFF_NORMED)

        # 解析出匹配区域的左上角图标
        left_top_angle = cv2.minMaxLoc(result)[2]
        # 计算出匹配区域右下角图标（左上角坐标加上模板的长宽即可得到）
        bottom_right_angle = (
            left_top_angle[0] + width, left_top_angle[1] + height)

        # 画框
        cv2.rectangle(snapshot, (left_top_angle[0], left_top_angle[1]),
                      (bottom_right_angle[0], bottom_right_angle[1]), (0, 255, 0), 2)

        # 计算坐标的平均值并将其返回
        coord = (int(((left_top_angle[0] + bottom_right_angle[0]) / 2) * x_scale),
                 int(((left_top_angle[1] + bottom_right_angle[1]) / 2) * y_scale))

        self.log('已找到坐标{}，{}'.format(coord, img_model_path))
        return coord

    def switch_to_window(self, app_name):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if app_name.lower() in proc.info['name'].lower():
                    # macOS
                    os.system(
                        f"osascript -e 'tell application \"{app_name}\" to activate'")
                    # Windows
                    # os.startfile(proc.info['name'])  # 另一种方式打开应用
                    time.sleep(1)
                    self.log('切换到窗口 [{}]'.format(
                        proc.info['name']))
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                self.log('未找到窗口 [{}]'.format(app_name))
                pass

    def click(self, coord):
        self.log('左击 {}'.format(coord))
        pyautogui.click(coord[0], coord[1], button='left')

    def moveTo(self, coord):
        self.log('移动到 {}'.format(coord))
        pyautogui.moveTo(coord[0], coord[1], duration=2)

    def match_test(img_model_path):
        pyautogui.screenshot().save("./pic/screenshot.png")
        snapshot = cv2.imread("./pic/screenshot.png")
        img = cv2.imread(img_model_path)
        # 读取模板的高度宽度和通道数
        height, width = img.shape

        # 使用matchTemplate进行模板匹配（标准平方差匹配）
        result = cv2.matchTemplate(snapshot, img, cv2.TM_SQDIFF_NORMED)

        # 解析出匹配区域的左上角图标
        left_top_angle = cv2.minMaxLoc(result)[2]
        bottom_right_angle = (
            left_top_angle[0] + width, left_top_angle[1] + height)

        # 画框
        cv2.rectangle(snapshot, (left_top_angle[0], left_top_angle[1]),
                      (bottom_right_angle[0], bottom_right_angle[1]), (0, 255, 0), 2)

        # 展示画框图像
        cv2.imshow('Matched Image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
