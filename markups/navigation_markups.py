from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

Navigation = ReplyKeyboardMarkup(resize_keyboard=True)
Navigation.add(KeyboardButton('Товары 🔥'), KeyboardButton('Рассылка ✉')).add(
               KeyboardButton('Админ 👨'), KeyboardButton('Корзина 🧺'))