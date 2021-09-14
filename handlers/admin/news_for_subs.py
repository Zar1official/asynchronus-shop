from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from utils.admin_utils import message_for_subs
from states import MessageSubs
from loader import dp, bot


@dp.callback_query_handler(text="news_for_subs")
async def news_for_subs(query: CallbackQuery):
    await bot.send_message(query.from_user.id, "О чем уведомить подписчиков?")
    await query.answer()
    await MessageSubs.message.set()


@dp.message_handler(state=MessageSubs.message)
async def get_message_subs(message: types.Message, state: FSMContext):
    await message_for_subs(dp, message.text)
    await message.answer("Сообщение успешно отправлено подписчикам!")
    await state.reset_state()

