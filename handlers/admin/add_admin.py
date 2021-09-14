from aiogram import types
from aiogram.types import CallbackQuery
from states import AddAdmin

from loader import dp, bot, adminsDB


@dp.callback_query_handler(text="add_admin")
async def add_administrator(query: CallbackQuery):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await bot.send_message("Отправьте ссылку на профиль пользователя телеграм")
    await AddAdmin.confirm.set()


# @dp.message_handler(state=AddAdmin.confirm)
# async def confirm_adding_admin(message: types.Message):
#
