from settings import *

def ask_plate_num(message, bot, set_step, create_keyboard):
    ''' Ask for plate no to send info about it '''
    bot.send_message(chat_id=message.chat.id, text="Введите номерной знак для проверки авто в базе (например `АА0000AA`):", reply_markup=create_keyboard(), parse_mode='Markdown')
    set_step(message, STEP_PLATE_INFO)