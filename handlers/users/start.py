from aiogram.dispatcher.filters import CommandStart
from loader import dp
from aiogram import types
from markups import navigation_markups


@dp.message_handler(CommandStart())
async def start_message(message: types.Message):
    await message.answer("Приветствуем вас в нашем магазине!",
                         reply_markup=navigation_markups.Navigation
                         )