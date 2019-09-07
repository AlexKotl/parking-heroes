import os
import telebot
from queries import Queries 

BOT_TOKEN = os.environ['BOT_TOKEN']

bot = telebot.TeleBot(BOT_TOKEN)

queries = Queries()
for row in queries.get_all_parking():
    print(row)

def create_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    buttons = [
        "🅿️ Список нарушителей", 
        "ℹ️ Информация",
        "🚨 Сообщить о нарушителе",
    ]
    keyboard.add(*buttons)
    return keyboard

@bot.message_handler()
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id=message.chat.id, text='Hi there', reply_markup=create_keyboard())

bot.polling()
