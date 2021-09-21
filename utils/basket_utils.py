from aiogram import Bot
from markups.basket_markups import basket_nav

from loader import basketDB


async def send_basket(user_id, bot: Bot):
    basket_data = await basketDB.get_basket(user_id)

    if basket_data:
        total_amount = 0
        names = ""
        for doc in basket_data:
            total_amount += doc['product_price'] * doc['product_count']
            names += f"<b>{doc['product_name']}</b>: {doc['product_count']}, "
        await bot.send_message(user_id,
                               names + '\n\nОбщая сумма покупки: {0}'.format(total_amount),
                               reply_markup=basket_nav)
    else:
        await bot.send_message(user_id, "В корзине нет товаров!")
