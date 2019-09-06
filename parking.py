import os
import telebot
from queries import Queries 

BOT_TOKEN = os.environ['BOT_TOKEN']

bot = telebot.TeleBot(BOT_TOKEN)

queries = Queries()
for row in queries.get_all_parking():
    print(row)

@bot.message_handler()
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id=message.chat.id, text='Hi there')

bot.polling()
