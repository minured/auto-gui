import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils import load_yaml, merge_configs


# SMTP 服务器配置 (以 Gmail 为例)
config = {}


def send_email(message: str, subject='Notification'):

    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = config['sender_email']
    msg['To'] = config['receiver_email']
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    # 发送邮件
    try:
        # 连接到 SMTP 服务器
        print('connecting smtp server')
        server = smtplib.SMTP(config['smtp_server'], config["smtp_port"])
        server.starttls()  # 启用 TLS 加密

        # 登录 SMTP 服务器
        server.login(config['sender_email'], config['sender_password'])

        # 发送邮件
        text = msg.as_string()
        server.sendmail(config['sender_email'], config['receiver_email'], text)
        print("邮件发送成功！")

    except Exception as e:
        print(f"邮件发送失败：{e}")

    finally:
        # 关闭服务器连接
        server.quit()


def init():
    global config

    file1_path = 'config.local.yaml'
    file2_path = 'config.yaml'

    config1 = load_yaml(file1_path) or {}
    config2 = load_yaml(file2_path) or {}

    config = (merge_configs(config1, config2))['mail']


def notify(message: str, subject: str):
    send_email(message, subject)


init()
