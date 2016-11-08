#!/usr/bin/env python3
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import bcolors
import logging
import telepot
import os

from proverb_pro import *

SEND_PIC = "📷" # ":camera:"
SEND_TEXT = "💬" # ":speech_balloon:"

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    logging.info("Received a {} in chat {}".format(content_type, chat_id))
    if content_type == "text" and msg["text"] == SEND_PIC:
        logging.info("Received command {}, sending picture".format(SEND_PIC))
        img_file_path = apply_proverb(get_random_image(), get_proverb())
        bot.sendPhoto(chat_id, (img_file_path, open(img_file_path, "rb")))
        os.remove(img_file_path)
    elif content_type == "text" and msg["text"] == SEND_TEXT:
        logging.info("Received command {}, sending text".format(SEND_TEXT))
        bot.sendMessage(chat_id, get_proverb())
    else:
        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=SEND_PIC)], [KeyboardButton(text=SEND_TEXT)]])
        bot.sendMessage(chat_id, "Yo!", reply_markup=keyboard)

if __name__ == "__main__":
    logging.basicConfig(
        format="{}[%(levelname)s %(asctime)s]{} %(message)s".format(
            bcolors.BOLD,
            bcolors.ENDC
        ), level=logging.INFO
    )
    TOKEN = open("proverb_bot.token").read().strip()

    bot = telepot.Bot(TOKEN)
    bot.message_loop(handle, run_forever=True)


