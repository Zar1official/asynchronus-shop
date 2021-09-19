from aiogram.dispatcher.filters import CommandStart
from loader import dp
from aiogram import types


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer("Привет")
