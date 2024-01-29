# encoding=utf-8
import os
import time
import requests
import datetime
import redis
from alert_telegram import alert
from alert_email import send_email_alert


POLYGON_NODE_URL = os.getenv('POLYGON_NODE_URL')
HOST = os.getenv('NFT_REDIS_HOST')
PASSWD = os.getenv('NFT_REDIS_PASSWD')
REDIS_KEY = os.getenv('NFT_REDIS_KEY')
DB = 10
# 报警阈值
THRESHOLD = 10


def get_depoist_block_data():
    try:
        rt = redis.Redis(host=HOST, db=DB, password=PASSWD, ssl=True)
        block_number = int(rt.get(REDIS_KEY), base=10)
    except Exception as e:
        print(e)
        block_number = 0
    return block_number


def get_newest_block(url, block_number=None):
    if not block_number:
        block_number = "latest"
    param = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [block_number, False],
        "id": 1
    }
    try:
        res = requests.post(url, json=param, timeout=10)
        result = res.json()
        data = result.get("result", {})
    except Exception as e:
        data = {}
    return data


def monitor():
    process_number = get_depoist_block_data()
    if not process_number:
        text = f"【用户充值监测延迟告警】主链:Polygon\n已解析高度获取失败, 请及时检查!"
        diff_min = 10000
    else:
        process_number_hex = hex(process_number)
        node_block_data = get_newest_block(POLYGON_NODE_URL, block_number=process_number_hex)
        if not node_block_data:
            text = f"【用户充值监测延迟告警】主链:Polygon\n已解析区块的信息获取失败, 请及时检查!"
            diff_min = 10000
        else:
            block_timestamp_hex = node_block_data.get("timestamp")
            if not block_timestamp_hex:
                text = f"【用户充值监测延迟告警】主链:Polygon\n已解析区块的出块时间失败, 请及时检查!"
                diff_min = 10000
            else:
                now_timestamp = int(time.time())
                block_timestamp = int(str(block_timestamp_hex), base=16)
                diff_seconds = max(0, now_timestamp-block_timestamp)
                diff_min = diff_seconds // 60
                text =f"【用户充值监测延迟告警】主链:Polygon\n已解析高度: {process_number}\n当前延迟约: {diff_min}分钟"
                now = str(datetime.datetime.now())
                print(now, text)
    if int(diff_min) >= THRESHOLD:
        alert(text)
        send_email_alert("Polygon充值", process_number, diff_min)


if __name__ == '__main__':
    monitor()
