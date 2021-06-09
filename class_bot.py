#!/usr/local/bin/python3

import telebot
from start_class import click_all
# import time
# import logging

bot = telebot.TeleBot('1438451238:AAHYpWwXrXwnAMRBCTtQtZdxPJZXwU0MDNg')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Я бот. Приятно познакомиться')


@bot.message_handler(commands=['buttom'])
def send_welcome(message):
    bot.reply_to(message, 'Отмечаюсь в классе')
    click_all()


bot.polling(none_stop=True)
