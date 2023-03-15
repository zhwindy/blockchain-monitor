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
    '''
    if not MAIL_USER:
        print("email send failed")
        return
    msg = MIMEText(message, 'plain', _charset="utf-8")
    # 邮件主题描述
    msg["Subject"] = subject
    # 发件人显示
    msg["from"] = 'notice@nftscan.com'
    # 收件人显示
    msg["to"] = to_addrs
    with SMTP_SSL(host="smtp.qiye.aliyun.com", port=465) as smtp:
        smtp.login(user=MAIL_USER, password=MAIL_PASSWD)
        smtp.sendmail(from_addr=MAIL_USER, to_addrs=to_addrs.split(','), msg=msg.as_string())


def send_email_alert(chain, block, delay):
    subject = f"【延迟告警】【{chain}】【延迟{delay}分钟】"
    message = f"【数据解析延迟】主链: {chain} \n已解析区块高度: {block} \n当前延迟约: {delay}分钟"
    to_addrs = "842076364@qq.com, 919009082@qq.com, pengfei@nftscan.com, even366@qq.com, 841048524@qq.com, lewis@nftscan.com, 2532986201@qq.com"
    sendMail(message, subject, to_addrs)
    print("email send success")


if __name__ == "__main__":
    send_email_alert("BTC", 770082, 5)
