import os
import telebot
from queries import Queries 
from settings import *
BOT_TOKEN = os.environ['BOT_TOKEN']

bot = telebot.TeleBot(BOT_TOKEN)

queries = Queries()
for row in queries.get_all_parking():
    print(row)
    


def create_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(*keyboard_buttons.values())
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(chat_id=message.chat.id, 
        text=START_TEXT, 
        reply_markup=create_keyboard())
        
@bot.message_handler(func=lambda message: message.text == keyboard_buttons['about'])
def handle_message(message):
    bot.send_message(chat_id=message.chat.id, text=ABOUT_TEXT, reply_markup=create_keyboard())

@bot.message_handler()
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id=message.chat.id, text='Hi there', reply_markup=create_keyboard())

bot.polling()
