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
# 报警阈值
THRESHOLD = 60


def get_data():
    database = "bitcoin_data"
    conn = get_conn(database=database)
    cursor = conn.cursor()
    sql = "select block_number, timestamp from btc_source_block order by block_number desc limit 1"
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
    url = f"http://{BTC_U}:{BTC_P}@172.31.22.119:8080"
    params = {
        "jsonrpc": "2.0",
        "id":"1",
        "method": "getblockchaininfo",
        "params": []
    }
    rep = requests.post(url=url, json=params, timeout=20)
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
    record_timestamp = int(record_time)
    diff_seconds = max(0, now_timestamp-record_timestamp)
    diff_min = diff_seconds // 60
    new_height = get_block_height()
    diff_block = new_height - block_number
    text =f"【Tidb 解析延迟告警】主链: BTC\n已解析高度: {block_number}\n当前最新高度: {new_height}\n当前延迟约: {diff_min}分钟"
    print(text)
    if MODE == 'dev':
        return None
    if (diff_min > THRESHOLD) and (diff_block > 2):
        alert(text)
        send_email_alert("BTC", block_number, diff_min)


if __name__ == "__main__":
    monitor()
