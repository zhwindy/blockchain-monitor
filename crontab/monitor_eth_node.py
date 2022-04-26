# encoding=utf-8
import requests
import pytz
from datetime import datetime

node_list = {
    "eth-node-01": "http://172.31.23.144:40000",
    # "eth-node-02": "http://172.31.31.186:40000",
    "eth-node-02": "http://172.31.25.134:40000",
}

def send_news(content):
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
    url = "https://oapi.dingtalk.com/robot/send?access_token=601e6864aa1dcd0e07e1fb61227b114a32ebfc9c2c335689b9a6b473397b0bd3"
    requests.post(url=url, json=message)


def get_newest_block(url):
    param = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": ["latest", False],
        "id": 1
    }
    try:
        res = requests.post(url, json=param, timeout=30)
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


def main():
    for key, url in node_list.items():
        try:
            node_data = get_newest_block(url)
            block_height = get_block_height(node_data)
            block_time = get_block_time(node_data)
            content = f"monitor节点: {key}\n最新高度: {block_height}\n出块时间: {block_time}"""
        except Exception as e:
            content = str(e)
        print(content)
        send_news(content)


if __name__ == '__main__':
    main()
