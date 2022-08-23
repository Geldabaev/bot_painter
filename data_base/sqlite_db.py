import random
import sqlite3 as sq
from create_bot import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from create_bot import dp, bot
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import re
import time
from keyboards import comment_nou, kb_client
from handlers.client import unique_code


colich = {}
name_user = {}
phone_users = {}
mail = ''
address = {}
com = {}


# эту функцию надо запускать отдельно (1) bot_telegram.py
# запуск или создание бд
def sql_start():
    global base, cur
    base = sq.connect('pizza_cool.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()

# загрузка в бд (admin.py)
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES(?, ?, ?, ?)', tuple(data.values()))
        # tuple переводит в кортеж
        base.commit()

# Выгрузка данных из бд
async def sql_read(message):
    global photo
    if unique_code:
        for ret in cur.execute('SELECT * FROM menu').fetchall():
            msg = await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Оформить заказ ^^^', callback_data=f'shop {ret[1]}')))
    else:
        for ret in cur.execute('SELECT * FROM menu').fetchall():
            msg = await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Оформить заказ ^^^', url=f'https://t.me/mllemauvaiston_bot?start')))




# машинное состояние
# сработает на оформить заказ тс. shop
class FSMAdvvod(StatesGroup):
    col = State()
    name_buyer = State()
    phone_number = State()
    email = State()
    adress = State()
    comment = State()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('shop '), state=None)
async def cm_start(callback_query: types.CallbackQuery):
    global name_buyer, shop_group
    # находим по имени товара
    shop_group = callback_query.data.replace('shop ', '')
    # ждем следующий
    await FSMAdvvod.col.set()
    await bot.send_message(callback_query.from_user.id, "Введите количество")


@dp.message_handler(state=FSMAdvvod.col)
async def name(message: types.Message):
    global colich
    colich[message.from_user.id] = message.text
    try:
        int(colich[message.from_user.id])

        await FSMAdvvod.next()  # режим ожидания
        await bot.send_message(message.from_user.id, "Введите ваше имя")
    except:
        await bot.send_message(message.from_user.id, "Введите в цифрах")




@dp.message_handler(state=FSMAdvvod.name_buyer)
async def name(message: types.Message):
    global name_user
    name_user[message.from_user.id] = message.text
    await FSMAdvvod.next()  # режим ожидания
    await bot.send_message(message.from_user.id, "Введите номер телефона для обратной связи")


# ловим второй ответ
@dp.message_handler(state=FSMAdvvod.phone_number)
async def load_nom_tel_tur(message: types.Message):
    global phone_users, callback_query
    result = re.match(r'\b\+?[7,8](\s*\d{3}\s*\d{3}\s*\d{2}\s*\d{2})\b', message.text)
    result = bool(result)
    if result:
        phone_users[message.chat.id] = message.text
        await FSMAdvvod.next() # режим ожидания
        await bot.send_message(message.chat.id, "Номер телефона принят")
        await bot.send_message(message.chat.id, "Введите ваш email")

    else:
        await bot.send_message(message.chat.id, "Некорректный номер")


@dp.message_handler(state=FSMAdvvod.email)
async def mail(message: types.Message):
    global mail
    mail = message.text
    # mail[message.from_user.id] = message.text

    await FSMAdvvod.next()  # режим ожидания
    await bot.send_message(message.from_user.id, "Укажите ваш адрес для доставки")


@dp.message_handler(state=FSMAdvvod.adress)
async def adr(message: types.Message):
    global address
    address[message.from_user.id] = message.text
    await FSMAdvvod.next()  # режим ожидания
    await bot.send_message(message.from_user.id, "Напишите комментарии если есть", reply_markup=comment_nou)


@dp.message_handler(state=FSMAdvvod.comment)
async def comment(message: types.Message, state: FSMContext):
    global com
    com[message.from_user.id] = message.text
    await FSMAdvvod.next()  # режим ожидания
    await bot.send_message(message.from_user.id, "Ваш заказ принят", reply_markup=kb_client)
    # перессылаем в закрытую группу
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        if shop_group == ret[1]:
            name_photo = ret[1]
            descrip = ret[2]
            price_photo = ret[-1]
            # пересылаем в группу
            group_id = '-1001627614783'
            await bot.send_message(group_id, "НОВЫЙ ЗАКАЗ!")
            await bot.send_photo(group_id, ret[0], f'{name_photo}\n'
                                                   f'Цена: {price_photo}\n'
                                                   f'Заказчик: {name_user[message.from_user.id]}\n'
                                                   f'Номер телефона: {phone_users[message.from_user.id]}\n'
                                                   f'Почта: {mail}\n'
                                                   f'Адрес: {address[message.from_user.id]}\n'
                                                   f'Комментарий {com[message.from_user.id]}')

    await state.finish()  # выходим из состояний





# # Функция для персылки заказа
# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('shop '))
# async def shop(callback_query: types.CallbackQuery):
#     # находим по имени товара
#     shop_group = callback_query.data.replace('shop ', '')
#     for ret in cur.execute('SELECT * FROM menu').fetchall():
#         if shop_group == ret[1]:
#             name_photo = ret[1]
#             descrip = ret[2]
#             price_photo = ret[-1]
#             # пересылаем в группу
#             group_id = '-1001772207470'
#             await bot.send_photo(group_id, ret[0], f'{name_photo}\nОписание: {descrip}\nЦена {price_photo}')





# Выгрузка и удаление(admin)
async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()