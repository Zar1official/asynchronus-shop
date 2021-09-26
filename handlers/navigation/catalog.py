from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from loader import dp, bot, basketDB, shopDB
from states import BuyProduct


@dp.callback_query_handler(lambda call: call.data.startswith("buy_product_"), state=BuyProduct.buy)
async def add_to_basket(query: CallbackQuery):
    product_id = query.data.split("_")[2]
    if not await basketDB.is_in_basket(query.from_user.id, product_id):
        product_price = await shopDB.get_product_attr(product_id, "price")
        product_name = await shopDB.get_product_attr(product_id, "name")
        await basketDB.add_to_basket(query.from_user.id, product_id, product_name, product_price)
        await query.answer("Товар добавлен в корзину.")
    else:
        count_in_basket = await basketDB.get_attr_in_basket(query.from_user.id, product_id, "product_count")
        count_in_store = await shopDB.get_product_attr(product_id, "count")
        if count_in_store > count_in_basket:
            await basketDB.update_in_basket(query.from_user.id, product_id)
            await query.answer(f"Добавлено в корзину {count_in_basket + 1}.")
        else:
            await query.answer("Товар закончился.")


@dp.callback_query_handler(state=BuyProduct.buy)
async def cancel_catalog(query: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await query.answer()


@dp.message_handler(state=BuyProduct.buy)
async def locked_state(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer("Нажмите назад для выхода из каталога товаров!")
