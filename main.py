# encoding=UTF-8
import logging
import time
import requests
import pytz
from settings import config
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CallbackContext, CallbackQueryHandler
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
    """
    请使用命令: /eth1 or /eth2
    """
    keyboard = [
        [
            InlineKeyboardButton("eth-node-01", callback_data='eth-node-01'),
            InlineKeyboardButton("eth-node-02", callback_data='eth-node-02'),
        ],
        # [
        #     InlineKeyboardButton("eth-", callback_data='3'),
        # ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("选择要查询的节点:", reply_markup=reply_markup)


def keyboard_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    call_data = query.data
    query.answer()
    query.edit_message_text(text=f"查询的节点是:{call_data}")
    if call_data == "eth-node-01":
        eth1(update, context)
    else:
        eth2(update, context)


def eth1(update: Update, context: CallbackContext):
    url = "http://eth-node-01-internal.nftscan.com:40000"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: eth-node-01\n地址: eth-node-01-internal.nftscan.com\n最新高度: {block_height}\n出块时间: {block_time}"""
    chat_id = update.effective_chat.id
    logging.info(text)
    context.bot.send_message(chat_id=chat_id, text=text)


def eth2(update: Update, context: CallbackContext):
    url = "http://eth-node-02-internal.nftscan.com:40000"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: eth-node-02\n地址: eth-node-02-internal.nftscan.com\n最新高度: {block_height}\n出块时间: {block_time}"""
    chat_id = update.effective_chat.id
    logging.info(text)
    context.bot.send_message(chat_id=chat_id, text=text)


def bsc(update: Update, context: CallbackContext):
    text = "请使用命令: /bsc1 or /bsc2"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def bsc1(update: Update, context: CallbackContext):
    url = "http://bsc-node-01-internal.nftscan.com:8545"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: bnb-node-01\n地址: bsc-node-01-internal.nftscan.com\n最新高度: {block_height}\n出块时间: {block_time}"""
    chat_id = update.effective_chat.id
    logging.info(text)
    context.bot.send_message(chat_id=chat_id, text=text)


def bsc2(update: Update, context: CallbackContext):
    url = "http://bsc-node-02-internal.nftscan.com:8545"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: bnb-node-02\n地址: bsc-node-02-internal.nftscan.com\n最新高度: {block_height}\n出块时间: {block_time}"""
    chat_id = update.effective_chat.id
    logging.info(text)
    context.bot.send_message(chat_id=chat_id, text=text)


def polygon1(update: Update, context: CallbackContext):
    url = "http://polygon-node-01-internal.nftscan.com:8545"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: polygon-node-01\n地址: polygon-node-01-internal.nftscan.com\n最新高度: {block_height}\n出块时间: {block_time}"""
    chat_id = update.effective_chat.id
    logging.info(text)
    context.bot.send_message(chat_id=chat_id, text=text)


def polygon2(update: Update, context: CallbackContext):
    url = "http://polygon-node-02-internal.nftscan.com:8545"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: polygon-node-02\n地址: polygon-node-02-internal.nftscan.com\n最新高度: {block_height}\n出块时间: {block_time}"""
    chat_id = update.effective_chat.id
    logging.info(text)
    context.bot.send_message(chat_id=chat_id, text=text)


def moonbeam(update: Update, context: CallbackContext):
    url = "http://moonbeam-node-internal.nftscan.com:30335"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: moonbeam-node\n地址: moonbeam-node-internal.nftscan.com\n最新高度: {block_height}\n出块时间: {block_time}"""
    chat_id = update.effective_chat.id
    logging.info(text)
    context.bot.send_message(chat_id=chat_id, text=text)


def arbitrum(update: Update, context: CallbackContext):
    url = "http://arbitrum-node-internal.nftscan.com:8547"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: Arbitrum-node\n地址: arbitrum-node-internal.nftscan.com\n最新高度: {block_height}\n出块时间: {block_time}"""
    chat_id = update.effective_chat.id
    logging.info(text)
    context.bot.send_message(chat_id=chat_id, text=text)


def avax(update: Update, context: CallbackContext):
    url = "http://avax-node-01-internal.nftscan.com:9650/ext/bc/C/rpc"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: Avax-node\n地址: avax-node-01-internal.nftscan.com\n最新高度: {block_height}\n出块时间: {block_time}"""
    chat_id = update.effective_chat.id
    logging.info(text)
    context.bot.send_message(chat_id=chat_id, text=text)


def opt(update: Update, context: CallbackContext):
    url = "http://opt-node-internal.nftscan.com:9991"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: opt-node\n地址: opt-node-internal.nftscan.com\n最新高度: {block_height}\n出块时间: {block_time}"""
    chat_id = update.effective_chat.id
    logging.info(text)
    context.bot.send_message(chat_id=chat_id, text=text)


def platon(update: Update, context: CallbackContext):
    url = "http://platon-node-internal.nftscan.com:8545"
    node_data = get_newest_block(url)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: PlatON-node\n地址: platon-node-internal.nftscan.com\n最新高度: {block_height}\n出块时间: {block_time}"""
    chat_id = update.effective_chat.id
    logging.info(text)
    context.bot.send_message(chat_id=chat_id, text=text)


def about(update: Update, context: CallbackContext):
    text = "visit: https://nftscan.com/aboutus"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def unknown(update: Update, context: CallbackContext):
    text = "Sorry, I didn't understand that command."
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


start_handler = CommandHandler('start', start)
eth_handler = CommandHandler('eth', eth)
eth1_handler = CommandHandler('eth1', eth1)
eth2_handler = CommandHandler('eth2', eth2)
bsc_handler = CommandHandler('bsc', bsc)
bsc1_handler = CommandHandler('bsc1', bsc1)
bsc2_handler = CommandHandler('bsc2', bsc2)
polygon1_handler = CommandHandler('polygon1', polygon1)
polygon2_handler = CommandHandler('polygon2', polygon2)
moonbeam_handler = CommandHandler('moonbeam', moonbeam)
arbitrum_handler = CommandHandler('arbitrum', arbitrum)
arbi_handler = CommandHandler('arbi', arbitrum)
avax_handler = CommandHandler('avax', avax)
opt_handler = CommandHandler('opt', opt)
platon_handler = CommandHandler('platon', platon)
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
dispatcher.add_handler(polygon1_handler)
dispatcher.add_handler(polygon2_handler)
dispatcher.add_handler(moonbeam_handler)
dispatcher.add_handler(arbitrum_handler)
dispatcher.add_handler(arbi_handler)
dispatcher.add_handler(avax_handler)
dispatcher.add_handler(opt_handler)
dispatcher.add_handler(platon_handler)
dispatcher.add_handler(about_handler)
dispatcher.add_handler(team_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(unknown_handler)
dispatcher.add_handler(CallbackQueryHandler(keyboard_callback))


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
    height = int(block_height, base=16)
    return height


def get_block_time(data):
    time = data.get("timestamp", "1000000000")
    timestamp = int(time, base=16)
    if timestamp > 16590017801:
        timestamp = timestamp // 1000
    date_time = datetime.fromtimestamp(timestamp, pytz.timezone('Asia/Shanghai'))
    time = date_time.strftime("%Y-%m-%d %H:%M:%S")
    return time


def main():
    updater.start_polling()


if __name__ == "__main__":
    main()
