from aiogram import types, Bot
from loader import basketDB, shopDB, adminsDB
import asyncio


async def set_prices(user_id):
    basket_data = await basketDB.get_basket(user_id)
    if basket_data:
        prices = []
        for doc in basket_data:
            prices.append(
                types.LabeledPrice(label=f"{doc['product_name']} - {doc['product_count']} шт.",
                                   amount=doc['product_count'] * doc['product_price'] * 100))
        return prices
    return None


async def decrease_counts(user_id, order_id, user_name, bot: Bot):
    basket_data = await basketDB.get_basket(user_id)
    text_for_notify = "<b>Заказ</b> №{0}\n\n".format(order_id)
    for doc in basket_data:
        product_id = doc['product_id']
        product_count_in_basket = doc['product_count']
        product_name = doc["product_name"]
        product_count = await shopDB.get_product_attr(product_id, "count")
        if product_count == product_count_in_basket:
            await shopDB.remove_product(product_id)
        else:
            await shopDB.edit_product(product_id, "count", product_count - product_count_in_basket)
        text_for_notify += f'{product_name}:{product_count_in_basket}, '
    text_for_notify += "\n\nПользователь @{0}".format(user_name)
    await notify_admins(bot, text_for_notify)


async def notify_admins(bot: Bot, text):
    admins = await adminsDB.get_admins()
    basket = []
    for admin in admins:
        basket.append(asyncio.create_task(bot.send_message(
            admin["user_id"], text
        )))
    await asyncio.gather(*basket)
