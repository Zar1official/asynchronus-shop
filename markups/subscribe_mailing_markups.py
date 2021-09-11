from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

sub_mailing = InlineKeyboardMarkup().add(InlineKeyboardButton('Подписаться 🔔', callback_data='sub'))
un_sub_mailing = InlineKeyboardMarkup().add(InlineKeyboardButton('Отписаться 🔇', callback_data='un_sub'))