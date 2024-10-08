# encoding=utf-8
import datetime
import requests
import time
import os
from db_mysql import get_conn
from alert_telegram import alert
from alert_email import send_email_alert

MODE = os.getenv('NFT_MONITOR_MODE', 'dev')
BTC_U = os.getenv('BTC_U')
BTC_P = os.getenv('BTC_P')
BTC_NODE_URL = os.getenv('BTC_NODE_URL')
# 报警阈值
THRESHOLD = 90


def get_data():
    database = "btc_data"
    conn = get_conn(database=database)
    cursor = conn.cursor()
    sql = "select block_number, create_time from rune_transaction order by block_number desc limit 1"
    info = {
        "block_number": 0,
        "create_time": 0
    }
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        block_number = result[0]
        create_time = result[1]
        info['block_number'] = block_number
        info['create_time'] = create_time
    except Exception as e:
        print(e)
    conn.close()
    return info

def get_block_height():
    """
    查询当前最新高度
    """
    params = {
        "jsonrpc": "2.0",
        "id":"1",
        "method": "getblockchaininfo",
        "params": []
    }
    rep = requests.post(url=BTC_NODE_URL, json=params, timeout=20)
    if rep.status_code == 200:
        rt_data = rep.json()
        rt = rt_data.get("result", {})
        height = rt.get("headers", 1)
    else:
        height = 1
    return height

def monitor():
    info = get_data()
    now_timestamp = int(time.time())
    block_number = info.get("block_number")
    record_time = info.get("create_time")
    record_timestamp = int(record_time.timestamp())
    diff_seconds = max(0, now_timestamp-record_timestamp)
    diff_min = diff_seconds // 60
    new_height = get_block_height()
    diff_block = new_height - block_number
    text =f"【HWC解析延迟告警】主链: BTC-RUNE\n已解析高度: {block_number}\n当前最新高度: {new_height}\n当前延迟约: {diff_min}分钟"
    print(text)
    if MODE == 'dev':
        return None
    if (diff_min > THRESHOLD) and (diff_block > 3):
        alert(text)
        send_email_alert("BTC-RUNE", block_number, diff_min)


if __name__ == "__main__":
    monitor()
