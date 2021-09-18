from aiogram.types import CallbackQuery
from utils.admin_utils import send_admins
from loader import bot, dp


@dp.callback_query_handler(text="remove_admin")
async def remove_administrator(query: CallbackQuery):
    await send_admins(dp, query.from_user.id)
    await bot.delete_message(query.message.chat.id, query.message.message_id)


