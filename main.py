import os
import random

import requests
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def get_text_messages(message):
        bot.send_message(message.chat.id, "Hello, lets start our trading!")

    @bot.message_handler()
    def get_text_messages(message):
        timeframe = random.choice(("5m", "15m", "1h", "4h", "1d", "1w", "1M"))
        candles = random.randint(0, 1001)
        period = random.randint(0, 365)
        take_profit_percentage = random.randint(0, 101)
        stop_loss_percentage = random.randint(0, 101)

        response = requests.get(
            "https://paper-trader.frwd.one/",
            params={
                message: message,
                timeframe: timeframe,
                candles: candles,
                period: period,
                take_profit_percentage: take_profit_percentage,
                stop_loss_percentage: stop_loss_percentage
            }
        )

        bot.send_message(message.chat.id, response)
        print(response.raw)

    bot.polling()


if __name__ == "__main__":
    telegram_bot(BOT_TOKEN)
