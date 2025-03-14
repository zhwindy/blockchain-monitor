# encoding=utf-8
import datetime
import time
import os
from db_mysql import get_conn
from alert_telegram import alert
from alert_email import send_email_alert

MODE = os.getenv('NFT_MONITOR_MODE', 'dev')
# 报警阈值
THRESHOLD = 10


def get_data():
    database = "bera_data"
    conn = get_conn(database=database)
    cursor = conn.cursor()
    sql = "select block_number, timestamp from bera_source_block order by block_number desc limit 1"
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


def monitor():
    info = get_data()
    now_timestamp = int(time.time())
    block_number = info.get("block_number")
    record_time = info.get("create_time")
    record_timestamp = int(str(record_time), base=16)
    diff_seconds = max(0, now_timestamp-record_timestamp)
    diff_min = diff_seconds // 60
    text =f"【HWC解析延迟告警】主链: Bera\n已解析高度: {block_number}\n当前延迟约: {diff_min}分钟"
    now = str(datetime.datetime.now())
    print(text)
    if MODE == 'dev':
        return None
    if int(diff_min) > THRESHOLD:
        alert(text)
        send_email_alert("Bera", block_number, diff_min)


if __name__ == "__main__":
    monitor()
