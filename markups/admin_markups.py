from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_nav = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Добавить товар', callback_data='add_product'),
).add(
    InlineKeyboardButton('Удалить товары', callback_data='remove_product')
).add(
    InlineKeyboardButton('Очистить магазин', callback_data='clean_shop')
).add(
    InlineKeyboardButton('Новость для подписчиков', callback_data='news_for_subs')
).add(
    InlineKeyboardButton('Добавить администратора', callback_data='add_admin')
).add(
    InlineKeyboardButton('Удалить администратора', callback_data='remove_admin')
)

confirm_adding_product = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Подтвердить', callback_data='confirm_adding_product'),
    InlineKeyboardButton('Отмена', callback_data='cancel_adding_product')
)

cancel_adding_product = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Отмена', callback_data='cancel_adding_product')
)

notify_about_product = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Уведомить подписчиков', callback_data='notify_about_product'),
    InlineKeyboardButton('Не уведомлять подписчиков', callback_data='do_not_notify_about_product')
)

cancel_adding_admin = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Отмена', callback_data='cancel_adding_admin')
)

confirm_adding_admin = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Подтвердить', callback_data='confirm_adding_admin'),
    InlineKeyboardButton('Отмена', callback_data='cancel_adding_admin')
)


