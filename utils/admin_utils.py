from aiogram import Dispatcher
import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import subscribeDB, shopDB


async def notify_subs(dp: Dispatcher, data):
    subs = await subscribeDB.get_users()
    document = data['photo_id']
    caption = (
        "Новый товар!\n<b>{0}</b>\n\n{1}\n\n<b>На складе, ед: </b>{2}\n\n<b>Цена "
        "товара, ₽: </b>{3}".format(
            data['name'], data['description'], data['count'], data['price']))
    mailing = []
    for user in subs:
        mailing.append(asyncio.create_task(dp.bot.send_document(
            chat_id=user['_id'],
            document=document,
            caption=caption
        )))
    await asyncio.gather(*mailing)


async def message_for_subs(dp: Dispatcher, message):
    subs = await subscribeDB.get_users()
    mailing = []
    for user in subs:
        mailing.append(asyncio.create_task(dp.bot.send_message(user['_id'], message)))
    await asyncio.gather(*mailing)


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
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("Изменить товар", callback_data=f"edit_product_{product['_id']}")
            ).add(
                InlineKeyboardButton("Удалить товар", callback_data=f"remove_product_{product['_id']}")
            )
        )))
    await asyncio.gather(*basket)


async def send_product_back(dp: Dispatcher, user_id, message_id, product_id):
    product = await shopDB.get_product_data(product_id)
    caption = (
        "<b>{0}</b>\n\n{1}\n\n<b>На складе, ед: </b>{2}\n\n<b>Цена "
        "товара, ₽: </b>{3}".format(
            product['name'], product['description'], product['count'], product['price']))

    await dp.bot.edit_message_caption(
        chat_id=user_id,
        message_id=message_id,
        caption=caption
    )

    await dp.bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=message_id,
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Изменить товар", callback_data=f"edit_product_{product['_id']}")
        ).add(
            InlineKeyboardButton("Удалить товар", callback_data=f"remove_product_{product['_id']}")
        )
    )


async def send_product(dp: Dispatcher, product_id, user_id):
    product = await shopDB.get_product_data(product_id)
    caption = (
        "<b>{0}</b>\n\n{1}\n\n<b>На складе, ед: </b>{2}\n\n<b>Цена "
        "товара, ₽: </b>{3}".format(
            product['name'], product['description'], product['count'], product['price']))

    await dp.bot.send_document(
        chat_id=user_id,
        caption=caption,
        document=product['photo'],
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Изменить товар", callback_data=f"edit_product_{product['_id']}")
        ).add(
            InlineKeyboardButton("Удалить товар", callback_data=f"remove_product_{product['_id']}")
        )
    )
