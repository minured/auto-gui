from abilities.notification import Notification
from abilities.operation import Operation


class ViewNewPost(Operation, Notification):

    def run(self):
        self.find_and_activate_window_by_title("Google Chrome")
        xy = self.get_xy("./pic/buy-confirm.png")
        self.moveTo(xy)
        self.click(xy)

        self.log("任务完成，发送通知邮件")
        self.notify("任务完成")
