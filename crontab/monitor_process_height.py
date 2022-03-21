# encoding=utf-8
import pymysql
import datetime
import time
import telegram
import os
import pytz

mode = 'pro'

# host = "nftscan-source-db-instance-1.cjotu4lyzmfi.ap-southeast-1.rds.amazonaws.com"
host = "nftscan-data-db-instance-1.cjotu4lyzmfi.ap-southeast-1.rds.amazonaws.com"

group_id = "-533453366"
token = "5108847036:AAEj6CsAvF2NyBTjDwvrAt56MMimupGRofs"


def get_eth_data():
    user = os.getenv('NFT_MYSQL_USER')
    passwd = os.getenv('NFT_MYSQL_PASSWD')
    database = "eth_data"
    conn = pymysql.connect(host=host, user=user, passwd=passwd, db=database, charset='utf8')
    cursor = conn.cursor()
    sql = "select block_number,create_time from eth_source_block order by block_number desc limit 1"
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


def get_bsc_data():
    user = os.getenv('NFT_MYSQL_USER')
    passwd = os.getenv('NFT_MYSQL_PASSWD')
    database = "bsc_data"
    conn = pymysql.connect(host=host, user=user, passwd=passwd, db=database, charset='utf8')
    cursor = conn.cursor()
    sql = "select block_number,create_time from bsc_source_block order by block_number desc limit 1"
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
    record_timestamp = int(record_time.replace(tzinfo=pytz.timezone('Asia/Shanghai')).timestamp())
    diff_seconds = max(0, now_timestamp-record_timestamp)
    diff_min = diff_seconds // 60
    text =f"【解析延迟告警】主链:ETH\n已解析高度: {block_number}\n当前延迟约: {diff_min}分钟\n请核实相关情况, 及时处理!"
    now = str(datetime.datetime.now())
    print(now, text)
    if mode == 'dev':
        return None
    if int(diff_min) > 10:
        bot = telegram.Bot(token=token)
        bot.send_message(text=text, chat_id=group_id)


def bsc_monitor():
    info = get_bsc_data()
    now_timestamp = int(time.time())
    block_number = info.get("block_number")
    record_time = info.get("create_time")
    # record_timestamp = int(datetime.datetime.timestamp(record_time))
    record_timestamp = int(record_time.replace(tzinfo=pytz.timezone('Asia/Shanghai')).timestamp())
    diff_seconds = max(0, now_timestamp-record_timestamp)
    diff_min = diff_seconds // 60
    text =f"【解析延迟告警】主链:BNB\n已解析高度: {block_number}\n当前延迟约: {diff_min}分钟\n请核实相关情况, 及时处理!"
    now = str(datetime.datetime.now())
    print(now, text)
    if mode == 'dev':
        return None
    if int(diff_min) > 10:
        bot = telegram.Bot(token=token)
        bot.send_message(text=text, chat_id=group_id)


def main():
    eth_monitor()
    time.sleep(5)
    bsc_monitor()


if __name__ == "__main__":
    main()
    