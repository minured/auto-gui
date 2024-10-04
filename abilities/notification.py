import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from abilities.interface import BaseWorker
from utils.common import load_yaml, merge_configs


class Notification(BaseWorker):
    # SMTP 服务器配置 (以 Gmail 为例)

    def __init__(self, ui_update_callback):
        super().__init__(self)
        self.load_config()

    def send_email(self, message: str, subject='Notification'):

        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = self.config['sender_email']
        msg['To'] = self.config['receiver_email']
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        # 发送邮件
        try:
            # 连接到 SMTP 服务器
            self.log("连接邮件服务器...")
            server = smtplib.SMTP(
                self.config['smtp_server'], self.config["smtp_port"])
            server.starttls()  # 启用 TLS 加密

            # 登录 SMTP 服务器
            server.login(self.config['sender_email'],
                         self.config['sender_password'])

            # 发送邮件
            text = msg.as_string()
            server.sendmail(self.config['sender_email'],
                            self.config['receiver_email'], text)
            self.log("邮件发送成功！")

        except Exception as e:
            self.log(f"邮件发送失败：{e}")

        finally:
            # 关闭服务器连接
            server.quit()

    def load_config(self):
        file1_path = 'config.local.yaml'
        file2_path = 'config.yaml'

        config1 = load_yaml(file1_path) or {}
        config2 = load_yaml(file2_path) or {}

        self.config = (merge_configs(config1, config2))['mail']

    def notify(self, message: str, subject='Notification'):
        self.send_email(message, subject)
