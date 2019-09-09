import os
import telebot
import datetime
import requests
import plural_ru
from collections import defaultdict
from queries import Queries 
from plate import Plate
from settings import *
BOT_TOKEN = os.environ['BOT_TOKEN']
STEP_DEFAULT, STEP_PLATE_INFO, STEP_ADD_PLATE, STEP_ADD_DESCRIPTION = range(4)

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
	bot.send_message(chat_id=message.chat.id, text=START_TEXT + '\n\n' + get_summary_text(), reply_markup=create_keyboard())
    
def get_summary_text():
    stats = repo.get_overall_stats()
    text = f'У нас уже зафиксировано: {stats["cars_count"]} {plural_ru.ru(stats["cars_count"],["нарушитель","нарушителя","нарушителей"])}, ' \
        f'{stats["records_count"]} {plural_ru.ru(stats["records_count"],["нарушение","нарушения","нарушений"])}, ' \
        f'о которых нам сообщили {stats["users_count"]} {plural_ru.ru(stats["users_count"], ["пользователь","пользователя","пользователей"])}. '
    return text

# INFO

@bot.message_handler(func=lambda message: message.text == keyboard_buttons['about'])
def handle_message(message):
    ''' Send info about bot '''
    print(message.from_user)
    bot.send_message(chat_id=message.chat.id, text=ABOUT_TEXT + '\n\n' + get_summary_text(), reply_markup=create_keyboard())
    set_step(message, STEP_DEFAULT)

# LIST

@bot.message_handler(func=lambda message: message.text == keyboard_buttons['list'])
def handle_message(message):
    ''' Send LIST of disturbers '''
    text = 'Список 10 героев парковки: \n\n'
    for row in repo.get_top_parkings():
        text += f" - {row['car_plate']} {row['description']} \n"
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=create_keyboard())
    set_step(message, STEP_DEFAULT)

# CAR DETAILS
    
@bot.message_handler(func=lambda message: message.text == keyboard_buttons['details'])
def handle_message(message):
    ''' Ask for plate no to send info about it '''
    bot.send_message(chat_id=message.chat.id, text="Введите номерной знак (например АА8765ОЕ):", reply_markup=create_keyboard())
    set_step(message, STEP_PLATE_INFO)
    
@bot.message_handler(func=lambda message: get_step(message) == STEP_PLATE_INFO)
def handle_message(message):
    ''' Send info about specific plate no '''
    number = plate.format_plate(message.text)
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

# ADD CAR

@bot.message_handler(func=lambda message: message.text == keyboard_buttons['report'])
def handle_message(message):
    ''' Ask for plate no to add new info '''
    bot.send_message(chat_id=message.chat.id, text="Введите номерной знак нарушителя, чтобы добавить его в базу (например АА8765ОЕ):", reply_markup=create_keyboard())
    set_step(message, STEP_ADD_PLATE)

@bot.message_handler(func=lambda message: get_step(message) == STEP_ADD_PLATE)
def handle_message(message):
    ''' Adding plate no to database, requesting details '''
    number = plate.format_plate(message.text)
    if number == False:
        reply = f'Введенный вами номер "{message.text}" не распознан как автомобильный номер. Попробуйте снова:'
    else:
        try:
            repo.add_parking(car_plate=number, user_id=message.from_user.id, user_username=message.from_user.username, user_first_name=message.from_user.first_name, user_last_name=message.from_user.last_name)
            reply = f'Машина с номерным знаком {number} добавлена. \n\n' \
                'Теперь вы можете прикрепить фото нарушения или добавить комментарий (такой как марку и модель авто, условия парковки, пожелания и прочее):'
            set_step(message, STEP_ADD_DESCRIPTION)
        except Exception as e:
            reply = f'Ошибка при добавлении записи: {e}'
            set_step(message, STEP_DEFAULT)
    bot.send_message(chat_id=message.chat.id, text=reply, reply_markup=create_keyboard())

@bot.message_handler(func=lambda message: get_step(message) == STEP_ADD_DESCRIPTION)
def handle_message(message):
    ''' Adding description to plate no '''
    record_id = repo.get_latest_parking_by_user(message.from_user.id)['id']
    reply = ''
    try:
        repo.add_parking_description(record_id, message.text)
        reply = 'Описание к нарушению добавлено. \nДобавить еще нарушителя? Воспользуйтесь кнопками ниже.'
    except:
        reply = f'Что-то пошло не так... Не могу добавить описание. '
    set_step(message, STEP_DEFAULT)
    bot.send_message(chat_id=message.chat.id, text=reply, reply_markup=create_keyboard())
    
@bot.message_handler(content_types=['photo'])
def handle_message(message):
    try:
        record_id = repo.get_latest_parking_by_user(message.from_user.id)['id']
        photo_info = bot.get_file(message.photo[-1].file_id)
        photo = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(BOT_TOKEN, photo_info.file_path))
        with open(os.path.join("upload", f"{record_id}.jpg"), 'wb') as f:
            f.write(photo.content)
        reply = 'Фото добавлено.'
    except:
        reply = 'Ошибка при загрузке фото.'
    bot.send_message(chat_id=message.chat.id, text=reply, reply_markup=create_keyboard())
    set_step(message, STEP_DEFAULT)

print('Starting bot...')
bot.polling()
