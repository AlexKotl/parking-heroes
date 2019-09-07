import os
import telebot
from queries import Queries 
BOT_TOKEN = os.environ['BOT_TOKEN']

bot = telebot.TeleBot(BOT_TOKEN)

queries = Queries()
for row in queries.get_all_parking():
    print(row)
    
keyboard_buttons = {
    "report": "🚨 Сообщить о нарушителе",
    "list": "🅿️ Список нарушителей", 
    "details": "🚙 Информация по номеру",
    "about": "ℹ️ О боте",
}

def create_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(*keyboard_buttons.values())
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(chat_id=message.chat.id, 
        text='Привет! Здесь вы сможете пожаловаться на нарушителей правил паровки ЖК "Сырецкий Бояр".'
        'Возспользуйтесь кнопками внизу, чтобы добавить нарушителя или просмотреть список "героев".', 
        reply_markup=create_keyboard())

@bot.message_handler()
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id=message.chat.id, text='Hi there', reply_markup=create_keyboard())

bot.polling()
