from aiogram import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import basketDB



async def send_basket(user_id, dp: Dispatcher):
    basket_data = await basketDB.get_basket(user_id)
    total_amount = 0
    names = ""
    for doc in basket_data:
        total_amount += doc['product_price'] * doc['product_count']
        names += f"{doc['product_name']}: {doc['product_count']}, "
    await dp.bot.send_message(user_id, names + '\n\nОбщая сумма покупки: {0}'.format(total_amount),
                              reply_markup=InlineKeyboardMarkup().add(
                                  InlineKeyboardButton("Оформить заказ", callback_data=f"buy")
                              ))
