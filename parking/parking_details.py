from settings import *

def ask_plate_num(message, bot, set_step, create_keyboard):
    ''' Ask for plate no to send info about it '''
    bot.send_message(chat_id=message.chat.id, text="Введите номерной знак для проверки авто в базе (например `АА0000AA`):", reply_markup=create_keyboard(), parse_mode='Markdown')
    set_step(message, STEP_PLATE_INFO)
    
def display_plate_details(message, plate, repo, set_step, bot, send_photo, create_keyboard):
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