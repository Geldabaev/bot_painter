from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db


unique_code={}

'''******************************КЛИЕНТСКАЯ ЧАСТЬ******************************'''
# @dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    global unique_code
    print(message)
    # чтобы кнопка для владельца была ссылкой для пересылки, а для пользователей кнопкой для заказа
    if message.from_user.id != 841457960:
        unique_code['code'] = message.text
    try:
        # отвечаем в личку
        await bot.send_message(message.from_user.id, 'Bienvenue!\nЯ Boutique-bot помогу Вам с выбором изящного приобретения\nот Mlle Mauvais Ton', reply_markup=kb_client)
        # reply_markup=kb_client вызывем клавиатуру
        # удаляем сообщение
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/mllemauvaiston_bot')


# @dp.message_handler(commands=['Режим_работы'])
async def pizza_open_command(message : types.Message):
    await bot.send_message(message.from_user.id, 'Вс-Чт с 9:00 до 20:00, Пт-Сб с 10:00 до 23:00')


# @dp.message_handler(commands=['Расположение'])
async def pizza_place_command(message : types.Message):
    await bot.send_message(message.from_user.id, 'Расположение не указано')
    #reply_markup=ReplyKeyboardRemove() удаляем клавиатуру полностью после нажатия

#@dp.message_handler(commands=['Меню'])
async def pizza_menu_command(message : types.Message):
    await sqlite_db.sql_read(message)


# регистрация хендлеров
def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands=['Режим_работы'])
    dp.register_message_handler(pizza_place_command, commands=['Расположение'])
    dp.register_message_handler(pizza_menu_command, commands=['Меню'])