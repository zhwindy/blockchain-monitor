# encoding=utf-8
import datetime
import time
import os
from db_mysql import get_conn
from alert_telegram import alert
from alert_email import send_email_alert
import pytz

MODE = os.getenv('NFT_MONITOR_MODE', 'DEV')
# 报警阈值
THRESHOLD = 5


def get_sol_data():
    database = "sol_data"
    conn = get_conn(database=database)
    cursor = conn.cursor()
    sql = "select max(block_number) as block_number, max(create_time) as timestamp from sol_transaction"
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


def solana_monitor():
    info = get_sol_data()
    now_timestamp = int(time.time())
    block_number = info.get("block_number")
    record_time = info.get("create_time")
    local_record_time = record_time - datetime.timedelta(hours=8)
    record_timestamp = int(local_record_time.timestamp())
    diff_seconds = max(0, now_timestamp-record_timestamp)
    diff_min = diff_seconds // 60
    text =f"【HWC解析延迟告警】主链: Solana\n已解析高度: {block_number}\n当前延迟约: {diff_min}分钟"
    now = str(datetime.datetime.now())
    print(text)
    if MODE == 'dev':
        return None
    if int(diff_min) > THRESHOLD:
        alert(text)
        send_email_alert("Solana", block_number, diff_min)


if __name__ == "__main__":
    solana_monitor()
