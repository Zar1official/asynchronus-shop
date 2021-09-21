from aiogram.types import CallbackQuery
from loader import dp, bot, basketDB


@dp.callback_query_handler(text="cancel_basket")
async def cancel_basket(query: CallbackQuery):
    await basketDB.remove_basket(query.from_user.id)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await bot.send_message(query.from_user.id, "Покупка отменена!")
