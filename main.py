# encoding=UTF-8
import logging
import requests
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler


logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO)

TOKEN = "5108847036:AAEj6CsAvF2NyBTjDwvrAt56MMimupGRofs"
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    text = "I'm blockchain node info bot, support command: eth bsc1 bsc2"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def bsc1(update: Update, context: CallbackContext):
    url = "http://10.0.0.112:8545"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"""
    最新高度: {block_height}
    出块时间: {block_time}
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


start_handler = CommandHandler('start', start)
eth_handler = CommandHandler('eth', start)
bsc1_handler = CommandHandler('bsc1', bsc1)
bsc2_handler = CommandHandler('bsc2', start)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(eth_handler)
dispatcher.add_handler(bsc1_handler)
dispatcher.add_handler(bsc2_handler)


def get_newest_block(url):
    param = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": ["latest", False],
        "id": 1
    }
    try:
        res = requests.post(url, json=param, timeout=20)
        result = res.json()
        data = result.get("result", {})
    except Exception as e:
        data = {}
    return data


def get_block_height(data):
    block_height = data.get("number", 1)
    height = int(block_height)
    return height


def get_block_time(data):
    time = data.get("timestamp")
    timestamp = int(time)
    return timestamp


def main():
    updater.start_polling()


if __name__ == "__main__":
    main()
