from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_db


# когда используется поллинг, чтобы наблюдать
# за ботом
async def o_startup(_):
    print('Бот вышел в онлайн')
    sqlite_db.sql_start()

# импорт хандлеров
from handlers import client, admin, other

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

# внизу потому что хендлер пустой и что бы бот на нем не останавливал
other.register_handlers_other(dp)

#без True нас засыпят смс когда бот выйден онлайн
executor.start_polling(dp, skip_updates=True, on_startup=o_startup)