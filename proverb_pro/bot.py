#!/usr/bin/env python3
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import logging
import os
import proverb_pro.generator as proverb_pro
import sys
import telepot

SEND_PIC = "📷"  # ":camera:"
SEND_TEXT = "💬"  # ":speech_balloon:"


def run():
    logging.basicConfig(level=logging.INFO)

    if "TELEGRAM_BOT_TOKEN" not in os.environ:
        print(
            "Please specify bot token in variable TELEGRAM_BOT_TOKEN.",
            file=sys.stderr,
        )
        sys.exit(1)

    bot = telepot.Bot(os.environ["TELEGRAM_BOT_TOKEN"].strip())

    def handle(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        logging.info("Received a {} in chat {}".format(content_type, chat_id))
        if content_type == "text" and msg["text"] == SEND_PIC:
            logging.info("Received command {}, sending picture".format(SEND_PIC))
            img_file_path = proverb_pro.apply_proverb(
                proverb_pro.get_random_image(), proverb_pro.get_proverb()
            )
            bot.sendPhoto(chat_id, (img_file_path, open(img_file_path, "rb")))
            os.remove(img_file_path)
        elif content_type == "text" and msg["text"] == SEND_TEXT:
            logging.info("Received command {}, sending text".format(SEND_TEXT))
            bot.sendMessage(chat_id, proverb_pro.get_proverb())
        else:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text=SEND_PIC), KeyboardButton(text=SEND_TEXT)]
                ]
            )
            bot.sendMessage(chat_id, "Yo!", reply_markup=keyboard)

    bot.message_loop(handle, run_forever=True)
