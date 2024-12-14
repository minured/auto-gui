import time
from abilities.notification import Notification
from abilities.operation import Operation


class BuyDiamonds(Operation, Notification):

    def run(self):
        # self.find_and_activate_window_by_title("Chrome")
        self.find_and_activate_window_by_title("QQ飞车")

        # self.clickImage("./pic/shop.png", "商城")
        # self.clickImage("./pic/shopSearch.png", "搜索商品")
        # self.input("效率")

        buyCount = 0

        while buyCount < 3:
            self.clickImage("./pic/buy-confirm.png", "确认购买")
            self.clickImage("./pic/buy-continue.png", "继续购买")

            buyCount = buyCount + 1

        # self.match_test("./pic/shop.png")

        self.log("任务完成，发送通知邮件")
        self.notify("任务完成")

        # self.logScreenMetrics()
        # self.positionMode()
