#encoding=utf-8
import os
import telegram

GROUP_ID = os.getenv('GROUP_ID', None)
BOT_TOKEN = os.getenv('BOT_TOKEN', None)


def alert(message):
    """
    send message to telegram group
    """
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.send_message(text=message, chat_id=GROUP_ID)


if __name__ == "__main__":
    text = "测试BCT"
    alert(text)
