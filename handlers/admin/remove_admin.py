from aiogram.types import CallbackQuery
from utils.admin_utils import send_admins
from loader import bot, dp, adminsDB


@dp.callback_query_handler(text="remove_admin")
async def send_administrators(query: CallbackQuery):
    await send_admins(dp, query.from_user.id)
    await bot.delete_message(query.message.chat.id, query.message.message_id)


@dp.callback_query_handler(lambda call: call.data.startswith("remove_admin_"))
async def remove_administrator(query: CallbackQuery):
    user_id = query.data.split('_')[2]
    if not await adminsDB.is_admin(user_id):
        await adminsDB.remove_admin(user_id)
        await bot.delete_message(query.message.chat.id, query.message.message_id)
    else:
        await query.answer("Нельзя удалить самого себя!")
