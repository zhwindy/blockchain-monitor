#encoding=utf-8
import os
from smtplib import SMTP_SSL
from email.mime.text import MIMEText

MAIL_USER = os.getenv('MAIL_USER', None)
MAIL_PASSWD = os.getenv('MAIL_PASSWD', None)

def sendMail(message, subject, to_addrs):
    '''
    :param message: str 邮件内容
    :param Subject: str 邮件主题描述
    :param sender_show: str 发件人显示，不起实际作用如："xxx"
    :param recipient_show: str 收件人显示，不起实际作用 多个收件人用','隔开如："xxx,xxxx"
    :param to_addrs: str 实际收件人
    :param cc_show: str 抄送人显示，不起实际作用，多个抄送人用','隔开如："xxx,xxxx"
    '''
    if not MAIL_USER:
        return
    # 邮件内容
    msg = MIMEText(message, 'plain', _charset="utf-8")
    # 邮件主题描述
    msg["Subject"] = subject
    # 发件人显示，不起实际作用
    msg["from"] = 'notice@nftscan.com'
    # 收件人显示，不起实际作用
    msg["to"] = 'notice@nftscan.com'
    with SMTP_SSL(host="smtp.qiye.aliyun.com", port=465) as smtp:
        # 登录发邮件服务器
        smtp.login(user=MAIL_USER, password=MAIL_PASSWD)
        # 实际发送、接收邮件配置
        smtp.sendmail(from_addr=MAIL_USER, to_addrs=to_addrs.split(','), msg=msg.as_string())


def send_email_alert(chain, block, delay):
    message = f"【数据解析延迟】主链: {chain} \n已解析高度: {block} \n当前延迟约: {delay}分钟"
    subject = f"【延迟告警】【{chain}】【延迟{delay}分钟】"
    to_addrs = "842076364@qq.com, 919009082@qq.com, pengfei@nftscan.com, even366@qq.com, 841048524@qq.com, lewis@nftscan.com, 2532986201@qq.com"
    sendMail(message, subject, to_addrs)


if __name__ == "__main__":
    # 收件人
    chain = "ETH"
    block = 123456
    delay = 12345
    send_email_alert(chain, block, delay)
