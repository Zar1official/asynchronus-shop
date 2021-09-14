from aiogram.types import CallbackQuery
from utils.admin_utils import send_products

from loader import dp, shopDB, bot


@dp.callback_query_handler(text="remove_product")
async def send_products_to_remove(query: CallbackQuery):
    await send_products(dp, query.from_user.id)
    await bot.delete_message(query.message.chat.id, query.message.message_id)


@dp.callback_query_handler(lambda call: call.data.startswith("remove_product_"))
async def remove_product(query: CallbackQuery):
    product_id = query.data.split('_')[2]
    await shopDB.remove_product(product_id)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
