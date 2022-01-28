import logging
import os
import time
from logging.handlers import RotatingFileHandler
from typing import Dict
import json
import requests
from telegram import (
    ReplyKeyboardRemove,
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from telegram.ext import Updater, Filters, CallbackContext, MessageHandler


TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TIMER_SLEEP = 300
URL_SERVER_IOT = "http://0.0.0.0:8001/"

button_choose_start_pc = "Выбор ПК для запуска"

start_word = "Запустить"


def generate_keyboard_pc(personals_computers) -> ReplyKeyboardMarkup:
    list_pcs = [
        f"{start_word} {pc['id']} {pc['name']}" for pc in personals_computers
    ]
    list_buttons = [KeyboardButton(text=pc) for pc in list_pcs]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[list_buttons],
        resize_keyboard=True,
    )
    return keyboard


def wake_on_lan_handler(update: Update, context: CallbackContext):
    splited = update.message.text.split()
    id = int(splited[1])
    telegram_chat_id: int = update.message.chat_id
    data = {
        "telegram_chat_id": telegram_chat_id,
    }

    requests.post(f"{URL_SERVER_IOT}api/wake-on-lan/{id}/", json=data)


def choose_start_pc_handler(update: Update, context: CallbackContext):
    response = requests.get(f"{URL_SERVER_IOT}api/personal-computers/")
    data = response.json()
    keyboard_list_pcs = generate_keyboard_pc(data)
    update.message.reply_text(
        text="Выберите пк для запуска", reply_markup=keyboard_list_pcs
    )


def message_handler(update: Update, context: CallbackContext):
    if update.message.text == button_choose_start_pc:
        return choose_start_pc_handler(update, context)
    if update.message.text.split()[0] == start_word:
        return wake_on_lan_handler(update, context)

    reply_markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=button_choose_start_pc)]],
        resize_keyboard=True,
    )
    update.message.reply_text(
        text="Выберите необходимое действие", reply_markup=reply_markup
    )


def main() -> None:
    print("start")
    updater = Updater(
        token=TELEGRAM_TOKEN,
        use_context=True,
    )
    updater.dispatcher.add_handler(
        MessageHandler(filters=Filters.all, callback=message_handler)
    )
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
