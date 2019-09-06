import os
import telebot
import pymysql
from pymysql.cursors import DictCursor
db = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='parking',
    charset='utf8mb4',
    cursorclass=DictCursor
)

BOT_TOKEN = os.environ['BOT_TOKEN']

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler()
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id=message.chat.id, text='Hi there')

bot.polling()

db.close()