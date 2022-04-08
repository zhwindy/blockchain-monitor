# encoding=UTF-8
import logging
import time
import requests
import pytz
from settings import config
from datetime import datetime
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO)


TOKEN = config.get("token")

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    text = "Hello everyone I'm Nftscan bot, happy to serve all. \n\nIf you have any questions, do not hesitate to let me know! \n\nMore information visit: https://nftscan.com"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def eth(update: Update, context: CallbackContext):
    text = "请使用命令: /eth1 or /eth2"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def eth1(update: Update, context: CallbackContext):
    url = "http://172.31.23.144:40000"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: eth-node-01\nip地址: 172.*.*.144\n最新高度: {block_height}\n出块时间: {block_time}"""
    chat_id = update.effective_chat.id
    logging.info(text)
    context.bot.send_message(chat_id=chat_id, text=text)


def eth2(update: Update, context: CallbackContext):
    url = "http://172.31.31.186:40000"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: eth-node-02\nip地址: 172.*.*.186\n最新高度: {block_height}\n出块时间: {block_time}"""
    chat_id = update.effective_chat.id
    logging.info(text)
    context.bot.send_message(chat_id=chat_id, text=text)


def bsc(update: Update, context: CallbackContext):
    text = "请使用命令: /bsc1 or /bsc2"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def bsc1(update: Update, context: CallbackContext):
    url = "http://10.0.0.139:8545"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: bnb-node-01\nip地址: 10.*.*.139\n最新高度: {block_height}\n出块时间: {block_time}"""
    # logging.info(update.effective_chat)
    chat_id = update.effective_chat.id
    logging.info(text)
    context.bot.send_message(chat_id=chat_id, text=text)


def bsc2(update: Update, context: CallbackContext):
    url = "http://10.0.0.172:8545"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: bnb-node-02\nip地址: 10.*.*.172\n最新高度: {block_height}\n出块时间: {block_time}"""
    chat_id = update.effective_chat.id
    logging.info(text)
    context.bot.send_message(chat_id=chat_id, text=text)


def moonbeam(update: Update, context: CallbackContext):
    url = "http://172.31.23.220:30335"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: moonbeam-node\nip地址: 172.*.*.220\n最新高度: {block_height}\n出块时间: {block_time}"""
    chat_id = update.effective_chat.id
    logging.info(text)
    context.bot.send_message(chat_id=chat_id, text=text)


def about(update: Update, context: CallbackContext):
    text = "visit: https://nftscan.com/aboutus"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def unknown(update: Update, context: CallbackContext):
    text = "Sorry, I didn't understand that command. Please wait..."
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


start_handler = CommandHandler('start', start)
eth_handler = CommandHandler('eth', eth)
eth1_handler = CommandHandler('eth1', eth1)
eth2_handler = CommandHandler('eth2', eth2)
bsc_handler = CommandHandler('bsc', bsc)
bsc1_handler = CommandHandler('bsc1', bsc1)
bsc2_handler = CommandHandler('bsc2', bsc2)
moonbeam_handler = CommandHandler('moonbeam', moonbeam)
about_handler = CommandHandler('about', about)
team_handler = CommandHandler('team', about)
help_handler = CommandHandler('help', about)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(eth_handler)
dispatcher.add_handler(eth1_handler)
dispatcher.add_handler(eth2_handler)
dispatcher.add_handler(bsc_handler)
dispatcher.add_handler(bsc1_handler)
dispatcher.add_handler(bsc2_handler)
dispatcher.add_handler(moonbeam_handler)
dispatcher.add_handler(about_handler)
dispatcher.add_handler(team_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(unknown_handler)


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
    updater.start_polling()


if __name__ == "__main__":
    main()
