from aiogram.dispatcher.filters import CommandStart
from loader import dp
from aiogram import types
from markups.navigation_markups import Navigation


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer("Приветствуем вас в нашем магазине!", reply_markup=Navigation)
