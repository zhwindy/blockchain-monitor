#encoding=utf-8
import os
import telegram

GROUP_ID = os.getenv('GROUP_ID', None)
BOT_TOKEN = os.getenv('BOT_TOKEN', None)


def alert(message):
    """
    send message to telegram group
    """
    if not GROUP_ID or not BOT_TOKEN:
        print("telegram msg send failed")
        return None
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.send_message(text=message, chat_id=GROUP_ID)
    print("telegram msg send success")


if __name__ == "__main__":
    text = "测试BCT"
    alert(text)
