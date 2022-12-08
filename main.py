import os
import random

import requests
import telebot
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ.get("BOT_TOKEN")
URL = "https://paper-trader.frwd.one/"


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def get_start_messages(message):
        bot.send_message(message.chat.id, "Hello, lets start our trading!")

    @bot.message_handler()
    def get_text_messages(message):

        # Defining random data for request
        timeframe = random.choice(("5m", "15m", "1h", "4h", "1d", "1w", "1M"))
        candles = random.randint(0, 1000)
        ma = random.randint(0, 50)
        tp = random.randint(0, 101)
        sl = random.randint(0, 101)

        # Collect data into one dictionary for better formatting
        data = {
            "pair": message.text,
            "timeframe": timeframe,
            "candles": candles,
            "ma": ma,
            "tp": tp,
            "sl": sl
            }

        # Sending request to the site (URL)
        try:
            response = requests.post(URL, data=data)
        except requests.RequestException:
            bot.send_message(message.chat.id, ("Oops, something went "
                                               "wrong... Try again"))

        # Finding a link for the image
        try:
            soup = BeautifulSoup(response.text, features="html.parser")
            images = soup.find_all('img')
            image_source = URL + images[0].get("src")[2:]
        except (IndexError, UnboundLocalError):
            bot.send_message(
                message.chat.id,
                "Oops, something went wrong... Try again"
            )

        # Sending photo with results via Telegram Bot
        bot.send_message(
            message.chat.id,
            f"Here are your result for {data['pair']}"
        )
        bot.send_photo(message.chat.id, image_source)

    bot.polling()


if __name__ == "__main__":
    telegram_bot(BOT_TOKEN)
