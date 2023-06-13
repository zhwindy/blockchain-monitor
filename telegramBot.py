# encoding=UTF-8
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CallbackContext, CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from settings import config
from common import get_block_height, get_newest_block, get_block_time

logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=logging.INFO)


TOKEN = config.get("token")

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    text = "Hello everyone I'm Nftscan bot, happy to serve all. \n\nIf you have any questions, do not hesitate to let me know! \n\nMore information visit: https://nftscan.com"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def eth_bak(update: Update, context: CallbackContext):
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


def eth(update: Update, context: CallbackContext):
    url = "http://eth-node-internal.nftscan.com:9090"
    name = "eth-node"
    text = get_node_message(url, name=name)
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text)


def moonbeam(update: Update, context: CallbackContext):
    url = "http://moonbeam-node-internal.nftscan.com:30335"
    name = "moonbeam-node"
    text = get_node_message(url, name=name)
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text)


def arbitrum(update: Update, context: CallbackContext):
    url = "http://arbitrum-node-internal.nftscan.com:8547"
    name = "arbitrum-node-internal"
    text = get_node_message(url, name=name)
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text)


def avax(update: Update, context: CallbackContext):
    url = "http://avax-node-01-internal.nftscan.com:9650/ext/bc/C/rpc"
    name = "avax-node-01-internal"
    text = get_node_message(url, name=name)
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text)


def opt(update: Update, context: CallbackContext):
    url = "http://opt-node-internal.nftscan.com:8545"
    name = "opt-node"
    text = get_node_message(url, name=name)
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text)


def platon(update: Update, context: CallbackContext):
    url = "http://platon-node-internal.nftscan.com:8545"
    name = "platon-node-internal"
    text = get_node_message(url, name=name)
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text)


def cronos(update, context):
    url = "http://cronos-node-internal.nftscan.com:8545"
    name = "cronos-node-internal"
    text = get_node_message(url, name=name)
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text)


def ftm(update, context):
    url = "http://ftm-node-internal.nftscan.com:8080"
    name = "ftm-node-internal"
    text = get_node_message(url, name=name)
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text)


def xdai(update, context):
    url = "http://xdai-node-internal.nftscan.com:8080"
    name = "xdai-node-internal"
    text = get_node_message(url, name=name)
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text)


def aptos(update, context):
    url = "http://aptos-node-internal.nftscan.com:8080"
    name = "aptos-node-internal"
    text = get_node_message(url, name=name)
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=text)


def about(update: Update, context: CallbackContext):
    text = "visit: https://nftscan.com/aboutus"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def unknown(update: Update, context: CallbackContext):
    text = "不支持的命令,请重新输入"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def get_node_message(endpoint, name='nftscan'):
    """
    提供节点接口
    """
    node_data = get_newest_block(endpoint)
    block_height = get_block_height(node_data)
    block_time = get_block_time(node_data)
    text = f"节点: {name}\n最新高度: {block_height}\n出块时间: {block_time}"""
    logging.info(text)
    return text


start_handler = CommandHandler('start', start)
eth_handler = CommandHandler('eth', eth)
moonbeam_handler = CommandHandler('moonbeam', moonbeam)
arbitrum_handler = CommandHandler('arbitrum', arbitrum)
arbi_handler = CommandHandler('arbi', arbitrum)
avax_handler = CommandHandler('avax', avax)
opt_handler = CommandHandler('opt', opt)
platon_handler = CommandHandler('platon', platon)
cro_handler = CommandHandler('cro', cronos)
ftm_handler = CommandHandler('ftm', ftm)
xdai_handler = CommandHandler('xdai', xdai)
help_handler = CommandHandler('help', about)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(eth_handler)
dispatcher.add_handler(moonbeam_handler)
dispatcher.add_handler(arbitrum_handler)
dispatcher.add_handler(arbi_handler)
dispatcher.add_handler(avax_handler)
dispatcher.add_handler(opt_handler)
dispatcher.add_handler(platon_handler)
dispatcher.add_handler(cro_handler)
dispatcher.add_handler(ftm_handler)
dispatcher.add_handler(xdai_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(unknown_handler)
dispatcher.add_handler(CallbackQueryHandler(keyboard_callback))


def main():
    updater.start_polling()


if __name__ == "__main__":
    main()
