from aiogram import Dispatcher
import asyncio
from markups.basket_markups import basket_nav
from loader import shopDB


async def send_products(dp: Dispatcher, user_id):
    products = await shopDB.get_products()
    basket = []
    for product in products:
        caption = (
            "<b>{0}</b>\n\n{1}\n\n<b>На складе, ед: </b>{2}\n\n<b>Цена "
            "товара, ₽: </b>{3}".format(
                product['name'], product['description'], product['count'], product['price']))

        basket.append(asyncio.create_task(dp.bot.send_document(
            chat_id=user_id,
            caption=caption,
            document=product['photo'],
            reply_markup=basket_nav
        )))
    await asyncio.gather(*basket)
