import os
import telebot
import flask
import datetime
import requests
import plural_ru
import logging
from collections import defaultdict
from classes.queries import Queries 
from classes.plate import Plate
from settings import *
BOT_TOKEN = os.environ['BOT_TOKEN']
BOT_METHOD = os.environ['BOT_METHOD']
STEP_DEFAULT, STEP_PLATE_INFO, STEP_ADD_PLATE, STEP_ADD_DESCRIPTION = range(4)

user_step = defaultdict(lambda: STEP_DEFAULT)
bot = telebot.TeleBot(BOT_TOKEN)
repo = Queries()
plate = Plate()

if BOT_METHOD == 'webhook':
    logger = telebot.logger
    # set to logging.DEBUG when debugging
    telebot.logger.setLevel(logging.INFO) 

    app = flask.Flask(__name__)

def create_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(*keyboard_buttons.values())
    return keyboard

def get_step(message):
    return user_step[message.chat.id]
    
def set_step(message, step):
    user_step[message.chat.id] = step

def send_photo(message, filename):
    if filename == '':
        return False
    try:
        photo = open(f'upload/{filename}', 'rb')
        bot.send_photo(message.chat.id, photo)
    except:
        print(f'Cant open photo {filename}')

def log_message(func):
    def wrapped(*kargs, **kwargs):
        print('{}: {}'.format(kargs[0].chat.id, kargs[0].text))
        repo.add_log(message=kargs[0].text, chat_id=kargs[0].chat.id, user_id=kargs[0].from_user.id, username=kargs[0].from_user.username)
        return func(*kargs, **kwargs)
    return wrapped


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(chat_id=message.chat.id, text=START_TEXT + '\n\n' + get_summary_text(), reply_markup=create_keyboard(), parse_mode='Markdown')
    
def get_summary_text():
    stats = repo.get_overall_stats()
    text = f'У нас уже зафиксировано: *{stats["cars_count"]}* {plural_ru.ru(stats["cars_count"],["нарушитель","нарушителя","нарушителей"])}, ' \
        f'*{stats["records_count"]}* {plural_ru.ru(stats["records_count"],["нарушение","нарушения","нарушений"])} ' \
        f'подтвержденных *{stats["photo_count"]}* {plural_ru.ru(stats["photo_count"],["фотографией","фотографиями","фотографиями"])}, ' \
        f'о которых нам {plural_ru.ru(stats["users_count"], ["сообщил","сообщило","сообщили"])} *{stats["users_count"]}* {plural_ru.ru(stats["users_count"], ["пользователь","пользователя","пользователей"])}. '
    return text

# INFO

@bot.message_handler(func=lambda message: message.text == keyboard_buttons['about'])
@log_message
def handle_message(message):
    ''' Send info about bot '''
    bot.send_message(chat_id=message.chat.id, text=ABOUT_TEXT + '\n\n' + get_summary_text(), reply_markup=create_keyboard(), parse_mode='Markdown')
    set_step(message, STEP_DEFAULT)

# LIST

@bot.message_handler(func=lambda message: message.text == keyboard_buttons['list'])
@log_message
def handle_message(message):
    ''' Send LIST of disturbers '''
    text = '🚗 Список 10 героев парковки: \n\n'
    for row in repo.get_top_parkings():
        text += f" /_{plate.cyr_to_latin(row['car_plate'])} - {row['count']} {plural_ru.ru(row['count'],['нарушение','нарушения','нарушений'])} \n"
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=create_keyboard())
    set_step(message, STEP_DEFAULT)

# CAR DETAILS
    
@bot.message_handler(func=lambda message: message.text == keyboard_buttons['details'])
@log_message
def handle_message(message):
    ''' Ask for plate no to send info about it '''
    bot.send_message(chat_id=message.chat.id, text="Введите номерной знак для проверки авто в базе (например `АА0000AA`):", reply_markup=create_keyboard(), parse_mode='Markdown')
    set_step(message, STEP_PLATE_INFO)
    
@bot.message_handler(func=lambda message: get_step(message) == STEP_PLATE_INFO or (getattr(message, 'text')!=None and getattr(message, 'text')[:2] == '/_'))
@log_message
def handle_message(message):
    ''' Send info about specific plate no '''
    if message.text[:2] == '/_':
        number = plate.format_plate(message.text[2:])
    else:
        number = plate.format_plate(message.text)
    reply = ''
    photos = []
    
    if number == False:
        reply = f'Введенный вами номер `{message.text}` не распознан как автомобильный номер. Попробуйте снова:'
    else:
        rows = repo.get_parking_by_plate(number)
        if rows == False:
            reply = f"Записей по номеру `{number}` *не найдено*. Похоже автомобиль не нарушал правил парковки."
        else:
            reply = f"Найденные записи по номеру `{number}`: \n\n"
            for row in rows:
                reply += f" ❗️ {row['description']} (_{row['date_created'].date()}_) \n"
                photos.append(row['photo'])
        set_step(message, STEP_DEFAULT)
    bot.send_message(chat_id=message.chat.id, text=reply, reply_markup=create_keyboard(), parse_mode='Markdown')
    for photo in photos[:4]:
        send_photo(message, photo)

# ADD CAR

@bot.message_handler(func=lambda message: message.text == keyboard_buttons['report'])
@log_message
def handle_message(message):
    ''' Ask for plate no to add new info '''
    bot.send_message(chat_id=message.chat.id, text="Введите номерной знак нарушителя, чтобы добавить его в базу (например `АА0000AA`):", reply_markup=create_keyboard(), parse_mode='Markdown')
    set_step(message, STEP_ADD_PLATE)

@bot.message_handler(func=lambda message: get_step(message) == STEP_ADD_PLATE)
@log_message
def handle_message(message):
    ''' Adding plate no to database, requesting details '''
    number = plate.format_plate(message.text)
    if number == False:
        reply = f'Введенный вами номер `{message.text}` не распознан как автомобильный номер. Попробуйте снова:'
    else:
        try:
            repo.add_parking(car_plate=number, user_id=message.from_user.id, user_username=message.from_user.username, user_first_name=message.from_user.first_name, user_last_name=message.from_user.last_name)
            reply = f'Машина с номерным знаком `{number}` *добавлена* ✅ \n\n' \
                'Теперь вы можете прикрепить *фото* 📷 нарушения или добавить *комментарий* 📝 (такой как _марку и модель_ авто, _условия парковки_, _пожелания_ и прочее):'
            set_step(message, STEP_ADD_DESCRIPTION)
        except Exception as e:
            reply = f'Ошибка при добавлении записи: {e}'
            set_step(message, STEP_DEFAULT)
    bot.send_message(chat_id=message.chat.id, text=reply, reply_markup=create_keyboard(), parse_mode='Markdown')

@bot.message_handler(func=lambda message: get_step(message) == STEP_ADD_DESCRIPTION)
@log_message
def handle_message(message):
    ''' Adding description to plate no '''
    row = repo.get_latest_parking_by_user(message.from_user.id)
    reply = ''
    try:
        repo.edit_parking(row['id'], { 'description': message.text })
        reply = 'Описание к нарушению добавлено ✅'
        if row['photo'] == '':
            reply += '\nТеперь можете прикрепить *фото* 📷 нарушения (_опционально_):'
        else:
            set_step(message, STEP_DEFAULT)
    except:
        reply = f'Что-то пошло не так... Не могу добавить описание. '
        set_step(message, STEP_DEFAULT)
    
    bot.send_message(chat_id=message.chat.id, text=reply, reply_markup=create_keyboard(), parse_mode='Markdown')
    
@bot.message_handler(content_types=['photo'])
def handle_message(message):
    try:
        row = repo.get_latest_parking_by_user(message.from_user.id)
        photo_info = bot.get_file(message.photo[-1].file_id)
        photo = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(BOT_TOKEN, photo_info.file_path))
        with open(os.path.join("upload", f"{row['id']}.jpg"), 'wb') as f:
            f.write(photo.content)
        repo.edit_parking(row['id'], { 'photo': f"{row['id']}.jpg" })
        reply = 'Фото добавлено ✅'
        if row['description'] == '':
            reply += '\nТакже можете добавить *комментарий* 📝 к нарушению (опционально):'
        else:
            set_step(message, STEP_DEFAULT)
    except:
        reply = 'Ошибка при загрузке фото.'
    bot.send_message(chat_id=message.chat.id, text=reply, reply_markup=create_keyboard(), parse_mode='Markdown')

# REST OF COMMANDS

@bot.message_handler(func=lambda _: True)
@log_message
def handle_message(message):
    pass

print("Starting bot...")
if BOT_METHOD == 'webhook':
    # Empty webserver index, return nothing, just http 200
    @app.route('/', methods=['GET', 'HEAD'])
    def index():
        return ''
        
    # Process webhook calls
    @app.route(f"/{BOT_TOKEN}/", methods=['POST'])
    def webhook():
        if flask.request.headers.get('content-type') == 'application/json':
            json_string = flask.request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            flask.abort(403)
            
    bot.remove_webhook()
    time.sleep(0.1)
    bot.set_webhook(url="https://{}:{}/{}/".format(os.environ['WEBHOOK_HOST'], os.environ['WEBHOOK_PORT'], BOT_TOKEN), certificate=open(os.environ['WEBHOOK_SSL_CERT'], 'r'))

    app.run(host=os.environ['WEBHOOK_LISTEN'], 
        port=os.environ['WEBHOOK_PORT'], 
        ssl_context=(os.environ['WEBHOOK_SSL_CERT'], os.environ['WEBHOOK_SSL_PRIV']), 
        debug=True)
else:
    bot.polling()
