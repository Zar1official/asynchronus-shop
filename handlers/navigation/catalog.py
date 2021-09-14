from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import bot, dp, shopDB


@dp.callback_query_handler(lambda call: call.data.startswith("buy_product"))
async def buy_product(query: CallbackQuery, state: FSMContext):
    await bot.edit_message_caption(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        caption="Выбрано - 0"
    )
    product_id = query.data.split('_')[2]
    await bot.edit_message_reply_markup(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("+", callback_data=f"increase_product_count_{product_id}"),
            InlineKeyboardButton("Оплатить", callback_data=f"pay_product_{product_id}"),
            InlineKeyboardButton("-", callback_data=f"decrease_product_count_{product_id}")
        )
    )
    await state.update_data(chosen=product_id)
    await state.set_state(f"buy_{product_id}")


@dp.callback_query_handler(lambda call: call.data.startswith("increase_product_count"))
async def increase_count(query: CallbackQuery, state: FSMContext):
    data=await state.get_data()
    print(await state.get_state())
    # await state
    # await state.update_data(chosen=chosen)
    # await bot.edit_message_caption(
    #     chat_id=query.message.chat.id,
    #     message_id=query.message.message_id,
    #     caption=f"Выбрано - {chosen}"
    # )
    #
    # await bot.edit_message_reply_markup(
    #     chat_id=query.message.chat.id,
    #     message_id=query.message.message_id,
    #     reply_markup=InlineKeyboardMarkup().add(
    #         InlineKeyboardButton("+", callback_data=f"increase_product_count_{product_id}"),
    #         InlineKeyboardButton("Оплатить", callback_data=f"pay_product_{product_id}"),
    #         InlineKeyboardButton("-", callback_data=f"decrease_product_count_{product_id}")
    #     )
    # )
    pass

# @dp.callback_query_handler(text="decrease_product_count")
# async def decrease_count():
#     pass
