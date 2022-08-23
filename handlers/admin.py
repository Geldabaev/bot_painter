from aiogram.dispatcher import FSMContext
# FSMContext для указания что дисп используется в мащинном состояние
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3 as sq


ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

# ограничиваем доступ к боту
# Получаем ID текущего модератора
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что хозяин надо???', reply_markup=admin_kb.button_case_admin)
    await message.delete()

# Начало диалога загрузки нового пункта меню
# @dp.message_handler(commands='Загрузить', state=None)
    # state=None еще нет мащинное состояние
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        # FSMAdmin.photo.set() переход в режим мащинного состояния
        await message.reply('Загрузи фото')

# Выход из состояний
# @dp.message_handler(state="*", commands='отмена') # * выход из состояний, где бы он не находился\ из любого состояния
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
# ignore_case=True как бы ненаписал
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        # в каком состояние находится бот
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('ОК')

# Ловим первый ответ и пишем в словарь
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        # next() Ожидание следующего ответа
        await message.reply("Теперь введи название")

# Ловим второй ответ
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply("Введи описание")

# Ловим третий ответ
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply("Теперь укажи цену")

# Ловим последний ответ и используем полученные данные
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        # # вывод в тг боте
        # async with state.proxy() as data:
        #     await message.reply(str(data))

        # загрузка данных в бд
        await sqlite_db.sql_add_command(state)

        await state.finish()
        # выход из машенного состояния

# хендлер для ответа и след для удаления
#2
# если событие 'del ' то запускается это функция
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_queryyy: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_queryyy.data.replace('del ', ''))
    await callback_queryyy.answer(text=f'{callback_queryyy.data.replace("del ", "")} удалена.', show_alert=True)

#1
@dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))




# запуск бд
def sql_start2():
    global base, cur
    base = sq.connect('pizza_cool.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()


@dp.message_handler(commands='Репостнуть')
async def repost_item(message: types.Message):
    # запускаем бд
    sql_start2()
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Репостнуть', callback_data=f'rep {ret[1]}')))
        await bot.send_message(message.from_user.id, "Выберите что хотите репостнуть на канал")


# если событие 'rep ' то запускается это функция
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('rep '))
async def rep_callback_run(callback_queryyy: types.CallbackQuery):
    global shop_group
    shop_group = callback_queryyy.data.replace('rep ', '')
    # перессылаем в закрытую группу
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        if shop_group == ret[1]:
            name_photo = ret[1]
            descrip = ret[2]
            price_photo = ret[-1]
            # пересылаем в канал
            group_id = '-1001523554334'
            await bot.send_photo(group_id, ret[0], f'{name_photo}\n'
                                                   f'Цена: {price_photo}\n', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f'Оформить заказ ^^^', url=f'https://t.me/mllemauvaiston_bot?start')))



#Регистрация хендлеров
def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)