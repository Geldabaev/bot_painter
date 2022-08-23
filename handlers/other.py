from aiogram import types, Dispatcher
# dp импорт потому что тут есть хендлер
from create_bot import dp
import json, string

'''*********************************ОБЩАЯ ЧАСТЬ********************************'''

# фильтар мата
# @dp.message_handler()
async def echo_send(message : types.Message):
    # генератор множеств
    # видео 3, 8 мин.
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('Оскорбления запрещены')
        await  message.delete()


# # пустой хендлер должен быть в самом внизу, чтобы на нем сообщение не останавливались
# @dp.message_handler()
# async def echo_send(message : types.Message):
#     if message.text == 'Привет':
#         await message.answer("И тебе привет!")
#     # # ответ на сообщение
#     # await message.answer(message.text)
#     # # ответ на конкретное собщение
#     # await message.reply(message.text)
#     # отправляет сообщение в личку пользователю
#     # await bot.send_message(message.from_user.id, message.text)


# регистрация хендлеров
def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(echo_send)