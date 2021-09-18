from aiogram import Dispatcher
import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiogram.utils.exceptions
from loader import subscribeDB, shopDB, adminsDB


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
                InlineKeyboardButton("Удалить товар", callback_data=f"remove_product_{product['_id']}")
            )
        )))
    await asyncio.gather(*basket)


async def send_admins(dp: Dispatcher, user_id):
    admins = await adminsDB.get_admins()
    basket = []
    for admin in admins:
        basket.append(asyncio.create_task(dp.bot.send_message(
            chat_id=user_id,
            text="Имя администратора: {0}"
                 "ID администратора: {1}".format(admin["user_name"], admin["user_id"]),
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("Удалить админа", callback_data=f"remove_admin_{admin['user_id']}")
            )
        )))
    await asyncio.gather(*basket)


def is_user_valid(user_id) -> bool:
    try:
        int(user_id)
    except ValueError:
        return False
    return True


async def is_chat_valid(chat_id, dp: Dispatcher) -> bool:
    try:
        await dp.bot.get_chat(int(chat_id))
    except aiogram.utils.exceptions.ChatNotFound:
        return False
    return True
