# encoding=utf-8
import os
import time
from utils import rpc
import datetime
import telegram
import redis

HOST = os.getenv('NFT_REDIS_HOST')
PASSWD = os.getenv('NFT_REDIS_PASSWD')
REDIS_KEY = os.getenv('NFT_REDIS_KEY')
DB = 4
GROUP_ID = "-533453366"
TOKEN = "5108847036:AAEj6CsAvF2NyBTjDwvrAt56MMimupGRofs"
NODE_URL = "http://eth-node-01-internal.nftscan.com:40000"
# 报警阈值
THRESHOLD = 10


def get_depoist_block_data():
    try:
        rt = redis.Redis(host=HOST, db=DB, password=PASSWD, ssl=True)
        block_number = int(rt.get(REDIS_KEY), base=10)
    except Exception as e:
        print(e)
        block_number = None
    return block_number


def monitor():
    process_number = get_depoist_block_data()
    if not process_number:
        text = f"【用户充值监控延迟告警】主链ETH用户充值\n已解析高度获取失败, 请及时检查!"
        diff_min = 10000
    else:
        process_number_hex = hex(process_number)
        node_block_data = rpc.get_newest_block(NODE_URL, block_number=process_number_hex)
        block_timestamp_hex = node_block_data.get("timestamp")
        if not block_timestamp_hex:
            text = f"【用户充值监控延迟告警】主链ETH用户充值\n已解析区块的出块时间失败, 请及时检查!"
            diff_min = 10000
        else:
            now_timestamp = int(time.time())
            block_timestamp = int(str(block_timestamp_hex), base=16)
            diff_seconds = max(0, now_timestamp-block_timestamp)
            diff_min = diff_seconds // 60
            text =f"【用户充值监控延迟告警】主链ETH用户充值\n已解析高度: {process_number}\n当前延迟约: {diff_min}分钟"
            now = str(datetime.datetime.now())
            print(now, text)
    if int(diff_min) >= THRESHOLD:
        bot = telegram.Bot(token=TOKEN)
        bot.send_message(text=text, chat_id=GROUP_ID)


if __name__ == '__main__':
    monitor()
