from aiogram.types import CallbackQuery

from loader import dp, shopDB, bot


@dp.callback_query_handler(text="clean_shop")
async def clean_shop(query: CallbackQuery):
    await shopDB.clean_shop()
    await bot.send_message(query.from_user.id, "Магазин очищен!")
    await query.answer()

#test