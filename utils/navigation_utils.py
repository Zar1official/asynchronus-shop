import asyncio
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import shopDB
import random
import string


async def send_products(bot: Bot, user_id):
    products = await shopDB.get_products()
    if products:
        basket = []
        for product in products:
            caption = (
                "<b>{0}</b>\n\n{1}\n\n<b>На складе, ед: </b>{2}\n\n<b>Цена "
                "товара, ₽: </b>{3}".format(
                    product['name'], product['description'], product['count'], product['price']))

            basket.append(asyncio.create_task(bot.send_document(
                chat_id=user_id,
                caption=caption,
                document=product['photo'],
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("В корзину", callback_data=f"buy_product_{product['_id']}")
                ).add(
                    InlineKeyboardButton("Назад", callback_data="cancel_catalog")
                )
            )))
        await asyncio.gather(*basket)
    else:
        await bot.send_message(user_id, "Товаров нет!", reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Назад", callback_data="cancel_catalog")))


def generate_order_number():
    alphabet = list(string.digits)
    random.shuffle(alphabet)
    result = ""
    for i in alphabet:
        result += i
    return result
