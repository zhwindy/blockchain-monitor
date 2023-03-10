#encoding=utf-8
import telegram

GROUP_ID = "-533453366"
BOT_TOKEN = "5108847036:AAEj6CsAvF2NyBTjDwvrAt56MMimupGRofs"


def alert(message):
    """
    send message to telegram group
    """
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.send_message(text=message, chat_id=GROUP_ID)


if __name__ == "__main__":
    text =f"【Tidb 解析延迟告警】主链: BTC\n已解析高度: 1\n当前延迟约: 0分钟"
    alert(text)
