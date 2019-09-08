import os
import telebot
import datetime
from collections import defaultdict
from queries import Queries 
from plate import Plate
from settings import *
BOT_TOKEN = os.environ['BOT_TOKEN']
STEP_DEFAULT, STEP_PLATE_INFO = 0, 1

user_step = defaultdict(lambda: STEP_DEFAULT)
bot = telebot.TeleBot(BOT_TOKEN)
repo = Queries()
plate = Plate()

def create_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(*keyboard_buttons.values())
    return keyboard

def get_step(message):
    return user_step[message.chat.id]
    
def set_step(message, step):
    user_step[message.chat.id] = step

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(chat_id=message.chat.id, 
        text=START_TEXT, 
        reply_markup=create_keyboard())
        
@bot.message_handler(func=lambda message: message.text == keyboard_buttons['about'])
def handle_abut(message):
    ''' Send info about bot '''
    bot.send_message(chat_id=message.chat.id, text=ABOUT_TEXT, reply_markup=create_keyboard())

@bot.message_handler(func=lambda message: message.text == keyboard_buttons['list'])
def handle_message(message):
    ''' Send LIST of disturbers '''
    text = 'Список 10 героев парковки: \n\n'
    for row in repo.get_all_parking():
        text += f" - {row['car_plate']} {row['description']} \n"
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=create_keyboard())
    
@bot.message_handler(func=lambda message: message.text == keyboard_buttons['details'])
def handle_abut(message):
    ''' Ask for plate no to send info about it '''
    bot.send_message(chat_id=message.chat.id, text="Введите номерной знак (например АА8765ОЕ):", reply_markup=create_keyboard())
    set_step(message, STEP_PLATE_INFO)
    
@bot.message_handler(func=lambda message: get_step(message) == STEP_PLATE_INFO)
def handle_abut(message):
    ''' Send info about specific plate no '''
    number = plate.format_plate(message.text)
    print('Checking plate {}'.format(number))
    reply = ''
    
    if number == False:
        reply = f'Введенный вами номер "{message.text}" не распознан как автомобильный номер.'
    else:
        rows = repo.get_parking_by_plate(number)
        if rows == False:
            reply = f"Записей по номеру {message.text} не было найдено. Похоже автомобиль не нарушал правил парковки."
        else:
            reply = f"Найденные записи по номеру {message.text}: \n\n"
            for row in rows:
                reply += f" - {row['description']} ({row['date_created'].date()})"
        
    bot.send_message(chat_id=message.chat.id, text=reply, reply_markup=create_keyboard())
    set_step(message, STEP_DEFAULT)
    

print('Starting bot...')
bot.polling()
