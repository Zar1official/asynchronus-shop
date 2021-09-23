from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType
from loader import dp, bot, basketDB
from aiogram import types

from states import Basket


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == "some-invoice-payload-for-our-internal-use":
        await message.answer("Отлично!")


@dp.callback_query_handler(text="cancel_basket", state=Basket.on_buy)
async def cancel_basket(query: CallbackQuery, state: FSMContext):
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await state.reset_state()


@dp.callback_query_handler(text="remove_basket", state=Basket.on_buy)
async def remove_basket(query: CallbackQuery, state: FSMContext):
    await basketDB.remove_basket(query.from_user.id)
    await bot.delete_message(query.message.chat.id, query.message.message_id)
    await bot.send_message(query.from_user.id, "Покупка отменена!")
    await state.reset_state()
