# encoding=utf-8
import pymysql
import datetime
import time
import telegram
import os
import pytz

MODE = os.getenv('NFT_MONITOR_MODE', 'dev')
HOST = os.getenv('NFT_MYSQL_HOST')
USER = os.getenv('NFT_MYSQL_USER')
PASSWD = os.getenv('NFT_MYSQL_PASSWD')
GROUP_ID = "-533453366"
TOKEN = "5108847036:AAEj6CsAvF2NyBTjDwvrAt56MMimupGRofs"
# 报警阈值
THRESHOLD = 15


def get_eth_data():
    database = "eth_data"
    conn = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=database, charset='utf8')
    cursor = conn.cursor()
    sql = "select block_number, timestamp from eth_source_block order by block_number desc limit 1"
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


def eth_monitor():
    info = get_eth_data()
    now_timestamp = int(time.time())
    block_number = info.get("block_number")
    record_time = info.get("create_time")
    # record_timestamp = int(datetime.datetime.timestamp(record_time))
    # record_timestamp = int(record_time.replace(tzinfo=pytz.timezone('Asia/Shanghai')).timestamp())
    record_timestamp = int(str(record_time), base=16)
    diff_seconds = max(0, now_timestamp-record_timestamp)
    diff_min = diff_seconds // 60
    text =f"【解析延迟告警】主链:ETH\n已解析高度: {block_number}\n当前延迟约: {diff_min}分钟\n请及时关注处理!"
    now = str(datetime.datetime.now())
    print(now, text)
    if MODE == 'dev':
        return None
    if int(diff_min) > THRESHOLD:
        bot = telegram.Bot(token=TOKEN)
        bot.send_message(text=text, chat_id=GROUP_ID)


if __name__ == "__main__":
    eth_monitor()
