import time
from abilities.notification import Notification
from abilities.operation import Operation


class BuyDiamonds(Operation, Notification):

    def run(self):
        # self.find_and_activate_window_by_title("Chrome")
        # self.clickImage("./pic/shop.png", "商城")
        # self.clickImage("./pic/shopSearch.png", "搜索商品")
        # self.input("效率")
        # self.match_test("./pic/shop.png")
        # self.logScreenMetrics()
        # self.positionMode()

        # 买宝石
        # self.find_and_activate_window_by_title("QQ飞车")
        # buyCount = 0

        # while buyCount <= 120:
        #     self.clickImage("./pic/buy-confirm.png", "确认购买")
        #     self.clickImage("./pic/buy-continue.png", "继续购买")
        #     buyCount = buyCount + 1

        # 合宝石
        self.find_and_activate_window_by_title("QQ飞车")
        buyCount = 0

        while buyCount <= 100:
            self.clickImage("./pic/kaishihecheng.png", "开始合成")
            self.clickImage("./pic/jixuhecheng.png", "继续合成")
            buyCount = buyCount + 1

        self.log("任务完成，发送通知邮件")
        self.notify("任务完成")
