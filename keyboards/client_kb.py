from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ReplyKeyboardRemove удаляет клавиатуру полностью, пример показан в client расположение

# создаем кнопки
b1 = KeyboardButton('/Режим_работы')
b2 = KeyboardButton('/Расположение')
b3 = KeyboardButton('/Меню')
# b4 = KeyboardButton ('Поделиться номером', request_contact=True)
# b5 = KeyboardButton ('Отправить где я', request_location=True)

# создаем клавиатуру
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
# resize_keyboard=True уменьшает кнопки
# one_time_keyboard=True скрывает клавиатуру после нажатия на может по кнопке открыть его/ kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

# добавляем кнопки в клавиатуру
kb_client.add(b1).add(b2).add(b3)#.row(b4, b5)
# add добавляем сновой строки, insert добавляем втуже строку если есть место
# kb_client.row(b1, b2, b3)
# row добавляем кнопки в строку


kb_comment = KeyboardButton('Нет')
comment_nou = ReplyKeyboardMarkup(resize_keyboard=True)
comment_nou.add(kb_comment)
