from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from states import AddAdmin

from loader import dp, bot, adminsDB


@dp.callback_query_handler(text="add_admin")
async def add_administrator(query: CallbackQuery):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await bot.send_message(query.from_user.id, "Отправьте id человека, которого нужно сделать админом."
                           " User-id можно узнать здесь @get_any_telegram_id_bot")
    await AddAdmin.confirm.set()


@dp.message_handler(state=AddAdmin.confirm)
async def confirm_adding_admin(message: types.Message, state: FSMContext):
    await adminsDB.add_admin(int(message.text))
    await message.answer("Добавлен новый администратор!")
    await state.finish()


