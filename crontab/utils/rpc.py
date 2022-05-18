# encoding=utf-8
import requests
from datetime import datetime
import pytz

DingDing = "https://oapi.dingtalk.com/robot/send?access_token={token}"


def send_news(content, token="601e6864aa1dcd0e07e1fb61227b114a32ebfc9c2c335689b9a6b473397b0bd3"):
    """
    发送通知
    """
    message = {
        "at": {
            "isAtAll": False
        },
        "text": {
            "content": content
        },
        "msgtype": "text"
    }
    url = DingDing.format(token=token)
    requests.post(url=url, json=message)


def get_newest_block(url):
    param = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": ["latest", False],
        "id": 1
    }
    try:
        res = requests.post(url, json=param, timeout=10)
        result = res.json()
        data = result.get("result", {})
    except Exception as e:
        data = {}
    return data


def get_block_height(data):
    block_height = data.get("number", 1)
    height = int(block_height, base=16)
    return height


def get_block_time(data):
    time = data.get("timestamp", "1000000000")
    timestamp = int(time, base=16)
    date_time = datetime.fromtimestamp(timestamp, pytz.timezone('Asia/Shanghai'))
    time = date_time.strftime("%Y-%m-%d %H:%M:%S")
    return time
