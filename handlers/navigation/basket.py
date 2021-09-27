from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType
from loader import dp, bot, basketDB
from aiogram import types
from utils.basket_utils import decrease_counts

from states import Basket


@dp.pre_checkout_query_handler(lambda query: True, state=Basket.on_buy)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT, state=Basket.on_buy)
async def process_pay(message: types.Message, state: FSMContext):
    if message.successful_payment.invoice_payload.__contains__(str(message.from_user.id)):
        await decrease_counts(
            message.from_user.id,
            message.successful_payment.invoice_payload.split("_")[2],
            message.from_user.username,
            bot)
        await basketDB.remove_basket(message.from_user.id)
        await message.answer("Операция проведена успешно! Ожидайте, когда с вами свяжется наш менеджер.")
        await state.reset_state()


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
